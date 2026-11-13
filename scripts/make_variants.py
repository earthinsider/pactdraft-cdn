#!/usr/bin/env python3
"""Makes the feature and card versions of every image in image/ while the CDN site is built.

  image/<slug>.<ext>            the original, published exactly as uploaded
  image/feature/<slug>.<ext>    800x450, a bit compressed   -> the big first card on the home page
  image/card/<slug>.<ext>       480x270, compressed more    -> every small card (latest posts, sections with many posts)

The new files are written only into _site/image/... (the published site). They are NOT committed to git, so the repo keeps
the originals only. They are remembered in .cache/variants (the workflow caches that folder), so only new or changed
originals are processed. Supported types: jpg, jpeg, webp, png. For other types (avif, gif) no variants are made and the
site simply uses the original. A problem with one image never stops the build.
"""
import hashlib, io, json, shutil, sys
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC, CACHE, OUT = ROOT / "image", ROOT / ".cache/variants", ROOT / "_site/image"
KINDS = {"feature": (800, 45), "card": (480, 16)}      # target width, size budget in KB
SUPPORTED = {".jpg", ".jpeg", ".webp", ".png"}
VERSION = "v1"


def crop169(im):
    w, h = im.size
    if abs(w / h - 16 / 9) < 0.01:
        return im
    if w / h > 16 / 9:
        nw = round(h * 16 / 9); left = (w - nw) // 2
        return im.crop((left, 0, left + nw, h))
    nh = round(w * 9 / 16); top = int((h - nh) * 0.3)    # tall picture: keep more of the top
    return im.crop((0, top, w, top + nh))


def encode(im, ext, budget_kb):
    limit, data = budget_kb * 1024, b""
    if ext == ".png":
        for colors in (0, 128, 64, 32):
            buf = io.BytesIO()
            (im if colors == 0 else im.quantize(colors=colors, method=Image.MEDIANCUT)).save(buf, "PNG", optimize=True)
            data = buf.getvalue()
            if len(data) <= limit:
                break
        return data
    for q in (82, 76, 70, 64, 58, 52, 46, 40):
        buf = io.BytesIO()
        if ext == ".webp":
            im.save(buf, "WEBP", quality=q, method=6)
        else:
            im.save(buf, "JPEG", quality=q, optimize=True, progressive=True)
        data = buf.getvalue()
        if len(data) <= limit:
            break
    return data


def main():
    index_file = CACHE / "index.json"
    try:
        index = json.loads(index_file.read_text()) if index_file.exists() else {}
    except Exception:
        index = {}
    for k in KINDS:
        (CACHE / k).mkdir(parents=True, exist_ok=True)
        (OUT / k).mkdir(parents=True, exist_ok=True)
    originals = sorted(p for p in SRC.glob("*.*") if p.is_file() and p.name != "README.txt")
    names, new, cached, skipped, failed = set(), 0, 0, 0, []
    for p in originals:
        if p.suffix.lower() not in SUPPORTED:
            skipped += 1
            continue
        names.add(p.name)
        key = hashlib.sha1(p.read_bytes() + (VERSION + str(KINDS)).encode()).hexdigest()[:16]
        have = all((CACHE / k / p.name).exists() for k in KINDS)
        if not (index.get(p.name) == key and have):
            try:
                ext = p.suffix.lower()
                im = ImageOps.exif_transpose(Image.open(p))
                if im.mode in ("RGBA", "LA", "P"):
                    im = im.convert("RGBA"); bg = Image.new("RGBA", im.size, (255, 255, 255, 255)); bg.alpha_composite(im); im = bg
                base = crop169(im.convert("RGB"))
                for k, (width, kb) in KINDS.items():
                    w = min(width, base.width); h = round(w * 9 / 16)
                    (CACHE / k / p.name).write_bytes(encode(base.resize((w, h), Image.LANCZOS), ext, kb))
                index[p.name] = key; new += 1
            except Exception as e:
                print("::warning::could not make variants for %s: %s" % (p.name, e)); failed.append(p.name)
                index.pop(p.name, None)
                continue
        else:
            cached += 1
        for k in KINDS:
            shutil.copyfile(CACHE / k / p.name, OUT / k / p.name)
    for n in list(index):                                   # forget deleted originals
        if n not in names:
            index.pop(n)
            for k in KINDS:
                (CACHE / k / n).unlink(missing_ok=True)
    index_file.write_text(json.dumps(index))
    mb = sum(f.stat().st_size for k in KINDS for f in (OUT / k).glob("*.*")) / 1048576
    print("variants: %d originals | new %d, from cache %d, no variants for type %d, failed %d | feature+card files %.1f MB" % (len(originals), new, cached, skipped, len(failed), mb))


if __name__ == "__main__":
    sys.exit(main())
