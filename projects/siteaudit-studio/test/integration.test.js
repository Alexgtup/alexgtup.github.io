import test from 'node:test';
import assert from 'node:assert/strict';
import { auditSite } from '../src/audit.js';

const runNetworkTests = process.env.RUN_NETWORK_TESTS === '1';

test('live audit can crawl the production portfolio through the safe network layer', { skip: !runNetworkTests, timeout: 90000 }, async () => {
  const report = await auditSite('https://alexgtup.github.io/');
  assert.equal(report.response.status, 200);
  assert.equal(report.finalUrl, 'https://alexgtup.github.io/');
  assert.equal(report.page.noindex, false);
  assert.ok(report.page.title.length > 0);
  assert.ok(report.discovery.crawledPages >= 1);
  assert.equal(report.discovery.robots.present, true);
  assert.equal(report.discovery.sitemap.present, true);
  assert.ok(report.discovery.sitemap.urlCount >= 50);
});
