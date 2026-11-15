# Expansion: separa las zonas, llena los huecos con plataformas y coloca enemigos
import os, shutil
try:
    import unreal
except ImportError:
    unreal = None
A, B, C = 5200.0, 5600.0, 5200.0
CUT_A, CUT_B, CUT_C = 1605.0, 4400.0, 8610.0
JZ, GS, WALK = 560.0, 1.15, 450.0
GR = 980.0 * GS
DMAX = WALK * 2 * JZ / GR
HMAX = JZ * JZ / (2 * GR)
g, G, h = round(0.68 * DMAX), round(0.78 * DMAX), round(0.45 * HMAX)

def sh(x):
    return x + (A if x > CUT_A else 0) + (B if x > CUT_B else 0) + (C if x > CUT_C else 0)

SPEC = {'p': (g, 280, 320), 's': (g * 0.9, 170, 220), 'L': (G, 320, 360), 'up': (g * 0.8, 240, 300),
        'isla': (g, 1000, 800), 'check': (g, 420, 420), 'mx': (g, 900, 320), 'my': (g, 300, 320),
        'fr': (g, 570, 320), 'pel': (g, 560, 420)}

def gen(name, x0, x1, y, z, pattern):
    out = []; cur = x0; i = 0; nchk = 0; zo = 0; nisla = 0; miss = 0
    while miss < len(pattern):
        if nchk < 1 and cur - x0 > 0.45 * (x1 - x0): t = 'check'
        else: t = pattern[i % len(pattern)]; i += 1
        gap, L, W = SPEC[t]
        if cur + gap + L > x1 - 150:
            if t == 'check': nchk += 1
            miss += 1; continue
        miss = 0
        zo = min(zo + h, 2 * h) if t == 'up' else 0
        a = cur + gap; e = dict(t=t, y=y, z=z + zo, W=W, gap=gap)
        if t == 'mx': e.update(x=a + 150, L=300, x2=a + 750)
        elif t == 'my': e.update(x=a + 150, L=300, y=y - 330, y2=y + 330)
        elif t == 'fr': e.update(x=a + 285, L=570)
        elif t == 'isla':
            nisla += 1; e.update(x=a + 500, L=1000, n=1 if (name == 'S1' and nisla == 1) else 2)
        else: e.update(x=a + L / 2, L=L)
        if t == 'check': nchk += 1
        out.append(e); cur = a + L
    rem = x1 - cur
    if rem > g:
        L = rem - 2 * g; gp = g
        if L < 160: L = 160; gp = (rem - 160) / 2
        out.append(dict(t='p', x=cur + gp + L / 2, y=y, z=z, L=L, W=340, gap=gp)); cur = cur + gp + L
    out.append(dict(t='fin', gap=x1 - cur))
    return out

STRETCH = [
    ('S1', 1600, 1600 + A, 3400, 0, ['p', 'up', 'isla', 'mx', 's', 'L', 'fr', 'p']),
    ('S2', 4600 + A, 4593 + A + B, 4150, 500, ['p', 'my', 'isla', 'fr', 'L', 'up', 'mx', 'pel', 'p']),
    ('S3', 8600 + A + B, 8600 + A + B + C, 4200, 0, ['s', 'L', 'pel', 'isla', 'mx', 'up', 'up', 'my', 'fr']),
    ('S4', 8600 + A + B, 8600 + A + B + C, 1000, 0, ['p', 'fr', 'isla', 'L', 'my', 's', 'up', 'mx', 'pel']),
    ('S5', 4200 + A, 4200 + A + B, 1000, 0, ['L', 'my', 'isla', 'fr', 's', 'mx', 'up', 'pel', 'p']),
]
# enemigos en las zonas (coordenadas originales): x, y, velocidad, vision, casa
ZONE_EN = [(500, 2750, 180, 700, 300), (2700, 3950, 240, 800, 350), (3300, 2650, 240, 800, 350),
           (6950, 4250, 240, 700, 250), (8050, 4200, 220, 600, 200), (9450, 4350, 250, 800, 350),
           (9700, 3700, 250, 800, 300), (9250, 1350, 250, 800, 300), (9100, 700, 250, 700, 250), (5400, 1000, 230, 700, 300)]

