"""Hojas guía para 3D: vistas ortográficas en cm (1 uu de Unreal = 1 cm), presupuesto y texturas por plano."""
import sys, math, textwrap
from svglib import *
OUT = sys.argv[1]
W, H = 2400, 1600
items = []
SW = 3
def T(x, y, t, size=22, fill=C['tinta'], weight=500, anchor='start', fam=SG): return text(x, y, t, size, fill, fam, weight, anchor)

class View:
    """Vista ortográfica con autoajuste: se dibuja en cm y la escala se calcula para que todo quepa."""
    def __init__(s, x, y, w, h, scmax, title, *_, grid=50):
        s.x, s.y, s.w, s.h, s.scmax, s.title, s.grid = x, y, w, h, scmax, title, grid
        s.ops = []; s.b = ''; s.sc = 1; s.x0 = s.y0 = 0
    def _op(s, fn, x0, y0, x1, y1, pl=4, pr=4, pt=4, pb=4):
        s.ops.append((fn, min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1), pl, pr, pt, pb)); return s
    def X(s, v): return round(s.x0 + v * s.sc, 1)
    def Y(s, v): return round(s.y0 - v * s.sc, 1)
    def raw(s, fn, x0, y0, x1, y1): return s._op(fn, x0, y0, x1, y1)
    def R(s, x, y, w, h, fill='none', stroke=C['tinta'], sw=SW, rx=0, extra=''):
        return s._op(lambda: rect(s.X(x), s.Y(y + h), round(w * s.sc, 1), round(h * s.sc, 1), fill, round(rx * s.sc, 1), stroke, sw, extra), x, y, x + w, y + h)
    def P(s, pts, fill='none', stroke=C['tinta'], sw=SW, extra='stroke-linejoin="round"'):
        return s._op(lambda: poly([(s.X(a), s.Y(b)) for a, b in pts], fill, stroke, sw, extra), min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts))
    def L(s, x1, y1, x2, y2, stroke=C['tinta'], sw=SW, extra='stroke-linecap="round"'):
        return s._op(lambda: line(s.X(x1), s.Y(y1), s.X(x2), s.Y(y2), stroke, sw, extra), x1, y1, x2, y2)
    def Ci(s, x, y, r, fill='none', stroke=C['tinta'], sw=SW, extra=''):
        return s._op(lambda: circle(s.X(x), s.Y(y), round(r * s.sc, 1), fill, stroke, sw, extra), x - r, y - r, x + r, y + r)
    def ground(s, label='Z = 0', z=0):
        return s._op(lambda: line(s.x, s.Y(z), s.x + s.w, s.Y(z), C['tinta'], 2, 'stroke-dasharray="14 8"') + T(s.x + s.w - 14, s.Y(z) - 8, label, 18, C['borde'], 500, 'end'), 0, z, 0, z, 0, 0, 0, 34)
    def water(s, z=0):
        s.ops.insert(0, (lambda: rect(s.x + 1, s.Y(z), s.w - 2, max(0, s.y + s.h - s.Y(z) - 1), C['agua'], 0, None, 0, 'opacity=".35"') + T(s.x + 14, s.Y(z) - 8, 'nivel del agua', 18, C['personaje'], 500), 0, z, 0, z, 0, 0, 0, 50)); return s
    def dh(s, x1, x2, y, label=None, off=0):
        t = label or f'{abs(x2 - x1):g}'; c = C['marca_osc']
        def fn():
            Y = s.Y(y) + off; a, b = s.X(x1), s.X(x2)
            return (line(a, Y, b, Y, c, 2) + line(a, Y - 8, a, Y + 8, c, 2) + line(b, Y - 8, b, Y + 8, c, 2)
                    + rect((a + b) / 2 - len(t) * 6.6 - 6, Y - 14, len(t) * 13.2 + 12, 28, C['blanco'], 6) + T((a + b) / 2, Y + 7, t, 20, c, 700, 'middle'))
        e = len(t) * 7
        return s._op(fn, x1, y, x2, y, e, e, 18 + max(0, -off), 18 + max(0, off))
    def dv(s, x, y1, y2, label=None, off=0):
        t = label or f'{abs(y2 - y1):g}'; c = C['marca_osc']
        def fn():
            X = s.X(x) + off; a, b = s.Y(y1), s.Y(y2)
            return (line(X, a, X, b, c, 2) + line(X - 8, a, X + 8, a, c, 2) + line(X - 8, b, X + 8, b, c, 2)
                    + rect(X - len(t) * 6.6 - 6, (a + b) / 2 - 14, len(t) * 13.2 + 12, 28, C['blanco'], 6) + T(X, (a + b) / 2 + 7, t, 20, c, 700, 'middle'))
        e = len(t) * 7 + 10
        return s._op(fn, x, y1, x, y2, e + max(0, -off), e + max(0, off), 6, 6)
    def note(s, x, y, t, anchor='start', dy=0):
        wpx = len(t) * 10.4
        pl, pr = (0, wpx) if anchor == 'start' else ((wpx / 2, wpx / 2) if anchor == 'middle' else (wpx, 0))
        return s._op(lambda: T(s.X(x), s.Y(y) + dy, t, 19, C['personaje'], 500, anchor), x, y, x, y, pl + 2, pr + 2, 20 + max(0, -dy), 8 + max(0, dy))
    def fig(s, x, hgt=180, z=0):
        w = hgt * .26
        def fn():
            return (rect(s.X(x - w / 2), s.Y(z + hgt * .8), w * s.sc, hgt * .8 * s.sc, C['personaje'], w * s.sc / 2, None, 0, 'opacity=".28"')
                    + circle(s.X(x), s.Y(z + hgt * .88), hgt * .12 * s.sc, C['personaje'], None, 0, 'opacity=".28"') + T(s.X(x), s.Y(z + hgt) - 8, f'{hgt} cm', 17, C['personaje'], 700, 'middle'))
        return s._op(fn, x - w / 2, z, x + w / 2, z + hgt, 22, 22, 30, 2)
    def build(s):
        x, y, w, h = s.x, s.y, s.w, s.h
        aw, ah = w - 48, h - 64 - 28
        def ext(sc):
            mnx = min(o[1] * sc - o[5] for o in s.ops); mxx = max(o[3] * sc + o[6] for o in s.ops)
            mny = min(-o[4] * sc - o[7] for o in s.ops); mxy = max(-o[2] * sc + o[8] for o in s.ops)
            return mnx, mxx, mny, mxy
        lo, hi = .02, s.scmax
        for _ in range(40):
            mid = (lo + hi) / 2; a, b_, c, d = ext(mid)
            if b_ - a <= aw and d - c <= ah: lo = mid
            else: hi = mid
        a, b_, c, d = ext(hi if (lambda e: e[1] - e[0] <= aw and e[3] - e[2] <= ah)(ext(hi)) else lo)
        s.sc = hi if (lambda e: e[1] - e[0] <= aw and e[3] - e[2] <= ah)(ext(hi)) else lo
        a, b_, c, d = ext(s.sc)
        s.x0 = x + 24 + (aw - (b_ - a)) / 2 - a; s.y0 = y + 64 + (ah - (d - c)) / 2 - c
        sc, grid = s.sc, s.grid
        if sc * grid < 22: grid = 100
        b = rect(x, y, w, h, C['blanco'], 10, C['com_linea'], 2)
        b += f'<clipPath id="c{x}_{y}"><rect x="{x+1}" y="{y+1}" width="{w-2}" height="{h-2}" rx="9"/></clipPath><g clip-path="url(#c{x}_{y})">'
        n0 = -int((s.x0 - x) / sc / grid) - 1; n1 = int((x + w - s.x0) / sc / grid) + 1
        for i in range(n0, n1 + 1):
            X = s.x0 + i * grid * sc; M = (i * grid) % 100 == 0; b += line(round(X, 1), y, round(X, 1), y + h, C['com_linea'] if M else '#e6e8ee', 1.5 if M else 1)
        m0 = -int((y + h - s.y0) / sc / grid) - 1; m1 = int((s.y0 - y) / sc / grid) + 1
        for i in range(m0, m1 + 1):
            Y = s.y0 - i * grid * sc; M = (i * grid) % 100 == 0; b += line(x, round(Y, 1), x + w, round(Y, 1), C['com_linea'] if M else '#e6e8ee', 1.5 if M else 1)
        for o in s.ops: b += o[0]()
        b += '</g>'
        b += rect(x + 14, y + 14, 34 + len(s.title) * 14.5, 40, C['tinta'], 20) + T(x + 32, y + 42, s.title, 22, C['papel'], 700)
        b += T(x + w - 14, y + h - 12, f'escala 1 cm = {sc:.2f} px', 16, C['borde'], 500, 'end')
        s.b = b; return b

