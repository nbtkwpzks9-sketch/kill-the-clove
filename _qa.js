const http = require('http');
const fs = require('fs');
const path = require('path');
const puppeteer = require('c:/Users/Gentech/CodeBuddy/奶龙moni/node_modules/puppeteer-core');
const mime = { '.html': 'text/html', '.png': 'image/png', '.jpg': 'image/jpeg', '.gif': 'image/gif' };
const srv = http.createServer((q, s) => {
  var p = q.url.split('?')[0]; if (p === '/') p = '/index.html';
  fs.readFile(path.join(__dirname, p), (e, d) => {
    if (e) { s.writeHead(404); s.end(); return; }
    s.writeHead(200, { 'Content-Type': mime[path.extname(p).toLowerCase()] || 'text/plain' }); s.end(d);
  });
});
(async () => {
  await new Promise(r => srv.listen(8801, '127.0.0.1', r));
  const b = await puppeteer.launch({ executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', headless: true });
  const pg = await b.newPage();
  await pg.setViewport({ width: 1280, height: 720 });
  pg.on('pageerror', e => console.log('PAGE ERROR:', e.message));
  pg.on('response', r => { if (r.status() >= 400) console.log('HTTP', r.status(), r.url()); });
  pg.on('console', m => { if (m.type() === 'error') console.log('CONSOLE ERR:', m.text().slice(0, 120)); });
  await pg.goto('http://127.0.0.1:8801/index.html', { waitUntil: 'networkidle2' });
  await new Promise(r => setTimeout(r, 600));
  const imgs = await pg.evaluate(() => Array.from(document.images).map(i => i.naturalWidth + 'x' + i.naturalHeight));
  console.log('IMGS:', imgs.join(' | '));
  await pg.click('#startBtn');
  await new Promise(r => setTimeout(r, 700));
  const v1 = await pg.evaluate(() => {
    const v = document.getElementById('vid');
    return 'display=' + getComputedStyle(v).display + ' src=' + v.src.split('/').pop() + ' t=' + v.currentTime.toFixed(2);
  });
  console.log('VIDEO intro:', v1);
  await new Promise(r => setTimeout(r, 2500));
  const v2 = await pg.evaluate(() => 'display=' + getComputedStyle(document.getElementById('vid')).display);
  console.log('VIDEO after:', v2);
  await new Promise(r => setTimeout(r, 800));
  await pg.screenshot({ path: '_qa_p1.png' });
  await pg.keyboard.down('Space');
  await new Promise(r => setTimeout(r, 6000));
  await pg.keyboard.up('Space');
  await new Promise(r => setTimeout(r, 1500));
  await pg.screenshot({ path: '_qa_p2.png' });
  const st = await pg.evaluate(() => {
    const c = document.getElementById('cv');
    const r = c.getBoundingClientRect();
    return c.width + 'x' + c.height + ' css ' + Math.round(r.width) + 'x' + Math.round(r.height) + ' ratio ' + (r.width / r.height).toFixed(3);
  });
  console.log('CANVAS:', st);
  const dec = await pg.evaluate(() => Promise.all(
    ['assets/king_sleep.png', 'assets/king_alert.png', 'assets/spy_sneak_cut.png', 'assets/spy_walk_sheet.png']
      .map(u => new Promise(res => {
        const i = new Image();
        i.onload = () => res(u + ' ' + i.naturalWidth + 'x' + i.naturalHeight);
        i.onerror = () => res(u + ' FAIL');
        i.src = u;
      }))));
  console.log('SPRITES:', dec.join(' | '));
  await b.close(); srv.close();
})();
