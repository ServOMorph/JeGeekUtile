"""
Découpe les images du dossier banners/ au format 1200x300px (ratio 4:1).
Stratégie : redimensionne à largeur cible, puis crop vertical centré.

Usage : python scripts/crop_banners.py [--mode center|top|bottom]
"""

import os
import sys
import argparse
from PIL import Image

TARGET_W = 1200
TARGET_H = 300
BANNERS_DIR = os.path.join(os.path.dirname(__file__), "..", "site internet", "static", "images", "banners")


def crop_banner(img: Image.Image, mode: str) -> Image.Image:
    # Redimensionne en gardant la largeur cible
    scale = TARGET_W / img.width
    new_h = int(img.height * scale)
    img = img.resize((TARGET_W, new_h), Image.LANCZOS)

    if img.height <= TARGET_H:
        return img

    if mode == "top":
        y = 0
    elif mode == "bottom":
        y = img.height - TARGET_H
    else:  # center
        y = (img.height - TARGET_H) // 2

    return img.crop((0, y, TARGET_W, y + TARGET_H))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["center", "top", "bottom"], default="center",
                        help="Position du crop vertical (default: center)")
    args = parser.parse_args()

    folder = os.path.abspath(BANNERS_DIR)
    if not os.path.isdir(folder):
        print(f"Dossier introuvable : {folder}")
        sys.exit(1)

    files = [f for f in os.listdir(folder) if f.lower().endswith(".png")]
    if not files:
        print("Aucune image PNG trouvée.")
        sys.exit(0)

    for filename in sorted(files):
        path = os.path.join(folder, filename)
        img = Image.open(path).convert("RGBA")
        original_size = img.size

        result = crop_banner(img, args.mode)
        result.save(path, "PNG")
        print(f"{filename}: {original_size} -> {result.size}  [mode={args.mode}]")

    print(f"\n{len(files)} image(s) traitée(s).")


if __name__ == "__main__":
    main()
