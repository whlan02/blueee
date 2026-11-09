"""生成多语言官网：python build.py
英文直接写进 HTML（没有 JS 也能读），所有语言放在 i18n.js，由右上角的语言下拉切换。默认英文。"""
import json
import pathlib

from translations import L

ISSUES = '<a href="https://github.com/whlan02/blueee/issues">github.com/whlan02/blueee/issues</a>'
EN = L['en']
import hashlib
VERSION = hashlib.md5(json.dumps(L, sort_keys=True).encode()).hexdigest()[:8]  # 文案变了地址就变，浏览器不会用旧缓存
RTL = ['ar', 'ur', 'fa', 'he']


def fill(s):
    return s.replace('{issues}', ISSUES).replace('{privacy}', f'<a href="privacy.html">{EN["privacyLink"]}</a>')


def el(tag, key):
    return f'<{tag} data-i18n="{key}">{fill(EN[key])}</{tag}>'


CSS = '''*{box-sizing:border-box}body{margin:0;font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC",sans-serif;color:#114163;background:linear-gradient(160deg,#e3e3fe,#c7dcf8) fixed;min-height:100vh}
main{max-width:720px;margin:0 auto;padding:40px 20px 80px}header{display:flex;gap:18px;flex-wrap:wrap;align-items:center;margin-bottom:32px;font-size:15px}
header .sp{flex:1}select{font:inherit;color:#114163;background:rgba(255,255,255,.7);border:1px solid rgba(17,65,99,.2);border-radius:999px;padding:6px 12px}
a{color:#114163}h1{font-size:34px;margin:0 0 4px}h2{font-size:20px;margin-top:28px}.card{background:rgba(255,255,255,.7);border-radius:22px;padding:8px 24px 24px;margin-top:20px}
img.icon{width:96px;height:96px;border-radius:22px;box-shadow:0 8px 24px rgba(17,65,99,.25)}footer{margin-top:40px;font-size:13px;opacity:.65}[dir=rtl] ul{padding-right:1.4em;padding-left:0}'''

OPTIONS = ''.join(f'<option value="{code}">{data["name"]}</option>' for code, data in L.items())
NAV = ''.join(f'<a data-i18n="nav.{k}" href="{href}">{EN["nav." + k]}</a>' for k, href in
              [('home', 'index.html'), ('privacy', 'privacy.html'), ('terms', 'terms.html'), ('support', 'support.html')])
HEADER = f'<header>{NAV}<span class="sp"></span><select id="lang" aria-label="Language">{OPTIONS}</select></header>'


def page(filename, title_key, body):
    html = (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{EN[title_key]} – Blueee</title><link rel="icon" href="icon.png"><style>{CSS}</style></head>'
            f'<body><main>{HEADER}{body}<footer data-i18n="foot">{EN["foot"]}</footer></main>'
            f'<script src="i18n.js?v={VERSION}"></script></body></html>')
    pathlib.Path(filename).write_text(html, encoding='utf-8')


def card(*parts):
    return '<div class="card">' + ''.join(parts) + '</div>'


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

translations = {code: {k: fill(v) for k, v in data.items()} for code, data in L.items()}
script = 'var T=' + json.dumps(translations, ensure_ascii=False) + ';\nvar RTL=' + json.dumps(RTL) + ''';
(function () {
  var KEY = 'blueee-lang', select = document.getElementById('lang');
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
    select.value = code;
  }
  select.addEventListener('change', function () {
    try { localStorage.setItem(KEY, select.value); } catch (e) {}
    apply(select.value);
  });
  apply(lang);
})();
'''
pathlib.Path('i18n.js').write_text(script, encoding='utf-8')
print(len(L), 'languages:', ', '.join(L))
