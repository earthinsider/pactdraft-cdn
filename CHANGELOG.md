# Changelog

## v2.0.0 - feature and card made at deploy time
- `scripts/make_variants.py` builds `image/feature/` (800x450) and `image/card/` (480x270) into the published site only; cached by the workflow; never fails the deploy. The size report counts the published size.
Suggested commit message: `feat: build feature and card images at deploy time from the one upload`

## v1.3.0 - one image per article
- Back to one file per article. The workflow warns about bad names and files over 150 KB and prints the average size and how many more images fit before 700 MB.
Suggested commit message: `change: one image per article, capacity report`

## v1.2.1 - folders exist from the start
- `image/feature/` and `image/card/` come with a README.txt so the folders exist after the first upload (Git does not keep empty folders).
Suggested commit message: `fix: create feature and card folders`

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
