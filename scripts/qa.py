#!/usr/bin/env python3
"""Automated page QA. Usage: python3 qa.py <work>/index.html [--axe path/to/axe.min.js]
Checks at 320 (WCAG reflow), 390, 768, 1024, 1440px: horizontal overflow, small tap targets, small input text.
Runs axe-core (WCAG 2.2 A/AA) from the kit's scripts/vendor/axe.min.js by default. Reports loaded fonts,
phone first-screen contents, H1 count, CTA labels, em dashes and file size. Saves screenshots at 390 and 1440px."""
import json, pathlib, argparse
from playwright.sync_api import sync_playwright
ap=argparse.ArgumentParser(); ap.add_argument("file"); ap.add_argument("--axe",default=str(pathlib.Path(__file__).resolve().parent/"vendor"/"axe.min.js"))
a=ap.parse_args(); f=pathlib.Path(a.file).resolve(); out={}
PROBE="""() => {
 const vis=e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);return r.width>0&&r.height>0&&s.visibility!=='hidden'&&s.display!=='none'};
 const small=[...document.querySelectorAll('a,button,input,select,textarea,[role=button]')].filter(vis)
   .map(e=>{const r=e.getBoundingClientRect();return {t:(e.innerText||e.getAttribute('aria-label')||e.name||e.tagName).trim().slice(0,40),w:Math.round(r.width),h:Math.round(r.height)}})
   .filter(x=>x.w<44||x.h<44);
 const tinyInputs=[...document.querySelectorAll('input,select,textarea')].filter(vis)
   .filter(e=>parseFloat(getComputedStyle(e).fontSize)<16).map(e=>e.name||e.id||e.type);
 return {overflow:document.documentElement.scrollWidth>window.innerWidth, small_targets:small.slice(0,15), tiny_inputs:tinyInputs};
}"""
with sync_playwright() as p:
    b=p.chromium.launch()
    for w in (320,390,768,1024,1440):
        pg=b.new_page(viewport={"width":w,"height":900}); pg.goto(f.as_uri()); pg.wait_for_timeout(600)
        out[f"w{w}"]=pg.evaluate(PROBE)
        if w in (390,1440): pg.screenshot(path=str(f.with_name(f"{f.stem}-{w}.png")),full_page=True)
    pg=b.new_page(viewport={"width":390,"height":844}); pg.goto(f.as_uri()); pg.wait_for_timeout(600)
    pg.evaluate("document.fonts.ready")
    pg.screenshot(path=str(f.with_name(f"{f.stem}-fold.png")))
    out["fold"]=pg.evaluate("""() => { const inView=e=>{const r=e.getBoundingClientRect();return r.top<844&&r.bottom>0&&r.width>0};
      const h1=[...document.querySelectorAll('h1')]; const btns=[...document.querySelectorAll('a,button')].filter(inView).map(e=>e.innerText.trim()).filter(Boolean);
      return {h1_count:h1.length, h1_text:h1.map(e=>e.innerText.trim()), h1_in_first_screen:h1.some(inView), actions_in_first_screen:btns.slice(0,8)} }""")
    focus=[]
    for _ in range(12):
        pg.keyboard.press("Tab")
        focus.append(pg.evaluate("""() => { const e=document.activeElement; if(!e||e===document.body) return null;
          const s=getComputedStyle(e); const ring=(s.outlineStyle!=='none'&&parseFloat(s.outlineWidth)>0)||s.boxShadow!=='none';
          return {el:(e.innerText||e.getAttribute('aria-label')||e.name||e.tagName).trim().slice(0,30), visible_focus:ring} }"""))
    out["keyboard_tab_order"]=[x for x in focus if x]
    out["fonts_loaded"]=pg.evaluate("[...new Set([...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family))]")
    out["cta_labels"]=pg.evaluate("[...new Set([...document.querySelectorAll('a,button')].map(e=>e.innerText.trim()).filter(t=>t&&t.length<40))]")
    out["em_dashes"]=pg.evaluate("document.body.innerText.split('\\u2014').length-1")
    out["data_blocks"]=pg.evaluate("[...document.querySelectorAll('[data-block]')].map(e=>e.dataset.block)")
    if a.axe and pathlib.Path(a.axe).exists():
        pg.add_script_tag(path=a.axe)
        r=pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']}});return r.violations.map(v=>({id:v.id,impact:v.impact,help:v.help,count:v.nodes.length,target:v.nodes[0]&&v.nodes[0].target.join(' ')}))}")
        out["axe_violations"]=r
    else: out["axe_violations"]="NOT RUN (axe-core missing)"
    b.close()
out["file_size_kb"]=round(f.stat().st_size/1024,1)
print(json.dumps(out,indent=1))
