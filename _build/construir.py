# -*- coding: utf-8 -*-
"""
Genera las páginas de aterrizaje de Danibox.

El header y el pie se LEEN de index.html, así que nunca se desincronizan:
si cambia el menú en la home, se corre este script y las landings quedan iguales.

    python _build/construir.py
"""
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITIO = "https://dani-box.vercel.app"   # cambiar acá cuando esté danibox.com.ar
WA = "https://wa.me/5491162575186?text="

# ---------------------------------------------------------------- datos duros
# Distancias en línea recta desde Av. Zeballos 2650 (medidas con OpenStreetMap)
# estación Castelar 0,62 km · Ituzaingó 2,17 km · Morón 2,36 km · Haedo 5,11 km
GEO = {"lat": "-34.6577433", "lon": "-58.6432122"}


def leer_index():
    t = open(os.path.join(BASE, "index.html"), encoding="utf-8").read()
    cab = re.search(r"<!-- barra de datos -->.*?</header>", t, re.S).group(0)
    pie = re.search(r"<footer class=\"pie\">.*?</footer>", t, re.S).group(0)
    wa_flot = re.search(r"<a class=\"wa-flotante\".*?</a>", t, re.S).group(0)
    # en una landing, los anclas de la home tienen que ser absolutas
    cab = re.sub(r'href="#([a-z-]+)"', r'href="/#\1"', cab)
    pie = re.sub(r'href="#([a-z-]+)"', r'href="/#\1"', pie)
    cab = cab.replace('<a class="marca" href="/#inicio"', '<a class="marca" href="/"')
    return cab, pie, wa_flot


PLANTILLA = """<!DOCTYPE html>
<html lang="es-AR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="#0e1116">
<link rel="canonical" href="{sitio}/{slug}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="geo.region" content="AR-B">
<meta name="geo.placename" content="Castelar, Morón, Buenos Aires">
<meta name="geo.position" content="{lat};{lon}">
<meta name="ICBM" content="{lat}, {lon}">

<meta property="og:type" content="article">
<meta property="og:locale" content="es_AR">
<meta property="og:site_name" content="Danibox — Escuela de Boxeo">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{sitio}/{slug}">
<meta property="og:image" content="{sitio}/assets/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">

<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@500;700;800;900&family=Barlow+Condensed:wght@500;600;700&family=Barlow:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/estilos.css">
</head>
<body>

<a class="saltar" href="#contenido">Ir al contenido</a>

{cab}

<main id="contenido">

<section class="seccion seccion--crema landing">
  <div class="contenedor contenedor--angosto">
    <nav class="miga" aria-label="Migas de pan">
      <a href="/">Inicio</a> <span>›</span> <span aria-current="page">{miga}</span>
    </nav>

    <p class="etiqueta">{etiqueta}</p>
    <h1>{h1}</h1>
    <p class="entrada">{entrada}</p>

    <div class="ctas-landing">
      <a class="btn btn--wa" href="{wa}{wa_texto}" target="_blank" rel="noopener">
        <svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 3A13 13 0 0 0 4.6 22.4L3 29l6.8-1.8A13 13 0 1 0 16 3Zm7.6 18.4c-.3.9-1.8 1.7-2.5 1.8-.7.1-1.5.1-2.5-.2-.6-.2-1.3-.4-2.2-.8-3.9-1.7-6.4-5.6-6.6-5.9-.2-.3-1.6-2.1-1.6-4s1-2.8 1.4-3.2c.4-.4.8-.5 1-.5h.8c.3 0 .6 0 .9.7l1.2 2.9c.1.2.2.5 0 .8l-.5.7-.5.5c-.2.2-.4.4-.2.8.2.4 1 1.6 2.1 2.6 1.4 1.3 2.6 1.7 3 1.8.4.2.6.2.8-.1l1.2-1.4c.3-.3.5-.3.8-.2l2.8 1.3c.3.2.6.3.7.4.1.3.1 1-.1 1.9Z"/></svg>
        {cta}
      </a>
      <a class="btn btn--linea" href="/#horarios">Ver los turnos</a>
    </div>

    <figure class="landing__foto">
      <img src="/assets/fotos/{foto}.webp" alt="{foto_alt}" width="{foto_w}" height="{foto_h}" loading="eager">
    </figure>

    {cuerpo}

    <h2>Preguntas</h2>
    <div class="faq" itemscope itemtype="https://schema.org/FAQPage">
{faq}
    </div>

    <div class="caja-cta">
      <h2>{cierre_titulo}</h2>
      <p>{cierre_texto}</p>
      <a class="btn btn--wa" href="{wa}{wa_texto}" target="_blank" rel="noopener">{cta}</a>
      <p class="caja-cta__dato">Av. Zeballos 2650, Castelar (Club Castelar) · 011 6257-5186</p>
    </div>

    <nav class="relacionadas" aria-label="Otras páginas">
      <p class="etiqueta">Seguí leyendo</p>
      <ul>
{relacionadas}
      </ul>
    </nav>
  </div>
</section>

</main>

{pie}

{wa_flot}

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "Inicio", "item": "{sitio}/" }},
        {{ "@type": "ListItem", "position": 2, "name": "{miga}", "item": "{sitio}/{slug}" }}
      ]
    }},
    {{
      "@type": "WebPage",
      "@id": "{sitio}/{slug}#pagina",
      "url": "{sitio}/{slug}",
      "name": "{title}",
      "description": "{description}",
      "inLanguage": "es-AR",
      "isPartOf": {{ "@id": "{sitio}/#sitio" }},
      "about": {{ "@id": "{sitio}/#danibox" }},
      "primaryImageOfPage": "{sitio}/assets/fotos/{foto}.webp"
    }},
    {{
      "@type": "SportsActivityLocation",
      "@id": "{sitio}/#danibox",
      "name": "Danibox — Escuela de Boxeo",
      "url": "{sitio}/",
      "telephone": "+54 11 6257-5186",
      "address": {{
        "@type": "PostalAddress",
        "streetAddress": "Av. Zeballos 2650",
        "addressLocality": "Castelar",
        "addressRegion": "Buenos Aires",
        "postalCode": "B1712",
        "addressCountry": "AR"
      }},
      "geo": {{ "@type": "GeoCoordinates", "latitude": {lat}, "longitude": {lon} }},
      "areaServed": {area_served},
      "sport": "Boxeo"
    }}
  ]
}}
</script>

<script src="/js/main.js" defer></script>
</body>
</html>
"""

