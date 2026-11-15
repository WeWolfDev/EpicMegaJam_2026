# The Last Patch: Director's Cut — Cambios del nivel L_Puerto

Rama: `nivel-puerto-crod3` · Autor del nivel: Cesar Rodríguez · Mecánica de la caña, menú, música y arte retro: Emilio Arellano ([Eacvellano](https://github.com/Eacvellano))

_Actualizado el 15 de noviembre con los commits de Emilio de las 03:00 y 11:30 (ver «Cambios posteriores»)._

Este documento explica qué contiene la rama, qué se hizo en el nivel del puerto y qué falta. La primera parte es un resumen para cualquiera (equipo o jueces); la segunda es el detalle técnico para el equipo.

---

## Parte 1 · Resumen

### Qué se juega
Un plataformero 3D de un solo nivel, `L_Puerto`. El jugador es el ratón pescador original, que vuelve a un puerto convertido en remake comercial. Con la caña pesca "bocetos" de objetos antiguos (OG) y los aplica a objetos modernos para crear híbridos que abren el camino.

Recorrido:

0. **Menú principal** (`L_MainMenu`): START, SETTINGS (volumen y calidad gráfica) y EXIT.
1. **Muelle de llegada.** Movimiento, salto y primer enemigo.
2. **Tramo 1 de plataformas** hasta el patio.
3. **Puzzle 1 · El ascensor de lujo.** Pescar el *Rebote* del trampolín OG y aplicarlo al ascensor para llegar al muelle alto y liberar a **Toto**.
4. **Tramo 2**, en altura, hasta el corredor.
5. **Puzzle 2 · Publicidad obligatoria.** Toto repara la polea OG; se pesca su *Tracción* y se aplica a la valla publicitaria para abrir el paso.
6. **Tramo 3** hasta la orilla de la grúa.
7. **Puzzle 3 · El puente eliminado.** *Tracción* a la grúa para cruzar el canal y rescatar a **Paco**, que abre el acceso al escenario.
8. **Tramos 4 y 5** de regreso por la pasarela.
9. **Final.** En el escenario aparece por primera vez la nueva mascota. Con *Rebote* en la plataforma de presentación sale volando a un expositor acolchado y el puerto recupera su versión original.
10. **Cierre.** El ratón, Toto y Paco en el muelle, la pantalla "Director's Cut completado" y los créditos.

### Mecánicas
- **Caña y fusión** (de Emilio): pescar un boceto de una fuente OG y lanzarlo a un receptor compatible. Hay dos propiedades: *Rebote* y *Tracción*.
- **Quitar el poder** (agregado en el nivel): lanzar la caña a un objeto que ya tiene poder se lo quita y el boceto vuelve a la caña. Así la grúa, la valla o el panel regresan a su sitio y nadie se queda atascado.
- **Vidas:** 3 vidas, mostradas como corazones de queso. Al perder la última vuelves al último checkpoint con las vidas llenas; los puzzles resueltos no se pierden.
- **Quesos:** recuperan 1 vida (máximo 3). Hay 7 en las zonas y 10 en los tramos nuevos.
- **Enemigos ("bots de marketing"):** te persiguen dentro de su zona. Saltarles encima los aplasta y te impulsa; tocarlos de lado quita una vida.
- **Obstáculos:** agua, troncos que barren pasarelas, letreros electrificados intermitentes y tablas frágiles que se caen.
- **Pausa:** P (Esc en el juego empaquetado). Desde la pausa o la pantalla final, R reinicia y Q sale.

### Controles
WASD mover · Espacio saltar · Clic izquierdo (mantener y soltar) caña · P pausa · R reiniciar · Q salir.

---

## Parte 2 · Detalle técnico

### Quién hizo qué

| Parte | Autor | Carpeta |
|---|---|---|
| Caña, sistema de fusión, ratón jugable, animaciones corregidas, apuntado, sonidos | **Emilio Arellano** | `Content/OneMoreCast/` |
| Nuevo modelo del ratón, corazones de vida, música, menú principal, cielo, texturas y carteles retro | **Emilio Arellano** | `OneMoreCast/Player/MouseExport`, `OneMoreCast/Health`, `TheLastPatch/MainMenu`, `RetroSurfaces`, `RetroSigns`, `RetroSky`, `SourceArt/` |
| Integración de la caña en el nivel y opción de quitar poder | Cesar (sobre el trabajo de Emilio) | `OneMoreCast/Fusion/BP_FusionTestRig` (ver abajo) |
| Nivel, blockout, puzzles, vidas, HUD, obstáculos, enemigos, NPC, final, pausa | Cesar | `Content/L_Puerto.umap`, `Content/TheLastPatch/` |
| Scripts de Python usados para construir el nivel | Cesar | `Tools/UnrealScripts/` |

### Cambio en el trabajo de Emilio (para que lo revise)
Solo se tocó **un** asset suyo: `OneMoreCast/Fusion/BP_FusionTestRig`, función **`CompleteCast`**.

- **Antes:** si el anzuelo caía en un receptor, siempre intentaba aplicar el boceto actual.
- **Ahora:** si el receptor ya está en estado `Hybrid`, se llama a `ResetObject` del objeto y a `AcquireSketch` del inventario con su `SketchType`. El objeto pierde el poder y el boceto vuelve a la caña. Si no está en `Hybrid`, el flujo es el original (`ApplySketch` y, si aplica, `ClearSketch`).

Nada más de OneMoreCast se modificó. El rig está colocado en el nivel como `OMC_FusionRig`, y los receptores y fuentes son instancias de su `BP_FusionObject`.

### Blueprints nuevos (`Content/TheLastPatch/Blueprints/`)

| Blueprint | Qué hace |
|---|---|
| `BP_TLP_Respawn` | Guarda las vidas (3). Evento `PerderVida`: lleva al jugador al último checkpoint y resta una vida; si llega a 0, rellena a 3. Evento `GanarVida`: +1 hasta 3. |
| `BP_TLP_Checkpoint` | Al pisarlo, mueve el punto de reaparición a su posición. |
| `BP_TLP_Agua` | Volumen del agua: al caer, llama a `PerderVida`. |
| `BP_TLP_Vida` | Queso: gira y flota; si el jugador lo toca y le falta vida, llama a `GanarVida` y desaparece. |
| `BP_TLP_Enemigo` | Persigue al jugador si está dentro de `RadioVision`, sin alejarse más de `RadioCasa` de su origen. Si el jugador está más de 60 cm por encima al tocarlo, lo aplasta (el enemigo desaparece y el jugador recibe un impulso con `LaunchCharacter`); si no, `PerderVida`. |
| `BP_TLP_Peligro` | Obstáculo que se mueve en vaivén (`PuntoB`, `Periodo`, `Desfase`) o se enciende y apaga (`Intermitente`, `FraccionEncendido`). Al tocarlo, `PerderVida`. |
| `BP_TLP_TablaFragil` | Al pisarla, se cae tras `Retraso` y reaparece tras `Reaparece`. |
| `BP_TLP_Mover` | Mueve una `Pieza` entre su origen y `Destino`. Modo `Vaiven` (plataformas móviles) o ligado a un `Receptor` de fusión: va al destino si el receptor está en `Hybrid` y regresa si pierde el poder. |
| `BP_TLP_Meta` | Meta de puzzle: al entrar el jugador, oculta los actores con `TagAnuncios`, muestra los de `TagRestaurar` y muestra `Mensaje`. Solo una vez (`Resuelto`). |
| `BP_TLP_Charla` | Texto en el mundo que mira a la cámara y aparece al acercarse (`Radio`). Cambia de `TextoAntes` a `TextoDespues` cuando su `Meta` se resuelve. Se usa para Toto, Paco y las pistas. |
| `BP_TLP_Final` | Máquina de estados del final: espera la plataforma en `Hybrid` con la mascota revelada, la lanza en arco hacia el expositor, restaura el puerto, coloca al ratón, Toto y Paco en el muelle, cambia a la cámara final y bloquea el control. |
| `BP_TLP_Pausa` | Teclas P/Esc (pausar), R (reiniciar) y Q (salir); también activas en la pantalla final. |
| `BP_TLP_HUD` | Panel con controles y el boceto en la caña. Dibuja el menú de pausa y la pantalla final. Emilio cambió los 3 cuadros de vida por el widget de corazones `WBP_PlayerHealth`. |

Los Blueprints `BP_Ascensor`, `BP_Grua`, `BP_NPC`, `BP_PanelCierre`, `BP_PuzzleManager`, `BP_ReceptorRebote`, `BP_SketchSource`, `BP_SketchSystem`, `BP_VallaPublicitaria`, `BP_VersionableObject` y `BP_FinaleController` son esqueletos de la propuesta inicial del documento de diseño. Están vacíos y el nivel no los usa; se pueden borrar o reutilizar.

### El nivel (`Content/L_Puerto.umap`)
- Mapa inicial del editor. El juego empaquetado arranca ahora en `L_MainMenu`, que carga `L_Puerto` con START (`Config/DefaultEngine.ini`). El World Settings del nivel usa `BP_ThirdPersonGameMode` con `BP_TLP_HUD`.
- Unos 400 actores, organizados en carpetas del Outliner: `Blockout/0_Muelle` … `4_Escenario`, `TLP/Logica`, `TLP/Puzzles`, `TLP/Obstaculos`, `TLP/Enemigos`, `TLP/Charlas`, `TLP/Puertas`, `TLP/Vidas` y `TLP/Plataformas/S1…S5`.
- **Puzzles y estado:** cada zona tiene una `BO_Goal_*` (`BP_TLP_Meta`) que retira anuncios (`Ads_P1`, `Ads_P2`, `Ads_P3`, `Ads_Final`) y devuelve piezas OG (`Restore_*`).
- **Progresión:** la polea de Tracción lleva la etiqueta `Restore_P1`, así que no existe hasta liberar a Toto. La puerta este del escenario lleva `Ads_P3` y se abre al rescatar a Paco. La mascota (`Mascot`) solo aparece al entrar al escenario.
- **Ampliación plataformera:** las zonas se separaron unos 160 m en total y los huecos se llenaron con 5 tramos de 52–56 m. Cada tramo mezcla plataformas fijas, pequeñas y escalonadas, móviles, tablas frágiles, troncos, una isla con enemigos y un checkpoint con queso. Los saltos van de 2.7 a 3.5 m; el máximo del ratón es de unos 4.5 m. El tramo 2 va a 5 m sobre el agua.
- **Enemigos:** 19 en total, 10 en las zonas y 9 en las islas de los tramos.

### Otros assets de `Content/TheLastPatch/`
- `Blockout/`: material base `M_Blockout` e instancias de color (peligro, frágil, enemigo, móvil, queso, etc.).
- `Materiales/`, `Texturas/OG|UE`, `Senaletica/OG|UE`, `UI/`: assets visuales importados desde `Assets_Mapa` (versiones OG low-poly y UE pulidas).
- `Personajes/Raton/`: importación del ratón de Meshy con retarget del maniquí.

### Cambios posteriores de Emilio (15 de noviembre)
Emilio subió dos commits sobre esta rama. Lo que sigue resume sus propios documentos en `Docs/`.

**`8c616cb` · Fusión de los dos proyectos de Unreal (03:00).** Detalle en `Docs/FUSION_MEJORAS_EMILIO.md`.
- Nuevo modelo del ratón con 13 animaciones (reposo con caña, caminar, correr, salto, apuntado, carga, lanzamiento y recuperación), en `OneMoreCast/Player/MouseExport`. Se aplicó al personaje predeterminado y al ratón colocado en el mapa.
- Mejoras en la caña (`BP_FishingRod`, `BP_FusionTestRig`): agarre, línea alineada con la punta y lanzamiento sincronizado. **Conservó el cambio de quitar el poder** en `CompleteCast`.
- Corazones de queso (`WBP_PlayerHealth`) que leen `BP_TLP_Respawn.Vidas`, sin un segundo sistema de vida. Retiró los cuadrados del HUD.
- 0,8 s de invulnerabilidad entre golpes, y el daño estándar de Unreal también resta vidas del puerto.
- Música en bucle «Mischief at the Docks», que continúa al reaparecer.
- Toca varios Blueprints del nivel (`Agua`, `Checkpoint`, `Enemigo`, `HUD`, `Peligro`, `Respawn`, `Vida` y los GameModes) para conectar todo lo anterior.
- Según su documento, 31 comprobaciones automáticas pasaron.

**`f470197` · Improvements (11:30).** Detalle en `Docs/MENU_PRINCIPAL.md`, `Docs/TEXTURAS_SUPERFICIE_RETRO.md` y `Docs/CARTELES_RETRO_34.md`.
- **Menú principal** `L_MainMenu` (`TheLastPatch/MainMenu`) con START, SETTINGS (volumen y calidad) y EXIT. Ahora es el mapa inicial del juego.
- **Texturas retro** en todo el puerto (`RetroSurfaces`): tablones, madera agrietada en las tablas frágiles, metal en las plataformas móviles, piedra en las islas, agua animada y detalles sin colisión.
- **34 carteles** con arte nuevo (`RetroSigns`) y **cielo morado de atardecer** (`RetroSky`). Desactivó las nubes volumétricas y la niebla anteriores.
- Originales de las imágenes en `SourceArt/`.
- `MapsToCook` con `L_Puerto` y `L_MainMenu`, y los plugins de MCP activados en el `.uproject`.
- Según sus documentos, no se modificó la lógica de la caña, el personaje ni los puzzles en este commit.

### Herramientas (`Tools/UnrealScripts/`)
Scripts de Python para el editor de Unreal que construyeron el nivel (blockout, colocación de puzzles y obstáculos, ampliación de tramos) y para pruebas automáticas en Play. Los archivos `.t3d` son los gráficos de Blueprint en texto que se pegaron en los editores. No hacen falta para jugar; sirven para rehacer o ajustar el nivel. `subir_al_repo*.bat` es el script que subió esta rama.

### Cómo se probó
Pruebas en Play dentro del editor, con scripts que mueven y lanzan al ratón:
- **Vidas:** perder 3 vidas vuelve al checkpoint con 3; un queso suma 1.
- **Puzzles:** al liberar a Toto aparece la polea. La grúa va con Tracción y regresa al quitarle el poder. Al rescatar a Paco se abre la puerta.
- **Final completo:** la mascota vuela al expositor, se restaura el puerto, los tres quedan en el muelle y se activa la pantalla final.
- **Enemigos:** persiguen al jugador, quitan una vida al tocarlo de lado y se aplastan al caerles encima.
- **Saltos:** los 34 saltos entre plataformas fijas de los 5 tramos se completan. Las plataformas móviles llevan al ratón.

**No probado:** los 8 saltos que dependen de plataformas móviles (dependen del momento del salto), el menú de pausa en pantalla, el encuadre de la cámara final y un recorrido completo jugado a mano.

### Pendientes y cosas a revisar
- **Empaquetar** el juego y probar el ejecutable: que abra en el menú, que START cargue `L_Puerto` y que EXIT cierre. Los dos mapas ya están en la lista de cocinado (`DefaultGame.ini`).
- **Plugins de MCP:** el último commit activó `ModelContextProtocol` y `AllToolsets` en el `.uproject`. Son herramientas del editor; conviene confirmar que no impiden abrir el proyecto en otras computadoras ni empaquetar, y desactivarlos para la entrega si estorban.
- **Recorrido manual completo:** ni las pruebas de Cesar ni las de Emilio cubren una partida entera jugada a mano (menú, tres puzzles y final) con el modelo, las texturas y el cielo nuevos.
- **`main` va por otro lado:** Lander subió a `main` los assets de origen del mapa y modelos 3D (`Assets_Mapa/`, `Modelos_3d/`). No toca los mismos archivos que esta rama, así que el Pull Request no debería tener conflictos.
- **Estructura de carpetas:** el contenido está en `Content/TheLastPatch/`, no en `Content/_Game/` como pide `CONTRIBUTING.md`. Se intentó reorganizar y rompió referencias, así que se dejó así. Moverlo es mejor hacerlo después de la jam, con "Fix Up Redirectors".
- El texto del objeto híbrido de OneMoreCast siempre dice "REBOTE ACTIVADO", aunque sea Tracción (detalle del `BP_FusionObject` de Emilio).
- `Lvl_ThirdPerson` y `Nivel_1` no se subieron; el juego no los usa.
- **Si sobra tiempo** (según el documento de diseño): pistas automáticas tras 30–45 s sin avanzar, sonidos al aplicar bocetos, ruta alternativa con la caja del puzzle 2 y el modo comercial con dash.
