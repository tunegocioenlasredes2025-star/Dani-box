# Danibox — Escuela de Boxeo (Castelar)

Sitio one-page para **Danibox**, la escuela de boxeo de Daniel "Dani" Zamorano dentro del
Club Castelar (Av. Zeballos 2650, Castelar, Morón). Hecho por
[Tu Negocio En Las Redes](https://tunegocioenlasredes.com.ar).

## Stack

HTML + CSS + JavaScript vanilla. Sin build, sin dependencias, sin framework.
Se sirve tal cual está: pensado para Vercel (proyecto estático).

```
index.html            página completa
css/estilos.css       estilos (mobile-first, tokens en :root)
js/main.js            menú, estado abierto/cerrado, horario de hoy, animaciones
assets/               logo, favicon, og
assets/fotos/         fotos optimizadas en webp (versión grande + -800 para mobile)
insumos/              NO se publica (gitignored): análisis, fotos originales, script de proceso
```

## Datos del negocio usados en el sitio

| Dato | Valor |
|---|---|
| Dirección | Av. Zeballos 2650, Castelar (Club Castelar), Morón |
| Teléfono / WhatsApp | 011 6257-5186 → `wa.me/5491162575186` |
| Instagram | [@boxeo.danibox](https://www.instagram.com/boxeo.danibox/) |
| Horarios | Lun, Mié y Vie 8–22 · Mar y Jue 18–21 · Sáb y Dom cerrado |
| Google | 4,4 ★ (7 opiniones) |

Si cambia alguno, hay que tocarlo en **tres lugares**: el HTML visible, el bloque
`application/ld+json` del final y —si es el horario— la constante `HORARIOS` de `js/main.js`.

## Desarrollo local

```bash
python -m http.server 5195
```

Y abrir http://localhost:5195. (En Claude Code está como configuración `danibox` en el
`launch.json` de la carpeta "Futbol playa".)

## Fotos

Las fotos salen de Google Maps y del Instagram del cliente. `insumos/procesar-fotos.py`
las recorta, les aplica un tratamiento parejo (contraste + virado cálido para emparejar
fotos de celular de distinta calidad) y las exporta a webp en dos tamaños.

```bash
python insumos/procesar-fotos.py
```

**Pendiente:** conseguir el logo en alta (hoy sale del avatar de Instagram, 150 px
escalado) y fotos propias del gimnasio.

## Deploy

Vercel conectado a este repo, rama `main`. Framework preset: **Other** (sitio estático,
sin build command). `vercel.json` define cleanUrls y el cacheo largo de `/assets`.

> Si se cambia una foto, conviene cambiarle el nombre al archivo: `/assets` va con
> cache inmutable por un año.
