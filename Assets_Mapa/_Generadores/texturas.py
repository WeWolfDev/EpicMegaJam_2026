"""Generador de texturas tileables · The Last Patch: Director's Cut
Dos planos: OG (low poly, 64x64, paleta corta, sin PBR) y UE (pulido, 1024, BaseColor + Normal DX + ORM).
Uso: python3 texturas.py <carpeta_salida>
"""
import sys, os
import numpy as np
from PIL import Image

OUT = sys.argv[1]
def hx(s): s = s.lstrip('#'); return np.array([int(s[i:i+2], 16) for i in (0, 2, 4)], float) / 255
OG, OGD, COM, MARCA = hx('ac7d49'), hx('74502c'), hx('f0f1f5'), hx('c55b7f')
AGUA, ARENA, ARENA_L, MUELLE = hx('7ca6ce'), hx('ebc5a0'), hx('f2dec3'), hx('c6b89d')
ESC, NOCHE, TINTA = hx('3a3343'), hx('292533'), hx('2b2a2e')

def fnoise(N, beta, seed, ax=1.0, ay=1.0):
    rng = np.random.default_rng(seed)
    fx = np.fft.fftfreq(N)[None, :] * N; fy = np.fft.fftfreq(N)[:, None] * N
    f = np.sqrt((fx * ax) ** 2 + (fy * ay) ** 2); f[0, 0] = 1
    spec = (rng.normal(size=(N, N)) + 1j * rng.normal(size=(N, N))) / f ** beta
    spec[0, 0] = 0
    n = np.fft.ifft2(spec).real
    lo, hi = np.percentile(n, [1, 99])
    return np.clip((n - lo) / (hi - lo), 0, 1)

def blur(a, sigma):
    N = a.shape[0]
    fx = np.fft.fftfreq(N)[None, :]; fy = np.fft.fftfreq(N)[:, None]
    g = np.exp(-2 * (np.pi * sigma) ** 2 * (fx ** 2 + fy ** 2))
    return np.fft.ifft2(np.fft.fft2(a) * g).real

def grid(N):
    v, u = np.meshgrid((np.arange(N) + .5) / N, (np.arange(N) + .5) / N, indexing='ij')
    return u, v  # u = x 0..1, v = y 0..1
def mix(a, b, t): return a + (b - a) * t[..., None]
def col(c, N): return np.broadcast_to(c, (N, N, 3)).copy()

def planks(N, n, seed, base, dark, grain_amt=.10, tone_amt=.10, joints=2):
    """Tablones horizontales. Devuelve albedo, altura."""
    rng = np.random.default_rng(seed)
    u, v = grid(N)
    px = 1 / N
    idx = np.floor(v * n).astype(int); t = v * n - idx
    gap = max(px * n, .045)
    g = fnoise(N, 1.1, seed + 1, ax=14, ay=1)
    offs = rng.integers(0, N, n); tone = rng.uniform(-1, 1, n); joff = rng.uniform(0, 1, n)
    grain = np.empty_like(g); seg = np.zeros((N, N)); jm = np.zeros((N, N), bool); nails = np.zeros((N, N))
    rows = idx[:, 0]
    for r in range(N):
        grain[r] = np.roll(g[r], offs[rows[r]])
    uu = (u + joff[idx]) % 1
    segi = np.floor(uu * joints); st = uu * joints - segi
    jw = max(px * joints, .012 * joints)
    jm = st < jw
    segtone = np.sin((segi + 1) * 12.9898 + idx * 78.233) * .5
    tonemap = tone[idx] * .7 + segtone * .6
    # clavos
    if N >= 256:
        d = np.hypot((st - jw - .06) / joints * n, t - .5 + .25) ; d2 = np.hypot((st - jw - .06) / joints * n, t - .5 - .25)
        nails = ((d < .045) | (d2 < .045)).astype(float)
    gapm = (t < gap) | jm
    cup = 1 - np.clip((np.abs(t - (.5 + gap / 2)) - .34) / .16, 0, 1) ** 2 * .5
    h = np.where(gapm, 0, cup * .85 + (grain - .5) * .18)
    h = h - nails * .25
    alb = col(base, N) * (1 + tonemap * tone_amt)[..., None]
    alb = alb * (1 + (grain - .5) * 2 * grain_amt)[..., None]
    alb = mix(alb, col(dark, N), gapm.astype(float) * .9)
    alb = mix(alb, col(dark * .8, N), nails)
    return np.clip(alb, 0, 1), h, gapm

