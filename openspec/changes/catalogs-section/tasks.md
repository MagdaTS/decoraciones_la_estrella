# Tasks: Catálogos Section

## Summary
- **Total tasks**: 10 (3 PR1 + 7 PR2)
- **Total estimated lines**: ~229 code + 9 binaries
- **PR split**: 2 PRs (PR 1: ~40 lines + 9 binaries, PR 2: ~190 lines)
- **Chain strategy**: `stacked-to-main` (proposed — pending user confirmation)
- **Critical path**: T1.1 → T1.2 → T1.3 → [merge to main] → T2.1 → T2.2 + (T2.3\|T2.4\|T2.5) → T2.6 → T2.7

Decision needed before apply: No
Chained PRs recommended: Yes
Chain strategy: stacked-to-main (proposed)
400-line budget risk: Low

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Script extension + preview generation | PR 1 (main) | ~40 code lines + 9 binaries. Isolated from site — zero site risk |
| 2 | Component + integration + verification | PR 2 (main) | ~190 code lines. Depends on PR 1 assets being on main |

---

## PR 1: Script Extension & Preview Generation (~40 lines + 9 binaries)

**Base**: `main`. **Merge to**: `main`. Zero site risk — script changes only.

### T1.1 — Add `--previews` flag to compress_catalogs.py
**Est**: 15 lines. **Dep**: —

- [x] Add `--previews` argparse flag (`action="store_true"`)
- [x] Add `PREVIEW_PAGE_COUNT = 3` constant
- [x] Add `_render_page_previews(src, preview_dir, dry_run)` reusing existing PDFium render logic (same `PREVIEW_DPI`, `PREVIEW_MAX_WIDTH`, WebP encoding as `_make_preview`)
- [x] Output naming: `{stem}_p1.webp`, `{stem}_p2.webp`, `{stem}_p3.webp` in `public/catalogos/previews/`
- [x] Idempotency per page: skip if output newer than source (`_is_up_to_date`)
- [x] `--previews` works combined with `--dry-run` (validates without writing)
- [x] CLI help text documents the flag
- [x] Hook into `main()`: if `--previews`, iterate `INPUT_FILES`, call `_render_page_previews`, print summary
- [x] Verify: `python scripts/compress_catalogs.py --previews --dry-run` exits 0

### T1.2 — Generate 9 preview WebPs
**Est**: 0 lines (binary gen). **Dep**: T1.1

- [x] Run `python scripts/compress_catalogs.py --previews` — produces 9 files in `public/catalogos/previews/`
- [x] Each WebP: ~50–150 KB, 3 pages × 3 catalogs (`dia-de-muertos`, `fiestas-patrias`, `navideno`)
- [x] Existing cover files NOT regenerated (idempotent)
- [x] `git add public/catalogos/previews/` + commit with message: `feat(catalogs): add 9 page preview WebPs`

### T1.3 — Verify PR 1 build health
**Est**: 0 lines. **Dep**: T1.2

- [x] `astro build` exits 0 (sanity — site unchanged)
- [x] Spot-check: browser loads `public/catalogos/previews/catalogo-dia-de-muertos_p1.webp`

---

## PR 2: Component & Integration (~190 lines)

**Base**: `main`. **Merge to**: `main`. Expects preview WebPs already on main.

### T2.1 — Create `Catalogs.astro`
**Est**: 135 lines. **Dep**: T2.0 (PR1 merged)

- [ ] Frontmatter: `CATALOGS` const array with 3 entries (slug, title, cover, previewPages, pdf, pages, fileSizeMB, description)
- [ ] `Catalog` documented as TS-style interface comment
- [ ] Section: `<section id="catalogos" class="py-16 md:py-20 bg-white" aria-labelledby="catalogos-title">`
- [ ] Header: badge + `<h2 id="catalogos-title">` + subtitle, `animate-on-scroll` on h2
- [ ] Grid: `<div class="catalogs-grid grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">`
- [ ] Card via `.map()`: `<article class="catalog-card group animate-on-scroll">` with stacked absolute cover+preview `<img>`
- [ ] Cover img: `src={c.cover}`, alt like `"Portada del catálogo Día de Muertos"`
- [ ] Preview img: `src={c.previewPages[0]}`, `class="absolute inset-0 opacity-0 transition-opacity duration-300"`
- [ ] Metadata: title, `"{c.pages} páginas"` badge, `"{c.fileSizeMB} MB"` badge
- [ ] Two `<a>` buttons: "Descargar PDF" (primary, `download`, `encodeURI` on href) and "Ver vista previa" (secondary, `target="_blank" rel="noopener noreferrer"`)
- [ ] `encodeURI()` applied to PDF href for `Catalogo-navideño.pdf`

