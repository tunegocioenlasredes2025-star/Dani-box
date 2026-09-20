/* Danibox — interacciones del sitio */
(function () {
  'use strict';

  /* --- menu mobile --- */
  var burger = document.getElementById('burger');
  var nav = document.getElementById('nav');

  function cerrarMenu() {
    nav.classList.remove('abierto');
    burger.setAttribute('aria-expanded', 'false');
    burger.setAttribute('aria-label', 'Abrir menú');
    document.body.style.overflow = '';
  }

  if (burger && nav) {
    burger.addEventListener('click', function () {
      var abierto = nav.classList.toggle('abierto');
      burger.setAttribute('aria-expanded', String(abierto));
      burger.setAttribute('aria-label', abierto ? 'Cerrar menú' : 'Abrir menú');
      document.body.style.overflow = abierto && window.innerWidth < 960 ? 'hidden' : '';
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') cerrarMenu();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('abierto')) cerrarMenu();
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth >= 960) cerrarMenu();
    });
  }

  /* --- turnos de clase + estado en vivo --- */
  var MANANA_Y_TARDE = [[8, 9.5], [16, 17.5], [17.5, 19], [19, 20.5]];
  var NOCHE = [[18, 19.5], [19.5, 21]];
  var TURNOS = {
    0: [],              // domingo
    1: MANANA_Y_TARDE,
    2: NOCHE,
    3: MANANA_Y_TARDE,
    4: NOCHE,
    5: MANANA_Y_TARDE,
    6: []               // sabado
  };

  function hhmm(h) {
    var hs = Math.floor(h);
    var ms = Math.round((h - hs) * 60);
    return hs + ':' + (ms < 10 ? '0' + ms : ms);
  }

  function ahoraEnBuenosAires() {
    // el sitio se ve desde cualquier lado: fijamos el huso del gimnasio
    var f = new Intl.DateTimeFormat('es-AR', {
      timeZone: 'America/Argentina/Buenos_Aires',
      weekday: 'short', hour: 'numeric', minute: 'numeric', hour12: false
    }).formatToParts(new Date());
    var v = {};
    f.forEach(function (p) { v[p.type] = p.value; });
    var dias = { 'dom': 0, 'lun': 1, 'mar': 2, 'mié': 3, 'mie': 3, 'jue': 4, 'vie': 5, 'sáb': 6, 'sab': 6 };
    var clave = (v.weekday || '').toLowerCase().replace('.', '').slice(0, 3);
    return {
      dia: dias[clave],
      hora: parseInt(v.hour, 10) + parseInt(v.minute, 10) / 60
    };
  }

  var t = ahoraEnBuenosAires();
  var fila = document.querySelector('.horarios tr[data-dia="' + t.dia + '"]');
  if (fila) fila.classList.add('hoy');

  var estado = document.getElementById('estado');
  if (estado && typeof t.dia === 'number') {
    var DIAS = ['domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado'];
    var hoy = TURNOS[t.dia] || [];
    var enCurso = null, siguienteHoy = null;

    hoy.forEach(function (turno) {
      if (t.hora >= turno[0] && t.hora < turno[1]) enCurso = turno;
      else if (turno[0] > t.hora && !siguienteHoy) siguienteHoy = turno;
    });

    if (enCurso) {
      estado.textContent = 'Clase en curso · termina ' + hhmm(enCurso[1]);
      estado.className = 'tira__item abierto';
    } else if (siguienteHoy) {
      estado.textContent = 'Hoy hay clase a las ' + hhmm(siguienteHoy[0]);
      estado.className = 'tira__item abierto';
    } else {
      var prox = null;
      for (var i = 1; i <= 7 && !prox; i++) {
        var dia = (t.dia + i) % 7;
        if ((TURNOS[dia] || []).length) prox = { nombre: DIAS[dia], hora: TURNOS[dia][0][0] };
      }
      estado.textContent = prox
        ? 'Próxima clase: ' + prox.nombre + ' ' + hhmm(prox.hora)
        : 'Sin clases hoy';
      estado.className = 'tira__item cerrado';
    }
    estado.hidden = false;
  }

  /* --- revelar al hacer scroll --- */
  var objetivos = document.querySelectorAll('.seccion .dos, .cards > *, .opiniones > *, .pasos > *, .galeria figure, .faq, .horarios');
  if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var io = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    objetivos.forEach(function (el, i) {
      el.classList.add('revelar');
      el.style.transitionDelay = Math.min(i % 4, 3) * 70 + 'ms';
      io.observe(el);
    });
    // red de seguridad: si algo falla, nada queda invisible
    setTimeout(function () {
      objetivos.forEach(function (el) { el.classList.add('visible'); });
    }, 6000);
  }

  /* --- el clip de la galeria: carga y arranca solo cuando se ve --- */
  var clip = document.getElementById('clip');
  if (clip && 'IntersectionObserver' in window) {
    var quieto = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    new IntersectionObserver(function (entradas) {
      entradas.forEach(function (e) {
        if (e.isIntersecting) {
          if (!clip.src) clip.src = clip.dataset.src;
          if (!quieto) { var pr = clip.play(); if (pr && pr.catch) pr.catch(function () {}); }
        } else if (!clip.paused) {
          clip.pause();
        }
      });
    }, { threshold: 0.35 }).observe(clip);
  }

  /* --- año del pie --- */
  var anio = document.getElementById('anio');
  if (anio) anio.textContent = '© ' + new Date().getFullYear();
})();
