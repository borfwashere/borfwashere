# GifSweeper

Editor de GIF con estética Win95. `index.html` unifica las antiguas ramas **GifSweeper** y **KlearMine / Klear.me**, que eran el mismo programa con distinta piel.

## Uso

Abrir `index.html` en el navegador. Requiere conexión para cargar gifler.js y gif.js desde CDN.

Arranca con una secuencia animada de 8 frames (sprite sheet PNG embebido como data URI en `DEFAULT_SHEET`), así que el canvas nunca queda vacío. Se reproduce con `requestAnimationFrame` a 130 ms por frame y no depende de `gifler`, que se usa solo para los GIFs que cargues. Para recuperarla tras usar `X`, recarga la página.

- `LOAD` — cargar un GIF local.
- `GET` — cargar un GIF desde URL (puede fallar por CORS según el servidor).
- Clic en el canvas — muestrear hasta 3 colores para eliminar por similitud.
- Slider — umbral de luminancia (0–255) para transparencia.
- Cara — rotar entre los 6 efectos de composición.
- `GIF` — iniciar/detener la captura y exportar el GIF.
- `WEBM` — iniciar/detener la grabación y exportar WebM (VP8, 2.5 Mbps, 30 fps).

## Efectos

`copy`, `darker`, `source-over`, `source-out`, `destination-over`, `destination-out` (ver `lista de efectos.txt`).

## Notas

- El worker de gif.js se descarga una sola vez y se reutiliza.
- Al cambiar de GIF durante una grabación, la captura se detiene para evitar mezclar tamaños de frame.
- `_archive/html/` conserva las 12 versiones anteriores, incluida la que bloqueaba F12/Ctrl+U.
