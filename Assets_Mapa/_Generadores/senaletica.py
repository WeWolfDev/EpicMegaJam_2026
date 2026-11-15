"""Señalética del mapa. Salida: Senaletica/UE_Pulido (PNG alta), Senaletica/OG_LowPoly (PNG 1/8, paleta corta), Senaletica/SVG."""
import sys, os
import numpy as np
from PIL import Image
from svglib import *
OUT = sys.argv[1]
items = []
def add(name, w, h, body, defs=''):
    items.append(dict(name=name, w=w, h=h, svg=svg(w, h, body, defs),
                      png=f'{OUT}/UE_Pulido/T_Senal_{name}.png', svgpath=f'{OUT}/SVG/Senal_{name}.svg'))

# ---------- comercial
def valla_remake():
    w = h = 1024; b = rect(8, 8, w - 16, h - 16, C['com'], 28, C['com_linea'], 8)
    b += f'<path d="M8 36 a28 28 0 0 1 28 -28 h{w-72} a28 28 0 0 1 28 28 v124 h-{w-16} z" fill="{C["marca"]}"/>'
    b += text(72, 118, 'PATROCINADO', 62, C['com'], BC, 700, extra='letter-spacing="6"')
    b += text(64, 410, '¡REMAKE', 228, C['marca'], BC, 700)
    b += text(64, 626, 'ULTRA HD!', 228, C['marca'], BC, 700)
    b += text(72, 740, 'Ahora con pase de temporada', 44, C['borde'], SG, 500)
    b += rect(72, 810, 500, 130, C['marca'], 65) + text(322, 900, 'COMPRAR YA', 76, C['com'], BC, 700, 'middle', 'letter-spacing="3"')
    b += circle(830, 850, 108, C['moneda'], C['tinta'], 6) + text(830, 884, '4K', 100, C['tinta'], BC, 700, 'middle')
    return w, h, b
def valla_mega():
    w, h = 512, 1024; b = rect(6, 6, w - 12, h - 12, C['com'], 22, C['com_linea'], 6)
    b += f'<path d="M6 28 a22 22 0 0 1 22 -22 h{w-56} a22 22 0 0 1 22 22 v108 h-{w-12} z" fill="{C["marca"]}"/>'
    b += text(w / 2, 96, 'MEGA OFERTA', 60, C['com'], BC, 700, 'middle', 'letter-spacing="6"')
    for i, t in enumerate(['¡PASA', 'POR', 'CAJA!']):
        b += text(w / 2, 370 + i * 170, t, 190, C['marca'], BC, 700, 'middle')
    b += text(w / 2, 900, 'Pasillo patrocinado', 40, C['borde'], SG, 500, 'middle')
    return w, h, b
def acceso_vip():
    w, h = 512, 256; b = rect(0, 0, w, h, C['marca'], 20)
    b += text(w / 2, 122, 'ACCESO VIP', 110, C['com'], BC, 700, 'middle', 'letter-spacing="2"')
    b += text(w / 2, 204, 'solo 4,99 €', 64, C['com'], BC, 500, 'middle')
    return w, h, b
def poster(t, estilo):
    w = h = 512
    fill, ink, stroke = {'marca': (C['marca'], C['com'], None), 'blanco': (C['blanco'], C['marca'], C['com_linea']), 'tinte': (C['marca_tinte'], C['marca_osc'], None)}[estilo]
    b = rect(4, 4, w - 8, h - 8, fill, 12, stroke, 8 if stroke else 0)
    size = 230 if len(t) <= 3 else 190
    b += text(w / 2, h / 2 + size * .34, t, size, ink, BC, 700, 'middle')
    return w, h, b
def banda(t, w, size):
    h = 128; return w, h, rect(0, 0, w, h, C['marca']) + text(w / 2, 64 + size * .35, t, size, C['com'], BC, 700, 'middle', 'letter-spacing="10"')
def caja_comercial():
    w = h = 512; b = rect(6, 6, w - 12, h - 12, C['com'], 56, C['com_linea'], 8)
    b += rect(10, 150, w - 20, 84, C['marca']) + circle(w / 2, 350, 36, 'none', C['marca'], 16)
    return w, h, b
def moneda():
    return 256, 256, circle(128, 128, 120, C['moneda'], C['tinta'], 8) + circle(128, 128, 96, 'none', '#d9b85c', 5) + text(128, 168, '4K', 116, C['tinta'], BC, 700, 'middle')

