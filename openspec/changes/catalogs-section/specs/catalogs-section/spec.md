# catalogs-section Specification

## Purpose

Defines the Catálogos section: a responsive grid of three downloadable product catalogs (Día de Muertos, Fiestas Patrias, Navideño) with cover cards, desktop hover preview, and PDF actions. Positioned between Cases and Contact on the single-page site.

## Requirements

### Requirement: Responsive Catalog Grid

The section MUST render 3 catalog cards in a responsive grid on a white background, with `id="catalogos"` and `aria-labelledby` pointing to the section heading.

#### Scenario: Desktop 3-column grid
- GIVEN viewport width ≥1024px
- WHEN the page loads
- THEN 3 cards display side-by-side in equal-width columns with `bg-white` background

#### Scenario: Tablet and mobile breakpoints
- GIVEN viewport between 768–1023px
- THEN 2 cards per row; third wraps to new row
- GIVEN viewport <768px
- THEN each card occupies full width in a single-column stack

#### Scenario: Animate-on-scroll stagger
- GIVEN cards enter the viewport using the existing animate-on-scroll pattern
- THEN card 1 delays 0.1s, card 2 delays 0.2s, card 3 delays 0.3s before entrance animation

### Requirement: Card Content

Each card MUST display: cover WebP image, catalog title, page count, and file size.

#### Scenario: Metadata rendering
- GIVEN the section is rendered
- THEN "Día de Muertos" shows cover, "20 páginas", "10.3 MB"
- AND "Fiestas Patrias" shows cover, "27 páginas", "12.7 MB"
- AND "Navideño" shows cover, "27 páginas", "12.2 MB"

### Requirement: Desktop Hover Preview

On devices supporting `:hover`, cards MUST cross-fade (300ms opacity) from cover to page-1 preview WebP. Touch-only devices SHALL display static covers.

#### Scenario: Hover cross-fade
- GIVEN desktop device with pointer
- WHEN user hovers over a card
- THEN cover cross-fades to page-1 preview WebP over 300ms; on mouse leave, cover returns

#### Scenario: Touch-only and missing preview fallback
- GIVEN a touch-only device OR a missing page-1 preview file
- THEN the card displays only the static cover WebP with no transition and no broken image icon

### Requirement: Download and Preview Actions

Each card MUST have "Descargar PDF" (primary, `download` attribute) and "Ver vista previa" (secondary, `target="_blank"`).

#### Scenario: Download triggers native save
- GIVEN the "Fiestas Patrias" card
- WHEN user clicks "Descargar PDF"
- THEN browser initiates download with filename matching source (URI-encoded via `encodeURI`)

#### Scenario: Preview opens in new tab
- GIVEN any catalog card
- WHEN user clicks "Ver vista previa"
- THEN PDF opens in new tab with `rel="noopener noreferrer"`

#### Scenario: Missing PDF resilience
- GIVEN a PDF file is absent from `public/catalogos/`
- THEN the "Descargar PDF" button is disabled or hidden; no broken link appears

### Requirement: Navigation Link

The Navbar MUST include "Catálogos" between Servicios and Proceso, scrolling smoothly to `#catalogos` and highlighting when in view.

#### Scenario: Smooth scroll on click
- GIVEN "Catálogos" nav link is rendered
- WHEN user clicks it
- THEN page scrolls smoothly to `#catalogos`

#### Scenario: Active state when section in viewport
- GIVEN Catálogos section is scrolled into viewport
- WHEN Navbar active-link detection runs
- THEN "Catálogos" link receives primary-color + underline active styling

### Requirement: Accessibility

The section MUST provide: descriptive `alt` on all images, keyboard-navigable buttons, `prefers-reduced-motion` support, and WCAG AA contrast.

#### Scenario: Screen reader and keyboard
- GIVEN a screen reader or keyboard user
- THEN each image has `alt` like "Portada del catálogo Día de Muertos"
- AND Tab moves focus through buttons; Enter activates focused button

#### Scenario: Reduced motion and contrast
- GIVEN `prefers-reduced-motion: reduce` is active
- THEN no cross-fade transition occurs; cover remains static
- GIVEN body text on white, primary button on white
- THEN contrast meets WCAG AA (text ≥4.5:1, button ≥3:1)

### Requirement: Static Build Generation

All catalog data MUST be statically generated at build time. `astro build` MUST exit 0.

#### Scenario: No client-side fetching
- GIVEN production build HTML output
- THEN all card content (titles, metadata, image refs) is present in static markup; no `fetch()` or XHR populates catalog data

#### Scenario: Build succeeds
- GIVEN `astro build` is executed
- THEN exit code is 0 with zero errors
