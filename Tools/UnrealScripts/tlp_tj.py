# Prueba automatica de la pelea contra el lobo en PIE
import unreal, os
out=os.path.join(unreal.Paths.project_saved_dir(),"tlp_tj.txt")
def W(*a): open(out,"a",encoding="utf-8").write(" ".join(str(x) for x in a)+"\n")
open(out,"w").write("")
ST={"t0":None,"step":0,"h":None,"last":-1}
def tick(dt):
    try:
        w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
        if w is None: return
        now=unreal.GameplayStatics.get_time_seconds(w)
        acts=unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor)
        L={a.get_actor_label():a for a in acts}
        J=L["TLP_Jefe_Controlador"]; lobo=L["TLP_Jefe_Lobo"]; pc=unreal.GameplayStatics.get_player_character(w,0)
        resp=next(a for a in acts if a.get_class().get_name()=="BP_TLP_Respawn_C")
        fin=next(a for a in acts if a.get_class().get_name()=="BP_TLP_Final_C")
        g=lambda k: J.get_editor_property(k)
        def st(): 
            v=lobo.get_actor_location()
            bots=[a for a in acts if a.get_class().get_name()=="BP_TLP_Enemigo_C" and not a.get_editor_property("Muerto") and any(str(t).startswith("Bot_F") for t in a.tags)]
            focos=[a.get_actor_label() for a in acts if a.get_class().get_name()=="BP_TLP_Foco_C" and a.get_editor_property("Activo")]
            return f"t={now:.1f} est={g('Estado')} fase={g('Fase')} golpes={g('Golpes')} lobo=({v.x:.0f},{v.y:.0f},{v.z:.0f}) oculto={lobo.get_editor_property('hidden')} linea='{g('Linea')}' bots_vivos={len(bots)} focos={focos} vidas={resp.get_editor_property('Vidas')} final_est={fin.get_editor_property('Estado')}"
        S=ST
        if S["t0"] is None:
            S["t0"]=now; W("inicio",st())
            for a in acts:
                if a.get_class().get_name() in ("BP_TLP_Enemigo_C","BP_TLP_Foco_C","BP_TLP_Peligro_C"): pass
            pc.set_actor_location(unreal.Vector(9200,1000,120),False,True); S["step"]=1; S["ts"]=now; return
        e=now-S["ts"]
        if S["step"]==1 and e>2.0:
            W("tras entrar al escenario",st()); 
            pc.set_actor_location(unreal.Vector(9100,1000,120),False,True)
            L["OMC_Receiver_Bounce_Plataforma_Presentacion"].set_editor_property("VersionState",unreal.Name("Hybrid")); S["step"]=2; S["ts"]=now
        elif S["step"]==2 and e>0.6: W("fase1 golpe, volando",st()); S["step"]=3; S["ts"]=now
        elif S["step"]==3 and e>2.0: W("atorado",st()); S["step"]=4; S["ts"]=now
        elif S["step"]==4 and e>2.5:
            W("fase2 iniciada",st()); W(" plataforma A tras reset",L["OMC_Receiver_Bounce_Plataforma_Presentacion"].get_editor_property("VersionState"))
            S["step"]=5; S["ts"]=now
        elif S["step"]==5 and e>3.5:
            fs=[a for a in acts if a.get_class().get_name()=="BP_TLP_Foco_C"]
            W(" focos:",[(a.get_actor_label(),a.get_editor_property("hidden"),round(a.get_actor_location().z)) for a in fs], "vidas",resp.get_editor_property("Vidas"))
            L["TLP_Jefe_Receptor_Palanca"].set_editor_property("VersionState",unreal.Name("Hybrid")); S["step"]=6; S["ts"]=now
        elif S["step"]==6 and e>0.2: W("foco del techo cayendo",st(), "foco z",round(L["TLP_Jefe_FocoTecho"].get_actor_location().z)); S["step"]=7; S["ts"]=now
        elif S["step"]==7 and e>5.5: W("fase3 iniciada",st()); S["step"]=8; S["ts"]=now
        elif S["step"]==8 and e>4.5:
            lado=J.get_editor_property("Lado"); W(" lado",lado,st())
            L["TLP_Jefe_Receptor_PlataformaB" if lado else "OMC_Receiver_Bounce_Plataforma_Presentacion"].set_editor_property("VersionState",unreal.Name("Hybrid")); S["step"]=9; S["ts"]=now
        elif S["step"]==9 and e>2.0: W("golpe 3",st()); S["step"]=10; S["ts"]=now
        elif S["step"]==10 and e>4.5:
            W("derrota/final",st(), "fin",fin.get_editor_property("Fin"), "mural oculto", L["BO_Mural_Final"].get_editor_property("hidden"))
            unreal.unregister_slate_post_tick_callback(S["h"])
    except Exception as ex:
        W("ERROR",repr(ex)); unreal.unregister_slate_post_tick_callback(ST["h"])
ST["h"]=unreal.register_slate_post_tick_callback(tick)
