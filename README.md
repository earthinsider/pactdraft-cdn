# pactdraft-cdn

Images for PactDraft. Simple on purpose: **the file you upload is the file that is served.**

`image/<article-slug>.webp`  ->  `https://cdn.pactdraft.com/image/<article-slug>.webp`

## Rules
- File name = the article slug (lowercase letters, digits, hyphens) + `.webp`.
- Compress BEFORE upload. 16:9, about 1280x720, 40-90 KB. The same file is used for the hero, the home page cards and the social preview.
- The slug is checked in the SITE repo (not here), because images can live in several CDN repos over time.

## One-time setup
1. Create a PUBLIC repo `pactdraft-cdn`, upload these files to branch `main`.
2. Settings -> Pages -> Source: **GitHub Actions**. Custom domain: `cdn.pactdraft.com`. Tick Enforce HTTPS when it is offered.
3. DNS: `cdn` CNAME -> `<github-user-or-org>.github.io`, **DNS only (grey cloud)** if the DNS is on Cloudflare.
4. n8n token: fine-grained, Contents read/write, only this repo and the site repo.

## n8n upload
`PUT /repos/<owner>/pactdraft-cdn/contents/image/<slug>.webp`  body `{"message":"image: <slug>","content":"<base64>","branch":"main"}`
To replace an existing image also send its `sha`. The image is live about a minute later (the workflow redeploys; bursts are merged).

## Limits (GitHub Pages, free)
- About 1 GB per site and a soft 100 GB/month bandwidth. At about 70 KB per image that is roughly 10,000 images per repo.
- The workflow warns at 700 MB and stops at 900 MB. Then create `pactdraft-cdn-2` (same files), DNS `cdn-2`, add host `c2` in the site's `site.json`, and let n8n write `image: c2/<slug>` for new articles. Never change the old articles.
- GitHub keeps history, so do not upload the same image again and again.
- Do not turn on Cloudflare's orange-cloud proxy for this host (free-plan rules restrict serving images hosted outside Cloudflare). Later upgrade path: Cloudflare R2 with the same URL scheme.
- GitHub Pages caches files for about 10 minutes; replaced images can look old for that long.
