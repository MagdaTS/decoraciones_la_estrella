# Design: Catálogos Section

## Technical Approach

Static 3-card catalog grid inserted between Cases and Contact on the single-page site. Cards show cover WebP with desktop hover cross-fade to page-1 preview via inline IIFE (~30 lines). Data lives as a frontmatter const array—no props, no fetch, no runtime overhead. Script extension generates 9 preview WebPs at build-prep time. Follows existing section-wrapper, stagger-delay, and IIFE conventions exactly.

## Architecture Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Data location | `const CATALOGS` in frontmatter | Data is static business content; Astro frontmatter constants are zero-cost at build, no props plumbing needed |
| Hover preview gate | `(hover: hover) and (pointer: fine)` only | Avoids broken hover on touchscreens and hybrid devices; mobile shows static covers per spec |
| Cross-fade | Opacity transition on stacked `<img>` elements | Simpler than canvas or CSS background swap; works with existing `transition-opacity duration-300` Tailwind classes |
| Preview file naming | `{stem}_p1.webp` (underscore separator) | Avoids collision with existing cover `{stem}.webp`; clearly distinguishes page previews from covers |

## Data Model

```ts
interface Catalog {
  slug: string;           // matches PDF stem for path generation
  title: string;          // display name (normalized)
  cover: string;          // /catalogos/previews/{stem}.webp
  previewPages: string[]; // /catalogos/previews/{stem}_p1.webp, _p2, _p3
  pdf: string;            // /catalogos/{filename}.pdf (encodeURI in template)
  pages: number;          // 20 | 27 | 27
  fileSizeMB: number;     // 10.3 | 12.7 | 12.2
  description: string;
}
```

Three entries: `dia-de-muertos`, `fiestas-patrias`, `navideno`. Title displayed: "Día de Muertos", "Fiestas Patrias", "Navideño". File size + page count from proposal metadata.

## Component Structure

`src/components/Catalogs.astro` (~180 lines):

1. **Frontmatter** (`---`): CATALOGS const array (~30 lines). No imports needed—no child components.
2. **Section wrapper** (~8 lines): `<section id="catalogos" class="py-16 md:py-20 bg-white" aria-labelledby="catalogos-title">` — matches Cases and Services pattern.
3. **Header** (~12 lines): badge + `<h2 id="catalogos-title">` + subtitle. `animate-on-scroll` on heading and subtitle. Spanish: badge="Catálogos", title="Nuestros catálogos", subtitle about browsing before requesting.
4. **Grid** (`<div class="catalogs-grid grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">`) (~8 lines wrapping).
5. **Card** (`<article>`) repeated 3× via `CATALOGS.map()` (~30 lines total). Each card: `animate-on-scroll catalog-card group` wrapper, stacked cover+preview images with `absolute inset-0`, metadata (title, pages, MB), two `<a>` buttons styled as primary/secondary.
6. **IIFE script** (~25 lines): queries `.catalog-card`, gates on `(hover: hover) and (pointer: fine)` and `!prefersReducedMotion`, attaches `mouseenter`/`mouseleave` to opacity-toggle preview layer. Uses existing `transition-opacity duration-300`.
7. **No scoped `<style>`** — all rules in global.css.

## CSS Strategy

**Tailwind classes on cards**: `rounded-2xl overflow-hidden shadow-md hover:shadow-xl transition-shadow`, cover image `object-cover w-full h-full`, preview layer `absolute inset-0 opacity-0 transition-opacity duration-300`. Buttons: primary `bg-primary hover:bg-primary-dark text-white font-semibold py-2 px-4 rounded-xl`, secondary `border border-primary/30 text-primary hover:bg-primary/5`.

**Add to `src/styles/global.css`** (after existing Cases rules, line ~136):

```css
/* Catalogs */
.catalogs-grid > article:nth-child(1) .animate-on-scroll.visible { transition-delay: 0.1s; }
.catalogs-grid > article:nth-child(2) .animate-on-scroll.visible { transition-delay: 0.2s; }
.catalogs-grid > article:nth-child(3) .animate-on-scroll.visible { transition-delay: 0.3s; }
```

**Reduced motion**: existing `@media (prefers-reduced-motion: reduce)` block already handles `.animate-on-scroll`. Catalogs IIFE adds its own `matchMedia` check to skip hover transitions.

## JavaScript Strategy

Inline IIFE in Catalogs.astro, `<script>` block after closing `</section>`:

```
1. const prefersReduced = matchMedia('(prefers-reduced-motion: reduce)').matches
2. if (prefersReduced) return — skip entirely
3. const supportsHover = matchMedia('(hover: hover) and (pointer: fine)').matches
4. if (!supportsHover) return — static covers for touch
5. querySelectorAll('.catalog-card') → forEach attach:
   - mouseenter: previewImg.style.opacity = '1'; coverImg.style.opacity = '0'
   - mouseleave: previewImg.style.opacity = '0'; coverImg.style.opacity = '1'
```

