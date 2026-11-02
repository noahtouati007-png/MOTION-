// Exporte charte-graphique.pdf + PNG des logos. Usage : node charte-graphique/_source/export.js
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");
const root = path.resolve(__dirname, "..");
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1600, height: 900 } });
  await p.goto("file://" + path.join(__dirname, "charte.html"));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(400);
  await p.pdf({ path: path.join(root, "charte-graphique.pdf"), width: "1600px", height: "900px", printBackground: true });
  if (process.argv[2] === "--apercu") {
    const n = await p.$$eval(".page", (e) => e.length);
    for (let i = 0; i < n; i++) {
      await p.evaluate((i) => window.scrollTo(0, i * 900), i);
      await p.screenshot({ path: path.join(process.argv[3], `page-${i + 1}.png`) });
    }
  }
  const out = path.join(root, "logo", "png");
  fs.mkdirSync(out, { recursive: true });
  for (const f of fs.readdirSync(path.join(root, "logo")).filter((f) => f.endsWith(".svg") && !f.includes("TEXTE"))) {
    const svg = fs.readFileSync(path.join(root, "logo", f), "utf8");
    const [, w, h] = svg.match(/width="(\d+)" height="(\d+)"/);
    const scale = 2000 / Math.max(+w, +h);
    const q = await b.newPage({ viewport: { width: Math.round(w * scale), height: Math.round(h * scale) } });
    const tmp = path.join(require("os").tmpdir(), "logo-export.html");
    fs.writeFileSync(tmp, `<html><body style="margin:0;background:transparent"><img src="file://${path.join(root, "logo", f)}" style="width:100%;display:block"></body></html>`);
    await q.goto("file://" + tmp);
    await q.waitForTimeout(150);
    await q.screenshot({ path: path.join(out, f.replace(".svg", ".png")), omitBackground: true });
    await q.close();
  }
  await b.close();
})();