if unreal is None:
    print("g", g, "G", G, "h", h, "Dmax", round(DMAX), "Hmax", round(HMAX))
    for s in STRETCH:
        o = gen(*s); print(s[0], len(o) - 1, "max gap", round(max(e['gap'] for e in o)), [e['t'] for e in o])
else:
    LOG = []
    def log(*a):
        s = " ".join(str(x) for x in a); LOG.append(s); unreal.log("[TLP] " + s)
    proj = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
    eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    V = unreal.Vector
    def R(yaw=0, pitch=0): return unreal.Rotator(roll=0, pitch=pitch, yaw=yaw)
    BPD = "/Game/TheLastPatch/Blueprints"
    def CL(n): return unreal.load_asset(f"{BPD}/{n}").generated_class()
    ENE, MOV, TAB, PEL, CHK, VIDA, CHARLA = [CL(n) for n in ("BP_TLP_Enemigo", "BP_TLP_Mover", "BP_TLP_TablaFragil", "BP_TLP_Peligro", "BP_TLP_Checkpoint", "BP_TLP_Vida", "BP_TLP_Charla")]
    CUBE = unreal.load_asset("/Engine/BasicShapes/Cube.Cube"); CYL = unreal.load_asset("/Engine/BasicShapes/Cylinder.Cylinder")
    MB = "/Game/TheLastPatch/Blockout/"
    M = {n: unreal.load_asset(MB + n) for n in ("MI_Peligro", "MI_Fragil", "MI_Enemigo", "MI_Movil", "MI_Queso")}
    acts = eas.get_all_level_actors()
    L = {a.get_actor_label(): a for a in acts}
    done = "TLP_Expansion_Marca" in L
    # ---------- 1. separar zonas (una sola vez)
    if not done:
        bk = os.path.join(proj, "Respaldo_20261114_2146", "L_Puerto_antes_de_expansion.umap")
        shutil.copy2(os.path.join(proj, "Content", "L_Puerto.umap"), bk); log("respaldo", bk)
        SKIP = {"Floor", "BO_Agua", "BO_Trigger_Agua", "BO_Limite_N", "BO_Limite_S", "BO_Limite_O", "BO_PostProceso", "SM_SkySphere", "BO_Cam_Puerto_Restaurado"}
        n = 0
        for a in acts:
            lab = a.get_actor_label()
            if lab in SKIP or str(a.get_folder_path()) == "Lighting" or a.get_attach_parent_actor(): continue
            p = a.get_actor_location(); d = sh(p.x) - p.x
            if lab.startswith("TLP_Puerta_Escenario_Oeste"): d = A
            if d:
                a.set_actor_location(V(p.x + d, p.y, p.z), False, False); n += 1
        T = A + B + C
        for lab, w in (("BO_Agua", 15000.0), ("BO_Trigger_Agua", 15000.0), ("BO_Limite_N", 12700.0), ("BO_Limite_S", 12700.0)):
            a = L[lab]; p = a.get_actor_location(); s = a.get_actor_scale3d()
            a.set_actor_location(V(p.x + T / 2, p.y, p.z), False, False); a.set_actor_scale3d(V(s.x * (w + T + 2000) / w, s.y, s.z))
        mk = eas.spawn_actor_from_class(unreal.TargetPoint, V(0, -500, 0), R()); mk.set_actor_label("TLP_Expansion_Marca"); mk.set_folder_path("TLP/Logica")
        log("zonas separadas, actores movidos:", n)
    # ---------- 2. limpiar lo generado antes
    for a in eas.get_all_level_actors():
        lab = a.get_actor_label()
        if lab.startswith("TLP_Plat_") or lab.startswith("TLP_Enemigo_") or lab == "TLP_Charla_Enemigos":
            eas.destroy_actor(a)
    L = {a.get_actor_label(): a for a in eas.get_all_level_actors()}
    WOOD = L["BO_Pasarela_3_4"].static_mesh_component.get_material(0)
    ISLA = L["BO_Orilla_A"].static_mesh_component.get_material(0)
    ck0 = L["BO_Checkpoint_1"]; mk0 = L["BO_Checkpoint_1_Marca"]
    cnt = {}
    def name(a, kind, st):
        cnt[kind] = cnt.get(kind, 0) + 1
        a.set_actor_label(f"TLP_Plat_{st}_{kind}_{cnt[kind]}"); a.set_folder_path("TLP/Plataformas/" + st)
    def box(st, kind, x, y, ztop, Lx, Wy, mat, movable=False, thick=50.0, col=True):
        a = eas.spawn_actor_from_class(unreal.StaticMeshActor, V(x, y, ztop - thick / 2), R())
        c = a.static_mesh_component
        if movable: c.set_mobility(unreal.ComponentMobility.MOVABLE)
        c.set_static_mesh(CUBE); c.set_material(0, mat); a.set_actor_scale3d(V(Lx / 100, Wy / 100, thick / 100))
        if not col: c.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
        name(a, kind, st); return a
    def pilar(st, x, y, ztop):
        H = ztop - 50 + 60
        if H > 20:
            a = eas.spawn_actor_from_class(unreal.StaticMeshActor, V(x, y, -60 + H / 2), R())
            c = a.static_mesh_component; c.set_static_mesh(CUBE); c.set_material(0, WOOD); a.set_actor_scale3d(V(0.3, 0.3, H / 100))
            c.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION); name(a, "pilar", st)
    def overlap(a):
        c = a.static_mesh_component; c.set_mobility(unreal.ComponentMobility.MOVABLE)
        c.set_collision_profile_name("OverlapAllDynamic"); c.set_editor_property("generate_overlap_events", True)
    NE = [0]
    def enemigo(x, y, ztop, vel, vis, casa):
        a = eas.spawn_actor_from_class(ENE, V(x, y, ztop + 35), R())
        c = a.static_mesh_component; overlap(a); c.set_static_mesh(CUBE); c.set_material(0, M["MI_Enemigo"]); a.set_actor_scale3d(V(0.8, 0.8, 0.7))
        for k, v in (("Velocidad", float(vel)), ("RadioVision", float(vis)), ("RadioCasa", float(casa))): a.set_editor_property(k, v)
        NE[0] += 1; a.set_actor_label(f"TLP_Enemigo_{NE[0]}"); a.set_folder_path("TLP/Enemigos")
    def queso(st, x, y, ztop):
        q = eas.spawn_actor_from_class(VIDA, V(x, y, ztop + 70), R()); overlap(q)
        q.static_mesh_component.set_static_mesh(CYL); q.static_mesh_component.set_material(0, M["MI_Queso"]); q.set_actor_scale3d(V(0.6, 0.6, 0.3)); name(q, "queso", st)
    def movil(st, x, y, ztop, x2, y2, Lx, Wy, vel):
        p = box(st, "movil", x, y, ztop, Lx, Wy, M["MI_Movil"], movable=True)
        d = eas.spawn_actor_from_class(unreal.TargetPoint, V(x2, y2, ztop - 25), R()); name(d, "destino", st)
        mv = eas.spawn_actor_from_class(MOV, V(x, y, ztop + 100), R()); name(mv, "mover", st)
        mv.set_editor_property("Pieza", p); mv.set_editor_property("Destino", d); mv.set_editor_property("Vaiven", True); mv.set_editor_property("Velocidad", float(vel))
    # ---------- 3. tramos de plataformas
    for st, x0, x1, y, z, pat in STRETCH:
        els = gen(st, x0, x1, y, z, pat)
        log(st, "elementos", len(els) - 1, "salto max", round(max(e['gap'] for e in els)), [e['t'] for e in els])
        for k, e in enumerate(els):
            t = e['t']
            if t == 'fin': continue
            x, yy, zt, Lx, Wy = e['x'], e['y'], e['z'], e['L'], e['W']
            if t in ('p', 's', 'L', 'up', 'check', 'pel'):
                box(st, "plat", x, yy, zt, Lx, Wy, WOOD); pilar(st, x, yy, zt)
            if t == 'isla':
                box(st, "isla", x, yy, zt, Lx, Wy, ISLA); pilar(st, x - 300, yy, zt); pilar(st, x + 300, yy, zt)
                if e['n'] == 1: enemigo(x + 100, yy, zt, 200, 650, 300)
                else:
                    enemigo(x - 220, yy - 170, zt, 240, 650, 230); enemigo(x + 230, yy + 170, zt, 240, 650, 230)
                queso(st, x, yy + 300, zt)
            if t == 'check':
                c = eas.spawn_actor_from_class(CHK, V(x, yy, zt + 150), R()); c.set_actor_scale3d(ck0.get_actor_scale3d())
                c.set_actor_hidden_in_game(True); c.tags = [unreal.Name("Checkpoint")]; name(c, "checkpoint", st)
                mm = eas.spawn_actor_from_class(unreal.StaticMeshActor, V(x, yy, zt + 50), R())
                mm.static_mesh_component.set_static_mesh(mk0.static_mesh_component.static_mesh); mm.static_mesh_component.set_material(0, mk0.static_mesh_component.get_material(0))
                mm.set_actor_scale3d(mk0.get_actor_scale3d()); name(mm, "marca", st)
                queso(st, x + 130, yy + 130, zt)
            if t == 'mx': movil(st, x, yy, zt, e['x2'], yy, Lx, Wy, 1.1)
            if t == 'my': movil(st, x, yy, zt, x, e['y2'], Lx, Wy, 1.4)
            if t == 'fr':
                for j in range(3):
                    tb = eas.spawn_actor_from_class(TAB, V(x - 190 + 190 * j, yy, zt - 25), R())
                    c = tb.static_mesh_component; c.set_mobility(unreal.ComponentMobility.MOVABLE); c.set_static_mesh(CUBE); c.set_material(0, M["MI_Fragil"])
                    tb.set_actor_scale3d(V(1.9, Wy / 100, 0.5))
                    tb.set_editor_property("Retraso", 0.5); tb.set_editor_property("Reaparece", 3.0)
                    tb.set_editor_property("ZonaOffset", V(0, 0, 97)); tb.set_editor_property("ZonaExtent", V(100, Wy / 2 + 20, 40)); name(tb, "fragil", st)
            if t == 'pel':
                b = eas.spawn_actor_from_class(PEL, V(x, yy - 150, zt + 40), R(pitch=90)); overlap(b)
                b.static_mesh_component.set_static_mesh(CYL); b.static_mesh_component.set_material(0, M["MI_Peligro"]); b.set_actor_scale3d(V(0.8, 0.8, 1.4))
                for kk, vv in (("Mueve", True), ("PuntoB", V(0, 300, 0)), ("Periodo", 2.6), ("Desfase", 0.4 * k), ("Intermitente", False), ("FraccionEncendido", 0.5), ("Activo", True)): b.set_editor_property(kk, vv)
                name(b, "peligro", st)
    # ---------- 4. enemigos en las zonas
    for x, y, vel, vis, casa in ZONE_EN: enemigo(sh(x), y, 0, vel, vis, casa)
    log("enemigos", NE[0])
    a = eas.spawn_actor_from_class(CHARLA, V(500, 2450, 330), R())
    txt = "¡Bots de marketing! Te persiguen.\nSáltales encima para aplastarlos."
    a.set_editor_property("TextoAntes", txt); a.set_editor_property("TextoDespues", txt); a.set_editor_property("Meta", L["BO_Goal_P1"]); a.set_editor_property("Radio", 800.0)
    tr = a.get_editor_property("text_render"); tr.set_editor_property("text", txt); tr.set_editor_property("world_size", 26.0)
    tr.set_editor_property("horizontal_alignment", unreal.HorizTextAligment.EHTA_CENTER); tr.set_editor_property("text_render_color", unreal.Color(r=230, g=150, b=255, a=255))
    a.set_actor_hidden_in_game(True); a.set_actor_label("TLP_Charla_Enemigos"); a.set_folder_path("TLP/Charlas")
    unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
    log("Nivel guardado. total actores", len(eas.get_all_level_actors()))
    open(os.path.join(proj, "Saved", "tlp_en2.txt"), "w", encoding="utf-8").write("\n".join(LOG))
