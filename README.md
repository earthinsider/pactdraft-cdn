# pactdraft-cdn

Images for PactDraft. Simple on purpose: **the file you upload is the file that is served.**

Three ready-made files per article:

| File | URL | Used for | Aim for |
|---|---|---|---|
| `image/<slug>.<ext>` | `https://cdn.pactdraft.com/image/<slug>.<ext>` | hero on the article page, social preview and Discover (original size, original file type) | 1280x720 or larger |
| `image/feature/<slug>.<ext>` | `.../image/feature/<slug>.<ext>` | the big featured card on the home page | 800x450, 25-55 KB |
| `image/card/<slug>.<ext>` | `.../image/card/<slug>.<ext>` | every small card (latest, categories, related) | 480x270, 8-20 KB |

If a feature or card file is missing, the site falls back to the hero file, and the workflow prints a warning.

## Rules
- File name = the article slug (lowercase letters, digits, hyphens) + `.webp`.
- The extension is whatever you upload (webp, jpg, png, avif, gif) and is written in the article front matter (`image: c1/<slug>.<ext>`). The feature and card files should have the same extension, or the article says otherwise with `imageFeatureExt` / `imageCardExt`.
- All three are 16:9 and compressed BEFORE upload; the CDN never resizes anything.
- The slug is checked in the SITE repo (not here), because images can live in several CDN repos over time.

## One-time setup
1. Create a PUBLIC repo `pactdraft-cdn`, upload these files to branch `main`.
2. Settings -> Pages -> Source: **GitHub Actions**. Custom domain: `cdn.pactdraft.com`. Tick Enforce HTTPS when it is offered.
3. DNS: `cdn` CNAME -> `<github-user-or-org>.github.io`, **DNS only (grey cloud)** if the DNS is on Cloudflare.
4. n8n token: fine-grained, Contents read/write, only this repo and the site repo.

## n8n upload
Three calls: `PUT /repos/<owner>/pactdraft-cdn/contents/image/<slug>.<ext>`, `.../image/feature/<slug>.<ext>`, `.../image/card/<slug>.<ext>`, each with body `{"message":"image: <slug>","content":"<base64>","branch":"main"}`.
To replace an existing file also send its `sha`. The image is live about a minute later (the workflow redeploys; bursts are merged).

## Limits (GitHub Pages, free)
- About 1 GB per site and a soft 100 GB/month bandwidth. At about 130 KB for all three files of an article that is roughly 7,000 articles per repo.
- The workflow warns at 700 MB and stops at 900 MB. Then create `pactdraft-cdn-2` (same files), DNS `cdn-2`, add host `c2` in the site's `site.json`, and let n8n write `image: c2/<slug>` for new articles. Never change the old articles.
- GitHub keeps history, so do not upload the same image again and again.
- Do not turn on Cloudflare's orange-cloud proxy for this host (free-plan rules restrict serving images hosted outside Cloudflare). Later upgrade path: Cloudflare R2 with the same URL scheme.
- GitHub Pages caches files for about 10 minutes; replaced images can look old for that long.
