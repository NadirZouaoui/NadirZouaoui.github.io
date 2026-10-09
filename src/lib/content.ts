import { getCollection, getEntry, render, type CollectionEntry } from 'astro:content';

/**
 * Drafts are visible in `astro dev` and in builds made with SHOW_DRAFTS=1 (see `npm run build:drafts`).
 * A normal production build never contains a draft page, nav link or card.
 */
export const SHOW_DRAFTS: boolean = import.meta.env.DEV || !!process.env.SHOW_DRAFTS;

const byOrder = (a: { data: { order: number }; id: string }, b: { data: { order: number }; id: string }) =>
  a.data.order - b.data.order || a.id.localeCompare(b.id);

export async function getProjects(): Promise<CollectionEntry<'projects'>[]> {
  const all = await getCollection('projects', ({ data }) => SHOW_DRAFTS || !data.draft);
  return all.sort(byOrder);
}

export async function getSimulators(): Promise<CollectionEntry<'simulators'>[]> {
  const all = await getCollection('simulators', ({ data }) => SHOW_DRAFTS || !data.draft);
  return all.sort(byOrder);
}

export type Lang = 'en' | 'fr';

/**
 * Render the EN body and the (optional) FR body of an entry.
 * If there is no index.fr.md, the French slot falls back to the English text (flagged with fallback=true)
 * so the page never shows an empty French view.
 */
export async function renderBilingual(section: 'projects' | 'simulators', id: string) {
  const en = await getEntry(section, id as never);
  const fr = await getEntry((section + 'Fr') as 'projectsFr' | 'simulatorsFr', id);
  if (!en) throw new Error(`No ${section} entry "${id}"`);
  const EnContent = (await render(en as never)).Content;
  if (!fr) {
    console.warn(`[content] ${section}/${id}: no index.fr.md, French view falls back to English.`);
    return { En: EnContent, Fr: EnContent, frFallback: true };
  }
  return { En: EnContent, Fr: (await render(fr)).Content, frFallback: false };
}

/** Warn at build time about empty alt text on non-draft entries (accessibility). */
export function warnMissingAlt(where: string, items: { alt: { en: string; fr: string } }[], draft: boolean) {
  if (draft) return;
  items.forEach((it, i) => {
    if (!it.alt.en.trim() || !it.alt.fr.trim()) console.warn(`[a11y] ${where}: item ${i + 1} has empty alt text (en/fr).`);
  });
}
