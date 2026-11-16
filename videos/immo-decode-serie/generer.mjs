// Générateur de vidéos « conseil » Immo Décodé (version dynamique + effets sonores).
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
const SFX_DIR = path.join(HERE, "_sfx");
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

// Durées des effets sonores (s), bibliothèque _sfx/
const SFX_LEN = { "whoosh-short": 0.57, whoosh: 0.57, pop: 0.72, "click-soft": 0.37, click: 0.37, "impact-bass-1": 2.12, "impact-bass-2": 2.59, typing: 1.5, ping: 1.32, sparkle: 1.8, riser: 10.03, chime: 2.5, "key-press": 0.4 };

const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const words = (t) => t.split(/\s+/).filter(Boolean);
const split = (t) => words(t).map((w) => `<span class="w"><span class="wi">${esc(w)}</span></span>`).join(" ");
const icon = (name, cls, color) =>
  `<svg class="${cls}" viewBox="0 0 120 120" fill="none" stroke="${color}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round">${ICONS[name].replace(/<(path|circle|rect)/g, '<$1 pathLength="1"')}</svg>`;
const r2 = (x) => +x.toFixed(2);

const T = { hook: 3.4, takeaway: 4.4, end: 3.2 };
const WIPE = 0.3; // demi-durée du volet de transition