def sheet(num, title, sub, views, info):
    b = rect(0, 0, W, H, C['papel'])
    b += T(60, 74, f'HOJA GUÍA 3D · {num:02d}', 24, C['og_osc'], 700).replace('<text', '<text letter-spacing="3"')
    b += T(60, 142, title, 68, C['tinta'], 700) + T(60, 186, sub, 24, C['borde'], 500)
    b += T(W - 60, 74, 'The Last Patch: Director’s Cut', 24, C['marca'], 700, 'end') + T(W - 60, 110, 'cuadrícula 50 cm · línea gruesa 100 cm · 1 uu = 1 cm', 20, C['borde'], 500, 'end')
    for v in views: b += v.build()
    x = 1740; y = 230
    b += rect(x - 20, 210, 620, 1330, C['blanco'], 10, C['com_linea'], 2)
    for head, lines in info:
        col = {'OG · low poly': C['og_osc'], 'UE · pulido': C['marca_osc']}.get(head, C['tinta'])
        y += 34; b += rect(x, y - 26, 26 + len(head) * 13, 36, col, 18) + T(x + 14, y, head, 20, C['papel'], 700); y += 16
        for ln in lines:
            for i, wl in enumerate(textwrap.wrap(ln, 50)):
                y += 28; b += T(x + (0 if i == 0 else 18), y, ('· ' if i == 0 else '') + wl, 20, C['tinta'], 500)
        y += 14
    items.append(dict(name=f'HG_{num:02d}_{title.replace(" ", "").replace("+", "Y").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace(",","")}', w=W, h=H, bg=C['papel'], svg=svg(W, H, b)))

DX, DY, DW, DH = 60, 210, 1640, 1330
def std(sc_note=''):
    return []

# ---------- 00 reglas
def h00():
    v = View(DX, DY, 1000, 640, 1.6, 'ESCALA', 80, 80)
    v.ground().fig(60).R(150, 0, 100, 100, C['og'], C['og_prof']).L(150, 0, 250, 100, C['og_osc'], 6).L(250, 0, 150, 100, C['og_osc'], 6)
    v.R(300, 0, 200, 20, C['og']).dh(150, 250, -22).dv(270, 0, 100, off=6).dh(300, 500, -22, '200 = 1 tile').note(300, 34, 'tablero: textura repite cada 200')
    v2 = View(DX + 1020, DY, 620, 640, 1, 'TEXEL', 60, 60)
    for i in range(8):
        for j in range(8):
            v2.R(i * 25, 200 + j * 25, 25, 25, C['og'] if (i + j) % 2 == 0 else C['og_osc'], None, 0)
    v2.R(0, 200, 200, 200, 'none', C['tinta']).note(0, 410, 'OG · 64 px', dy=-30).note(0, 410, 'Nearest, 1 cuadro = 8 px', dy=-6)
    v2.R(260, 200, 200, 200, C['marca'], C['marca_osc']).note(260, 410, 'UE · 1024 px', dy=-30).note(260, 410, 'BC + N + ORM', dy=-6)
    v2.dh(0, 200, 170, '200 cm').dh(260, 460, 170, '200 cm')
    v2.note(0, 110, 'Misma UV para los dos planos: al cambiar').note(0, 82, 'de forma solo se cambia el material.').note(0, 40, 'UV en espacio mundo: 1 UV = 200 cm.')
    v3 = View(DX, DY + 660, 1640, 670, 1.1, 'MISMO PROP, DOS PLANOS', 120, 110)
    v3.ground()
    # OG faro facetado vs UE
    v3.P([(60, 0), (240, 0), (210, 380), (90, 380)], C['arena_clara']).L(150, 0, 150, 380, C['borde'], 2).P([(90, 380), (210, 380), (210, 450), (90, 450)], C['luz']).P([(70, 450), (230, 450), (150, 520)], C['og_osc'])
    v3.note(60, -40, 'OG: 8 lados, aristas duras, sin biseles', dy=10)
    v3.P([(560, 0), (740, 0), (712, 380), (588, 380)], C['arena_clara'])
    v3.R(580, 380, 140, 16, C['com'], rx=6).R(596, 396, 108, 70, C['luz'], rx=8)
    v3.raw(lambda: path(f'M{v3.X(580)} {v3.Y(466)} Q{v3.X(650)} {v3.Y(560)} {v3.X(720)} {v3.Y(466)} Z', C['og_osc'], C['tinta'], SW), 580, 466, 720, 520)
    v3.note(560, -40, 'UE: 24+ lados, biseles de 1–2 cm, normales suaves', dy=10)
    v3.raw(lambda: path(f'M{v3.X(290)} {v3.Y(250)} H{v3.X(500)} M{v3.X(470)} {v3.Y(280)} L{v3.X(500)} {v3.Y(250)} L{v3.X(470)} {v3.Y(220)}', 'none', C['tinta'], 4, 'stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="14 10"'), 290, 220, 500, 280)
    v3.note(395, 290, 'misma silueta y pivote', 'middle')
    v3.note(900, 470, 'Reglas comunes').note(900, 430, '1. Modela primero el OG; el UE sale de biselarlo.').note(900, 395, '2. Silueta, altura y colisión idénticas en los dos planos.')
    v3.note(900, 360, '3. Pivote en el centro de la base (Z = 0), +X al frente.').note(900, 325, '4. Medidas en múltiplos de 10 cm; módulos de 100 y 200.')
    v3.note(900, 290, '5. OG: color plano, texturas 64 px, sin normal map.').note(900, 255, '6. UE: PBR 1024 px, bordes redondeados.')
    v3.note(900, 220, '7. Nombres: SM_<Prop>_OG y SM_<Prop>_UE.').note(900, 185, '8. Colisión simple (cajas), la misma para ambos.')
    sheet(0, 'Reglas y escala', 'Lo que comparten todos los props del mapa en los dos planos.', [v, v2, v3], [
        ('Unidades', ['Unreal: 1 uu = 1 cm. Exporta FBX en cm, escala 1.', 'Referencia de altura: maniquí UE5 de 180 cm (los rigs del repo usan ese esqueleto). Ajusta si el ratón queda más bajo.']),
        ('OG · low poly', ['Texturas T_OG_*_64.png, 64×64, filtro Nearest, sin mipmaps, sRGB.', 'Densidad: 64 px cada 200 cm (0.32 px/cm).', 'Material sin normal ni ORM: Roughness 1, Specular 0.', 'Sombreado plano (hard edges). 12–600 tris por prop.']),
        ('UE · pulido', ['Texturas T_UE_*_BC / _N / _ORM, 1024×1024.', 'Densidad: 1024 px cada 200 cm (5.12 px/cm).', 'N en formato DirectX. ORM: R = AO, G = Roughness, B = Metallic; desmarca sRGB.', '500–8 000 tris por prop, biseles en todas las aristas visibles.']),
        ('Color', ['Madera OG = lo original. Rosa marca + blanco comercial = lo que impuso la empresa.', 'Trazo punteado = mecánica híbrida (rebote, tracción).']),
        ('Carpetas', ['Mallas a Content/_Game/Props/, texturas y materiales a Content/_Game/Materials/.', 'Prefijos del equipo: SM_, T_, M_, MI_.'])])

