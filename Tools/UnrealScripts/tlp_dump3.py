import unreal
eas=unreal.get_editor_subsystem(unreal.EditorActorSubsystem); out=[]
for a in eas.get_all_level_actors():
    o,e=a.get_actor_bounds(False); l=a.get_actor_label()
    key=any(k in l for k in ("Paco","Toto","Jaula","Barca","Checkpoint","marca","Marca","Puerta","Goal","Final","Foco","Ending","Reveal"))
    stage=6500<o.x<9700 and -300<o.y<2300 and (e.x>500 or e.y>500 or e.z>250)
    if key or stage or "Vida" in a.get_class().get_name():
        out.append(f"{l}|{a.get_class().get_name()}|o={o.x:.0f},{o.y:.0f},{o.z:.0f}|e={e.x:.0f},{e.y:.0f},{e.z:.0f}|tags={[str(t) for t in a.tags]}|hid={a.is_hidden_ed()}")
p="/Game/TheLastPatch/Props/"
for n in ("Bandera_Roja/SM_Bandera_Roja","Bandera_Verde/SM_Bandera_Verde","Bote/SM_Bote","Queso/SM_Queso","Jaula/SM_Jaula"):
    m=unreal.load_asset(p+n); out.append(f"ASSET {n} {m.get_bounds().box_extent if m else None}")
s=unreal.load_asset("/Game/TheLastPatch/Personajes/Paco/SK_Paco"); out.append(f"ASSET SK_Paco {s.get_bounds().box_extent if s else None}")
import os
open(r"C:/Proyectos/EpicMegaJam_2026/Saved/tlp_dump3.txt","w",encoding="utf-8").write("\n".join(out))
