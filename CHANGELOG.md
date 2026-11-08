# Changelog

## v1.0.0 - simple CDN
- Serves files exactly as uploaded: `image/<article-slug>.webp` -> `https://cdn.pactdraft.com/image/<article-slug>.webp`.
- No resizing, no variants, no scripts. The workflow only warns about wrong names or files over 150 KB and about repo size (700 MB warning, 900 MB stop).
Suggested commit message: `feat: simple image CDN repo`
