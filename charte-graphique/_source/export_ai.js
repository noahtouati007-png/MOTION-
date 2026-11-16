// Exporte les fichiers Illustrator (.ai compatibles PDF, vectoriels) dans charte-graphique/illustrator/
// Usage : node charte-graphique/_source/export_ai.js
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");
const root = path.resolve(__dirname, "..");
const out = path.join(root, "illustrator");
fs.mkdirSync(out, { recursive: true });
const read = (f) => fs.readFileSync(path.join(root, f), "utf8").replace(/<\?xml[^>]*>\s*/, "");
const size = (svg) => svg.match(/width="(\d+)" height="(\d+)"/).slice(1).map(Number);
const C = [["Sable", "#F2E8DC", "242 232 220", "0 4 9 5"], ["Bleu nuit", "#1F2A44", "31 42 68", "54 38 0 73"], ["Terracotta", "#C8553D", "200 85 61", "0 58 70 22"], ["Vert olivier", "#6B7F4E", "107 127 78", "16 0 39 50"], ["Sable clair", "#FBF6EF", "251 246 239", "0 2 5 2"]];
const fonts = ["fraunces-latin-700-normal", "inter-latin-500-normal", "inter-latin-700-normal"].map((f) => {
  const [fam, , w] = f.split("-");
  return `@font-face{font-family:"${fam === "fraunces" ? "Fraunces" : "Inter"}";src:url("file://${path.join(__dirname, "woff2", f + ".woff2")}");font-weight:${w}}`;
}).join("");
const page = (w, h, body, bg = "transparent") => `<!doctype html><html><head><meta charset="utf-8"><style>${fonts}@page{size:${w}px ${h}px;margin:0}html,body{margin:0;width:${w}px;height:${h}px;background:${bg};font-family:Inter}</style></head><body>${body}</body></html>`;

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  const tmp = path.join(require("os").tmpdir(), "ai-export.html");
  async function save(name, w, h, html) {
    fs.writeFileSync(tmp, html);
    await p.setViewportSize({ width: Math.min(w, 4000), height: Math.min(h, 4000) });
    await p.goto("file://" + tmp);
    await p.evaluate(() => document.fonts.ready);
    await p.pdf({ path: path.join(out, name + ".ai"), width: w + "px", height: h + "px", printBackground: true, pageRanges: "1" });
  }
  // 1. Un fichier par logo
  for (const f of fs.readdirSync(path.join(root, "logo")).filter((f) => f.endsWith(".svg"))) {
    const svg = read("logo/" + f);
    const [w, h] = size(svg);
    await save(f.replace(".svg", ""), w, h, page(w, h, svg));
  }
  // 2. Planche des illustrations
  const pl = read("illustrations/planche-illustrations.svg");
  const [pw, ph] = size(pl);
  await save("illustrations-planche", pw, ph, page(pw, ph, pl));
  // 3. Palette
  const sw = C.map(([n, hx, rgb, cmyk], i) => `<div style="position:absolute;left:${60 + i * 330}px;top:60px;width:300px"><div style="height:300px;border-radius:24px;background:${hx};border:2px solid rgba(31,42,68,.15)"></div><div style="font:700 30px Fraunces;margin-top:18px;color:#1F2A44">${n}</div><div style="font:500 20px/1.6 Inter;color:#1F2A44">${hx}<br>RVB ${rgb}<br>CMJN ${cmyk}</div></div>`).join("");
  await save("couleurs-palette", 1770, 560, page(1770, 560, sw, "#FBF6EF"));
  // 4. Kit complet : tout sur un seul plan de travail
  const L = (f, x, y, wd) => { const s = read(f); const [w, h] = size(s); return `<div style="position:absolute;left:${x}px;top:${y}px;width:${wd}px;height:${(wd * h) / w}px">${s.replace(/width="\d+" height="\d+"/, 'width="100%" height="100%"')}</div>`; };
  const kit = [
    `<div style="position:absolute;left:80px;top:60px;font:700 64px Fraunces;color:#1F2A44">Immo Décodé · kit de marque</div>`,
    L("logo/logo-principal-couleur.svg", 80, 200, 620),
    L("logo/logo-principal-negatif.svg", 760, 200, 620),
    L("logo/logo-principal-mono-nuit.svg", 1440, 200, 620),
    L("logo/logo-horizontal-couleur.svg", 80, 780, 1300),
    L("logo/logo-horizontal-negatif.svg", 80, 1100, 1300),
    L("logo/monogramme-terracotta.svg", 1460, 780, 280),
    L("logo/monogramme-nuit.svg", 1780, 780, 280),
    L("logo/monogramme-sable.svg", 1460, 1100, 280),
    L("illustrations/planche-illustrations.svg", 2140, 200, 1280),
    `<div style="position:absolute;left:2140px;top:780px;width:1300px">${sw.replace(/left:(\d+)px;top:60px;width:300px/g, (m, x) => `left:${(x - 60) * 0.78}px;top:0;width:234px`).replace(/height:300px/g, "height:234px")}</div>`,
  ].join("");
  await save("IMMO-DECODE-kit-complet", 3500, 1500, page(3500, 1500, `<div style="position:relative;width:3500px;height:1500px">${kit}</div>`, "#F2E8DC"));
  await b.close();
  // 5. La charte : chaque page en .ai + le document complet
  const { PDFDocument } = (() => { try { return require("pdf-lib"); } catch { return {}; } })();
  fs.copyFileSync(path.join(root, "charte-graphique.pdf"), path.join(out, "charte-graphique-complete.ai"));
  if (PDFDocument) {
    const src = await PDFDocument.load(fs.readFileSync(path.join(root, "charte-graphique.pdf")));
    for (let i = 0; i < src.getPageCount(); i++) {
      const d = await PDFDocument.create();
      const [pg] = await d.copyPages(src, [i]);
      d.addPage(pg);
      fs.writeFileSync(path.join(out, `charte-page-${String(i + 1).padStart(2, "0")}.ai`), await d.save());
    }
  }
})();
