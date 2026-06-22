# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pypdfium2==4.30.1",
#     "img2pdf==0.5.1",
#     "Pillow==11.0.0",
#     "tqdm==4.67.1",
# ]
# ///
"""
Compress PDF catalogs, generate WebP cover previews, and render page previews.

Pipeline per PDF:
  1. Render every page to JPEG (200 DPI) using pypdfium2 (PDFium engine).
  2. Re-encapsulate JPEGs into a new PDF with img2pdf (lossless container swap,
     no double re-encoding of the image stream).
  3. Render page 1 to a WebP preview (150 DPI, max width 800px, quality 80).

Preview mode (--previews):
  Renders pages 1-3 of each input PDF as individual WebP page previews
  ({stem}_p1.webp, {stem}_p2.webp, {stem}_p3.webp) using the same render
  settings as the cover preview. Mutually exclusive with the default
  compression pipeline — PDF compression is skipped entirely in this mode.

Idempotent: if the output exists and is newer than the input, the file is
skipped. Use --dry-run to validate without writing anything.
"""

from __future__ import annotations

import argparse
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pypdfium2 as pdfium
from PIL import Image
import img2pdf

try:
    from tqdm import tqdm
except ImportError:  # pragma: no cover - tqdm is optional
    tqdm = None  # type: ignore[assignment]

# --- Configuration ---------------------------------------------------------

RENDER_DPI = 200
JPEG_QUALITY = 88
PREVIEW_DPI = 150
PREVIEW_MAX_WIDTH = 800
PREVIEW_WEBP_QUALITY = 80
LARGE_PAGE_COUNT_WARN = 200
SAMPLE_PAGE_COUNT = 3  # how many pages to render when estimating benefit
RERENDER_WORTH_THRESHOLD = 0.95  # ratio < this means re-render saves >=5%
PREVIEW_PAGE_COUNT = 3  # how many pages to render for the --previews mode

REPO_ROOT = Path(__file__).resolve().parent.parent
INPUT_DIR = REPO_ROOT / "public" / "material" / "catalogos"
OUTPUT_DIR = REPO_ROOT / "public" / "catalogos"
PREVIEW_DIR = OUTPUT_DIR / "previews"

# Filenames are listed explicitly (not globbed) so the user sees exactly what
# will be processed. The non-ASCII stem is preserved via the Path object.
INPUT_FILES: tuple[Path, ...] = (
    INPUT_DIR / "catalogo-dia-de-muertos.pdf",
    INPUT_DIR / "catalogo-fiestas-patrias.pdf",
    INPUT_DIR / "Catalogo-navideño.pdf",
)


# --- Data classes ----------------------------------------------------------


@dataclass
class CatalogResult:
    src: Path
    dst_pdf: Path
    dst_preview: Path
    pages: int
    width_pt: float
    height_pt: float
    original_bytes: int
    pdf_bytes: int
    preview_bytes: int
    skipped: bool
    strategy: str = ""  # "rerender" | "copy" | "auto-copy" | "auto-rerender" | "skipped"
    error: str | None = None


# --- Helpers ---------------------------------------------------------------


def _human_mb(num_bytes: int) -> float:
    return num_bytes / (1024 * 1024)


def _iter_progress(iterable: Iterable, desc: str, total: int):
    if tqdm is not None:
        return tqdm(iterable, desc=desc, total=total, unit="page")
    print(f"{desc}: {total} pages", file=sys.stderr)
    return iterable


def _is_up_to_date(src: Path, dst: Path) -> bool:
    if not dst.exists():
        return False
    return dst.stat().st_mtime >= src.stat().st_mtime


