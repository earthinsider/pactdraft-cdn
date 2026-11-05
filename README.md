# pactdraft-cdn

Images for PactDraft live here, NOT in the site repo. The site repo only holds code and posts.

## URL scheme (no dates, same slug as the article)
Article: `https://pactdraft.com/article/<slug>/`  ->  images: `https://cdn.pactdraft.com/img/<slug>/800.webp`
(also `480.webp`, `1280.webp`, `og.jpg`). Every image is exactly 16:9.
The site derives the image from the post slug and a host key: `c1` = this repo (`cdn.pactdraft.com`), later `c2` = `cdn-2.pactdraft.com`.
A slug must be unique and never change after publishing (no dates means a repeated slug would overwrite the old image).

## One-time setup
1. Create a PUBLIC repo `pactdraft-cdn` (GitHub Pages on the free plan needs a public repo), upload these files, branch `main`.
2. Settings -> Pages -> Source: **GitHub Actions**.
3. After you own the domain: rename `CNAME.example` to `CNAME`, add DNS `cdn` CNAME -> `<your-github-user-or-org>.github.io`
   and keep it **DNS only (grey cloud)**, then Settings -> Pages -> tick Enforce HTTPS.
   Until then the images work at `https://<user>.github.io/pactdraft-cdn/img/...`.
4. Create a fine-grained token (Contents: read/write, only this repo and the site repo) for n8n. Keep it in n8n credentials only.

## Add an image (n8n or by hand)
Upload the ORIGINAL image as `incoming/<post-slug>.png` (any size, PNG/JPG/WebP).
API: `PUT https://api.github.com/repos/<owner>/pactdraft-cdn/contents/incoming/<post-slug>.png`
body `{"message":"images: add <post-slug>","content":"<base64>","branch":"main"}`.
The workflow converts it and the image is live after ~1-2 minutes. Wrong file names go to `incoming/_rejected/`.

## Limits (GitHub Pages, free)
- Site size about 1 GB, soft bandwidth about 100 GB/month. About 210 KB per post -> roughly 2,500-3,000 images per repo.
- The workflow's size report warns at 700 MB and fails at 900 MB. Then create `pactdraft-cdn-2` (same files, host `cdn-2.pactdraft.com`)
  and tell the site that new posts use host key `c2`. Old posts keep working.
- `img/` holds one folder per post. GitHub's web page only lists the first 1,000 entries of a folder; the CDN itself is not affected.
- GitHub keeps history: never re-upload the same image again and again.
- Do not put Cloudflare's orange-cloud proxy in front of this host: images hosted outside Cloudflare are restricted on its free CDN.
  Upgrade path when traffic grows: Cloudflare R2 + custom domain (same URL scheme, only the host mapping in the site config changes).
