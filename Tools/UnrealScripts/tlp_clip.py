# Guarda el texto del portapapeles de Windows en Saved/clip.t3d
import ctypes, os, unreal
from ctypes import wintypes
u32, k32 = ctypes.windll.user32, ctypes.windll.kernel32
u32.GetClipboardData.restype = wintypes.HANDLE
k32.GlobalLock.restype = ctypes.c_void_p
k32.GlobalLock.argtypes = [wintypes.HANDLE]
k32.GlobalUnlock.argtypes = [wintypes.HANDLE]
txt = ""
if u32.OpenClipboard(None):
    try:
        h = u32.GetClipboardData(13)  # CF_UNICODETEXT
        if h:
            p = k32.GlobalLock(h)
            txt = ctypes.wstring_at(p)
            k32.GlobalUnlock(h)
    finally:
        u32.CloseClipboard()
out = os.path.join(unreal.Paths.project_saved_dir(), "clip.t3d")
open(out, "w", encoding="utf-8").write(txt)
unreal.log(f"[TLP] portapapeles guardado: {len(txt)} caracteres")
