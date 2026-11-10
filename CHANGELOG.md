# Changelog

## v1.2.0 - any file extension
- Names may end in webp, jpg, jpeg, png, avif or gif. The workflow looks for the feature and card partner with any extension; hero warning limit is now 300 KB.
Suggested commit message: `change: accept any image extension in the checks`

## v1.1.0 - three images per article
- Added `image/feature/` and `image/card/` next to the hero `image/<slug>.webp`. The workflow warns about missing partners and about files over 150/80/40 KB.
Suggested commit message: `feat: feature and card image folders with checks`

## v1.0.0 - simple CDN
- Serves files exactly as uploaded: `image/<article-slug>.webp` -> `https://cdn.pactdraft.com/image/<article-slug>.webp`.
- No resizing, no variants, no scripts. The workflow only warns about wrong names or files over 150 KB and about repo size (700 MB warning, 900 MB stop).
Suggested commit message: `feat: simple image CDN repo`
