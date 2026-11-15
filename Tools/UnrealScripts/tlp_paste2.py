# Deja un .t3d en el portapapeles y abre el Blueprint. Usar: BP='...'; F='...'; exec(...)
import unreal, subprocess, os
d = r'C:\Proyectos\EpicMegaJam_2026\Tools\UnrealScripts'
txt = open(os.path.join(d, F), encoding='utf-8').read()
subprocess.run('clip', input=txt.encode('ascii'), shell=True)
unreal.get_editor_subsystem(unreal.AssetEditorSubsystem).open_editor_for_assets([unreal.load_asset(BP)])
