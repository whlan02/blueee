"""生成多语言官网：python build.py
英文直接写进 HTML（没有 JS 也能读），所有语言放在 i18n.js，由右上角的语言下拉切换。默认英文。"""
import json
import pathlib

from translations import L

ISSUES = '<a href="https://github.com/whlan02/blueee/issues">github.com/whlan02/blueee/issues</a>'
EN = L['en']
import hashlib
RTL = ['ar', 'ur', 'fa', 'he']


def fill(s):
    return s.replace('{issues}', ISSUES).replace('{privacy}', f'<a href="privacy.html">{EN["privacyLink"]}</a>')


def el(tag, key):
    return f'<{tag} data-i18n="{key}">{fill(EN[key])}</{tag}>'


CSS = '''*{box-sizing:border-box}body{margin:0;font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC",sans-serif;color:#114163;background:linear-gradient(160deg,#e3e3fe,#c7dcf8) fixed;min-height:100vh}
main{max-width:720px;margin:0 auto;padding:40px 20px 80px}header{display:flex;gap:18px;flex-wrap:wrap;align-items:center;margin-bottom:32px;font-size:15px}
header .sp{flex:1}header{position:relative}.lang{position:relative}
#langBtn{display:inline-flex;align-items:center;gap:8px;font:inherit;font-size:15px;color:#114163;background:rgba(255,255,255,.55);border:1px solid rgba(17,65,99,.14);border-radius:999px;padding:8px 14px;cursor:pointer;backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);transition:background .15s}
#langBtn:hover,#langBtn[aria-expanded=true]{background:rgba(255,255,255,.85)}#langBtn svg:last-child{opacity:.6;transition:transform .15s}#langBtn[aria-expanded=true] svg:last-child{transform:rotate(180deg)}
#langPanel{position:absolute;inset-inline-end:0;top:calc(100% + 8px);z-index:10;width:min(680px,calc(100vw - 40px));max-height:calc(100vh - 110px);overflow:auto;scrollbar-width:thin;scrollbar-color:rgba(17,65,99,.28) transparent;padding:10px;display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:4px;background:rgba(255,255,255,.88);backdrop-filter:blur(24px);-webkit-backdrop-filter:blur(24px);border:1px solid rgba(17,65,99,.1);border-radius:22px;box-shadow:0 16px 48px rgba(17,65,99,.22)}
#langPanel::-webkit-scrollbar{width:8px}#langPanel::-webkit-scrollbar-track{background:transparent;margin:14px 0}#langPanel::-webkit-scrollbar-thumb{background:rgba(17,65,99,.28);border-radius:999px;border:2px solid transparent;background-clip:padding-box}#langPanel[hidden]{display:none}#langPanel button{font:inherit;font-size:15px;color:#114163;text-align:start;background:none;border:0;border-radius:12px;padding:9px 12px;cursor:pointer}
#langPanel button:hover{background:rgba(17,65,99,.08)}#langPanel button[aria-current=true]{background:#114163;color:#fff}#langBtn:focus-visible,#langPanel button:focus-visible{outline:2px solid #114163;outline-offset:2px}
a{color:#114163}h1{font-size:34px;margin:0 0 4px}h2{font-size:20px;margin-top:28px}.card{background:rgba(255,255,255,.7);border-radius:22px;padding:8px 24px 24px;margin-top:20px}
img.icon{width:96px;height:96px;border-radius:22px;box-shadow:0 8px 24px rgba(17,65,99,.25)}footer{margin-top:40px;font-size:13px;opacity:.65}[dir=rtl] ul{padding-right:1.4em;padding-left:0}'''

GLOBE = ('<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
         'stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9S14.5 18.4 12 21c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z"/></svg>')
CHEVRON = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>'
NAV = ''.join(f'<a data-i18n="nav.{k}" href="{href}">{EN["nav." + k]}</a>' for k, href in
              [('home', 'index.html'), ('privacy', 'privacy.html'), ('terms', 'terms.html'), ('support', 'support.html')])
PICKER = (f'<div class="lang"><button id="langBtn" type="button" aria-haspopup="true" aria-expanded="false" aria-controls="langPanel">'
          f'{GLOBE}<span id="langName">English</span>{CHEVRON}</button><div id="langPanel" role="menu" hidden></div></div>')
HEADER = f'<header>{NAV}<span class="sp"></span>{PICKER}</header>'


