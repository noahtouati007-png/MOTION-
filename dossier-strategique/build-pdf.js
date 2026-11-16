// Génère dossier-strategique-immo-decode.pdf : vraie mise en page A4 (une page = un format fixe),
// à partir du contenu de index.html. Polices locales.
// Usage : NODE_PATH=$(npm root -g) node dossier-strategique/build-pdf.js [prefixe-apercu]
const { chromium } = require("playwright");
const fs = require("fs"), path = require("path");
const here = __dirname, w2 = path.resolve(here, "../charte-graphique/_source/woff2");
const ff = (fam, file, w, it) => `@font-face{font-family:"${fam}";src:url("file://${w2}/${file}.woff2");font-weight:${w};font-style:${it ? "italic" : "normal"}}`;
const fonts = [ff("Fraunces", "fraunces-latin-600-normal", 600), ff("Fraunces", "fraunces-latin-700-normal", 700), ff("Fraunces", "fraunces-latin-600-italic", 600, 1), ff("Inter", "inter-latin-400-normal", 400), ff("Inter", "inter-latin-500-normal", 500), ff("Inter", "inter-latin-700-normal", 700), ff("Inter", "inter-latin-800-normal", 800)].join("");

const src = fs.readFileSync(path.join(here, "index.html"), "utf8");
const style = src.match(/<style>([\s\S]*?)<\/style>/)[1];
const sprite = src.match(/<svg width="0"[\s\S]*?<\/svg>\n/)[0];
const section = (id) => {
  const m = src.match(new RegExp(`<section class="part wrap" id="${id}">([\\s\\S]*?)</section>`));
  if (!m) throw new Error("section introuvable : " + id);
  return `<section class="part" id="${id}">${m[1]}</section>`;
};

// Pages : chaque page regroupe une ou plusieurs parties, dans l'ordre de la consigne
// Les 13 parties de la consigne : numéro, titre, id de la section
const PARTS = [
  ["01", "Objectifs", "objectifs"], ["02", "Cible et personas", "cible"], ["03", "Positionnement", "positionnement"],
  ["04", "Choix des plateformes", "plateformes"], ["05", "Thème et concept", "concept"], ["06", "Stratégie éditoriale", "editorial"],
  ["07", "Piliers de contenu", "piliers"], ["08", "Accessibilité", "accessibilite"], ["09", "Charte de ton", "ton"],
  ["10", "Calendrier éditorial", "calendrier"], ["11", "Organisation de la production", "production"],
  ["12", "KPI et mesure de la performance", "kpi"], ["13", "Risques et bad buzz", "risques"],
];
// Pages : chaque page regroupe une ou plusieurs parties, dans l'ordre de la consigne (page 1 = couverture)
const LAYOUT = [["compte"], ["objectifs", "cible"], ["positionnement", "plateformes"], ["concept"], ["editorial"], ["piliers", "accessibilite"], ["ton"], ["calendrier"], ["production"], ["kpi"], ["risques"]];
const pageOf = {};
LAYOUT.forEach((ids, i) => ids.forEach((id) => (pageOf[id] = i + 2)));
const tocHtml = `<nav class="toc"><p class="label">Sommaire</p><ol class="toc-p">${PARTS.map(([n, t, id]) => `<li><a href="#${id}"><span class="tn">${n}</span><span class="tt">${t}</span><span class="lead-dots"></span><span class="tp">p. ${pageOf[id]}</span></a></li>`).join("")}</ol></nav>`;
const PAGES = LAYOUT.map((ids) => ({
  label: ids[0] === "compte" ? "Sommaire · Le compte" : ids.map((id) => { const [n, t] = PARTS.find((x) => x[2] === id); return `${n} ${t}`; }).join(" · "),
  body: (ids[0] === "compte" ? tocHtml : "") + ids.map(section).join(""),
}));
const total = PAGES.length + 2;
const roof = `<svg viewBox="0 0 84 34" class="mini-roof"><path d="M6 30 L42 6 L78 30"/></svg>`;