### T2.2 — Add hover preview IIFE script
**Est**: 25 lines. **Dep**: T2.1

- [ ] Inline `<script>` after `</section>`, wrapped in IIFE
- [ ] Gate 1: `matchMedia('(prefers-reduced-motion: reduce)').matches` → skip
- [ ] Gate 2: `matchMedia('(hover: hover) and (pointer: fine)').matches` → if false, skip
- [ ] `querySelectorAll('.catalog-card')` → forEach: `mouseenter` sets preview opacity 1, cover opacity 0; `mouseleave` reverses
- [ ] Uses existing `transition-opacity duration-300` Tailwind classes (no custom CSS)
- [ ] Graceful: if preview img 404, cover remains visible (no broken-image icon)

### T2.3 — Add stagger-delay CSS rules
**Est**: 4 lines. **Dep**: —

- [ ] Append after Cases rules in `src/styles/global.css`:
  ```css
  /* Catalogs */
  .catalogs-grid > article:nth-child(1) .animate-on-scroll.visible { transition-delay: 0.1s; }
  .catalogs-grid > article:nth-child(2) .animate-on-scroll.visible { transition-delay: 0.2s; }
  .catalogs-grid > article:nth-child(3) .animate-on-scroll.visible { transition-delay: 0.3s; }
  ```

### T2.4 — Integrate into `index.astro`
**Est**: 3 lines. **Dep**: T2.1, T2.3

- [ ] `import Catalogs from '../components/Catalogs.astro';` (preserve import order)
- [ ] `<Catalogs />` between `<Cases />` and `<Contact />`
- [ ] No other changes

### T2.5 — Add Navbar entry
**Est**: 2 lines. **Dep**: T2.1

- [ ] Add `{ href: '#catalogos', label: 'Catálogos' }` to `navLinks` array between Servicios and Proceso
- [ ] Active-link detection works via existing `id="catalogos"` section — no JS changes needed

### T2.6 — Visual verification
**Est**: 0 lines. **Dep**: T2.4, T2.5

- [ ] `astro build` exits 0
- [ ] Desktop (1280px): 3 cards side-by-side, hover cross-fades cover→preview, hover-out restores
- [ ] Tablet (768px): 2 cards per row, third wraps, hover still works
- [ ] Mobile (375px): single column, static covers (no broken hover)
- [ ] Tab navigation focuses all 6 buttons; Enter triggers download/new-tab
- [ ] `prefers-reduced-motion: reduce` → no cross-fade, static covers
- [ ] Nav "Catálogos" click smooth-scrolls to `#catalogos`, link highlights
- [ ] Screenshots saved to `openspec/changes/catalogs-section/verify/`

### T2.7 — Update task status
**Est**: 0 lines. **Dep**: T2.6

- [ ] All checkboxes marked `[x]`
- [ ] Notes added: lines added, file count, observations
- [ ] Ready for `/sdd-verify`

---

## Dependency Graph

```
T1.1 → T1.2 → T1.3 → [merge to main] ─┬→ T2.1 ──→ T2.2 ─→ T2.6 → T2.7
                                        │    ↕ (parallel)  ↑
                                        ├→ T2.3 ──────────┘
                                        ├→ T2.4 ──────────┘
                                        └→ T2.5 ──────────┘
```

T2.3, T2.4, T2.5 are independent of T2.1's body and can be done in any order before T2.6.

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | ~229 code + 9 binaries |
| 400-line budget risk | Low (PR1 ~40, PR2 ~190 — both well under 400) |
| Chained PRs recommended | Yes — isolates asset-generation risk in PR1 |
| Suggested split | PR 1 (script + binaries) → PR 2 (component + integration) |
| Delivery strategy | auto-chain |
| Chain strategy | stacked-to-main (each PR merges to main in order) |

## Decision needed before apply: chain strategy

The delivery_strategy is `auto-chain`, so execution can proceed automatically. However, the specific **chain strategy** is not yet confirmed by the user. Proposing `stacked-to-main` (simplest for a 2-PR change in a single repo):
- **PR 1** merges to `main` — script extension + 9 binary preview files
- **PR 2** merges to `main` — component + integration (expects previews already on main)

If the user prefers **feature-branch-chain** instead: PR #1 targets a `catalogs-section` tracker branch, PR #2 targets PR #1's branch. The tracker merges to main only when both PRs are complete. This adds branch complexity without benefit for a 2-PR additive change.

**Recommendation**: `stacked-to-main`. Surface to user for confirmation before sdd-apply begins.
