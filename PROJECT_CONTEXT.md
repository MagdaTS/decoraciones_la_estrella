# 🧠 Contexto del Proyecto — Decoraciones La Estrella

> **Última actualización:** 2026-06-20  
> **Para agentes:** Lee este archivo ANTES de tocar cualquier componente.

## 0. Sobre la Empresa (NEGOCIO REAL)

**Nombre:** Decoraciones La Estrella
**Core:** Fabricación, montaje y mantenimiento de adornos temáticos para espacios comerciales y públicos.
**Trabajan TODO EL AÑO:** Desde Reyes Magos, Día de Muertos, Día de la Independencia, hasta Navidad.
**Clientes:** Centros comerciales + Gobiernos municipales (plazas, explanadas, espacios públicos).
**Diferenciador clave:** Servicio llave en mano que incluye desmontaje, embalaje profesional y organización en bodega. Los clientes celebran especialmente esta organización post-servicio.
**NO son:** Agencia de eventos genérica, productora de escenografías fotográficas, ni solo fabricantes sueltos.

**Los 4 servicios reales:**
1. Centros Comerciales (malls, plazas comerciales)
2. Plazas y Espacios Públicos (gobiernos municipales)
3. Temporadas y Festividades (todo el año, no solo navidad)
4. Servicio Llave en Mano (diseño → fabricación → montaje → mantenimiento → desmontaje → embalaje → bodega)

---

## 1. Stack y Decisiones Clave

| Tecnología | Versión | Nota Importante |
|-----------|---------|-----------------|
| Astro | v5.7.3 | `output: 'static'` — HTML puro, no SSR |
| Tailwind CSS | v4.1.15 | **NO usa** `tailwind.config.js`. Config en `@theme` dentro de `global.css` |
| Plugin Tailwind | `@tailwindcss/vite` | `@astrojs/tailwind` es INCOMPATIBLE con v4 |
| Fonts | Google Fonts CDN | Inter (body) + Montserrat (headings) |
| Icons | FontAwesome 6.5.1 | CDN con async loading |
| Imágenes | Pexels CDN | Todas externas, excepto Logo.jpg |

**Build:** `npm run build` → genera carpeta `dist/` con HTML estático listo para VPS.

---

## 2. Estructura de Componentes

```
src/components/
├── SkipNav.astro       # Accesibilidad — "Saltar al contenido"
├── Navbar.astro        # Sticky nav + mobile hamburger menu (JS inline)
├── Hero.astro          # Full viewport + background image + CTAs + scroll indicator
├── Services.astro      # 4 tarjetas de servicios REALES (grid 2 cols): Centros Comerciales, Plazas/Espacios Públicos, Temporadas/Festividades, Servicio Llave en Mano
├── Gallery.astro       # 8 imágenes masonry (3 cols desktop, primer item 2x2)
├── Benefits.astro      # 4 tarjetas de beneficios (grid 4 cols desktop)
├── BeforeAfter.astro   # Slider interactivo antes/después (JS inline)
├── Process.astro       # Timeline vertical de 5 pasos
├── Cases.astro         # 3 tarjetas de casos de éxito (grid 3 cols)
├── WhyUs.astro         # 4 diferenciadores (grid 4 cols)
├── Contact.astro       # Formulario + info de contacto (JS inline)
├── Footer.astro        # 4-column footer
├── WhatsAppFloat.astro # Botón flotante WhatsApp (JS inline)
└── ScrollTop.astro     # Botón volver arriba (JS inline)
```

---

## 3. Convenciones ESTRICTAS

### CSS / Tailwind v4
- **NUNCA** crees `tailwind.config.js` — no funciona con v4.
- Configura colores en `src/styles/global.css` dentro del bloque `@theme {}`.
- Usa las variables del theme: `bg-primary`, `text-foreground`, `text-muted-foreground`, etc.
- Colores custom manuales (si no están en theme): usa hex directo o CSS custom props.