def h01():
    v = View(DX, DY, 1000, 760, 1.25, 'FRENTE', 200, 330)
    v.water(0).R(0, 200, 400, 20, C['og'], C['og_prof'])
    for i in range(1, 16): v.L(i * 25, 200, i * 25, 220, C['og_prof'], 1.5)
    v.R(0, 170, 400, 30, C['og_osc'])
    for x in (35, 335): v.R(x, -220, 30, 390, C['og_osc']).R(x - 5, 150, 40, 14, C['og_prof'])
    v.fig(300, 180, 220)
    v.dh(0, 400, 250).dv(-30, 200, 220, '20').dv(-30, 0, 200, '200').dh(35, 65, 120, '30').dv(430, 170, 200, '30', off=10).dh(65, 335, -40, '270 entre pilotes')
    v2 = View(DX + 1020, DY, 620, 760, 1.25, 'LADO', 190, 330)
    v2.water(0).R(0, 200, 200, 20, C['og'], C['og_prof']).R(20, 170, 20, 30, C['og_osc']).R(160, 170, 20, 30, C['og_osc']).R(15, -220, 30, 390, C['og_osc']).R(155, -220, 30, 390, C['og_osc'])
    v2.dh(0, 200, 250).dh(15, 185, -40, '170').dv(230, -220, 170, '390 (hincado)', off=20)
    v3 = View(DX, DY + 780, 1640, 550, 1.25, 'PLANTA', 420, 130)
    v3.R(0, 0, 400, 200, C['og'], C['og_prof'])
    for i in range(1, 16): v3.L(i * 25, 0, i * 25, 200, C['og_prof'], 1.5)
    for x in (35, 335):
        for y in (15, 155): v3.R(x, y, 30, 30, 'none', C['og_prof'], 2, extra='stroke-dasharray="6 5"')
    v3.dh(0, 400, 230).dv(-30, 0, 200).dh(0, 25, -22, '25 por tabla')
    v3.R(440, 0, 200, 200, C['og'], C['og_prof']).note(440, 215, 'medio módulo 200×200', dy=-4).R(680, 0, 400, 200, 'none', C['borde'], 2, extra='stroke-dasharray="10 8"').note(680, 215, 'se encadena cada 400 en X', dy=-4)
    sheet(1, 'Muelle modular', 'Zonas 0, 1 y 5. Tablero + vigas + pilotes; se repite cada 400 cm.', [v, v2, v3], [
        ('Piezas', ['SM_Muelle_Tablero 400×200×20.', 'SM_Muelle_Medio 200×200×20.', 'SM_Muelle_Viga 400×20×30 (dos por módulo).', 'SM_Muelle_Pilote 30×30×390, con collar de 40×14.']),
        ('OG · low poly', ['Tablero: 1 caja (12 tris). Las tablas van en la textura.', 'Pilote: caja de 12 tris, sin collar.', 'T_OG_MaderaMuelle_64 arriba, T_OG_MaderaOscura_64 en vigas y pilotes.']),
        ('UE · pulido', ['Tablas separadas de 25 cm con hueco de 1 cm y bisel; alguna torcida 1–2°. ~1 200 tris.', 'Pilote de 12 lados con collar y punta desgastada. ~300 tris.', 'T_UE_MaderaMuelle y T_UE_MaderaOscura (BC, N, ORM).']),
        ('Notas', ['Cubierta a Z = 220 sobre el agua (Z = 0). El ascensor de la zona 1 sube a una cubierta alta: usa pilotes de 700.', 'Pivote: esquina inferior izquierda del tablero para encadenar con snap de 100.', 'Colisión: una caja por tablero.'])])

def h02():
    v = View(DX, DY, 810, 660, 2.6, 'CAJA OG · FRENTE', 270, 150)
    v.ground().R(0, 0, 100, 100, C['og'], C['og_prof']).L(8, 8, 92, 92, C['og_osc'], 22, '').L(92, 8, 8, 92, C['og_osc'], 22, '').R(0, 0, 100, 100, 'none', C['og_prof']).R(5, 5, 90, 90, 'none', C['og_osc'], 26).R(0, 0, 100, 100, 'none', C['og_prof']).R(10, 10, 80, 80, 'none', C['og_prof'], 2)
    v.dh(0, 100, -20).dv(-18, 0, 100).note(0, 108, 'marco 10').fig(-60, 180)
    v2 = View(DX + 830, DY, 810, 660, 2.6, 'CAJA COMERCIAL · FRENTE', 270, 150)
    v2.ground().R(0, 0, 100, 100, C['com'], C['borde'], rx=12).R(1, 58, 98, 16, C['marca'], None, 0).Ci(50, 30, 8, 'none', C['marca'], 8).R(0, 0, 100, 100, 'none', C['borde'], rx=12)
    v2.dh(0, 100, -20).dv(-18, 0, 100).dv(118, 58, 74, '16').note(0, 108, 'radio 12').note(112, 28, 'aro Ø 16')
    v3 = View(DX, DY + 680, 810, 650, 2.6, 'CAJA OG · PLANTA', 270, 190)
    v3.R(0, 0, 100, 100, C['og'], C['og_prof']).R(5, 5, 90, 90, 'none', C['og_osc'], 26)
    for i in range(1, 5): v3.L(10, i * 20, 90, i * 20, C['og_prof'], 1.5)
    v3.R(0, 0, 100, 100, 'none', C['og_prof']).dh(0, 100, -20).dv(-18, 0, 100).note(0, 118, 'tapa: 5 tablas de 16 + marco de 10')
    v4 = View(DX + 830, DY + 680, 810, 650, 2.6, 'APILADO Y VARIANTES', 90, 150)
    v4.ground().R(0, 0, 100, 100, C['og'], C['og_prof']).R(100, 0, 100, 100, C['og'], C['og_prof']).R(50, 100, 100, 100, C['com'], C['borde'], rx=12).R(51, 158, 98, 16, C['marca'], None, 0)
    v4.R(220, 0, 50, 50, C['og'], C['og_prof']).note(220, 60, '50', dy=-4).note(0, 215, 'se apilan en rejilla de 100', dy=-6)
    sheet(2, 'Cajas', 'Zona 0. La caja OG es la “fuente”; la comercial es el “receptor”.', [v, v2, v3, v4], [
        ('Piezas', ['SM_Caja_OG 100×100×100, marco de 10 y cruz de 10 de ancho.', 'SM_Caja_Comercial 100×100×100, radio 12, banda rosa de 16 a Z = 58.', 'Variante pequeña 50×50×50 de cada una.']),
        ('OG · low poly', ['Caja OG: cubo de 12 tris con T_OG_Senal_CajaOG_Cara en las 6 caras.', 'Comercial: cubo con esquinas a 45° (44 tris) y T_OG_Senal_CajaComercial_Cara.']),
        ('UE · pulido', ['Caja OG: marco y cruz en relieve de 2 cm, tablas con hueco, clavos. ~900 tris.', 'Comercial: bisel redondo de 12 cm en 6 segmentos, banda hundida 0.5 cm. ~1 500 tris.', 'Texturas: T_UE_MaderaMuelle para madera; T_UE_PanelComercial + color marca para la comercial.']),
        ('Notas', ['Pivote en el centro de la base.', 'Si se empujan, masa OG 20 kg, comercial 35 kg.', 'La cara con la cruz es T_Senal_CajaOG_Cara (512 px) en el plano UE.'])])

