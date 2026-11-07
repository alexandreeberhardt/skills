#!/bin/bash
# Usage : variantes.sh <photo> [dossier_sortie]
# Génère 10 variantes 1200x1200 d'une photo de profil + 00_apercu.jpg
set -euo pipefail

IN="$1"
[ -f "$IN" ] || { echo "Fichier introuvable : $IN" >&2; exit 1; }
IN="$(cd "$(dirname "$IN")" && pwd)/$(basename "$IN")"
NAME="$(basename "${IN%.*}")"
OUT="${2:-$(dirname "$IN")/variantes_$NAME}"
mkdir -p "$OUT"; OUT="$(cd "$OUT" && pwd)"
HERE="$(cd "$(dirname "$0")" && pwd)"
FONT=/System/Library/Fonts/Supplemental/Arial.ttf

# Outils Vision compilés une seule fois
mkdir -p "$HERE/bin"
for t in visage detoure; do
  [ -x "$HERE/bin/$t" ] || swiftc -O "$HERE/$t.swift" -o "$HERE/bin/$t"
done

T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
cd "$T"

# 1. Image orientée en pleine résolution (sips en secours pour certains DNG)
if ! magick "$IN" -auto-orient -quality 97 full.jpg 2>/dev/null; then
  sips -s format jpeg "$IN" --out full.jpg >/dev/null
  magick mogrify -auto-orient full.jpg
fi
read -r W H <<< "$(magick identify -format "%w %h" full.jpg)"

# 2. Recadrage carré autour du visage (visage à 38 % du haut, largeur du carré = 3,4 x visage)
FACE="$("$HERE/bin/visage" full.jpg)" || { echo "Aucun visage détecté." >&2; exit 1; }
read -r FX FY FW FH <<< "$FACE"
read -r SIDE X0 Y0 < <(awk -v fx="$FX" -v fy="$FY" -v fw="$FW" -v fh="$FH" -v W="$W" -v H="$H" 'BEGIN{
  s = 3.4 * fw; m = (W < H ? W : H); if (s > m) s = m
  x = fx + fw/2 - s/2; y = fy + fh/2 - 0.38*s
  if (x < 0) x = 0; if (y < 0) y = 0
  if (x > W - s) x = W - s; if (y > H - s) y = H - s
  printf "%d %d %d\n", s, x, y }')

# 3. Retouche de base : couleurs, contraste, clarté, netteté
magick full.jpg -crop "${SIDE}x${SIDE}+${X0}+${Y0}" +repage \
  -channel R -evaluate multiply 0.975 -channel B -evaluate multiply 1.03 +channel \
  -modulate 100,95,100 -sigmoidal-contrast 1.8,50% -unsharp 0x40+0.2+0 \
  -resize 1600x1600 -unsharp 0x1.0+0.6+0.01 base.png

# 4. Détourage
"$HERE/bin/detoure" base.png mask.png
magick mask.png -colorspace gray -morphology Erode Disk:3 -blur 0x1.8 m.png
magick mask.png -colorspace gray -blur 0x1.2 -morphology Dilate Disk:12 -negate inv.png

# 5. Reconstruction du fond caché (flou normalisé multi-échelle)
magick base.png inv.png -compose Multiply -composite pre.png
for s in 3 9 40; do
  magick pre.png -resize 400x400 -blur 0x$s -resize 1600x1600! p.png
  magick inv.png -resize 400x400 -blur 0x$s -resize 1600x1600! a_$s.png
  magick a_$s.png -evaluate max 1 aa.png
  magick p.png aa.png -compose DivideSrc -composite n_$s.png
done
magick a_9.png -level 0,25% w9.png; magick a_3.png -level 0,25% w3.png
magick n_40.png n_9.png w9.png -composite f1.png
magick f1.png n_3.png w3.png -composite bg_fill.png
magick bg_fill.png -blur 0x10 bgA.png
magick bg_fill.png -resize 400x400 -blur 0x12 -resize 1600x1600! bgB.png

# 6. Fonds et éclairages
grad() { magick -size 1600x1600 -define gradient:center=800,560 -define gradient:extent=diagonal \
           radial-gradient:"$1"-"$2" -colorspace sRGB -type TrueColor "$3"; }
put()  { magick "$1" -colorspace sRGB -type TrueColor "$2" m.png -composite \
           -resize 1200x1200 -quality 93 "$OUT/$3.jpg"; }

magick base.png -resize 1200x1200 -quality 93 "$OUT/01_dezoomee.jpg"
put bgA.png base.png 02_fond_flou_leger
magick bgB.png -modulate 75,80,100 bg3.png;        put bg3.png base.png 03_fond_flou_fort_sombre
grad "#a8a8a8" "#3a3a3a" bg4.png;                  put bg4.png base.png 04_fond_gris_studio
grad "#7393b8" "#1a2c44" bg5.png;                  put bg5.png base.png 05_fond_bleu
grad "#f8f8f6" "#c9ccd1" bg6.png;                  put bg6.png base.png 06_fond_clair

magick base.png -channel R -evaluate multiply 1.04 -channel B -evaluate multiply 0.92 +channel -modulate 102,105 s7.png
magick bgB.png -channel B -evaluate multiply 0.9 +channel -modulate 95,105 bg7.png
put bg7.png s7.png 07_lumiere_chaude

magick -size 1600x1600 gradient:white-"#5a5a5a" -rotate 90 -flop g8.png
magick base.png g8.png -compose Multiply -composite tmp8.png
magick base.png tmp8.png -compose Blend -define compose:args=75 -composite -modulate 108 s8.png
magick bgB.png -modulate 60,80 g8.png -compose Multiply -composite bg8.png
put bg8.png s8.png 08_eclairage_lateral

grad white black vig.png
magick bgB.png -modulate 60,70 vig.png -compose Multiply -composite bg9.png
magick base.png -modulate 104 -sigmoidal-contrast 1.5,45% s9.png
put bg9.png s9.png 09_spot_studio

magick bgB.png -colorspace gray -modulate 85 bg10.png
magick base.png -colorspace gray -sigmoidal-contrast 3,50% s10.png
put bg10.png s10.png 10_noir_et_blanc

# 7. Aperçu
montage "$OUT"/[0-9][0-9]_*.jpg -font "$FONT" -pointsize 18 -set label '%t' \
  -geometry 380x380+6+6 -tile 5x "$OUT/00_apercu.jpg"
echo "$OUT"