# ---------- OG / puerto
def tablas(w, h, n, borde=10, clavos=True, vetas=True):
    b = rect(borde / 2, borde / 2, w - borde, h - borde, C['og'], 6, C['og_osc'], borde)
    ph = (h - 2 * borde) / n
    for i in range(1, n):
        b += line(borde, borde + i * ph, w - borde, borde + i * ph, C['og_osc'], 5)
    for i in range(n):
        y = borde + i * ph + ph / 2
        if vetas: b += line(borde + 40 + (i * 97) % 120, y - ph * .2, borde + 40 + (i * 97) % 120 + w * .22, y - ph * .2, C['og_luz'], 4, 'stroke-linecap="round"')
        if vetas: b += line(w * .55 + (i * 53) % 90, y + ph * .22, w * .55 + (i * 53) % 90 + w * .18, y + ph * .22, '#95683a', 4, 'stroke-linecap="round"')
        if clavos:
            b += circle(borde + 18, y, 6, C['og_prof']) + circle(w - borde - 18, y, 6, C['og_prof'])
    return b
def zona(n, nombre):
    w, h = 1024, 256; b = tablas(w, h, 1, vetas=False)
    b += rect(44, 44, 168, 168, C['og_osc'], 10) + text(128, 178, str(n), 150, C['papel'], SG, 700, 'middle')
    b += text(250, 160, nombre, 86, C['og_prof'], BC, 700, extra='letter-spacing="1"')
    return w, h, b
def flecha(rot):
    w = h = 256; b = tablas(w, h, 2, clavos=False)
    b += f'<g transform="rotate({rot} 128 128)">' + path('M52 128 H180 M136 78 L190 128 L136 178', 'none', C['og_prof'], 30, 'stroke-linecap="round" stroke-linejoin="round"') + '</g>'
    return w, h, b
def franjas(id_, a=C['precaucion'], bcol=C['tinta'], s=64):
    return f'<pattern id="{id_}" width="{s}" height="{s}" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="{s}" height="{s}" fill="{a}"/><rect width="{s/2}" height="{s}" fill="{bcol}"/></pattern>'
def puente_cerrado():
    w = h = 512; d = franjas('fr', s=64)
    b = rect(0, 0, w, h, 'url(#fr)', 16) + rect(40, 40, w - 80, h - 80, C['papel'], 8, C['tinta'], 8)
    b += text(w / 2, 216, 'PUENTE', 124, C['tinta'], BC, 700, 'middle') + text(w / 2, 336, 'CERRADO', 124, C['tinta'], BC, 700, 'middle')
    b += text(w / 2, 420, 'eliminado en la actualización', 38, C['borde'], BC, 500, 'middle')
    return w, h, b, d
def barrera():
    w, h = 1024, 256; d = franjas('fr', s=128)
    return w, h, rect(4, 4, w - 8, h - 8, 'url(#fr)', 10, C['tinta'], 8), d
def banderolas():
    w, h = 2048, 256; b = path(f'M0 30 Q {w/4} 62 {w/2} 30 T {w} 30', 'none', C['borde'], 6)
    cols = [C['og'], C['marca'], None]
    n = 12
    for i in range(n):
        x = (i + .5) * w / n; import math
        y = 30 + 16 * math.sin(math.pi * 2 * (x / w) * 2) * (1 if (x % (w / 2)) < w / 4 else 1)
        yy = 30 + 16 * abs(math.sin(math.pi * 2 * x / w))  # aproximación de la comba
        c = cols[i % 3]
        pts = [(x - 58, yy + 4), (x + 58, yy + 4), (x, yy + 150)]
        if c: b += poly(pts, c, C['og_prof'] if c == C['og'] else C['marca_osc'], 5, 'stroke-linejoin="round"')
        else: b += poly(pts, C['blanco'], C['borde'], 5, 'stroke-dasharray="12 9" stroke-linejoin="round"')
    return w, h, b
def mural():
    w = h = 1024; f = 44
    b = rect(0, 0, w, h, C['og_osc'], 8) + rect(f, f, w - 2 * f, h - 2 * f, '#f3e3c3')
    b += circle(700, 300, 96, C['sol'])
    b += rect(f, 610, w - 2 * f, h - f - 610, C['agua']) + rect(f, 560, w - 2 * f, 50, C['og'])
    for x, y, l in [(140, 700, 120), (420, 790, 160), (700, 720, 110), (240, 880, 140), (760, 900, 120)]:
        b += line(x, y, x + l, y, '#c9dcee', 8, 'stroke-linecap="round"')
    b += poly([(560, 640), (800, 640), (760, 720), (600, 720)], C['og'], C['og_prof'], 6, 'stroke-linejoin="round"')
    b += line(660, 640, 660, 440, C['og_prof'], 8) + poly([(672, 450), (672, 620), (780, 620)], C['papel'], C['borde'], 5, 'stroke-linejoin="round"')
    b += rect(f, f, w - 2 * f, h - 2 * f, 'none', 0, C['og_prof'], 8)
    return w, h, b
