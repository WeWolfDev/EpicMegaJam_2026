# Pruebas en PIE. Usar: S='a'; exec(...)   pasos: a b c d e f g rep
import unreal, os
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
out=os.path.join(unreal.Paths.project_saved_dir(),"tlp_tf.txt")
def W(*a): open(out,"a",encoding="utf-8").write(" ".join(str(x) for x in a)+"\n")
if w is None:
    W("NO PIE"); raise SystemExit
acts=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor)
L={a.get_actor_label():a for a in acts}
cn=lambda n: next(a for a in acts if a.get_class().get_name()==n)
pc=unreal.GameplayStatics.get_player_character(w,0)
resp=cn("BP_TLP_Respawn_C"); fin=cn("BP_TLP_Final_C"); pau=cn("BP_TLP_Pausa_C")
def loc(a): v=a.get_actor_location(); return f"({v.x:.0f},{v.y:.0f},{v.z:.0f})"
def go(n,dz=100):
    v=L[n].get_actor_location(); pc.set_actor_location(unreal.Vector(v.x,v.y,v.z+dz),False,True)
def st(): 
    return f"vidas={resp.get_editor_property('Vidas')} raton={loc(pc)} estado={fin.get_editor_property('Estado')} fin={fin.get_editor_property('Fin')}"
S=globals().get("S","rep")
W("== paso",S)
if S=="a":   # vidas: perder 3 -> vuelve a 3
    for i in range(3):
        resp.call_method("PerderVida"); W(" perder",i+1,st())
    resp.set_editor_property("Vidas",1); go("TLP_Queso_0",0); W(" en queso 0",st())
elif S=="b":
    q=L["TLP_Queso_0"]; W(" queso0 oculto",q.get_editor_property("hidden"),st())
    p=L["OMC_Source_Pull_Polea OG (fuente Traccion)"]; W(" polea oculta",p.get_editor_property("hidden"),"col",p.get_actor_enable_collision())
    go("BO_Goal_P1",0)
elif S=="c":
    p=L["OMC_Source_Pull_Polea OG (fuente Traccion)"]; W(" tras P1 polea oculta",p.get_editor_property("hidden"),"col",p.get_actor_enable_collision())
    ch=L["TLP_Charla_Toto"]; W(" charla toto oculta",ch.get_editor_property("hidden"),"texto:",ch.get_editor_property("text_render").get_editor_property("text"))
    g=L["OMC_Receiver_Pull_Grua_Plataforma"]; g.set_editor_property("VersionState",unreal.Name("Hybrid"))
    W(" grua -> Hybrid; plataforma",loc(L["BO_Grua_Plataforma"]))
elif S=="d":
    W(" grua tras 3s",loc(L["BO_Grua_Plataforma"]))
    L["OMC_Receiver_Pull_Grua_Plataforma"].call_method("ResetObject")
    W(" grua quitado poder ->",L["OMC_Receiver_Pull_Grua_Plataforma"].get_editor_property("VersionState"))
    go("BO_Goal_P3",0)
elif S=="e":
    W(" grua tras quitar 3s",loc(L["BO_Grua_Plataforma"]))
    pe=L["TLP_Puerta_Escenario_Este"]; W(" puerta este oculta",pe.get_editor_property("hidden"),"col",pe.get_actor_enable_collision())
    ch=L["TLP_Charla_Paco"]; W(" charla paco:",ch.get_editor_property("text_render").get_editor_property("text"))
    go("BO_Finale_Reveal",-150)
elif S=="f":
    m=L["BO_Nueva mascota"]; W(" mascota oculta",m.get_editor_property("hidden"),loc(m))
    L["OMC_Receiver_Bounce_Plataforma_Presentacion"].set_editor_property("VersionState",unreal.Name("Hybrid"))
    W(" plataforma -> Hybrid",st())
elif S=="g":
    m=L["BO_Nueva mascota"]; W(" mascota",loc(m),st())
    W(" toto",loc(L["BO_Toto"]),"paco",loc(L["BO_Paco"]),"mural oculto",L["BO_Mural_Final"].get_editor_property("hidden"),"pausa.finjuego",pau.get_editor_property("FinJuego"))
elif S=="h":
    resp.call_method("PerderVida"); W(" perdi 1",st()); go("TLP_Queso_1",0)
elif S=="i":
    W(" queso1 oculto",L["TLP_Queso_1"].get_editor_property("hidden"),st())
else:
    W(st())
