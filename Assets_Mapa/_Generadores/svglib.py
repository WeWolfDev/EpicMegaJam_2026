"""Utilidades comunes: paleta, envoltura SVG y render con Chromium."""
import os, asyncio, json
C = dict(tinta='#2b2b29', papel='#f4f3ee', blanco='#ffffff', borde='#6c6c6a',
         og='#ac7d49', og_osc='#74502c', og_prof='#48321c', og_luz='#c1935c',
         com='#f0f1f5', com_pared='#e8ecef', com_linea='#c3c7d3',
         marca='#c55b7f', marca_osc='#8f3d5b', marca_tinte='#f0ccd8',
         cielo='#e0eaf4', agua='#7ca6ce', agua_osc='#6a94bf', arena='#ebc5a0', arena_clara='#f2dec3', muelle='#c6b89d',
         personaje='#394962', moneda='#f6d880', luz='#fcf3ca', sol='#e9a640', precaucion='#e8b24a',
         escenario='#3a3343', noche='#292533', gris='#82878d')
FONTS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Fuentes'))
FACES = [('Space Grotesk', 'SpaceGrotesk', (400, 500, 700)), ('Barlow Condensed', 'BarlowCondensed', (400, 500, 700)), ('Silkscreen', 'Silkscreen', (400, 700))]
WN = {400: 'Regular', 500: 'Medium', 700: 'Bold'}
def font_css():
    return ''.join(f"@font-face{{font-family:'{fam}';src:url('file://{FONTS}/{stem}-{WN[w]}.ttf');font-weight:{w}}}" for fam, stem, ws in FACES for w in ws)
SG = "font-family:'Space Grotesk',sans-serif"
BC = "font-family:'Barlow Condensed',sans-serif"
SK = "font-family:'Silkscreen',monospace"
def esc(t): return t.replace('&', '&amp;').replace('<', '&lt;')
def svg(w, h, body, defs=''):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{("<defs>"+defs+"</defs>") if defs else ""}{body}</svg>\n'
def text(x, y, t, size, fill, fam=SG, weight=700, anchor='start', extra=''):
    return f'<text x="{x}" y="{y}" style="{fam};font-weight:{weight};font-size:{size}px" fill="{fill}" text-anchor="{anchor}" {extra}>{esc(t)}</text>'
def rect(x, y, w, h, fill='none', rx=0, stroke=None, sw=0, extra=''):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{s} {extra}/>'
def line(x1, y1, x2, y2, stroke, sw, extra=''):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
def circle(cx, cy, r, fill='none', stroke=None, sw=0, extra=''):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"{s} {extra}/>'
def path(d, fill='none', stroke=None, sw=0, extra=''):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    return f'<path d="{d}" fill="{fill}"{s} {extra}/>'
def poly(pts, fill='none', stroke=None, sw=0, extra=''):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    return f'<polygon points="{" ".join(f"{x},{y}" for x, y in pts)}" fill="{fill}"{s} {extra}/>'

async def _render(items):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for it in items:
            w, h, s = it['w'], it['h'], it.get('scale', 1)
            pg = await b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=s)
            html = f"<!doctype html><html><head><style>{font_css()}html,body{{margin:0;background:{it.get('bg','transparent')}}}svg{{display:block}}</style></head><body>{it['svg']}</body></html>"
            tmp = it['png'] + '.html'
            open(tmp, 'w').write(html)
            await pg.goto('file://' + os.path.abspath(tmp))
            await pg.evaluate('document.fonts.ready')
            await pg.screenshot(path=it['png'], omit_background=it.get('bg') is None)
            await pg.close(); os.remove(tmp)
        await b.close()
def render(items):
    for it in items:
        os.makedirs(os.path.dirname(it['png']), exist_ok=True)
        if it.get('svgpath'):
            os.makedirs(os.path.dirname(it['svgpath']), exist_ok=True); open(it['svgpath'], 'w').write(it['svg'])
    asyncio.run(_render(items))