def caja_og():
    w = h = 512; m = 44
    b = rect(4, 4, w - 8, h - 8, C['og'], 6, C['og_prof'], 8)
    b += line(m, m, w - m, h - m, C['og_osc'], 44) + line(w - m, m, m, h - m, C['og_osc'], 44)
    b += rect(m / 2 + 4, m / 2 + 4, w - m - 8, h - m - 8, 'none', 0, C['og_osc'], m)
    b += rect(4, 4, w - 8, h - 8, 'none', 6, C['og_prof'], 8) + rect(m + 4, m + 4, w - 2 * m - 8, h - 2 * m - 8, 'none', 0, C['og_prof'], 6)
    for x, y in [(26, 26), (w - 26, 26), (26, h - 26), (w - 26, h - 26)]: b += circle(x, y, 8, C['og_prof'])
    return w, h, b
def hibrido(tipo):
    w = h = 512
    b = rect(14, 14, w - 28, h - 28, C['blanco'], 40, C['tinta'], 10, 'stroke-dasharray="30 22" stroke-linecap="round"')
    if tipo == 'Rebote':
        b += path('M146 120 H366 M146 330 H366 M170 120 L342 162 L170 204 L342 246 L170 288 L342 330', 'none', C['tinta'], 22, 'stroke-linecap="round" stroke-linejoin="round"')
        t = 'REBOTE'
    else:
        b += path('M110 300 C 180 120, 300 110, 392 210', 'none', C['tinta'], 22, 'stroke-linecap="round" stroke-dasharray="34 30"')
        b += path('M318 222 L400 220 L384 138', 'none', C['tinta'], 22, 'stroke-linecap="round" stroke-linejoin="round"')
        t = 'TRACCIÓN'
    b += text(w / 2, 446, t, 92, C['tinta'], BC, 700, 'middle', 'letter-spacing="6"')
    return w, h, b

add('Valla_RemakeUltraHD', *valla_remake()); add('Valla_MegaOferta', *valla_mega()); add('Cartel_AccesoVIP', *acceso_vip())
for t, e, n in [('¡YA!', 'marca', 'Ya'), ('-80%', 'blanco', 'Menos80'), ('NEW', 'tinte', 'New'), ('TOP', 'blanco', 'Top'), ('4K', 'marca', '4K'),
                ('VIP', 'marca', 'Vip'), ('SALE', 'blanco', 'Sale'), ('HOT', 'marca', 'Hot'), ('+XP', 'tinte', 'MasXP'), ('DLC', 'tinte', 'Dlc')]:
    add(f'Poster_{n}', *poster(t, e))
add('Banda_PresentacionExclusiva', *banda('PRESENTACIÓN EXCLUSIVA · SOLO HOY', 2048, 76)); add('Banda_Nuevo', *banda('¡NUEVO!', 512, 84))
add('CajaComercial_Cara', *caja_comercial()); add('Moneda_4K', *moneda())
for n, nom in enumerate(['Muelle de llegada', 'Ascensor de lujo', 'Corredor de anuncios', 'Puente eliminado', 'Escenario final', 'Puerto restaurado']):
    add(f'Zona_{n}', *zona(n, nom))
for nom, r in [('Derecha', 0), ('Abajo', 90), ('Izquierda', 180), ('Arriba', 270)]: add(f'Flecha_{nom}', *flecha(r))
add('PuenteCerrado', *puente_cerrado()); add('Barrera_Precaucion', *barrera()); add('Banderolas', *banderolas()); add('Mural_Antiguo', *mural()); add('CajaOG_Cara', *caja_og())
add('Hibrido_Rebote', *hibrido('Rebote')); add('Hibrido_Traccion', *hibrido('Traccion'))
render(items)

# ---------- versiones OG: 1/8 del tamaño, paleta del sistema, alfa de 1 bit
PAL = np.array([[int(v[i:i+2], 16) for i in (1, 3, 5)] for v in C.values()], float)
os.makedirs(f'{OUT}/OG_LowPoly', exist_ok=True)
for it in items:
    im = Image.open(it['png']).convert('RGBA')
    sm = im.resize((im.width // 8, im.height // 8), Image.BOX)
    a = np.asarray(sm, float); rgb = a[..., :3]; al = a[..., 3]
    d = ((rgb[:, :, None, :] - PAL[None, None]) ** 2).sum(-1)
    q = PAL[d.argmin(-1)]
    o = np.dstack([q, np.where(al >= 128, 255, 0)]).astype(np.uint8)
    Image.fromarray(o).save(f"{OUT}/OG_LowPoly/T_OG_Senal_{it['name']}.png", optimize=True)
    im.save(it['png'], optimize=True)
print(len(items), 'señales')
