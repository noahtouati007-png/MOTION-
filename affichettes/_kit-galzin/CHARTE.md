# Charte affiches Galzin — kit Illustrator

Ce dossier est la base de toutes les affiches Galzin. Chaque nouvelle affiche est livrée en **SVG modifiable dans Illustrator** (textes, formes, dégradés, calques), avec un aperçu PNG.

## Fichiers

| Fichier | Rôle |
|---|---|
| `galzin-gabarit-A4.svg` | Gabarit A4 prêt à décliner (Fichier > Ouvrir dans Illustrator) |
| `galzin-bibliotheque.svg` | Planche d'éléments à copier-coller : ovales de prix, pastilles, « + », vagues, badge fidélité, logo |
| `galzin-couleurs.ase` | Nuancier : panneau Nuances > menu > Ouvrir une bibliothèque de nuances > Autre bibliothèque |
| `galzin-logo.png` | Logo rond (intégré dans les SVG) |
| `build.py` | Script qui régénère les fichiers |
| `*-apercu.png` | Aperçus (polices de remplacement : Anton pour Impact, Zilla Slab pour Heroica) |

Les groupes nommés du gabarit : `FOND`, `VAGUES`, `PHOTOS`, `TEXTES`, `PRIX`, `LOGO_MENTIONS`. Dans Illustrator, ils apparaissent dans le panneau Calques. Les cadres en pointillés de `PHOTOS` sont à remplacer par les photos détourées (Fichier > Importer).

## Typographies

- **Impact** : titres en capitales (« FORMULE », « DÉCOUVREZ L'OFFRE », pastilles produits, « 5% », « CARTE DE FIDÉLITÉ »).
- **Heroica** : accroches, prix, mots-clés (« Petit Déjeuner », « Boisson », « Dessert », « 5,50€ »).
- **Heroica italique** : slogans et mentions (« Pour bien commencer la journée ! », « Pour seulement », « Photos non contractuelles »).

Si Illustrator signale Heroica manquante, choisir la Heroica installée dans Texte > Polices manquantes : les textes restent modifiables.

## Couleurs

| Nom | HEX | Usage |
|---|---|---|
| Chocolat | `#5C2E15` | vagues, bandeaux, titres sur fond clair |
| Chocolat foncé | `#3B1F0E` | contour des ovales cuivre, prix sur cuivre |
| Crème | `#FDF0E2` | fond principal, textes sur chocolat |
| Sable | `#EEDDC5` | fond clair alternatif |
| Caramel | `#C58243` | fond bas (pizza), liserés, étiquette fidélité |
| Turquoise | `#51A3A3` | pastilles produits, ovales de prix |
| Turquoise clair | `#6CBDB5` | reflet des dégradés turquoise |
| Orange → Rouge | `#E8721D` → `#E30F20` | promos chocs (OFFRE+, « pour seulement ») |
| Cuivre | `#8A4A1C` / `#D89D58` / `#F1C680` | dégradé métal des ovales de prix |

## Règles de composition

1. **Les vagues** structurent l'affiche : fond crème en haut, chocolat en bas (ou un bandeau chocolat ondulé en haut). Jamais de coupure droite.
2. **Prix** = ovale cuivre (prix de formule), turquoise (prix secondaires) ou orange-rouge (prix choc), toujours en Heroica, légère rotation possible (-4° à +4°).
3. **Produits listés** = pastilles turquoise légèrement inclinées, reliées par des « + » chocolat épais.
4. **Photos** détourées, grandes, qui débordent sur la vague pour donner du relief.
5. **Bas d'affiche** : logo Galzin rond + badge « 5% carte de fidélité » + « Photos non contractuelles ». Ajouter « L'abus d'alcool… » dès qu'il y a de l'alcool.
6. Prix inconnus : livrer les ovales **vides**, jamais de « 0,00€ ».
7. Une affiche = une seule promesse lisible à 3 mètres : titre, offre, prix.