def _format_table(results: list[CatalogResult]) -> str:
    header = (
        f"{'file':<32} {'orig MB':>9} {'comp MB':>9} {'reduce':>8} "
        f"{'pages':>6} {'cover KB':>9} {'strategy':<14} {'status':<10}"
    )
    sep = "-" * len(header)
    lines = [header, sep]
    for r in results:
        status = "skipped" if r.skipped else ("error" if r.error else "done")
        if r.original_bytes and r.pdf_bytes and not r.skipped:
            reduction = 1 - (r.pdf_bytes / r.original_bytes)
            reduce_str = f"{reduction * 100:>7.1f}%"
        else:
            reduce_str = "    n/a"
        orig_mb = _human_mb(r.original_bytes)
        comp_mb = _human_mb(r.pdf_bytes) if r.pdf_bytes else 0.0
        preview_kb = r.preview_bytes / 1024 if r.preview_bytes else 0.0
        lines.append(
            f"{r.src.stem:<32} {orig_mb:>9.2f} {comp_mb:>9.2f} {reduce_str:>8} "
            f"{r.pages:>6} {preview_kb:>9.1f} {r.strategy:<14} {status:<10}"
        )
    return "\n".join(lines)


# --- Core processing -------------------------------------------------------


def _read_metadata(src: Path) -> tuple[int, float, float]:
    """Return (page_count, width_pt, height_pt) for the first page."""
    pdf = pdfium.PdfDocument(str(src))
    try:
        page = pdf[0]
        # PDF coordinates are 1/72 inch. pypdfium2 returns width/height in points.
        width_pt = float(page.get_width())
        height_pt = float(page.get_height())
        page_count = len(pdf)
    finally:
        pdf.close()
    return page_count, width_pt, height_pt


def _render_page_range(src: Path, jpeg_dir: Path, page_indices: range) -> list[Path]:
    """Render a specific subset of pages (used for dry-run validation)."""
    pdf = pdfium.PdfDocument(str(src))
    scale = RENDER_DPI / 72.0
    paths: list[Path] = []
    try:
        for i in page_indices:
            page = pdf[i]
            pil_image = page.render(scale=scale).to_pil()
            out = jpeg_dir / f"page_{i:05d}.jpg"
            pil_image.save(out, format="JPEG", quality=JPEG_QUALITY, optimize=False)
            paths.append(out)
    finally:
        pdf.close()
    return paths


def _render_pages_to_jpegs(src: Path, jpeg_dir: Path) -> list[Path]:
    """Render every page of src to a JPEG file under jpeg_dir.

    Using disk (not RAM) keeps memory bounded for very large catalogs.
    Returns the list of JPEG paths in page order.
    """
    pdf = pdfium.PdfDocument(str(src))
    page_count = len(pdf)
    jpeg_paths: list[Path] = []
    scale = RENDER_DPI / 72.0  # PDF default is 72 DPI.
    try:
        for i in _iter_progress(range(page_count), f"render {src.name}", page_count):
            try:
                page = pdf[i]
            except Exception as exc:  # noqa: BLE001
                raise RuntimeError(
                    f"failed to load page {i} of {src.name}: {exc}"
                ) from exc
            pil_image = page.render(scale=scale).to_pil()
            out = jpeg_dir / f"page_{i:05d}.jpg"
            # optimize=False keeps render fast; the JPEG stream is just a
            # payload for the new PDF, it won't be re-decoded.
            pil_image.save(out, format="JPEG", quality=JPEG_QUALITY, optimize=False)
            jpeg_paths.append(out)
    finally:
        pdf.close()
    return jpeg_paths


def _make_preview(src: Path, dst: Path, *, dry_run: bool) -> int:
    """Render page 1 to a WebP preview, return bytes written (0 on dry-run)."""
    if _is_up_to_date(src, dst):
        return dst.stat().st_size
    pdf = pdfium.PdfDocument(str(src))
    try:
        page = pdf[0]
        scale = PREVIEW_DPI / 72.0
        pil_image = page.render(scale=scale).to_pil()
    finally:
        pdf.close()
    if pil_image.width > PREVIEW_MAX_WIDTH:
        ratio = PREVIEW_MAX_WIDTH / pil_image.width
        new_size = (PREVIEW_MAX_WIDTH, int(pil_image.height * ratio))
        pil_image = pil_image.resize(new_size, Image.LANCZOS)
    pil_image = pil_image.convert("RGB")  # WebP encoder prefers RGB.
    if dry_run:
        return 0
    dst.parent.mkdir(parents=True, exist_ok=True)
    pil_image.save(dst, format="WEBP", quality=PREVIEW_WEBP_QUALITY, method=4)
    return dst.stat().st_size