const printCss = `
  @page { size: A4; margin: 0; }
  html, body { margin: 0; padding: 0; background: #fff; }
  body { font-size: 12.5px; line-height: 1.5; background-image: none; }
  .sheet { width: 210mm; height: 297mm; position: relative; overflow: hidden; break-after: page; background: var(--sable);
    background-image: repeating-linear-gradient(0deg, var(--grille) 0 1px, transparent 1px 24px), repeating-linear-gradient(90deg, var(--grille) 0 1px, transparent 1px 24px); }
  .sheet:last-child { break-after: auto; }
  .inner { position: absolute; left: 15mm; right: 15mm; top: 21mm; bottom: 17mm; overflow: hidden; }
  .fit { display: flex; flex-direction: column; gap: 9mm; transform-origin: 0 0; }
  .run { position: absolute; left: 15mm; right: 15mm; top: 8mm; display: flex; justify-content: space-between; align-items: center; font: 800 8px/1 var(--sans); letter-spacing: .18em; text-transform: uppercase; color: var(--encre-douce); border-bottom: 1px solid var(--trait); padding-bottom: 3mm; }
  .run b { display: flex; align-items: center; gap: 6px; color: var(--nuit); }
  .mini-roof { width: 18px; height: 8px; fill: none; stroke: var(--terra); stroke-width: 9; stroke-linecap: round; stroke-linejoin: round; }
  .folio { position: absolute; left: 15mm; right: 15mm; bottom: 7mm; display: flex; justify-content: space-between; font: 700 8px/1 var(--sans); letter-spacing: .14em; text-transform: uppercase; color: var(--encre-douce); }
  .folio .n { font: 700 11px/1 var(--serif); color: var(--terra); letter-spacing: 0; }

  section.part { padding: 0; border: 0; break-before: auto; }
  .part-head { margin-bottom: 4mm; gap: 2px 12px; }
  .roofnum { width: 48px; height: 42px; }
  .roofnum svg { width: 48px; height: 20px; stroke-width: 9; }
  .roofnum b { font-size: 22px; }
  h2 { font-size: 21px; line-height: 1.12; }
  h3 { font-size: 14px; }
  .label { font-size: 7.5px; }
  .lead { font-size: 12.5px; line-height: 1.5; }
  .part-intro { margin-bottom: 4mm; }
  .muted { font-size: 10.5px; }
  .grid { gap: 3mm; }
  .g2 { grid-template-columns: 1fr 1fr; }
  .g3 { grid-template-columns: repeat(3, 1fr); }
  .g4 { grid-template-columns: repeat(4, 1fr); }
  .card { padding: 4mm; border-radius: 10px; }
  .kpi { padding: 3.5mm; border-radius: 10px; }
  .kpi b { font-size: 24px; }
  .kpi span { font-size: 9.5px; }
  .chip { font-size: 8.5px; padding: 4px 8px; }
  .steps-line { margin-top: 3mm; gap: 6px; }
  .tbl { border-radius: 10px; overflow: hidden; }
  table { font-size: 9.5px; min-width: 0; }
  th { font-size: 7px; padding: 2.2mm 2.5mm; }
  td { padding: 2.2mm 2.5mm; }
  .profile { gap: 4mm; }
  .profile img { width: 70px; height: 70px; }
  .profile .handle { font-size: 16px; }
  .profile .bio { font-size: 10.5px; }
  .persona { gap: 2mm; }
  .persona .av { width: 34px; height: 34px; }
  .persona .av svg { width: 18px; height: 18px; }
  .persona dl { font-size: 10px; gap: 1.5mm; }
  .persona dt { font-size: 7px; }
  .map { aspect-ratio: 1.25; border-radius: 10px; }
  .quote { font-size: 15px; padding-left: 4mm; border-left-width: 4px; }
  .flow { gap: 3mm; grid-template-columns: repeat(3, 1fr); }
  .flow .card { padding-top: 12mm; }
  .flow .card::before { top: 4mm; left: 4mm; width: 22px; height: 22px; font-size: 12px; line-height: 22px; }
  .timeline { padding: 4mm; border-radius: 10px; overflow: visible; }
  .timeline svg { min-width: 0; }
  .stack { height: 30px; border-radius: 8px; margin-bottom: 4mm; }
  .stack div { font-size: 10px; }
  .checks { gap: 2.5mm; grid-template-columns: 1fr 1fr; }
  .checks li { padding: 3mm 3.5mm; border-radius: 9px; gap: 3mm; font-size: 10.5px; }
  .tick { width: 18px; height: 18px; }
  .tick svg { width: 10px; height: 10px; }
  .dodont { gap: 3mm; grid-template-columns: 1fr 1fr; }
  .dodont li { font-size: 10.5px; padding-left: 16px; }
  .dodont ul { gap: 1.5mm; margin-top: 2mm; }
  .swatches { gap: 2.5mm; grid-template-columns: repeat(3, 1fr); }
  .sw { min-height: 70px; padding: 3mm; font-size: 9px; border-radius: 9px; }
  .sw b { font-size: 12px; }
  svg.ic { width: 22px; height: 22px; }
  .week { grid-template-columns: repeat(7, minmax(0, 1fr)); gap: 2mm; overflow: visible; }
  .day .f { overflow-wrap: anywhere; hyphens: auto; }
  .day { min-height: 0; padding: 2mm 1.6mm; border-radius: 8px; gap: 1.5mm; min-width: 0; }
  .day .d { font-size: 9px; letter-spacing: -0.01em; } .day .h { font-size: 7.5px; } .day .f { font-size: 8.5px; }
  .week { gap: 1.5mm !important; }
  .phones { gap: 2.5mm; overflow: visible; flex-wrap: nowrap; }
  .phones figure { width: calc((100% - 7 * 2.5mm) / 8); }
  .phones img { width: 100%; border-width: 2px; border-radius: 8px; }
  .phones figcaption { font-size: 7.5px; }
  .process { gap: 2mm; }
  .process li { grid-template-columns: 26px 1fr; gap: 3mm; font-size: 10.5px; }
  .process li::before { width: 22px; height: 22px; font-size: 11px; line-height: 19px; }
  .process li > div { padding-top: 3px; }
  .prob { font-size: 7px; padding: 2px 6px; }
  .toc { padding: 0; }
  .toc ol.toc-p { list-style: none; margin: 3mm 0 0; padding: 0; display: grid; grid-template-columns: 1fr 1fr; gap: 0 8mm; }
  .toc-p li { border-bottom: 1px solid var(--trait); }
  .toc-p li::before { content: none !important; }
  .toc-p a { flex: 1; width: 100%; display: grid; grid-template-columns: 22px auto 1fr auto; gap: 8px; align-items: baseline; padding-block: 2.2mm; color: inherit; text-decoration: none; font-size: 11.5px; font-weight: 500; }
  .toc-p .tn { font: 700 11px var(--serif); color: var(--terra); }
  .toc-p .lead-dots { border-bottom: 1.5px dotted rgba(31,42,68,.35); height: 0; align-self: center; margin-top: 4px; }
  .toc-p .tp { font: 700 10px var(--sans); color: var(--encre-douce); font-variant-numeric: tabular-nums; }
  .toc ol { grid-template-columns: repeat(3, 1fr); gap: 0 6mm; margin-top: 3mm; }
  .toc li { padding-block: 2.2mm; font-size: 11.5px; }
  .toc li::before { font-size: 11px; }

  /* Couverture et 4e de couverture */
  .cover-sheet { background: var(--nuit); background-image: none; color: var(--clair); }
  .cover-sheet .c { position: absolute; left: 18mm; right: 18mm; top: 22mm; bottom: 20mm; display: flex; flex-direction: column; justify-content: space-between; }
  .cover-sheet .top { display: flex; justify-content: space-between; gap: 8mm; font: 700 8px/1.5 var(--sans); letter-spacing: .18em; text-transform: uppercase; color: rgba(251,246,239,.65); }
  .cover-sheet .top span:first-child { max-width: 95mm; }
  .cover-sheet img.logo { width: 95mm; display: block; }
  .cover-sheet h1 { font-size: 64px; line-height: .95; color: var(--clair); }
  .cover-sheet h1 em { font-style: italic; font-weight: 600; color: var(--terra); }
  .cover-sheet .lead { color: rgba(251,246,239,.85); font-size: 14px; max-width: 120mm; margin-top: 6mm; }
  .cover-sheet .meta { display: grid; grid-template-columns: repeat(4, 1fr); gap: 5mm; border-top: 1px solid rgba(251,246,239,.2); padding-top: 6mm; }
  .cover-sheet .meta b { display: block; font: 700 14px/1.2 var(--serif); }
  .cover-sheet .meta span { font-size: 9px; color: rgba(251,246,239,.6); }
  .cover-sheet .bigroof { position: absolute; right: -30mm; bottom: 40mm; width: 150mm; fill: none; stroke: var(--clair); stroke-width: 14; stroke-linecap: round; stroke-linejoin: round; opacity: .07; }
  .back { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8mm; text-align: center; }
  .back img { width: 70mm; }
  .back p { color: rgba(251,246,239,.7); font-size: 11px; max-width: 120mm; }
  .back .h { font: 700 18px var(--serif); color: var(--clair); }
`;

