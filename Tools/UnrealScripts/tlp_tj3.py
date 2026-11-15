# Prueba PIE: puerta, banderas, Paco, luces y movimiento del lobo
import unreal, os
out=r"C:/Proyectos/EpicMegaJam_2026/Saved/tlp_tj3.txt"
def W(*a): open(out,"a",encoding="utf-8").write(" ".join(str(x) for x in a)+"\n")
open(out,"w").write("")
ST={"t0":None,"step":0,"h":None}
def tick(dt):
    S=ST
    try:
        w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
        if w is None: return
        now=unreal.GameplayStatics.get_time_seconds(w)
        acts=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor)
        L={a.get_actor_label():a for a in acts}
        J=L["TLP_Jefe_Controlador"]; lobo=L["TLP_Jefe_Lobo"]; pc=unreal.GameplayStatics.get_player_character(w,0)
        pu=L["TLP_Puerta_Escenario_Este"]; g=lambda k: J.get_editor_property(k)
        def st():
            v=lobo.get_actor_location(); r=lobo.get_actor_rotation()
            luces=[a.get_editor_property("hidden") for a in acts if a.get_actor_label().startswith("TLP3_Luz")]
            return f"t={now:.1f} est={g('Estado')} fase={g('Fase')} S={g('S'):.2f} lobo=({v.x:.0f},{v.y:.0f},{v.z:.0f}) yaw={r.yaw:.0f} puerta_z={pu.get_actor_location().z:.0f} luces_ocultas={luces} linea='{g('Linea')}'"
        if S["t0"] is None:
            S["t0"]=now; S["ts"]=now; W("inicio",st())
            b=L["TLP3_Bandera_BO_Checkpoint_0_Marca"]; W(" bandera0",b.static_mesh_component.static_mesh.get_name(),"pasado",b.get_editor_property("Pasado"))
            b=L["TLP3_Bandera_BO_Checkpoint_2_Marca"]; W(" bandera2",b.static_mesh_component.static_mesh.get_name())
            W(" paco anim",L["TLP3_Paco"].skeletal_mesh_component.is_playing(),"jaula oculta",L["TLP3_Jaula_Paco"].get_editor_property("hidden"))
            pc.set_actor_location(unreal.Vector(26000,700,120),False,True); S["step"]=1; return
        e=now-S["ts"]
        if S["step"]==1 and e>1.5:
            W("junto a Paco",st(),"P3",L["BO_Goal_P3"].get_editor_property("Resuelto"))
            L["BO_Goal_P3"].set_editor_property("Resuelto",True); S["step"]=2; S["ts"]=now
        elif S["step"]==2 and e>1.0:
            W("P3 resuelta +1s",st(),"jaula oculta",L["TLP3_Jaula_Paco"].get_editor_property("hidden"),"npc liberado",L["TLP3_Paco_Anim"].get_editor_property("Liberado"))
            S["step"]=3; S["ts"]=now
        elif S["step"]==3 and e>2.0:
            W("P3 +3s puerta",st(),"npc despues",L["TLP3_Paco_Anim"].get_editor_property("Despues"))
            pc.set_actor_location(unreal.Vector(9200,1000,120),False,True); S["step"]=4; S["ts"]=now
        elif S["step"]==4 and e>1.0:
            b=L["TLP3_Bandera_BO_Checkpoint_4_Marca"]; W("en checkpoint 4 bandera",b.static_mesh_component.static_mesh.get_name(),b.get_editor_property("Pasado"),st())
            pc.set_actor_location(unreal.Vector(8900,1000,120),False,True); S["step"]=5; S["ts"]=now
        elif S["step"]==5 and e>2.5:
            W("revelacion",st()); pc.set_actor_location(unreal.Vector(8600,600,120),False,True); S["step"]=6; S["ts"]=now; S["n"]=0
        elif S["step"]==6 and e>0.4*(S["n"]+1):
            W(" muestra",st()); S["n"]+=1
            if S["n"]>=12: unreal.unregister_slate_post_tick_callback(S["h"]); W("FIN")
    except Exception as ex:
        W("ERROR",repr(ex)); unreal.unregister_slate_post_tick_callback(S["h"])
ST["h"]=unreal.register_slate_post_tick_callback(tick)
