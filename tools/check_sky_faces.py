"""Check the prepared sky faces the uploaded skies were made from.

A Sky's six images become one cube texture, so they should all be square,
the same size and a plain 8-bit picture. The site's import scripts never
checked that for the 63 skies taken from sky mods. This lists every sky
whose faces break one of those rules, which is the next thing to rule out
if the skies still crash once their images are Open Use.

    python check_sky_faces.py "C:/path/to/rivals-skins/tools/skies/prepared"

Needs Pillow (pip install pillow).
"""
import os
import sys
from PIL import Image

FACES = ["bk", "dn", "ft", "lf", "rt", "up"]
MAX = 1024


def problems(folder):
    found, sizes = [], {}
    for face in FACES:
        path = os.path.join(folder, face + ".png")
        if not os.path.exists(path):
            found.append("%s missing" % face)
            continue
        with Image.open(path) as im:
            sizes[face] = im.size
            if im.mode not in ("RGB", "RGBA"):
                found.append("%s is %s, not RGB" % (face, im.mode))
            if im.info.get("interlace"):
                found.append("%s is interlaced" % face)
        w, h = sizes[face]
        if w != h:
            found.append("%s is not square (%dx%d)" % (face, w, h))
        if max(w, h) > MAX:
            found.append("%s is larger than %d (%dx%d)" % (face, MAX, w, h))
        if w & (w - 1) or h & (h - 1):
            found.append("%s is not a power of two (%dx%d)" % (face, w, h))
    if len(set(sizes.values())) > 1:
        found.append("faces differ in size: " + ", ".join("%s %dx%d" % (f, *sizes[f]) for f in FACES if f in sizes))
    return found, sizes


def main(argv):
    if not argv or not os.path.isdir(argv[0]):
        print(__doc__)
        return 1
    root, bad = argv[0], 0
    skies = sorted(d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d)))
    for sky in skies:
        found, sizes = problems(os.path.join(root, sky))
        size = sizes.get("ft")
        if found:
            bad += 1
            print("%-28s %s" % (sky, "; ".join(found)))
        else:
            print("%-28s ok (%dx%d)" % (sky, *size))
    print("\n%d of %d skies have face problems" % (bad, len(skies)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
