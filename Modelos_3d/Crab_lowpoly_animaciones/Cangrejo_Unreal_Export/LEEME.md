# Cangrejo enemigo — exportación para Unreal Engine 5

Rig, expresiones y cuatro animaciones en el sitio hechas a partir de `Meshy_AI_CrabMechanic_…_remesh_tri.fbx`. Todo se verificó reimportando cada FBX en Blender. **No se probó en Unreal.**

> **Aviso sobre el modelo:** el único modelo de la carpeta es un cangrejo con gorra café y overol verde con una llave inglesa, que coincide con la descripción de Toto (el cangrejo mecánico) en el documento de diseño. No lo rediseñé. Si el enemigo debía ser otro cangrejo, hay que repetir el trabajo con ese modelo.

## Contenido

| Archivo | Qué es |
|---|---|
| `SK_Cangrejo.fbx` | Malla con esqueleto, material y 7 morph targets, en pose de referencia |
| `Animations/Crab_Idle.fbx` | Bucle, 90 frames (3,0 s) |
| `Animations/Crab_Walk_Side.fbx` | Bucle, 24 frames (0,8 s) |
| `Animations/Crab_Attack.fbx` | Una vez, 24 frames (0,8 s) |
| `Animations/Crab_Dead.fbx` | Una vez, 54 frames (1,8 s); mantener el último frame |
| `Textures/T_Cangrejo_*.png` | BaseColor, Normal, Metallic, Roughness (4096 px) |
| `Preview_Cangrejo.mp4` | Cada clip (bucles ×5, el walk también en reversa) y la secuencia de transiciones |
| `Expresiones_MorphTargets.png` | Cada morph target al 100 % |

Todos los FBX comparten malla, esqueleto, jerarquía, pose de referencia, pesos, unidades (cm), ejes (Z arriba, frente a +X) y 30 fps. Cada clip trae las 7 curvas de morph con el nombre exacto del morph target.

## Qué traía el modelo

- Una sola malla fusionada (4 770 vértices, 9 529 triángulos), un material y 4 texturas. Sin rig ni animaciones.
- 6 patas (3 por lado), cortas y sin rodilla marcada. 2 pinzas simétricas.
- Ojos fijos en la cara (no en tallo), cejas y párpados modelados. La boca es una línea pintada.

## Escala

- **50 cm de alto, 63 cm de ancho (de pinza a pinza) y 34 cm de fondo.** El modelo es más alto que ancho, así que no puede medir 90 × 50 cm sin deformarse; mantuve la altura para que el ratón pueda saltarlo.
- `root` está en el suelo, en (0, 0, 0), bajo el centro de las patas.

## Esqueleto (20 huesos)

- `root` → `body`
- Patas: `leg_l_01_a` → `leg_l_01_b`, y lo mismo para `02`, `03` y el lado `r` (01 delante, 02 en medio, 03 detrás).
- Pinzas: `claw_l_arm` → `claw_l_hand` → `claw_l_pincer`, y lo mismo para `r`. `pincer` mueve el dedo superior.
- Máximo 2 influencias por vértice. Gorra, cara y overol van al 100 % a `body`.
- **No hay `eyestalk_l`, `eyestalk_r` ni `jaw`:** el modelo no tiene tallos oculares ni mandíbula.

## Morph targets

`Blink`, `Eyes_Wide`, `Eyes_Angry`, `Eyes_Squint`, `Eyes_X`, `Mouth_Open`, `Mouth_Frown`.

Como la malla es rígida y los ojos y la boca están pintados, los morphs usan piezas pequeñas añadidas (párpados, discos de ojo, pupila, cruz e interior de la boca) que en reposo quedan ocultas dentro de la cabeza. Las cejas sí se deforman en `Eyes_Wide`, `Eyes_Angry` y `Eyes_Squint`. Por eso la malla exportada tiene 4 965 vértices y 9 743 triángulos.

## Clips

| Clip | Frames | Duración | Bucle | Expresión | Extensión máxima desde `root` |
|---|---|---|---|---|---|
| `Crab_Idle` | 90 | 3,0 s | Sí | `Eyes_Squint` 0,4; un parpadeo en los frames 38–54 | 33 cm |
| `Crab_Walk_Side` | 24 | 0,8 s | Sí | `Eyes_Angry` 0,55 | 31 cm |
| `Crab_Attack` | 24 | 0,8 s | No | `Eyes_Angry` 1,0 (frames 5–17); `Mouth_Open` 1,0 (13–16) | 44,5 cm (hacia +X) |
| `Crab_Dead` | 54 | 1,8 s | No | `Eyes_Wide` (3–17) → `Eyes_X` (desde 25); `Mouth_Open` (3–8) → `Mouth_Frown` (desde 15) | 54 cm (hacia −X) |

### Crab_Idle

- Abre y cierra las pinzas alternadas, balancea el caparazón y gira el cuerpo ±5° para mirar a los lados (no hay tallos).
- Las seis patas quedan apoyadas todo el clip.

### Crab_Walk_Side

- **Velocidad recomendada: 45 cm/s a play rate 1,0.** Reproducido hacia delante camina hacia **+Y** (su izquierda); con play rate negativo camina hacia −Y sin girar.
- Rango de play rate estimado: 0,6 a 1,5 (27 a 68 cm/s). Es una estimación mía, no una prueba en Unreal.
- Marcha en dos trípodes alternados; cada pata da 3 pasos por bucle. Zancada de 6 cm y levantamiento de 1,7 cm.
- El cuerpo oscila ±0,4 cm en Y y su posición media es exactamente 0: no avanza dentro del clip.

### Crab_Attack

