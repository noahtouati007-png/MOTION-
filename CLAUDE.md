# MOTION- — Contexte pour Claude (à lire en premier)

Ce dépôt contient tout le travail **motion design et print** réalisé pour **Galzin** (boulangerie-pâtisserie,
Maison fondée en 1938, Montpellier / Millau, site : galzin.fr), ainsi que quelques autres projets
(Immo Décodé, BUT × ÉCHO, bannières LinkedIn). Branche principale : `main`. Il a été repris depuis un autre compte Claude : ce fichier résume ce qui a été
décidé pendant les sessions précédentes pour qu'on continue exactement dans le même style.

Langue : l'utilisateur parle **français** — réponds en français, textes à l'écran en français.

## Outils et skills

- Toutes les vidéos sont des projets **HyperFrames** (HTML + GSAP, rendu MP4 via le CLI `hyperframes`).
- Les skills sont versionnées dans le dépôt (`.claude/skills/`, `.agents/skills/`, liste dans
  `skills-lock.json`). Pour toute demande vidéo, commence par le skill **`/hyperframes`**, qui route vers
  `motion-graphics`, `general-video`, `media-use`, `hyperframes-audio`, etc.
- Chaque projet a son propre `CLAUDE.md` / `AGENTS.md` (règles HyperFrames) et un `hyperframes.json`.
- Pour mettre à jour les skills : `npx hyperframes skills update`.
- **`galzin-da`** (`.claude/skills/galzin-da/`, copie zippée `galzin-da-skill.zip`) : la direction
  artistique officielle Galzin. **À charger pour tout visuel Galzin** (affiche, PLV, menu, vidéo…).
  C'est la référence pour la charte — elle prime sur la section « Charte visuelle » ci-dessous.
- `illustrator` : Illustrator via MCP (nécessite Illustrator ouvert sur l'ordinateur de l'utilisateur).
- `replica-*` : pack de skills pour cloner / reconstruire une app (sans rapport avec Galzin).
- Voix off : connecteur **ElevenLabs** (à reconnecter sur le compte, avec le même compte ElevenLabs).
- Guide d'édition manuelle dans Studio (pour l'utilisateur) : `GUIDE-MONTAGE.md`.

## Arborescence

```
videos/<projet>/           un projet HyperFrames par vidéo
  index.html               la composition
  assets/img|fonts|vendor  images détourées, polices woff2 locales, gsap.min.js
  audio/                   voix.wav, musique.wav, sfx.wav, mix.wav, mix-sans-voix.wav (+ prises ElevenLabs)
  renders/                 MP4 finaux (versionnés malgré .gitignore → `git add -f`)
affichettes/               PLV Galzin imprimables (affiches, stickers, menus, panneaux) — kit dans `_kit-galzin/`
print/                     étiquettes prix (SVG/PDF modifiables dans Illustrator)
charte-graphique/          charte Immo Décodé (logos, polices Fraunces/Inter, .ai)
dossier-strategique/       dossier stratégique Immo Décodé (web + PDF A4)
banniere-linkedin-noah/    bannières LinkedIn de l'utilisateur
references/                vidéo TikTok de référence + son (à déposer par l'utilisateur)
mon-premier-montage/       projet d'entraînement pour Studio
```

## Charte visuelle Galzin

**Charte officielle (skill `galzin-da`)** : polices **Impact** (titres en capitales, étiquettes) +
**Eroika Slab** (produits, accroches, prix ; Bold Italic pour slogans/mentions). Couleurs chocolat
`#5C2E15`, crème `#FDF0E2`, sable `#EEDDC5`, caramel `#C58243`, cuivre `#8A4A1C`→`#F1C680`,
orange→rouge `#E8721D`→`#E30F20`, turquoise `#51A3A3` (réservé au froid). Vagues, logo rond,
ovales de prix cuivrés, « Chocolatine » (jamais « pain au chocolat »). Détails et règles validées
par le client dans `.claude/skills/galzin-da/SKILL.md`.

**Ce que les vidéos existantes utilisent** (avant la formalisation de la charte) :

- **Polices** (fichiers woff2 locaux dans chaque projet, pas de Google Fonts en ligne) :
  - **Crimson Pro** (600 italique / 700) — titres élégants, police principale
  - **Bebas Neue** — prix, gros chiffres, bandeaux
  - **Dancing Script** 700 — touches manuscrites (« fait maison », accroches)
  - Ponctuellement : Anton, Montserrat, Zilla Slab
- **Couleurs récurrentes** (variables CSS dans chaque `index.html`) :
  - Crème / papier : `#fdf0e3`, `#f6efe4`, `#fffaf2`
  - Encre / chocolat : `#2a1d12`, `#3a2213`, `#5b2f15`, `#4a2a17`
  - Jaune accent : `#ffcc4d` (le plus utilisé) · orange `#f2a531`
  - Bronze / doré : `#b0743d` → `#f2c890`, `#ffcf8a`
  - Promo chaude : `#f07a1e` → `#e3001b` · vert `#2e7d4f` · teal `#4b9b98`/`#7cc7bb`
  - Fond prune (certaines pubs) : `#5e1d52` → `#22081f`