def _render_page_previews(
    src: Path, preview_dir: Path, *, dry_run: bool, page_count: int = PREVIEW_PAGE_COUNT
) -> int:
    """Render pages 0..page_count-1 as WebP previews.

    Uses the same render settings as _make_preview (PREVIEW_DPI, PREVIEW_MAX_WIDTH,
    WebP quality). Output naming: {stem}_p{1..page_count}.webp.

    Idempotent: skips any page whose output is newer than the source PDF.
    Returns the count of files written (0 on dry-run).
    """
    files_written = 0
    pdf = pdfium.PdfDocument(str(src))
    try:
        for page_num in range(page_count):
            dst = preview_dir / f"{src.stem}_p{page_num + 1}.webp"
            if _is_up_to_date(src, dst):
                continue
            if dry_run:
                files_written += 1
                continue
            page = pdf[page_num]
            scale = PREVIEW_DPI / 72.0
            pil_image = page.render(scale=scale).to_pil()
            if pil_image.width > PREVIEW_MAX_WIDTH:
                ratio = PREVIEW_MAX_WIDTH / pil_image.width
                new_size = (PREVIEW_MAX_WIDTH, int(pil_image.height * ratio))
                pil_image = pil_image.resize(new_size, Image.LANCZOS)
            pil_image = pil_image.convert("RGB")
            preview_dir.mkdir(parents=True, exist_ok=True)
            pil_image.save(dst, format="WEBP", quality=PREVIEW_WEBP_QUALITY, method=4)
            files_written += 1
    finally:
        pdf.close()
    return files_written


def _build_pdf(jpeg_paths: list[Path], page_width_pt: float, page_height_pt: float) -> bytes:
    """Wrap JPEG files into a fresh PDF using img2pdf, preserving aspect ratio.

    img2pdf is purpose-built for this: it reads each JPEG's native dimensions
    and emits a PDF where the JPEG stream is stored verbatim (no re-encode).
    Page size honors the original (passed as points), so aspect ratio matches.
    """
    layout = img2pdf.get_layout_fun(
        pagesize=(page_width_pt, page_height_pt),
        fit=img2pdf.FitMode.into,  # shrink-to-fit, never upscale
    )
    return img2pdf.convert(
        [str(p) for p in jpeg_paths],
        layout_fun=layout,
        producer="compress_catalogs.py",
    )


def _estimate_render_benefit(
    src: Path, page_count: int, sample_indices: range
) -> tuple[int, int, bool]:
    """Render a few pages and project whether re-encoding saves bytes.

    Returns (sample_pdf_bytes, sample_orig_bytes, worth_rerendering).
    `worth_rerendering` is True when projected output is meaningfully smaller
    than the source. We use a 5% threshold: anything less is treated as a wash
    and the original is copied verbatim (faster, lossless, identical visual).
    """
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        jpegs = _render_page_range(src, tmp, sample_indices)
        # Use the first sample's dimensions as a representative page size.
        # (All pages of a single catalog share the same layout.)
        _, width_pt, height_pt = _read_metadata(src)
        pdf_bytes = len(_build_pdf(jpegs, width_pt, height_pt))
    # Estimate source bytes attributed to those sample pages: proportional.
    sample_orig_bytes = (src.stat().st_size / page_count) * len(jpegs)
    if sample_orig_bytes == 0:
        return pdf_bytes, sample_orig_bytes, False
    ratio = pdf_bytes / sample_orig_bytes
    return pdf_bytes, int(sample_orig_bytes), ratio < 0.95  # <5% savings = wash