FAQ_ITEM = """      <details itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
        <summary itemprop="name">{p}</summary>
        <div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">
          <p itemprop="text">{r}</p>
        </div>
      </details>"""

ZONAS = '["Castelar", "Morón", "Ituzaingó", "Haedo", "El Palomar", "Villa Tesei", "Zona Oeste del GBA"]'


def faq_html(pares):
    return "\n".join(FAQ_ITEM.format(p=p, r=r) for p, r in pares)


def relacionadas_html(items):
    return "\n".join(
        '        <li><a href="/{slug}"><strong>{t}</strong><span>{d}</span></a></li>'.format(**i)
        for i in items)


# ------------------------------------------------------------------ contenido
PAGINAS = [

{
 "slug": "boxeo-en-moron",
 "title": "Boxeo en Morón — Clases en el Club Castelar, a una estación | Danibox",
 "og_title": "Boxeo en Morón — Danibox, en el Club Castelar",
 "description": "Clases de boxeo para gente de Morón: Danibox entrena en el Club Castelar, a una estación de tren del centro de Morón. Recreativo y competitivo, todas las edades. 25 años de trayectoria.",
 "miga": "Boxeo en Morón",
 "etiqueta": "Para los que vienen de Morón",
 "h1": "Boxeo en Morón: entrenás en el Club Castelar, a una estación",
 "entrada": "Danibox es la escuela de boxeo de Dani Zamorano y funciona adentro del Club Castelar, "
            "en Av. Zeballos 2650. Castelar es parte del partido de Morón, así que no te estás yendo "
            "a otro lado: desde el centro de Morón son unos 2,5 kilómetros.",
 "foto": "bolsas-grupo",
 "foto_alt": "Alumnos de Danibox entrenando en las bolsas, en el gimnasio del Club Castelar",
 "foto_w": "1400", "foto_h": "1867",
 "cta": "Escribile a Dani",
 "wa_texto": "Hola%20Dani!%20Soy%20de%20Mor%C3%B3n%20y%20quiero%20empezar%20a%20entrenar%20boxeo.",
 "cuerpo": """
    <h2>Cómo llegar desde Morón</h2>
    <p>La estación de Morón y la de Castelar son <strong>consecutivas</strong> en el Sarmiento: hay
    una sola estación de diferencia. Bajás en Castelar y el gimnasio queda a poco más de medio
    kilómetro, unos diez minutos caminando.</p>
    <ul class="tilde">
      <li><strong>En tren:</strong> Morón → Castelar, una estación, y después diez cuadras largas.</li>
      <li><strong>En auto o moto:</strong> unos 2,5 km por Rivadavia hasta Castelar y después a Zeballos.</li>
      <li><strong>La dirección exacta:</strong> Av. Zeballos 2650, adentro del Club Castelar.</li>
    </ul>

    <h2>Qué vas a encontrar</h2>
    <p>No es un gimnasio de cintas y espejos con una clase de boxeo colgada del cronograma. Es una
    escuela de boxeo: ring de verdad, bolsas, peras, sogas y un profesor que <strong>lleva 25 años
    enseñando</strong> y conoce a cada alumno por su nombre.</p>
    <p>Entrenan hombres y mujeres, chicos, adolescentes y adultos, en el mismo grupo. El que quiere
    competir tiene camino —exhibiciones en el club, licencia de la Federación y torneos— y el que
    viene por salud o por descargar nunca está obligado a subirse al ring.</p>

    <h2>Qué turno te conviene si venís de Morón</h2>
    <p>Los turnos de lunes, miércoles y viernes son cuatro: 8:00, 16:00, 17:30 y 19:00, todos de una
    hora y media. Martes y jueves hay dos: 18:00 y 19:30. Si trabajás en Morón y salís a las seis,
    el de <strong>19:00</strong> (lunes, miércoles y viernes) o el de <strong>19:30</strong>
    (martes y jueves) te dan el tiempo del viaje sin correr.</p>
 """,
 "faq": [
   ("¿El gimnasio queda en Morón?",
    "Queda en Castelar, que es parte del partido de Morón. Desde el centro de Morón son unos 2,5 km: una estación de tren o unos minutos en auto."),
   ("¿Cuánto tardo desde la estación Morón?",
    "Una estación en el Sarmiento hasta Castelar y después unos diez minutos a pie: el gimnasio está a poco más de medio kilómetro de la estación Castelar."),
   ("¿Puedo ir a probar antes de anotarme?",
    "Sí. Escribinos por WhatsApp al 011 6257-5186, te decimos qué turno te conviene según tu edad y tu experiencia, y venís."),
   ("¿Necesito experiencia previa?",
    "No. La mayoría llega sin haberse puesto nunca un guante. Se empieza por la postura, el movimiento y la guardia."),
 ],
 "cierre_titulo": "¿Venís de Morón?",
 "cierre_texto": "Escribinos y te decimos el turno que mejor te queda según a qué hora podés llegar.",
 "relacionadas": [
   {"slug": "boxeo-desde-cero", "t": "Nunca boxeaste", "d": "Cómo es la primera clase, paso por paso"},
   {"slug": "boxeo-femenino", "t": "Boxeo femenino", "d": "Mujeres entrenando y compitiendo en Danibox"},
   {"slug": "boxeo-para-chicos", "t": "Boxeo para chicos", "d": "Chicos y adolescentes en el grupo"},
 ],
},

{
 "slug": "boxeo-en-ituzaingo",
 "title": "Boxeo en Ituzaingó — Clases a una estación, en Castelar | Danibox",
 "og_title": "Boxeo en Ituzaingó — Danibox, a una estación",
 "description": "¿Buscás clases de boxeo en Ituzaingó? Danibox entrena en el Club Castelar, a unos 2 km y una estación de tren de Ituzaingó. Recreativo, competitivo, femenino y juveniles.",
 "miga": "Boxeo en Ituzaingó",
 "etiqueta": "Para los que vienen de Ituzaingó",
 "h1": "Boxeo en Ituzaingó: la escuela está a una estación, en Castelar",
 "entrada": "Ituzaingó y Castelar son vecinos. Danibox funciona adentro del Club Castelar, en "
            "Av. Zeballos 2650, a unos dos kilómetros del centro de Ituzaingó: una estación de tren "
            "o diez minutos en auto.",
 "foto": "ring-cartel",
 "foto_alt": "El ring de Danibox con el cartel de la Escuela de Boxeo",
 "foto_w": "1400", "foto_h": "1867",
 "cta": "Escribile a Dani",
 "wa_texto": "Hola%20Dani!%20Soy%20de%20Ituzaing%C3%B3%20y%20quiero%20empezar%20a%20entrenar%20boxeo.",
 "cuerpo": """
    <h2>Cómo llegar desde Ituzaingó</h2>
    <p>En el Sarmiento, Ituzaingó y Castelar son <strong>estaciones consecutivas</strong>: una sola
    parada. Desde la estación Castelar hasta el gimnasio hay poco más de medio kilómetro, unos diez
    minutos caminando.</p>
    <ul class="tilde">
      <li><strong>En tren:</strong> Ituzaingó → Castelar, una estación.</li>
      <li><strong>En auto o moto:</strong> unos 2 km, el viaje más corto de toda la zona.</li>
      <li><strong>La dirección exacta:</strong> Av. Zeballos 2650, adentro del Club Castelar.</li>
    </ul>

    <h2>Una escuela, no una clase suelta</h2>
    <p>En Ituzaingó vas a encontrar varios lugares que dan una clase de boxeo dentro de un gimnasio
    más grande. Danibox es otra cosa: es una <strong>escuela de boxeo</strong> con ring propio,
    bolsas y peras, y un profesor que lleva 25 años enseñando el deporte y arma exhibiciones y
    torneos con su equipo.</p>
    <p>Eso cambia el día a día: se aprende técnica de verdad, se corrige uno por uno y el que quiere
    competir tiene un camino armado, con licencia de la Federación Argentina de Box incluida.</p>

    <h2>Los turnos</h2>
    <p>Lunes, miércoles y viernes: 8:00, 16:00, 17:30 y 19:00. Martes y jueves: 18:00 y 19:30.
    Cada turno dura una hora y media. Si cursás o trabajás en Ituzaingó, el viaje corto hace que
    entres cómodo a cualquiera de los turnos de la tarde.</p>
 """,
 "faq": [
   ("¿Hay clases de boxeo en Ituzaingó?",
    "Danibox funciona en Castelar, pegado a Ituzaingó: a unos 2 km del centro, una sola estación de tren. Es el gimnasio de boxeo más cercano para buena parte de Ituzaingó."),
   ("¿Cuánto tardo desde la estación Ituzaingó?",
    "Una estación hasta Castelar y después unos diez minutos a pie. En auto, unos 2 km."),
   ("¿Hay boxeo para mujeres y para chicos?",
    "Sí. El equipo es femenino y masculino desde siempre, y entrenan chicos y adolescentes junto a los adultos."),
   ("¿Qué llevo a la primera clase?",
    "Ropa cómoda, zapatillas, toalla y agua. Si todavía no tenés guantes, escribinos antes de venir y lo vemos."),
 ],
 "cierre_titulo": "¿Venís de Ituzaingó?",
 "cierre_texto": "Contanos tu edad y qué días te quedan bien, y te decimos en qué turno entrás mejor.",
 "relacionadas": [
   {"slug": "boxeo-desde-cero", "t": "Nunca boxeaste", "d": "Cómo es la primera clase, paso por paso"},
   {"slug": "boxeo-en-moron", "t": "Boxeo en Morón", "d": "Cómo llegar si venís del centro de Morón"},
   {"slug": "boxeo-para-chicos", "t": "Boxeo para chicos", "d": "Chicos y adolescentes en el grupo"},
 ],
},

{
 "slug": "boxeo-femenino",
 "title": "Boxeo femenino en Castelar y Zona Oeste — Danibox",
 "og_title": "Boxeo femenino en Castelar — Danibox",
 "description": "Boxeo femenino en el Club Castelar: el equipo de Danibox es femenino y masculino desde siempre. Clases mixtas, de cero o para competir, en Castelar (Morón), cerca de Ituzaingó y Haedo.",
 "miga": "Boxeo femenino",
 "etiqueta": "Equipo femenino",
 "h1": "Boxeo femenino en Castelar: entrenás con el mismo grupo",
 "entrada": "En Danibox el equipo es femenino y masculino desde siempre. No hay un “horario de "
            "mujeres” aparte ni una versión liviana de la clase: entrenás con el grupo, con la misma "
            "técnica y el mismo ring.",
 "foto": "cancha-grupo",
 "foto_alt": "Clase de Danibox entrenando en la cancha del Club Castelar, con alumnas y alumnos",
 "foto_w": "1400", "foto_h": "1867",
 "cta": "Consultar por el equipo femenino",
 "wa_texto": "Hola%20Dani!%20Quer%C3%ADa%20consultar%20por%20las%20clases%20de%20boxeo%20para%20mujeres.",
 "cuerpo": """
    <h2>Cómo es en la práctica</h2>
    <p>Las clases son mixtas y las dirige Dani, que lleva 25 años enseñando. Se arranca con entrada
    en calor y movimiento, se trabaja la guardia y el desplazamiento, después bolsa, soga y guanteo
    con el profe. Nadie te manda a pelear el primer día, ni el primer mes.</p>
    <p>Hay alumnas que entrenan solo por salud y por descargar la semana, y hay alumnas que compiten:
    en las exhibiciones del club y en torneos de la zona participan mujeres del equipo.</p>

    <h2>Si nunca hiciste un deporte de contacto</h2>
    <p>Es el caso más común. Lo que se enseña primero no es pegar: es pararse bien, moverse, cuidar
    la guardia y respirar. El contacto aparece mucho después y solo si vos querés.</p>
    <ul class="tilde">
      <li>No hace falta estado físico previo.</li>
      <li>No hace falta tener guantes para probar: avisanos antes y lo resolvemos.</li>
      <li>Podés venir sola: el grupo es de barrio y se ocupa de que nadie quede en un rincón.</li>
    </ul>

    <h2>Dónde queda</h2>
    <p>En el Club Castelar, Av. Zeballos 2650, Castelar (partido de Morón), a diez minutos a pie de
    la estación Castelar. Para Ituzaingó y Morón es una estación de tren; para Haedo, dos.</p>
 """,
 "faq": [
   ("¿Hay un grupo solo de mujeres?",
    "Las clases son mixtas: el equipo es femenino y masculino desde siempre y se entrena junto. Si querés consultar por un horario en particular, escribinos."),
   ("¿Tengo que pelear o subirme al ring?",
    "No. La mayoría del grupo entrena de forma recreativa y nunca compite. Competir es una opción para quien la busca y se prepara con tiempo."),
   ("¿Sirve para bajar de peso y para el estrés?",
    "Es uno de los motivos más comunes por los que la gente empieza: el boxeo mezcla trabajo aeróbico, fuerza y coordinación, y descarga muchísimo."),
   ("¿Desde qué edad se puede entrenar?",
    "Entrenan adolescentes y adultas. Escribinos por WhatsApp con la edad y te decimos en qué turno entrás mejor."),
 ],
 "cierre_titulo": "Probá una clase",
 "cierre_texto": "Escribinos por WhatsApp contando si hiciste algo de deporte antes y qué días te quedan bien.",
 "relacionadas": [
   {"slug": "boxeo-desde-cero", "t": "Nunca boxeaste", "d": "Cómo es la primera clase, paso por paso"},
   {"slug": "boxeo-en-ituzaingo", "t": "Boxeo en Ituzaingó", "d": "A una estación del centro de Ituzaingó"},
   {"slug": "boxeo-en-moron", "t": "Boxeo en Morón", "d": "Cómo llegar si venís del centro de Morón"},
 ],
},

{
 "slug": "boxeo-para-chicos",
 "title": "Boxeo para chicos y adolescentes en Castelar — Danibox",
 "og_title": "Boxeo para chicos en Castelar — Danibox",
 "description": "Boxeo para chicos y adolescentes en el Club Castelar (Morón). Disciplina, rutina y técnica con un profesor con 25 años de trayectoria. Cerca de Ituzaingó, Morón y Haedo.",
 "miga": "Boxeo para chicos",
 "etiqueta": "Chicos y adolescentes",
 "h1": "Boxeo para chicos y adolescentes en Castelar",
 "entrada": "En Danibox entrenan chicos y adolescentes junto a los adultos, en el mismo grupo y con "
            "el mismo profesor. Para muchos padres es menos una búsqueda de deporte que de rutina: "
            "un lugar donde los esperan tres veces por semana.",
 "foto": "correr",
 "foto_alt": "Alumno joven corriendo durante la entrada en calor de la clase de Danibox",
 "foto_w": "1200", "foto_h": "1600",
 "cta": "Consultar por los chicos",
 "wa_texto": "Hola%20Dani!%20Quer%C3%ADa%20consultar%20por%20las%20clases%20para%20chicos.%20La%20edad%20es%3A%20",
 "cuerpo": """
    <h2>Qué se llevan además del deporte</h2>
    <p>Es lo que más repiten los alumnos y las familias en las reseñas: acá no se enseña solamente a
    pelear. Se enseña a saludar, a esperar el turno, a bancar al compañero y a entrenar aunque ese
    día no haya ganas. Dani lo dice seguido en la clase, y lo deja escrito en el pizarrón del
    gimnasio: <em>“la disciplina vale más que la motivación”</em>.</p>

    <h2>No empiezan peleando</h2>
    <p>Al que llega por primera vez no lo mandan al ring. Arranca por la postura, el movimiento, la
    guardia y la soga, y recién después golpea la bolsa. El contacto aparece mucho más adelante, con
    cabezal y protección, y solo cuando el chico y el profe están de acuerdo.</p>

    <h2>Si después quiere competir</h2>
    <p>Hay camino: primero exhibiciones en el propio Club Castelar, para perderle el miedo al público,
    después la licencia de la <strong>Federación Argentina de Box</strong> y los torneos de la zona.
    Nada de eso es obligatorio: la mayoría entrena y no compite nunca.</p>

    <h2>Dónde y cuándo</h2>
    <p>Club Castelar, Av. Zeballos 2650, Castelar (Morón). Lunes, miércoles y viernes hay turnos a las
    8:00, 16:00, 17:30 y 19:00; martes y jueves, a las 18:00 y 19:30. Para los chicos que salen del
    colegio al mediodía, los de la tarde son los más cómodos.</p>
 """,
 "faq": [
   ("¿Desde qué edad aceptan chicos?",
    "Entrenan chicos y adolescentes, pero la edad mínima conviene consultarla: escribinos por WhatsApp al 011 6257-5186 con la edad y te decimos en qué turno entra mejor."),
   ("¿Es peligroso para un chico?",
    "Se empieza sin contacto: postura, movimiento, guardia, soga y bolsa. El guanteo aparece después, con cabezal y protección, y siempre con el profesor encima."),
   ("¿Tiene que competir?",
    "No. Competir es optativo y se prepara con tiempo. La mayor parte del grupo entrena de forma recreativa."),
   ("¿Qué necesita para la primera clase?",
    "Ropa cómoda, zapatillas, toalla y agua. Si todavía no tiene guantes, avisanos antes y lo vemos."),
 ],
 "cierre_titulo": "Contanos la edad",
 "cierre_texto": "Escribinos por WhatsApp con la edad y te decimos en qué turno entra y cómo arrancar.",
 "relacionadas": [
   {"slug": "boxeo-desde-cero", "t": "Nunca boxeaste", "d": "Cómo es la primera clase, paso por paso"},
   {"slug": "boxeo-femenino", "t": "Boxeo femenino", "d": "Mujeres entrenando y compitiendo en Danibox"},
   {"slug": "boxeo-en-ituzaingo", "t": "Boxeo en Ituzaingó", "d": "A una estación del centro de Ituzaingó"},
 ],
},

{
 "slug": "boxeo-desde-cero",
 "title": "Clases de boxeo desde cero en Castelar — Cómo es la primera clase | Danibox",
 "og_title": "Boxeo desde cero en Castelar — Danibox",
 "description": "Querés aprender a boxear desde cero: cómo es una clase de boxeo recreativo en Danibox (Club Castelar), qué llevar, qué se hace el primer día y qué NO va a pasar.",
 "miga": "Boxeo desde cero",
 "etiqueta": "Primera vez",
 "h1": "Boxeo desde cero: cómo es tu primera clase",
 "entrada": "La pregunta que más nos hacen por WhatsApp no es el precio: es “no hice nunca nada, "
            "¿puedo ir igual?”. Sí. La mayoría del grupo llegó así.",
 "foto": "pera",
 "foto_alt": "Alumno de Danibox trabajando la pera en el gimnasio",
 "foto_w": "1200", "foto_h": "1600",
 "cta": "Quiero probar una clase",
 "wa_texto": "Hola%20Dani!%20Nunca%20hice%20boxeo%20y%20quiero%20probar%20una%20clase.",
 "cuerpo": """
    <h2>Qué es el boxeo recreativo</h2>
    <p>Es entrenar boxeo de verdad —técnica, bolsa, soga, guanteo con el profesor— sin competir ni
    pelear con nadie. Se aprende a golpear bien, pero sobre todo a moverse, a cubrirse y a manejar
    la respiración. Es la forma en la que entrena la mayor parte del grupo.</p>

    <h2>Qué pasa el primer día</h2>
    <ul class="tilde">
      <li>Entrada en calor y movilidad, para soltar el cuerpo.</li>
      <li>Postura y guardia: cómo pararte, dónde van las manos, cómo mirar.</li>
      <li>Desplazamiento: moverte sin cruzar los pies.</li>
      <li>Soga y trabajo físico, al ritmo que te dé.</li>
      <li>Bolsa, para pasar a los golpes lo que acabás de aprender.</li>
    </ul>
    <p>Lo que <strong>no</strong> pasa: nadie te sube al ring, nadie te pega y nadie te hace quedar en
    ridículo adelante del grupo. Si estás muy desentrenado, se nota y se adapta.</p>

    <h2>Qué llevar</h2>
    <p>Ropa cómoda, zapatillas, toalla y una botella de agua. Nada más. Si todavía no tenés guantes,
    escribinos antes de venir y lo resolvemos. Las vendas y los guantes propios se compran después,
    cuando ya sabés que vas a seguir.</p>

    <h2>Cuándo se empieza a notar</h2>
    <p>Lo primero que cambia es el aire: en dos o tres semanas terminás la clase menos fundido. La
    técnica tarda un poco más, y ahí es donde se nota tener un profesor que corrige uno por uno en
    vez de un video. Dani lleva 25 años haciendo eso.</p>
 """,
 "faq": [
   ("¿Necesito experiencia o estado físico?",
    "No. Se empieza por la postura, el movimiento y la guardia, y cada uno va a su ritmo. La mayoría llega sin haberse puesto nunca un guante."),
   ("¿Me van a hacer pelear?",
    "No. Podés entrenar siempre de forma recreativa y no subirte nunca al ring. Competir es una opción aparte, para el que la busca."),
   ("¿Qué es el guanteo?",
    "Es practicar los golpes con el profesor, que sostiene las manoplas o los guantes. No es pelear: es la forma de corregir la técnica golpeando en movimiento."),
   ("¿Cuántas veces por semana conviene ir?",
    "Hay turnos lunes, miércoles y viernes, y martes y jueves. Con dos o tres veces por semana ya se nota; eso lo vas a charlar con Dani según tu objetivo."),
   ("¿Dónde queda?",
    "En el Club Castelar, Av. Zeballos 2650, Castelar, partido de Morón, a diez minutos a pie de la estación Castelar."),
 ],
 "cierre_titulo": "Vení a probar",
 "cierre_texto": "Escribinos por WhatsApp, contanos tu edad y qué días te quedan bien, y te decimos cuándo venir.",
 "relacionadas": [
   {"slug": "boxeo-femenino", "t": "Boxeo femenino", "d": "Mujeres entrenando y compitiendo en Danibox"},
   {"slug": "boxeo-para-chicos", "t": "Boxeo para chicos", "d": "Chicos y adolescentes en el grupo"},
   {"slug": "boxeo-en-moron", "t": "Boxeo en Morón", "d": "Cómo llegar si venís del centro de Morón"},
 ],
},
]