- **Logo** : `assets/img/galzin-logo.png` (copié dans chaque projet).
- **Photos produits** : vraies photos Galzin détourées proprement (PNG transparents). Soigner les
  détourages (pas d'assiette ni de croûte coupée) — l'utilisateur y est attentif.
- Prix au format français : `5,50 €`.

## Formats

| Usage | Taille | Durée type |
|---|---|---|
| Pubs écran TV en boutique | 1920×1080 | 15 s (cartes/menus 22–30 s, boucle affiches 1m45–2m27) |
| TikTok / Reels | 1080×1920, 30 i/s | ~23 s |
| End card verticale (s'abonner / cloche / commenter) | 1080×1920 | 4 s (`galzin-outro`) |
| Overlay (fond transparent) | 1080×1920 | MOV/WebM transparents + version fond vert (`galzin-beignet-pop`) |

Les pubs TV doivent pouvoir **tourner en boucle** : vraie end card + fondu de sortie.

## Audio / voix off (TikTok)

- Voix ElevenLabs française, ton chaleureux et **calme** (voix utilisée : « Chloé – Warm, Friendly
  & UGC Ready » pour la fidélité ; voix plus posée pour `galzin-commande`).
- Lire le texte d'une traite, puis découper sur les pauses et caler chaque phrase sur sa scène.
- **Prononciation de « Galzin »** : nasale (« gal-zin » comme « vin »). Pour l'obtenir, on a testé
  l'orthographe phonétique « Galzain » dans le texte envoyé à ElevenLabs (prises dans
  `videos/galzin-commande/audio/elevenlabs/`). « galzin.fr » se dit « galzin point FR ».
- Mixage : niveler la voix phrase par phrase, **musique baissée sous la voix (ducking doux et
  régulier)**, effets sonores (whoosh, clic, bip, ding, succès) calés à l'image, fondu musique à la fin.
- Livrer à chaque fois 3 versions : `…-voix-off.mp4`, version musique + effets sans voix,
  `…-sans-audio.mp4`, plus les pistes séparées (48 kHz) dans `audio/`.
- Exemple complet avec timecodes : `videos/galzin-fidelite-tiktok/RECAP-TIMECODE.md`.

## Projets existants

- **Pubs TV 15 s** : `galzin-3plus1` (croissant/chocolatine), `galzin-americain`, `galzin-baguette`
  (par 2), `galzin-tielles` (lot 3+1), `galzin-pizza` (variantes rouge/marron), `galzin-pizza-semaine`,
  `galzin-menu` / `galzin-menu-plateau` / `galzin-menu-affiche` (« Compose ton menu » 5,50 €),
  `galzin-plus` / `galzin-plus-sandwich` (offre plus), `galzin-prix-garantis`, `galzin-sandwich-panini`,
  `galzin-salade-wrap`, `galzin-fidelite`, `galzin-happy-hour`, `galzin-petit-dej` (tartine).
- **Cartes TV** : `galzin-carte-pizzas` (30 s), `galzin-carte-sandwichs` (22 s).
- **Boucle affiches 3e écran** : `galzin-affiches`.
- **TikTok** : `galzin-fidelite-tiktok` (activer sa carte sur galzin.fr, vraies pages du site sur un
  ordinateur portable), `galzin-commande` (comment commander, 23 s).
- **Galette des rois** : `galzin-minions-tiktok` (22 s), `galzin-minions-tv` (15 s) — Galzin × Les Minions.
- **Divers** : `galzin-outro` (end card), `galzin-beignet-pop` (overlay Halloween).
- **PLV / print** (`affichettes/`) : petit-déj A5, formule matin A3, pizza de la semaine A3, menus
  boissons chaudes/fraîches, stop-trottoir, stickers (Wi-Fi, allergènes, table), flyer recrutement,
  panneaux (paiement, WC, toilettes hors service, vidéosurveillance, poubelle Balaruc), étiquettes
  internes (envoi Millau, four Unox). `print/lot-2-pains-speciaux` : étiquette prix 4€50.

## Autres projets (hors Galzin)

- **Immo Décodé** : `charte-graphique/`, `dossier-strategique/`, vidéos `videos/immo-decode-*`.
- **BUT × ÉCHO** : `videos/but-echo-ia` (16:9, ~152 s, voix ElevenLabs féminine, prononciation « BUT » corrigée).
- **Bannières LinkedIn** : `banniere-linkedin-noah/`.

## Façon de travailler

- Proposer d'abord un storyboard / quelques images clés pour validation, puis rendre.
- Vérifier visuellement (snapshots HyperFrames) avant de livrer.
- Pour un nouveau projet, partir du projet existant le plus proche (copier polices, logo, gsap).
- Commiter chaque vidéo avec un message clair en anglais (`Add Galzin … TV ad (15s)`), puis pousser.
