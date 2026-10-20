# Éditer tes vidéos toi-même (Hyperframes Studio)

Studio est l'éditeur de Hyperframes : une timeline dans ton navigateur où tu lis la vidéo,
cliques sur un élément, le déplaces, le recoupes ou changes son timing. Il tourne **sur ton ordinateur**.

## 1. À installer une seule fois

- **Node.js 22 ou plus récent** : https://nodejs.org (prends la version « LTS »)
- **FFmpeg** (pour le rendu MP4) :
  - Mac : `brew install ffmpeg`
  - Windows : `winget install ffmpeg`
- **Git** : https://git-scm.com
- **Claude Code desktop** (pour travailler avec Claude pendant que tu édites) : https://claude.ai/download

## 2. Récupérer le projet

Dans un terminal :

```bash
git clone https://github.com/noahtouati007-png/MOTION-.git
cd MOTION-
```

## 3. Ouvrir l'éditeur

```bash
cd mon-premier-montage
npm run dev
```

Studio s'ouvre dans ton navigateur à l'adresse :
`http://localhost:3002/#project/mon-premier-montage`

Chaque modification (de toi ou de Claude) se recharge automatiquement dans Studio.

## 4. Éditer avec Claude

Ouvre le dossier `MOTION-` dans **Claude Code desktop**, sur ton ordinateur, pendant que Studio est ouvert. Ensuite :

- **Tu édites à la main** dans Studio (déplacer, couper, retimer).
- **Tu demandes à Claude** ce qui est plus long à faire à la main. Clique sur un élément dans Studio puis
  écris par exemple « rends ça plus gros » ou « fais arriver ce texte plus tard » : Claude voit
  ce que tu as sélectionné.
- **Rendu final** : `npm run render` (crée le MP4).

> Option : l'application HyperFrames desktop (https://hyperframes.dev/studio/download) fait la même chose
> avec un chat intégré. Depuis le dossier du projet : `npx hyperframes open`.

## 5. Garder tout synchronisé

Le projet vit sur GitHub : ce que Claude fait dans le cloud et ce que tu fais sur ton PC se retrouvent au même endroit.

- Avant de commencer : `git pull`
- Après tes modifications : `git add -A && git commit -m "mes retouches" && git push`

## Nouveau projet vidéo

Depuis le dossier `MOTION-` :

```bash
npx hyperframes init nom-du-projet
cd nom-du-projet
npm run dev
```
