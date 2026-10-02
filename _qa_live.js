const puppeteer = require('c:/Users/Gentech/CodeBuddy/奶龙moni/node_modules/puppeteer-core');
(async () => {
  const b = await puppeteer.launch({ executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', headless: true });
  const pg = await b.newPage();
  await pg.setViewport({ width: 1280, height: 560 });
  pg.on('pageerror', e => console.log('PAGE ERROR:', e.message.slice(0, 300)));
  pg.on('console', m => { if (m.type() === 'error') console.log('CONSOLE ERR:', m.text().slice(0, 200)); });
  pg.on('requestfailed', r => console.log('REQ FAIL:', r.url().slice(-70), r.failure() && r.failure().errorText));
  pg.on('response', r => { if (r.status() >= 400) console.log('HTTP', r.status(), r.url().slice(-80)); });
  await pg.goto('https://www.bilibili.com/toy/preview/preview_o44GY3pj/index.html', { waitUntil: 'networkidle2', timeout: 60000 });
  await new Promise(r => setTimeout(r, 3000));
  const f = pg.frames().find(f => f.url().includes('bilibilitoy.com'));
  const st0 = await f.evaluate(() => {
    const c = document.getElementById('cv');
    return { cw: c.width, ch: c.height, cssW: Math.round(c.getBoundingClientRect().width), startCls: document.getElementById('startScreen').className };
  });
  console.log('BEFORE:', JSON.stringify(st0));
  await f.click('#startBtn');
  await new Promise(r => setTimeout(r, 1200));
  const st1 = await f.evaluate(() => {
    const v = document.getElementById('vid');
    return {
      display: getComputedStyle(v).display, src: v.src.split('/').pop(),
      t: v.currentTime.toFixed(2), ready: v.readyState, netState: v.networkState,
      err: v.error && v.error.code, paused: v.paused, muted: v.muted,
      startCls: document.getElementById('startScreen').className
    };
  });
  console.log('AFTER CLICK:', JSON.stringify(st1));
  await new Promise(r => setTimeout(r, 3500));
  const st2 = await f.evaluate(() => {
    const v = document.getElementById('vid');
    return { display: getComputedStyle(v).display, t: v.currentTime.toFixed(2), paused: v.paused };
  });
  console.log('LATER:', JSON.stringify(st2));
  await b.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });
