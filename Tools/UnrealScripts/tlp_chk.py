import unreal, os
L=[]
sk=unreal.load_asset("/Game/TheLastPatch/Personajes/Lobo/SK_Lobo")
L.append(f"mesh skel {sk.get_editor_property('skeleton').get_path_name()}")
for n in ("A_Lobo_Talk","A_Lobo_Idle_Smug","A_Lobo_Launched_Tumble"):
    a=unreal.load_asset("/Game/TheLastPatch/Personajes/Lobo/Anims/"+n)
    try: L.append(f"{n} skel {a.get_editor_property('skeleton').get_path_name()} len {a.get_editor_property('sequence_length') if hasattr(a,'sequence_length') else unreal.AnimationLibrary.get_sequence_length(a)} frames {unreal.AnimationLibrary.get_num_frames(a)}")
    except Exception as ex: L.append(f"{n} err {ex}")
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
L.append(f"PIE {w}")
if w:
    for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.SkeletalMeshActor):
        if a.get_actor_label()=="TLP_Jefe_Lobo":
            c=a.skeletal_mesh_component
            L.append(f"lobo mode {c.get_animation_mode()} playing {c.is_playing()} pos {c.get_position() if hasattr(c,'get_position') else '?'} hidden {a.get_editor_property('hidden')} visible {c.is_visible()} tick {c.is_component_tick_enabled()} vbo {c.get_editor_property('visibility_based_anim_tick_option')}")
            j=[x for x in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor) if x.get_actor_label()=="TLP_Jefe_Controlador"][0]
            L.append(f"jefe estado {j.get_editor_property('Estado')} fase {j.get_editor_property('Fase')}")
open(os.path.join(unreal.Paths.project_saved_dir(),"tlp_chk.txt"),"w").write("\n".join(L))
