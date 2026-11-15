# Assets del mapa · The Last Patch: Director's Cut

Arte fuente para los seis niveles del mapa (muelle, ascensor, corredor de anuncios, puente, escenario y puerto restaurado). Todo sale de `Bocetos para Lander/Mapa_levels.jpeg`: misma paleta, mismos textos y mismos props.

Cada asset existe para los **dos planos** del juego:

| Plano | Prefijo | Qué es |
|---|---|---|
| OG (polígonos low poly) | `T_OG_` | 64×64 px, paleta corta, color plano, sin PBR |
| UE (3D pulido) | `T_UE_`, `T_Senal_` | 1024 px, BaseColor + Normal + ORM |

Mira primero `_Vistas/`: son hojas de contacto con todo lo que hay.

## Carpetas

- `Texturas/OG_LowPoly/` — 14 texturas tileables `T_OG_<Material>_64.png`.
- `Texturas/UE_Pulido/` — los mismos 14 materiales en `T_UE_<Material>_BC.png`, `_N.png` y `_ORM.png`.
- `Senaletica/UE_Pulido/` — 34 vallas, pósters, letreros de zona, flechas, barreras, banderolas y caras de caja (`T_Senal_*.png`, con alfa).
- `Senaletica/OG_LowPoly/` — las mismas 34 a 1/8 de tamaño (`T_OG_Senal_*.png`, alfa de 1 bit).
- `Senaletica/SVG/` y `UI/SVG/` — fuentes editables. Necesitan las tipografías de `Fuentes/` instaladas.
- `UI/` — 64 piezas para UMG (`T_UI_*.png`, exportadas a 2×): título, paneles, botones, etiquetas, iconos, vida, progreso de zonas, diálogo, teclas y cursor.
- `Hojas_Guia_3D/` — 11 hojas `HG_00` a `HG_10` con vistas ortográficas en cm, piezas, presupuesto de triángulos y qué textura usa cada prop en cada plano.
- `Fuentes/` — Space Grotesk, Barlow Condensed y Silkscreen en TTF (licencia SIL OFL, incluida).
- `_Generadores/` — los scripts de Python que produjeron todo, por si hay que cambiar un texto o un color.

## Materiales

MaderaMuelle, MaderaOscura, PisoEscenario, Agua, Arena, ConcretoMuelle, EstucoFaro, PanelComercial, ContenedorMarca, ContenedorBlanco, MetalGrua, Telon, Precaucion, Acolchado.

Todas repiten sin costura en X y en Y. Están pensadas para **200 cm por repetición** en los dos planos, así la misma UV sirve para OG y UE y cambiar de forma es solo cambiar de material.

## Importar en Unreal

Copia los PNG a `Content/_Game/Materials/` (texturas), `Content/_Game/Props/` (señalética) y `Content/_Game/UI/`. Los nombres ya llevan el prefijo `T_` del equipo.

**Plano OG**

- Texture Group: `2D Pixels (unfiltered)`; Filter: `Nearest`; Mip Gen Settings: `NoMipmaps`; sRGB activado.
- Material: solo Base Color. Roughness 1, Specular 0, sin normal map.
- Señalética OG: Blend Mode `Masked`.

**Plano UE**

- `_BC`: sRGB activado.
- `_N`: Compression `Normalmap`. Están en formato DirectX (el de Unreal); no hay que invertir el canal verde.
- `_ORM`: sRGB **desactivado**, Compression `Masks`. R = Ambient Occlusion, G = Roughness, B = Metallic.
- Señalética: Base Color + un poco de Emissive (≈0.3) para que lo comercial “brille” frente a lo OG. Blend Mode `Masked` para las esquinas redondeadas.

**UI**

- Texture Group `UI`, Compression `UserInterface2D`, sin mipmaps.
- Están exportadas a 2×: en UMG usa la mitad del tamaño en píxeles.
- Paneles, botones, etiquetas y teclas son 9‑slice: Draw As `Box`. Margen en px del PNG: paneles 64, botones 64 a los lados, etiquetas 32, teclas 24.

## Paleta

| Nombre | Hex | Uso |
|---|---|---|
| OG | `#ac7d49` | Madera original |
| OG oscuro | `#74502c` | Vigas, pilotes, marcos |
| Comercial | `#f0f1f5` | Paneles y vallas de la empresa |
| Marca | `#c55b7f` | Rosa de la empresa: anuncios, franjas, telón |
| Marca oscuro | `#8f3d5b` | Texto sobre rosa claro, sombras del rosa |
| Cielo | `#e0eaf4` | Fondo |
| Agua | `#7ca6ce` | Mar |
| Arena | `#ebc5a0` | Playa |
| Muelle | `#c6b89d` | Concreto del puerto |
| Tinta | `#2b2b29` | Líneas, texto |
| Papel | `#f4f3ee` | Fondos de UI |
| Personaje | `#394962` | Etiquetas de personajes |
| Moneda | `#f6d880` | Moneda 4K, selección |
| Precaución | `#e8b24a` | Franjas de las barreras |
| Escenario / Noche | `#3a3343` / `#292533` | Piso y fondo del teatro |

Regla de lectura del mapa: **madera OG = lo original**, **rosa y blanco = lo que impuso la empresa**, **trazo punteado = mecánica híbrida** (rebote, tracción).

## Tipografía

- **Space Grotesk** — títulos, UI, letreros de zona.
- **Barlow Condensed Bold** — todo lo que “grita”: vallas, pósters, botones comerciales.
- **Silkscreen** — textos del HUD cuando el jugador está en el plano OG.

## Regenerar

Requiere Python 3 con `numpy`, `pillow` y `playwright` (Chromium).

```
cd Assets_Mapa
python3 _Generadores/texturas.py Texturas
python3 _Generadores/senaletica.py Senaletica
python3 _Generadores/ui.py UI
python3 _Generadores/hojas.py Hojas_Guia_3D
```

Los colores viven en `_Generadores/svglib.py` (señalética, UI y hojas) y al inicio de `texturas.py`.

## Pendientes conocidos

- La altura de referencia en las hojas es el maniquí de UE5 (180 cm), porque los rigs del repo usan ese esqueleto. Si el ratón queda más bajo en el juego, escalen los props en la misma proporción.
- Las medidas de los props son una propuesta a partir del boceto en perfil; el mapa no trae cotas.
- Los PNG pasan por Git LFS (≈33 MB en total, casi todo en `Texturas/UE_Pulido`).
