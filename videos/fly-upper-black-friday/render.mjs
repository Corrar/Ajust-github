// node render.mjs fps from to out.mkv [scale]  → renderiza quadros [from,to) direto num ffmpeg (sem PNGs em disco)
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PW || '/opt/node22/lib/node_modules/playwright');
import path from 'path'; import { spawn } from 'child_process';
const [fps, from, to, out, scale = '1'] = process.argv.slice(2);
const sc = +scale, W = Math.round(1080 * sc), H = Math.round(1920 * sc);
const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', fps, '-i', '-',
  '-c:v', 'libx264', '-preset', 'fast', '-crf', sc < 1 ? '23' : '8', '-pix_fmt', 'yuv444p', out], { stdio: ['pipe', 'inherit', 'inherit'] });
const b = await chromium.launch({ args: ['--force-color-profile=srgb'] });
const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: sc });
p.on('pageerror', e => console.error('PAGEERR', e.message));
await p.goto('file://' + path.resolve('index.html'));
await p.waitForFunction(() => window.__ready);
for (let f = +from; f < +to; f++) {
  await p.evaluate(t => render(t), f / +fps);
  const buf = await p.screenshot({ type: 'jpeg', quality: 98 });
  if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
}
ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close();
