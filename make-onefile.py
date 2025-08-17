#!/usr/bin/env python3
import re, pathlib, sys

repo   = pathlib.Path.home() / "strabismusai"
p_text = repo / "textbook.single.html"
p_tools= repo / "tools.single.html"
out    = repo / "StrabismusAI-OneFile.html"

def load(path):
    if not path.exists():
        sys.exit(f"ERR: missing {path.name}")
    s = path.read_text(encoding="utf-8", errors="ignore")
    # remove DOCTYPE (not allowed inside <template>)
    s = re.sub(r'<!doctype[^>]*>\s*', '', s, flags=re.I)
    return s

textbook = load(p_text)
tools    = load(p_tools)

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>StrabismusAI — One-File Bundle</title>
<style>
  :root{--bar-h:56px}
  *{box-sizing:border-box}
  html,body{height:100%}
  body{margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,Inter,Helvetica,Arial,sans-serif;background:#f3f4f6}
  .bar{position:sticky;top:0;z-index:10;height:var(--bar-h);background:#111827;color:#fff;display:flex;align-items:center;gap:.5rem;padding:0 .75rem}
  .tab{border:0;background:#1f2937;color:#e5e7eb;padding:.45rem .8rem;border-radius:10px;font-weight:700;cursor:pointer}
  .tab[aria-selected="true"]{background:#3b82f6;color:#fff}
  .wrap{height:calc(100vh - var(--bar-h))}
  iframe{display:none;width:100%;height:100%;border:0;background:#fff}
  iframe.active{display:block}
</style>
</head>
<body>
  <nav class="bar" role="tablist" aria-label="StrabismusAI Views">
    <button class="tab" role="tab" aria-selected="true"  aria-controls="view-textbook" id="tab-textbook">Textbook</button>
    <button class="tab" role="tab" aria-selected="false" aria-controls="view-tools"    id="tab-tools">Clinical Tools</button>
    <span style="margin-left:auto;opacity:.8;font-size:.9rem">One file · both pages embedded</span>
  </nav>

  <div class="wrap">
    <iframe id="view-textbook" title="Textbook" class="active"></iframe>
    <iframe id="view-tools"    title="Clinical Tools"></iframe>
  </div>

  <!-- The full HTML of each page is stored inside inert templates -->
  <template id="tpl-textbook">
@@@TEXTBOOK@@@
  </template>
  <template id="tpl-tools">
@@@TOOLS@@@
  </template>

<script>
  const tabs=[...document.querySelectorAll('.tab')];
  const frames={textbook:document.getElementById('view-textbook'),
                tools:document.getElementById('view-tools')};
  const tpl={textbook:document.getElementById('tpl-textbook'),
             tools:document.getElementById('tpl-tools')};

  function loadOnce(){
    frames.textbook.srcdoc = tpl.textbook.innerHTML;
    frames.tools.srcdoc    = tpl.tools.innerHTML;
  }
  function select(which){
    for(const t of tabs) t.setAttribute('aria-selected', String(t.id==='tab-'+which));
    for(const id of Object.keys(frames)) frames[id].classList.toggle('active', id===which);
    history.replaceState(null,'','#'+which);
  }
  tabs.forEach(btn=>btn.addEventListener('click',()=>select(btn.id.split('-')[1])));
  loadOnce();
  const hash=location.hash.replace('#','');
  if(hash==='tools'||hash==='textbook') select(hash);
</script>
</body>
</html>
"""

html = TEMPLATE.replace('@@@TEXTBOOK@@@', textbook).replace('@@@TOOLS@@@', tools)
out.write_text(html, encoding='utf-8')
print(f"OK: wrote {out} ({out.stat().st_size} bytes)")
