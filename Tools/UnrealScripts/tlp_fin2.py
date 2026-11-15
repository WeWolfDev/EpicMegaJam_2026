# Fin paso 2: coloca quesos, charlas, puertas, final, pausa y ajusta etiquetas
import unreal, os
LOG=[]
def log(*a):
    s=" ".join(str(x) for x in a); LOG.append(s); unreal.log("[TLP] "+s)
eas=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
BPD="/Game/TheLastPatch/Blueprints"
def C(n): return unreal.load_asset(f"{BPD}/{n}").generated_class()
VIDA,CHARLA,FINAL,PAUSA=C("BP_TLP_Vida"),C("BP_TLP_Charla"),C("BP_TLP_Final"),C("BP_TLP_Pausa")
V=unreal.Vector
def R(yaw=0,pitch=0): return unreal.Rotator(roll=0,pitch=pitch,yaw=yaw)
CUBE=unreal.load_asset("/Engine/BasicShapes/Cube.Cube"); CYL=unreal.load_asset("/Engine/BasicShapes/Cylinder.Cylinder")
QUESO=unreal.load_asset("/Game/TheLastPatch/Blockout/MI_Queso")
# limpiar corrida anterior
for a in eas.get_all_level_actors():
    if a.get_class() in (VIDA,CHARLA,FINAL,PAUSA) or a.get_actor_label().startswith("TLP_Puerta_"):
        eas.destroy_actor(a)
L={a.get_actor_label():a for a in eas.get_all_level_actors()}
def need(n):
    a=L.get(n)
    if not a: log("FALTA",n)
    return a
def movable(a):
    if a and a.root_component: a.root_component.set_mobility(unreal.ComponentMobility.MOVABLE)
def tag(a,t):
    if a:
        tags=list(a.tags)
        if unreal.Name(t) not in tags: tags.append(unreal.Name(t)); a.tags=tags

# 1. Quesos (recuperar vidas)
for i,p in enumerate([(1450,3450,70),(2700,3000,70),(7000,4400,70),(9300,4500,70),(9300,700,70),(7300,1000,70),(4800,1000,70)]):
    q=eas.spawn_actor_from_class(VIDA,V(*p),R())
    c=q.static_mesh_component; c.set_mobility(unreal.ComponentMobility.MOVABLE)
    c.set_static_mesh(CYL); c.set_material(0,QUESO); q.set_actor_scale3d(V(0.6,0.6,0.3))
    c.set_collision_profile_name("OverlapAllDynamic"); c.set_editor_property("generate_overlap_events",True)
    q.set_actor_label(f"TLP_Queso_{i}"); q.set_folder_path("TLP/Vidas")
log("quesos 7")

# 2. Charlas
def charla(label,pos,antes,despues="",meta=None,radio=900.0,size=26.0,color=(255,235,170)):
    a=eas.spawn_actor_from_class(CHARLA,V(*pos),R())
    a.set_editor_property("TextoAntes",antes); a.set_editor_property("TextoDespues",despues or antes)
    if meta: a.set_editor_property("Meta",meta)
    a.set_editor_property("Radio",radio)
    t=a.get_editor_property("text_render")
    for k,v in (("horizontal_alignment",unreal.HorizTextAligment.EHTA_CENTER),("vertical_alignment",unreal.VerticalTextAligment.EVRTA_TEXT_BOTTOM),
                ("world_size",size),("text_render_color",unreal.Color(r=color[0],g=color[1],b=color[2],a=255))):
        try: t.set_editor_property(k,v)
        except Exception as ex: log("text prop",k,ex)
    t.set_editor_property("text",antes)
    a.set_actor_hidden_in_game(True)
    a.set_actor_label("TLP_Charla_"+label); a.set_folder_path("TLP/Charlas")
    return a
charla("Toto",(3800,4200,800),
 "TOTO: ¡Ratón! ¡Sácame de esta jaula!\nUsa el REBOTE del trampolín OG en el ascensor.",
 "TOTO: Pensé que me habían borrado.\nRATÓN: Lo intentaron. Nunca aprendieron a borrar bien.\nTOTO: Reparé la polea OG del corredor. ¡Pesca su TRACCIÓN!",
 need("BO_Goal_P1"),1300.0)
charla("Ascensor",(3000,3150,430),"Antes esto era un trampolín.\nAhora cuesta 4.99 saltar.",radio=700.0,color=(255,140,140))
charla("Paco",(10000,1000,330),
 "PACO: ¡Ratón! Estoy atrapado al otro lado del canal.\nLa grúa necesita TRACCIÓN para mover su plataforma.",
 "PACO: No me acuerdo de cuántos polígonos tenías.\nMe acuerdo de que volviste.\nAbrí el paso a la presentación: sigue la pasarela al oeste.",
 need("BO_Goal_P3"),2600.0,32.0)
