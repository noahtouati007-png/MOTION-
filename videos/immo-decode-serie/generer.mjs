// Générateur de vidéos « conseil » Immo Décodé.
//
//   node videos/immo-decode-serie/generer.mjs            → crée/met à jour un projet par conseil
//   node videos/immo-decode-serie/generer.mjs --render   → idem + rendu MP4 de chaque vidéo
//   node videos/immo-decode-serie/generer.mjs --render 03-negocier-le-prix   → une seule vidéo
//
// Pour ajouter une vidéo : ajouter une entrée dans conseils.json (3 à 5 points), relancer.

import fs from "node:fs";
import path from "node:path";
import { execSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(HERE, "../..");
const ASSETS = path.join(REPO, "videos/immo-decode-v1-bienvenue/assets");
const LOGO = path.join(REPO, "charte-graphique/logo/logo-principal-couleur.svg");
const HF = "hyperframes@0.9.2";

const CATS = {
  immo: { label: "Conseil immo", color: "#6b7f4e" },
  reno: { label: "Conseil réno", color: "#c8553d" },
  invest: { label: "Conseil invest", color: "#1f2a44" },
};

// Même jeu de pictos que charte-graphique/illustrations (grille 120, trait 7)
const ICONS = {
  maison: '<path d="M18 58 L60 22 L102 58"/><path d="M30 48 V100 H90 V48"/><path d="M50 100 V72 H70 V100"/>',
  cle: '<circle cx="38" cy="60" r="20"/><path d="M58 60 H104 M90 60 V76 M104 60 V72"/>',
  calculatrice: '<rect x="28" y="14" width="64" height="92" rx="12"/><rect x="40" y="26" width="40" height="18" rx="4"/><path d="M42 62h8M70 62h8M42 78h8M70 78h8M42 94h8M70 94h8M56 62h8M56 94h8"/>',
  marteau: '<path d="M24 26 h56 a8 8 0 0 1 8 8 v10 a8 8 0 0 1 -8 8 h-56 z"/><path d="M88 34 h14"/><path d="M50 52 v54"/>',
  "appareil-photo": '<path d="M18 40 h84 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-84 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/><path d="M40 40 l8 -14 h24 l8 14"/><circle cx="60" cy="71" r="18"/>',
  epingle: '<path d="M60 108 C60 108 28 74 28 50 a32 32 0 0 1 64 0 c0 24 -32 58 -32 58 z"/><circle cx="60" cy="50" r="11"/>',
  signet: '<path d="M34 14 h52 a6 6 0 0 1 6 6 v88 l-32 -22 l-32 22 v-88 a6 6 0 0 1 6 -6 z"/>',
  plan: '<rect x="14" y="18" width="92" height="84" rx="4"/><path d="M14 62 H52 M70 62 H106 M60 18 V44"/>',
  graphique: '<path d="M16 104 H106"/><path d="M30 90 V70 M54 90 V54 M78 90 V40 M102 90 V24"/><path d="M24 50 L48 36 L70 42 L100 16"/>',
  euro: '<path d="M88 30 a34 34 0 1 0 0 60"/><path d="M20 52 H70 M20 68 H66"/>',
  document: '<path d="M30 12 h42 l20 20 v76 h-62 z"/><path d="M72 12 v20 h20"/><path d="M44 58 h32 M44 74 h32 M44 90 h20"/>',
  loupe: '<circle cx="52" cy="52" r="30"/><path d="M74 74 L104 104"/>',
};

const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
// Ajoute pathLength=1 à chaque tracé pour l'animation « dessin »
const icon = (name, cls, color) =>
  `<svg class="${cls}" viewBox="0 0 120 120" fill="none" stroke="${color}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round">${ICONS[name].replace(/<(path|circle|rect)/g, '<$1 pathLength="1"')}</svg>`;

const T = { hook: 3.6, takeaway: 4.2, end: 3.0 };

function build(c) {
  const cat = CATS[c.categorie];
  const n = c.points.length;
  // Durée d'un point : assez longue pour lire le titre + le détail (≈ 0,2 s par mot)
  const words = (t) => t.split(/\s+/).filter(Boolean).length;
  const dur = c.points.map((p) => +Math.min(5.6, Math.max(3.8, 2.4 + 0.2 * (words(p.titre) + words(p.detail)))).toFixed(1));
  const starts = dur.map((_, i) => +(T.hook + dur.slice(0, i).reduce((x, y) => x + y, 0)).toFixed(2));
  const pointsEnd = +(T.hook + dur.reduce((x, y) => x + y, 0)).toFixed(2);
  const total = +(pointsEnd + T.takeaway + T.end).toFixed(2);
  const logoSvg = fs.readFileSync(LOGO, "utf8").replace(/<\?xml[^>]*>\s*/, "").replace(/<title>.*?<\/title>/, "").replace(/width="\d+" height="\d+"/, 'id="logo-fin"');

  let html = "";
  let tl = "";
  // ── Accroche (déjà à l'écran à 0 s = miniature)
  html += `
      <div class="scene clip" id="hook" data-start="0" data-duration="${T.hook}" data-track-index="1">
        ${icon(c.icone, "hook-icon", "#c8553d")}
        <div class="hook-title">${esc(c.accroche)}</div>
        <div class="hook-sub">${esc(c.sous_titre)}</div>
      </div>`;
  tl += `
      tl.fromTo("#hook .hook-icon", { rotation: 0, y: 0 }, { rotation: -6, y: -10, duration: 0.6, ease: "sine.inOut", yoyo: true, repeat: 3 }, 0.3);
      tl.fromTo("#hook .hook-sub", { autoAlpha: 0, y: 24 }, { autoAlpha: 1, y: 0, duration: 0.45, ease: "power3.out" }, 0.7);
      tl.to("#hook > *", { opacity: 0, y: -50, duration: 0.3, stagger: 0.04, ease: "power2.in" }, ${T.hook - 0.35});`;

  // ── Points
  c.points.forEach((p, i) => {
    const s = starts[i];
    const D = dur[i];
    const id = `p${i + 1}`;
    const dots = c.points.map((_, j) => `<span class="dot${j <= i ? " on" : ""}"></span>`).join("");
    html += `
      <div class="scene clip" id="${id}" data-start="${s}" data-duration="${D}" data-track-index="1">
        <div class="pnum">${i + 1}<small>/${n}</small></div>
        ${icon(p.icone, "picon", "#1f2a44")}
        <div class="ptitle">${esc(p.titre)}</div>
        <div class="pbar"></div>
        <div class="pdetail">${esc(p.detail)}</div>
        <div class="dots">${dots}</div>
      </div>`;
    tl += `
      tl.fromTo("#${id} .pnum", { autoAlpha: 0, scale: 0.5 }, { autoAlpha: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, ${s + 0.05});
      tl.fromTo("#${id} .picon *", { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.7, stagger: 0.12, ease: "power2.out" }, ${s + 0.1});
      tl.fromTo("#${id} .ptitle", { autoAlpha: 0, y: 36 }, { autoAlpha: 1, y: 0, duration: 0.45, ease: "power3.out" }, ${s + 0.2});
      tl.fromTo("#${id} .pbar", { scaleX: 0 }, { scaleX: 1, duration: 0.4, ease: "power3.out" }, ${s + 0.5});
      tl.fromTo("#${id} .pdetail", { autoAlpha: 0, y: 24 }, { autoAlpha: 1, y: 0, duration: 0.45, ease: "power3.out" }, ${s + 0.55});
      tl.fromTo("#${id} .dots", { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.3 }, ${s + 0.2});
      tl.fromTo("#${id} .picon", { y: 0, rotation: 0 }, { y: -14, rotation: -5, duration: ${+((D - 1.2) / 2).toFixed(2)}, ease: "sine.inOut", yoyo: true, repeat: 1 }, ${+(s + 0.85).toFixed(2)});
      tl.fromTo("#${id} .dot.on:last-child, #${id} .dot.on", { scale: 1 }, { scale: 1.25, duration: 0.25, ease: "sine.inOut", yoyo: true, repeat: 1 }, ${+(s + D / 2 + 0.3).toFixed(2)});
      tl.to("#${id} > *", { opacity: 0, y: -40, duration: 0.3, stagger: 0.03, ease: "power2.in" }, ${+(s + D - 0.35).toFixed(2)});`;
  });

  // ── À retenir
  const a = pointsEnd;
  html += `
      <div class="scene clip" id="retenir" data-start="${a}" data-duration="${T.takeaway}" data-track-index="1">
        <div class="k">À retenir</div>
        <div class="card"><div class="card-txt">${esc(c.a_retenir)}</div></div>
      </div>`;
  tl += `
      tl.fromTo("#retenir .k", { autoAlpha: 0, y: 20 }, { autoAlpha: 1, y: 0, duration: 0.35, ease: "power3.out" }, ${a + 0.05});
      tl.fromTo("#retenir .card", { autoAlpha: 0, scale: 0.9 }, { autoAlpha: 1, scale: 1, duration: 0.5, ease: "back.out(1.6)" }, ${a + 0.2});
      tl.fromTo("#retenir .card", { rotation: 0 }, { rotation: -1.2, duration: 1.4, ease: "sine.inOut", yoyo: true, repeat: 1 }, ${a + 0.8});
      tl.to("#retenir > *", { opacity: 0, y: -40, duration: 0.3, stagger: 0.05, ease: "power2.in" }, ${+(a + T.takeaway - 0.35).toFixed(2)});`;

  // ── Fin
  const e = +(a + T.takeaway).toFixed(2);
  html += `
      <div class="scene clip" id="fin" data-start="${e}" data-duration="${T.end}" data-track-index="1">
        ${logoSvg}
        <div class="fin-cta">${icon("signet", "fin-icon", "#fbf6ef")}Enregistre ce conseil</div>
        <div class="fin-handle">@immo.decode</div>
      </div>`;
  tl += `
      tl.to(["#brand", "#legal"], { opacity: 0, duration: 0.3 }, ${e - 0.3});
      tl.fromTo("#logo-fin", { autoAlpha: 0, scale: 0.85 }, { autoAlpha: 1, scale: 1, duration: 0.5, ease: "back.out(1.6)" }, ${e});
      tl.fromTo(".fin-cta", { autoAlpha: 0, y: 30 }, { autoAlpha: 1, y: 0, duration: 0.4, ease: "power3.out" }, ${e + 0.15});
      tl.fromTo(".fin-handle", { autoAlpha: 0, y: 20 }, { autoAlpha: 1, y: 0, duration: 0.35, ease: "power3.out" }, ${e + 0.25});
      tl.to(".fin-cta", { scale: 1.05, duration: 0.3, ease: "sine.inOut", yoyo: true, repeat: 1 }, ${e + 1.2});`;

  return { total, html: TEMPLATE(c, cat, total, html, tl) };
}

const TEMPLATE = (c, cat, total, scenes, tl) => `<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <!-- Généré par videos/immo-decode-serie/generer.mjs à partir de conseils.json : modifier la source puis relancer. -->
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      @font-face { font-family: "Fraunces"; src: url("assets/fonts/fraunces-latin-700-normal.woff2") format("woff2"); font-weight: 700; }
      @font-face { font-family: "Fraunces"; src: url("assets/fonts/fraunces-latin-600-normal.woff2") format("woff2"); font-weight: 600; }
      @font-face { font-family: "Fraunces"; src: url("assets/fonts/fraunces-latin-600-italic.woff2") format("woff2"); font-weight: 600; font-style: italic; }
      @font-face { font-family: "Inter"; src: url("assets/fonts/inter-latin-500-normal.woff2") format("woff2"); font-weight: 500; }
      @font-face { font-family: "Inter"; src: url("assets/fonts/inter-latin-700-normal.woff2") format("woff2"); font-weight: 700; }
      @font-face { font-family: "Inter"; src: url("assets/fonts/inter-latin-800-normal.woff2") format("woff2"); font-weight: 800; }
      :root { --sable: #f2e8dc; --clair: #fbf6ef; --terra: #c8553d; --nuit: #1f2a44; --olive: #6b7f4e; --cat: ${cat.color}; }
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1080px; height: 1920px; overflow: hidden; background: var(--sable); }
      #root { position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: "Inter", sans-serif; color: var(--nuit); background: var(--sable); }
      #grid { position: absolute; inset: 0; background-image: repeating-linear-gradient(0deg, rgba(200, 85, 61, 0.07) 0 2px, transparent 2px 60px), repeating-linear-gradient(90deg, rgba(200, 85, 61, 0.07) 0 2px, transparent 2px 60px); }

      #brand { position: absolute; left: 0; right: 0; top: 150px; text-align: center; }
      #brand-roof { width: 150px; height: 46px; display: block; margin: 0 auto 6px; }
      #brand-roof path { fill: none; stroke: var(--terra); stroke-width: 9; stroke-linecap: round; stroke-linejoin: round; stroke-dasharray: 1; stroke-dashoffset: 1; }
      #brand-name { font-family: "Fraunces", serif; font-weight: 700; font-size: 60px; letter-spacing: -1px; white-space: nowrap; }
      #tag { display: inline-block; margin-top: 18px; padding: 10px 26px; border-radius: 40px; background: var(--cat); color: var(--clair); font-weight: 700; font-size: 28px; letter-spacing: 4px; text-transform: uppercase; }
      .decode .dl { position: relative; display: inline-block; }
      .decode .glyph { position: absolute; left: 50%; top: 0; transform: translateX(-50%); font-family: "Inter", sans-serif; font-weight: 800; color: var(--terra); opacity: 0; }
      .decode .real { opacity: 0; }

      .scene { position: absolute; left: 80px; right: 80px; top: 600px; text-align: center; }
      .picon * { stroke-dasharray: 1; }

      .hook-icon { width: 220px; height: 220px; display: block; margin: 0 auto 40px; }
      .hook-title { font-family: "Fraunces", serif; font-weight: 700; font-size: 104px; line-height: 1.05; letter-spacing: -1px; }
      .hook-sub { margin-top: 34px; font-family: "Fraunces", serif; font-style: italic; font-weight: 600; font-size: 54px; line-height: 1.2; color: var(--terra); }

      .pnum { vertical-align: middle; display: inline-flex; align-items: baseline; justify-content: center; width: 150px; height: 150px; padding-top: 22px; border-radius: 50%; background: var(--terra); color: var(--clair); font-family: "Fraunces", serif; font-weight: 700; font-size: 92px; line-height: 1; }
      .pnum small { font-family: "Inter", sans-serif; font-weight: 700; font-size: 32px; opacity: 0.85; }
      .picon { display: inline-block; vertical-align: middle; margin-left: 46px; width: 150px; height: 150px; }
      .ptitle { margin-top: 50px; font-family: "Fraunces", serif; font-weight: 700; font-size: 92px; line-height: 1.05; letter-spacing: -1px; }
      .pbar { width: 160px; height: 12px; border-radius: 6px; background: var(--terra); margin: 34px auto 0; transform-origin: 0% 50%; }
      .pdetail { margin-top: 34px; font-weight: 500; font-size: 50px; line-height: 1.32; }
      .dots { display: flex; justify-content: center; gap: 16px; margin-top: 60px; }
      .dot { width: 22px; height: 22px; border-radius: 50%; background: rgba(31, 42, 68, 0.18); }
      .dot.on { background: var(--terra); }

      #retenir .k { font-weight: 800; font-size: 34px; letter-spacing: 8px; text-transform: uppercase; color: var(--terra); }
      .card { margin-top: 30px; background: var(--nuit); color: var(--clair); border-radius: 36px; padding: 70px 60px; border-left: 20px solid var(--terra); text-align: left; }
      .card-txt { font-family: "Fraunces", serif; font-weight: 700; font-size: 72px; line-height: 1.15; }

      #fin { top: 470px; }
      #logo-fin { width: 620px; height: auto; display: block; margin: 0 auto; }
      .fin-cta { display: inline-flex; align-items: center; gap: 20px; margin-top: 70px; padding: 26px 50px; border-radius: 70px; background: var(--terra); color: var(--clair); font-weight: 800; font-size: 48px; }
      .fin-icon { width: 54px; height: 54px; }
      .fin-handle { margin-top: 36px; font-weight: 800; font-size: 54px; }

      #legal { position: absolute; left: 80px; right: 80px; bottom: 300px; text-align: center; font-size: 28px; font-weight: 500; opacity: 0.75; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="${total}" data-fps="30" data-width="1080" data-height="1920">
      <div id="grid"></div>
      <div id="brand">
        <svg id="brand-roof" viewBox="0 0 150 46"><path pathLength="1" d="M8 40 L75 6 L142 40" /></svg>
        <div id="brand-name" class="decode" data-text="IMMO DÉCODÉ"></div>
        <div id="tag">${esc(cat.label)}</div>
      </div>
${scenes}
      <div id="legal">${esc(c.mention || "")}</div>
    </div>
    <script>
      const GLYPHS = "ABCDEFGHJKLMNPQRSTUVWXYZ0123456789#%€?";
      function makeDecoder(el, seed) {
        const text = el.dataset.text;
        el.textContent = "";
        const letters = Array.from(text).map((ch, i) => {
          const s = document.createElement("span"); s.className = "dl";
          const r = document.createElement("span"); r.className = "real"; r.textContent = ch === " " ? "\\u00A0" : ch;
          const g = document.createElement("span"); g.className = "glyph";
          s.appendChild(r); s.appendChild(g); el.appendChild(s);
          return { r, g, i, space: ch === " " };
        });
        const n = letters.length;
        return function (p) {
          letters.forEach((L) => {
            const a = (L.i / n) * 0.3, d = 0.4 + (L.i / n) * 0.55;
            if (p <= a) { L.r.style.opacity = 0; L.g.style.opacity = 0; }
            else if (p < d && !L.space) {
              const h = (((L.i + 1) * 2654435761) ^ ((Math.floor(p * 40) + 7) * 40503) ^ ${c.slug.length * 977}) >>> 0;
              L.g.textContent = GLYPHS[h % GLYPHS.length]; L.g.style.opacity = 1; L.r.style.opacity = 0;
            } else { L.g.style.opacity = 0; L.r.style.opacity = 1; }
          });
        };
      }
      const dec = makeDecoder(document.getElementById("brand-name"), 1);
      dec(0);
      const P = { d: 0 };
      const tl = gsap.timeline({ paused: true });
      tl.fromTo("#brand-roof path", { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.5, ease: "power2.out" }, 0);
      tl.fromTo(P, { d: 0 }, { d: 1, duration: 0.7, ease: "none", onUpdate: () => dec(P.d) }, 0.1);
      tl.fromTo("#tag", { autoAlpha: 0, y: 14 }, { autoAlpha: 1, y: 0, duration: 0.35, ease: "power3.out" }, 0.6);
      tl.fromTo("#legal", { opacity: 0 }, { opacity: 0.75, duration: 0.5 }, ${T.hook});
${tl}
      window.__timelines = window.__timelines || {};
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
`;

function copyDir(src, dst) {
  fs.mkdirSync(dst, { recursive: true });
  for (const f of fs.readdirSync(src, { withFileTypes: true })) {
    const s = path.join(src, f.name), d = path.join(dst, f.name);
    f.isDirectory() ? copyDir(s, d) : fs.copyFileSync(s, d);
  }
}

const args = process.argv.slice(2);
const render = args.includes("--render");
const only = args.find((a) => !a.startsWith("--"));
const conseils = JSON.parse(fs.readFileSync(path.join(HERE, "conseils.json"), "utf8"));

for (const c of conseils) {
  if (only && c.slug !== only) continue;
  if (!CATS[c.categorie]) throw new Error(`${c.slug} : catégorie inconnue « ${c.categorie} » (immo, reno, invest)`);
  for (const ic of [c.icone, ...c.points.map((p) => p.icone)]) if (!ICONS[ic]) throw new Error(`${c.slug} : picto inconnu « ${ic} »`);
  const dir = path.join(HERE, c.slug);
  copyDir(ASSETS, path.join(dir, "assets"));
  const { total, html } = build(c);
  fs.writeFileSync(path.join(dir, "index.html"), html);
  const name = `immo-decode-${c.slug}`;
  fs.writeFileSync(path.join(dir, "package.json"), JSON.stringify({ name, private: true, type: "module", scripts: { dev: `npx --yes ${HF} preview`, check: `npx --yes ${HF} check`, render: `npx --yes ${HF} render`, publish: `npx --yes ${HF} publish` } }, null, 2) + "\n");
  fs.writeFileSync(path.join(dir, "meta.json"), JSON.stringify({ id: name, name }, null, 2) + "\n");
  fs.copyFileSync(path.join(REPO, "videos/immo-decode-v1-bienvenue/hyperframes.json"), path.join(dir, "hyperframes.json"));
  console.log(`✓ ${c.slug} (${total} s)`);
  if (render) {
    execSync(`npx --yes ${HF} render . -q high -o ./renders/${name}.mp4`, { cwd: dir, stdio: "inherit" });
  }
}
