---
name: variantes
description: Génère 10 variantes de photo de profil (LinkedIn, CV) à partir d'une photo portrait - recadrage centré sur le visage, retouche couleurs/netteté, détourage automatique, fonds flous, fonds studio unis (gris, bleu, clair), lumière chaude, éclairage latéral, spot, noir et blanc. Utiliser quand l'utilisateur invoque /variantes avec une photo, ou demande des variantes / déclinaisons d'une photo de profil.
---

# /variantes <photo> [dossier_sortie]

Produit 10 JPEG 1200×1200 et un aperçu `00_apercu.jpg` à partir d'une photo (HEIC, JPG, PNG, DNG).
Par défaut, la sortie va dans `variantes_<nom>/`, à côté de la photo.

Prérequis : macOS (Vision, swiftc) et ImageMagick (`magick`).

## Étapes

1. Lance le script (compter environ 1 min) :
   ```bash
   bash ~/.claude/skills/variantes/variantes.sh "<photo>" ["<dossier_sortie>"]
   ```
   Le script s'arrête avec un message s'il ne trouve aucun visage.
2. Ouvre `<dossier_sortie>/00_apercu.jpg` avec Read et vérifie :
   - le cadrage : tête entière, épaules visibles ;
   - le détourage sur les fonds unis 04, 05, 06 et 09 : pas de morceau de fond ni de bras coupé.
   Si le détourage est raté, dis-le à l'utilisateur et recommande plutôt 02 ou 03, où le fond reste flou et un défaut se voit moins.
3. Réponds en français et en peu de mots : le chemin du dossier, un tableau des 10 variantes, et ta recommandation (05 bleu ou 04 gris pour LinkedIn).

## Les 10 variantes

| Fichier | Fond | Sujet |
|---|---|---|
| 01_dezoomee | d'origine | retouché |
| 02_fond_flou_leger | flou léger | retouché |
| 03_fond_flou_fort_sombre | très flou, assombri | retouché |
| 04_fond_gris_studio | dégradé gris | retouché |
| 05_fond_bleu | dégradé bleu | retouché |
| 06_fond_clair | dégradé blanc cassé | retouché |
| 07_lumiere_chaude | flou, réchauffé | réchauffé |
| 08_eclairage_lateral | flou, assombri à droite | lumière venant de la gauche |
| 09_spot_studio | sombre avec vignette | légèrement éclairci |
| 10_noir_et_blanc | flou gris | N&B contrasté |

La retouche de base corrige la dominante orange (R×0,975, B×1,03), désature à 95 %, ajoute un léger contraste en S, de la clarté et de la netteté.
Le fond caché par la personne est reconstruit avant d'être flouté, ce qui évite le halo autour de la silhouette.

Pour ajuster une variante (autre couleur de fond, flou plus fort, etc.), modifie la ligne correspondante dans `variantes.sh` ou refais-la à la main avec `magick`, en suivant le même principe : fond, sujet, masque `m.png`, puis `-composite`.
