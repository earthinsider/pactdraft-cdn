# pactdraft-cdn

Images for PactDraft. Simple on purpose: **the file you upload is the file that is served, one image per article.**

`image/<article-slug>.<ext>`  ->  `https://cdn.pactdraft.com/image/<article-slug>.<ext>`

## Rules
- File name = the article slug (lowercase letters, digits, hyphens) + the extension of the file (webp, jpg, jpeg, png, avif, gif). The extension is also written in the article front matter (`image: c1/<slug>.<ext>`).
- 16:9, about 1280x720, under 100 KB on average, compressed BEFORE upload. The CDN never resizes anything.
- The slug is checked in the SITE repo (not here), because images can live in several CDN repos over time.
- Small cards: the site either uses this same file, or (site.json -> `images.thumbs: true`) makes its own small pictures at build time and keeps them on the main site. Nothing extra to upload here.

## One-time setup
1. Create a PUBLIC repo `pactdraft-cdn`, upload these files to branch `main`.
2. Settings -> Pages -> Source: **GitHub Actions**. Custom domain: `cdn.pactdraft.com`. Tick Enforce HTTPS when it is offered.
3. DNS: `cdn` CNAME -> `<github-user-or-org>.github.io`, **DNS only (grey cloud)** if the DNS is on Cloudflare.
4. n8n token: fine-grained, Contents read/write, only this repo and the site repo.

## n8n upload
`PUT /repos/<owner>/pactdraft-cdn/contents/image/<slug>.<ext>`  body `{"message":"image: <slug>","content":"<base64>","branch":"main"}`
To replace an existing file also send its `sha`. The image is live about a minute later (the workflow redeploys; bursts are merged).

## How many images fit in one repo (GitHub Pages, free)
A Pages site should stay under about 1 GB. The workflow warns at 700 MB (our soft limit) and stops at 900 MB.

| Average image size | Images at the 700 MB soft limit | Images at 1 GB |
|---|---|---|
| 60 KB | about 11,900 | about 17,000 |
| 80 KB | about 8,900 | about 12,800 |
| 100 KB | about 7,100 | about 10,200 |

Every run prints the real numbers: size, image count, average size and how many more fit before 700 MB.
Bandwidth: GitHub's soft limit is about 100 GB per month, which is roughly 1 million downloads of a 100 KB image.
When a repo is nearly full: create `pactdraft-cdn-2` (same files), DNS `cdn-2`, add host `c2` in the site's `site.json`, and let n8n write `image: c2/<slug>.<ext>` for new articles. Never change the old articles. GitHub keeps history, so do not upload the same image again and again.

## Other notes
- Do not turn on Cloudflare's orange-cloud proxy for this host (free-plan rules restrict serving images hosted outside Cloudflare). Later upgrade path: Cloudflare R2 with the same URL scheme.
- GitHub Pages caches files for about 10 minutes; replaced images can look old for that long.
- Old `image/card/` and `image/feature/` folders from earlier tests are not used any more and can be deleted.
