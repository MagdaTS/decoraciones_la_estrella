# Decoraciones La Estrella — Landing

Sitio web estático de **Decoraciones La Estrella**, fabricante de decoraciones temáticas para centros comerciales y espacios públicos en México.

## Stack

- **Astro 6.4.7** — Static Site Generation
- **Tailwind CSS 4** — Sin `tailwind.config.js`, configuración en `src/styles/global.css` con `@theme {}`
- **Formspree** — Backend del formulario de contacto
- **GitHub Pages** — Hosting (con dominio custom `decoracioneslaestrella.com`)

## Estructura

```
.
├── public/
│   ├── CNAME                  # Dominio custom para GitHub Pages
│   ├── catalogos/             # PDFs y previews de catálogos
│   ├── material/gallery/      # Imágenes propias para la galería
│   ├── Logo-*.png             # Logos
│   ├── favicon.*              # Favicon
│   ├── robots.txt             # SEO
│   └── sitemap.xml            # SEO
├── src/
│   ├── assets/                # Imágenes importadas por Astro (ej. hero)
│   ├── components/            # Componentes Astro (16 secciones)
│   ├── layouts/Layout.astro   # Layout base con SEO, OG, meta tags
│   ├── pages/
│   │   ├── index.astro       # Home
│   │   └── privacidad.astro   # Aviso de Privacidad (LFPDPPP)
│   └── styles/global.css      # Tailwind v4 + animaciones globales
├── scripts/
│   └── compress_catalogs.py   # Pipeline de compresión de catálogos PDF
├── astro.config.mjs           # Configuración de Astro
├── .github/workflows/         # GitHub Actions para deploy automático
└── package.json
```

## Comandos

```bash
npm install     # Instalar dependencias
npm run dev     # Servidor de desarrollo (http://localhost:4321)
npm run build   # Build de producción → dist/
npm run preview # Preview del build
```

## Deploy

El sitio se deploya automáticamente a GitHub Pages en cada `push` a `master` mediante GitHub Actions (`.github/workflows/deploy.yml`).

- **URL GitHub Pages**: `https://magdats.github.io/decoraciones_la_estrella`
- **Dominio custom**: `https://decoracioneslaestrella.com` (configurado vía `public/CNAME`)

El `astro.config.mjs` detecta automáticamente si el build es para subpath o raíz según la variable de entorno `USE_BASE_PATH` (configurada en el workflow).

### Configurar dominio custom

1. En tu registrador DNS, agregar registros CNAME:
   - `decoracioneslaestrella.com` → `MagdaTS.github.io`
   - `www.decoracioneslaestrella.com` → `MagdaTS.github.io`
2. En GitHub: Settings → Pages → Custom domain: `decoracioneslaestrella.com`
3. Marcar "Enforce HTTPS" cuando el certificado esté emitido (puede tardar hasta 1 hora)

## Formulario de contacto

El formulario usa **Formspree** (ID `xgojenld` en `src/components/Contact.astro`). Para cambiar el destino de los mensajes, reemplazá el ID por el tuyo en Formspree.

## Catálogos

Los catálogos PDF están en `public/catalogos/` (versión comprimida) y sus previews WebP en `public/catalogos/previews/`. Para regenerarlos desde PDFs fuente, usá el script `scripts/compress_catalogs.py` con `pypdfium2` y `pypdf`.

## Licencia

© Decoraciones La Estrella. Todos los derechos reservados.
