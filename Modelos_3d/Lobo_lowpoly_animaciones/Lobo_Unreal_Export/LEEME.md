# Lobo (villano) — exportación para Unreal

Generado a partir del FBX riggeado de `Lobo_lowpoly_animaciones`. Todos los archivos comparten unidades (cm), ejes (Z arriba, personaje mirando a +X) y escala 1.

## Archivos

| Archivo | Contenido |
|---|---|
| `SK_Lobo.fbx` | Personaje en A-pose con esqueleto, pesos, material y 11 morph targets. 39354 triángulos, 62 huesos, máx. 4 influencias por vértice. Sin lentes. |
| `SM_Lobo_Glasses.fbx` | Lentes como malla aparte, con el origen en `GlassesSocket`. |
| `Animations/A_Lobo_*.fbx` | 10 archivos: 9 clips y la pose de referencia. Cada uno incluye la misma malla, esqueleto y pesos, y las 11 curvas de morph targets. |
| `Textures/T_Lobo_BaseColor.png` | Color base (el del FBX original, con cuatro muestras de color añadidas en una esquina libre). |
| `Preview_Lobo.mp4` | Vista previa de los clips en el orden de la secuencia, con primer plano de la cara; los bucles se repiten 5 veces. |
| `Expresiones_MorphTargets.png` | Cada morph target al 100 %, con los lentes ocultos. |

## Clips

Todos a 30 fps. En los bucles, el último frame es idéntico al primero (huesos y morphs).

| Clip | Frames | Duración | Bucle | Expresión (morphs y orejas) | Fotogramas clave |
|---|---|---|---|---|---|
| `A_Lobo_RefPose` | 1 | — | — | Neutra | Pose de referencia |
| `A_Lobo_Reveal_Pose` | 60 | 2,0 s | No, mantener el último | `Mouth_Smirk` 1, `Brow_Up_L` 1; orejas erguidas | Empieza de perfil (girado 78° a su izquierda); remata la pose en el 30; estable desde el 44 |
| `A_Lobo_Idle_Smug` | 120 | 4,0 s | Sí | `Mouth_Smirk` 0,75–1, `Brow_Up_L` al tocar los lentes, 2 parpadeos | Se ajusta los lentes con la mano izquierda del 30 al 80 (toque del 46 al 60) |
| `A_Lobo_Talk` | 60 | 2,0 s | Sí | `Mouth_Open` (hasta 0,75) + hueso `jaw`, alternando con `Mouth_Smirk`; `Brow_Up_L` | Abre la boca 3 veces por ciclo; se señala con el pulgar izquierdo 2 veces |
| `A_Lobo_Triumph_Pose` | 54 | 1,8 s | No, mantener el último | `Mouth_Open` 1 riendo, `Brow_Up` 1; orejas erguidas | Anticipación hasta el 10; brazos arriba en el 18; estable desde el 40 |
| `A_Lobo_Launched_Tumble` | 30 | 1,0 s | Sí | `Mouth_O` 1, `Brow_Up` 1, `Brow_Sad` 0,4; orejas hacia atrás | `root` no rota: la pelvis solo se balancea |
| `A_Lobo_Land_Stuck` | 60 | 2,0 s | No | `Mouth_O` → `Brow_Angry` 1 + `Mouth_Frown` 1 | Impacto en el 4; rebote en el 10; pataleo desde el 16; el último frame es el 0 del bucle |
| `A_Lobo_Land_Stuck_Loop` | 30 | 1,0 s | Sí | `Brow_Angry` 1, `Mouth_Frown` 1 | Pataleo de piernas y cola |
| `A_Lobo_Defeat` | 70 | 2,33 s | No, mantener el último | `Mouth_O` 1 + `Brow_Up` → `Eyes_Dizzy` 1 + `Mouth_Open` 0,6 + `Brow_Sad` 1; orejas caídas | Golpe en el 4; pirueta de 360° del 9 al 34; cae del 34 al 46; **impacto contra el suelo en el 46**; segundo rebote en el 56 |
| `A_Lobo_Defeated_Loop` | 90 | 3,0 s | Sí | `Eyes_Dizzy` 1, `Mouth_Open` 0,6–0,75 con lengua, `Brow_Sad` 1; orejas caídas | La mano derecha se levanta y cae del 28 al 51; la pierna izquierda tiembla del 58 al 76 |

**Lentes en `A_Lobo_Defeat`:** tuércelos en el frame 4 (golpe) y suéltalos en el frame 46 (impacto contra el suelo). `Eyes_Dizzy` ya está al 100 % en ese frame.

## Derrota: dirección y espacio

- Cae **hacia atrás (−X)**: la cabeza queda hacia −X y los pies hacia +X, con la pelvis en X = −14 cm.
- Tumbado ocupa de X = -89 a 83 cm y de Y = -74 a 71 cm (brazos abiertos). Radio máximo respecto a `root`: 105 cm.
- La cola queda apoyada en el suelo hacia su derecha (−Y).

## Caída en el expositor

- En `A_Lobo_Land_Stuck` y su bucle, `root` es el punto de la superficie del cojín por donde entra.
- El cuerpo queda boca abajo y todo lo que está por debajo de Z = 0 se supone dentro del expositor: la cabeza llega a Z = -63 cm en el impacto y a Z = -54 cm en el bucle. Los brazos van extendidos hacia abajo, así que quedan ocultos.
- Si tu expositor es menos profundo, sube el actor esa diferencia.

