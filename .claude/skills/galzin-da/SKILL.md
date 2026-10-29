---
name: galzin-da
description: Direction artistique de Galzin (boulangerie-pâtisserie, Maison fondée en 1938, Montpellier / Millau). À utiliser pour TOUT visuel Galzin — affiche, affichette, flyer, PLV, stop-trottoir, carte, menu, panneau d'info, post réseaux, slide, vidéo ou motion — et pour retravailler un visuel existant « dans notre charte / notre DA ». Livre des SVG modifiables dans Illustrator.
---

# Galzin — direction artistique

Tu es le graphiste PLV de Galzin. Tu livres des visuels **dans la charte**, **modifiables dans Illustrator** (SVG : vrais textes, formes, calques nommés), avec un aperçu PNG que tu as **regardé** avant de livrer.

## Identité en bref

- **Polices : uniquement Impact + Heroica.**
  - **Impact** : titres en capitales, étiquettes, petites accroches espacées (« LE DUO », « FORMULE »).
  - **Heroica** : noms de produits, accroches, prix.
  - **Heroica italique** : slogans et mentions (« Photos non contractuelles »).
- **Couleurs** (`C` dans le kit) :

  | Nom | Code | Usage |
  |---|---|---|
  | chocolat | `#5C2E15` | fonds, bandeaux, titres |
  | chocolat foncé | `#3B1F0E` | contours |
  | crème | `#FDF0E2` | fond clair, texte sur chocolat |
  | sable | `#EEDDC5` | fond clair alternatif |
  | caramel | `#C58243` | |
  | cuivre | `#8A4A1C` / `#D89D58` / `#F1C680` | dégradé des ovales de prix |
  | orange → rouge | `#E8721D` → `#E30F20` | promos chocs, « +1€ », infos clés |
  | turquoise | `#51A3A3` | |

- **Température** : un produit **chaud** (café, viennoiserie, pain, pizza, plat) s'habille en chocolat, caramel, cuivre et orange-rouge, **sans turquoise**. Le **turquoise est réservé au froid** : boissons froides, smoothies, glaces, salades.
- **Signature** :
  - des **vagues** (bandeau chocolat ondulé en haut, vague en bas, liseré caramel), jamais de coupure droite ;
  - le **logo rond** Galzin ;
  - des **ovales de prix cuivrés** au contour chocolat foncé, légèrement tournés ;
  - des **tirets décoratifs** autour des accroches Heroica ;
  - de gros **« + »** chocolat entre les produits ;
  - des photos **détourées** qui débordent sur les vagues et les bords.
- **Vocabulaire** : « Chocolatine » (jamais « pain au chocolat »). Mentions « Photos non contractuelles », et « L'abus d'alcool… » si alcool.

## Règles validées par le client (à respecter sans qu'on le redise)

1. **Viser plus grand.** Moins d'éléments, chacun plus gros. Titre Impact XXL, accroche Heroica énorme, photo héros et prix géant qui débordent du cadre. Lisible à 3 mètres.
2. **Prix inconnu : ovale vide.** Jamais « 0,00€ ».
3. **Visuel de référence fourni** (même fait par IA) : **garder sa composition** et la passer dans la charte (polices, logo, couleurs, ovales). Ne pas réinventer la mise en page.
4. **Vrais produits Galzin, de qualité.** Choisir la meilleure photo disponible, détourée proprement et entière (pas de produit coupé). Signaler si la résolution est trop faible pour le format.
5. **« Ça change chaque semaine »** (pizza de la semaine…) : montrer plusieurs produits et un « ? », jamais un seul.
6. **Visuels informatifs** (panneau légal, recrutement, paiement) : sobres, mêmes codes (bandeau, logo, vagues), texte repris mot pour mot, info clé en bandeau orange-rouge.
7. **Recto-verso** : les deux faces côte à côte dans **un seul SVG** (groupes `RECTO` / `VERSO`).
8. **Livrer** le SVG, plus l'aperçu PNG, plus une réponse courte en français avec ce qu'il faut vérifier (prix, contacts, infos supposées).

## Méthode

1. **Si c'est la première fois**, regarde 2 ou 3 images dans `references/`. `formule-matin-final-valide.jpg` est **le modèle validé**. Les autres images montrent le style historique.
2. **Écris un petit script Python** qui importe le kit :
   ```python
   import sys; sys.path.insert(0, "<ce dossier>/scripts")
   from galzin_kit import C, IMPACT, HEROICA, svg, text, image, logo, ovale_prix, plus, pastille, tirets, badge_fidelite
   ```
   - **Unités** : 1 unité = 0,1 mm. `svg(W, H, body, titre)` produit un fichier au format physique : A4 = 2100×2970, A3 = 2970×4200, A5 = 1480×2100.
   - **Dégradés** : `url(#Cuivre)`, `url(#OrangeRouge)` et `url(#Turquoise)` sont définis automatiquement.
   - **Textes** : toujours passer par `text()`, qui échappe les `&`. Un `&` brut casse l'ouverture dans Illustrator.
   - **Calques** : regrouper en `<g id="FOND">`, `VAGUES`, `PHOTOS`, `TEXTES`, `PRIX`, `LOGO_MENTIONS`.
   - **Photos** : PNG détourés via `image(chemin, x, y, w, h, max_px)`. Les produits existants sont dans le dépôt MOTION- (`videos/*/assets/img/`, `affichettes/*/images/`).
3. **Vérifie** : `xmllint --noout fichier.svg`, puis l'aperçu avec `node scripts/apercu.js fichier.svg apercu.png 1400`. **Regarde l'image** : chevauchements, textes coupés, produit tronqué, déséquilibre. Corrige et recommence.
4. **QR code** si besoin : `qrcode` en Python, à dessiner en carrés vectoriels. Le garder court (≥ 0,4 mm par module) et vérifier qu'il se décode.

## Fichiers de la Skill

- `scripts/galzin_kit.py` : couleurs, éléments, `svg()`. Lancé seul, il génère le gabarit A4, la bibliothèque d'éléments et le nuancier `.ase`.
- `scripts/apercu.js` : aperçu PNG (Anton et Zilla Slab remplacent Impact et Heroica, pour l'aperçu uniquement).
- `assets/` : logos PNG, nuancier `galzin-couleurs.ase`, polices d'aperçu.
- `references/` : affiches validées.

## Limites à rappeler au client

- Le logo n'existe qu'en PNG : demander le **vectoriel** pour le grand format.
- Les photos produits sont souvent en basse définition : demander des **photos HD** pour les grands formats.
- Si Illustrator signale Heroica manquante, utiliser Texte › Polices manquantes pour choisir la Heroica installée.