const cover = `<div class="sheet cover-sheet">
  <svg class="bigroof" viewBox="0 0 360 140"><path d="M20 130 L180 14 L340 130"/></svg>
  <div class="c">
    <div class="top"><span>Mise en application · Les médias sociaux dans la stratégie digitale globale de la marque</span><span>Novembre 2026</span></div>
    <div>
      <img class="logo" src="img/logo-principal-negatif.svg" alt="">
      <h1 style="margin-top:14mm">Dossier<br><em>stratégique</em></h1>
      <p class="lead">Un compte Instagram et TikTok qui décode l'immobilier, la rénovation et l'investissement à Montpellier, en vidéos motion design de 30 secondes.</p>
    </div>
    <div class="meta">
      <div><b>@immo.decode</b><span>Instagram · TikTok</span></div>
      <div><b>2 nov. → 13 déc.</b><span>6 semaines de campagne</span></div>
      <div><b>3 000 abonnés</b><span>Objectif au 13 décembre</span></div>
      <div><b>#DevineLePrix</b><span>Le format challenge</span></div>
    </div>
  </div>
</div>`;
const back = `<div class="sheet cover-sheet"><div class="c back">
  <img src="img/logo-principal-negatif.svg" alt="">
  <div class="h">@immo.decode</div>
  <p>Dossier stratégique · Les médias sociaux dans la stratégie digitale globale de la marque · Novembre 2026</p>
</div></div>`;
const pages = PAGES.map((p, i) => `<div class="sheet">
  <div class="run"><b>${roof}Immo Décodé</b><span>Dossier stratégique · ${p.label}</span></div>
  <div class="inner"><div class="fit">${p.body}</div></div>
  <div class="folio"><span>@immo.decode</span><span class="n">Page ${i + 2} / ${total}</span></div>
</div>`).join("\n");