def h03():
    v = View(DX, DY, 1640, 640, 1.9, 'LADO LARGO', 250, 100)
    v.ground().R(0, 0, 600, 260, C['marca'], C['marca_osc'])
    for i in range(1, 30): v.L(18 + i * 18.8, 14, 18 + i * 18.8, 246, C['marca_osc'], 1.5)
    v.R(0, 110, 600, 40, C['com'], None, 0).R(0, 0, 600, 260, 'none', C['marca_osc'])
    for x in (0, 582):
        for y in (0, 242): v.R(x, y, 18, 18, C['com_linea'], C['tinta'], 2)
    v.dh(0, 600, 290).dv(-30, 0, 260).dv(630, 110, 150, '40', off=10).dh(0, 18, -22, '18').fig(-90, 180).note(190, 122, 'franja para T_Senal_Banda_* o logotipo')
    v2 = View(DX, DY + 660, 800, 670, 1.9, 'PUERTAS', 280, 100)
    v2.ground().R(0, 0, 240, 260, C['marca'], C['marca_osc']).L(120, 8, 120, 252, C['marca_osc'], 3)
    for x in (30, 90, 150, 210): v2.L(x, 10, x, 250, C['com_linea'], 5)
    for x in (0, 222):
        for y in (0, 242): v2.R(x, y, 18, 18, C['com_linea'], C['tinta'], 2)
    v2.R(60, 100, 40, 14, C['com'], C['tinta'], 2).R(140, 100, 40, 14, C['com'], C['tinta'], 2).dh(0, 240, 290).dv(-30, 0, 260).note(30, -34, '4 barras de cierre Ø 4', dy=10)
    v3 = View(DX + 820, DY + 660, 820, 670, 1.1, 'PLANTA Y COLGADO', 90, 110)
    v3.R(0, 0, 600, 240, C['marca'], C['marca_osc'])
    for i in range(1, 30): v3.L(18 + i * 18.8, 6, 18 + i * 18.8, 234, C['marca_osc'], 1)
    v3.dh(0, 600, -30).dv(-34, 0, 240)
    v3.R(-10, 300, 620, 20, C['com'], C['borde']).L(0, 300, 0, 280, C['tinta'], 2).L(600, 300, 600, 280, C['tinta'], 2).L(300, 320, 300, 420, C['tinta'], 3).L(60, 320, 300, 400, C['tinta'], 2).L(540, 320, 300, 400, C['tinta'], 2)
    v3.note(0, 440, 'spreader de la grúa: 620×250×20, cuelga de 4 puntos', dy=-4).note(0, 262, 'las esquinas (18 cm) son los puntos de enganche', dy=-2)
    sheet(3, 'Contenedor', 'Zona 3. Lo mueve la grúa; es plataforma y obstáculo.', [v, v2, v3], [
        ('Piezas', ['SM_Contenedor 600×240×260.', 'Esquineros 18×18×18 en las 8 esquinas.', 'Variantes de color: marca (rosa) y blanco con franja rosa.']),
        ('OG · low poly', ['Caja de 12 tris; la chapa ondulada va solo en textura.', 'T_OG_ContenedorMarca_64 o T_OG_ContenedorBlanco_64, 3 repeticiones a lo largo.', 'Puertas: misma textura, sin barras.']),
        ('UE · pulido', ['Ondulado real en los lados largos: 16 ondas por cada 200 cm, 3 cm de fondo. ~4 000 tris.', 'Marco perimetral de 10 cm, esquineros con agujero, barras y bisagras en puertas.', 'T_UE_ContenedorMarca / T_UE_ContenedorBlanco (BC, N, ORM).']),
        ('Notas', ['El techo es zona pisable: colisión de caja simple.', 'Pivote al centro de la base; socket “Enganche” arriba al centro para la grúa.', 'Medidas redondeadas de un contenedor de 20 pies.'])])