~25 lines. No `DOMContentLoaded` wait needed—script runs after card markup is parsed (inline script placement). No event delegation (3 elements).

## Navbar Integration

Insert in `navLinks` array (Navbar.astro, line 3-8):

```js
{ href: '#servicios', label: 'Servicios' },
{ href: '#catalogos', label: 'Catálogos' },  // ← new
{ href: '#proceso', label: 'Proceso' },
```

Active-link detection already works: `updateActiveLink()` scans `section[id]` elements and matches `href` to `#id`. Adding `id="catalogos"` to the section is sufficient—no Navbar JS changes needed.

## Script Extension (`--previews` flag)

Add to `scripts/compress_catalogs.py` (~40 lines):

- New `--previews` arg (argparse, `action='store_true'`)
- New constant: `PREVIEW_PAGE_COUNT = 3`
- New function: `_render_page_previews(src, preview_dir, dry_run) → list[Path]` — reuses existing PDFium render logic (same scale, same WebP encoding as `_make_preview`). Renders pages 0, 1, 2 at `PREVIEW_DPI`, resize to `PREVIEW_MAX_WIDTH`, save as `{stem}_p1.webp`, `{stem}_p2.webp`, `{stem}_p3.webp` into `preview_dir`.
- Idempotency per file: skip if output newer than source (`_is_up_to_date` check per page).
- Hook into `main()`: if `--previews`, iterate `INPUT_FILES`, call `_render_page_previews`, print summary.

Naming convention: `catalogo-dia-de-muertos_p1.webp`, `catalogo-fiestas-patrias_p1.webp`, `Catalogo-navideño_p1.webp` (stems preserved, pages 1-3). Avoids collision with existing cover `catalogo-dia-de-muertos.webp`.

## File Touch List

| File | Action | Lines |
|------|--------|-------|
| `src/components/Catalogs.astro` | Create | ~180 |
| `src/pages/index.astro` | Modify: import + `<Catalogs />` slot between Cases and Contact | +3 |
| `src/components/Navbar.astro` | Modify: add 1 entry to navLinks array | +2 |
| `src/styles/global.css` | Modify: add 3 stagger-delay rules + comment | +4 |
| `scripts/compress_catalogs.py` | Modify: add `--previews` flag + `_render_page_previews()` | +40 |
| `public/catalogos/previews/*_p{1,2,3}.webp` | Create: 9 binary preview files | — |

**Total code**: ~229 lines + 9 binaries.

## PR Split Strategy

Review budget is 400 lines. Split into 2 chained PRs:

**PR 1** (script + assets): extend `compress_catalogs.py` with `--previews`, run once to generate 9 preview WebPs, commit script changes + binaries. ~40 code lines, independent of site, low risk.

**PR 2** (component + integration): create `Catalogs.astro`, integrate into `index.astro`, add Navbar entry, add CSS stagger rules. ~190 code lines, depends on PR 1 for preview images to exist at build time.

## Verification Plan

1. `astro build` exits 0
2. Visual check via Playwright MCP: section renders between Cases and Contact
3. Desktop (1280px): 3 cards side-by-side, hover cross-fades cover→preview, hover-out restores
4. Tablet (768px): 2 cards per row, third wraps
5. Mobile (375px): single column, static covers, no broken hover
6. Tab navigation: focus moves through download/preview buttons
7. "Descargar PDF" click → browser download with correct filename (check network)
8. `prefers-reduced-motion: reduce` → no cross-fade, static covers only
9. Nav "Catálogos" click → smooth scroll to `#catalogos`, link highlights with `text-primary`

## Open Risks

- **Hybrid device hover**: touchscreen laptops may trigger hover unintentionally — mitigated by `(hover: hover) and (pointer: fine)` gate
- **Stagger + IntersectionObserver timing**: both `animate-on-scroll` and stagger delays share the same transition property — verified zero-conflict in existing sections (Services, Cases). Same pattern, no collision.
- **Navideño filename encoding**: source `Catalogo-navideño.pdf` (mixed case, accented). `encodeURI` in `href` handles the accent; filesystem uses the actual bytes. Confirmed existing covers work: `Catalogo-navideño.webp` already exists in previews/.
- **Aspect ratio drift**: covers are 792×612 (1.29:1 landscape). Cards use `aspect-[4/3]` (1.33:1) — near-match, `object-cover` handles the minimal crop.

## Open Questions

- None — all decisions grounded in existing codebase patterns and spec requirements.