const html = `<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Dossier stratégique Immo Décodé</title><style>${fonts}${style}${printCss}</style></head><body>${sprite}${cover}${pages}${back}</body></html>`;
const tmp = path.join(here, ".print.html");
fs.writeFileSync(tmp, html);
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 794, height: 1123 } });
  await p.goto("file://" + tmp);
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(300);
  // Ajuste chaque page : agrandit le contenu (zoom) tant qu'il tient dans la page, jusqu'à 1,6×
  await p.$$eval(".sheet .inner", (els) => els.forEach((inner) => {
    const fit = inner.firstElementChild;
    const W = inner.clientWidth, H = inner.clientHeight;
    let best = 1;
    for (let z = 1.6; z >= 1; z -= 0.02) {
      fit.style.zoom = z;
      fit.style.width = W / z + "px";
      if (fit.getBoundingClientRect().height <= H - 4) { best = z; break; }
    }
    fit.style.zoom = best;
    fit.style.width = W / best + "px";
    // Répartit l'espace restant entre les parties d'une même page
    const rest = H - fit.getBoundingClientRect().height;
    if (rest > 40 && fit.children.length > 1) fit.style.gap = (parseFloat(getComputedStyle(fit).rowGap) + rest / best / (fit.children.length - 1) * 0.6) + "px";
    inner.dataset.zoom = best.toFixed(2);
  }));
  console.log("Zoom par page :", (await p.$$eval(".sheet .inner", (els) => els.map((e) => e.dataset.zoom))).join(" "));
  // Contrôle : aucune page ne doit déborder
  const over = await p.$$eval(".sheet .inner", (els) => els.map((e, i) => ({ page: i + 2, over: Math.round(e.firstElementChild.getBoundingClientRect().bottom - e.getBoundingClientRect().bottom) })).filter((x) => x.over > 1));
  if (over.length) console.log("DÉBORDEMENT :", JSON.stringify(over));
  const free = await p.$$eval(".sheet .inner", (els) => els.map((e, i) => `${i + 2}:${Math.round(e.getBoundingClientRect().bottom - e.firstElementChild.getBoundingClientRect().bottom)}px`));
  console.log("Espace libre en bas de page :", free.join(" "));
  await p.pdf({ path: path.join(here, "dossier-strategique-immo-decode.pdf"), preferCSSPageSize: true, printBackground: true, outline: true, tagged: true });
  await b.close();
  if (!process.argv.includes("--garder")) fs.unlinkSync(tmp);
})();
