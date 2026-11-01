/* North Star Terminal · aplicación
   Enrutador por hash (#/eq/FEMSAUBD/kpis), línea de comandos con autocompletado,
   teclas de función, cinta de cotizaciones, relojes y barra de estado. */
'use strict';
(function (N) {
  const { F, esc, $, $$, Local, Bus, D } = N;

  // ───────────────────────── piezas de interfaz comunes ─────────────────────────
  const UI = {
    sym(t, { nombre = false, clic = true } = {}) {
      const u = D.U[t]; const lg = D.logo(t);
      const marca = (u && u.n ? u.n : t).replace(/[^A-Za-zÁÉÍÓÚÑ ]/g, '').trim().split(/\s+/).map((w) => w[0]).join('').slice(0, 3).toUpperCase();
      return `<span class="sym" ${clic ? `data-ir="#/eq/${esc(t)}"` : ''} title="${esc(D.nombre(t))}"><span class="lg"><b>${esc(marca || t.slice(0, 3))}</b>${lg ? `<img src="${lg}" alt="" loading="lazy" onerror="this.remove()">` : ''}</span>${esc(t)}</span>${nombre ? ` <span class="nombre">${esc(D.nombre(t))}</span>` : ''}`;
    },
    cambio(x, d = 2) { return `<span class="${F.cls(x)}">${F.flecha(x)} ${F.pctS(x, d)}</span>`; },
    num(x, fn = F.num) { return `<span class="${F.cls(x)}">${fn(x)}</span>`; },
    rango(lo, hi, x) {
      if (!N.esNum(lo) || !N.esNum(hi) || !N.esNum(x) || hi <= lo) return '<span class="dim">—</span>';
      const p = Math.max(0, Math.min(1, (x - lo) / (hi - lo)));
      return `<span class="rango" title="${F.precio(lo)} – ${F.precio(hi)}"><i style="left:calc(${(p * 100).toFixed(1)}% - 1px)"></i></span>`;
    },
    panel(titulo, cuerpo, { nota = '', acciones = '', clase = '', p0 = false, id = '' } = {}) {
      return `<section class="panel ${clase}" ${id ? `id="${id}"` : ''}><div class="panel-h">${titulo}${nota ? ` <span class="nota">${nota}</span>` : ''}<span class="esp"></span>${acciones}</div><div class="panel-b ${p0 ? 'p0' : ''}">${cuerpo}</div></section>`;
    },
    titulo(t, sub = '', acciones = '') { return `<div class="ttl"><h1>${t}</h1><span class="sub">${sub}</span><span class="esp"></span>${acciones}</div>`; },
    /** Tabla ordenable. cols: [{k, t, i, f(fila), v(fila), cls(fila), title}] */
    tabla(el, cols, filas, { orden = null, dir = -1, alClic = null, pie = null, idFila = (f) => f.t, sel = null } = {}) {
      let o = orden, d = dir;
      const pintar = () => {
        const fs = filas.slice();
        if (o) {
          const c = cols.find((x) => x.k === o);
          const val = c && (c.v || ((f) => f[c.k]));
          fs.sort((a, b) => {
            const x = val(a), y = val(b);
            const nx = x === null || x === undefined || (typeof x === 'number' && !isFinite(x));
            const ny = y === null || y === undefined || (typeof y === 'number' && !isFinite(y));
            if (nx && ny) return 0; if (nx) return 1; if (ny) return -1;
            return (typeof x === 'string' ? x.localeCompare(y, 'es') : x - y) * d;
          });
        }
        const th = cols.map((c) => `<th class="${c.i ? 'i' : ''} ${c.v || c.k ? 'ord' : ''} ${o === c.k ? 'on' : ''}" data-k="${c.k}" ${c.title ? `title="${esc(c.title)}"` : ''}>${c.t}${o === c.k ? (d > 0 ? ' ▲' : ' ▼') : ''}</th>`).join('');
        const tr = fs.map((f) => `<tr class="${alClic ? 'clic' : ''} ${sel && sel(f) ? 'sel' : ''}" data-id="${esc(idFila(f))}">${cols.map((c) => `<td class="${c.i ? 'i' : ''} ${c.cls ? c.cls(f) : ''}">${c.f ? c.f(f) : esc(f[c.k] ?? '—')}</td>`).join('')}</tr>`).join('');
        el.innerHTML = `<div class="tabla-env"><table class="t"><thead><tr>${th}</tr></thead><tbody>${tr || `<tr><td colspan="${cols.length}" class="i dim">Sin resultados</td></tr>`}</tbody>${pie ? `<tfoot>${pie}</tfoot>` : ''}</table></div>`;
        $$('th.ord', el).forEach((h) => h.addEventListener('click', () => { const k = h.dataset.k; d = o === k ? -d : -1; o = k; pintar(); }));
        if (alClic) $$('tbody tr.clic', el).forEach((r) => r.addEventListener('click', (ev) => { if (ev.target.closest('a,button,input')) return; alClic(r.dataset.id, ev); }));
      };
      pintar();
      return { repintar: (nuevas) => { if (nuevas) filas = nuevas; pintar(); } };
    },
  };
  N.UI = UI;

  // ───────────────────────── pantallas y enrutador ─────────────────────────
  const P = {};
  const TECLAS = [
    { id: 'ayuda', f: 'F1', n: 'AYUDA' }, { id: 'panel', f: 'F2', n: 'PANEL' }, { id: 'mercado', f: 'F3', n: 'MERCADO' },
    { id: 'eq', f: 'F4', n: 'EMISORA' }, { id: 'seg', f: 'W', n: 'SEGUIMIENTO' }, { id: 'port', f: 'F6', n: 'PORTAFOLIO' },
    { id: 'noticias', f: 'F7', n: 'NOTICIAS' }, { id: 'macro', f: 'F8', n: 'MACRO' }, { id: 'filtro', f: 'F9', n: 'FILTRO' },
    { id: 'comp', f: 'F10', n: 'COMPARAR' }, { id: 'cal', f: 'CAL', n: 'CALENDARIO' }, { id: 'mcp', f: 'MCP', n: 'IA · MCP' },
    { id: 'estado', f: 'SYS', n: 'ESTADO' },
  ];
  const App = {
    actual: null, args: [], ultimaEmisora: Local.leer('ultima', 'FEMSAUBD'),
    registrar(id, def) { P[id] = def; },
    ir(hash) { if (location.hash === hash) this.rutear(); else location.hash = hash; },
    rutear() {
      const partes = location.hash.replace(/^#\/?/, '').split('/').map(decodeURIComponent).filter(Boolean);
      let id = (partes[0] || 'panel').toLowerCase();
      if (!P[id]) id = 'panel';
      const args = partes.slice(1);
      if (id === 'eq') {
        if (!args[0]) args[0] = this.ultimaEmisora;
        args[0] = args[0].toUpperCase();
        this.ultimaEmisora = args[0]; Local.guardar('ultima', args[0]);
      }
      this.actual = id; this.args = args;
      $$('.tecla').forEach((b) => b.classList.toggle('on', b.dataset.id === id));
      this.pintar();
    },
    pintar() {
      const cont = $('#contenido');
      if (!D.cargado) return;
      N.G.limpiar();
      const def = P[this.actual];
      document.title = `${def.titulo ? def.titulo(this.args) : this.actual.toUpperCase()} · North Star Terminal`;
      try { def.pintar(cont, this.args); } catch (e) {
        console.error(e);
        cont.innerHTML = `<div class="aviso-barra">No se pudo dibujar la pantalla: ${esc(e.message)}</div>`;
      }
      cont.scrollTop = 0;
    },
    /** Repinta solo si la pantalla lo permite (para no perder el estado de la interacción). */
    refrescar() { const def = P[this.actual]; if (def && def.refrescar) def.refrescar($('#contenido'), this.args); else if (def && def.vivo) this.pintar(); },
  };
  N.App = App;

  // ───────────────────────── línea de comandos ─────────────────────────
  const FUNCIONES = {
    panel: ['PANEL', 'DASH', 'INICIO', 'HOME'], mercado: ['MERCADO', 'MKT', 'MON', 'MONITOR', 'MOST', 'TOP'],
    seg: ['W', 'SEG', 'SEGUIMIENTO', 'WATCH', 'LISTA'], port: ['PORT', 'PORTAFOLIO', 'FONDO', 'CARTERA', 'PRTU'],
    noticias: ['N', 'NOT', 'NOTICIAS', 'NEWS', 'TOPN'], macro: ['ECO', 'MACRO', 'WEI', 'FX', 'CMDTY', 'TASAS', 'WB'],
    filtro: ['EQS', 'FILTRO', 'SCREENER', 'QVM'], comp: ['COMP', 'COMPARAR', 'CMP', 'COMPARE'],
    cal: ['CAL', 'EVTS', 'CALENDARIO', 'EVENTOS', 'ERN'], ayuda: ['AYUDA', 'HELP', '?', 'H'], mcp: ['MCP', 'IA', 'CLAUDE'],
    estado: ['ESTADO', 'STATUS', 'SYS', 'DATOS'],
  };
  const PESTANAS = {
    resumen: ['DES', 'RESUMEN', 'GO'], grafica: ['GP', 'GRAF', 'GRAFICA', 'GIP', 'CHART'], financieros: ['FA', 'FIN', 'FINANCIEROS', 'EF'],
    kpis: ['KPI', 'KPIS', 'IND', 'INDICADORES'], pares: ['RV', 'PARES', 'VAL', 'VALUACION', 'COMP'], noticias: ['N', 'NOT', 'NOTICIAS', 'CN'],
    tesis: ['TESIS', 'TES', 'ANR', 'POSTURA'], dividendos: ['DVD', 'DIV', 'DIVIDENDOS'],
  };
  const DESC = {
    panel: 'Panel general del mercado y del fondo', mercado: 'Monitor de cotizaciones del universo', seg: 'Tu lista de seguimiento y alertas',
    port: 'Portafolio del fondo contra el MEXTRAC', noticias: 'Noticias del equipo, LSEG y Google', macro: 'Divisas, tasas, índices y materias primas',
    filtro: 'Filtro de emisoras por KPI y modelo QVM', comp: 'Compara emisoras: rendimiento y KPIs', cal: 'Reportes, dividendos y eventos',
    ayuda: 'Comandos y atajos', mcp: 'Conecta Claude a la terminal (MCP)', estado: 'Estado de los datos y de GitHub Actions',
  };
  const quitarAcentos = (s) => s.normalize('NFD').replace(/[̀-ͯ]/g, '');

  function buscarEmisoras(txt) {
    const q = quitarAcentos(txt.toUpperCase());
    if (!q) return [];
    return D.emisoras().map((e) => {
      const n = quitarAcentos((e.n + ' ' + (e.nombre || '')).toUpperCase());
      let s = 0;
      if (e.t === q) s = 100; else if (e.t.startsWith(q)) s = 80; else if (n.startsWith(q)) s = 60;
      else if (n.split(/\s+/).some((w) => w.startsWith(q))) s = 50; else if (n.includes(q)) s = 30;
      return { e, s };
    }).filter((x) => x.s).sort((a, b) => b.s - a.s).map((x) => x.e);
  }

  function interpretar(txt) {
    const tok = txt.trim().toUpperCase().split(/[\s,]+/).filter(Boolean);
    if (!tok.length) return null;
    const fn = Object.keys(FUNCIONES).find((k) => FUNCIONES[k].includes(tok[0]));
    const em = D.U[tok[0]] ? tok[0] : null;
    if (em) {
      const p = tok[1] && Object.keys(PESTANAS).find((k) => PESTANAS[k].includes(tok[1]));
      return `#/eq/${em}/${p || 'resumen'}`;
    }
    if (fn) {
      if (fn === 'comp') return `#/comp/${tok.slice(1).filter((t) => D.U[t]).join(',')}`;
      if (fn === 'noticias' && tok[1] && D.U[tok[1]]) return `#/eq/${tok[1]}/noticias`;
      if (fn === 'mercado' && tok[0] === 'TOP') return '#/mercado/cambio';
      return `#/${fn}`;
    }
    const r = buscarEmisoras(tok[0]);
    if (r.length) {
      const p = tok[1] && Object.keys(PESTANAS).find((k) => PESTANAS[k].includes(tok[1]));
      return `#/eq/${r[0].t}/${p || 'resumen'}`;
    }
    return null;
  }

  function sugerencias(txt) {
    const tok = txt.trim().toUpperCase().split(/\s+/).filter(Boolean);
    const out = [];
    if (!tok.length) {
      Object.keys(FUNCIONES).slice(0, 8).forEach((k) => out.push({ k: FUNCIONES[k][0], d: DESC[k], t: 'función', h: `#/${k}` }));
      return out;
    }
    if (tok.length === 1) {
      buscarEmisoras(tok[0]).slice(0, 7).forEach((e) => out.push({ k: e.t, d: e.n, t: e.sector, h: `#/eq/${e.t}/resumen` }));
      Object.keys(FUNCIONES).forEach((k) => {
        if (FUNCIONES[k].some((a) => a.startsWith(tok[0]))) out.push({ k: FUNCIONES[k].find((a) => a.startsWith(tok[0])), d: DESC[k], t: 'función', h: `#/${k}` });
      });
    } else if (D.U[tok[0]] || buscarEmisoras(tok[0]).length) {
      const t = D.U[tok[0]] ? tok[0] : buscarEmisoras(tok[0])[0].t;
      const nombres = { resumen: 'Resumen y datos clave', grafica: 'Gráfica de velas con indicadores', financieros: 'Estados financieros',
        kpis: 'Pestaña de KPIs', pares: 'Valuación contra pares', noticias: 'Noticias de la emisora', tesis: 'Tesis del equipo', dividendos: 'Historial de dividendos' };
      Object.keys(PESTANAS).forEach((k) => {
        if (PESTANAS[k].some((a) => a.startsWith(tok[1]))) out.push({ k: `${t} ${PESTANAS[k][0]}`, d: nombres[k], t: D.nombre(t), h: `#/eq/${t}/${k}` });
      });
    }
    return out.slice(0, 12);
  }

  function montarComando() {
    const inp = $('#cmd'), caja = $('#sug');
    let sel = 0, lista = [];
    const pintar = () => {
      lista = sugerencias(inp.value);
      sel = Math.min(sel, Math.max(0, lista.length - 1));
      caja.innerHTML = lista.map((s, i) => `<button type="button" class="${i === sel ? 'on' : ''}" data-h="${esc(s.h)}"><span class="k">${esc(s.k)}</span><span class="d">${esc(s.d)}</span><span class="t">${esc(s.t || '')}</span></button>`).join('');
      caja.hidden = !lista.length || document.activeElement !== inp;
    };
    const ejecutar = () => {
      const h = (lista[sel] && inp.value.trim().split(/\s+/).length === 1 && !D.U[inp.value.trim().toUpperCase()] && lista[sel].h) || interpretar(inp.value) || (lista[sel] && lista[sel].h);
      if (h) { App.ir(h); inp.value = ''; caja.hidden = true; inp.blur(); } else N.toast(`No reconozco «${esc(inp.value)}». Escriba AYUDA para ver los comandos.`);
    };
    inp.addEventListener('input', () => { sel = 0; pintar(); });
    inp.addEventListener('focus', pintar);
    inp.addEventListener('blur', () => setTimeout(() => { caja.hidden = true; }, 150));
    inp.addEventListener('keydown', (ev) => {
      if (ev.key === 'ArrowDown') { sel = Math.min(sel + 1, lista.length - 1); pintar(); ev.preventDefault(); }
      else if (ev.key === 'ArrowUp') { sel = Math.max(sel - 1, 0); pintar(); ev.preventDefault(); }
      else if (ev.key === 'Tab' && lista[sel]) { inp.value = lista[sel].k + ' '; pintar(); ev.preventDefault(); }
      else if (ev.key === 'Enter') { ejecutar(); ev.preventDefault(); }
      else if (ev.key === 'Escape') { inp.value = ''; inp.blur(); }
    });
    caja.addEventListener('mousedown', (ev) => { const b = ev.target.closest('button'); if (b) { ev.preventDefault(); App.ir(b.dataset.h); inp.value = ''; caja.hidden = true; inp.blur(); } });
  }

  // ───────────────────────── atajos de teclado ─────────────────────────
  function montarTeclado() {
    document.addEventListener('keydown', (ev) => {
      const escribiendo = /INPUT|SELECT|TEXTAREA/.test(document.activeElement.tagName);
      if ((ev.key === '/' && !escribiendo) || ((ev.ctrlKey || ev.metaKey) && ev.key.toLowerCase() === 'k')) { ev.preventDefault(); $('#cmd').focus(); return; }
      const t = TECLAS.find((x) => x.f === ev.key);
      if (t && /^F\d+$/.test(ev.key)) { ev.preventDefault(); App.ir(`#/${t.id}`); return; }
      if (ev.key === 'Escape' && !escribiendo && App.actual !== 'panel') App.ir('#/panel');
    });
    document.addEventListener('click', (ev) => {
      const a = ev.target.closest('[data-ir]');
      if (a && !ev.target.closest('a[href^="http"]')) { ev.preventDefault(); App.ir(a.dataset.ir); }
    });
  }

  // ───────────────────────── cinta, relojes, estado de la BMV ─────────────────────────
  function pintarCinta() {
    const pista = $('#cintaPista'); if (!pista) return;
    const claves = ['IPC', 'MEXTRAC', 'USDMXN', ...D.emisoras(false).map((e) => e.t), 'SP500', 'COBRE', 'ORO', 'BRENT', 'UST10'];
    const items = claves.filter((t) => D.cot(t).p).map((t) => {
      const q = D.cot(t);
      return `<span class="cinta-it" data-ir="${D.U[t] ? `#/eq/${t}` : '#/macro'}"><b>${esc(t)}</b>${F.precio(q.p)} <span class="${F.cls(q.cp)}">${F.flecha(q.cp)}${F.pctS(q.cp)}</span></span>`;
    }).join('');
    pista.innerHTML = items + items;               // duplicado para el ciclo continuo
    pista.style.setProperty('--dur', Math.max(60, claves.length * 4) + 's');
  }

  function horaEn(zona) { return new Date().toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit', hour12: false, timeZone: zona }); }
  function estadoBMV() {
    const ahora = new Date();
    const partes = Object.fromEntries(new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Mexico_City', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', hour12: false, weekday: 'short' })
      .formatToParts(ahora).map((p) => [p.type, p.value]));
    const fecha = `${partes.year}-${partes.month}-${partes.day}`;
    const min = (+partes.hour % 24) * 60 + +partes.minute;
    const feriados = ((D.universo && D.universo.fondo && D.universo.fondo.feriados) || []);
    if (['Sat', 'Sun'].includes(partes.weekday)) return { e: 'cerrado', t: 'BMV cerrada · fin de semana' };
    if (feriados.includes(fecha)) return { e: 'cerrado', t: 'BMV cerrada · día inhábil' };
    if (min < 510) return { e: 'preapertura', t: 'BMV abre 8:30' };
    if (min < 900) return { e: 'abierto', t: 'BMV abierta' };
    return { e: 'cerrado', t: 'BMV cerrada' };
  }
  function tic() {
    $('#hCdmx').textContent = horaEn('America/Mexico_City');
    $('#hNy').textContent = horaEn('America/New_York');
    $('#hLdn').textContent = horaEn('Europe/London');
    const b = estadoBMV(), el = $('#bmv');
    el.className = 'estado-bmv ' + b.e; $('#bmvTxt').textContent = b.t;
  }

  function pintarPie() {
    const e = D.estado || {}, pie = $('#pie');
    if (!pie) return;
    const min = e.generado ? (Date.now() - new Date(e.generado)) / 60000 : Infinity;
    const b = estadoBMV();
    const viejo = b.e === 'abierto' ? min > 45 : min > 60 * 30;
    const fuentes = (e.fuentes || []).join(' · ') || '—';
    const errores = (e.errores || []).length;
    pie.innerHTML = `<span class="${viejo ? 'av' : 'ok'}">● ${viejo ? 'Datos atrasados' : 'Datos al día'}</span>
      <span>Actualizado <b>${e.generado ? F.fechaHora(e.generado) : '—'}</b> (${e.generado ? F.hace(e.generado) : '—'})</span>
      <span class="opc">Fuente <b>${esc(fuentes)}</b></span>
      <span class="opc">Cobertura <b>${esc(Object.entries(e.cobertura || {}).map(([k, v]) => `${k} ${v}`).join(' · ') || '—')}</b></span>
      ${errores ? `<a data-ir="#/estado" class="mal">${errores} error${errores > 1 ? 'es' : ''}</a>` : ''}
      <span class="esp"></span>
      <span class="opc">Sin vigilante · GitHub Actions${b.e === 'abierto' ? ' cada 15 min' : ''}</span>
      <a href="https://github.com/${esc(D.repo)}" target="_blank" rel="noopener">${esc(D.repo)}</a>`;
  }

  // ───────────────────────── arranque ─────────────────────────
  function montarTeclas() {
    $('#teclas').innerHTML = TECLAS.map((t) => `<button class="tecla" data-id="${t.id}" data-ir="#/${t.id}" title="${esc(DESC[t.id] || t.n)}"><b>${t.f}</b>${t.n}</button>`).join('');
  }
  function tema() {
    const actual = Local.leer('tema', 'ambar');
    document.documentElement.dataset.tema = actual;
    $('#btnTema').addEventListener('click', () => {
      const t = document.documentElement.dataset.tema === 'ambar' ? 'marino' : 'ambar';
      document.documentElement.dataset.tema = t; Local.guardar('tema', t); App.pintar();
    });
  }

  async function iniciar() {
    montarTeclas(); montarComando(); montarTeclado(); tema();
    tic(); setInterval(tic, 15000);
    window.addEventListener('hashchange', () => App.rutear());
    $('#contenido').innerHTML = '<div class="cargando">Cargando datos de la terminal</div>';
    Bus.on('datos:error', (msg) => { $('#contenido').innerHTML = `<div class="aviso-barra">${esc(msg)}</div>${P.ayuda ? '' : ''}`; });
    Bus.on('datos', (x) => {
      pintarCinta(); pintarPie(); tic();
      if (x && x.inicial) App.rutear(); else { App.refrescar(); N.Alertas && N.Alertas.revisar(); }
    });
    Bus.on('datos:igual', pintarPie);
    setInterval(pintarPie, 60000);
    await D.iniciar();
  }
  document.addEventListener('DOMContentLoaded', iniciar);
})(window.NST);
