# Charte graphique Immo Décodé

| Dossier | Contenu |
| --- | --- |
| `charte-graphique.pdf` | La charte complète (9 pages). S'ouvre aussi dans Illustrator : chaque page devient un plan de travail modifiable. |
| `logo/` | Logos en SVG vectoriel : principal, horizontal, monogramme, négatif, monochromes, photo de profil. `logo/png/` : versions PNG prêtes à poster. |
| `logo/logo-principal-TEXTE-EDITABLE.svg` | Le logo avec du vrai texte (pas vectorisé), pour changer les mots. Installer d'abord les polices. |
| `illustrations/` | 12 pictos au trait (maison, clé, calculatrice, marteau, appareil photo…), en bleu nuit et terracotta, plus la planche complète. |
| `couleurs/` | Nuancier Illustrator `.ase` + les codes HEX, RVB et CMJN. |
| `polices/` | Fraunces et Inter en `.ttf` (licence libre OFL) : double-clic pour installer. |

## Dans Illustrator

1. **Installer les polices** du dossier `polices/` (double-clic sur chaque fichier, puis « Installer »).
2. **Ouvrir un logo ou un picto** : Fichier › Ouvrir › le fichier `.svg`. Tout est vectoriel : chaque lettre, le toit et la barre sont des objets séparés et nommés (`toit`, `immo`, `decode`, `barre`).
3. **Ajouter les couleurs** : Fenêtre › Nuancier › menu ☰ › Ouvrir une bibliothèque de nuances › Autre bibliothèque › `couleurs/immo-decode-nuancier.ase`.
4. **Enregistrer en .ai** : Fichier › Enregistrer sous › Adobe Illustrator (.ai).

Les pictos sont des **contours** (trait de 7 px, extrémités arrondies) : on peut changer l'épaisseur ou la couleur du trait, ou les vectoriser (Objet › Décomposer).

## Régénérer les fichiers

Les fichiers sont produits par `_source/build_brand.py` (logos, pictos, nuancier, polices) et `_source/export.js` (PDF et PNG) :

```bash
pip install fonttools brotli
python3 charte-graphique/_source/build_brand.py
node charte-graphique/_source/export.js
```

Si vous modifiez un fichier à la main dans Illustrator, ne relancez pas le script : il écraserait vos modifications.