def process(
    src: Path,
    output_dir: Path,
    preview_dir: Path,
    *,
    dry_run: bool,
    strategy: str = "auto",
) -> CatalogResult:
    """Compress one catalog PDF according to `strategy`.

    strategy:
      "auto"        - sample a few pages, re-render only if it saves >=5%.
      "force-render"- always re-render all pages to JPEG@200DPI and re-encapsulate.
      "copy"        - copy the source PDF verbatim, no re-encoding.
    """
    original_bytes = src.stat().st_size
    dst_pdf = output_dir / src.name
    dst_preview = preview_dir / f"{src.stem}.webp"

    try:
        page_count, width_pt, height_pt = _read_metadata(src)
    except Exception as exc:  # noqa: BLE001
        return CatalogResult(
            src=src,
            dst_pdf=dst_pdf,
            dst_preview=dst_preview,
            pages=0,
            width_pt=0.0,
            height_pt=0.0,
            original_bytes=original_bytes,
            pdf_bytes=0,
            preview_bytes=0,
            skipped=False,
            error=f"metadata read failed: {exc}",
        )

    if page_count > LARGE_PAGE_COUNT_WARN:
        print(
            f"WARNING: {src.name} has {page_count} pages (> {LARGE_PAGE_COUNT_WARN}). "
            "Rendering and PDF rebuild will take time; press Ctrl-C to abort if needed.",
            file=sys.stderr,
        )

    if _is_up_to_date(src, dst_pdf) and _is_up_to_date(src, dst_preview):
        return CatalogResult(
            src=src,
            dst_pdf=dst_pdf,
            dst_preview=dst_preview,
            pages=page_count,
            width_pt=width_pt,
            height_pt=height_pt,
            original_bytes=original_bytes,
            pdf_bytes=dst_pdf.stat().st_size,
            preview_bytes=dst_preview.stat().st_size,
            skipped=True,
            strategy="skipped",
        )

    # Resolve effective strategy for this file.
    effective = strategy
    if strategy == "auto":
        sample_n = min(SAMPLE_PAGE_COUNT, page_count)
        sample_idx = range(sample_n)
        sample_pdf, sample_orig, worth = _estimate_render_benefit(
            src, page_count, sample_idx
        )
        if sample_orig > 0:
            ratio = sample_pdf / sample_orig
            print(
                f"  auto: {sample_n}-page sample -> {sample_pdf/1024:.0f} KB vs "
                f"{sample_orig/1024:.0f} KB (ratio {ratio:.2f}x) "
                f"-> {'rerender' if worth else 'copy'}",
                file=sys.stderr,
            )
        effective = "force-render" if worth else "copy"

    if effective == "copy":
        # Lossless path: copy the original bytes verbatim. Fast and lossless.
        if not dry_run:
            output_dir.mkdir(parents=True, exist_ok=True)
            dst_pdf.write_bytes(src.read_bytes())
        pdf_bytes = 0 if dry_run else dst_pdf.stat().st_size
        preview_bytes = 0 if dry_run else _make_preview(
            src, dst_preview, dry_run=dry_run
        )
        return CatalogResult(
            src=src,
            dst_pdf=dst_pdf,
            dst_preview=dst_preview,
            pages=page_count,
            width_pt=width_pt,
            height_pt=height_pt,
            original_bytes=original_bytes,
            pdf_bytes=pdf_bytes,
            preview_bytes=preview_bytes,
            skipped=False,
            strategy="auto-copy" if strategy == "auto" else "copy",
        )

    # effective == "force-render" (or auto-decided to rerender)
    if dry_run:
        # Touch the codepath with page 0 only; skip the expensive full render.
        with tempfile.TemporaryDirectory() as tmp:
            _render_page_range(src, Path(tmp), range(1))
        pdf_bytes = 0
    else:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            jpeg_paths = _render_pages_to_jpegs(src, tmp_dir)
            pdf_bytes_obj = _build_pdf(jpeg_paths, width_pt, height_pt)
            output_dir.mkdir(parents=True, exist_ok=True)
            dst_pdf.write_bytes(pdf_bytes_obj)
            pdf_bytes = dst_pdf.stat().st_size

    preview_bytes = 0 if dry_run else _make_preview(
        src, dst_preview, dry_run=dry_run
    )

    return CatalogResult(
        src=src,
        dst_pdf=dst_pdf,
        dst_preview=dst_preview,
        pages=page_count,
        width_pt=width_pt,
        height_pt=height_pt,
        original_bytes=original_bytes,
        pdf_bytes=pdf_bytes,
        preview_bytes=preview_bytes,
        skipped=False,
        strategy="auto-rerender" if strategy == "auto" else "force-render",
    )


