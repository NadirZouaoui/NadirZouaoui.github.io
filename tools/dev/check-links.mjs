#!/usr/bin/env node
/**
 * Link checker for a built folder (default: dist). No dependency.
 *
 *   node tools/dev/check-links.mjs [folder] [--external] [--site https://host]
 *
 * For every href / src / srcset / poster / content URL in the HTML files:
 *  - internal targets (relative, root-relative, or on the site's own origin) must exist in the folder,
 *    including the #fragment (an id= or name= in the target page);
 *  - with --external, other http(s) URLs are requested (HEAD, then GET) and reported.
 * Exit code 1 only when an INTERNAL link is broken. External problems are a report: sites such as LinkedIn
 * answer 999/403 to bots, they are listed as "blocked, check by hand".
 */
import { readdir, readFile, stat } from 'node:fs/promises';
import path from 'node:path';

const args = process.argv.slice(2);
const flag = (n) => args.includes(n);
const opt = (n) => { const i = args.indexOf(n); return i >= 0 ? args[i + 1] : undefined; };
const skipVals = new Set([opt('--site')].filter(Boolean));
const root = path.resolve(args.find((a) => !a.startsWith('--') && !skipVals.has(a)) ?? 'dist');
const SITE = new URL(opt('--site') ?? 'https://nadirzouaoui.github.io');
const EXTERNAL = flag('--external');
const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36';

async function walk(dir) {
  const out = [];
  for (const e of await readdir(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) out.push(...(await walk(p)));
    else out.push(p);
  }
  return out;
}
const exists = async (p) => { try { return (await stat(p)).isFile(); } catch { return false; } };

/** Map a URL path (decoded, no query/hash) to a file in the build, the way GitHub Pages would serve it. */
async function resolveFile(urlPath) {
  const rel = decodeURIComponent(urlPath).replace(/^\/+/, '');
  const base = path.join(root, rel);
  if (!path.resolve(base).startsWith(root)) return null;
  const candidates = urlPath.endsWith('/') || rel === '' ? [path.join(base, 'index.html')] : [base, base + '.html', path.join(base, 'index.html')];
  for (const c of candidates) if (await exists(c)) return c;
  return null;
}

const idCache = new Map();
async function idsOf(file) {
  if (!idCache.has(file)) {
    const html = await readFile(file, 'utf8');
    const ids = new Set();
    for (const m of html.matchAll(/\s(?:id|name)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))/gi)) ids.add(m[1] ?? m[2] ?? m[3]);
    idCache.set(file, ids);
  }
  return idCache.get(file);
}

/** Collect [attr, value] URL candidates from the tags of an HTML document (script/style bodies and comments ignored). */
function extract(html) {
  const clean = html.replace(/<!--[\s\S]*?-->/g, '').replace(/<(script|style)\b[^>]*>[\s\S]*?<\/\1>/gi, (m) => m.slice(0, m.indexOf('>') + 1));
  const found = [];
  for (const tag of clean.matchAll(/<([a-zA-Z][\w-]*)\b([^>]*)>/g)) {
    for (const a of tag[2].matchAll(/([\w:-]+)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'>]+))/g)) {
      const name = a[1].toLowerCase();
      const val = (a[2] ?? a[3] ?? a[4] ?? '').replace(/&amp;/g, '&').trim();
      if (!val) continue;
      if (name === 'href' || name === 'src' || name === 'poster') found.push([name, val, tag[1]]);
      else if (name === 'srcset') for (const part of val.split(',')) { const u = part.trim().split(/\s+/)[0]; if (u) found.push([name, u, tag[1]]); }
      else if (name === 'content' && /^(https?:)?\/\/|^\//.test(val)) found.push([name, val, tag[1]]);
    }
  }
  return found;
}

const files = await walk(root);
const htmlFiles = files.filter((f) => f.endsWith('.html'));
const broken = [];
const externals = new Map(); // url -> [pages]
let checked = 0;

for (const file of htmlFiles) {
  const rel = path.relative(root, file).split(path.sep).join('/');
  const pageUrl = new URL('/' + rel.replace(/(^|\/)index\.html$/, '$1'), SITE);
  for (const [attr, raw, tag] of extract(await readFile(file, 'utf8'))) {
    if (/^(mailto:|tel:|data:|javascript:|blob:)/i.test(raw)) continue;
    let u;
    try { u = new URL(raw, pageUrl); } catch { broken.push(`${rel}: <${tag} ${attr}> invalid URL "${raw}"`); continue; }
    if (u.protocol !== 'http:' && u.protocol !== 'https:') continue;
    if (u.origin !== SITE.origin) {
      if (!externals.has(u.href.split('#')[0])) externals.set(u.href.split('#')[0], new Set());
      externals.get(u.href.split('#')[0]).add(rel);
      continue;
    }
    checked++;
    const target = await resolveFile(u.pathname);
    if (!target) { broken.push(`${rel}: <${tag} ${attr}> ${raw}  ->  no such file`); continue; }
    if (u.hash.length > 1 && target.endsWith('.html')) {
      const id = decodeURIComponent(u.hash.slice(1));
      if (id !== 'top' && !(await idsOf(target)).has(id)) broken.push(`${rel}: <${tag} ${attr}> ${raw}  ->  no #${id} in ${path.relative(root, target).split(path.sep).join('/')}`);
    }
  }
}

console.log(`Checked ${htmlFiles.length} page(s) in ${path.relative(process.cwd(), root) || '.'}: ${checked} internal link(s), ${externals.size} distinct external URL(s).`);
if (broken.length) {
  console.log(`\nBROKEN INTERNAL LINKS (${broken.length}):`);
  for (const b of broken) console.log('  ' + b);
} else console.log('Internal links: all OK.');

if (EXTERNAL && externals.size) {
  const BLOCKED = new Set([401, 403, 405, 406, 429, 451, 999]);
  async function probe(url) {
    const once = async (method) => {
      const ctl = new AbortController();
      const t = setTimeout(() => ctl.abort(), 15000);
      try {
        const r = await fetch(url, { method, redirect: 'follow', signal: ctl.signal, headers: { 'User-Agent': UA, Accept: 'text/html,*/*;q=0.8', 'Accept-Language': 'en' } });
        r.body?.cancel?.().catch(() => {});
        return r.status;
      } finally { clearTimeout(t); }
    };
    try {
      let s = await once('HEAD');
      if (s >= 400) s = await once('GET');
      return { url, status: s };
    } catch (e) {
      return { url, error: e.name === 'AbortError' ? 'timeout' : (e.cause?.code ?? e.message) };
    }
  }
  const urls = [...externals.keys()];
  const results = [];
  let next = 0;
  await Promise.all(Array.from({ length: 6 }, async () => { while (next < urls.length) results.push(await probe(urls[next++])); }));
  const ok = results.filter((r) => r.status && r.status < 400);
  const blocked = results.filter((r) => r.status && BLOCKED.has(r.status));
  const bad = results.filter((r) => (r.status && r.status >= 400 && !BLOCKED.has(r.status)) || r.error);
  console.log(`\nEXTERNAL: ${ok.length} OK, ${blocked.length} blocked (check by hand), ${bad.length} failing`);
  const pages = (u) => [...externals.get(u)].join(', ');
  for (const r of ok) console.log(`  OK      ${r.status}  ${r.url}`);
  for (const r of blocked) console.log(`  BLOCKED ${r.status}  ${r.url}  (bots refused; check by hand)  [${pages(r.url)}]`);
  for (const r of bad) console.log(`  FAILING ${r.status ?? r.error}  ${r.url}  [${pages(r.url)}]`);
}

process.exit(broken.length ? 1 : 0);
