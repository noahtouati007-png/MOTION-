// Aperçu PNG d'un SVG Galzin (polices de remplacement : Anton = Impact, Zilla Slab = Heroica).
// usage : node apercu.js fichier.svg sortie.png [largeurPx=1400]
// Nécessite Playwright + Chromium (sinon : ouvrir le SVG dans Illustrator ou un navigateur).
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const F = path.resolve(__dirname, '../assets/fonts-apercu');
(async () => {
  const [file, out, pw = '1400'] = process.argv.slice(2);
  let svg = fs.readFileSync(file, 'utf8').replace(/<\?xml[^>]*>/, '');
  const m = svg.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/); const w = +pw, h = Math.round(w * m[2] / m[1]);
  svg = svg.replace(/width="[\d.]+mm" height="[\d.]+mm"/, `width="${w}" height="${h}"`);
  const ff = (st, wt, f) => `@font-face{font-family:"Eroika Slab";font-style:${st};font-weight:${wt};src:url(file://${F}/${f})}`;
  const css = `@font-face{font-family:Impact;src:url(file://${F}/anton-latin-400-normal.woff2)}` +
    ff('normal', 400, 'zilla-slab-latin-700-normal.woff2') + ff('normal', 700, 'zilla-slab-latin-700-normal.woff2') +
    ff('italic', 400, 'zilla-slab-latin-700-italic.woff2') + ff('italic', 700, 'zilla-slab-latin-700-italic.woff2');
  const tmp = path.resolve(out + '.html');
  fs.writeFileSync(tmp, `<meta charset="utf-8"><style>${css}body{margin:0}</style>${svg}`);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: w, height: h } });
  await p.goto('file://' + tmp); await p.waitForTimeout(800); await p.screenshot({ path: out });
  fs.unlinkSync(tmp); await b.close();
})();
