# Changelog

## v0.1.1 - no dates in paths
- Input is now `incoming/<post-slug>.<ext>` and output `img/<post-slug>/...` (same slug as `/article/<slug>/`).
Suggested commit message: `change: image paths use only the post slug, no dates`

## v0.1.0 - first release
- Image CDN repo: drop a file in `incoming/`, the workflow makes 480/800/1280 WebP + og.jpg (all 16:9) and deploys to GitHub Pages.
- Budgets: 1280w <= 100 KB, 800w <= 50 KB, 480w <= 22 KB, og.jpg <= 120 KB.
- Size report warns at 700 MB and fails at 900 MB (GitHub Pages limit is 1 GB).
Suggested commit message: `feat: image CDN repo with variant workflow and size report`
