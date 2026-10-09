import { getImage } from 'astro:assets';
import type { ImageMetadata } from 'astro';

/**
 * Open Graph image for a page: the entry's cover, cropped to fill 1200x630 and encoded as JPEG at build time.
 * Returns the props to pass to <Base> (absolute URL), or `{}` when there is no cover (Base then keeps the CV's /og.png).
 * The file is only referenced from <meta>, which is why the prune step in astro.config.mjs scans HTML for file names.
 */
export async function ogImageProps(cover: ImageMetadata | undefined, alt: string, site: URL | undefined) {
  if (!cover) return {};
  const img = await getImage({ src: cover, width: 1200, height: 630, fit: 'cover', format: 'jpg', quality: 82 });
  return { ogImage: new URL(img.src, site).href, ogImageAlt: alt };
}
