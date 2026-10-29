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
| `*-apercu.png` | Aperçus (polices de remplacement : Anton pour Impact, Zilla Slab pour Eroika Slab) |

Les groupes nommés du gabarit : `FOND`, `VAGUES`, `PHOTOS`, `TEXTES`, `PRIX`, `LOGO_MENTIONS`. Dans Illustrator, ils apparaissent dans le panneau Calques. Les cadres en pointillés de `PHOTOS` sont à remplacer par les photos détourées (Fichier > Importer).

## Typographies

- **Impact** : titres en capitales (« FORMULE », « DÉCOUVREZ L'OFFRE », pastilles produits, « 5% », « CARTE DE FIDÉLITÉ »).
- **Eroika Slab** (toujours, avec Impact : ce sont les deux seules polices) : accroches, prix, mots-clés (« Petit Déjeuner », « Boisson », « Dessert », « 5,50€ »).
- **Eroika Slab Bold Italic** : slogans et mentions (« Pour bien commencer la journée ! », « Pour seulement », « Photos non contractuelles »).

Si Illustrator signale Eroika Slab manquante, choisir la Eroika Slab installée dans Texte > Polices manquantes : les textes restent modifiables.

## Couleurs

| Nom | HEX | Usage |
|---|---|---|
| Chocolat | `#5C2E15` | vagues, bandeaux, titres sur fond clair |
| Chocolat foncé | `#3B1F0E` | contour des ovales cuivre, prix sur cuivre |
| Crème | `#FDF0E2` | fond principal, textes sur chocolat |
| Sable | `#EEDDC5` | fond clair alternatif |
| Caramel | `#C58243` | fond bas (pizza), liserés, étiquette fidélité |
| Turquoise | `#51A3A3` | **visuels froids uniquement** : pastilles, ovales de prix |
| Turquoise clair | `#6CBDB5` | reflet des dégradés turquoise |
| Orange → Rouge | `#E8721D` → `#E30F20` | promos chocs (OFFRE+, « pour seulement ») |
| Cuivre | `#8A4A1C` / `#D89D58` / `#F1C680` | dégradé métal des ovales de prix |

## Règles de composition

1. **Les vagues** structurent l'affiche : fond crème en haut, chocolat en bas (ou un bandeau chocolat ondulé en haut). Jamais de coupure droite.
2. **Prix** = ovale cuivre (prix de formule), turquoise (prix secondaires) ou orange-rouge (prix choc), toujours en Eroika Slab, légère rotation possible (-4° à +4°).
3. **Produits listés** = pastilles turquoise légèrement inclinées, reliées par des « + » chocolat épais.
4. **Photos** détourées, grandes, qui débordent sur la vague pour donner du relief.
5. **Bas d'affiche** : logo Galzin rond + badge « 5% carte de fidélité » + « Photos non contractuelles ». Ajouter « L'abus d'alcool… » dès qu'il y a de l'alcool.
6. **Température des couleurs** : produits chauds (pizza, café, viennoiseries, plats) = chocolat, caramel, cuivre, orange-rouge, **sans turquoise**. Le turquoise est réservé aux visuels froids (boissons froides, glaces, salades, fraîcheur).
7. Prix inconnus : livrer les ovales **vides**, jamais de « 0,00€ ».
8. Une affiche = une seule promesse lisible à 3 mètres : titre, offre, prix.

## Références validées (`references/`)

Les affiches finales validées sont rangées dans `references/`. À relire avant chaque nouvelle demande.

### Ce que montre la version finale de « La formule du matin » (`formule-matin-final-valide.jpg`)

- **Échelle XXL** : le titre en Impact remplit toute la largeur à côté du logo (logo en haut à gauche, titre à droite). L'accroche Eroika Slab (« du matin ») est énorme, en cuivre clair, entre deux groupes de **tirets épais**.
- **Photo produit héroïque** : le plateau occupe presque toute la largeur et **déborde du bord de page**. Il est posé sur une vague caramel qui évoque la table.
- **Prix géant** : l'ovale cuivre est très grand, à cheval sur la photo, et **déborde du bord droit**. Le prix est écrit en Eroika Slab noir/chocolat foncé.
- **Accroches secondaires en Eroika Slab non gras** (« Avec votre boisson chaude »), grandes, en crème, encadrées de tirets.
- **Filets verticaux épais** couleur cuivre pour séparer les choix (boissons).
- **Bloc du bas en deux cases** dans un cadre arrondi cuivre :
  - à gauche, le prix 4,80€ dans un grand ovale cuivre, la photo des viennoiseries et la mention « AU CHOIX » ;
  - à droite, la pastille caramel « FORMULE AVEC VIENNOISERIE » et « Avec un croissant / OU / Une Chocolatine » en Eroika Slab.
  - La pastille « +1€ » orange-rouge **chevauche le coin du cadre**, elle n'est pas dedans.
- **Moins de texte** : pas de ligne de composition, pas de badge fidélité quand la place manque. On garde l'essentiel lisible de loin.
- **Vocabulaire maison** : on dit **« Chocolatine »**, pas « pain au chocolat ».

### Leçons générales
1. Viser plus grand : moins d'éléments, chacun plus gros. Laisser photos et prix déborder des bords.
2. Fond chocolat plein + une vague caramel ou crème sous le produit héros : ça marche très bien pour les produits chauds.
3. Les tirets décoratifs autour des accroches Eroika Slab font partie du style.
4. En cas de référence fournie (même faite par IA), garder sa composition et la passer dans la charte : polices, logo, couleurs, ovales.

> La version à jour et autonome de cette charte est la Skill `.claude/skills/galzin-da/` (chargée automatiquement par Claude Code quand on demande un visuel Galzin).
