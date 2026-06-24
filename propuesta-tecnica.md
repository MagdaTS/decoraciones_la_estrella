# Propuesta Técnica - Landing Page Decoraciones Web

## Resumen Ejecutivo

**Proyecto**: Landing page corporativa para empresa de decoraciones e instalaciones temáticas en centros comerciales y plazas.

**Objetivo**: Convertir visitantes en leads cualificados mediante una experiencia visual impactante que demuestre capacidad de diseño y ejecución.

**Stack Recomendado**:
- **Frontend**: HTML5 + CSS3 + JavaScript vanilla
- **Framework**: Next.js (fase 2, si escala)
- **Hosting**: Vercel (gratis, rápido, CDN global)
- **Formularios**: Formspree (plan gratuito disponible)
- **Galería**: Lightbox2 o PhotoSwipe
- **Animaciones**: CSS + Intersection Observer API
- **WhatsApp**: API de WhatsApp Business (gratuita)

---

## 1. Análisis de la Propuesta de Diseño

### Fortalezas Identificadas
- **Estructura clara**: 9 secciones bien definidas con flujo lógico
- **Enfoque en resultados**: No vende "decoración", vende "más visitantes", "más tiempo", "más redes"
- **Elementos de prueba social**: Galería, casos de éxito, antes/después
- **CTA estratégicos**: Múltiples puntos de conversión (hero, formulario, WhatsApp)

### Riesgos y Mitigaciones

| Riesgo | Impacto | Mitigación |
|--------|---------|------------|
| Sin contenido real (fotos) | Alto | Usar placeholders de Unsplash/crear mockups con IA |
| Fase 2: Simulador visual | Medio | Dejarlo como "Próximamente" en MVP, implementar en v2 |
| Velocidad de carga (galería) | Medio | Lazy loading + compresión WebP + CDN |
| Mobile experience | Medio | Mobile-first design obligatorio |

---

## 2. Arquitectura de la Landing Page

### 2.1 Estructura de Navegación (Single Page)

```
├── Navbar (fixed, sticky on scroll)
│   ├── Logo
│   ├── Links: Inicio | Proyectos | Servicios | Nosotros | Contacto
│   └── CTA móvil: "Solicitar Propuesta"
│
├── Hero Section (full viewport)
│   ├── Background: Video/Imagen de plaza decorada
│   ├── Overlay: gradient oscuro (texto legible)
│   ├── H1: "Transformamos Centros Comerciales en Experiencias Memorables"
│   ├── Subtítulo: Descripción de servicios
│   └── CTAs: [Solicitar Propuesta] [Ver Proyectos]
│
├── Servicios (Sección 2)
│   ├── Título: "Lo que hacemos"
│   └── Grid 2x2 (responsive)
│       ├── Tarjeta 1: Centros Comerciales (icono magenta #E5007D)
│       ├── Tarjeta 2: Eventos Temáticos (icono verde #39B257)
│       ├── Tarjeta 3: Escenografías Fotográficas (icono rojo #F31212)
│       └── Tarjeta 4: Fabricación Especial (icono amarillo #F0C400)
│
├── Galería (Sección 3 - MÁS IMPORTANTE)
│   ├── Título: "Nuestros proyectos hablan por nosotros"
│   ├── Grid masonry o grid regular (responsive)
│   └── Cada item: thumbnail + overlay + click -> modal/lightbox
│
├── Beneficios (Sección 4)
│   ├── Título: "Resultados que puedes medir"
│   └── Grid 2x2 con iconos
│       ├── Más visitantes
│       ├── Más tiempo de permanencia
│       ├── Más fotografías y redes
│       └── Diferenciación
│
├── Antes/Después (Sección 5)
│   ├── Título: "La transformación habla por sí sola"
│   └── Slider comparativo (2-3 ejemplos)
│       ├── Imagen izquierda: "Antes" (plaza normal)
│       └── Imagen derecha: "Después" (plaza decorada)
│
├── Proceso (Sección 6)
│   ├── Título: "Nuestro proceso de trabajo"
│   └── Timeline horizontal (desktop) / vertical (mobile)
│       ├── 1. Visita y diagnóstico
│       ├── 2. Diseño conceptual
│       ├── 3. Fabricación
│       ├── 4. Instalación
│       └── 5. Soporte
│
├── Casos de Éxito (Sección 7)
│   ├── Título: "Proyectos que generan resultados"
│   └── 2-3 tarjetas de caso
│       ├── Foto grande
│       ├── Ubicación, Año, Tipo
│       ├── Objetivo → Solución → Resultado
│
├── Diferenciadores (Sección 8)
│   ├── Título: "¿Por qué elegirnos?"
│   └── Grid 2x2 con iconos
│       ├── Atención personalizada
│       ├── Diseño a medida
│       ├── Instalación profesional
│       └── Respuesta rápida
│
├── Formulario (Sección 9)
│   ├── Título: "Solicita una propuesta personalizada"
│   ├── Formulario (5 campos)
│   └── Botón: "Quiero una propuesta"
│
├── Footer
│   ├── Logo + tagline
│   ├── Contacto: email, teléfono, WhatsApp
│   ├── Redes sociales
│   └── Copyright + legal
│
└── Floating Elements
    ├── WhatsApp Button (sticky bottom-right)
    └── Scroll-to-top (aparece después de scroll)
```

