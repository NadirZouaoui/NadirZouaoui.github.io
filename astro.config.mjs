// @ts-check
import { defineConfig } from 'astro/config';

// Static output, served by GitHub Pages at https://nadirzouaoui.github.io/ (user site, so no `base`).
export default defineConfig({
  site: 'https://nadirzouaoui.github.io',
  output: 'static',
  trailingSlash: 'ignore',
  build: {
    // Keep each page self-contained (the CV was a single file; the CSS is small).
    inlineStylesheets: 'always',
  },
});
