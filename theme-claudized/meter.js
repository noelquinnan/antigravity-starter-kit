// meter.js - local tweak (not in git, 小克 2026-11-25).
// A small "context used" badge in the input bar, like Claude Code's.
//
// Why a custom one: Antigravity has an official meter, but the public build
// ships it as an empty slot (buildBindings.contextUsageIndicator = undefined),
// so it cannot be switched on. The language server still computes
// ContextWindowUsage {estimatedTokensUsed, maxContextTokens,
// estimatedAfterCompaction} and sends it inside conversation updates, which
// travel as JSON text over the page's local WebSocket. This script only
// READS those messages (it never changes them) and draws the badge.
// Delete this file (and the require in inject.js) to undo.

const METER_SCRIPT = `(() => {
  if (window.__agMeter) return;
  const M = window.__agMeter = { byConv: {}, streamConv: {}, last: null };
  const UUID = /[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/;
  const currentConv = () => (location.pathname.match(/\\/c\\/([0-9a-f-]{36})/) || [])[1];

  // Outgoing frames tell us which conversation a stream belongs to.
  const origSend = WebSocket.prototype.send;
  WebSocket.prototype.send = function (data) {
    try {
      if (typeof data === 'string' && data.indexOf('"streamId"') >= 0) {
        const sid = (data.match(/"streamId":"([^"]+)"/) || [])[1];
        const conv = (data.match(/"(?:cascadeId|conversationId|trajectoryId)":"([0-9a-f-]{36})"/) || [])[1];
        if (sid && conv) M.streamConv[sid] = conv;
      }
    } catch {}
    return origSend.apply(this, arguments);
  };

  const find = (o, depth) => {
    if (!o || typeof o !== 'object' || depth > 12) return null;
    if (o.contextWindowUsage && typeof o.contextWindowUsage === 'object') return o.contextWindowUsage;
    for (const k in o) { const r = find(o[k], depth + 1); if (r) return r; }
    return null;
  };
  const seen = new WeakSet();
  const desc = Object.getOwnPropertyDescriptor(MessageEvent.prototype, 'data');
  if (desc && desc.get) {
    Object.defineProperty(MessageEvent.prototype, 'data', {
      configurable: true,
      enumerable: desc.enumerable,
      get() {
        const v = desc.get.call(this);
        if (typeof v === 'string' && !seen.has(this) && v.indexOf('contextWindowUsage') >= 0) {
          seen.add(this);
          try {
            const msg = JSON.parse(v);
            const u = find(msg, 0);
            if (u) {
              const conv = M.streamConv[msg.streamId] || (v.match(UUID) || [])[0];
              const rec = { used: Number(u.estimatedTokensUsed || 0), max: Number(u.maxContextTokens || 0),
                after: Number(u.estimatedAfterCompaction || 0), t: Date.now() };
              if (conv) M.byConv[conv] = rec;
              M.last = rec;
              render();
            }
          } catch {}
        }
        return v;
      },
    });
  }

  const fmt = (n) => n >= 1e6 ? (n / 1e6).toFixed(1) + 'M' : n >= 1e3 ? Math.round(n / 1e3) + 'k' : String(n);
  function render() {
    const footer = document.querySelector('.agy-composer-footer');
    const right = footer && footer.lastElementChild;
    let el = document.getElementById('ag-ctx-meter');
    const conv = currentConv();
    const rec = (conv && M.byConv[conv]) || null;
    if (!right || !rec || !rec.max) { if (el) el.style.display = 'none'; return; }
    if (!el) {
      el = document.createElement('span');
      el.id = 'ag-ctx-meter';
      el.innerHTML = '<svg viewBox="0 0 20 20" width="15" height="15"><circle cx="10" cy="10" r="8" fill="none" stroke-width="2.4" class="bg"/><circle cx="10" cy="10" r="8" fill="none" stroke-width="2.4" class="fg" stroke-linecap="round" transform="rotate(-90 10 10)"/></svg><b></b>';
    }
    if (el.parentElement !== right) right.insertBefore(el, right.firstChild);
    const pct = Math.min(100, Math.round(rec.used / rec.max * 100));
    const c = 2 * Math.PI * 8;
    const fg = el.querySelector('.fg');
    fg.setAttribute('stroke-dasharray', (c * pct / 100).toFixed(1) + ' ' + c.toFixed(1));
    el.dataset.level = pct >= 85 ? 'high' : pct >= 60 ? 'mid' : 'low';
    el.querySelector('b').textContent = pct + '%';
    el.title = '上下文 ' + fmt(rec.used) + ' / ' + fmt(rec.max) + ' tokens（' + pct + '%）' +
      (rec.after ? '\\n压缩后约 ' + fmt(rec.after) : '') + '\\n发送 /compact 可手动压缩';
    el.style.display = '';
  }
  M.render = render;
  setInterval(render, 1000); // React may re-render the footer; put the badge back.
})();`;

module.exports = { METER_SCRIPT };
