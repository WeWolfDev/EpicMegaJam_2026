# Coloca la pelea contra el lobo en el escenario de L_Puerto
import unreal, os
LOG=[]
def log(*a):
    s=" ".join(str(x) for x in a); LOG.append(s); unreal.log("[TLP] "+s)
eas=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
V=unreal.Vector
def R(yaw=0,pitch=0): return unreal.Rotator(roll=0,pitch=pitch,yaw=yaw)
BPD="/Game/TheLastPatch/Blueprints"
def C(n): return unreal.load_asset(n).generated_class()
JEFE,FOCO,ENE=C(f"{BPD}/BP_TLP_Jefe"),C(f"{BPD}/BP_TLP_Foco"),C(f"{BPD}/BP_TLP_Enemigo")
CUBE=unreal.load_asset("/Engine/BasicShapes/Cube.Cube"); CYL=unreal.load_asset("/Engine/BasicShapes/Cylinder.Cylinder")
MB="/Game/TheLastPatch/Blockout/"
M={n:unreal.load_asset(MB+n) for n in ("MI_Peligro","MI_Electrico","MI_Enemigo")}
KW=unreal.AttachmentRule.KEEP_WORLD; SR=unreal.AttachmentRule.SNAP_TO_TARGET; DK=unreal.DetachmentRule.KEEP_WORLD
# limpiar corrida anterior
for a in eas.get_all_level_actors():
    if a.get_actor_label().startswith("TLP_Jefe_") or a.get_class() in (JEFE,FOCO):
        eas.destroy_actor(a)
import re
ORIG=("OMC_Receiver_Bounce_Plataforma_Presentacion","OMC_Receiver_Pull_Panel_Cierre","OMC_Source_Bounce_Trampolin_OG","BO_Trampolin_OG","OMC_Source_Pull_Polea OG (fuente Traccion)","BO_Polea OG (fuente Traccion)")
for a in eas.get_all_level_actors():
    l=a.get_actor_label()
    for o in ORIG:
        if l!=o and re.fullmatch(re.escape(o)+r"\d+",l): eas.destroy_actor(a); log("borrado resto",l)
L={a.get_actor_label():a for a in eas.get_all_level_actors()}
def need(n):
    a=L.get(n)
    if not a: log("FALTA",n)
    return a
def lab(a,n,folder="TLP/Jefe"):
    a.set_actor_label("TLP_Jefe_"+n); a.set_folder_path(folder); return a
def box(n,mesh,mat,loc,scale,col=True):
    a=eas.spawn_actor_from_class(unreal.StaticMeshActor,loc,R())
    c=a.static_mesh_component; c.set_mobility(unreal.ComponentMobility.MOVABLE); c.set_static_mesh(mesh)
    if mat: c.set_material(0,mat)
    a.set_actor_scale3d(scale)
    if not col: c.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
    return lab(a,n)
def dup(src,n,loc,keep_tags=False,hidden=False):
    a=eas.duplicate_actor(src,None,V(0,0,0))
    if a.get_attach_parent_actor(): a.detach_from_actor(DK,DK,DK)
    a.set_actor_location(loc,False,False)
    if not keep_tags: a.tags=[]
    a.set_actor_hidden_in_game(hidden)
    return lab(a,n)
def tp(n,loc):
    t=eas.spawn_actor_from_class(unreal.TargetPoint,loc,R()); return lab(t,n)