charla("Escenario",(3900,1450,320),"Pista: TRACCIÓN al panel del escenario,\ny REBOTE a la plataforma de presentación.",radio=900.0,color=(170,230,255))

# 3. Toto habilita la Traccion: la polea aparece al liberar a Toto
for n in ("OMC_Source_Pull_Polea OG (fuente Traccion)","BO_Polea OG (fuente Traccion)","BO_Brillo_Polea"):
    a=need(n)
    if a: tag(a,"Restore_P1"); a.set_actor_hidden_in_game(True); log("polea bloqueada",n)

# 4. Puertas del escenario
ref=need("BO_Logo_Estudio"); mat=ref.static_mesh_component.get_material(0) if ref else None
def puerta(label,x,yaw,tags,texto):
    p=eas.spawn_actor_from_class(unreal.StaticMeshActor,V(x,1000,200),R())
    p.static_mesh_component.set_static_mesh(CUBE)
    if mat: p.static_mesh_component.set_material(0,mat)
    p.set_actor_scale3d(V(0.4,4.3,4.0)); p.tags=[unreal.Name(t) for t in tags]
    p.set_actor_label("TLP_Puerta_"+label); p.set_folder_path("TLP/Puertas")
    t=eas.spawn_actor_from_class(unreal.TextRenderActor,V(x+(26 if yaw==0 else -26),1000,250),R(yaw))
    tr=t.get_editor_property("text_render")
    tr.set_editor_property("text",texto); tr.set_editor_property("world_size",34.0)
    tr.set_editor_property("horizontal_alignment",unreal.HorizTextAligment.EHTA_CENTER)
    tr.set_editor_property("text_render_color",unreal.Color(r=255,g=255,b=255,a=255))
    t.tags=[unreal.Name(x_) for x_ in tags]; t.set_actor_label("TLP_Puerta_"+label+"_Texto"); t.set_folder_path("TLP/Puertas")
    log("puerta",label,x)
puerta("Escenario_Este",4350,0,["Ads_P3"],"CERRADO\nEvento privado del estudio")
puerta("Escenario_Oeste",1450,180,[],"ACCESO SOLO VIP")

# 5. Revelacion: al entrar al escenario aparece la nueva mascota
fr=need("BO_Finale_Reveal")
if fr:
    fr.set_editor_property("TagAnuncios",unreal.Name("Nada_Final")); fr.set_editor_property("TagRestaurar",unreal.Name("Mascot"))
    fr.set_editor_property("Mensaje","¡Les presentamos a la NUEVA mascota de la saga! ...¿Y tú quién eras?")
for n in ("BO_Nueva mascota","BO_Toto","BO_Paco"): movable(need(n))

# 6. Controlador del final
f=eas.spawn_actor_from_class(FINAL,V(2600,1000,700),R()); f.set_actor_label("TLP_Final"); f.set_folder_path("TLP/Logica")
for k,n in (("Plataforma","OMC_Receiver_Bounce_Plataforma_Presentacion"),("Revelacion","BO_Finale_Reveal"),("Mascota","BO_Nueva mascota"),
            ("Destino","BO_Mascota_Vuelo_Fin"),("Camara","BO_Cam_Final"),("Toto","BO_Toto"),("Paco","BO_Paco"),
            ("PuntoRaton","BO_Ending_Raton"),("PuntoToto","BO_Ending_Toto"),("PuntoPaco","BO_Ending_Paco")):
    a=need(n)
    if a: f.set_editor_property(k,a)
cam=need("BO_Cam_Final")
if cam:
    cam.set_actor_rotation(unreal.MathLibrary.find_look_at_rotation(cam.get_actor_location(),V(500,235,130)),False)

# 7. Pausa
p=eas.spawn_actor_from_class(PAUSA,V(500,300,400),R()); p.set_actor_label("TLP_Pausa"); p.set_folder_path("TLP/Logica")
try: p.set_editor_property("auto_receive_input",unreal.AutoReceiveInput.PLAYER0); log("pausa input",p.get_editor_property("auto_receive_input"))
except Exception as ex: log("auto input ERROR",ex)

fl=L.get("Floor")
if fl:
    o,e=fl.get_actor_bounds(False); log("Floor top z", o.z+e.z)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
log("Nivel guardado")
open(os.path.join(unreal.Paths.project_saved_dir(),"tlp_fin2.txt"),"w",encoding="utf-8").write("\n".join(LOG))
