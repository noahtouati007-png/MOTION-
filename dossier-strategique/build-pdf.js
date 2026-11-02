// Génère dossier-strategique.pdf (A4) à partir de index.html, polices locales.
// Usage : NODE_PATH=$(npm root -g) node dossier-strategique/build-pdf.js
const { chromium } = require("playwright");
const fs = require("fs"), path = require("path");
const here = __dirname, w2 = path.resolve(here, "../charte-graphique/_source/woff2");
const ff = (fam, file, w, it) => `@font-face{font-family:"${fam}";src:url("file://${w2}/${file}.woff2");font-weight:${w};font-style:${it ? "italic" : "normal"}}`;
const fonts = [ff("Fraunces", "fraunces-latin-600-normal", 600), ff("Fraunces", "fraunces-latin-700-normal", 700), ff("Fraunces", "fraunces-latin-600-italic", 600, 1), ff("Inter", "inter-latin-400-normal", 400), ff("Inter", "inter-latin-500-normal", 500), ff("Inter", "inter-latin-700-normal", 700), ff("Inter", "inter-latin-800-normal", 800)].join("");
const src = fs.readFileSync(path.join(here, "index.html"), "utf8").replace(/<link[^>]+fonts\.g[^>]+>\s*/g, "");
const html = `<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>${fonts}@page{size:A4;margin:12mm 0}</style></head><body>${src}</body></html>`;
const tmp = path.join(here, ".print.html");
fs.writeFileSync(tmp, html);
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1100, height: 1400 } });
  await p.goto("file://" + tmp);
  await p.evaluate(() => document.fonts.ready);
  if (process.argv[2]) {
    await p.screenshot({ path: process.argv[2] + "-desktop.png", fullPage: true });
    await p.setViewportSize({ width: 400, height: 900 });
    await p.screenshot({ path: process.argv[2] + "-mobile.png", fullPage: false });
    await p.setViewportSize({ width: 1100, height: 1400 });
  }
  await p.pdf({ path: path.join(here, "dossier-strategique-immo-decode.pdf"), format: "A4", printBackground: true, margin: { top: "0", bottom: "0" }, scale: 0.72 });
  await b.close();
  fs.unlinkSync(tmp);
})();
