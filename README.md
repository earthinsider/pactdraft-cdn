# pactdraft-cdn

Images for PactDraft. **You upload one image per article; this repo's build makes the other two versions by itself.**

| URL | What it is | Used for |
|---|---|---|
| `https://cdn.pactdraft.com/image/<slug>.<ext>` | the original, exactly as uploaded | article hero, social preview, Discover |
| `https://cdn.pactdraft.com/image/feature/<slug>.<ext>` | 800x450, a bit compressed (about 25-35 KB) | the big first card on the home page |
| `https://cdn.pactdraft.com/image/card/<slug>.<ext>` | 480x270, compressed more (about 8-15 KB) | every small card: latest posts, sections with many posts, related posts |

## Rules
- Upload only `image/<article-slug>.<ext>` (lowercase letters, digits, hyphens; webp, jpg, jpeg or png work for all three versions; avif and gif stay original only and the site then uses the original).
- 16:9, about 1280x720, around 100 KB, compressed BEFORE upload. jpg or webp are best: a png is resized but does not get much smaller.
- The slug is checked in the SITE repo (not here), because images can live in several CDN repos over time.
- The feature and card files are made while the site is built (`scripts/make_variants.py`) and published, but they are NOT stored in git, so the repo only holds the originals. The workflow caches them, so only new or changed images are processed. A problem with one image never stops the deploy.
- Old folders `image/card/` and `image/feature/` from earlier tests are not used any more and can be deleted.

## One-time setup
1. Create a PUBLIC repo `pactdraft-cdn`, upload these files to branch `main`.
2. Settings -> Pages -> Source: **GitHub Actions**. Custom domain: `cdn.pactdraft.com`. Tick Enforce HTTPS when it is offered.
3. DNS: `cdn` CNAME -> `<github-user-or-org>.github.io`, **DNS only (grey cloud)** if the DNS is on Cloudflare.
4. n8n token: fine-grained, Contents read/write, only this repo and the site repo.

## n8n upload
`PUT /repos/<owner>/pactdraft-cdn/contents/image/<slug>.<ext>`  body `{"message":"image: <slug>","content":"<base64>","branch":"main"}`
To replace an existing file also send its `sha`. All three URLs are live about a minute or two later; until then the site shows the original.

## How many articles fit in one repo (GitHub Pages, free)
The published site (original + feature + card) should stay under about 1 GB. The workflow warns at 700 MB (our soft limit) and stops at 900 MB. Rough numbers, with about 35 KB + 12 KB added per article:

| Original | All three together | Articles at 700 MB | Articles at 1 GB |
|---|---|---|---|
| 60 KB | about 107 KB | about 6,700 | about 9,800 |
| 80 KB | about 127 KB | about 5,600 | about 8,200 |
| 100 KB | about 147 KB | about 4,900 | about 7,100 |

These are estimates. Every run prints the real numbers (size, articles, KB per article, how many more fit before 700 MB).
Bandwidth: GitHub's soft limit is about 100 GB per month, roughly 700,000 views of a 147 KB set; a card view costs only about 12 KB.
When a repo is nearly full: create `pactdraft-cdn-2` (same files), DNS `cdn-2`, add host `c2` in the site's `site.json`, and let n8n write `image: c2/<slug>.<ext>` for new articles. Never change the old articles. GitHub keeps history, so do not upload the same image again and again.

## Other notes
- Do not turn on Cloudflare's orange-cloud proxy for this host (free-plan rules restrict serving images hosted outside Cloudflare). Later upgrade path: Cloudflare R2 with the same URL scheme.
- GitHub Pages caches files for about 10 minutes; replaced images can look old for that long.
