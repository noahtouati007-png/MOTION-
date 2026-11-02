# Série de vidéos « conseil » Immo Décodé

Chaque vidéo est générée à partir d'une entrée de `conseils.json` :

```json
{
  "slug": "07-mon-nouveau-conseil",
  "categorie": "immo",
  "accroche": "Le titre affiché dès la première image",
  "sous_titre": "Une phrase en italique sous le titre",
  "icone": "maison",
  "points": [
    { "titre": "Titre court", "detail": "Une phrase d'explication.", "icone": "cle" }
  ],
  "a_retenir": "La phrase à retenir.",
  "mention": "Petite mention en bas (source, prudence)."
}
```

- `categorie` : `immo` (étiquette verte), `reno` (terracotta) ou `invest` (bleu nuit).
- `icone` : maison, cle, calculatrice, marteau, appareil-photo, epingle, signet, plan, graphique, euro, document, loupe.
- 3 à 5 points. Titre : 2 à 4 mots. Détail : 15 mots maximum. La durée s'adapte toute seule à la longueur du texte.

## Générer

```bash
node videos/immo-decode-serie/generer.mjs              # crée ou met à jour les projets
node videos/immo-decode-serie/generer.mjs --render     # + rendu MP4 de toutes les vidéos
node videos/immo-decode-serie/generer.mjs --render 07-mon-nouveau-conseil   # une seule
```

Le MP4 arrive dans `videos/immo-decode-serie/<slug>/renders/`. Pour retoucher une vidéo à la main : `cd` dans son dossier, puis `npm run dev`. Attention : relancer le générateur écrase les retouches faites dans `index.html`.