def h04():
    v = View(DX, DY, 1640, 900, .52, 'FRENTE', 760, 90, grid=100)
    v.ground()
    # torre de celosía
    v.R(-60, 0, 120, 1400, 'none', C['borde'])
    for i in range(14):
        y = i * 100; v.L(-60, y, 60, y + 100, C['borde'], 2).L(60, y, -60, y + 100, C['borde'], 2).L(-60, y + 100, 60, y + 100, C['borde'], 2)
    v.R(-110, 0, 220, 30, C['com_linea'], C['tinta'])
    # pluma y contrapluma
    v.R(-500, 1400, 2100, 50, C['com'], C['borde']).R(-500, 1400, 2100, 14, C['marca'], None, 0)
    v.P([(0, 1450), (0, 1680), (-40, 1450)], C['com'], C['borde']).L(0, 1680, 1560, 1450, C['borde'], 2).L(0, 1680, -480, 1450, C['borde'], 2)
    v.R(-500, 1290, 260, 110, C['com_linea'], C['borde']).R(70, 1230, 170, 170, C['com'], C['borde']).R(90, 1300, 90, 70, C['cielo'], C['borde'], 2).R(70, 1230, 170, 24, C['marca'], None, 0)
    # carro, cable, spreader, contenedor
    v.R(1060, 1370, 120, 30, C['tinta'], C['tinta']).L(1120, 1370, 1120, 620, C['tinta'], 2).L(1120, 620, 830, 540, C['tinta'], 2).L(1120, 620, 1410, 540, C['tinta'], 2)
    v.R(810, 520, 620, 20, C['com'], C['borde']).R(820, 260, 600, 260, C['com'], C['borde']).R(820, 370, 600, 40, C['marca'], None, 0)
    v.dv(-560, 0, 1400, '1400').dh(0, 1600, 1740, '1600 pluma').dh(-500, 0, 1740, '500').dh(-60, 60, -50, '120').dv(1640, 1400, 1450, '50', off=20).fig(-300, 180)
    v.note(1200, 900, 'cable: longitud variable').note(1200, 1320, 'carro 120×100×30, corre por la pluma')
    v2 = View(DX, DY + 920, 800, 410, 1.5, 'CABINA', 300, 70)
    v2.ground('base de cabina').R(0, 0, 170, 170, C['com'], C['borde']).R(20, 70, 90, 70, C['cielo'], C['borde'], 2).R(0, 0, 170, 24, C['marca'], None, 0).dh(0, 170, 200).dv(-28, 0, 170).note(190, 100, 'ventana 90×70').note(190, 60, 'cuelga del lado de la pluma')
    v3 = View(DX + 820, DY + 920, 820, 410, 1.3, 'TRAMO DE TORRE', 330, 70)
    v3.R(0, 0, 120, 200, 'none', C['borde'])
    for y in (0, 100): v3.L(0, y, 120, y + 100, C['borde'], 2).L(120, y, 0, y + 100, C['borde'], 2).L(0, y + 100, 120, y + 100, C['borde'], 2)
    for x in (0, 110): v3.R(x, 0, 10, 200, C['com_linea'], C['tinta'], 2)
    v3.dh(0, 120, 230).dv(-28, 0, 100, '100').note(150, 150, 'montantes 10×10').note(150, 110, 'diagonales 6×6').note(150, 70, 'tramo modular: 120×120×100')
    sheet(4, 'Grúa comercial', 'Zona 3. Torre de celosía blanca con detalles rosa; mueve el contenedor.', [v, v2, v3], [
        ('Piezas', ['SM_Grua_Tramo 120×120×100 (se apila 14 veces).', 'SM_Grua_Pluma 2100×100×50 con tirantes.', 'SM_Grua_Cabina 170×170×170.', 'SM_Grua_Carro, SM_Grua_Spreader 620×250×20.', 'Contrapeso 260×100×110.']),
        ('OG · low poly', ['Tramo: 4 montantes de caja + diagonales como planos con alfa, o caja con textura de celosía recortada. ~60 tris por tramo.', 'Pluma: una caja larga + 2 tirantes de 2 tris.', 'T_OG_MetalGrua_64; franjas rosa con color plano de marca.']),
        ('UE · pulido', ['Celosía modelada: perfiles en L, cartelas en las uniones. ~500 tris por tramo.', 'Cabina con cristal, barandilla y escalera. ~3 000 tris.', 'T_UE_MetalGrua (BC, N, ORM) + MI con color marca para las franjas.']),
        ('Notas', ['Separa carro, cable y spreader en actores o sockets: se animan.', 'El cable puede ser un Cable Component.', 'Fondo de la zona: siluetas de edificios en color cielo oscurecido, sin textura.'])])

def h05():
    v = View(DX, DY, 1000, 1330, 1.35, 'VALLA · FRENTE', 220, 120)
    v.ground()
    for x in (40, 440): v.R(x, 0, 20, 300, C['com_linea'], C['borde'])
    v.R(0, 250, 500, 450, C['com'], C['borde'], rx=12).R(1, 625, 498, 74, C['marca'], None, 0).R(0, 250, 500, 450, 'none', C['borde'], rx=12)
    v.note(30, 648, 'PATROCINADO').note(30, 520, '¡REMAKE ULTRA HD!').note(30, 480, 'T_Senal_Valla_RemakeUltraHD').R(30, 290, 180, 50, C['marca'], None, 0, rx=25).Ci(410, 320, 46, C['moneda'], C['tinta'], 2)
    v.dh(0, 500, 730).dv(-30, 250, 700, '450').dv(-30, 0, 250, '250').dh(40, 60, -24, '20').dh(60, 440, 215, '380').fig(-100, 180)
    v2 = View(DX + 1020, DY, 620, 640, 1.35, 'VALLA · LADO', 250, 120)
    v2.ground().R(0, 0, 20, 300, C['com_linea'], C['borde']).R(-5, 250, 30, 450, C['com'], C['borde']).L(20, 0, 80, 0, C['borde'], 3).L(20, 180, 80, 0, C['borde'], 3)
    v2.dh(-5, 25, 730, '30').dv(110, 0, 700, '700', off=10).note(90, 90, 'tornapunta opcional')
    v3 = View(DX + 1020, DY + 660, 620, 670, 1.1, 'FORMATOS', 50, 60)
    v3.R(0, 380, 200, 200, C['marca'], C['marca_osc']).note(0, 590, 'póster 200×200').R(230, 380, 200, 200, C['marca_tinte'], C['marca_osc'])
    v3.R(0, 0, 150, 300, C['com'], C['borde'], rx=8).note(0, 310, 'Mega oferta 150×300').R(190, 170, 200, 100, C['marca'], C['marca_osc'], rx=8).note(190, 280, 'cartel 200×100')
    v3.R(190, 0, 320, 20, C['marca'], C['marca_osc']).note(190, 30, 'banda 1600×100 (a 1/5)').R(450, 170, 60, 60, C['moneda'], C['tinta'], rx=30).note(450, 240, 'Ø 60')
    sheet(5, 'Vallas y carteles', 'Zonas 0, 1, 2 y 4. Todo lo comercial es un plano con textura sobre un soporte.', [v, v2, v3], [
        ('Piezas', ['SM_Valla_Grande: panel 500×450×30 sobre 2 postes 20×20×300.', 'SM_Valla_Riel (zona 2): panel 150×300×10 con dos ruedas sobre riel.', 'SM_Poster 200×200×4, SM_Cartel 200×100×4.', 'SM_Banda 1600×100 (escenario) y 400×100.']),
        ('OG · low poly', ['Un quad por cartel (2 tris) + postes de caja.', 'Texturas T_OG_Senal_* (1/8 de tamaño, Nearest, alfa de 1 bit: usa Masked).']),
        ('UE · pulido', ['Panel con marco de 3 cm, radio 12, tornillos en las esquinas. ~400 tris.', 'Texturas T_Senal_* como BaseColor; Roughness 0.25, un poco de Emissive (0.3) para que “brillen” frente a lo OG.', 'Material Masked o Translucent para esquinas redondeadas.']),
        ('Notas', ['La valla de la zona 0 tapa el faro: colócala entre la cámara y el faro.', 'La valla en riel es mecánica de tracción: pivote en el eje de las ruedas.', 'Mantén los pósters en rejilla de 50 cm; el desorden es intencional pero alineado.'])])