# --- CLI -------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run", action="store_true", help="do not write any output files"
    )
    parser.add_argument(
        "--input-dir", type=Path, default=INPUT_DIR, help="override input directory"
    )
    parser.add_argument(
        "--strategy",
        choices=["auto", "force-render", "copy"],
        default="auto",
        help=(
            "auto: sample first 3 pages and re-render only if it saves >=5%%. "
            "force-render: always re-render all pages at 200 DPI. "
            "copy: copy source PDF verbatim, no re-encoding."
        ),
    )
    parser.add_argument(
        "--previews",
        action="store_true",
        help=(
            "generate page preview WebPs for each input PDF (pages 1-3, "
            "same render settings as cover previews). "
            "Mutually exclusive with the default compression pipeline -- "
            "when set, PDF compression is skipped entirely."
        ),
    )
    args = parser.parse_args(argv)

    input_dir: Path = args.input_dir
    files = tuple(input_dir / f.name for f in INPUT_FILES)

    missing = [f for f in files if not f.exists()]
    if missing:
        for m in missing:
            print(f"ERROR: missing input: {m}", file=sys.stderr)
        return 1

    # --- Preview mode (mutually exclusive with compression) ----------------
    if args.previews:
        t0 = time.monotonic()

        header = (
            f"{'file':<32} {'page 1 KB':>10} {'page 2 KB':>10} "
            f"{'page 3 KB':>10} {'total KB':>10} {'status':<12}"
        )
        sep = "-" * len(header)
        print(header)
        print(sep)

        for src in files:
            written = _render_page_previews(
                src, PREVIEW_DIR, dry_run=args.dry_run
            )
            # Collect per-page sizes (0 for skipped pages in dry-run, or files
            # that haven't been generated yet).
            sizes: list[int] = []
            for page_num in range(1, PREVIEW_PAGE_COUNT + 1):
                dst = PREVIEW_DIR / f"{src.stem}_p{page_num}.webp"
                if dst.exists():
                    sizes.append(dst.stat().st_size)
                else:
                    sizes.append(0)

            total_kb = sum(sizes) / 1024
            status = "dry-run" if args.dry_run else (
                "skipped" if written == 0 else "written"
            )
            print(
                f"{src.stem:<32} "
                f"{sizes[0] / 1024:>10.1f} "
                f"{sizes[1] / 1024:>10.1f} "
                f"{sizes[2] / 1024:>10.1f} "
                f"{total_kb:>10.1f} "
                f"{status:<12}"
            )

        elapsed = time.monotonic() - t0
        print(f"\nElapsed: {elapsed:.1f}s  (dry-run={args.dry_run})")
        return 0

    # --- Default compression pipeline ---------------------------------------
    results: list[CatalogResult] = []
    t0 = time.monotonic()
    for src in files:
        print(f"\n>>> {src.name}", file=sys.stderr)
        results.append(
            process(
                src,
                OUTPUT_DIR,
                PREVIEW_DIR,
                dry_run=args.dry_run,
                strategy=args.strategy,
            )
        )
    elapsed = time.monotonic() - t0

    print()
    print(_format_table(results))
    print(
        f"\nElapsed: {elapsed:.1f}s  (dry-run={args.dry_run}, strategy={args.strategy})"
    )
    return 0 if all(r.error is None for r in results) else 2


if __name__ == "__main__":
    raise SystemExit(main())
