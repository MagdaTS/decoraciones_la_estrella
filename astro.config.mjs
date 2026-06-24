// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config

// GitHub Pages with a custom domain (decoracioneslaestrella.com) serves the
// site from the domain root, so no `base` is needed.
// GitHub Pages without a custom domain (e.g. magdats.github.io/<repo>) serves
// the site from a subpath; set USE_BASE_PATH=true to enable the subpath prefix.
const useBasePath = process.env.USE_BASE_PATH === 'true';
const base = useBasePath ? '/decoraciones_la_estrella/' : '/';

export default defineConfig({
  output: 'static',
  site: 'https://decoracioneslaestrella.com',
  base,
  server: {
    host: true,
    allowedHosts: true,
  },
  vite: {
    plugins: [tailwindcss()]
  }
});
