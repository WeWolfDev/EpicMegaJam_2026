import unreal
eas=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L={a.get_actor_label():a for a in eas.get_all_level_actors()}
lo=L["TLP_Jefe_Lobo"]; eas.set_selected_level_actors([lo])
o,e=lo.get_actor_bounds(False); c=lo.skeletal_mesh_component
open(r'C:/Proyectos/EpicMegaJam_2026/Saved/chk3.txt','w').write(f"o={o} e={e} mesh={c.get_skeletal_mesh_asset()} vis={c.is_visible()} scale={lo.get_actor_scale3d()} hidEd={lo.is_hidden_ed()}")
