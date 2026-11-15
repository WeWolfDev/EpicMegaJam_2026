import unreal, os
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
out=os.path.join(unreal.Paths.project_saved_dir(),"tlp_te.txt")
def W(*a): open(out,"a",encoding="utf-8").write(" ".join(str(x) for x in a)+"\n")
acts=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor)
L={a.get_actor_label():a for a in acts}
pc=unreal.GameplayStatics.get_player_character(w,0)
resp=next(a for a in acts if a.get_class().get_name()=="BP_TLP_Respawn_C")
ens=[a for a in acts if a.get_class().get_name()=="BP_TLP_Enemigo_C"]
def near(x,y): return min(ens,key=lambda a:(a.get_actor_location().x-x)**2+(a.get_actor_location().y-y)**2)
def loc(a): v=a.get_actor_location(); return f"({v.x:.0f},{v.y:.0f},{v.z:.0f})"
def tp(x,y,z): pc.set_actor_location(unreal.Vector(x,y,z),False,True)
def st(): return f"vidas={resp.get_editor_property('Vidas')} raton={loc(pc)}"
S=globals().get("S","rep"); W("== paso",S)
E1=near(500,2750); E2=near(7900,3950)
if S=="a":
    W(" enemigos",len(ens)); tp(500,2250,150); W(" E1 antes",loc(E1),st())
elif S=="b":
    W(" E1 a 1.5s (debe acercarse al raton)",loc(E1),st())
elif S=="c":
    W(" E1 tras contacto",loc(E1),"muerto",E1.get_editor_property("Muerto"),st())
    v=E2.get_actor_location(); tp(v.x,v.y,v.z+260); W(" sobre E2",loc(E2),st())
elif S=="d":
    W(" E2 muerto",E2.get_editor_property("Muerto"),"oculto",E2.get_editor_property("hidden"),st())
    pc.get_component_by_class(unreal.CharacterMovementComponent).set_editor_property("braking_deceleration_falling",0.0); tp(19824,4200,95); pc.launch_character(unreal.Vector(450,0,560),True,True); W(" salto largo S3 desde 19824 -> plataforma 20193..20513")
elif S=="e":
    W(" tras salto largo",st())
    m=L["TLP_Plat_S1_movil_1"]; v=m.get_actor_location(); tp(v.x,v.y,v.z+120); W(" sobre movil S1",loc(m),st())
elif S=="f":
    m=L["TLP_Plat_S1_movil_1"]; W(" movil 3s despues",loc(m),st())
else: W(st())
