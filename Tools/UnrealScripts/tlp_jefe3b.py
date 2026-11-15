# Banderas, quesos, jaulas, Paco, bote, puerta del jefe y luces del escenario
import unreal, os
LOG=[]
def log(*a):
    s=" ".join(str(x) for x in a); LOG.append(s); unreal.log("[TLP3] "+s)
eas=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
V=unreal.Vector
def R(yaw=0): return unreal.Rotator(roll=0,pitch=0,yaw=yaw)
BPD="/Game/TheLastPatch/Blueprints"; P="/Game/TheLastPatch/Props/"
def C(n): return unreal.load_asset(n).generated_class()
BAND,NPC=C(f"{BPD}/BP_TLP_Bandera"),C(f"{BPD}/BP_TLP_NPCAnim")
MV=unreal.ComponentMobility.MOVABLE; NOC=unreal.CollisionEnabled.NO_COLLISION
KW=unreal.AttachmentRule.KEEP_WORLD
ROJA=unreal.load_asset(P+"Bandera_Roja/SM_Bandera_Roja"); VERDE=unreal.load_asset(P+"Bandera_Verde/SM_Bandera_Verde")
BOTE=unreal.load_asset(P+"Bote/SM_Bote"); QUESO=unreal.load_asset(P+"Queso/SM_Queso"); JAULA=unreal.load_asset(P+"Jaula/SM_Jaula")
# colision simple (caja) para los props que la necesitan
sme=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
for m in (BOTE,QUESO,JAULA):
    try:
        if sme.get_simple_collision_count(m)==0: sme.add_simple_collisions(m,unreal.ScriptCollisionShapeType.BOX); unreal.EditorAssetLibrary.save_loaded_asset(m)
        log("colision",m.get_name(),sme.get_simple_collision_count(m))
    except Exception as ex: log("colision ERR",m.get_name(),ex)
# limpiar corrida anterior
for a in eas.get_all_level_actors():
    l=a.get_actor_label()
    if l.startswith("TLP3_") or a.get_class() in (BAND,NPC): eas.destroy_actor(a)
L={a.get_actor_label():a for a in eas.get_all_level_actors()}
def need(n):
    a=L.get(n)
    if not a: log("FALTA",n)
    return a
def lab(a,n,folder="TLP/Arte"):
    a.set_actor_label("TLP3_"+n); a.set_folder_path(folder); return a
def bottom(a):
    o,e=a.get_actor_bounds(False); return o.z-e.z
def fit_center(a,o_target,z_bottom=None):
    o,e=a.get_actor_bounds(False); loc=a.get_actor_location()
    nz=loc.z+(o_target.z-o.z) if z_bottom is None else loc.z+(z_bottom-(o.z-e.z))
    a.set_actor_location(V(loc.x+(o_target.x-o.x),loc.y+(o_target.y-o.y),nz),False,False)
def setmesh(a,mesh):
    c=a.static_mesh_component; c.set_mobility(MV); c.set_static_mesh(mesh)
    for i in range(c.get_num_materials()): c.set_material(i,None)
    try: c.set_editor_property("override_materials",[])
    except Exception: pass
    return c
# ---- banderas de checkpoint
marcas=[l for l in L if (l.startswith("BO_Checkpoint_") and l.endswith("_Marca")) or l.startswith("TLP_Plat_") and "_marca_" in l]
for l in sorted(marcas):
    m=L[l]; o,e=m.get_actor_bounds(False)
    b=eas.spawn_actor_from_class(BAND,V(o.x,o.y,o.z),R())
    c=setmesh(b,ROJA); c.set_collision_enabled(NOC)
    b.set_editor_property("MallaVerde",VERDE); b.set_editor_property("Radio",320.0)
    fit_center(b,V(o.x,o.y,0),z_bottom=o.z-e.z)
    m.set_actor_hidden_in_game(True); m.set_is_temporarily_hidden_in_editor(True); m.set_actor_enable_collision(False)
    lab(b,"Bandera_"+l)
log("banderas",len(marcas))
# ---- quesos de vida
n=0
for a in list(L.values()):
    if a.get_class().get_name()=="BP_TLP_Vida_C":
        o,e=a.get_actor_bounds(False)
        c=setmesh(a,QUESO); a.set_actor_scale3d(V(0.7,0.7,0.7)); fit_center(a,o); n+=1
log("quesos",n)
# ---- bote
bar=need("BO_Barca")
if bar:
    o,e=bar.get_actor_bounds(False); setmesh(bar,BOTE)
    yaw=90 if e.y>e.x else 0
    bar.set_actor_rotation(R(yaw),False); s=max(e.x,e.y)/95.0; bar.set_actor_scale3d(V(s,s,s)); fit_center(bar,o,z_bottom=o.z-e.z-40)
    log("bote",bar.get_actor_bounds(False))
# ---- jaula de Toto
jt=need("BO_Jaula_Toto")
if jt:
    o,e=jt.get_actor_bounds(False); setmesh(jt,JAULA); jt.set_actor_scale3d(V(e.x/40.0,e.y/40.3,e.z/47.6)); fit_center(jt,o)
    log("jaula toto",jt.get_actor_bounds(False),jt.tags)