## Esqueleto

- Raíz única `root` en el suelo y `pelvis` separada. Nombres del UE5 Mannequin: `spine_01`–`03`, `neck_01`, `head`, `clavicle_*`, `upperarm_*`, `lowerarm_*`, `hand_*`, `thigh_*`, `calf_*`, `foot_*`, `ball_*`.
- Dedos: `thumb`, `index`, `middle`, `ring` y `pinky`, cada uno con `_01`–`_03`, con pesos.
- Extras: `tail_01`–`tail_05`, `ear_l`, `ear_r`, `jaw`.
- `GlassesSocket`: hueso hijo de `head` en (11, 0, 153.4) cm, sin rotación respecto al mundo en la pose de referencia. Acopla `SM_Lobo_Glasses` a ese hueso (o a un socket sobre él) con transformación relativa cero.
- El esqueleto tiene 3 huesos de columna y 1 de cuello; el Mannequin de UE5 tiene 5 y 2. Para retargeting, asigna las cadenas en el IK Rig.

## Morph targets

`Brow_Up`, `Brow_Up_L`, `Brow_Angry`, `Brow_Sad`, `Mouth_Smirk`, `Mouth_Smile`, `Mouth_Frown`, `Mouth_Open`, `Mouth_O`, `Blink`, `Eyes_Dizzy`.

- Cejas, sonrisas y parpadeo desplazan la piel de la cara, que lleva esos rasgos pintados.
- `Mouth_Open`, `Mouth_O` y `Eyes_Dizzy` usan geometría nueva (146 vértices): interior de boca, lengua, dientes y discos con una X. En reposo está encogida y oculta dentro de la cabeza, y el morph la saca a la superficie.
- `Brow_Up_L` es la ceja izquierda del personaje (+Y).

## Importación en Unreal

1. Importa `SK_Lobo.fbx` como Skeletal Mesh con escala 1, **Import Morph Targets** activado y sin "Force Front XAxis".
2. Importa los clips eligiendo el esqueleto de `SK_Lobo`, desmarcando "Import Mesh". Las curvas llegan con el mismo nombre que cada morph target.
3. Marca como bucle: Idle_Smug, Talk, Launched_Tumble, Land_Stuck_Loop y Defeated_Loop.
4. Importa `SM_Lobo_Glasses.fbx` como Static Mesh y acóplalo a `GlassesSocket`.
5. Comprueba que mida 175 unidades de alto y mire a +X.

## Validación realizada

Comprobado reimportando cada FBX en Blender y midiendo la malla deformada en cada frame:

- Mismos 62 huesos, jerarquía, pose de referencia y malla en los 11 archivos del personaje; mismas unidades y ejes en los 12 FBX.
- Las 11 curvas de morph están en los 10 archivos de animación con el nombre exacto.
- Escala de huesos constante (desviación máxima 0,000002) y `root` inmóvil en todos los clips.
- Altura en pose de referencia: 174.9 cm con las orejas.
- Idle_Smug y Talk: suelas entre -0.11 y -0.00 cm del suelo, con un desplazamiento máximo de 0.06 cm.
- Triumph_Pose: se pone de puntillas; la puntera baja hasta -1.6 cm.
- Defeat: el punto más bajo del cuerpo llega a -4.1 cm durante un frame (punta de la cola en el 38) y a −2 cm en el impacto. Defeated_Loop: entre -2.4 y −1,1 cm (la base de la cola y la cabeza se hunden ligeramente).

## Limitaciones y cambios respecto a lo pedido

- **Texturas de `Animaciones_villano`:** no corresponden a esta malla; su distribución de UV es distinta. Usé el color base que trae el FBX riggeado, así que no hay mapas de normales, metálico ni rugosidad.
- **Aspecto menos low-poly:** subdividí y suavicé la malla (de 8 337 a 39354 triángulos) conservando silueta, UV y textura. No es una retopología manual.
- **Altura y centrado:** escalé el modelo un 2,9 % (de 170 a 175 cm) y lo desplacé 16,5 cm para que `root` quede bajo el cuerpo.
- **Pesos:** conservé los del rig original en cuerpo, brazos y piernas. Generé los de cola, orejas, mandíbula y dedos; la cola estaba pesada al muslo derecho.
- **Cejas:** el flequillo las tapa en parte, así que su movimiento se lee menos que el de la boca.
- **`Eyes_Dizzy`:** asoma unos 2 mm por encima de los lentes cuando siguen puestos.
- **Pies en los giros:** en Reveal_Pose y en la pirueta de Defeat los pies giran alrededor de `root` deslizándose, sin dar pasos.
- **Muñecas:** el antebrazo gira hasta 85° en algún frame de Talk y Defeat; la mitad se reparte en el antebrazo y la otra mitad en la muñeca.
- **Intersecciones:** las revisé solo visualmente en las hojas de contacto; no medí cruces entre camisa, cadena, cola y extremidades.
- **Unreal:** no pude abrir Unreal. La importación de morph targets, el socket de los lentes, la escala y la secuencia completa quedan por comprobar en el motor.
