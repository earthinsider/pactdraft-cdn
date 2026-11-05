#!/usr/bin/env python3
"""Turn files dropped in incoming/ into responsive WebP variants + a social og.jpg.

Drop:    incoming/<post-slug>.<png|jpg|webp|gif|bmp|tiff>      (no dates anywhere)
Result:  img/<post-slug>/480.webp  800.webp  1280.webp  og.jpg  meta.json
Every image is cropped to exactly 16:9, so the site can reserve its space (no layout shift).
Size budgets: 1280w <= 100 KB, 800w <= 50 KB, 480w <= 22 KB, og.jpg <= 120 KB.
"""
import datetime, io, json, os, re, sys
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
INCOMING, IMG, OUT = ROOT / "incoming", ROOT / "img", ROOT / ".out"
NAME = re.compile(r"^([a-z0-9][a-z0-9-]{0,120})\.(png|jpe?g|webp|gif|bmp|tiff?)$", re.I)
WIDTHS = {480: 22 * 1024, 800: 50 * 1024, 1280: 100 * 1024}
OG_BUDGET = 120 * 1024


def to_rgb(im):
    if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
        im = im.convert("RGBA")
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255)); bg.alpha_composite(im)
        return bg.convert("RGB")
    return im.convert("RGB")


def crop_16x9(im):
    w, h = im.size
    if abs(w / h - 16 / 9) < 0.01:
        return im
    if w / h > 16 / 9:                                   # too wide: centre crop
        nw = round(h * 16 / 9); left = (w - nw) // 2
        return im.crop((left, 0, left + nw, h))
    nh = round(w * 9 / 16); top = int((h - nh) * 0.3)    # too tall: keep more of the top (faces)
    return im.crop((0, top, w, top + nh))


def encode(im, fmt, budget, qualities):
    data = b""
    for q in qualities:
        buf = io.BytesIO()
        if fmt == "WEBP": im.save(buf, "WEBP", quality=q, method=6)
        else: im.save(buf, "JPEG", quality=q, optimize=True, progressive=True)
        data = buf.getvalue()
        if len(data) <= budget:
            return data
    return data


def process(path, m):
    slug = m.group(1).lower()
    src = ImageOps.exif_transpose(Image.open(path))
    sw, sh = src.size
    base = crop_16x9(to_rgb(src))
    dest = IMG / slug
    dest.mkdir(parents=True, exist_ok=True)
    sizes = {}
    for w, budget in WIDTHS.items():
        if w != 480 and base.width < w * 0.9:            # never blow a tiny source up a lot
            continue
        data = encode(base.resize((w, round(w * 9 / 16)), Image.LANCZOS), "WEBP", budget, (84, 80, 76, 72, 68, 64, 60, 56, 52, 48, 44, 40))
        (dest / f"{w}.webp").write_bytes(data); sizes[w] = len(data)
    og = encode(base.resize((1280, 720), Image.LANCZOS), "JPEG", OG_BUDGET, (86, 82, 78, 74, 70, 66, 62, 58, 54))
    (dest / "og.jpg").write_bytes(og)
    meta = {"id": slug, "aspect": "16:9", "variants": sizes, "og_bytes": len(og),
            "source": [sw, sh], "created": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")}
    (dest / "meta.json").write_text(json.dumps(meta, indent=1))
    return meta


def reject(p, rejected):
    rej = INCOMING / "_rejected"; rej.mkdir(exist_ok=True); p.rename(rej / p.name); rejected.append(p.name)


def main():
    OUT.mkdir(exist_ok=True)
    ids, rows, rejected = [], [], []
    for p in sorted(INCOMING.iterdir()) if INCOMING.exists() else []:
        if p.name.startswith(".") or p.is_dir():
            continue
        m = NAME.match(p.name)
        if not m:
            print(f"::warning::rejected {p.name}: name must be the post slug, like my-post-slug.png (lowercase letters, digits, hyphens)")
            reject(p, rejected); continue
        try:
            meta = process(p, m)
        except Exception as e:                                # broken image: keep the run alive
            print(f"::warning::failed {p.name}: {e}")
            reject(p, rejected); continue
        p.unlink(); ids.append(meta["id"])
        rows.append(f"| {meta['id']} | " + ", ".join(f"{w}w {b // 1024} KB" for w, b in meta["variants"].items()) + f" | og {meta['og_bytes'] // 1024} KB |")
        print("ok", meta["id"], meta["variants"], "og", meta["og_bytes"])
    (OUT / "ids.txt").write_text("\n".join(ids))
    summary = "### Images processed: %d (rejected: %d)\n\n| id | variants | social |\n|---|---|---|\n%s\n" % (len(ids), len(rejected), "\n".join(rows))
    (OUT / "summary.md").write_text(summary)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as f: f.write(summary)


if __name__ == "__main__":
    sys.exit(main())