# ---- puntos
pA=tp("PuntoA",V(7800,1000,50)); pB=tp("PuntoB",V(8100,1650,50)); pP=tp("PuntoPodio",V(7450,380,250)); pE=tp("Expositor",V(7200,1700,150))
# ---- geometria nueva
plat=need("BO_Plataforma_Presentacion"); pmat=plat.static_mesh_component.get_material(0) if plat else None
box("PlataformaB",CUBE,pmat,V(8100,1650,25),V(3,3,0.5))
podmat=need("BO_Escenario").static_mesh_component.get_material(0)
box("Podio",CUBE,pmat,V(7450,380,125),V(3,3,2.5))
box("Palanca_Base",CYL,M["MI_Electrico"],V(8200,380,50),V(0.6,0.6,1.0))
fj=box("FocoTecho",CUBE,M["MI_Electrico"],V(7450,380,560),V(1.4,1.4,0.6),col=False)
# ---- receptores y fuentes
rA=need("OMC_Receiver_Bounce_Plataforma_Presentacion")
rB=dup(rA,"Receptor_PlataformaB",V(8100,1650,50))
rP=dup(need("OMC_Receiver_Pull_Panel_Cierre"),"Receptor_Palanca",V(8200,380,110))
dummy=dup(rA,"Receptor_Inerte",V(8100,-600,-600),hidden=True)
for n,(dx,dy) in (("OMC_Source_Bounce_Trampolin_OG",(9000,380)),("BO_Trampolin_OG",(9000,380)),("OMC_Source_Pull_Polea OG (fuente Traccion)",(9000,1650)),("BO_Polea OG (fuente Traccion)",(9000,1650))):
    s=need(n)
    if s:
        z=s.get_actor_location().z; d=dup(s,"Fuente_"+("Rebote" if "Trampolin" in n else "Traccion")+("_Pieza" if n.startswith("BO_") else ""),V(dx,dy,z))
# ---- lobo
sk=unreal.load_asset("/Game/TheLastPatch/Personajes/Lobo/SK_Lobo")
lobo=eas.spawn_actor_from_class(unreal.SkeletalMeshActor,V(7800,1000,50),R())
lc=lobo.skeletal_mesh_component; lc.set_editor_property("skeletal_mesh_asset",sk) if hasattr(lc,"skeletal_mesh_asset") else None
try: lc.set_skeletal_mesh_asset(sk)
except Exception as ex: log("set mesh",ex)
lc.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION); lc.set_mobility(unreal.ComponentMobility.MOVABLE)
lobo.tags=[unreal.Name("Mascot")]; lobo.set_actor_hidden_in_game(True); lab(lobo,"Lobo")
gl=eas.spawn_actor_from_class(unreal.StaticMeshActor,V(7800,1000,200),R())
gc=gl.static_mesh_component; gc.set_mobility(unreal.ComponentMobility.MOVABLE); gc.set_static_mesh(unreal.load_asset("/Game/TheLastPatch/Personajes/Lobo/SM_Lobo_Glasses")); gc.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
gl.attach_to_actor(lobo,"GlassesSocket",SR,SR,SR,False)
gl.tags=[unreal.Name("Mascot")]; gl.set_actor_hidden_in_game(True); lab(gl,"Lentes")
log("lobo",lobo.get_actor_location(),"lentes",gl.get_actor_location())
# ---- textos
def tset(a,text,size,col):
    t=a.get_editor_property("text_render")
    t.set_editor_property("text",text); t.set_editor_property("world_size",size)
    t.set_editor_property("horizontal_alignment",unreal.HorizTextAligment.EHTA_CENTER)
    t.set_editor_property("vertical_alignment",unreal.VerticalTextAligment.EVRTA_TEXT_BOTTOM)
    t.set_editor_property("text_render_color",unreal.Color(r=col[0],g=col[1],b=col[2],a=255))