# ---- Paco
bp=need("BO_Paco"); sk=unreal.load_asset("/Game/TheLastPatch/Personajes/Paco/SK_Paco")
paco=None
if bp and sk:
    o,e=bp.get_actor_bounds(False)
    paco=eas.spawn_actor_from_class(unreal.SkeletalMeshActor,V(o.x,o.y,o.z-e.z),bp.get_actor_rotation())
    pc=paco.skeletal_mesh_component; pc.set_mobility(MV)
    try: pc.set_skeletal_mesh_asset(sk)
    except Exception: pc.set_editor_property("skeletal_mesh_asset",sk)
    pc.set_collision_enabled(NOC); pc.set_animation_mode(unreal.AnimationMode.ANIMATION_SINGLE_NODE)
    po,pe=paco.get_actor_bounds(False); off=paco.get_actor_location().z-(po.z-pe.z)
    fit_center(paco,V(o.x,o.y,0),z_bottom=o.z-e.z)
    paco.tags=[unreal.Name("NPC_Paco")]; lab(paco,"Paco","TLP/Personajes")
    bp.set_actor_hidden_in_game(True); bp.set_is_temporarily_hidden_in_editor(True); bp.set_actor_enable_collision(False)
    log("paco",paco.get_actor_location(),"pivote sobre suelo",off)
    # jaula sobre Paco
    jp=eas.spawn_actor_from_class(unreal.StaticMeshActor,V(o.x,o.y,0),R())
    setmesh(jp,JAULA); jp.set_actor_scale3d(V(1.9,1.9,1.9)); fit_center(jp,V(o.x,o.y,0),z_bottom=o.z-e.z)
    jp.tags=[unreal.Name("Ads_P3")]; lab(jp,"Jaula_Paco")
    # animaciones
    A="/Game/TheLastPatch/Personajes/Paco/Anims/A_Paco_"
    an=eas.spawn_actor_from_class(NPC,V(o.x,o.y,o.z+200),R()); lab(an,"Paco_Anim","TLP/Logica")
    for k,v in (("Personaje",paco),("Meta",need("BO_Goal_P3")),("AnimAntes",unreal.load_asset(A+"Trapped_Idle")),("AnimLiberado",unreal.load_asset(A+"Freed_Celebrate")),("AnimDespues",unreal.load_asset(A+"Idle"))):
        try: an.set_editor_property(k,v)
        except Exception as ex: log("npc prop",k,ex)
        if v is None: log("FALTA anim",k)
    try: pc.set_editor_property("animation_data",unreal.SingleAnimationPlayData(anim_to_play=unreal.load_asset(A+"Trapped_Idle"),saved_looping=True,saved_playing=True))
    except Exception as ex: log("animdata",ex)
    fin=need("TLP_Final")
    if fin:
        try: fin.set_editor_property("Paco",paco); log("final paco ok")
        except Exception as ex: log("final paco",ex)
    ep=need("BO_Ending_Paco")
    if ep: l0=ep.get_actor_location(); ep.set_actor_location(V(l0.x,l0.y,-40.0+off),False,False)
# ---- puerta del jefe
pu=need("TLP_Puerta_Escenario_Este"); pt=need("TLP_Puerta_Escenario_Este_Texto"); j=need("TLP_Jefe_Controlador")
if pu:
    pu.tags=[]; pu.static_mesh_component.set_mobility(MV)
    if pt: pt.tags=[]; pt.get_editor_property("text_render").set_mobility(MV); pt.attach_to_actor(pu,"",KW,KW,KW,False)
    if j:
        cl=pu.get_actor_location()
        for k,v in (("Puerta",pu),("PuertaCerrada",cl),("PuertaAbierta",V(cl.x,cl.y,cl.z+420)),("MetaP3",need("BO_Goal_P3")),("BaseA",V(7800,1000,50)),("BaseB",V(7800,1000,50)),("S",1.0)):
            try: j.set_editor_property(k,v)
            except Exception as ex: log("jefe prop",k,ex)
        log("puerta ok",cl)
fr=need("BO_Finale_Reveal")
if fr: l0=fr.get_actor_location(); fr.set_actor_location(V(8900,l0.y,l0.z),False,False)
# ---- luces que se encienden con la presentacion
for i in range(4):
    f=need(f"BO_Foco_{i}")
    if f:
        f.tags=list(f.tags)+[unreal.Name("Mascot")]; f.set_actor_hidden_in_game(True)
for i,(x,y) in enumerate(((7300,500),(7300,1500),(8100,500),(8100,1500),(8900,500),(8900,1500))):
    pl=eas.spawn_actor_from_class(unreal.PointLight,V(x,y,560),R())
    c=pl.point_light_component; c.set_mobility(MV)
    c.set_editor_property("intensity_units",unreal.LightUnits.CANDELAS); c.set_intensity(2500.0)
    c.set_attenuation_radius(1600.0); c.set_light_color(unreal.LinearColor(1.0,0.9,0.75,1.0)); c.set_cast_shadows(False)
    pl.tags=[unreal.Name("Mascot")]; pl.set_actor_hidden_in_game(True); lab(pl,f"Luz_{i+1}","TLP/Jefe")
log("actores",len(eas.get_all_level_actors()))
open(r"C:/Proyectos/EpicMegaJam_2026/Saved/tlp_jefe3b.txt","w",encoding="utf-8").write("\n".join(LOG))
