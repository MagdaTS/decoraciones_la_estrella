# Decoraciones Web - Landing Page

Landing page profesional para **Decoraciones La Estrella** — empresa especializada en decoración e instalaciones temáticas para centros comerciales, plazas y eventos.

## Stack Tecnológico

- **Framework:** [Astro](https://astro.build/) v5.7.3 (Static Site Generation)
- **CSS Framework:** [Tailwind CSS](https://tailwindcss.com/) v4.1.15
- **Fonts:** Google Fonts (Inter + Montserrat)
- **Icons:** FontAwesome 6.5.1
- **Images:** Pexels (CDN externo)
- **Form Backend:** Formspree (placeholder configurado)

## Estructura del Proyecto

```
.
├── public/
│   ├── Logo.jpg              # Logo principal
│   ├── favicon.ico           # Favicon
│   └── favicon.svg           # Favicon SVG
├── src/
│   ├── components/           # Componentes Astro
│   │   ├── Hero.astro
│   │   ├── Navbar.astro
│   │   ├── Services.astro
│   │   ├── Gallery.astro
│   │   ├── Benefits.astro
│   │   ├── BeforeAfter.astro
│   │   ├── Process.astro
│   │   ├── Cases.astro
│   │   ├── WhyUs.astro
│   │   ├── Contact.astro
│   │   ├── Footer.astro
│   │   ├── WhatsAppFloat.astro
│   │   ├── ScrollTop.astro
│   │   └── SkipNav.astro
│   ├── layouts/
│   │   └── Layout.astro      # Layout base con SEO y meta tags
│   ├── pages/
│   │   └── index.astro       # Página principal
│   └── styles/
│       └── global.css        # Tailwind v4 + custom styles
├── astro.config.mjs          # Configuración Astro
├── package.json
└── README.md
```

## Instalación Local

```bash
# Clonar o navegar al proyecto
cd decoraciones-web-astro

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev

# Build para producción
npm run build
```

## Deploy en VPS

### 1. Build del Proyecto

```bash
npm run build
```

Esto genera la carpeta `dist/` con HTML estático, CSS y assets.

### 2. Copiar al Servidor

Copia el contenido de la carpeta `dist/` al directorio web de tu VPS:

```bash
# Ejemplo con SCP
scp -r dist/* usuario@vps-ip:/var/www/decoraciones-web/

# O con rsync
rsync -avz --delete dist/ usuario@vps-ip:/var/www/decoraciones-web/
```

### 3. Configuración Nginx

```nginx
server {
    listen 80;
    server_name decoraciones-web.com www.decoraciones-web.com;
    root /var/www/decoraciones-web;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/javascript image/svg+xml;

    # Cache static assets
    location ~* \.(css|js|jpg|jpeg|png|gif|ico|svg|woff|woff2)$ {
        expires 1M;
        add_header Cache-Control "public, immutable";
    }

    # SPA fallback (Astro genera HTML estático, pero por si acaso)
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

### 4. SSL con Certbot (Let's Encrypt)

```bash
sudo certbot --nginx -d decoraciones-web.com -d www.decoraciones-web.com
```

### 5. Permisos

```bash
sudo chown -R www-data:www-data /var/www/decoraciones-web
sudo chmod -R 755 /var/www/decoraciones-web
```

## Configuración del Formulario de Contacto

El formulario usa **Formspree** como backend. Para activarlo:

1. Crear cuenta en [formspree.io](https://formspree.io)
2. Crear un nuevo formulario y obtener el endpoint
3. Reemplazar `YOUR_FORM_ID` en `src/components/Contact.astro`:

```html
<form action="https://formspree.io/f/TU_FORM_ID_REAL" method="POST">
```

4. Rebuild y redeploy

## Personalización

### Colores

Editar `src/styles/global.css`:

```css
@theme {
  --color-primary: #D9BC4A;      /* Dorado */
  --color-primary-dark: #C99A18; /* Dorado oscuro */
  --color-secondary: #14A4CC;    /* Azul tecnología */
  --color-accent-magenta: #E5007D;
  --color-accent-red: #F31212;
  --color-accent-green: #39B257;
  --color-accent-yellow: #F0C400;
}
```

### Meta Tags / SEO

Editar `src/layouts/Layout.astro`:

```astro
const { 
  title = 'Tu título personalizado',
  description = 'Tu descripción personalizada'
} = Astro.props;
```

### Imágenes

Las imágenes de la galería y casos se cargan desde **Pexels**. Para usar imágenes propias:

1. Copiar imágenes a `public/images/`
2. Actualizar los `src` en los componentes correspondientes

## Features Implementadas

- [x] Responsive design (mobile-first)
- [x] Scroll animations con IntersectionObserver
- [x] Lazy loading de imágenes
- [x] Accesibilidad (skip-nav, aria-labels, reduced-motion)
- [x] Formulario con validación JS
- [x] Slider antes/después interactivo
- [x] Navbar sticky con hide/show on scroll
- [x] Mobile menu con hamburger animation
- [x] WhatsApp floating button
- [x] Scroll to top button
- [x] Preconnect y preload de recursos críticos
- [x] Open Graph y Twitter Cards
- [x] Schema.org LocalBusiness JSON-LD

## Licencia

© 2024 Decoraciones Web. Todos los derechos reservados.
