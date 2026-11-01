/* North Star Terminal · NOTICIAS, SEGUIMIENTO (con alertas), CALENDARIO, AYUDA, MCP y ESTADO */
'use strict';
(function (N) {
  const { F, esc, $, $$, D, UI, App, Local } = N;

  // ───────────────────────── NOTICIAS ─────────────────────────
  const ORIGEN = { equipo: ['EQUIPO', 'acc'], lseg: ['LSEG', 'info'], google: ['GOOGLE', ''], yahoo: ['YAHOO', ''] };
  const Noticias = {
    tarjeta(n, { corta = false, sinEmisora = false } = {}) {
      const [o, oc] = ORIGEN[n.origen] || [String(n.origen || '').toUpperCase(), ''];
      const fecha = String(n.fecha || '');
      const t = n.t && n.t !== 'MERCADO' && D.U[n.t] ? UI.sym(n.t) : '<span class="chip">MERCADO</span>';
      return `<article class="noti ${esc(n.tono || '')}">
        <div class="h">${esc(F.fechaCorta(fecha.slice(0, 10)))}<br>${esc(fecha.slice(11, 16))}</div>
        <div class="tit">${n.url ? `<a href="${esc(n.url)}" target="_blank" rel="noopener">${esc(n.titulo)}</a>` : esc(n.titulo)}</div>
        <div class="meta">${sinEmisora ? '' : t}<span>${esc(n.fuente || '')}</span><span class="chip ${oc}">${o}</span>
          ${n.tono && n.tono !== 'neutral' ? `<span class="chip ${n.tono === 'positiva' ? 'pos' : 'neg'}">${n.tono}${n.tono_auto ? ' · auto' : ''}</span>` : ''}
          ${n.impacto ? `<span class="chip warn">impacto ${esc(n.impacto)}</span>` : ''}</div>
        ${!corta && n.resumen ? `<div class="res">${esc(n.resumen)}</div>` : ''}
      </article>`;
    },
    lista(el, items, { sinEmisora = false } = {}) {
      const st = { q: '', tono: '', origen: '' };
      el.innerHTML = `<div class="graf-barra"><input placeholder="Buscar en titulares…" data-f="q" style="width:220px">
        <select data-f="tono"><option value="">Todo tono</option><option value="positiva">Positivas</option><option value="negativa">Negativas</option><option value="neutral">Neutrales</option></select>
        <select data-f="origen"><option value="">Todo origen</option><option value="equipo">Equipo</option><option value="lseg">LSEG</option><option value="google">Google Noticias</option></select>
        <span class="dim" data-n></span></div><div class="panel"><div class="panel-b p0" data-l></div></div>`;
      const pintar = () => {
        const q = st.q.toLowerCase();
        const xs = items.filter((n) => (!st.tono || n.tono === st.tono) && (!st.origen || n.origen === st.origen) &&
          (!q || (n.titulo + ' ' + (n.resumen || '')).toLowerCase().includes(q)));
        $('[data-n]', el).textContent = `${xs.length} noticias`;
        $('[data-l]', el).innerHTML = xs.slice(0, 300).map((n) => Noticias.tarjeta(n, { sinEmisora })).join('') || '<div class="vacio">Sin noticias con ese filtro.</div>';
      };
      $$('[data-f]', el).forEach((c) => c.addEventListener('input', () => { st[c.dataset.f] = c.value; pintar(); }));
      pintar();
    },
  };
  N.Noticias = Noticias;

  App.registrar('noticias', {
    titulo: () => 'Noticias',
    pintar(cont, args) {
      const sel = (args[0] || '').toUpperCase();
      const sectores = [...new Set(D.emisoras().map((e) => e.sector))].sort();
      cont.innerHTML = `${UI.titulo('Noticias', 'Equipo y LSEG (noticias.txt) más Google Noticias en español, actualizadas por GitHub Actions')}
        <div class="graf-barra"><select id="nEm"><option value="">Todas las emisoras</option><option value="MERCADO" ${sel === 'MERCADO' ? 'selected' : ''}>Mercado general</option>
          ${D.emisoras().map((e) => `<option value="${e.t}" ${sel === e.t ? 'selected' : ''}>${e.t} · ${esc(e.n)}</option>`).join('')}</select>
          <select id="nSec"><option value="">Todos los sectores</option>${sectores.map((s) => `<option>${esc(s)}</option>`).join('')}</select></div><div id="nLista"></div>`;
      const pintar = () => {
        const t = $('#nEm', cont).value, s = $('#nSec', cont).value;
        const xs = D.noticias.filter((n) => (!t || n.t === t) && (!s || (D.U[n.t] && D.U[n.t].sector === s)));
        Noticias.lista($('#nLista', cont), xs);
      };
      $('#nEm', cont).addEventListener('change', pintar); $('#nSec', cont).addEventListener('change', pintar);
      pintar();
    },
  });

  // ───────────────────────── SEGUIMIENTO y alertas ─────────────────────────
  const Alertas = {
    lista() { return Local.leer('alertas', []); },
    guardar(xs) { Local.guardar('alertas', xs); },
    revisar() {
      const xs = this.lista(); let cambio = false;
      xs.forEach((a) => {
        const q = D.cot(a.t); if (!q.p || a.disparada) return;
        const ok = a.tipo === 'arriba' ? q.p >= a.valor : a.tipo === 'abajo' ? q.p <= a.valor : Math.abs((q.cp || 0) * 100) >= a.valor;
        if (ok) {
          a.disparada = new Date().toISOString(); cambio = true;
          N.toast(`<b class="acc">ALERTA ${esc(a.t)}</b> · ${a.tipo === 'cambio' ? `se movió ${F.pctS(q.cp)}` : `${a.tipo === 'arriba' ? 'subió a' : 'bajó a'} ${F.precio(q.p)}`} (objetivo ${a.tipo === 'cambio' ? '±' + a.valor + '%' : F.precio(a.valor)})`, 9000);
          try { if (window.Notification && Notification.permission === 'granted') new Notification(`North Star · ${a.t}`, { body: `Precio ${F.precio(q.p)}` }); } catch (e) { /* sin permiso */ }
        }
      });
      if (cambio) this.guardar(xs);
    },
  };
  N.Alertas = Alertas;

  App.registrar('seg', {
    titulo: () => 'Seguimiento',
    pintar(cont) {
      const fondo = ((D.port && D.port.actual && D.port.actual.posiciones) || []).map((p) => p.t);
      const listas = Local.leer('listas', { 'Mi lista': ['FEMSAUBD', 'GMEXICOB', 'WALMEX', 'GFNORTEO'] });
      const nombres = ['Fondo', ...Object.keys(listas)];
      let actual = Local.leer('lista:actual', 'Fondo'); if (!nombres.includes(actual)) actual = 'Fondo';
      const ts = actual === 'Fondo' ? fondo : listas[actual] || [];
      const alertas = Alertas.lista();
      cont.innerHTML = `${UI.titulo('Seguimiento', 'Listas propias y alertas de precio · se guardan en este navegador')}
        <div class="graf-barra">${nombres.map((n) => `<button class="btn sm ${n === actual ? 'on' : ''}" data-l="${esc(n)}">${esc(n.toUpperCase())}</button>`).join('')}
          <button class="btn sm" id="sNueva">+ LISTA</button><span class="sep"></span>
          ${actual !== 'Fondo' ? `<select id="sAdd"><option value="">+ agregar emisora</option>${D.emisoras().filter((e) => !ts.includes(e.t)).map((e) => `<option value="${e.t}">${e.t} · ${esc(e.n)}</option>`).join('')}</select>` : '<span class="dim">La lista «Fondo» son las posiciones actuales.</span>'}</div>
        <div class="rejilla g21">${UI.panel(esc(actual), '<div id="sTabla"></div>', { p0: true })}
          ${UI.panel('Alertas', `<div class="criterio" style="grid-template-columns:1fr 1fr 1fr auto"><select id="aT">${D.emisoras().map((e) => `<option>${e.t}</option>`).join('')}</select>
            <select id="aTipo"><option value="arriba">precio ≥</option><option value="abajo">precio ≤</option><option value="cambio">cambio diario ± %</option></select>
            <input id="aV" type="number" step="any" placeholder="valor"><button class="btn sm" id="aAdd">AGREGAR</button></div>
            <table class="t" style="margin-top:6px"><tbody>${alertas.map((a, i) => `<tr><td class="i">${UI.sym(a.t)}</td><td class="i">${a.tipo === 'cambio' ? `± ${a.valor}%` : `${a.tipo === 'arriba' ? '≥' : '≤'} ${F.precio(a.valor)}`}</td>
              <td class="i">${a.disparada ? `<span class="chip warn">disparada ${F.fechaHora(a.disparada)}</span>` : '<span class="chip">activa</span>'}</td><td><button class="btn sm" data-x="${i}">✕</button></td></tr>`).join('') || '<tr><td class="i dim">Sin alertas. Se revisan cada vez que llegan precios nuevos mientras la terminal está abierta.</td></tr>'}</tbody></table>
            <button class="btn sm" id="aNotif" style="margin-top:8px">ACTIVAR NOTIFICACIONES DEL NAVEGADOR</button>`)}</div>`;
      UI.tabla($('#sTabla', cont), [
        { k: 't', t: 'Emisora', i: true, f: (x) => UI.sym(x.t, { nombre: true }) }, { k: 'p', t: 'Último', f: (x) => F.precio(x.p) },
        { k: 'cp', t: 'Hoy', f: (x) => UI.cambio(x.cp) }, { k: 'r1m', t: '1M', f: (x) => UI.cambio(x.r1m, 1) }, { k: 'ytd', t: 'Año', f: (x) => UI.cambio(x.ytd, 1) },
        { k: 'r52', t: '52 sem.', f: (x) => UI.rango(x.lo, x.hi, x.p) }, { k: 'spk', t: '30 días', f: (x) => N.spark(D.serie(x.t, 30), { w: 70, h: 18 }) },
        { k: 'not', t: 'Noticias 7d', f: (x) => (x.not ? `<span class="chip info">${x.not}</span>` : '<span class="dim">0</span>') },
        ...(actual !== 'Fondo' ? [{ k: 'q', t: '', f: (x) => `<button class="btn sm" data-quitar="${x.t}">✕</button>` }] : []),
      ], ts.map((t) => {
        const q = D.cot(t), lim = new Date(Date.now() - 7 * 864e5).toISOString().slice(0, 10);
        return { t, p: q.p, cp: q.cp, r1m: D.rend(t, 21), ytd: D.rendYTD(t), lo: q.lo52, hi: q.hi52, not: D.noticias.filter((n) => n.t === t && (n.fecha || '') >= lim).length };
      }), { alClic: (t) => App.ir(`#/eq/${t}`) });
      $$('[data-l]', cont).forEach((b) => b.addEventListener('click', () => { Local.guardar('lista:actual', b.dataset.l); App.pintar(); }));
      $('#sNueva', cont).addEventListener('click', () => { const n = prompt('Nombre de la lista nueva'); if (n && !listas[n] && n !== 'Fondo') { listas[n] = []; Local.guardar('listas', listas); Local.guardar('lista:actual', n); App.pintar(); } });
      const add = $('#sAdd', cont); if (add) add.addEventListener('change', () => { if (add.value) { listas[actual] = [...ts, add.value]; Local.guardar('listas', listas); App.pintar(); } });
      $$('[data-quitar]', cont).forEach((b) => b.addEventListener('click', (ev) => { ev.stopPropagation(); listas[actual] = ts.filter((t) => t !== b.dataset.quitar); Local.guardar('listas', listas); App.pintar(); }));
      $('#aAdd', cont).addEventListener('click', () => {
        const v = parseFloat($('#aV', cont).value); if (!N.esNum(v)) { N.toast('Escriba un valor para la alerta.'); return; }
        Alertas.guardar([...alertas, { t: $('#aT', cont).value, tipo: $('#aTipo', cont).value, valor: v }]); Alertas.revisar(); App.pintar();
      });
      $$('[data-x]', cont).forEach((b) => b.addEventListener('click', () => { alertas.splice(+b.dataset.x, 1); Alertas.guardar(alertas); App.pintar(); }));
      $('#aNotif', cont).addEventListener('click', () => { try { Notification.requestPermission(); } catch (e) { N.toast('Este navegador no permite notificaciones.'); } });
    },
    vivo: true,
  });

  // ───────────────────────── CALENDARIO ─────────────────────────
  App.registrar('cal', {
    titulo: () => 'Calendario',
    pintar(cont) {
      const hoy = new Date().toISOString().slice(0, 10);
      const modo = Local.leer('cal:modo', 'proximos');
      const fondo = new Set(((D.port && D.port.actual && D.port.actual.posiciones) || []).map((p) => p.t));
      const xs = (D.cal.eventos || []).filter((e) => (modo === 'proximos' ? e.fecha >= hoy : e.fecha < hoy));
      if (modo !== 'proximos') xs.reverse();
      const porFecha = {}; xs.forEach((e) => { (porFecha[e.fecha] = porFecha[e.fecha] || []).push(e); });
      cont.innerHTML = `${UI.titulo('Calendario', 'Reportes trimestrales, dividendos y eventos · equipo, LSEG y Yahoo Finance')}
        <div class="graf-barra"><button class="btn sm ${modo === 'proximos' ? 'on' : ''}" data-m="proximos">PRÓXIMOS</button><button class="btn sm ${modo !== 'proximos' ? 'on' : ''}" data-m="pasados">PASADOS</button></div>
        <div class="panel"><div class="panel-b p0"><table class="t"><tbody>${Object.keys(porFecha).map((f) => `<tr class="grupo"><td colspan="4">${F.fecha(f)}${f === hoy ? ' · HOY' : ''}</td></tr>${porFecha[f].map((e) => {
          const ts = String(e.t || '').split(/\s+/).filter((t) => D.U[t]);
          return `<tr><td class="i">${ts.map((t) => UI.sym(t) + (fondo.has(t) ? ' <span class="chip acc">FONDO</span>' : '')).join(' ') || `<span class="chip">${esc(e.t || 'MERCADO')}</span>`}</td>
            <td class="i"><span class="chip ${/reporte/i.test(e.tipo) ? 'info' : /dividendo/i.test(e.tipo) ? 'pos' : ''}">${esc(e.tipo)}</span></td><td class="i" style="white-space:normal">${esc(e.titulo)}</td><td class="i dim">${esc(e.fuente || '')}</td></tr>`;
        }).join('')}`).join('') || '<tr><td class="i dim">Sin eventos.</td></tr>'}</tbody></table></div></div>`;
      $$('[data-m]', cont).forEach((b) => b.addEventListener('click', () => { Local.guardar('cal:modo', b.dataset.m); App.pintar(); }));
    },
  });

  // ───────────────────────── AYUDA ─────────────────────────
  App.registrar('ayuda', {
    titulo: () => 'Ayuda',
    pintar(cont) {
      const filas = [
        ['FEMSAUBD', 'Abre la ficha de la emisora (también funciona con el nombre: «femsa», «banorte»).'],
        ['FEMSAUBD KPI', 'Pestaña de KPIs de la ficha. Otras: DES, GP (gráfica), FA (financieros), RV (pares), N (noticias), TESIS, DVD.'],
        ['PANEL · F2', 'Índices, mapa de calor por sector, el fondo hoy, ganadoras, perdedoras, noticias y eventos.'],
        ['MERCADO · F3 · TOP', 'Monitor de todo el universo; TOP lo ordena por cambio del día.'],
        ['PORT · F6', 'Portafolio del fondo contra el MEXTRAC, riesgo ex ante y revisión de política.'],
        ['N · F7', 'Noticias; «N GFNORTEO» abre las de una emisora.'],
        ['ECO · F8', 'Macro: divisas, tasas, índices y materias primas, con la matriz de sensibilidad.'],
        ['EQS · F9', 'Filtro por KPIs con preajustes (QVM, valor, calidad, momentum, dividendos…).'],
        ['COMP A B C · F10', 'Compara emisoras: «COMP FEMSAUBD KOFUBL AC».'],
        ['W', 'Listas de seguimiento y alertas de precio.'], ['CAL', 'Calendario de reportes y dividendos.'],
        ['MCP', 'Cómo consultar la terminal desde Claude.'], ['SYS', 'Estado de los datos y de GitHub Actions.'],
      ];
      const defs = (D.kpisArch && D.kpisArch.definiciones) || {};
      cont.innerHTML = `${UI.titulo('Ayuda', 'Escriba en la línea de comandos (atajo «/» o Ctrl+K) y presione Enter')}
        <div class="rejilla g2">
          ${UI.panel('Comandos', `<table class="t ayuda-tabla"><tbody>${filas.map(([a, b]) => `<tr><td>${esc(a)}</td><td>${esc(b)}</td></tr>`).join('')}</tbody></table>`, { p0: true })}
          <div class="rejilla" style="align-content:start">
            ${UI.panel('Atajos', `<table class="t ayuda-tabla"><tbody><tr><td>/ · Ctrl+K</td><td>Ir a la línea de comandos</td></tr><tr><td>↑ ↓ · Tab</td><td>Moverse y completar sugerencias</td></tr>
              <tr><td>F1 F2 F3 F4 F6 F7 F8 F9 F10</td><td>Ayuda, panel, mercado, emisora, portafolio, noticias, macro, filtro, comparar</td></tr><tr><td>Esc</td><td>Regresar al panel</td></tr></tbody></table>`, { p0: true })}
            ${UI.panel('De dónde salen los datos', `<div class="texto" style="font-size:11.5px"><p>Ya no hace falta encender el vigilante. Un workflow de <b>GitHub Actions</b> descarga todo en la nube y lo publica en la rama <b>datos</b> del repositorio:</p>
              <p>· Cada 15 minutos durante la sesión de la BMV (9:30 a 16:00 de Nueva York: 7:30–14:00 CDMX con horario de verano de EUA, 8:30–15:00 sin él): cotizaciones, intradía y portafolio.<br>· A las 6:20 y a las 16:40 CDMX de cada día hábil: velas de cinco años, estados financieros, múltiplos, consenso, KPIs, noticias y macro.<br>
              · Cada vez que se edita empresas.txt, noticias.txt u operaciones.csv en main.</p>
              <p>Fuentes: Yahoo Finance, Google Noticias, Banxico (opcional) y los archivos del equipo. La página revisa cada minuto si hay datos nuevos.</p></div>`)}
            ${UI.panel('Capturar KPIs operativos', `<div class="texto" style="font-size:11.5px"><p>En <b>empresas.txt</b>, dentro del bloque de la emisora:</p></div>
              <div class="mono-bloque">=== FEMSAUBD ===\nkpis:\n  - VMT OXXO México | +9.5% | 2T26 | ticket +7.4%, tráfico +2.0% | crecimiento orgánico\n  - Margen operativo OXXO | 10.0% | 2T26 | +10 pb a/a | rentabilidad del negocio</div>`)}
          </div></div>
        ${UI.panel('Glosario de KPIs', `<table class="t ayuda-tabla"><tbody>${Object.entries(defs).map(([k, d]) => `<tr><td>${esc(d.nombre)}</td><td>${esc(d.que || '')} <span class="dim">${esc(d.formula || '')}</span></td></tr>`).join('')}</tbody></table>`, { p0: true, clase: 'ancho' })}`;
    },
  });

  // ───────────────────────── MCP ─────────────────────────
  App.registrar('mcp', {
    titulo: () => 'IA · MCP',
    pintar(cont) {
      const cfgDesktop = JSON.stringify({ mcpServers: { 'north-star': { command: 'python3', args: ['/ruta/a/bbva-clinicas/terminal/mcp/servidor_mcp.py'] } } }, null, 2);
      const herr = [['cotizacion', 'Precio, cambio y rango de una o varias emisoras'], ['ficha', 'Ficha completa: perfil, datos clave, tesis, catalizadores y riesgos'],
        ['kpis', 'Todos los KPIs de una emisora con su comparación contra pares'], ['ranking_kpi', 'Ordena el universo por cualquier KPI'],
        ['filtrar', 'Filtro con criterios (ej. ROE ≥ 15% y P/U ≤ 12)'], ['noticias', 'Noticias recientes por emisora o del mercado'],
        ['portafolio', 'Posiciones, pesos, desviaciones y rendimiento contra el MEXTRAC'], ['macro', 'Series macro y su último valor'],
        ['estados_financieros', 'Estado de resultados, balance o flujo trimestral y anual'], ['comparar', 'Compara KPIs de varias emisoras'],
        ['estado_datos', 'Cuándo se actualizó la terminal y qué falló']];
      cont.innerHTML = `${UI.titulo('IA · Model Context Protocol', 'Pregúntele a Claude por las emisoras con los mismos datos de la terminal')}
        <div class="rejilla g2">
          ${UI.panel('Qué es', `<div class="texto" style="font-size:12px"><p>El servidor MCP de la terminal (<b>terminal/mcp/servidor_mcp.py</b>) expone los datos como herramientas para Claude Desktop, Claude Code o cualquier cliente MCP. Solo usa la biblioteca estándar de Python: no hay que instalar nada.</p>
            <p>Lee los mismos JSON que publica GitHub Actions en la rama <b>datos</b>, así que las respuestas coinciden con lo que se ve aquí. Ejemplos: «¿Qué emisoras del universo tienen ROE arriba de 20% y P/U debajo de 12?», «Compara los márgenes de FEMSA, KOF y Arca», «¿Cómo va el fondo contra el MEXTRAC esta semana?».</p></div>`)}
          ${UI.panel('Herramientas', `<table class="t ayuda-tabla"><tbody>${herr.map(([a, b]) => `<tr><td>${a}</td><td>${b}</td></tr>`).join('')}</tbody></table>`, { p0: true })}
          ${UI.panel('Claude Code', '<div class="mono-bloque">claude mcp add north-star -- python3 terminal/mcp/servidor_mcp.py</div><p class="dim" style="margin-top:6px;font-size:10.5px">Desde la carpeta del repositorio.</p>')}
          ${UI.panel('Claude Desktop', `<div class="mono-bloque">${esc(cfgDesktop)}</div><p class="dim" style="margin-top:6px;font-size:10.5px">En claude_desktop_config.json. Con <b>--local</b> lee una copia local de los datos; sin él los descarga de GitHub.</p>`)}
        </div>`;
    },
  });

  // ───────────────────────── ESTADO ─────────────────────────
  App.registrar('estado', {
    titulo: () => 'Estado',
    pintar(cont) {
      const e = D.estado || {};
      const filas = [['Última actualización', `${F.fechaHora(e.generado)} (${F.hace(e.generado)})`], ['Modo', e.modo], ['Última corrida completa', F.fechaHora(e.ultimo_completo)],
        ['Última corrida rápida', F.fechaHora(e.ultimo_rapido)], ['Fuentes', (e.fuentes || []).join(' · ')], ['Duración', e.duracion_s ? e.duracion_s + ' s' : '—'],
        ['Origen', e.origen], ['Datos leídos de', `<a href="${esc(D.base)}estado.json" target="_blank" rel="noopener">${esc(D.base)}</a>`],
        ['Mercado al correr', e.mercado ? `${esc(e.mercado.texto)} · ${esc(e.mercado.hora_cdmx)}` : '—']];
      const act = `https://github.com/${D.repo}/actions/workflows/terminal-datos.yml`;
      cont.innerHTML = `${UI.titulo('Estado de los datos', 'Lo que hizo la última corrida de GitHub Actions')}
        <div class="rejilla g2">
          ${UI.panel('Corrida', `<table class="t"><tbody>${filas.map(([k, v]) => `<tr><td class="i dim">${k}</td><td class="i" style="white-space:normal">${v || '—'}</td></tr>`).join('')}</tbody></table>
            <div class="graf-barra" style="padding:8px"><a class="btn" href="${act}" target="_blank" rel="noopener">ABRIR GITHUB ACTIONS</a><span class="dim">Ahí, «Run workflow» fuerza una descarga en cualquier momento.</span></div>`, { p0: true })}
          ${UI.panel('Cobertura', `<table class="t"><tbody>${Object.entries(e.cobertura || {}).map(([k, v]) => `<tr><td class="i">${esc(k)}</td><td>${esc(v)}</td></tr>`).join('') || '<tr><td class="i dim">—</td></tr>'}</tbody></table>`, { p0: true })}
          ${UI.panel(`Errores (${(e.errores || []).length})`, (e.errores || []).map((x) => `<div class="neg" style="padding:3px 0">${esc(x)}</div>`).join('') || '<div class="pos">Sin errores.</div>')}
          ${UI.panel(`Avisos (${e.n_avisos || 0})`, (e.avisos || []).map((x) => `<div class="dim" style="padding:2px 0">${esc(x)}</div>`).join('') || '<div class="dim">Sin avisos.</div>')}
        </div>`;
    },
    vivo: true,
  });
})(window.NST);