j=eas.spawn_actor_from_class(JEFE,V(7800,1000,300),R()); tset(j,"",26.0,(255,235,170)); lab(j,"Controlador","TLP/Logica")
bar=eas.spawn_actor_from_class(unreal.TextRenderActor,V(7800,1000,345),R()); tset(bar,"LOBO   [ ### ]",36.0,(255,80,80)); lab(bar,"Barra")
bar.attach_to_actor(j,"",KW,KW,KW,False)
for a in (j,bar): a.tags=[unreal.Name("Mascot")]; a.set_actor_hidden_in_game(True)
for k,v in (("Lobo",lobo),("Barra",bar),("Revelacion",need("BO_Finale_Reveal")),("PlatA",rA),("PlatB",rB),("Palanca",rP),("FocoJefe",fj),
            ("PuntoA",pA),("PuntoB",pB),("PuntoPodio",pP),("Expositor",pE),("Final",need("TLP_Final"))):
    try: j.set_editor_property(k,v)
    except Exception as ex: log("jefe prop",k,ex)
j.set_editor_property("Linea","")
# ---- focos de ataque
def foco(n,tag,per,des):
    f=eas.spawn_actor_from_class(FOCO,V(8000,1000,560),R())
    c=f.static_mesh_component; c.set_mobility(unreal.ComponentMobility.MOVABLE); c.set_static_mesh(CUBE); c.set_material(0,M["MI_Electrico"])
    f.set_actor_scale3d(V(1.2,1.2,0.6)); c.set_collision_profile_name("OverlapAllDynamic"); c.set_editor_property("generate_overlap_events",True)
    s=box("Sombra_"+n,CYL,M["MI_Peligro"],V(8000,1000,3),V(1.5,1.5,0.02),col=False); s.set_actor_hidden_in_game(True)
    for k,v in (("Activo",False),("Periodo",per),("Desfase",des),("Sombra",s),("MinXY",V(6950,100,0)),("MaxXY",V(9150,1900,0))): f.set_editor_property(k,v)
    f.tags=[unreal.Name(tag)]; f.set_actor_hidden_in_game(True); lab(f,"Foco_"+n)
foco("1","FocoF2",3.2,0.0); foco("2","FocoF2",3.2,1.6); foco("3","FocoF3",2.6,0.8); foco("4","FocoF3",2.6,2.1)
# ---- bots por fase
for i,(x,y,f) in enumerate(((8700,350,1),(8700,1650,1),(8300,500,2),(8300,1500,2),(8650,1000,3),(7950,450,3),(8800,1700,3))):
    e=eas.spawn_actor_from_class(ENE,V(x,y,35),R())
    c=e.static_mesh_component; c.set_mobility(unreal.ComponentMobility.MOVABLE); c.set_static_mesh(CUBE); c.set_material(0,M["MI_Enemigo"])
    c.set_collision_profile_name("OverlapAllDynamic"); c.set_editor_property("generate_overlap_events",True); e.set_actor_scale3d(V(0.8,0.8,0.7))
    for k,v in (("Velocidad",260.0),("RadioVision",1000.0),("RadioCasa",700.0),("Muerto",True)): e.set_editor_property(k,v)
    e.tags=[unreal.Name(f"Bot_F{f}"),unreal.Name("Bot_Jefe")]; e.set_actor_hidden_in_game(True); e.set_actor_enable_collision(False)
    lab(e,f"Bot_{i+1}")
# ---- ajustes del final existente
nm=need("BO_Nueva mascota")
if nm: nm.tags=[t for t in nm.tags if str(t)!="Mascot"]; nm.set_actor_hidden_in_game(True)
fin=need("TLP_Final")
if fin: fin.set_editor_property("Plataforma",dummy)
fr=need("BO_Finale_Reveal")
if fr: fr.set_editor_property("Mensaje","El lobo, nueva mascota de la saga, sube al escenario!")
ch=need("TLP_Charla_Escenario")
if ch:
    tx="Pesca REBOTE y TRACCION de las piezas OG del escenario\ny usalas contra el lobo."
    ch.set_editor_property("TextoAntes",tx); ch.set_editor_property("TextoDespues",tx)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
log("Nivel guardado. actores", len(eas.get_all_level_actors()))
open(os.path.join(unreal.Paths.project_saved_dir(),"tlp_jefe2.txt"),"w",encoding="utf-8").write("\n".join(LOG))
