/* North Star Terminal · PANEL: vista general del mercado y del fondo */
'use strict';
(function (N) {
  const { F, esc, $, $$, D, UI, App, Local } = N;

  const MOSAICOS = ['IPC', 'MEXTRAC', 'USDMXN', 'SP500', 'UST10', 'COBRE', 'ORO', 'BRENT'];
  const PERIODOS = { '1D': null, '1S': 5, '1M': 21, '3M': 63, 'AÑO': 'ytd', '1A': 252 };

  function serieCorta(t) {
    const s = D.serie(t, 30);
    if (s.length) return s;
    const m = D.macro[t]; return m ? m.c.slice(-30) : [];
  }
  function cambioPeriodo(t, p) {
    if (p === '1D') return D.cot(t).cp;
    const n = PERIODOS[p];
    return n === 'ytd' ? D.rendYTD(t) : D.rend(t, n);
  }

  function mosaicos() {
    return `<div class="mos">${MOSAICOS.map((t) => {
      const q = D.cot(t); if (!q.p) return '';
      const nombre = D.U[t] ? D.U[t].n : (D.macro[t] ? D.macro[t].n : t);
      const ir = D.U[t] ? `#/eq/${t}/grafica` : `#/macro/${t}`;
      return `<div class="mos-it" data-ir="${ir}" title="${esc(nombre)}"><div class="n">${esc(t)} · ${esc(nombre)}</div>
        <div class="v">${t === 'UST10' ? F.num(q.p, 3) + '%' : F.precio(q.p)}</div>
        <div class="c ${F.cls(q.cp)}">${F.flecha(q.cp)} ${F.pctS(q.cp)} <span class="dim">${q.c != null ? F.num(q.c, 2) : ''}</span></div>
        ${N.spark(serieCorta(t), { w: 140, h: 26 })}</div>`;
    }).join('')}</div>`;
  }

  function mapa(p) {
    const porSector = {};
    D.emisoras(false).forEach((e) => { (porSector[e.sector] = porSector[e.sector] || []).push(e); });
    const tope = p === '1D' ? 0.03 : p === '1S' ? 0.06 : p === '1M' ? 0.1 : 0.25;
    return `<div class="mapa">${Object.keys(porSector).sort().map((s) => `<div class="mapa-sec"><h4>${esc(s)}</h4><div class="mapa-fila">${
      porSector[s].sort((a, b) => (b.peso_indice || 0) - (a.peso_indice || 0)).map((e) => {
        const x = cambioPeriodo(e.t, p);
        return `<div class="mapa-it" data-ir="#/eq/${e.t}" style="background:${N.calor(x, tope)}" title="${esc(e.n)} · ${F.pctS(x)}">
          <b>${esc(e.t)}</b><span>${F.flecha(x)} ${F.pctS(x, 1)}</span></div>`;
      }).join('')}</div></div>`).join('')}</div>`;
  }

  function fondo() {
    const p = D.port; if (!p || !p.actual) return '<div class="vacio">Sin datos del portafolio.</div>';
    const a = p.actual, s = p.serie || [], u = s[s.length - 1] || {};
    const filas = [
      ['Valor del portafolio', F.pesos(a.valor)],
      ['Cartera · hoy', UI.cambio(a.rend_dia)],
      ['MEXTRAC · hoy', UI.cambio(a.bench_dia)],
      ['Diferencia · hoy', `<span class="${F.cls(a.activo_dia)}">${F.pp(a.activo_dia)}</span>`],
      [`Acumulado cartera (desde ${F.fechaCorta(p.referencia)})`, UI.cambio(u.rend_acum)],
      ['Acumulado MEXTRAC', UI.cambio(u.bench_acum)],
      ['Diferencia acumulada', `<span class="${F.cls(u.activo_acum)}">${F.pp(u.activo_acum)}</span>`],
      ['Error de seguimiento ex post', `<span class="${(u.te_expost || 0) > 0.1 ? 'neg' : ''}">${F.pct(u.te_expost)}</span> <span class="dim">límite 10%</span>`],
      ['Efectivo', `${F.pesos(a.efectivo)} <span class="dim">${F.pct(a.efectivo_pct)}</span>`],
    ];
    return `<table class="t"><tbody>${filas.map(([k, v]) => `<tr><td class="i dim">${k}</td><td>${v}</td></tr>`).join('')}</tbody></table>
      <div class="graf bajo" id="panelFondo" style="margin-top:8px"></div>`;
  }

  function movidas() {
    const filas = D.emisoras(false).map((e) => ({ t: e.t, cp: D.cot(e.t).cp, p: D.cot(e.t).p, imp: (D.cot(e.t).p || 0) * (D.cot(e.t).v || 0) }))
      .filter((x) => N.esNum(x.cp));
    const lista = (xs, campo) => `<table class="t"><tbody>${xs.map((x) => `<tr class="clic" data-ir="#/eq/${x.t}"><td class="i">${UI.sym(x.t)}</td>
      <td>${F.precio(x.p)}</td><td>${campo === 'imp' ? F.dinero(x.imp) : UI.cambio(x.cp)}</td></tr>`).join('')}</tbody></table>`;
    const arriba = filas.slice().sort((a, b) => b.cp - a.cp).slice(0, 6);
    const abajo = filas.slice().sort((a, b) => a.cp - b.cp).slice(0, 6);
    const operadas = filas.filter((x) => x.imp > 0).sort((a, b) => b.imp - a.imp).slice(0, 6);
    return [lista(arriba), lista(abajo), operadas.length ? lista(operadas, 'imp') : '<div class="vacio">Sin volumen reportado todavía.</div>'];
  }

  function noticias() {
    const xs = D.noticias.slice(0, 9);
    if (!xs.length) return '<div class="vacio">Sin noticias.</div>';
    return xs.map((n) => N.Noticias.tarjeta(n, { corta: true })).join('');
  }
  function eventos() {
    const hoy = new Date().toISOString().slice(0, 10);
    const xs = (D.cal.eventos || []).filter((e) => e.fecha >= hoy).slice(0, 12);
    if (!xs.length) return '<div class="vacio">Sin eventos próximos.</div>';
    return `<table class="t"><tbody>${xs.map((e) => `<tr><td class="i">${F.fechaCorta(e.fecha)}</td><td class="i">${String(e.t || '').split(/\s+/).filter((t) => D.U[t]).map((t) => UI.sym(t)).join(' ') || esc(e.t)}</td>
      <td class="i"><span class="chip">${esc(e.tipo)}</span></td><td class="i" style="white-space:normal">${esc(e.titulo)}</td></tr>`).join('')}</tbody></table>`;
  }

  App.registrar('panel', {
    titulo: () => 'Panel',
    pintar(cont) {
      const p = Local.leer('panel:periodo', '1D');
      const [arriba, abajo, operadas] = movidas();
      const sem = D.qSemilla ? '<div class="aviso-barra info">Mostrando el último corte de Refinitiv que dejó el vigilante. En cuanto corra GitHub Actions, la terminal toma precios de Yahoo Finance automáticamente.</div>' : '';
      cont.innerHTML = `${UI.titulo('Panel', `Corte ${D.qGenerado ? F.fechaHora(D.qGenerado) : '—'} · ${D.emisoras(false).length} emisoras del universo`)}
        ${sem}${mosaicos()}
        <div class="rejilla g21" style="margin-top:8px">
          ${UI.panel('Mapa de calor', mapa(p), { nota: 'tamaño por sector · color por rendimiento', acciones: `<span class="chips">${Object.keys(PERIODOS).map((k) => `<button class="btn sm ${k === p ? 'on' : ''}" data-p="${k}">${k}</button>`).join('')}</span>`, id: 'pMapa' })}
          ${UI.panel('El fondo hoy', fondo(), { nota: 'contra MEXTRAC 09', acciones: '<a class="btn sm" data-ir="#/port">PORT ›</a>' })}
        </div>
        <div class="rejilla g3" style="margin-top:8px">
          ${UI.panel('Ganadoras del día', arriba, { p0: true })}
          ${UI.panel('Perdedoras del día', abajo, { p0: true })}
          ${UI.panel('Más operadas', operadas, { p0: true, nota: 'importe del día' })}
        </div>
        <div class="rejilla g2" style="margin-top:8px">
          ${UI.panel('Noticias recientes', noticias(), { p0: true, acciones: '<a class="btn sm" data-ir="#/noticias">N ›</a>' })}
          ${UI.panel('Próximos eventos', eventos(), { p0: true, acciones: '<a class="btn sm" data-ir="#/cal">CAL ›</a>' })}
        </div>`;
      $$('#pMapa [data-p]', cont).forEach((b) => b.addEventListener('click', () => { Local.guardar('panel:periodo', b.dataset.p); App.pintar(); }));
      const s = (D.port && D.port.serie) || [];
      const el = $('#panelFondo', cont);
      if (el && s.length > 1) {
        N.G.lineas(el, [
          { titulo: 'Cartera', datos: s.map((x) => ({ time: x.f, value: (x.rend_acum || 0) * 100 })) },
          { titulo: 'MEXTRAC', datos: s.map((x) => ({ time: x.f, value: (x.bench_acum || 0) * 100 })), punteada: true },
        ], { porcentaje: 'pct' });
      }
    },
    vivo: true,
  });
})(window.NST);