def main():
    cab, pie, wa_flot = leer_index()
    for p in PAGINAS:
        html = PLANTILLA.format(
            sitio=SITIO, wa=WA, cab=cab, pie=pie, wa_flot=wa_flot,
            lat=GEO["lat"], lon=GEO["lon"], area_served=ZONAS,
            faq=faq_html(p["faq"]), relacionadas=relacionadas_html(p["relacionadas"]),
            **{k: v for k, v in p.items() if k not in ("faq", "relacionadas")})
        destino = os.path.join(BASE, p["slug"] + ".html")
        open(destino, "w", encoding="utf-8").write(html)
        print("escrita", p["slug"] + ".html", len(html), "bytes")

    # sitemap con la home + las landings
    urls = [("", "1.0", "monthly")] + [(p["slug"], "0.8", "monthly") for p in PAGINAS]
    hoy = "2026-10-03"
    cuerpo = "\n".join(
        f"  <url>\n    <loc>{SITIO}/{u}</loc>\n    <lastmod>{hoy}</lastmod>\n"
        f"    <changefreq>{c}</changefreq>\n    <priority>{pr}</priority>\n  </url>"
        for u, pr, c in urls)
    open(os.path.join(BASE, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + cuerpo + "\n</urlset>\n")
    print("sitemap con", len(urls), "URLs")


if __name__ == "__main__":
    main()
