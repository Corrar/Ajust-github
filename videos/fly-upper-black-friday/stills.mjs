// node stills.mjs out_dir t1 t2 ...  → PNGs dos tempos pedidos (para revisão)
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PW || '/opt/node22/lib/node_modules/playwright');
import path from 'path'; import fs from 'fs';
const [out, ...ts] = process.argv.slice(2);
fs.mkdirSync(out, { recursive: true });
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
p.on('pageerror', e => console.error('PAGEERR', e.message));
await p.goto('file://' + path.resolve('index.html'));
await p.waitForFunction(() => window.__ready);
for (const t of ts) {
  await p.evaluate(t => render(t), +t);
  await p.screenshot({ path: `${out}/t${(+t).toFixed(2)}.png` });
}
await b.close();