### Patrón de Secciones
Todas las secciones siguen este patrón:
```astro
<section id="nombre-seccion" class="py-20 md:py-28 bg-white" aria-labelledby="titulo-id">
  <div class="max-w-[1200px] mx-auto px-6">
    <!-- Section Header -->
    <div class="text-center mb-16 max-w-[700px] mx-auto">
      <span class="inline-block text-xs font-semibold uppercase tracking-[0.15em] text-primary mb-2 px-3 py-1 bg-primary/10 rounded-full">
        Tag
      </span>
      <h2 id="titulo-id" class="animate-on-scroll text-3xl md:text-4xl font-bold text-foreground mb-4">
        Título
      </h2>
      <p class="animate-on-scroll text-lg text-muted-foreground leading-relaxed">
        Subtítulo
      </p>
    </div>
    <!-- Grid / Content -->
  </div>
</section>
```

### Animaciones
- Para animar elementos al hacer scroll, añade la clase `animate-on-scroll`.
- El JS está en `Layout.astro` — **no lo copies** a componentes.
- Los delays stagger se manejan en `global.css` (selectores `nth-child`).
- Hero tiene sus propios keyframes scoped (fadeInUp, bounce).

### JavaScript
- **NO uses** `<script src="...">` — todo es inline dentro de cada componente `.astro`.
- Cada componente que necesita JS lo encapsula en: `<script>(function() { ... })();</script>`.
- Esto evita conflictos de scope y Astro lo minifica automáticamente.

---

## 4. Paleta de Colores

| Nombre | Hex | Tailwind |
|--------|-----|----------|
| Dorado (primary) | `#D9BC4A` | `bg-primary`, `text-primary` |
| Dorado oscuro | `#C99A18` | `bg-primary-dark` |
| Azul tecnología | `#14A4CC` | `text-[#14A4CC]` (no en theme) |
| Magenta | `#E5007D` | `bg-magenta` |
| Verde | `#39B257` | `bg-green` |
| Rojo | `#F31212` | `bg-red` |
| Amarillo | `#F0C400` | `bg-yellow` |
| Negro | `#111111` | `bg-[#111111]`, `text-foreground` |
| Blanco | `#FFFFFF` | `bg-white` |

---

## 5. Componentes Reutilizables

### Botón Primario
```html
<a href="#contacto" class="bg-primary hover:bg-primary-dark text-foreground font-semibold py-4 px-8 rounded-xl transition-all duration-300 shadow-lg hover:shadow-xl hover:-translate-y-1">
  Texto
</a>
```

### Tarjeta (Cards)
```html
<article class="animate-on-scroll bg-white rounded-2xl p-8 shadow-md hover:shadow-xl transition-all duration-300 hover:-translate-y-1 border border-black/5">
  <!-- contenido -->
</article>
```

### Section Header
Copiar el patrón del punto 3. Siempre con tag dorado + título + subtítulo.

---

## 6. Cosas que ROMPERÍAN el Build

| ❌ No hagas esto | ✅ En su lugar |
|------------------|---------------|
| `tailwind.config.js` | Editar `@theme {}` en `global.css` |
| `@astrojs/tailwind` | Usar `@tailwindcss/vite` (ya configurado) |
| `import` de scripts externos | Inline `<script>` dentro del componente |
| `class="animate-on-scroll"` sin definición | Ya está en `global.css`, solo úsala |
| Modificar `dist/` directamente | Siempre editar `src/` y hacer `npm run build` |

---

## 7. Comandos Útiles

```bash
# Dev server
npm run dev

# Build producción
npm run build

# Preview del build
npm run preview

# Deploy: copiar dist/ al VPS
```

---

## 8. Archivos Clave para Contexto

| Archivo | Qué contiene |
|---------|-------------|
| `src/styles/global.css` | Tailwind v4 config + `@theme` + animaciones globales |
| `src/layouts/Layout.astro` | HTML base, SEO, meta tags, fonts, IntersectionObserver |
| `src/pages/index.astro` | Ensamblado de TODOS los componentes en orden |
| `astro.config.mjs` | Static output, plugin Tailwind v4 |

---

## 9. Agregar una Nueva Sección

1. Crear `src/components/MiNuevaSeccion.astro`
2. Copiar el patrón de sección del punto 3
3. Importar en `src/pages/index.astro` y añadir en el `<main>`
4. Añadir link en Navbar si corresponde
5. `npm run build` y verificar

---

**Si este archivo no responde tu duda, busca en Engram con query: "decoraciones-web astro"**
