import dns from 'node:dns/promises';
import http from 'node:http';
import https from 'node:https';
import net from 'node:net';
import ipaddr from 'ipaddr.js';

const REDIRECTS = new Set([301, 302, 303, 307, 308]);
const DEFAULT_TIMEOUT_MS = 9000;
const DEFAULT_MAX_BYTES = 2 * 1024 * 1024;

export function isPublicAddress(address) {
  if (!net.isIP(address)) return false;
  let parsed;
  try {
    parsed = ipaddr.parse(address);
    if (parsed.kind() === 'ipv6' && parsed.isIPv4MappedAddress()) parsed = parsed.toIPv4Address();
  } catch { return false; }
  return parsed.range() === 'unicast';
}

export function parseTargetUrl(raw) {
  const input = String(raw || '').trim();
  if (!input || input.length > 2048) throw new Error('Введите корректный URL');
  let url;
  try { url = new URL(input.includes('://') ? input : `https://${input}`); }
  catch { throw new Error('Не удалось разобрать URL'); }
  if (!['http:', 'https:'].includes(url.protocol)) throw new Error('Разрешены только HTTP и HTTPS');
  if (url.username || url.password) throw new Error('URL с логином или паролем не поддерживается');
  const host = url.hostname.toLowerCase().replace(/\.$/, '');
  if (!host || host === 'localhost' || host.endsWith('.localhost') || host.endsWith('.local') || host.endsWith('.internal')) throw new Error('Локальные адреса запрещены');
  url.hash = '';
  return url;
}

async function resolvePublicHost(hostname) {
  if (net.isIP(hostname)) {
    if (!isPublicAddress(hostname)) throw new Error('Приватные и служебные IP запрещены');
    return { address: hostname, family: net.isIP(hostname) };
  }
  const records = await dns.lookup(hostname, { all: true, verbatim: true });
  if (!records.length) throw new Error('DNS не вернул адрес для домена');
  if (records.some((record) => !isPublicAddress(record.address))) throw new Error('Домен резолвится в приватный или служебный IP');
  return records[0];
}

function headersToObject(headers) {
  const out = {};
  for (const [key, value] of Object.entries(headers || {})) out[key.toLowerCase()] = Array.isArray(value) ? value.join(', ') : String(value ?? '');
  return out;
}

async function requestOnce(url, { method = 'GET', timeoutMs = DEFAULT_TIMEOUT_MS, maxBytes = DEFAULT_MAX_BYTES } = {}) {
  const { address, family } = await resolvePublicHost(url.hostname);
  const client = url.protocol === 'https:' ? https : http;
  const started = Date.now();
  return new Promise((resolve, reject) => {
    const req = client.request({
      protocol: url.protocol,
      hostname: address,
      family,
      port: url.port || undefined,
      path: `${url.pathname || '/'}${url.search || ''}`,
      method,
      servername: url.protocol === 'https:' && net.isIP(url.hostname) === 0 ? url.hostname : undefined,
      headers: { Host: url.host, 'User-Agent': 'SiteAudit-Studio/0.1 (+https://alexgtup.github.io/)', Accept: method === 'HEAD' ? '*/*' : 'text/html,application/xhtml+xml,application/xml;q=0.9,text/plain;q=0.8,*/*;q=0.5', Connection: 'close' },
      rejectUnauthorized: true
    }, (res) => {
      const headers = headersToObject(res.headers);
      const status = Number(res.statusCode || 0);
      if (method === 'HEAD') { res.resume(); resolve({ status, headers, body: '', durationMs: Date.now() - started }); return; }
      const chunks = [];
      let size = 0;
      let settled = false;
      const fail = (error) => { if (settled) return; settled = true; res.destroy(); reject(error); };
      res.on('data', (chunk) => {
        size += chunk.length;
        if (size > maxBytes) { fail(new Error(`Ответ превышает лимит ${Math.round(maxBytes / 1024)} KB`)); return; }
        chunks.push(chunk);
      });
      res.on('end', () => { if (settled) return; settled = true; resolve({ status, headers, body: Buffer.concat(chunks).toString('utf8'), durationMs: Date.now() - started }); });
      res.on('error', fail);
    });
    req.setTimeout(timeoutMs, () => req.destroy(new Error(`Таймаут ${timeoutMs} мс`)));
    req.on('error', reject);
    req.end();
  });
}

export async function fetchSafe(rawUrl, options = {}) {
  const maxRedirects = Number.isInteger(options.maxRedirects) ? options.maxRedirects : 5;
  let current = parseTargetUrl(rawUrl);
  const redirects = [];
  for (let hop = 0; hop <= maxRedirects; hop += 1) {
    const response = await requestOnce(current, options);
    const location = response.headers.location;
    if (REDIRECTS.has(response.status) && location) {
      if (hop === maxRedirects) throw new Error('Слишком много редиректов');
      const next = parseTargetUrl(new URL(location, current).toString());
      redirects.push({ from: current.toString(), to: next.toString(), status: response.status });
      current = next;
      continue;
    }
    return { ...response, requestedUrl: parseTargetUrl(rawUrl).toString(), finalUrl: current.toString(), redirects };
  }
  throw new Error('Не удалось получить URL');
}

export async function headSafe(rawUrl, options = {}) {
  return fetchSafe(rawUrl, { ...options, method: 'HEAD', maxBytes: 0 });
}
