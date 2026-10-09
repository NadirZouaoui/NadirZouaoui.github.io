/**
 * /sitemap.xml: every built, published page with an absolute URL. Uses the same draft filter and the same
 * "section index only when it has a visible entry" condition as the routes. Never the 404.
 */
import type { APIRoute } from 'astro';
import { getProjects, getSimulators } from '../lib/content';

const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

export const GET: APIRoute = async ({ site }) => {
  const abs = (p: string) => new URL(p, site).href;
  const [projects, simulators] = await Promise.all([getProjects(), getSimulators()]);
  const paths = ['/'];
  if (projects.length) paths.push('/projects/', ...projects.map((p) => `/projects/${p.id}/`));
  if (simulators.length) paths.push('/simulators/', ...simulators.map((s) => `/simulators/${s.id}/`));
  const body =
    '<?xml version="1.0" encoding="UTF-8"?>\n' +
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    paths.map((p) => `  <url><loc>${esc(abs(p))}</loc></url>`).join('\n') +
    '\n</urlset>\n';
  return new Response(body, { headers: { 'Content-Type': 'application/xml; charset=utf-8' } });
};
