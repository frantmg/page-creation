#!/usr/bin/env python3
"""Automated page QA. Usage: python3 qa.py <work>/index.html [--axe path/to/axe.min.js]
Checks at 320 (WCAG reflow), 390, 768, 1024, 1440px: horizontal overflow, small tap targets, small input text.
Runs axe-core (WCAG 2.2 A/AA) from the kit's scripts/vendor/axe.min.js by default. Reports loaded fonts,
phone first-screen contents, H1 count, CTA labels, em dashes and file size. Logo check at 390 and 1440px: the header
and footer each need a visible logo (img, svg or .wordmark) at least 24px tall with 3:1 contrast against its background.
Saves screenshots at 390 and 1440px."""
import json, base64, pathlib, argparse
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
FIND_LOGO="""(region) => {
 const root = region==='header' ? (document.querySelector('header, [data-block^="G1"]')) : (document.querySelector('footer, [data-block^="G3"]'));
 if(!root) return {found:false, reason:'no '+region+' element'};
 const vis=e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);return r.width>0&&r.height>0&&s.visibility!=='hidden'&&s.display!=='none'&&parseFloat(s.opacity)>0};
 const pick=[...root.querySelectorAll('img[alt*="logo" i], svg[role="img"], .wordmark, [class*="logo" i] img, [class*="logo" i] svg, [class*="logo" i], a[href] img, img')]
   .find(e=>!e.closest('button')&&!(e.tagName.toLowerCase()==='svg'&&e.getAttribute('aria-hidden')==='true'));
 if(!pick) return {found:false, reason:'no img, svg or .wordmark logo in the '+region};
 pick.scrollIntoView({block:'center'});
 const r=pick.getBoundingClientRect();
 return {found:true, visible:vis(pick), type:pick.classList.contains('wordmark')?'wordmark':pick.tagName.toLowerCase(),
   label:(pick.getAttribute('alt')||pick.getAttribute('aria-label')||pick.innerText||'').trim().slice(0,40),
   x:r.x, y:r.y, w:r.width, h:r.height};
}"""
# Background = most common color on a 6px ring around the logo; logo pixels = inside pixels that differ from it.
# Contrast = 80th percentile WCAG ratio of logo pixels vs background (ignores anti-aliased edges).
MEASURE="""async (b64) => {
 const img=new Image(); img.src='data:image/png;base64,'+b64; await img.decode();
 const c=document.createElement('canvas'); c.width=img.width; c.height=img.height; const x=c.getContext('2d'); x.drawImage(img,0,0);
 const d=x.getImageData(0,0,c.width,c.height).data, W=c.width, H=c.height, P=6;
 const L=(r,g,b)=>{const f=v=>{v/=255;return v<=0.04045?v/12.92:((v+0.055)/1.055)**2.4};return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b)};
 const ring=new Map(); const at=(i,j)=>{const k=(j*W+i)*4;return [d[k],d[k+1],d[k+2]]};
 for(let j=0;j<H;j++)for(let i=0;i<W;i++){ if(i>=P&&i<W-P&&j>=P&&j<H-P) continue; const p=at(i,j); const q=p.map(v=>v>>3).join(); if(!ring.has(q)) ring.set(q,[0,p]); ring.get(q)[0]++; }
 let bg=[255,255,255],n=0; for(const [k,[cnt,p]] of ring) if(cnt>n){n=cnt;bg=p}
 const Lb=L(...bg), cr=[]; let inner=0;
 for(let j=P;j<H-P;j++)for(let i=P;i<W-P;i++){ inner++; const p=at(i,j); if(Math.abs(p[0]-bg[0])+Math.abs(p[1]-bg[1])+Math.abs(p[2]-bg[2])>30){ const l=L(...p); cr.push((Math.max(l,Lb)+0.05)/(Math.min(l,Lb)+0.05)); } }
 cr.sort((a,b)=>a-b);
 return {bg:'#'+bg.map(v=>v.toString(16).padStart(2,'0')).join('').toUpperCase(), logo_pixel_share:+(cr.length/Math.max(inner,1)).toFixed(3),
   contrast: cr.length ? +cr[Math.floor(cr.length*0.8)].toFixed(2) : 1};
}"""
def check_logo(pg, region):
    info=pg.evaluate(FIND_LOGO, region)
    if not info.get("found"): return {"pass":False, **info}
    vw=pg.viewport_size
    x0=max(0,info["x"]-6); y0=max(0,info["y"]-6); x1=min(vw["width"],info["x"]+info["w"]+6); y1=min(vw["height"],info["y"]+info["h"]+6)
    m={"bg":None,"logo_pixel_share":0,"contrast":1}
    if info["visible"] and x1-x0>12 and y1-y0>12:
        png=pg.screenshot(clip={"x":x0,"y":y0,"width":x1-x0,"height":y1-y0})
        m=pg.evaluate(MEASURE, base64.b64encode(png).decode())
    shown=info["visible"] and m["logo_pixel_share"]>=0.02
    ok=shown and info["h"]>=24 and m["contrast"]>=3
    problems=[t for t,bad in (("not visible",not shown),("under 24px tall",info["h"]<24),("contrast under 3:1",m["contrast"]<3)) if bad]
    return {"pass":ok, "type":info["type"], "label":info["label"], "height":round(info["h"]), **m, "problems":problems}

with sync_playwright() as p:
    b=p.chromium.launch()
    for w in (320,390,768,1024,1440):
        pg=b.new_page(viewport={"width":w,"height":900}); pg.goto(f.as_uri()); pg.wait_for_timeout(600)
        out[f"w{w}"]=pg.evaluate(PROBE)
        if w in (390,1440):
            pg.screenshot(path=str(f.with_name(f"{f.stem}-{w}.png")),full_page=True)
            out.setdefault("logo",{})[f"w{w}"]={r:check_logo(pg,r) for r in ("header","footer")}
            pg.evaluate("window.scrollTo(0,0)")
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
        pg.evaluate("document.activeElement && document.activeElement.blur(); window.scrollTo(0,0)")   # focused skip link would cover the header
        pg.add_script_tag(path=a.axe)
        r=pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']}});return r.violations.map(v=>({id:v.id,impact:v.impact,help:v.help,count:v.nodes.length,target:v.nodes[0]&&v.nodes[0].target.join(' ')}))}")
        out["axe_violations"]=r
    else: out["axe_violations"]="NOT RUN (axe-core missing)"
    b.close()
out["file_size_kb"]=round(f.stat().st_size/1024,1)
print(json.dumps(out,indent=1))