| Frame | Qué ocurre |
|---|---|
| 0–9 | Anticipación (0,3 s): se encoge y echa atrás la pinza derecha |
| **9** | **Sin retorno:** despega hacia delante. Pon el aviso al jugador antes de este frame |
| **13** | **Impacto:** la pinza derecha se cierra (0,43 s). Sonido, pantalla de pérdida y reinicio |
| 16–22 | Salto de vuelta |
| 24 | Pose idéntica al frame 0 de `Crab_Idle` |

- El cuerpo se adelanta 21 cm y la pinza llega a 43 cm de `root` en +X. `root` no se mueve.
- El frame 0 también coincide exactamente con el frame 0 de `Crab_Idle`.

### Crab_Dead

| Frame | Qué ocurre |
|---|---|
| 0–4 | Recibe el golpe |
| **4** | **Desactiva la colisión de ataque** a partir de aquí (también puedes hacerlo en el frame 0) |
| 4–16 | Se tambalea de lado a lado |
| 16–26 | Cae de espaldas |
| **26** | **Impacto contra el suelo** (sonido y polvo) |
| 26–32 | Rebote pequeño |
| 28–46 | Agita las patas |
| 54 | Pose final |

- **Cae hacia atrás (−X)**, alejándose del jugador, y queda boca arriba sobre la espalda y la gorra, con la panza y las patas hacia arriba.
- La pose final ocupa de X = −53 a −2 cm y 33 cm de alto. Se apoya en dos zonas (gorra y borde trasero) y no atraviesa el suelo.

## Importar en Unreal

1. Arrastra `SK_Cangrejo.fbx` al Content Browser.
   - Skeletal Mesh: activado. Skeleton: ninguno (crea uno nuevo; renómbralo `SK_Cangrejo_Skeleton`).
   - **Import Morph Targets: activado.**
   - Import Uniform Scale: 1,0. Convert Scene: activado. Force Front XAxis: desactivado.
   - Import Animations: desactivado en este archivo.
2. Importa las texturas de `Textures/` y conéctalas en el material `M_Cangrejo`. Desactiva sRGB en Metallic y Roughness; Normal como Normalmap.
3. Arrastra los 4 FBX de `Animations/`.
   - Skeleton: `SK_Cangrejo_Skeleton`. Import Animations: activado. Import Mesh: desactivado.
   - **Import Morph Target Curves** (o «Import Custom Attribute»): activado.
   - Import Uniform Scale: 1,0.
4. En `Crab_Idle` y `Crab_Walk_Side` activa Loop. En todos, deja Root Motion desactivado.
5. Comprueba la escala: el cangrejo debe medir 50 cm de alto junto al ratón de 150 cm.
6. Comprueba los morphs: abre la malla, pestaña Morph Target Previewer, y mueve cada deslizador. En cada animación, la pestaña Curves debe listar las 7 curvas.

## Animation Blueprint

Variables (las fija el Blueprint del actor): `Speed` (float, cm/s con signo en Y), `bAttack` (bool), `bDead` (bool).

- **Idle:** `Crab_Idle` en bucle.
- **Walk:** `Crab_Walk_Side` en bucle, con **Play Rate = Speed / 45**. Al ser negativo, camina hacia −Y. Limita el valor absoluto entre 0,6 y 1,5.
- **Attack:** `Crab_Attack` sin bucle.
- **Dead:** `Crab_Dead` sin bucle; al terminar se queda en el último frame.

Transiciones:

- Idle → Walk si |Speed| > 5; Walk → Idle si |Speed| < 5. Mezcla de 0,1–0,15 s.
- Idle o Walk → Attack si `bAttack`. Mezcla de 0,05 s.
- Attack → Idle al terminar (regla automática por tiempo restante). Sin mezcla: la pose final es la del Idle.
- Cualquiera → Dead si `bDead`. Mezcla de 0,05–0,1 s. Sin salida.

Añade Anim Notifies en `Crab_Attack` (frames 9 y 13) y `Crab_Dead` (frames 4 y 26) para los eventos de las tablas.

## Lo que no se cumple del prompt

- **Tallos oculares y mandíbula:** el modelo no los tiene, así que no hay huesos `eyestalk_*` ni `jaw`. La mirada se hace girando el cuerpo.
- **Ancho de 90 cm:** mide 63 cm con 50 cm de alto.
- **Velocidad del walk:** las patas miden 7,5 cm, así que el paso sincroniza a 45 cm/s, no a 150 cm/s. Si Unreal lo mueve más rápido que unos 68 cm/s, las patas patinarán.
- **Parpadeo en el walk:** el bucle dura 0,8 s y no incluye parpadeo. Si lo quieres, anima la curva `Blink` desde el Animation Blueprint cada 3–5 s.
- **Apoyo de las patas:** las patas son rígidas y ruedan sobre su punta al caminar. El punto de apoyo no patina, pero la suela baja hasta 0,25 cm bajo el suelo y bascula durante el paso.
- **Idle → Walk:** el primer frame del walk no coincide con el Idle (diferencia de hasta 5 cm en las pinzas); necesita la mezcla de 0,1–0,15 s.
- **`Eyes_Wide` → `Eyes_X`:** durante unos 3 frames de la caída (20–23) los ojos se ven como discos blancos sin pupila.
- **`Mouth_Frown`:** deforma la zona de la línea pintada; es sutil y deja un pliegue pequeño en la comisura.
- **Intersecciones:** las revisé visualmente y con una estimación aproximada. En el ataque y en el tambaleo, las pinzas rozan el costado del cuerpo unos 2–3 cm.
- **Topología:** es la malla triangulada de Meshy, sin bucles de articulación. Las patas y las pinzas se doblan con pesos de 2 huesos; no la retopologicé.
- **Unreal:** no pude abrir Unreal. La importación, la escala, los morph targets y las mezclas del Animation Blueprint quedan por comprobar en el motor.