function build(c) {
  const cat = CATS[c.categorie];
  const n = c.points.length;
  const dur = c.points.map((p) => r2(Math.min(5.6, Math.max(3.8, 2.4 + 0.2 * (words(p.titre).length + words(p.detail).length)))));
  const starts = dur.map((_, i) => r2(T.hook + dur.slice(0, i).reduce((x, y) => x + y, 0)));
  const a = r2(T.hook + dur.reduce((x, y) => x + y, 0));
  const e = r2(a + T.takeaway);
  const total = r2(e + T.end);
  const sfx = [];
  const S = (name, t, vol, extra = "") => sfx.push({ name, t: r2(Math.max(0, t)), vol, extra });

  const logoSvg = fs
    .readFileSync(LOGO, "utf8")
    .replace(/<\?xml[^>]*>\s*/, "")
    .replace(/<title>.*?<\/title>/, "")
    .replace(/width="\d+" height="\d+"/, 'id="logo-fin"')
    .replace('<path id="toit"', '<path id="toit" pathLength="1" stroke-dasharray="1"');

  let html = "";
  let tl = "";

  // ── Accroche : déjà lisible à 0 s (miniature), puis « punch »
  html += `
      <div class="scene clip" id="hook" data-start="0" data-duration="${T.hook}" data-track-index="1"><div class="inner">
        ${icon(c.icone, "hook-icon", "#c8553d")}
        <div class="hook-title">${esc(c.accroche)}</div>
        <div class="hook-bar"></div>
        <div class="hook-sub">${esc(c.sous_titre)}</div>
      </div></div>`;
  tl += `
      tl.fromTo("#hook .hook-title", { scale: 1.08 }, { scale: 1, duration: 0.7, ease: "elastic.out(1, 0.45)" }, 0.1);
      tl.fromTo("#hook .hook-icon", { y: -40, rotation: -12 }, { y: 0, rotation: 0, duration: 0.8, ease: "bounce.out" }, 0.1);
      tl.fromTo("#hook .hook-bar", { scaleX: 0 }, { scaleX: 1, duration: 0.45, ease: "power3.out" }, 0.55);
      tl.fromTo("#hook .hook-sub", { autoAlpha: 0, x: -60 }, { autoAlpha: 1, x: 0, duration: 0.45, ease: "back.out(1.6)" }, 0.75);
      tl.fromTo("#hook .hook-icon", { rotation: 0 }, { rotation: 8, duration: 0.35, ease: "sine.inOut", yoyo: true, repeat: 3, immediateRender: false }, 1.6);
      tl.fromTo("#hook .inner", { scale: 1 }, { scale: 1.05, duration: ${T.hook}, ease: "none" }, 0);`;
  S("impact-bass-1", 0.08, 0.45);
  S("typing", 0.1, 0.16, 'data-duration="0.85" data-fade-out="0.2"');
  S("whoosh-short", 0.72, 0.35);

  // ── Points
  c.points.forEach((p, i) => {
    const s = starts[i];
    const D = dur[i];
    const id = `p${i + 1}`;
    const dots = c.points.map((_, j) => `<span class="dot${j <= i ? " on" : ""}"></span>`).join("");
    html += `
      <div class="scene clip" id="${id}" data-start="${s}" data-duration="${D}" data-track-index="1"><div class="inner">
        <div class="prow"><div class="pnum">${i + 1}<small>/${n}</small></div>${icon(p.icone, "picon", "#1f2a44")}</div>
        <div class="ptitle">${split(p.titre)}</div>
        <div class="pbar"></div>
        <div class="pdetail">${esc(p.detail)}</div>
        <div class="dots">${dots}</div>
      </div></div>`;
    tl += `
      tl.fromTo("#${id} .pnum", { scale: 0, rotation: -200 }, { scale: 1, rotation: 0, duration: 0.55, ease: "back.out(1.8)" }, ${r2(s + 0.02)});
      tl.fromTo("#${id} .picon *", { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.6, stagger: 0.1, ease: "power2.out" }, ${r2(s + 0.15)});
      tl.fromTo("#${id} .wi", { yPercent: 115, rotation: 8 }, { yPercent: 0, rotation: 0, duration: 0.5, stagger: 0.07, ease: "back.out(1.5)" }, ${r2(s + 0.2)});
      tl.fromTo("#${id} .pbar", { scaleX: 0 }, { scaleX: 1, duration: 0.35, ease: "power3.out" }, ${r2(s + 0.6)});
      tl.fromTo("#${id} .pdetail", { clipPath: "inset(0 100% 0 0)", x: -30 }, { clipPath: "inset(0 0% 0 0)", x: 0, duration: 0.6, ease: "power2.out" }, ${r2(s + 0.7)});
      tl.fromTo("#${id} .dot", { scale: 0 }, { scale: 1, duration: 0.3, stagger: 0.05, ease: "back.out(3)" }, ${r2(s + 0.3)});
      tl.fromTo("#${id} .picon", { y: 0, rotation: 0 }, { y: -16, rotation: -6, duration: ${r2((D - 1.0) / 2)}, ease: "sine.inOut", yoyo: true, repeat: 1 }, ${r2(s + 0.8)});
      tl.fromTo("#${id} .ptitle", { scale: 1 }, { scale: 1.06, duration: 0.22, ease: "power2.out", yoyo: true, repeat: 1 }, ${r2(s + D * 0.6)});
      tl.fromTo("#${id} .pnum", { scale: 1 }, { scale: 1.15, duration: 0.2, ease: "power2.out", yoyo: true, repeat: 1, immediateRender: false }, ${r2(s + D * 0.6 + 0.1)});
      tl.fromTo("#${id} .inner", { scale: 1, rotation: ${i % 2 ? -0.6 : 0.6} }, { scale: 1.05, rotation: 0, duration: ${D}, ease: "none" }, ${s});`;
    S("pop", s + 0.05, 0.5);
    S("click-soft", s + 0.25, 0.3);
    S("click-soft", s + 0.72, 0.35);
    S("pop", s + D * 0.6, 0.25);
  });

  // ── À retenir
  html += `
      <div class="scene clip" id="retenir" data-start="${a}" data-duration="${T.takeaway}" data-track-index="1"><div class="inner">
        <div class="k">À retenir</div>
        <div class="card"><div class="card-txt">${split(c.a_retenir)}</div></div>
      </div></div>`;
  tl += `
      tl.fromTo("#retenir .k", { scaleX: 2.2, autoAlpha: 0 }, { scaleX: 1, autoAlpha: 1, duration: 0.5, ease: "power3.out" }, ${r2(a + 0.02)});
      tl.fromTo("#retenir .card", { scale: 1.6, rotation: -12, autoAlpha: 0 }, { scale: 1, rotation: -1.5, autoAlpha: 1, duration: 0.5, ease: "back.out(1.6)" }, ${r2(a + 0.15)});
      tl.fromTo("#retenir .inner", { x: 0 }, { x: 14, duration: 0.05, ease: "none", yoyo: true, repeat: 5 }, ${r2(a + 0.6)});
      tl.fromTo("#retenir .wi", { yPercent: 115 }, { yPercent: 0, duration: 0.4, stagger: 0.05, ease: "back.out(1.5)" }, ${r2(a + 0.55)});
      tl.fromTo("#retenir .card", { rotation: -1.5 }, { rotation: 1, duration: 1.4, ease: "sine.inOut", yoyo: true, repeat: 1, immediateRender: false }, ${r2(a + 1.2)});
      tl.fromTo("#retenir .inner", { scale: 1 }, { scale: 1.05, duration: ${T.takeaway}, ease: "none" }, ${a});`;
  if (a - SFX_LEN.riser > 0.5) S("riser", a + 0.62 - SFX_LEN.riser, 0.16, 'data-fade-in="3"');
  S("impact-bass-2", a + 0.1, 0.4);
  S("ping", a + 1.0, 0.25);

  // ── Fin
  html += `
      <div class="scene clip" id="fin" data-start="${e}" data-duration="${T.end}" data-track-index="1"><div class="inner">
        ${logoSvg}
        <div class="fin-cta">${icon("signet", "fin-icon", "#fbf6ef")}Enregistre ce conseil</div>
        <div class="fin-handle">@immo.decode</div>
      </div></div>`;
  tl += `
      tl.to(["#brand", "#legal"], { opacity: 0, duration: 0.2 }, ${r2(e - 0.2)});
      tl.fromTo("#logo-fin #toit", { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.5, ease: "power2.out" }, ${r2(e + 0.05)});
      tl.fromTo("#logo-fin #immo", { autoAlpha: 0, y: 60 }, { autoAlpha: 1, y: 0, duration: 0.45, ease: "back.out(1.8)" }, ${r2(e + 0.25)});
      tl.fromTo("#logo-fin #decode", { autoAlpha: 0, y: 60 }, { autoAlpha: 1, y: 0, duration: 0.45, ease: "back.out(1.8)" }, ${r2(e + 0.38)});
      tl.fromTo("#logo-fin #barre", { scaleX: 0 }, { scaleX: 1, duration: 0.35, ease: "power3.out", transformOrigin: "50% 50%" }, ${r2(e + 0.6)});
      tl.fromTo(".fin-cta", { autoAlpha: 0, scale: 0.4 }, { autoAlpha: 1, scale: 1, duration: 0.5, ease: "back.out(2.2)" }, ${r2(e + 0.75)});
      tl.fromTo(".fin-handle", { autoAlpha: 0, y: 20 }, { autoAlpha: 1, y: 0, duration: 0.35, ease: "power3.out" }, ${r2(e + 0.95)});
      tl.fromTo(".fin-cta", { scale: 1 }, { scale: 1.08, duration: 0.25, ease: "sine.inOut", yoyo: true, repeat: 3, immediateRender: false }, ${r2(e + 1.6)});
      tl.fromTo("#fin .inner", { scale: 1 }, { scale: 1.04, duration: ${T.end}, ease: "none" }, ${e});`;
  S("sparkle", e + 0.1, 0.35);
  S("pop", e + 0.28, 0.35);
  S("pop", e + 0.41, 0.35);
  S("pop", e + 0.78, 0.5);
  S("click", e + 1.6, 0.3);

  // ── Volets de transition entre les scènes
  [...starts, a, e].forEach((b) => {
    tl += `
      tl.fromTo("#wipeA", { yPercent: 100 }, { yPercent: 0, duration: ${WIPE}, ease: "power3.in", immediateRender: false }, ${r2(b - WIPE)});
      tl.fromTo("#wipeA", { yPercent: 0 }, { yPercent: -100, duration: ${WIPE}, ease: "power3.out", immediateRender: false }, ${b});
      tl.fromTo("#wipeB", { yPercent: 100 }, { yPercent: 0, duration: ${r2(WIPE - 0.06)}, ease: "power3.in", immediateRender: false }, ${r2(b - WIPE + 0.06)});
      tl.fromTo("#wipeB", { yPercent: 0 }, { yPercent: -100, duration: ${WIPE}, ease: "power3.out", immediateRender: false }, ${r2(b + 0.04)});`;
    S("whoosh-short", b - WIPE - 0.05, 0.5);
  });

  // Une piste par son simultané : chaque effet va sur la première piste libre
  const lanes = [];
  const audio = sfx
    .sort((x, y) => x.t - y.t)
    .map((x, i) => {
      const m = x.extra.match(/data-duration="([\d.]+)"/);
      const len = r2(Math.min(m ? +m[1] : SFX_LEN[x.name], total - x.t));
      let lane = lanes.findIndex((end) => end <= x.t + 0.001);
      if (lane < 0) lane = lanes.push(0) - 1;
      lanes[lane] = x.t + len;
      const d = m ? "" : `data-duration="${len}"`;
      return `      <audio id="sfx-${i + 1}" src="assets/sfx/${x.name}.mp3" data-start="${x.t}" ${d} data-volume="${x.vol}" ${x.extra} data-track-index="${3 + lane}"></audio>`;
    })
    .join("\n");

  return { total, html: TEMPLATE(c, cat, total, html, tl, audio) };
}

