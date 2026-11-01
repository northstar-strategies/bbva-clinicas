/* North Star Terminal · PORTAFOLIO del fondo contra el MEXTRAC 09
   La serie diaria la reconstruye el pipeline desde operaciones.csv con la misma contabilidad
   del tracker; aquí se agrega el riesgo ex ante con los pesos de hoy y la revisión de política. */
'use strict';
(function (N) {
  const { F, esc, $, D, UI, App } = N;

  function riesgo(a) {
    const c = D.cierres; if (!c || !a) return null;
    const n = Math.min(253, c.d.length);
    const ini = c.d.length - n;
    const pos = a.posiciones.filter((p) => c.s[p.t]);
    const total = a.valor || 1;
    const w = Object.fromEntries(pos.map((p) => [p.t, p.valor / total]));
    const rp = [], rb = [];
    for (let i = ini + 1; i < c.d.length; i++) {
      let r = 0;
      for (const t in w) { const x0 = c.s[t][i - 1], x1 = c.s[t][i]; if (x0 && x1) r += w[t] * (x1 / x0 - 1); }
      const b0 = c.s.MEXTRAC && c.s.MEXTRAC[i - 1], b1 = c.s.MEXTRAC && c.s.MEXTRAC[i];
      if (b0 && b1) { rp.push(r); rb.push(b1 / b0 - 1); }
    }
    if (rp.length < 30) return null;
    const m = (xs) => xs.reduce((s, x) => s + x, 0) / xs.length;
    const sd = (xs) => { const u = m(xs); return Math.sqrt(xs.reduce((s, x) => s + (x - u) ** 2, 0) / (xs.length - 1)); };
    const act = rp.map((x, i) => x - rb[i]);
    const mp = m(rp), mb = m(rb);
    const cov = rp.reduce((s, x, i) => s + (x - mp) * (rb[i] - mb), 0) / (rp.length - 1);
    const vb = sd(rb) ** 2;
    const ord = rp.slice().sort((x, y) => x - y);
    return { n: rp.length, vol: sd(rp) * Math.sqrt(252), te: sd(act) * Math.sqrt(252), beta: cov / vb, var95: -ord[Math.floor(0.05 * ord.length)], volB: Math.sqrt(vb) * Math.sqrt(252) };
  }

  App.registrar('port', {
    titulo: () => 'Portafolio',
    pintar(cont) {
      const p = D.port;
      if (!p || !p.actual) { cont.innerHTML = '<div class="vacio">Sin datos del portafolio. Se calculan desde operaciones.csv y parametros.json.</div>'; return; }
      const a = p.actual, s = p.serie || [], u = s[s.length - 1] || {};
      const r = riesgo(a);
      const pol = Object.assign({ te_max: 0.1, beta: [0.7, 1.3], efectivo: [0, 0.05], pasiva: [0.4, 0.6], desviacion_max_pp: 10 }, p.politica || {});
      const pasiva = a.posiciones.filter((x) => x.bloque === 'ETF' || x.bloque === 'REPRESENTATIVA').reduce((t, x) => t + (x.peso || 0), 0);
      const activa = a.posiciones.filter((x) => x.bloque === 'ACTIVA').reduce((t, x) => t + (x.peso || 0), 0);
      const maxDev = Object.entries(a.desviacion || {}).reduce((m, [t, v]) => (Math.abs(v) > Math.abs(m[1]) ? [t, v] : m), ['', 0]);
      const reglas = [
        ['Error de seguimiento ex ante', r ? F.pct(r.te) : 'n/d', r ? r.te <= (pol.te_max || 0.1) : null, `≤ ${F.pct(pol.te_max || 0.1, 0)}`],
        ['Error de seguimiento ex post', F.pct(u.te_expost), N.esNum(u.te_expost) ? u.te_expost <= (pol.te_max || 0.1) : null, `≤ ${F.pct(pol.te_max || 0.1, 0)}`],
        ['Beta contra MEXTRAC', r ? F.num(r.beta, 2) : 'n/d', r ? r.beta >= pol.beta[0] && r.beta <= pol.beta[1] : null, `${F.num(pol.beta[0], 2)} – ${F.num(pol.beta[1], 2)}`],
        ['Efectivo', F.pct(a.efectivo_pct), N.esNum(a.efectivo_pct) ? a.efectivo_pct >= pol.efectivo[0] && a.efectivo_pct <= pol.efectivo[1] : null, `${F.pct(pol.efectivo[0], 0)} – ${F.pct(pol.efectivo[1], 0)}`],
        ['Cartera pasiva (ETF + representativas)', F.pct(pasiva), pasiva >= pol.pasiva[0] && pasiva <= pol.pasiva[1], `${F.pct(pol.pasiva[0], 0)} – ${F.pct(pol.pasiva[1], 0)}`],
        [`Mayor desviación (${esc(maxDev[0])})`, F.pp(maxDev[1]), Math.abs(maxDev[1]) * 100 <= (pol.desviacion_max_pp || 10), `± ${pol.desviacion_max_pp || 10} pp`],
      ];
      const tiles = [
        ['Valor del portafolio', F.pesos(a.valor), `capital inicial ${F.dinero(p.capital)}`],
        ['Cartera hoy', UI.cambio(a.rend_dia), `MEXTRAC ${F.pctS(a.bench_dia)}`],
        ['Diferencia hoy', `<span class="${F.cls(a.activo_dia)}">${F.pp(a.activo_dia)}</span>`, 'cartera − MEXTRAC'],
        [`Acumulado desde ${F.fechaCorta(p.referencia)}`, UI.cambio(u.rend_acum), `MEXTRAC ${F.pctS(u.bench_acum)}`],
        ['Diferencia acumulada', `<span class="${F.cls(u.activo_acum)}">${F.pp(u.activo_acum)}</span>`, `día ${u.dia || '—'} de gestión`],
        ['Ganancia o pérdida', UI.num(a.valor - p.capital, F.pesos), `${F.pctS(a.valor / p.capital - 1)} sobre el capital`],
      ];
      cont.innerHTML = `${UI.titulo('Portafolio del fondo', `${esc(p.modelo || '')} · gestión del ${F.fecha(p.inicio)} al ${F.fecha(p.fin)} · referencia ${F.fecha(p.referencia)} · ${p.operaciones} operaciones (última ${F.fecha(p.ultima_operacion)})`)}
        <div class="rejilla g6">${tiles.map(([k, v, n]) => `<div class="mos-it" style="cursor:default"><div class="n">${k}</div><div class="v">${v}</div><div class="c dim">${n}</div></div>`).join('')}</div>
        <div class="rejilla g21" style="margin-top:8px">
          ${UI.panel('Rendimiento acumulado contra el MEXTRAC', '<div class="graf medio" id="pAcum"></div>', { nota: 'precio del MEXTRAC09, estimado con la canasta los días sin operación' })}
          ${UI.panel('Política de inversión', `<table class="t"><tbody>${reglas.map(([k, v, ok, lim]) => `<tr><td class="i">${ok === null ? '<span class="dim">●</span>' : ok ? '<span class="pos">✔</span>' : '<span class="neg">✖</span>'} ${k}</td><td>${v}</td><td class="dim">${lim}</td></tr>`).join('')}</tbody></table>
            ${r ? `<p class="dim" style="font-size:10.5px;padding:6px 9px">Ex ante: pesos de hoy sobre ${r.n} rendimientos diarios · volatilidad ${F.pct(r.vol)} (MEXTRAC ${F.pct(r.volB)}) · VaR 95% de un día ${F.pct(r.var95)} (${F.pesos(r.var95 * a.valor)})</p>` : ''}`, { p0: true })}
        </div>
        ${UI.panel('Posiciones', '<div id="pPos"></div>', { p0: true, nota: `pasiva ${F.pct(pasiva)} · activa ${F.pct(activa)} · efectivo ${F.pct(a.efectivo_pct)}` })}
        <div class="rejilla g2" style="margin-top:8px">
          ${UI.panel('Sobre y subponderaciones contra el índice', '<div id="pDev"></div>', { nota: 'peso efectivo (ETF desglosado) − peso en el índice' })}
          ${UI.panel('Día por día', '<div id="pDia"></div>', { p0: true, nota: 'misma contabilidad del tracker de Excel' })}
        </div>
        <p class="dim" style="font-size:10.5px;margin-top:8px">El portafolio se reconstruye desde <b>operaciones.csv</b> y <b>parametros.json</b>. Para registrar una operación nueva basta agregar su renglón en operaciones.csv (en GitHub, botón «Edit»): la terminal recalcula todo en la siguiente corrida.</p>`;
      if (s.length > 1) N.G.lineas($('#pAcum', cont), [
        { titulo: 'Cartera', datos: s.map((x) => ({ time: x.f, value: (x.rend_acum || 0) * 100 })) },
        { titulo: 'MEXTRAC', datos: s.map((x) => ({ time: x.f, value: (x.bench_acum || 0) * 100 })), punteada: true },
        { titulo: 'Diferencia', datos: s.map((x) => ({ time: x.f, value: (x.activo_acum || 0) * 100 })), color: '#9aa3ad', grosor: 1 },
      ], { porcentaje: 'pct' });
      const ef = a.pesos_efectivos || {}, ix = (D.universo && D.universo.fondo && D.universo.fondo.pesos_indice) || {};
      const totIx = Object.values(ix).reduce((t, v) => t + v, 0) || 1;
      UI.tabla($('#pPos', cont), [
        { k: 't', t: 'Emisora', i: true, f: (x) => UI.sym(x.t) },
        { k: 'bloque', t: 'Bloque', i: true, f: (x) => `<span class="chip ${x.bloque === 'ACTIVA' ? 'acc' : x.bloque === 'ETF' ? 'pos' : 'info'}">${esc(x.bloque)}</span>` },
        { k: 'titulos', t: 'Títulos', f: (x) => F.ent(x.titulos) }, { k: 'precio', t: 'Precio', f: (x) => F.precio(x.precio) },
        { k: 'cambio_dia', t: 'Hoy', f: (x) => UI.cambio(x.cambio_dia) }, { k: 'valor', t: 'Valor', f: (x) => F.pesos(x.valor) },
        { k: 'peso', t: 'Peso', f: (x) => F.pct(x.peso) },
        { k: 'ef', t: 'Efectivo', v: (x) => ef[x.t], f: (x) => (x.t === 'MEXTRAC' ? '<span class="dim">—</span>' : F.pct(ef[x.t])), title: 'peso directo + peso del ETF × peso en el índice' },
        { k: 'ix', t: 'Índice', v: (x) => (ix[x.t] || 0) / totIx, f: (x) => F.pct((ix[x.t] || 0) / totIx) },
        { k: 'dev', t: 'Desv.', v: (x) => (a.desviacion || {})[x.t], f: (x) => (x.t === 'MEXTRAC' ? '' : `<span class="${F.cls((a.desviacion || {})[x.t])}">${F.pp((a.desviacion || {})[x.t])}</span>`) },
        { k: 'costo_promedio', t: 'Costo prom.', f: (x) => F.precio(x.costo_promedio) },
        { k: 'pyg', t: 'G/P', f: (x) => UI.num(x.pyg, F.pesos) }, { k: 'pyg_pct', t: 'G/P %', f: (x) => UI.cambio(x.pyg_pct) },
        { k: 'aporte_dia', t: 'Aporte hoy', f: (x) => UI.num(x.aporte_dia, F.pesos) },
      ], a.posiciones, { orden: 'valor', alClic: (t) => App.ir(`#/eq/${t}`),
        pie: `<tr><td class="i">Efectivo</td><td></td><td></td><td></td><td></td><td>${F.pesos(a.efectivo)}</td><td>${F.pct(a.efectivo_pct)}</td><td colspan="7"></td></tr>` });
      const devs = Object.entries(a.desviacion || {}).filter(([t, v]) => D.U[t] && Math.abs(v) > 0.0005).sort((x, y) => y[1] - x[1]);
      const mx = Math.max(...devs.map(([, v]) => Math.abs(v)), 0.001);
      $('#pDev', cont).innerHTML = `<table class="t"><tbody>${devs.map(([t, v]) => `<tr class="clic" data-ir="#/eq/${t}"><td class="i">${UI.sym(t)}</td>
        <td style="width:55%"><div style="display:flex;${v >= 0 ? '' : 'justify-content:flex-end'}"><span class="barra-mini" style="width:${(Math.abs(v) / mx * 50).toFixed(1)}%;background:${v >= 0 ? 'var(--pos)' : 'var(--neg)'};margin-${v >= 0 ? 'left:50%' : 'right:50%'}"></span></div></td>
        <td class="${F.cls(v)}">${F.pp(v)}</td></tr>`).join('')}</tbody></table>`;
      UI.tabla($('#pDia', cont), [
        { k: 'f', t: 'Fecha', i: true, f: (x) => `${F.fecha(x.f)}${x.estado === 'en curso' ? ' <span class="chip warn">en curso</span>' : ''}` },
        { k: 'valor', t: 'Valor', f: (x) => F.pesos(x.valor) }, { k: 'rend_dia', t: 'Cartera', f: (x) => UI.cambio(x.rend_dia) },
        { k: 'bench_dia', t: 'MEXTRAC', f: (x) => UI.cambio(x.bench_dia) }, { k: 'activo_dia', t: 'Dif.', f: (x) => `<span class="${F.cls(x.activo_dia)}">${F.pp(x.activo_dia)}</span>` },
        { k: 'activo_acum', t: 'Dif. acum.', f: (x) => `<span class="${F.cls(x.activo_acum)}">${F.pp(x.activo_acum)}</span>` },
        { k: 'te_expost', t: 'TE', f: (x) => F.pct(x.te_expost) },
      ], s.slice().reverse(), { idFila: (x) => x.f });
    },
    vivo: true,
  });
})(window.NST);
