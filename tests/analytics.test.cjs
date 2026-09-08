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
    click(url, demo) { handlers['document:click']({ target: { closest() { return { href: url, dataset: { demo } }; } } }); },
  };
}
test('no tracking or remote script before consent', () => {
  const p = page(null); p.click('https://t.me/Alexuys');
  assert.equal(p.box.hidden, false); assert.equal(p.scripts.length, 0); assert.equal(p.calls.length, 0);
});
test('both historic opt-in formats initialize exactly once, including repeated execution', () => {
  for (const value of ['yes', 'accepted']) {
    const p = page(value); p.choose('accepted'); vm.runInNewContext(source, p.context);
    assert.equal(p.scripts.length, 1); assert.equal(p.calls.filter(c => c[1] === 'init').length, 1);
    assert.equal(p.calls[0][2].webvisor, false);
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