const TEMPLATE = (c, cat, total, scenes, tl, audio) => `<!doctype html>
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
      #grid { position: absolute; inset: -120px; background-image: repeating-linear-gradient(0deg, rgba(200, 85, 61, 0.08) 0 2px, transparent 2px 60px), repeating-linear-gradient(90deg, rgba(200, 85, 61, 0.08) 0 2px, transparent 2px 60px); }
      .deco { position: absolute; width: 360px; height: 120px; }
      .deco path { fill: none; stroke: var(--terra); stroke-width: 10; stroke-linecap: round; stroke-linejoin: round; opacity: 0.12; }
      #d1 { left: -80px; top: 380px; } #d2 { right: -100px; top: 1180px; width: 480px; height: 160px; } #d3 { left: 120px; top: 1560px; width: 260px; height: 86px; }
      #prog { position: absolute; left: 0; top: 0; width: 1080px; height: 12px; background: var(--terra); transform-origin: 0% 50%; z-index: 30; }

      #brand { position: absolute; left: 0; right: 0; top: 150px; text-align: center; z-index: 10; }
      #brand-roof { width: 150px; height: 46px; display: block; margin: 0 auto 6px; }
      #brand-roof path { fill: none; stroke: var(--terra); stroke-width: 9; stroke-linecap: round; stroke-linejoin: round; stroke-dasharray: 1; stroke-dashoffset: 1; }
      #brand-name { font-family: "Fraunces", serif; font-weight: 700; font-size: 60px; letter-spacing: -1px; white-space: nowrap; }
      #tag { display: inline-block; margin-top: 18px; padding: 10px 26px; border-radius: 40px; background: var(--cat); color: var(--clair); font-weight: 700; font-size: 28px; letter-spacing: 4px; text-transform: uppercase; }
      .decode .dl { position: relative; display: inline-block; }
      .decode .glyph { position: absolute; left: 50%; top: 0; transform: translateX(-50%); font-family: "Inter", sans-serif; font-weight: 800; color: var(--terra); opacity: 0; }
      .decode .real { opacity: 0; }

      .scene { position: absolute; left: 0; right: 0; top: 0; bottom: 0; }
      .inner { position: absolute; left: 80px; right: 80px; top: 600px; text-align: center; transform-origin: 50% 30%; }
      .w { display: inline-block; overflow: hidden; vertical-align: top; padding: 0 2px 10px; margin-bottom: -10px; }
      .wi { display: inline-block; transform-origin: 0% 100%; }

      .hook-icon { width: 220px; height: 220px; display: block; margin: 0 auto 40px; }
      .hook-title { font-family: "Fraunces", serif; font-weight: 700; font-size: 104px; line-height: 1.05; letter-spacing: -1px; }
      .hook-bar { width: 220px; height: 14px; border-radius: 7px; background: var(--terra); margin: 34px auto 0; transform-origin: 0% 50%; }
      .hook-sub { margin-top: 30px; font-family: "Fraunces", serif; font-style: italic; font-weight: 600; font-size: 54px; line-height: 1.2; color: var(--terra); }

      .prow { display: flex; justify-content: center; align-items: center; gap: 46px; }
      .pnum { display: inline-flex; align-items: baseline; justify-content: center; width: 150px; height: 150px; padding-top: 22px; border-radius: 50%; background: var(--terra); color: var(--clair); font-family: "Fraunces", serif; font-weight: 700; font-size: 92px; line-height: 1; }
      .pnum small { font-family: "Inter", sans-serif; font-weight: 700; font-size: 32px; opacity: 0.85; }
      .picon { width: 150px; height: 150px; }
      .picon * { stroke-dasharray: 1; }
      .ptitle { margin-top: 50px; font-family: "Fraunces", serif; font-weight: 700; font-size: 92px; line-height: 1.05; letter-spacing: -1px; }
      .pbar { width: 160px; height: 12px; border-radius: 6px; background: var(--terra); margin: 34px auto 0; transform-origin: 0% 50%; }
      .pdetail { margin-top: 34px; font-weight: 500; font-size: 50px; line-height: 1.32; }
      .dots { display: flex; justify-content: center; gap: 16px; margin-top: 60px; }
      .dot { width: 22px; height: 22px; border-radius: 50%; background: rgba(31, 42, 68, 0.18); }
      .dot.on { background: var(--terra); }

      #retenir .k { display: inline-block; font-weight: 800; font-size: 34px; letter-spacing: 8px; text-transform: uppercase; color: var(--terra); }
      .card { margin-top: 30px; background: var(--nuit); color: var(--clair); border-radius: 36px; padding: 70px 60px; border-left: 20px solid var(--terra); text-align: left; box-shadow: 0 30px 60px rgba(31, 42, 68, 0.25); }
      .card-txt { font-family: "Fraunces", serif; font-weight: 700; font-size: 72px; line-height: 1.15; }

      #fin .inner { top: 470px; }
      #logo-fin { width: 620px; height: auto; display: block; margin: 0 auto; overflow: visible; }
      .fin-cta { display: inline-flex; align-items: center; gap: 20px; margin-top: 70px; padding: 26px 50px; border-radius: 70px; background: var(--terra); color: var(--clair); font-weight: 800; font-size: 48px; }
      .fin-icon { width: 54px; height: 54px; }
      .fin-handle { margin-top: 36px; font-weight: 800; font-size: 54px; }

      #legal { position: absolute; left: 80px; right: 80px; bottom: 300px; text-align: center; font-size: 28px; font-weight: 500; opacity: 0.75; z-index: 10; }
      .wipe { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; z-index: 40; }
      #wipeA { background: var(--terra); }
      #wipeB { background: var(--nuit); }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="${total}" data-fps="30" data-width="1080" data-height="1920">
      <div id="grid"></div>
      <svg class="deco" id="d1" viewBox="0 0 360 120"><path d="M20 110 L180 14 L340 110" /></svg>
      <svg class="deco" id="d2" viewBox="0 0 360 120"><path d="M20 110 L180 14 L340 110" /></svg>
      <svg class="deco" id="d3" viewBox="0 0 360 120"><path d="M20 110 L180 14 L340 110" /></svg>
      <div id="brand">
        <svg id="brand-roof" viewBox="0 0 150 46"><path pathLength="1" d="M8 40 L75 6 L142 40" /></svg>
        <div id="brand-name" class="decode" data-text="IMMO DÉCODÉ"></div>
        <div id="tag">${esc(cat.label)}</div>
      </div>
${scenes}
      <div id="legal">${esc(c.mention || "")}</div>
      <div id="prog"></div>
      <div class="wipe" id="wipeA"></div>
      <div class="wipe" id="wipeB"></div>
${audio}
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
      gsap.set(".wipe", { yPercent: 100 });
      const tl = gsap.timeline({ paused: true });
      // Mouvement de fond continu
      tl.fromTo("#grid", { x: 0, y: 0 }, { x: 60, y: -120, duration: ${total}, ease: "none" }, 0);
      tl.fromTo("#d1", { x: 0, rotation: -8 }, { x: 140, rotation: 6, duration: ${total}, ease: "none" }, 0);
      tl.fromTo("#d2", { x: 0, rotation: 10 }, { x: -160, rotation: -4, duration: ${total}, ease: "none" }, 0);
      tl.fromTo("#d3", { y: 0, rotation: 0 }, { y: -120, rotation: 12, duration: ${total}, ease: "none" }, 0);
      tl.fromTo("#prog", { scaleX: 0 }, { scaleX: 1, duration: ${total}, ease: "none" }, 0);
      // Signature
      tl.fromTo("#brand-roof path", { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.5, ease: "power2.out" }, 0);
      tl.fromTo(P, { d: 0 }, { d: 1, duration: 0.7, ease: "none", onUpdate: () => dec(P.d) }, 0.1);
      tl.fromTo("#tag", { autoAlpha: 0, scale: 0.4 }, { autoAlpha: 1, scale: 1, duration: 0.4, ease: "back.out(2.4)" }, 0.6);
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
const only = args.find((x) => !x.startsWith("--"));
const conseils = JSON.parse(fs.readFileSync(path.join(HERE, "conseils.json"), "utf8"));

for (const c of conseils) {
  if (only && c.slug !== only) continue;
  if (!CATS[c.categorie]) throw new Error(`${c.slug} : catégorie inconnue « ${c.categorie} » (immo, reno, invest)`);
  for (const ic of [c.icone, ...c.points.map((p) => p.icone)]) if (!ICONS[ic]) throw new Error(`${c.slug} : picto inconnu « ${ic} »`);
  const dir = path.join(HERE, c.slug);
  copyDir(ASSETS, path.join(dir, "assets"));
  copyDir(SFX_DIR, path.join(dir, "assets/sfx"));
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
