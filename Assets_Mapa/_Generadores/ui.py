"""UI del juego (UMG). PNG a 2x con alfa + SVG fuente. Paneles y botones son 9-slice."""
import sys
from svglib import *
OUT = sys.argv[1]
items = []
def add(name, w, h, body, defs='', scale=2):
    items.append(dict(name=name, w=w, h=h, scale=scale, svg=svg(w, h, body, defs), png=f'{OUT}/T_UI_{name}.png', svgpath=f'{OUT}/SVG/UI_{name}.svg'))
RJ = 'stroke-linecap="round" stroke-linejoin="round"'

# título
def titulo(c1, c2):
    return text(8, 96, 'The Last Patch:', 104, c1, SG, 700) + text(8, 216, 'Director’s Cut', 104, c2, SG, 700)
add('Titulo', 840, 256, titulo(C['tinta'], C['marca']))
add('Titulo_Claro', 840, 256, titulo(C['papel'], '#e39ab4'))

# paneles 9-slice (128, margen 32)
add('Panel_Comercial', 128, 128, rect(2, 2, 124, 124, C['com'], 14, C['com_linea'], 4))
add('Panel_ComercialCabecera', 128, 128, rect(2, 2, 124, 124, C['com'], 14, C['com_linea'], 4) + path('M2 16 a14 14 0 0 1 14 -14 h96 a14 14 0 0 1 14 14 v16 h-124 z', C['marca']))
add('Panel_OG', 128, 128, rect(3, 3, 122, 122, C['og'], 6, C['og_prof'], 6) + rect(12, 12, 104, 104, C['arena_clara'], 3, C['og_osc'], 4)
    + ''.join(circle(x, y, 2.5, C['og_prof']) for x in (8, 120) for y in (8, 120)))
add('Panel_Boceto', 128, 128, rect(3, 3, 122, 122, C['blanco'], 14, C['tinta'], 3, 'stroke-dasharray="8 6" stroke-linecap="round"'))
add('Panel_Noche', 128, 128, rect(2, 2, 124, 124, C['noche'], 14, C['escenario'], 4))

# botones 9-slice (píldora 160x64, margen 32)
def boton_marca(fill, ink, dy=0, sombra=True):
    b = rect(2, 6, 156, 56, C['marca_osc'], 28) if sombra else ''
    return b + rect(2, 2 + dy, 156, 56, fill, 28)
add('Boton_Marca_Normal', 160, 64, boton_marca(C['marca'], C['com']))
add('Boton_Marca_Hover', 160, 64, boton_marca('#d36e90', C['com']))
add('Boton_Marca_Presionado', 160, 64, boton_marca(C['marca_osc'], C['com'], 4, False))
add('Boton_Marca_Deshabilitado', 160, 64, rect(2, 2, 156, 56, C['com_linea'], 28))
def boton_og(fill, dy=0, sombra=True):
    b = rect(3, 7, 154, 54, C['og_prof'], 6) if sombra else ''
    return b + rect(3, 3 + dy, 154, 54, fill, 6, C['og_prof'], 4) + line(12, 14 + dy, 148, 14 + dy, C['og_luz'], 3, 'stroke-linecap="round" opacity=".7"')
add('Boton_OG_Normal', 160, 64, boton_og(C['og']))
add('Boton_OG_Hover', 160, 64, boton_og(C['og_luz']))
add('Boton_OG_Presionado', 160, 64, boton_og(C['og_osc'], 4, False))
add('Boton_OG_Deshabilitado', 160, 64, rect(3, 3, 154, 54, '#b7a98d', 6, '#9a8c72', 4))

# etiquetas (píldora 96x32, margen 16)
for n, f, s, ex in [('OG', C['og_osc'], None, ''), ('Comercial', C['marca_osc'], None, ''), ('Personaje', C['personaje'], None, ''), ('Hibrido', C['blanco'], C['tinta'], 'stroke-dasharray="5 4"')]:
    add(f'Etiqueta_{n}', 96, 32, rect(2, 2, 92, 28, f, 14, s, 2 if s else 0, ex))

# formas (planos)
def forma_og():
    P = [(64, 12), (110, 38), (110, 90), (64, 116), (18, 90), (18, 38)]; c = (64, 64)
    cols = [C['og_luz'], C['og'], C['og_osc'], C['og_prof'], C['og_osc'], C['og']]
    b = ''.join(poly([P[i], P[(i + 1) % 6], c], cols[i]) for i in range(6))
    return b + poly(P, 'none', C['og_prof'], 5, RJ) + ''.join(line(c[0], c[1], x, y, C['og_prof'], 3) for x, y in P)
def forma_ue():
    d = f'<radialGradient id="g" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#f3b3c8"/><stop offset=".45" stop-color="{C["marca"]}"/><stop offset="1" stop-color="{C["marca_osc"]}"/></radialGradient>'
    return circle(64, 64, 52, 'url(#g)', C['marca_osc'], 4) + f'<ellipse cx="46" cy="42" rx="14" ry="9" fill="#fff" opacity=".7" transform="rotate(-30 46 42)"/>', d
add('Forma_OG', 128, 128, forma_og())
b, d = forma_ue(); add('Forma_UE', 128, 128, b, d)
add('Forma_Selector', 128, 128, rect(4, 4, 120, 120, 'none', 20, C['tinta'], 6) + rect(4, 4, 120, 120, 'none', 20, C['moneda'], 6, 'stroke-dasharray="20 16" stroke-linecap="round"'))
add('Forma_Ranura', 128, 128, rect(4, 4, 120, 120, C['papel'], 20, C['borde'], 4))

