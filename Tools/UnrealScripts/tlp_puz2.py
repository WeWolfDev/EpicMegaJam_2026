# Puzzles paso 2: coloca movedores y metas en L_Puerto
import unreal, os
LOG = []
def log(*a):
    s = " ".join(str(x) for x in a); LOG.append(s); unreal.log("[TLP] " + s)

eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
BPDIR = "/Game/TheLastPatch/Blueprints"
mover_c = unreal.load_asset(f"{BPDIR}/BP_TLP_Mover").generated_class()
meta_c = unreal.load_asset(f"{BPDIR}/BP_TLP_Meta").generated_class()

actors = eas.get_all_level_actors()
for a in actors:
    if a.get_class() == mover_c:
        eas.destroy_actor(a)
actors = eas.get_all_level_actors()
L = {a.get_actor_label(): a for a in actors}
def by_tag(t):
    return next((a for a in actors if unreal.Name(t) in a.tags), None)
KW = unreal.AttachmentRule.KEEP_WORLD

def movable(a):
    a.root_component.set_mobility(unreal.ComponentMobility.MOVABLE)

def mover(nombre, pieza, receptor, destino, extras=(), inicio=None, vaiven=False):
    p = L.get(pieza); r = L.get(receptor); d = by_tag(destino)
    if not p or not d:
        log("FALTA", nombre, pieza, p, destino, d); return
    movable(p)
    for e in extras:
        if L.get(e):
            movable(L[e]); L[e].attach_to_actor(p, "", KW, KW, KW, False)
    if r:
        r.attach_to_actor(p, "", KW, KW, KW, False)
    if inicio:
        s = by_tag(inicio)
        if s:
            p.set_actor_location(s.get_actor_location(), False, False)
    m = eas.spawn_actor_from_class(mover_c, p.get_actor_location(), unreal.Rotator(0, 0, 0))
    m.set_actor_label("TLP_Mover_" + nombre); m.set_folder_path("TLP/Puzzles")
    m.set_editor_property("Pieza", p)
    m.set_editor_property("Destino", d)
    if r: m.set_editor_property("Receptor", r)
    m.set_editor_property("Vaiven", vaiven)
    log("Mover", nombre, "pieza", pieza, "receptor", receptor if r else None, "destino", d.get_actor_label(),
        "desde", p.get_actor_location(), "hasta", d.get_actor_location())

mover("P1_Ascensor", "BO_Ascensor_Plataforma", "OMC_Receiver_Bounce_Ascensor_Plataforma", "Move_Ascensor_End",
      extras=["BO_Ascensor_Marca"], inicio="Move_Ascensor_Start", vaiven=True)
mover("P2_Valla", "BO_Valla_Publicitaria", "OMC_Receiver_Pull_Valla_Publicitaria", "Move_Valla_End")
mover("P3_Grua", "BO_Grua_Plataforma", "OMC_Receiver_Pull_Grua_Plataforma", "Move_Grua_End")
mover("Final_Panel", "BO_Panel_Cierre", "OMC_Receiver_Pull_Panel_Cierre", "Move_Panel_End")

# ---- Metas
metas = {
    "BO_Goal_P1": ("Ads_P1", "Restore_P1", "Toto es libre! El taller OG vuelve al puerto."),
    "BO_Goal_P2": ("Ads_P2", "Restore_P2", "Los faroles OG vuelven a iluminar el corredor."),
    "BO_Goal_P3": ("Ads_P3", "Restore_P3", "Puente restaurado: las banderolas vuelven al puerto."),
    "BO_Finale_Reveal": ("Ads_Final", "Restore_Final", "El puerto recupera su esencia. Director's Cut!"),
}
for lab, (ta, tr, msg) in metas.items():
    old = L.get(lab)
    if not old:
        log("FALTA meta", lab); continue
    if old.get_class() == meta_c:
        n = old
    else:
        bc = old.get_component_by_class(unreal.BoxComponent)
        ext = bc.get_editor_property("box_extent") if bc else unreal.Vector(32, 32, 32)
        loc, rot, scl, tags, folder = old.get_actor_location(), old.get_actor_rotation(), old.get_actor_scale3d(), list(old.tags), old.get_folder_path()
        eas.destroy_actor(old)
        n = eas.spawn_actor_from_class(meta_c, loc, rot)
        n.set_actor_scale3d(scl)
        n.get_component_by_class(unreal.BoxComponent).set_editor_property("box_extent", ext)
        n.tags = tags; n.set_actor_label(lab); n.set_folder_path(folder)
    n.set_editor_property("TagAnuncios", unreal.Name(ta))
    n.set_editor_property("TagRestaurar", unreal.Name(tr))
    n.set_editor_property("Mensaje", msg)
    na = len([a for a in eas.get_all_level_actors() if unreal.Name(ta) in a.tags])
    nr = len([a for a in eas.get_all_level_actors() if unreal.Name(tr) in a.tags])
    log("Meta", lab, ta, na, "anuncios |", tr, nr, "piezas OG")

unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
log("Nivel guardado")
open(os.path.join(unreal.Paths.project_saved_dir(), "tlp_puz2.txt"), "w", encoding="utf-8").write("\n".join(LOG))