def h06():
    v = View(DX, DY, 900, 1330, .98, 'FRENTE', 440, 150)
    v.water(0)
    v.raw(lambda: f'<ellipse cx="{v.X(0)}" cy="{v.Y(20)}" rx="{250*v.sc}" ry="{60*v.sc}" fill="{C["gris"]}" stroke="{C["tinta"]}" stroke-width="3"/>', -250, -40, 250, 80)
    v.P([(-120, 40), (120, 40), (80, 840), (-80, 840)], '#f3eadb')
    for a, b_ in ((240, 340), (540, 640)):
        wa = 120 - 40 * (a - 40) / 800; wb = 120 - 40 * (b_ - 40) / 800
        v.P([(-wa, a), (wa, a), (wb, b_), (-wb, b_)], C['og'], C['og_prof'], 2)
    v.P([(-120, 40), (120, 40), (80, 840), (-80, 840)], 'none')
    v.R(-100, 840, 200, 16, C['com_linea']).R(-70, 856, 140, 140, C['luz'], C['og_prof']).L(-24, 856, -24, 996, C['og_prof'], 2).L(24, 856, 24, 996, C['og_prof'], 2).P([(-90, 996), (90, 996), (0, 1096)], C['og_osc'], C['og_prof'])
    v.dv(-300, 40, 840, '800').dh(-120, 120, -30, 'Ø 240 base', off=40).dh(-80, 80, 800, 'Ø 160').dv(170, 856, 996, '140').dv(170, 996, 1096, '100').dv(-300, 240, 340, '100', off=70).fig(190, 180, 40)
    v.note(140, 290, 'bandas OG a Z 240 y 540').note(270, 50, 'roca Ø 500, alto 40')
    v2 = View(DX + 920, DY, 720, 660, .98, 'PLANTA', 360, 330)
    v2.Ci(0, 0, 250, C['gris']).P([(120 * math.cos(math.radians(22.5 + 45 * i)), 120 * math.sin(math.radians(22.5 + 45 * i))) for i in range(8)], '#f3eadb')
    v2.Ci(0, 0, 80, 'none', C['borde'], 2, 'stroke-dasharray="8 6"').R(-70, -70, 140, 140, C['luz'], C['og_prof'], 2).note(-250, -290, 'OG: octágono · UE: 24 lados')
    v3 = View(DX + 920, DY + 680, 720, 650, 2.1, 'LINTERNA', 250, 110)
    v3.R(-100, 0, 200, 16, C['com_linea']).R(-70, 16, 140, 140, C['luz'], C['og_prof']).L(-24, 16, -24, 156, C['og_prof'], 2).L(24, 16, 24, 156, C['og_prof'], 2).P([(-90, 156), (90, 156), (0, 256)], C['og_osc'], C['og_prof'])
    v3.L(-74, 100, -150, 120, C['moneda'], 5).L(74, 100, 150, 120, C['moneda'], 5).dh(-100, 100, -18, '200 galería').dh(-70, 70, 60, '140').note(-110, 270, 'rayos: 2 planos con alfa, giran', dy=-6)
    sheet(6, 'Faro', 'Zonas 0 y 5. Tapado por la valla al inicio; despejado y encendido al final.', [v, v2, v3], [
        ('Piezas', ['SM_Faro_Torre: tronco Ø 240 → Ø 160, alto 800.', 'SM_Faro_Linterna 140×140×140 + galería Ø 200.', 'SM_Faro_Techo: pirámide 180×180×100.', 'SM_Faro_Roca: Ø 500, alto 40.']),
        ('OG · low poly', ['Torre octogonal sin tapa inferior: 32 tris. Linterna: cubo. Techo: 4 tris.', 'T_OG_EstucoFaro_64 en la torre; bandas con T_OG_MaderaMuelle_64 (dos loops de aristas a Z 240–340 y 540–640).', 'Luz: color plano “luz” sin emisivo.']),
        ('UE · pulido', ['Torre de 24 lados con ligera curva, puerta y 2 ventanas. Galería con barandilla. ~5 000 tris.', 'T_UE_EstucoFaro + T_UE_MaderaMuelle para bandas; cristal emisivo cálido (#fcf3ca, intensidad 5).', 'Rect Light o Spot giratorio en la zona 5.']),
        ('Notas', ['En la zona 0 basta la mitad superior: lo demás lo cubre la valla.', 'Pivote al centro de la roca, Z = 0 en el nivel del agua.'])])

def h07():
    v = View(DX, DY, 900, 1330, 1.05, 'ASCENSOR · FRENTE', 330, 130)
    v.water(0).R(110, -100, 80, 300, C['com_linea'], C['borde'])
    v.R(0, 200, 300, 900, 'none', C['borde']).R(0, 200, 14, 900, C['com'], C['borde'], 2).R(286, 200, 14, 900, C['com'], C['borde'], 2)
    v.R(-10, 1100, 320, 40, C['com'], C['borde']).R(-10, 1100, 320, 12, C['marca'], None, 0).R(20, 200, 260, 20, C['com'], C['borde']).R(20, 220, 260, 10, C['marca'], None, 0)
    v.R(50, 620, 200, 100, C['marca'], C['marca_osc'], rx=8).note(70, 664, 'ACCESO VIP')
    v.raw(lambda: path(f'M{v.X(150)} {v.Y(240)} C{v.X(150)} {v.Y(900)} {v.X(260)} {v.Y(1180)} {v.X(400)} {v.Y(1020)}', 'none', C['tinta'], 3, 'stroke-dasharray="6 10" stroke-linecap="round"'), 150, 240, 400, 1080)
    v.R(300, 940, 240, 20, C['og'], C['og_prof']).R(300, 910, 240, 30, C['og_osc'])
    v.dh(0, 300, 1180).dv(-40, 200, 1100, '900').dh(20, 280, 160, '260').dv(560, 220, 960, '740 de viaje', off=10).fig(-110, 180)
    v2 = View(DX + 920, DY, 720, 640, 2.0, 'TRAMPOLÍN OG · LADO', 90, 110)
    v2.ground('cubierta').R(60, 0, 200, 30, C['og'], C['og_prof'])
    v2.raw(lambda: path('M' + ' L'.join(f'{v2.X(130 + (25 if i % 2 else -25))} {v2.Y(30 + i * 10)}' for i in range(7)), 'none', C['tinta'], 5, 'stroke-linejoin="round" stroke-linecap="round"'), 105, 30, 155, 90)
    v2.P([(20, 92), (280, 100), (280, 115), (20, 107)], C['og'], C['og_prof'])
    v2.dh(60, 260, -18).dh(20, 280, 150, '260 tabla').dv(300, 0, 30, '30', off=6).dv(300, 30, 100, '≈ 65 resorte', off=6)
    v3 = View(DX + 920, DY + 660, 720, 670, 1.5, 'PLANTA', 130, 150)
    v3.R(0, 0, 300, 300, 'none', C['borde']).R(20, 20, 260, 260, C['com'], C['borde'])
    for x, y in ((0, 0), (286, 0), (0, 286), (286, 286)): v3.R(x, y, 14, 14, C['com_linea'], C['tinta'], 2)
    v3.R(110, 110, 80, 80, 'none', C['borde'], 2, extra='stroke-dasharray="6 5"').dh(0, 300, -24).dv(-26, 0, 300).note(0, 318, 'plataforma 260×260, pilar 80×80', dy=-4)
    sheet(7, 'Ascensor y trampolín', 'Zona 1. Híbrido ascensor‑resorte: el trampolín OG da el impulso que el ascensor comercial cobra.', [v, v2, v3], [
        ('Piezas', ['SM_Ascensor_Marco 300×300×900 con 4 montantes de 14.', 'SM_Ascensor_Plataforma 260×260×20 + banda rosa de 10.', 'SM_Ascensor_Pilar 80×80, altura variable.', 'SM_Trampolin: base 200×60×30, resorte Ø 50, tabla 260×60×15.']),
        ('OG · low poly', ['Trampolín: 2 cajas + resorte como zigzag de 6 quads (o plano con alfa). ~40 tris.', 'T_OG_MaderaMuelle_64 y T_OG_MaderaOscura_64.', 'Ascensor en OG: cajas con T_OG_PanelComercial_64.']),
        ('UE · pulido', ['Marco con perfiles redondeados, cristal en 2 caras, cabecero con banda luminosa. ~2 500 tris.', 'Resorte helicoidal real (8 vueltas) con metal. ~1 200 tris.', 'T_UE_PanelComercial, T_UE_MetalGrua y T_UE_MaderaMuelle.']),
        ('Notas', ['Plataforma, resorte y tabla son piezas aparte: se animan.', 'Marca la zona de rebote con T_Senal_Hibrido_Rebote en el suelo o como decal.', 'El cartel “ACCESO VIP” es SM_Cartel 200×100 a Z = 620.'])])

