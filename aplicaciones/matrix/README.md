# Matrix Engine

Visor 3D con filtro ASCII en estilo Win98. Dos motores unificados:

- `index.html` — visor web (Three.js + AsciiEffect). Importa `.glb/.gltf/.stl`, alterna vista ASCII/RAW, captura SNAP en alta resolución y graba REC en WebM.
- `python/matrix_engine.py` — motor de escritorio (PyQt6 + OpenCV + NumPy) con tres modos: `pure`, `rain` y `desktop`.

## Estructura

```
matrix/
├─ index.html                 entrada web (canónico)
├─ assets/models/             mask.glb (activo), windows pc.glb, 1.stl
├─ python/
│  ├─ matrix_engine.py        motor unificado
│  ├─ test_matrix_engine.py   pruebas del núcleo de procesamiento
│  └─ test_matrix_engine_ui.py pruebas de interfaz (Qt offscreen)
├─ _archive/                  versiones anteriores (html, python, assets)
└─ README.md
```

## Uso

### Web

Abrir `index.html` en el navegador. Requiere conexión para cargar Three.js desde unpkg.

- `IMPORT` — carga un modelo local (`.glb`, `.gltf`, `.stl`).
- `VIEW` — alterna entre `MATRIX_ASCII` y `MATRIX_RAW`.
- `SNAP` — descarga un PNG del fotograma actual (ASCII a 3x, RAW a 2x).
- `REC` — graba el viewport en WebM (VP9, 60 fps).

El modelo inicial se carga desde `assets/models/mask.glb`. Si no está disponible, el visor queda en `EMPTY` y se puede importar otro archivo.

La rejilla ASCII se ajusta al viewport: `fitAsciiGrid()` mide el avance real de la fuente resuelta por el navegador y calcula `letter-spacing` y `line-height` para que la última columna y la última fila lleguen al borde. Las capturas (SNAP/REC) reutilizan esas mismas métricas, así que coinciden con la pantalla.

### Python

```bash
python matrix_engine.py --mode desktop
python matrix_engine.py --mode pure
python matrix_engine.py --mode rain --cols 180
```

Dependencias: `PyQt6`, `opencv-python`, `numpy`.

| Modo | Comportamiento |
| --- | --- |
| `pure` | ASCII de cámara o video, columnas fijas (`--cols`). |
| `rain` | Igual que `pure`, con efecto de lluvia (generación y destruction de caracteres). |
| `desktop` | Escalado al ancho del visor, selector de color de fondo/frente, tamaño de dígito, F11 a pantalla completa. |

Controles: `START CAM`, `DEVICE` (cambia de cámara), `LOAD VIDEO`, `DIGIT SIZE`, `BG COLOR`, `FG COLOR`.

## Pruebas

```bash
python -m pytest test_matrix_engine.py test_matrix_engine_ui.py -q
```

`test_matrix_engine_ui.py` corre la interfaz Qt en modo offscreen (`QT_QPA_PLATFORM=offscreen`).

## Archivo

`_archive/` conserva el historial: versiones HTML previas (incluida la base `matrix version final 3.0.html`), los scripts PyQt originales y el `mask.glb` de alta resolución (68 MB), archivado por no ser el activo. El modelo activo es la versión ligera (2 MB).
