// @ts-check
import { defineConfig } from 'astro/config';
import { readdir, readFile, rm } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

/** @param {string} root @returns {Promise<string[]>} */
async function walk(root) {
  const out = [];
  for (const e of await readdir(root, { withFileTypes: true })) {
    const p = path.join(root, e.name);
    if (e.isDirectory()) out.push(...(await walk(p)));
    else out.push(p);
  }
  return out;
}

/** @param {string} dist @param {{ info: (m: string) => void }} logger */
async function sweepUnreferencedImages(dist, logger) {
  const all = await walk(dist);
  const text = (await Promise.all(all.filter((f) => /\.(html|css|m?js|json|xml|txt)$/.test(f)).map((f) => readFile(f, 'utf8')))).join('\n');
  let n = 0;
  for (const f of all) {
    if (!f.includes(`${path.sep}_astro${path.sep}`) || !/\.(jpe?g|png|webp|avif|gif|svg)$/i.test(f)) continue;
    if (!text.includes(path.basename(f))) {
      await rm(f, { force: true });
      n++;
    }
  }
  if (n) logger.info(`removed ${n} unreferenced image file(s) from _astro/ (originals of unpublished entries)`);
}

/**
 * Two clean-ups after the build (both only delete things that no page can reach):
 *
 * 1. Unreferenced images in dist/_astro. Astro emits the ORIGINAL file of every image() field of every content
 *    entry, drafts included, even when no page links to it. They are swept so draft photos are not published.
 * 2. Draft entries must not leak through /media/. Their images live in src/assets (only emitted when a page
 * uses them), but encoded clips live in public/media/<section>/<slug>/ and are copied verbatim.
 * After a production build this removes every dist/media/<section>/<slug>/ whose entry is not
 * explicitly `draft: false`. Builds with SHOW_DRAFTS=1 keep everything (preview only).
 * @returns {import('astro').AstroIntegration}
 */
function pruneUnpublished() {
  return {
    name: 'prune-unpublished',
    hooks: {
      'astro:build:done': async ({ dir, logger }) => {
        const dist = fileURLToPath(dir);
        await sweepUnreferencedImages(dist, logger);
        if (process.env.SHOW_DRAFTS) return;
        const src = path.resolve('src', 'content');
        for (const section of ['projects', 'simulators']) {
          const mediaDir = path.join(dist, 'media', section);
          /** @type {string[]} */
          let slugs = [];
          try { slugs = await readdir(mediaDir); } catch { continue; }
          for (const slug of slugs) {
            let published = false;
            try {
              const md = await readFile(path.join(src, section, slug, 'index.md'), 'utf8');
              published = /^draft:\s*false\s*(#.*)?$/m.test(md.split(/^---\s*$/m)[1] ?? '');
            } catch { /* no entry: not published */ }
            if (!published) {
              await rm(path.join(mediaDir, slug), { recursive: true, force: true });
              logger.info(`removed media of unpublished entry ${section}/${slug}`);
            }
          }
        }
      },
    },
  };
}

// Static output, served by GitHub Pages at https://nadirzouaoui.github.io/ (user site, so no `base`).
export default defineConfig({
  site: 'https://nadirzouaoui.github.io',
  output: 'static',
  trailingSlash: 'ignore',
  integrations: [pruneUnpublished()],
  build: {
    // Keep each page self-contained (the CV was a single file; the CSS is small).
    inlineStylesheets: 'always',
  },
});