---

## 3. Especificaciones Técnicas por Sección

### 3.1 Hero Section

**Requisitos técnicos:**
- Altura: 100vh (viewport height)
- Background: `object-fit: cover` o video autoplay muted loop
- Overlay: `background: linear-gradient(rgba(44, 24, 16, 0.6), rgba(44, 24, 16, 0.85))` (usando el color dark del logo)
- Texto centrado vertical y horizontal
- Botones: estilo primary (sólido) + secondary (outline/blur)
- Animación: fade-in suave al cargar (1.5s)

**Performance:**
- Imagen/video optimizado: WebP < 500KB, video < 2MB
- Carga prioritaria: `<link rel="preload">` para el hero image

**Ejemplo de estructura HTML:**
```html
<section id="hero" class="hero">
  <div class="hero-background">
    <img src="hero.webp" alt="Plaza decorada espectacular" loading="eager">
    <div class="hero-overlay"></div>
  </div>
  <div class="hero-content">
    <h1 class="hero-title">Transformamos Centros Comerciales en Experiencias Memorables</h1>
    <p class="hero-subtitle">Decoración e instalaciones temáticas...</p>
    <div class="hero-cta">
      <a href="#contacto" class="btn btn-primary">Solicitar Propuesta</a>
      <a href="#proyectos" class="btn btn-secondary">Ver Proyectos</a>
    </div>
  </div>
</section>
```

### 3.2 Galería de Impacto (Sección Crítica)

**Requisitos técnicos:**
- Layout: CSS Grid con `grid-template-columns: repeat(auto-fit, minmax(300px, 1fr))`
- Aspect ratio: 4:3 o 16:9 uniforme
- Hover effect: overlay oscuro con info del proyecto
- Lightbox: PhotoSwipe (más profesional que Lightbox2)
- Lazy loading: `loading="lazy"` + Intersection Observer
- Modal info: Cliente, Ciudad, Año, Tipo, Mini-galería

**Estructura de datos (JSON):**
```json
[
  {
    "id": 1,
    "cliente": "Plaza Mayor",
    "ciudad": "Ciudad de México",
    "año": 2024,
    "tipo": "Navidad",
    "imagen": "proyecto1.webp",
    "galeria": ["img1.webp", "img2.webp", "img3.webp"]
  }
]
```

### 3.3 Slider Antes/Después