def page(filename, title_key, body):
    html = (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{EN[title_key]} – Blueee</title><link rel="icon" href="icon.png"><style>{CSS}</style></head>'
            f'<body><main>{HEADER}{body}<footer data-i18n="foot">{EN["foot"]}</footer></main>'
            f'<script src="i18n.js?v={VERSION}"></script></body></html>')
    pathlib.Path(filename).write_text(html, encoding='utf-8')


def card(*parts):
    return '<div class="card">' + ''.join(parts) + '</div>'


translations = {code: {k: fill(v) for k, v in data.items()} for code, data in L.items()}
script = 'var T=' + json.dumps(translations, ensure_ascii=False) + ';\nvar RTL=' + json.dumps(RTL) + ''';
(function () {
  var KEY = 'blueee-lang';
  var btn = document.getElementById('langBtn'), panel = document.getElementById('langPanel'), label = document.getElementById('langName');
  var fromUrl = new URLSearchParams(location.search).get('lang');
  function saved() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  var lang = [fromUrl, saved()].find(function (c) { return c && T[c]; }) || 'en';

  function apply(code) {
    var d = T[code];
    document.documentElement.lang = code === 'zh' ? 'zh-Hans' : code;
    document.documentElement.dir = RTL.indexOf(code) >= 0 ? 'rtl' : 'ltr';
    document.querySelectorAll('[data-i18n]').forEach(function (e) {
      var v = d[e.dataset.i18n]; if (v != null) e.innerHTML = v;
    });
    var h1 = document.querySelector('h1');
    document.title = (h1 ? h1.textContent : 'Blueee') + ' – Blueee';
    label.textContent = d.name;
    panel.querySelectorAll('button').forEach(function (b) {
      if (b.dataset.code === code) b.setAttribute('aria-current', 'true'); else b.removeAttribute('aria-current');
    });
  }
  function setOpen(open) {
    panel.hidden = !open;
    btn.setAttribute('aria-expanded', String(open));
    if (open) (panel.querySelector('[aria-current]') || panel.firstChild).focus();
  }

  Object.keys(T).forEach(function (code) {
    var item = document.createElement('button');
    item.type = 'button'; item.role = 'menuitem'; item.dataset.code = code; item.textContent = T[code].name;
    item.lang = code === 'zh' ? 'zh-Hans' : code;
    item.addEventListener('click', function () {
      try { localStorage.setItem(KEY, code); } catch (e) {}
      apply(code); setOpen(false); btn.focus();
    });
    panel.appendChild(item);
  });
  btn.addEventListener('click', function () { setOpen(panel.hidden); });
  document.addEventListener('click', function (e) { if (!panel.hidden && !e.target.closest('.lang')) setOpen(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !panel.hidden) { setOpen(false); btn.focus(); } });
  apply(lang);
})();
'''
pathlib.Path('i18n.js').write_text(script, encoding='utf-8')
VERSION = hashlib.md5(script.encode()).hexdigest()[:8]  # 脚本或文案任何变化，地址就变，浏览器不会用旧缓存

page('index.html', 'nav.home',
     '<img class="icon" src="icon.png" alt="Blueee"><h1>Blueee</h1>' + el('p', 'home.tag')
     + card(el('h2', 'home.h'), '<ul>' + ''.join(el('li', f'home.l{i}') for i in range(1, 5)) + '</ul>'))

page('privacy.html', 'priv.title',
     el('h1', 'priv.title') + card(
         el('h2', 'priv.h1'), el('p', 'priv.p1'), el('h2', 'priv.h2'),
         '<ul>' + ''.join(el('li', k) for k in ('priv.loc', 'priv.ble', 'priv.cam', 'priv.mot')) + '</ul>',
         *[el(t, f'priv.{k}') for k in ('h3', 'p3', 'h4', 'p4', 'h5', 'p5') for t in ['h2' if k[0] == 'h' else 'p']]))

page('terms.html', 'terms.title',
     el('h1', 'terms.title') + card(*[el('h2', f'terms.h{i}') + el('p', f'terms.p{i}') for i in range(1, 6)]))

page('support.html', 'sup.title',
     el('h1', 'sup.title') + card(
         el('h2', 'sup.h1'), el('p', 'sup.p1'), el('h2', 'sup.h2'),
         *[f'<p><b data-i18n="sup.q{i}">{EN[f"sup.q{i}"]}</b><br>{el("span", f"sup.a{i}")}</p>' for i in (1, 2, 3)]))

print(len(L), 'languages:', ', '.join(L))