def emboss(h, k):
    dx = h - np.roll(h, 1, axis=1); dy = h - np.roll(h, 1, axis=0)
    return np.clip(1 + k * (dx + dy), .55, 1.35)

BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16 - .47
def quant(alb, pal, spread=.06):
    N = alb.shape[0]
    b = np.tile(BAYER, (N // 4, N // 4))[..., None] * spread
    a = alb + b
    P = np.array(pal)
    d = ((a[:, :, None, :] - P[None, None]) ** 2 * np.array([.3, .5, .2])).sum(-1)
    return P[d.argmin(-1)]

def normal_dx(h, strength, N):
    gx = (np.roll(h, -1, 1) - np.roll(h, 1, 1)) * .5 * strength * N / 1024
    gy = (np.roll(h, -1, 0) - np.roll(h, 1, 0)) * .5 * strength * N / 1024
    n = np.stack([-gx, -gy, np.ones_like(h)], -1)
    n /= np.linalg.norm(n, axis=-1, keepdims=True)
    return n * .5 + .5

def ao_from(h, N):
    a = h - blur(h, N / 64)
    return np.clip(1 + a * 1.6, .45, 1)

def save(a, path):
    im = Image.fromarray((np.clip(a, 0, 1) * 255 + .5).astype(np.uint8))
    im.save(path, optimize=True)

# ---------- materiales: f(N, og) -> alb, h, rough, metal, nstrength, paleta OG, relieve OG
def m_madera_muelle(N, og):
    alb, h, _ = planks(N, 4 if og else 8, 11, OG, OGD * .62, joints=1 if og else 2)
    return alb, h, .78 - h * .08, 0, 9, [OGD * .62, OGD, hx('95683a'), OG, hx('c1935c')], .5
def m_madera_oscura(N, og):
    alb, h, _ = planks(N, 4 if og else 4, 23, OGD, OGD * .45, grain_amt=.14, joints=1)
    alb = np.transpose(alb, (1, 0, 2)); h = h.T
    return alb, h, .82 - h * .08, 0, 10, [OGD * .45, hx('5c3f22'), OGD, hx('8a6238')], .5
def m_piso_escenario(N, og):
    alb, h, _ = planks(N, 4 if og else 8, 37, ESC, NOCHE * .7, grain_amt=.06, tone_amt=.07, joints=1 if og else 2)
    return alb, h, .32 + (1 - h) * .2 + fnoise(N, 1.5, 5) * .12, 0, 5, [NOCHE * .7, NOCHE, ESC, hx('4a4256')], .35
def m_agua(N, og):
    w = fnoise(N, 1.7, 41, ax=3.2, ay=1); w2 = fnoise(N, 1.2, 42, ax=6, ay=1)
    hgt = w * .7 + w2 * .3
    alb = col(AGUA, N) * (1 + (w - .5) * .16)[..., None]
    crest = np.clip((hgt - .74) / .05, 0, 1)
    alb = mix(alb, col(hx('b9d2ea'), N), crest * .8)
    alb = mix(alb, col(hx('6a94bf'), N), np.clip((.34 - hgt) / .1, 0, 1) * .6)
    return alb, hgt, .08 + crest * .1, 0, 14, [hx('6a94bf'), AGUA, hx('8fb3d6'), hx('c9dcee')], 0
def m_arena(N, og):
    lowf = fnoise(N, 1.8, 51); sp = fnoise(N, .15, 52); u, v = grid(N)
    rip = np.sin(2 * np.pi * (v * 6 + lowf * 1.2 + np.sin(2 * np.pi * u) * .12)) * .5 + .5
    h = lowf * .5 + rip * .22 + sp * .28
    alb = mix(col(hx('ddb38a'), N), col(ARENA_L, N), np.clip(lowf * .6 + rip * .4, 0, 1))
    alb = mix(alb, col(ARENA, N), np.full((N, N), .45))
    alb *= (1 + (sp - .5) * .10)[..., None]
    return alb, h, .92 - sp * .08, 0, 5, [hx('d9ae86'), ARENA, hx('efd0b0'), ARENA_L], .25
def m_concreto(N, og):
    lowf = fnoise(N, 1.9, 61); sp = fnoise(N, .25, 62); st = fnoise(N, 1.4, 63, ax=9, ay=1)
    u, v = grid(N)
    lines = (np.minimum(v * 2 % 1, 1 - v * 2 % 1) < max(.6 / N, .004) * 2)
    pits = np.clip((sp - .93) / .04, 0, 1) if not og else np.clip((sp - .97) / .02, 0, 1)
    h = .7 + lowf * .2 + (sp - .5) * .12 - pits * .5 - lines * .5
    alb = col(MUELLE, N) * (1 + (lowf - .5) * .14 + (st - .5) * .08)[..., None]
    alb = mix(alb, col(hx('9a8c72'), N), np.clip(pits + lines * .8, 0, 1))
    return alb, h, .88 - lowf * .1, 0, 6, [hx('9a8c72'), hx('b7a98d'), MUELLE, hx('d3c7ae')], .3
def m_estuco(N, og):
    lowf = fnoise(N, 2.0, 71); tr = fnoise(N, 1.5, 72, ax=4, ay=1); sp = fnoise(N, .3, 73)
    h = lowf * .45 + tr * .35 + sp * .2
    alb = col(hx('f3eadb'), N) * (1 + (h - .5) * .09)[..., None]
    return alb, h, .9 - tr * .08, 0, 5, [hx('dccfb8'), hx('e9dec9'), hx('f3eadb'), hx('faf5ea')], .4
def m_panel(N, og):
    u, v = grid(N); n = 2
    tu = u * n % 1; tv = v * n % 1
    e = np.minimum(np.minimum(tu, 1 - tu), np.minimum(tv, 1 - tv)) / n
    w = max(1.0 / N, .004)
    seam = e < w
    bevel = np.clip(e / (w * 5), 0, 1)
    lowf = fnoise(N, 2.2, 81)
    h = np.where(seam, 0, .55 + .45 * bevel) + (lowf - .5) * .03
    alb = col(COM, N) * (1 + (lowf - .5) * .025)[..., None]
    alb = mix(alb, col(hx('c3c7d3'), N), seam.astype(float))
    return alb, h, .22 + lowf * .1 + seam * .4, 0, 6, [hx('c3c7d3'), hx('e2e4ec'), COM, hx('fbfbfd')], .35
def _corr(N, og, base, dark, light, seed):
    u, v = grid(N); n = 8 if og else 16
    t = u * n % 1
    prof = np.clip((np.minimum(t, 1 - t) - .14) / .16, 0, 1)   # trapecio
    lowf = fnoise(N, 2.0, seed); sc = fnoise(N, 1.3, seed + 1, ax=1, ay=6)
    h = prof + (lowf - .5) * .04
    alb = col(base, N) * (1 + (lowf - .5) * .08 + (sc - .5) * .05)[..., None]
    return alb, h, .42 + lowf * .14 + (1 - prof) * .08, 0, 9, [dark, base * .9, base, light], .22
def m_contenedor_marca(N, og): return _corr(N, og, MARCA, hx('8f3d5b'), hx('dc86a4'), 91)
def m_contenedor_blanco(N, og): return _corr(N, og, COM, hx('b9bdca'), hx('ffffff'), 95)
def m_metal_grua(N, og):
    u, v = grid(N)
    tv = v * 2 % 1; ev = np.minimum(tv, 1 - tv) / 2
    w = max(1.0 / N, .003)
    seam = ev < w
    k = 8
    du = (u * k % 1 - .5) / k; dv = np.minimum(np.abs(v - .0625) , np.minimum(np.abs(v - .4375), np.minimum(np.abs(v - .5625), np.abs(v - .9375))))
    r = np.hypot(du, dv)
    riv = np.clip(1 - r / (.012 if not og else .017), 0, 1)
    lowf = fnoise(N, 2.0, 101); st = fnoise(N, 1.4, 102, ax=9, ay=1)
    h = .6 - seam * .6 + riv ** .5 * .4 + (lowf - .5) * .03
    base = hx('e3e6ee')
    alb = col(base, N) * (1 + (lowf - .5) * .05 + (st - .5) * .05)[..., None]
    alb = mix(alb, col(hx('aeb3c2'), N), seam.astype(float))
    if og: alb = mix(alb, col(hx('aeb3c2'), N), (riv > 0).astype(float))
    return alb, h, .38 + lowf * .15, .0, 7, [hx('aeb3c2'), hx('cfd3de'), base, hx('f6f7fa')], .3
def m_telon(N, og):
    u, v = grid(N); lowf = fnoise(N, 2.6, 111)
    ph = lowf * .22
    f = np.sin(2 * np.pi * (u * 4 + ph)) * .6 + np.sin(2 * np.pi * (u * 8 + ph * 1.7) + 1.3) * .4
    h = f * .5 + .5
    fib = fnoise(N, .4, 112, ax=1, ay=6)
    alb = mix(col(hx('93395a'), N), col(hx('d86f94'), N), np.clip(h, 0, 1) ** 1.2)
    alb = mix(alb, col(MARCA, N), np.full((N, N), .35)) * (1 + (fib - .5) * .05)[..., None]
    return alb, h, .93 - h * .1, 0, 16, [hx('8f3d5b'), hx('ad4b6e'), MARCA, hx('d9789a')], 0
def m_precaucion(N, og):
    u, v = grid(N); k = 4
    s = (u + v) * k % 1
    m = s < .5
    edge = np.minimum(np.abs(s - .5), np.minimum(s, 1 - s)) / k
    lowf = fnoise(N, 1.8, 121); sc = fnoise(N, .9, 122, ax=1, ay=5)
    wear = np.clip((sc * .6 + lowf * .4 - .72) / .06, 0, 1) * (0 if og else 1)
    amar, neg = hx('e8b24a'), hx('2b2a2e')
    alb = np.where(m[..., None], amar, neg) * (1 + (lowf - .5) * .1)[..., None]
    alb = mix(alb, col(hx('8b8d96'), N), wear * .7)
    h = .6 + m * .05 - wear * .3 + (lowf - .5) * .05
    return alb, h, .5 + wear * .25 + lowf * .1, wear * .6, 4, [neg, hx('b98832'), amar, hx('f3cd7a')], 0
def m_acolchado(N, og):
    u, v = grid(N); k = 4
    a = (u + v) * k; b = (u - v) * k
    puff = (np.abs(np.sin(np.pi * a)) * np.abs(np.sin(np.pi * b))) ** .45
    seam = puff < (.30 if og else .16)
    fa = np.abs(a - np.round(a)); fb = np.abs(b - np.round(b))
    btn = np.hypot(fa, fb) / k < (.02 if og else .011)
    lowf = fnoise(N, 2.0, 131)
    h = puff - btn * .3
    alb = mix(col(hx('e9a9bf'), N), col(hx('f6d3de'), N), np.clip(puff * 1.1, 0, 1))
    alb = mix(alb, col(MARCA, N), np.clip(seam * .75 + btn, 0, 1).astype(float))
    alb *= (1 + (lowf - .5) * .04)[..., None]
    return alb, h, .7 - puff * .15, 0, 14, [MARCA, hx('e39ab4'), hx('f0bdcd'), hx('f8dce5')], 0

MATS = [('MaderaMuelle', m_madera_muelle), ('MaderaOscura', m_madera_oscura), ('PisoEscenario', m_piso_escenario),
        ('Agua', m_agua), ('Arena', m_arena), ('ConcretoMuelle', m_concreto), ('EstucoFaro', m_estuco),
        ('PanelComercial', m_panel), ('ContenedorMarca', m_contenedor_marca), ('ContenedorBlanco', m_contenedor_blanco),
        ('MetalGrua', m_metal_grua), ('Telon', m_telon), ('Precaucion', m_precaucion), ('Acolchado', m_acolchado)]

if __name__ == '__main__':
    og_dir = os.path.join(OUT, 'OG_LowPoly'); ue_dir = os.path.join(OUT, 'UE_Pulido')
    os.makedirs(og_dir, exist_ok=True); os.makedirs(ue_dir, exist_ok=True)
    for name, f in MATS:
        alb, h, rough, metal, ns, pal, relief = f(64, True)
        if relief: alb = alb * emboss(h, relief)[..., None]
        save(quant(alb, pal), os.path.join(og_dir, f'T_OG_{name}_64.png'))
        N = 1024
        alb, h, rough, metal, ns, pal, relief = f(N, False)
        save(alb, os.path.join(ue_dir, f'T_UE_{name}_BC.png'))
        save(normal_dx(h, ns, N), os.path.join(ue_dir, f'T_UE_{name}_N.png'))
        orm = np.stack([ao_from(h, N), np.broadcast_to(rough, (N, N)), np.broadcast_to(metal, (N, N))], -1)
        save(orm, os.path.join(ue_dir, f'T_UE_{name}_ORM.png'))
        print(name)
