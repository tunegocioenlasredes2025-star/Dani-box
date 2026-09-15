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

  /* --- horario de hoy + abierto/cerrado --- */
  var HORARIOS = {
    0: null,            // domingo
    1: [8, 22],
    2: [18, 21],
    3: [8, 22],
    4: [18, 21],
    5: [8, 22],
    6: null             // sabado
  };

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
    var hoy = HORARIOS[t.dia];
    var abierto = !!hoy && t.hora >= hoy[0] && t.hora < hoy[1];
    if (abierto) {
      estado.textContent = 'Abierto ahora · hasta las ' + hoy[1] + ':00';
      estado.className = 'tira__item abierto';
    } else {
      var d = t.dia;
      var prox = null;
      for (var i = 1; i <= 7; i++) {
        var siguiente = HORARIOS[(d + i) % 7];
        if (siguiente) {
          prox = { nombre: ['domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado'][(d + i) % 7], hora: siguiente[0] };
          break;
        }
      }
      if (hoy && t.hora < hoy[0]) {
        estado.textContent = 'Cerrado · abre hoy ' + hoy[0] + ':00';
      } else if (prox) {
        estado.textContent = 'Cerrado · abre ' + prox.nombre + ' ' + prox.hora + ':00';
      } else {
        estado.textContent = 'Cerrado ahora';
      }
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

  /* --- año del pie --- */
  var anio = document.getElementById('anio');
  if (anio) anio.textContent = '© ' + new Date().getFullYear();
})();