def h08():
    v = View(DX, DY, 1640, 760, .92, 'FRENTE', 330, 330)
    v.water(0)
    v.R(-330, -330, 630, 550, C['muelle'], C['borde']).R(1100, -330, 330, 550, C['muelle'], C['borde'])
    v.R(-330, 220, 630, 20, C['og'], C['og_prof']).R(1100, 220, 330, 20, C['og'], C['og_prof'])
    v.P([(300, 240), (430, 215), (425, 198), (300, 220)], C['og'], C['og_prof']).P([(1100, 240), (980, 210), (984, 194), (1100, 220)], C['og'], C['og_prof']).P([(600, 20), (700, 50), (704, 34), (604, 4)], C['og'], C['og_prof'])
    for x in (150, 1180):
        v.R(x, 240, 12, 120, C['tinta']).R(x + 188, 240, 12, 120, C['tinta']).R(x, 320, 200, 40, C['precaucion'], C['tinta'])
        for i in range(5): v.P([(x + 10 + i * 40, 320), (x + 30 + i * 40, 320), (x + 50 + i * 40, 360), (x + 30 + i * 40, 360)], C['tinta'], None, 0)
    v.R(1140, 240, 30, 100, C['og_osc'])
    v.dh(300, 1100, 420, '800 de hueco').dh(300, 430, 150, '130 resto').dv(-250, 0, 220, '220').dh(150, 350, 400, '200').dv(380, 240, 360, '120', off=10).fig(-200, 180, 240)
    v.note(560, 80, 'restos flotando: tablas sueltas 100×16×8').note(1180, 380, 'poste de amarre 30×30×100: destino de la cuerda‑flecha', dy=-6)
    v2 = View(DX, DY + 780, 800, 550, 2.0, 'BARRERA', 240, 110)
    v2.ground('cubierta').R(0, 0, 12, 120, C['tinta']).R(188, 0, 12, 120, C['tinta']).R(0, 80, 200, 40, C['precaucion'], C['tinta'])
    for i in range(5): v2.P([(10 + i * 40, 80), (30 + i * 40, 80), (50 + i * 40, 120), (30 + i * 40, 120)], C['tinta'], None, 0)
    v2.R(-14, 0, 40, 8, C['tinta']).R(174, 0, 40, 8, C['tinta']).dh(0, 200, 150).dv(-34, 0, 120).dv(226, 80, 120, '40', off=6).note(0, -34, 'tabla: T_Senal_Barrera_Precaucion', dy=10)
    v3 = View(DX + 820, DY + 780, 820, 550, 1.3, 'SECCIÓN DEL MUELLE DE CONCRETO', 160, 300)
    v3.water(0).R(0, -200, 400, 420, C['muelle'], C['borde']).R(0, 220, 400, 20, C['og'], C['og_prof']).L(0, 110, 400, 110, C['borde'], 2).L(0, 0, 400, 0, C['borde'], 2)
    v3.dv(-34, -200, 220, '420').dh(0, 400, -230, 'módulo 400').note(20, 150, 'T_*_ConcretoMuelle: juntas cada 100')
    sheet(8, 'Puente eliminado', 'Zona 3. Dos muelles de concreto, un hueco de 8 m y lo que quedó del puente.', [v, v2, v3], [
        ('Piezas', ['SM_MuelleConcreto 400×200×420 (220 sobre el agua).', 'SM_Puente_Resto: tablero roto de 130, inclinado 10°.', 'SM_Tabla_Suelta 100×16×8.', 'SM_Barrera 200×120, tabla de 40.', 'SM_Poste_Amarre 30×30×100.']),
        ('OG · low poly', ['Muelle: caja. Resto del puente: caja cortada en diagonal (10 tris).', 'Barrera: 2 postes de caja + 1 quad con T_OG_Senal_Barrera_Precaucion.', 'T_OG_ConcretoMuelle_64, T_OG_MaderaMuelle_64, T_OG_Precaucion_64.']),
        ('UE · pulido', ['Borde de concreto con bisel de 5 cm, argollas y defensas de goma. ~1 500 tris por módulo.', 'Resto del puente con tablas astilladas y vigas a la vista. ~1 800 tris.', 'T_UE_ConcretoMuelle, T_UE_MaderaMuelle, T_UE_Precaucion.']),
        ('Notas', ['El hueco se cruza con la mecánica cuerda‑flecha hacia el poste de amarre o sobre el contenedor de la grúa.', 'Señal T_Senal_PuenteCerrado (100×100) en una de las barreras.', 'T_UE_Agua con UV en mundo; en OG, T_OG_Agua_64 con panning lento.'])])

