# Proposal: Catálogos Section

## Intent

Potential clients visit the site, see completed projects, and want to browse the printed catalogs before requesting a quote — but the current site has no way to showcase them. Adding a dedicated Catálogos section bridges the gap between "seeing what we've done" (Cases) and "requesting a proposal" (Contact), converting browsing interest into qualified leads.

The business has three professionally designed catalogs (Día de Muertos, Fiestas Patrias, Navideño) already compressed and hosted at `public/catalogos/`. This change makes them visible and downloadable.

## Scope

### In Scope
- New `Catalogs.astro` component: 3-column responsive grid with cover cards, hover preview, download/view buttons
- Integration into `index.astro` between Cases and Contact
- Nav link in `Navbar.astro` (Catálogos, between Servicios and Proceso)
- `--previews` flag on `scripts/compress_catalogs.py` to generate pages 1–3 as WebP previews
- One-time preview image generation (9 files: 3 pages × 3 catalogs)
- 3 stagger-delay CSS rules in `src/styles/global.css`

### Out of Scope
- PDF viewer/reader embedded in the page
- Catalog filtering, searching, or pagination
- Dynamic preview generation (it's a one-time build artifact)
- Analytics/tracking on catalog downloads
- Mobile swipe interaction on preview cards

## Capabilities

### New Capabilities
- `catalogs-section`: Display downloadable product catalogs in a responsive grid with cover cards, hover preview (desktop only), page count + file size metadata, and direct PDF download links.

### Modified Capabilities
- None

## Approach

**Hybrid cover card grid + hover preview + download** (Option F from exploration). A 3-column responsive grid (`1 col mobile → 2 col tablet → 3 col desktop`). Each card shows the cover WebP as background. On desktop hover, a 300ms opacity cross-fade reveals page 1 content WebP as a visual preview (inline IIFE, ~30 lines). No JS for mobile — static cover display only. Two buttons per card: "Descargar PDF" (primary, download attribute) and "Ver vista previa" (secondary, opens PDF in new tab). Section uses `bg-white`, follows existing animate-on-scroll stagger pattern.

**Filename normalization**: Source files use mixed casing (`Catalogo-navideño.pdf` vs lowercase others). Leave source filenames untouched; display normalized names in UI. Decision noted for /sdd-tasks.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `src/components/Catalogs.astro` | New | Catalog grid component (~180 lines) |
| `src/pages/index.astro` | Modified | Import + slot Catalogs between Cases and Contact (+3 lines) |
| `src/components/Navbar.astro` | Modified | Add `#catalogos` nav entry (+2 lines) |
| `src/styles/global.css` | Modified | 3 stagger-delay rules for `.catalogs-grid` (+3 lines) |
| `scripts/compress_catalogs.py` | Modified | Add `--previews` flag (~40 lines) |
| `public/catalogos/previews/` | New files | 9 page preview WebPs (~450 KB total) |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Preview images inflate build output | Medium | `--previews` is one-time manual run, not in CI; previews committed to repo |
| `Catalogo-navideño.pdf` filename mismatch breaks URI | Low | Use `encodeURI` in template; test with `astro build` + visual check |
| Hover preview JS conflicts with scroll animations | Low | IIFE isolated scope; test with Playwright MCP |
| 3 catalogs may not fill grid row on tablet (2-col) | Low | Last card spans full width or shows placeholder; CSS grid handles gracefully |

## Rollback Plan

Remove the `<Catalogs />` import and slot from `index.astro`, remove the nav entry from `Navbar.astro`, delete `Catalogs.astro`. All other files are additive (CSS rules + nav entry have no side effects). No data migration. Rollback is a single commit revert.

## Dependencies

- 9 preview WebPs must exist at `public/catalogos/previews/` before component renders them (generated via `--previews` flag)
- `public/catalogos/*.pdf` must exist (already satisfied)

## Success Criteria

- [ ] `astro build` completes with zero errors
- [ ] Catalogs section renders between Cases and Contact with 3 cards
- [ ] Desktop hover cross-fades cover to page-1 preview (300ms transition)
- [ ] Mobile shows static covers, no broken hover state
- [ ] "Descargar PDF" triggers native download; "Ver vista previa" opens PDF in new tab
- [ ] Nav link scrolls to `#catalogos` and highlights on active section
- [ ] Section respects `prefers-reduced-motion`
