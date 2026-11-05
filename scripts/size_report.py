#!/usr/bin/env python3
"""Prints how full this CDN repo is. GitHub Pages sites should stay under 1 GB."""
import os
from pathlib import Path
IMG = Path(__file__).resolve().parent.parent / "img"
SOFT, HARD = 700, 900                                          # MB
files = [f for f in IMG.rglob("*") if f.is_file() and f.name != ".gitkeep"]
mb = sum(f.stat().st_size for f in files) / 1048576
posts = len({f.parent for f in files if f.name == "meta.json"})
per = (mb / posts) if posts else 0.21
left = int(max(SOFT - mb, 0) / per) if per else 0
line = f"img/ = {mb:.1f} MB for {posts} images (~{per * 1024:.0f} KB each). Room before {SOFT} MB: about {left} more images."
print(line)
if os.environ.get("GITHUB_STEP_SUMMARY"):
    with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as f: f.write("\n**" + line + "**\n")
if mb > HARD:
    print(f"::error::CDN repo is over {HARD} MB: create pactdraft-cdn-2 now."); raise SystemExit(1)
if mb > SOFT:
    print(f"::warning::CDN repo passed {SOFT} MB: prepare pactdraft-cdn-2.")
