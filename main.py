#!/usr/bin/env python3
"""Sum 25 Round 5 — entry copier (stdlib only, no Pillow).

Copies entry.png byte-identical to $MAKEFUN_OUTPUT_DIR if set,
else /output/entry.png. Run as:
    python3 render.py && MAKEFUN_OUTPUT_DIR=/output python3 main.py
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print("entry.png not found next to main.py; run render.py first",
              file=sys.stderr)
        return 1
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    # Accept either a directory or a full .png path.
    if outdir.endswith(".png"):
        dest = outdir
        os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
    else:
        os.makedirs(outdir, exist_ok=True)
        dest = os.path.join(outdir, "entry.png")
    shutil.copyfile(src, dest)
    print("copied", src, "->", dest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