# iconos (64, trazo 5) en tinta y en claro
IC = {
 'Boya': lambda c: line(32, 6, 32, 20, c, 5, RJ) + path('M16 36 a16 16 0 0 1 32 0 z', c, c, 5, RJ) + circle(32, 36, 16, 'none', c, 5) + line(32, 52, 32, 58, c, 5, RJ),
 'Anzuelo': lambda c: circle(38, 10, 4, 'none', c, 4) + path('M38 14 V40 a13 13 0 0 1 -26 0 V34 L22 42', 'none', c, 5, RJ),
 'Resorte': lambda c: path('M14 10 H50 M14 54 H50 M18 10 L46 21 L18 32 L46 43 L18 54', 'none', c, 5, RJ),
 'CuerdaFlecha': lambda c: path('M8 46 C 18 16, 38 12, 52 28', 'none', c, 5, 'stroke-linecap="round" stroke-dasharray="7 7"') + path('M38 30 L54 30 L52 14', 'none', c, 5, RJ),
 'Caja': lambda c: rect(10, 10, 44, 44, 'none', 3, c, 5) + path('M10 10 L54 54 M54 10 L10 54', 'none', c, 5, RJ),
 'Faro': lambda c: path('M24 24 H40 L46 56 H18 Z M22 14 H42 V24 H22 Z M20 14 L32 5 L44 14 M21 40 H43', 'none', c, 5, RJ) + path('M6 16 L14 18 M58 16 L50 18', 'none', c, 4, RJ),
 'Flecha': lambda c: path('M10 32 H52 M36 16 L52 32 L36 48', 'none', c, 6, RJ),
 'Pausa': lambda c: rect(16, 12, 11, 40, c, 3) + rect(37, 12, 11, 40, c, 3),
 'Reintentar': lambda c: path('M50 32 a18 18 0 1 1 -6 -13.4', 'none', c, 5, RJ) + path('M46 6 V20 H32', 'none', c, 5, RJ),
 'Check': lambda c: path('M12 34 L26 48 L52 16', 'none', c, 7, RJ),
 'Cerrar': lambda c: path('M16 16 L48 48 M48 16 L16 48', 'none', c, 7, RJ),
 'Candado': lambda c: rect(14, 28, 36, 28, c, 5) + path('M22 28 V20 a10 10 0 0 1 20 0 V28', 'none', c, 5, RJ),
 'Volumen': lambda c: path('M10 26 H20 L32 14 V50 L20 38 H10 Z', c, c, 4, RJ) + path('M40 24 a10 10 0 0 1 0 16 M46 16 a20 20 0 0 1 0 32', 'none', c, 5, RJ),
 'Ajustes': lambda c: path('M8 18 H56 M8 32 H56 M8 46 H56', 'none', c, 5, RJ) + circle(22, 18, 6, c) + circle(42, 32, 6, c) + circle(28, 46, 6, c),
 'Casa': lambda c: path('M10 30 L32 10 L54 30 M16 26 V54 H48 V26 M27 54 V38 H37 V54', 'none', c, 5, RJ),
}
for n, f in IC.items():
    add(f'Icono_{n}', 64, 64, f(C['tinta'])); add(f'Icono_{n}_Claro', 64, 64, f(C['papel']))

# vida (boya a color), progreso de zonas, diálogo, teclas, cursor
def boya(llena):
    top = C['marca'] if llena else C['com_linea']
    return line(32, 5, 32, 18, C['tinta'], 5, RJ) + circle(32, 36, 17, C['blanco'] if llena else C['com'], C['tinta'], 4) + path('M15 36 a17 17 0 0 1 34 0 z', top, C['tinta'], 4, RJ) + line(32, 53, 32, 59, C['tinta'], 5, RJ)
add('Vida_Llena', 64, 64, boya(True)); add('Vida_Vacia', 64, 64, boya(False))
add('Nodo_Pendiente', 48, 48, circle(24, 24, 18, C['papel'], C['borde'], 4, 'stroke-dasharray="6 5"'))
add('Nodo_Actual', 48, 48, circle(24, 24, 20, C['moneda'], C['tinta'], 4) + circle(24, 24, 7, C['tinta']))
add('Nodo_Completo', 48, 48, circle(24, 24, 20, C['og'], C['og_prof'], 4) + path('M14 25 L21 32 L34 17', 'none', C['papel'], 5, RJ))
add('Progreso_Pista', 64, 16, line(0, 8, 64, 8, C['og_osc'], 6, 'stroke-dasharray="10 6"'))
add('Dialogo', 512, 160, path('M18 4 H494 a14 14 0 0 1 14 14 V118 a14 14 0 0 1 -14 14 H96 L64 156 V132 H18 a14 14 0 0 1 -14 -14 V18 a14 14 0 0 1 14 -14 Z', C['papel'], C['tinta'], 4, RJ))
add('Tecla', 48, 48, rect(3, 7, 42, 38, C['borde'], 8) + rect(3, 3, 42, 38, C['blanco'], 8, C['tinta'], 3))
add('Tecla_Ancha', 96, 48, rect(3, 7, 90, 38, C['borde'], 8) + rect(3, 3, 90, 38, C['blanco'], 8, C['tinta'], 3))
add('Cursor', 32, 32, path('M5 3 L5 25 L11 19 L15 28 L19 26 L15 17 L23 17 Z', C['blanco'], C['tinta'], 2.5, RJ))
add('Moneda', 64, 64, circle(32, 32, 28, C['moneda'], C['tinta'], 4) + text(32, 43, '4K', 30, C['tinta'], BC, 700, 'middle'))
render(items)
from PIL import Image
for it in items: Image.open(it['png']).save(it['png'], optimize=True)
print(len(items), 'UI')
