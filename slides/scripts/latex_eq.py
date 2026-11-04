#!/usr/bin/env python3
"""Renders slide equations with LaTeX into small transparent PNGs, in the deck's focus blue.

    python3 latex_eq.py eqs.json --out <dir> [--scale 1.3] [--colors 64]

eqs.json maps a file name to the LaTeX of one equation block (math mode, no $):

    {"09_model": "\\begin{aligned} y &= a x + b \\\\ z &= \\arctan(c x) \\end{aligned}",
     "10_energy": {"tex": "E = \\tfrac12 k x^2", "scale": 1.5}}

An entry can be a string or {"tex": ..., "scale": ...}. The scale sets the printed size: 1.0 is
LaTeX's 12 pt, 1.3 (default) matches 16 pt body text, 1.5 suits a single key equation, 1.2 two
blocks stacked in a tight column.

For each entry it writes <dir>/<name>.png (300 dpi, palette PNG, a few KB) and prints its size on
the slide. <dir>/manifest.json holds, per name, the pixel size, the width and height in EMU at
its scale, and the length of its base64 text. <dir>/sheet.png stitches every equation on white
so they can be checked in one look.

Needs latex and dvipng (TeX Live / MacTeX) and Pillow.
"""
import argparse
import base64
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

FOCUS = "2A5FA8"
DPI = 300
EMU_PER_PX_AT_1 = 914400 / DPI  # one pixel at scale 1.0
TEMPLATE = r"""\documentclass[border=4pt,12pt]{standalone}
\usepackage{amsmath,amssymb,xcolor}
\definecolor{focus}{HTML}{%s}
\begin{document}\color{focus}$\displaystyle %s$\end{document}
"""


def render(name, tex, out, colors):
    from PIL import Image

    with tempfile.TemporaryDirectory() as tmp:
        src = pathlib.Path(tmp) / "eq.tex"
        src.write_text(TEMPLATE % (FOCUS, tex))
        run = subprocess.run(["latex", "-interaction=nonstopmode", "-halt-on-error", "eq.tex"],
                             cwd=tmp, capture_output=True, text=True, timeout=60)
        if run.returncode != 0:
            errors = [line for line in run.stdout.splitlines() if line.startswith("!")]
            sys.exit(f"{name}: LaTeX failed: {' / '.join(errors) or run.stdout[-400:]}")
        raw = pathlib.Path(tmp) / "eq.png"
        subprocess.run(["dvipng", "-q", "-D", str(DPI), "-T", "tight", "-bg", "Transparent",
                        "-o", str(raw), "eq.dvi"], cwd=tmp, check=True, capture_output=True, timeout=60)
        image = Image.open(raw).convert("RGBA")
        # A palette without dithering keeps the strokes crisp and the file a few KB, which keeps
        # the base64 short enough to upload through the Drive connector.
        image = image.quantize(colors=colors, method=Image.FASTOCTREE, dither=Image.Dither.NONE)
        target = out / f"{name}.png"
        image.save(target, optimize=True)
        return target, image.size


def contact_sheet(paths, out):
    from PIL import Image

    images = [Image.open(p).convert("RGBA") for p in paths]
    width = max(i.width for i in images) + 40
    height = sum(i.height + 40 for i in images) + 20
    sheet = Image.new("RGB", (width, height), "white")
    y = 20
    for image in images:
        sheet.paste(image, (20, y), image)
        y += image.height + 40
    sheet.save(out / "sheet.png")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("spec")
    parser.add_argument("--out", required=True)
    parser.add_argument("--scale", type=float, default=1.3)
    parser.add_argument("--colors", type=int, default=64,
                        help="palette size; 6 gives a shorter base64 if an upload is refused")
    args = parser.parse_args()

    for tool in ("latex", "dvipng"):
        if not shutil.which(tool):
            sys.exit(f"{tool} not found: install MacTeX or TeX Live, or keep the equations as text")

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    spec = json.loads(pathlib.Path(args.spec).read_text())
    manifest, paths = {}, []
    for name, entry in spec.items():
        tex, scale = (entry, args.scale) if isinstance(entry, str) else (entry["tex"], entry.get("scale", args.scale))
        path, (w, h) = render(name, tex, out, args.colors)
        paths.append(path)
        emu = EMU_PER_PX_AT_1 * scale
        manifest[name] = {"file": str(path), "px": [w, h], "scale": scale,
                          "width_emu": round(w * emu), "height_emu": round(h * emu),
                          "base64_chars": len(base64.b64encode(path.read_bytes()))}
        m = manifest[name]
        print(f"{name}: {m['width_emu'] / 914400:.2f} x {m['height_emu'] / 914400:.2f} in "
              f"({m['width_emu']} x {m['height_emu']} EMU), base64 {m['base64_chars']} chars")
    (out / "manifest.json").write_text(json.dumps(manifest, indent=1))
    contact_sheet(paths, out)
    print(f"check {out / 'sheet.png'}")


if __name__ == "__main__":
    main()
