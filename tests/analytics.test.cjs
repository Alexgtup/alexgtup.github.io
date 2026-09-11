const { test } = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const source = fs.readFileSync('assets/analytics.js', 'utf8');

function page(saved, storageBlocked = false) {
  const calls = [], scripts = [], handlers = {};
  const node = name => ({ hidden: true, focus() {}, querySelector() { return { focus() {} }; },
    addEventListener(event, fn) { handlers[name + ':' + event] = fn; } });
  const box = node('box'), settings = node('settings');
  const context = {
    URL, Date,
    location: { pathname: '/web-development/', href: 'https://alexgtup.github.io/web-development/' },
    localStorage: { getItem() { if (storageBlocked) throw Error('blocked'); return saved; },
      setItem(_, value) { if (storageBlocked) throw Error('blocked'); saved = value; } },
    document: {
      querySelector(selector) { return selector.includes('data-analytics-consent') ? box
        : selector.includes('data-analytics-settings') ? settings : scripts[0] || null; },
      createElement() { return { dataset: {} }; },
      head: { appendChild(script) { scripts.push(script); } },
      addEventListener(event, fn) { handlers['document:' + event] = fn; },
    },
  };
  context.window = { ym: (...args) => calls.push(args), addEventListener(event, fn) { handlers['window:' + event] = fn; } };
  vm.runInNewContext(source, context);
  return { context, calls, scripts, box, settings,
    choose(value) { handlers['box:click']({ target: { closest() { return { dataset: { analyticsChoice: value } }; } } }); },
    storage(value) { handlers['window:storage']({ key: 'alexuys-analytics-consent-v1', newValue: value }); },
    click(url, demo, offer) { handlers['document:click']({ target: { closest() { return { href: url, dataset: { demo, offer } }; } } }); },
  };
}
test('no tracking or remote script before consent', () => {
  const p = page(null); p.click('https://t.me/Alexuys');
  assert.equal(p.box.hidden, false); assert.equal(p.scripts.length, 0); assert.equal(p.calls.length, 0);
});
test('both historic opt-in formats initialize exactly once with consent-only interaction analytics', () => {
  for (const value of ['yes', 'accepted']) {
    const p = page(value); p.choose('accepted'); vm.runInNewContext(source, p.context);
    assert.equal(p.scripts.length, 1); assert.equal(p.calls.filter(c => c[1] === 'init').length, 1);
    assert.equal(p.calls[0][2].webvisor, true);
    assert.equal(p.calls[0][2].trackLinks, true);
    assert.equal(p.calls[0][2].clickmap, true);
  }
});
test('both historic opt-out formats stay opted out', () => {
  for (const value of ['no', 'declined']) { const p = page(value); assert.equal(p.box.hidden, true); assert.equal(p.scripts.length, 0); }
});
test('contact and demo goals are recorded after consent without message text', () => {
  const p = page(null); p.choose('accepted');
  p.click('https://t.me/Alexuys?text=private');
  p.click('https://sheetpilot-ai-6omr.onrender.com', 'sheetpilot-ai');
  assert.deepEqual(p.calls.filter(c => c[1] === 'reachGoal').map(c => c[2]), ['telegram_click', 'demo_open']);
  assert.equal(JSON.stringify(p.calls).includes('private'), false);
});
test('freelance offer interest is recorded with a bounded offer key', () => {
  const p = page(null); p.choose('accepted');
  p.click('https://alexgtup.github.io/n8n-automation/', undefined, 'n8n');
  const hit = p.calls.filter(c => c[1] === 'reachGoal').at(-1);
  assert.equal(hit[2], 'freelance_offer_open');
  assert.equal(hit[3].offer, 'n8n');
  assert.equal(hit[3].page, '/web-development/');
});
test('revocation destroys tracking and reaccepting initializes again without a second script', () => {
  const p = page('accepted'); p.choose('declined');
  assert.equal(p.calls.at(-1)[1], 'destruct');
  const count = p.calls.length; p.click('https://t.me/Alexuys'); assert.equal(p.calls.length, count);
  p.choose('accepted'); assert.equal(p.calls.at(-1)[1], 'init'); assert.equal(p.scripts.length, 1);
});
test('another tab can revoke consent', () => {
  const p = page('yes'); p.storage('no'); assert.equal(p.calls.at(-1)[1], 'destruct');
  assert.equal(p.context.window.alexuysAnalytics.consent, 'declined');
});
test('blocked storage does not break consent controls', () => {
  const p = page(null, true); p.choose('accepted'); assert.equal(p.scripts.length, 1);
  p.choose('declined'); assert.equal(p.calls.at(-1)[1], 'destruct');
});

test('UX analytics records funnel and proof metadata without sending visitor-entered text', () => {
  const handoff = fs.readFileSync('assets/stage101-intent-handoff.js', 'utf8');
  for (const goal of [
    'catalog_filter', 'catalog_search', 'brief_start', 'brief_ready', 'brief_preview', 'brief_copy', 'brief_submit',
    'live_proof_open', 'review_open', 'proof_cases_open', 'reviews_anchor_open'
  ]) {
    assert.equal(handoff.includes(`'${goal}'`), true, `missing UX goal ${goal}`);
  }
  assert.equal(handoff.includes("goal('catalog_search', { family, length:"), true);
  assert.equal(handoff.includes("url.hostname === 'freelance.ru'"), true);
  assert.equal(handoff.includes("link.closest('.s115-live-proof')"), true);
  assert.equal(/goal\([^\n]*task\.value/.test(handoff), false);
  assert.equal(/goal\([^\n]*search\.value/.test(handoff), false);
  assert.equal(/goal\([^\n]*url\.search/.test(handoff), false);
});

test('navigation continuity owns browsing state but not Telegram draft mutation', () => {
  const continuity = fs.readFileSync('assets/navigation-continuity.js', 'utf8');
  for (const hub of ['/cases/', '/en/cases/', '/guides/', '/en/guides/', '/tools/', '/services/', '/en/services/', '/demos/']) {
    assert.equal(continuity.includes(`path: '${hub}'`), true, `missing continuity hub ${hub}`);
  }
  assert.equal(continuity.includes('location.pathname + location.search + location.hash'), true);
  assert.equal(continuity.includes('scrollY'), true);
  assert.equal(continuity.includes("goal('catalog_return'"), true);
  assert.equal(continuity.includes('t.me/Alexuys'), false);
  assert.equal(continuity.includes('searchParams.set(\'text\''), false);
});