**Requisitos técnicos:**
- Librería recomendada: [juxtaposeJS](https://juxtapose.knightlab.com/) (Nat Geo, PBS)
- Alternativa: CSS + JS vanilla (slider con input range)
- Responsive: 100% width en mobile, max 800px en desktop
- Imágenes: mismas dimensiones exactas

### 3.4 Formulario de Contacto

**Requisitos técnicos:**
- Campos: Nombre, Empresa, Teléfono, Email, Mensaje (textarea)
- Validación: HTML5 + JS (regex para email/teléfono)
- Envío: Formspree (POST a `https://formspree.io/f/{FORM_ID}`)
- UX: Loading state, success message, error handling
- Campos obligatorios: Nombre, Teléfono, Email

**Ejemplo de integración:**
```html
<form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
  <input type="text" name="nombre" required placeholder="Tu nombre">
  <input type="text" name="empresa" placeholder="Empresa">
  <input type="tel" name="telefono" required placeholder="Teléfono">
  <input type="email" name="email" required placeholder="Correo electrónico">
  <textarea name="mensaje" placeholder="¿Qué necesitas?"></textarea>
  <button type="submit">Quiero una propuesta</button>
</form>
```

### 3.5 WhatsApp Flotante

**Requisitos técnicos:**
- Posición: fixed, bottom: 20px, right: 20px
- Icono: FontAwesome o SVG propio
- Link: `https://wa.me/521XXXXXXXXXX?text=Hola,%20me%20interesa%20una%20propuesta%20de%20decoración`
- Animación: pulse sutil cada 5 segundos
- Tooltip: "¡Escríbenos!" (aparece al cargar, desaparece al hacer scroll)

---

## 4. Plan de Implementación (MVP)

### Fase 1: MVP (Semana 1-2)
**Objetivo**: Landing funcional, estática, con información real.

**Entregables:**
- [ ] Setup proyecto (HTML + CSS + JS)
- [ ] Navbar responsive con smooth scroll
- [ ] Hero section con imagen/video
- [ ] Sección de servicios (4 tarjetas)
- [ ] Galería con lightbox (mínimo 6 proyectos)
- [ ] Beneficios (4 items con iconos)
- [ ] Formulario de contacto con Formspree
- [ ] Footer con info básica
- [ ] WhatsApp flotante
- [ ] Responsive (mobile-first)

### Fase 2: Mejoras Visuales (Semana 3)
**Objetivo**: Animaciones, interacciones, optimización.

**Entregables:**
- [ ] Animaciones de entrada (fade-up, slide-in)
- [ ] Slider Antes/Después (1-2 ejemplos)
- [ ] Timeline de proceso (animado)
- [ ] Lazy loading en imágenes
- [ ] Optimización de performance (WebP, minificación)
- [ ] SEO básico (meta tags, schema.org)

### Fase 3: Contenido Avanzado (Semana 4)
**Objetivo**: Casos de éxito, catálogo PDF.

**Entregables:**
- [ ] Sección "Casos de Éxito" (2-3 tarjetas)
- [ ] Sección "¿Por qué elegirnos?"
- [ ] Catálogo PDF descargable (placeholder o real)
- [ ] Meta tags para redes sociales (OG tags)
- [ ] Favicon y manifest.json

### Fase 4: Escalabilidad (Opcional)
**Objetivo**: Next.js, CMS, simulador.

**Entregables:**
- [ ] Migración a Next.js (si aplica)
- [ ] Integración CMS (Sanity/Strapi) para galería
- [ ] Simulador visual (subir foto + render IA)
- [ ] Blog/Noticias
- [ ] Multi-idioma

---

## 5. Guía de Estilo Visual

### 5.1 Paleta de Colores Recomendada

**Paleta de Identidad Visual (2026)**
- **Primary**: `#D9BC4A` (Dorado Estrella - color dominante)
- **Primary Dark**: `#C99A18` (Oro Profundo - hover, énfasis)
- **Secondary**: `#14A4CC` (Azul Tecnología - inovación, contrastes)
- **Accent Magenta**: `#E5007D` (Magenta Innovación - IA, creatividad)
- **Accent Red**: `#F31212` (Rojo Energía - alertas, destacados)
- **Accent Green**: `#39B257` (Verde Soluciones - éxito, completados)
- **Accent Yellow**: `#F0C400` (Amarillo Brillo - destellos visuales)
- **Background**: `#F8F8F8` (Blanco Perla)
- **Text**: `#111111` (Negro Elegante)
- **Text Secondary**: `#5C5C5C` (Gris Grafito)
- **Dark**: `#111111` (Negro Elegante - fondos oscuros)
- **White**: `#FFFFFF`

**Uso de colores:**
- **Primary (Dorado)**: CTAs principales, botones, hover states, highlights
- **Primary Dark (Oro Profundo)**: Hover de botones dorados, énfasis dorado intenso
- **Secondary (Azul Tecnología)**: Degradados, acentos de innovación, elementos tecnológicos
- **Accents (Magenta, Rojo, Verde, Amarillo)**: Iconos de servicios, categorías, badges, gráficos
- **Background**: Blanco perla para legibilidad y limpieza
- **Text**: Negro elegante para lectura cómoda y máximo contraste
- **Dark**: Fondos de secciones oscuras (galería, proceso, contacto, footer)

### 5.2 Tipografía

**Headings (H1, H2, H3):**
- Fuente: Montserrat (Google Fonts) o Poppins
- Peso: 700 (bold)
- H1: 48px (desktop), 32px (mobile)
- H2: 36px (desktop), 28px (mobile)

**Body:**
- Fuente: Inter o Open Sans
- Peso: 400 (normal)
- Tamaño: 16px-18px
- Interlineado: 1.6

### 5.3 Espaciado (Sistema 8px)

```css
:root {
  --space-xs: 8px;
  --space-sm: 16px;
  --space-md: 24px;
  --space-lg: 32px;
  --space-xl: 48px;
  --space-2xl: 64px;
  --space-3xl: 96px;
}

.section { padding: var(--space-3xl) 0; }
```

### 5.4 Componentes UI

**Botón Primary:**
```css
.btn-primary {
  background: var(--primary);
  color: var(--dark);
  padding: 16px 32px;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(217, 188, 74, 0.3);
}
.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(217, 188, 74, 0.4);
  background: var(--primary-dark);
}
```

**Tarjeta de Servicio:**
```css
.service-card {
  background: white;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.08);
  transition: all 0.3s ease;
  border: 1px solid rgba(0,0,0,0.05);
}
.service-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(0,0,0,0.12);
}
```

---

## 6. Assets Necesarios

### 6.1 Imágenes (Prioridad)

**Mínimo viable para MVP:**

| Asset | Tipo | Cantidad | Uso |
|-------|------|----------|-----|
| Hero background | Foto/video | 1 | Sección principal |
| Proyectos galería | Fotos | 6-8 | Galería de impacto |
| Servicios | Iconos/ilustraciones | 4 | Tarjetas de servicio |
| Antes/Después | Comparativas | 2 | Slider |
| Casos de éxito | Fotos | 2-3 | Tarjetas de caso |
| Logo | SVG/PNG | 1 | Navbar + footer |
| Iconos | SVG set | 20+ | Beneficios, proceso, UI |

**Fuentes de imágenes (si no hay propias):**
- Unsplash (gratis, alta calidad): buscar "shopping mall decoration", "christmas mall", "plaza events"
- Pexels (alternativa gratuita)
- AI Generation (Midjourney/DALL-E): para crear renders conceptuales

### 6.2 Copy/Textos

**Recomendación**: Usar los textos de la propuesta como base. Refinar:
- Títulos: más acción, menos descripción
- CTAs: verbo imperativo + beneficio
- Beneficios: datos concretos si existen ("aumento del 30% en tráfico")

---

## 7. Performance y SEO

### 7.1 Performance Targets

| Métrica | Objetivo | Cómo lograrlo |
|---------|----------|---------------|
| First Contentful Paint (FCP) | < 1.8s | Preload hero, lazy load resto |
| Largest Contentful Paint (LCP) | < 2.5s | Imágenes WebP, CDN |
| Time to Interactive (TTI) | < 3.8s | JS diferido, no bloqueante |
| Cumulative Layout Shift (CLS) | < 0.1 | Dimensiones fijas en imágenes |

### 7.2 SEO Checklist

- [ ] Meta title: "Decoraciones Web | Transformamos Plazas en Experiencias"
- [ ] Meta description: 150-160 caracteres con keywords
- [ ] Open Graph tags (Facebook/LinkedIn)
- [ ] Twitter Cards
- [ ] Schema.org: LocalBusiness, Service, ImageGallery
- [ ] Sitemap.xml
- [ ] Robots.txt
- [ ] Alt text en todas las imágenes
- [ ] URL amigable: `decoraciones-web.com`
- [ ] Mobile-first index ready

---

## 8. Responsive Breakpoints

```css
/* Mobile First */
/* Small devices */
@media (min-width: 640px) { /* sm */ }

/* Medium devices */
@media (min-width: 768px) { /* md */ }

/* Large devices */
@media (min-width: 1024px) { /* lg */ }

/* Extra large */
@media (min-width: 1280px) { /* xl */ }
```

**Reglas de oro:**
- Touch targets mínimo: 48x48px
- Tipografía: 16px mínimo en mobile (accesibilidad)
- Espaciado reducido en mobile (padding: 24px vs 48px en desktop)
- Navegación: hamburger menu en < 768px
- Galería: 1 columna en mobile, 2-3 en tablet, 3-4 en desktop

---

## 9. Accesibilidad (a11y)

- [ ] Contraste mínimo 4.5:1 para texto
- [ ] Focus states visibles en todos los elementos interactivos
- [ ] Skip navigation link
- [ ] ARIA labels en iconos sin texto
- [ ] Formularios: labels asociados, error messages claros
- [ ] Alt text descriptivo en imágenes (no "imagen1.jpg")
- [ ] Reducir movimiento: `prefers-reduced-motion`

---

## 10. Tracking y Analytics

**Herramientas recomendadas:**
- **Google Analytics 4**: tráfico, comportamiento, conversiones
- **Google Search Console**: indexación, performance SERP
- **Hotjar** (gratis hasta 35 sesiones/día): heatmaps, recordings
- **Meta Pixel** (si usan Facebook/Instagram Ads)

**Eventos a trackear:**
- Click en "Solicitar Propuesta"
- Click en "Ver Proyectos"
- Envío de formulario (exitoso y fallido)
- Click en WhatsApp
- Descarga de catálogo PDF
- Interacción con slider antes/después
- Tiempo en galería

---

## 11. Presupuesto y Herramientas (Costos)

| Item | Herramienta | Costo Mensual |
|------|-------------|---------------|
| Hosting | Vercel | Gratis |
| Dominio | Namecheap/GoDaddy | ~$12/año |
| Formularios | Formspree | Gratis (100 envíos/mes) |
| Analytics | Google Analytics | Gratis |
| Imágenes | Unsplash/Pexels | Gratis |
| Iconos | Phosphor Icons / Heroicons | Gratis |
| WhatsApp | API oficial | Gratis (mensajes salientes) |
| **Total** | | **~$12/año** |

**Si se escala:**
- Formspree Pro: $10/mes (envíos ilimitados)
- Vercel Pro: $20/mes (analytics, más velocidad)
- CDN adicional: Cloudflare (gratis)

---

## 12. Próximos Pasos

### Para Empezar Hoy:
1. **Confirmar paleta de colores**: ¿Elegante, Festiva o Moderna?
2. **Reunir assets**: ¿Tienen fotos de proyectos reales? ¿Necesitamos usar stock temporalmente?
3. **Definir el nombre**: ¿"Decoraciones Web" es el nombre definitivo? ¿Hay logo?
4. **Información de contacto**: Teléfono, email, WhatsApp para el formulario
5. **Proyectos para la galería**: Mínimo 6 proyectos con datos (cliente, ciudad, año, tipo)

### Si quieren implementar con SDD:
- Podemos ejecutar el flujo completo: exploración → especificación → diseño técnico → tareas → implementación → verificación
- Cada fase genera un artefacto documentado y verificable
- Ideal para mantener trazabilidad y calidad

---

## 13. Anexo: Snippets de Código Útiles

### CSS Reset + Variables Base
```css
:root {
  --primary: #D9BC4A;
  --primary-dark: #C99A18;
  --secondary: #14A4CC;
  --accent-magenta: #E5007D;
  --accent-red: #F31212;
  --accent-green: #39B257;
  --accent-yellow: #F0C400;
  --bg: #F8F8F8;
  --text: #111111;
  --text-secondary: #5C5C5C;
  --dark: #111111;
  --white: #FFFFFF;
  
  --font-heading: 'Montserrat', sans-serif;
  --font-body: 'Inter', sans-serif;
  
  --radius: 12px;
  --shadow: 0 4px 24px rgba(0,0,0,0.08);
  --shadow-lg: 0 12px 40px rgba(0,0,0,0.12);
  
  --transition: all 0.3s ease;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: var(--font-body);
  color: var(--text);
  line-height: 1.6;
  background: var(--bg);
}

h1, h2, h3, h4 {
  font-family: var(--font-heading);
  font-weight: 700;
  line-height: 1.2;
}

img {
  max-width: 100%;
  height: auto;
  display: block;
}

a {
  text-decoration: none;
  color: inherit;
}

button {
  cursor: pointer;
  border: none;
  font-family: inherit;
}
```

### Smooth Scroll
```javascript
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    document.querySelector(this.getAttribute('href')).scrollIntoView({
      behavior: 'smooth'
    });
  });
});
```

### Intersection Observer (animaciones scroll)
```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('animate-in');
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.animate-on-scroll').forEach(el => observer.observe(el));
```

---

**Documento preparado por**: Gentle AI
**Fecha**: 2026-06-07
**Versión**: 1.0
**Estado**: Propuesta para revisión

---

¿Necesitás que ajustemos algo de esta guía o querés que empecemos con la implementación de alguna sección específica?