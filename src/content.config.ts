import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

/**
 * Content model. See CLAUDE.md ("Adding a project", "Adding a simulator") for the authoring guide.
 *
 * Layout on disk (one folder per entry, the folder name IS the slug / URL):
 *   src/content/projects/<slug>/index.md      frontmatter + ENGLISH body
 *   src/content/projects/<slug>/index.fr.md   FRENCH body only (frontmatter not needed)
 *   src/content/simulators/<slug>/index.md    idem
 *   src/content/simulators/<slug>/index.fr.md
 */

/** A bilingual string. */
const bi = z.object({ en: z.string(), fr: z.string() });
/** Bilingual string that may be left empty while drafting (alt text and captions). */
const biLoose = z
  .object({ en: z.string().default(''), fr: z.string().default('') })
  .default({ en: '', fr: '' });

/** Folder name = slug. `*\/index.md` only (the French sibling is its own collection). */
const slugFromFolder = ({ entry }: { entry: string }) => entry.split('/')[0];

const DOMAINS = ['oil-gas', 'atex', 'solar-pv', 'automation', 'scada'] as const; // keep in sync with DOMAINS in src/lib/content.ts

const videoRef = z.object({
  /** Public URL of the encoded mp4, as printed by tools/media/encode_clip.py, e.g. /media/projects/<slug>/hero.mp4 */
  src: z.string().startsWith('/media/'),
  /** Public URL of the poster jpg (same folder). */
  poster: z.string().startsWith('/media/'),
  /** Width / height of the encoded clip, e.g. "3 / 4" for a portrait clip. Default: 16 / 9. */
  ratio: z.string().regex(/^\d+(\.\d+)?\s*\/\s*\d+(\.\d+)?$/).optional(),
});

export const collections = {
  projects: defineCollection({
    loader: glob({ pattern: '*/index.md', base: './src/content/projects', generateId: slugFromFolder }),
    schema: ({ image }) => {
      const picture = z.object({ image: image(), alt: biLoose, caption: biLoose });
      return z.object({
        /** Drafts are hidden from production builds (visible in `npm run dev` or with SHOW_DRAFTS=1). */
        draft: z.boolean().default(true),
        /** Ascending sort key on /projects/ (lower = first). */
        order: z.number().default(100),
        title: bi,
        summary: bi,
        client: z.string(),
        role: bi,
        period: z.coerce.string(), // "2024" or "Mar 2025 - Jul 2025"; a bare YAML number is accepted
        /** A plain string (shown in both languages) or { en, fr }. */
        location: z.union([z.string(), bi]),
        domains: z.array(z.enum(DOMAINS)).min(1),
        tools: z.array(z.string()).default([]),
        keyFigure: z.object({ value: z.string(), label: bi }).optional(),
        cover: image(),
        coverAlt: biLoose,
        /** Optional large image at the top of the project page; `cover` stays the card / share image and is the fallback. */
        hero: image().optional(),
        heroAlt: biLoose,
        heroClip: videoRef.optional(),
        /** Up to two landscape pictures stacked beside a portrait `heroClip`, so that the hero reads as one landscape block. */
        heroSide: z.array(picture).max(2).default([]),
        gallery: z.array(picture).default([]),
        drawings: z.array(picture).default([]),
        videos: z.array(videoRef.extend({ caption: biLoose })).default([]),
        /** Anchor used by <ProjectLink anchor="..."/> on the CV to add a "See project" link. */
        cvAnchor: z.string().optional(),
      });
    },
  }),

  projectsFr: defineCollection({
    loader: glob({ pattern: '*/index.fr.md', base: './src/content/projects', generateId: slugFromFolder }),
    schema: z.object({}),
  }),

  simulators: defineCollection({
    loader: glob({ pattern: '*/index.md', base: './src/content/simulators', generateId: slugFromFolder }),
    schema: ({ image }) =>
      z.object({
        draft: z.boolean().default(true),
        order: z.number().default(100),
        title: bi,
        summary: bi,
        status: z.enum(['delivered', 'in-development']),
        tech: z.array(z.string()).default([]),
        /** Optional card image. Falls back to the poster of the first clip. */
        cover: image().optional(),
        coverAlt: biLoose,
        learningGoal: bi,
        clips: z
          .array(
            z.object({
              slug: z.string().regex(/^[a-z0-9-]+$/),
              title: bi,
              caption: biLoose,
              src: z.string().startsWith('/media/'),
              poster: z.string().startsWith('/media/'),
              /** Free text, e.g. "0:12". */
              duration: z.string().optional(),
            }),
          )
          .default([]),
        /** Bilingual bullets: how it is built / what is technically interesting. */
        underTheHood: z.array(bi).default([]),
      }),
  }),

  simulatorsFr: defineCollection({
    loader: glob({ pattern: '*/index.fr.md', base: './src/content/simulators', generateId: slugFromFolder }),
    schema: z.object({}),
  }),
};