def h09():
    v = View(DX, DY, 1640, 860, .7, 'FRENTE', 220, 190)
    v.R(-200, 0, 2000, 1000, C['noche'], None, 0)
    v.R(-200, -100, 2000, 100, C['escenario'], C['tinta'])
    for x0 in (-200, 1600):
        v.R(x0, 0, 200, 1000, C['marca'], C['marca_osc'])
        for i in range(1, 6): v.L(x0 + i * 33, 0, x0 + i * 33, 1000, C['marca_osc'], 2)
    v.R(-200, 850, 2000, 150, C['marca'], C['marca_osc'])
    for i in range(20): v.raw((lambda i=i: path(f'M{v.X(-200+i*100)} {v.Y(850)} Q{v.X(-150+i*100)} {v.Y(790)} {v.X(-100+i*100)} {v.Y(850)} Z', C['marca'], C['marca_osc'], 2)), -200 + i * 100, 800, -100 + i * 100, 850)
    v.R(300, 0, 220, 450, C['com'], C['borde']).R(300, 420, 220, 30, C['marca'], None, 0).Ci(410, 220, 26, 'none', C['marca'], 5).L(250, 470, 700, 470, C['gris'], 4)
    v.P([(700, 220), (1150, 220), (1115, 0), (735, 0)], C['com'], C['borde']).R(722, 80, 406, 40, C['marca'], None, 0)
    v.R(1300, 0, 280, 300, C['marca_tinte'], C['marca'], rx=40).R(1330, 300, 220, 30, C['marca_tinte'], C['marca'], rx=14)
    for x in (300, 800, 1300): v.R(x - 30, 770, 60, 40, C['com_linea'], C['tinta'], 2).P([(x - 20, 770), (x + 20, 770), (x + 150, 0), (x - 150, 0)], C['luz'], None, 0, 'opacity=".12"')
    v.dh(0, 1600, 1040, '1600 boca').dv(-240, 0, 850, '850').dv(-240, 850, 1000, '150', off=0).dh(-200, 0, -130, '200').dv(1840, -100, 0, '100', off=10)
    v.fig(120, 180)
    v2 = View(DX, DY + 880, 540, 450, 1.0, 'PANEL DESLIZANTE', 150, 70)
    v2.ground('escenario').R(0, 0, 220, 450, C['com'], C['borde']).R(0, 420, 220, 30, C['marca'], None, 0).Ci(110, 220, 26, 'none', C['marca'], 5).dh(0, 220, -22).dv(250, 0, 450, off=6)
    v3 = View(DX + 560, DY + 880, 540, 450, 1.0, 'PEDESTAL', 60, 80)
    v3.ground('escenario').P([(0, 220), (450, 220), (415, 0), (35, 0)], C['com'], C['borde']).R(22, 80, 406, 40, C['marca'], None, 0).dh(0, 450, 250).dh(35, 415, -22, '380').dv(480, 0, 220, off=4)
    v4 = View(DX + 1120, DY + 880, 520, 450, 1.0, 'EXPOSITOR', 110, 70)
    v4.ground('escenario').R(0, 0, 280, 300, C['marca_tinte'], C['marca'], rx=40).R(30, 300, 220, 30, C['marca_tinte'], C['marca'], rx=14)
    for i in range(1, 14):
        a = i * 40
        v4.L(min(a, 280), max(0, a - 280), max(0, a - 300), min(300, a), C['marca'], 1.5).L(280 - min(a, 280), max(0, a - 280), 280 - max(0, a - 300), min(300, a), C['marca'], 1.5)
    v4.dh(0, 280, -22).dv(-30, 0, 300).note(0, 345, 'acolchado: rebota', dy=-4)
    sheet(9, 'Escenario final', 'Zona 4. Teatro de la presentación: telón rosa, focos y tres piezas jugables.', [v, v2, v3, v4], [
        ('Piezas', ['SM_Escenario_Piso: módulos 400×400×100.', 'SM_Telon_Lateral 200×1000, SM_Telon_Bambalina 2000×150 con 16 ondas.', 'SM_Panel_Deslizante 220×450×40 sobre riel.', 'SM_Pedestal 450/380×220, banda “¡NUEVO!”.', 'SM_Expositor 280×300, radio 40.', 'SM_Foco 60×40.']),
        ('OG · low poly', ['Telón: plano plegado en zigzag de 6 pliegues (12 tris) con T_OG_Telon_64.', 'Expositor: caja con esquinas a 45° y T_OG_Acolchado_64.', 'Piso: T_OG_PisoEscenario_64. Haces de luz: planos con alfa.']),
        ('UE · pulido', ['Telón con pliegues modelados (o Cloth), terciopelo: T_UE_Telon, Roughness alto, algo de Sheen.', 'Expositor con capitoné real: T_UE_Acolchado con N fuerte. ~3 000 tris.', 'Piso brillante T_UE_PisoEscenario; focos con Spot Light y niebla volumétrica.']),
        ('Notas', ['Banda superior: T_Senal_Banda_PresentacionExclusiva sobre la bambalina.', 'El expositor es la superficie de rebote (híbrido) de esta zona.', 'Fondo: color noche (#292533), sin textura.'])])

def h10():
    v = View(DX, DY, 900, 660, 1.5, 'BOTE · LADO', 250, 190)
    v.water(40).P([(0, 120), (400, 120), (360, 20), (40, 20)], C['og'], C['og_prof']).L(0, 120, 400, 120, C['og_prof'], 5)
    for y in (45, 70, 95): v.L(20 + (120 - y) * .0, y, 380, y, C['og_osc'], 1.5)
    v.L(180, 120, 180, 440, C['og_prof'], 6).P([(192, 430), (192, 150), (330, 150)], C['papel'], C['borde'])
    v.dh(0, 400, 0, '400', off=40).dv(-30, 20, 120, '100').dv(430, 120, 440, '320 mástil', off=10).dh(192, 330, 480, '140 vela')
    v2 = View(DX + 920, DY, 720, 660, 1.5, 'POLEA OG', 360, 300)
    v2.R(-18, 90, 36, 100, C['og_osc'], C['og_prof']).Ci(0, 0, 90, C['og'], C['og_prof']).Ci(0, 0, 70, 'none', C['og_osc'], 2).Ci(0, 0, 18, C['og_osc'], C['og_prof'])
    v2.L(-90, 0, -90, -180, C['og_prof'], 4).dh(-90, 90, -110, 'Ø 180', off=20).note(-200, 215, 'cuelga del techo del corredor (zona 2)').note(-200, -175, 'grosor 30; la cuerda tira de la valla en riel', dy=20)
    v3 = View(DX, DY + 680, 1640, 650, 1.0, 'BANDEROLAS', 120, 150)
    v3.ground('cubierta').R(0, 0, 14, 440, C['og_osc'], C['og_prof']).R(1300, 0, 14, 420, C['og_osc'], C['og_prof'])
    v3.raw(lambda: path(f'M{v3.X(7)} {v3.Y(430)} Q{v3.X(650)} {v3.Y(330)} {v3.X(1307)} {v3.Y(410)}', 'none', C['borde'], 3), 7, 380, 1307, 430)
    cols = [C['og'], C['marca'], None]
    for i in range(9):
        t = (i + .8) / 10.2; x = 7 + 1300 * t; y = (1 - t) ** 2 * 430 + 2 * t * (1 - t) * 330 + t * t * 410
        c = cols[i % 3]
        v3.P([(x - 30, y), (x + 30, y), (x, y - 80)], c or C['blanco'], C['borde'] if not c else C['tinta'], 2, 'stroke-linejoin="round"' + ('' if c else ' stroke-dasharray="7 5"'))
    v3.dh(7, 1307, 480, '1300 entre postes').dv(-40, 0, 440, '440').dh(100, 160, 250, '60').dv(200, 320, 400, '80', off=0).fig(700, 180)
    v3.note(820, 200, 'orden: OG · marca · blanco punteado (boceto)').note(820, 165, 'T_Senal_Banderolas, repite en X')
    sheet(10, 'Bote, polea y banderolas', 'Zonas 0, 2 y 5. Props OG pequeños que dan vida al puerto.', [v, v2, v3], [
        ('Piezas', ['SM_Bote: casco 400×140×100, mástil 320, vela triangular 140×280.', 'SM_Polea: rueda Ø 180×30 + soporte 36×100.', 'SM_Banderolas: cuerda de 1300 con 9 banderines 60×80.', 'SM_Poste_Banderola 14×14×440.']),
        ('OG · low poly', ['Bote: casco de 10 tris (prisma trapezoidal), vela de 1 tri a dos caras.', 'Polea: cilindro de 8 lados (32 tris).', 'Banderolas: un quad curvo de 4 segmentos con T_OG_Senal_Banderolas (Masked).']),
        ('UE · pulido', ['Casco con tracas, bancos y timón. ~2 500 tris. Vela con Cloth o WPO de viento.', 'Polea de 32 lados con canal para la cuerda y eje metálico. ~900 tris.', 'Banderines como mallas sueltas con viento; cuerda con Cable Component.']),
        ('Notas', ['En la zona 5 no hay anuncios: solo banderolas, madera OG y trazos de boceto.', 'Los contornos punteados (cajas y banco de la zona 5) usan el estilo de T_UI_Panel_Boceto.', 'T_Senal_Mural_Antiguo (zona 2) va en un marco de madera de 300×300×10.'])])

for f in (h00, h01, h02, h03, h04, h05, h06, h07, h08, h09, h10): f()
for it in items:
    it['png'] = f"{OUT}/{it['name']}.png"; it['svgpath'] = f"{OUT}/SVG/{it['name']}.svg"
render(items)
from PIL import Image
for it in items: Image.open(it['png']).convert('RGB').save(it['png'], optimize=True)
print([it['name'] for it in items])
