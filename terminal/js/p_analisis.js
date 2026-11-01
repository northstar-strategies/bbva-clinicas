/* North Star Terminal · MACRO, FILTRO (screener) y COMPARAR */
'use strict';
(function (N) {
  const { F, esc, $, $$, D, UI, App, Local } = N;

  // ───────────────────────── utilidades de series ─────────────────────────
  function rendimientosAlineados(a, b, n = 252) {
    // a, b: {d:[], c:[]}  → rendimientos diarios en fechas comunes (últimas n)
    const mb = new Map(b.d.map((f, i) => [f, b.c[i]]));
    const comunes = a.d.map((f, i) => [f, a.c[i], mb.get(f)]).filter((x) => N.esNum(x[1]) && N.esNum(x[2])).slice(-(n + 1));
    const ra = [], rb = [];
    for (let i = 1; i < comunes.length; i++) {
      if (comunes[i - 1][1] && comunes[i - 1][2]) { ra.push(comunes[i][1] / comunes[i - 1][1] - 1); rb.push(comunes[i][2] / comunes[i - 1][2] - 1); }
    }
    return [ra, rb];
  }
  function correl(x, y) {
    const n = Math.min(x.length, y.length); if (n < 20) return null;
    const mx = x.reduce((s, v) => s + v, 0) / n, my = y.reduce((s, v) => s + v, 0) / n;
    let sxy = 0, sx = 0, sy = 0;
    for (let i = 0; i < n; i++) { sxy += (x[i] - mx) * (y[i] - my); sx += (x[i] - mx) ** 2; sy += (y[i] - my) ** 2; }
    return sx && sy ? sxy / Math.sqrt(sx * sy) : null;
  }
  const serieEmisora = (t) => ({ d: D.fechas(), c: D.serie(t) });
  function colorCorr(r) {
    if (!N.esNum(r)) return 'transparent';
    const a = Math.min(1, Math.abs(r));
    return r >= 0 ? `rgba(31,214,122,${(a * 0.75).toFixed(2)})` : `rgba(255,77,94,${(a * 0.75).toFixed(2)})`;
  }

  // ───────────────────────── MACRO ─────────────────────────
  const TIPOS = [['indice', 'Índices'], ['divisa', 'Divisas'], ['tasa', 'Tasas'], ['materia', 'Materias primas']];
  const FACTORES = ['USDMXN', 'COBRE', 'ORO', 'PLATA', 'BRENT', 'GASNAT', 'UST10', 'SP500', 'BRLMXN'];

  App.registrar('macro', {
    titulo: () => 'Macro',
    pintar(cont, args) {
      const M = D.macro;
      const sel = (args[0] || Local.leer('macro:sel', 'USDMXN')).toUpperCase();
      const fila = (k) => {
        const s = M[k]; if (!s || !s.c || !s.c.length) return null;
        const q = D.cot(k), ult = q.p || s.c[s.c.length - 1];
        const ch = (n) => (s.c.length > n ? ult / s.c[s.c.length - 1 - n] - 1 : null);
        const esTasa = s.tipo === 'tasa';
        // En tasas importa la diferencia en puntos base, no el cambio porcentual del rendimiento.
        const pb = (n) => (s.c.length > n ? (ult - s.c[s.c.length - 1 - n]) * 100 : null);
        const d1 = esTasa ? (q.c != null ? q.c * 100 : pb(1)) : (q.cp != null ? q.cp : ch(1));
        return { k, n: s.n, u: s.u, ult, d1, m1: esTasa ? pb(21) : ch(21), a1: esTasa ? pb(252) : ch(252),
          fecha: s.d[s.d.length - 1], fuente: s.fuente, mueve: s.mueve || [], spk: s.c.slice(-90), tipo: s.tipo };
      };
      const grupos = TIPOS.map(([tipo, nombre]) => [nombre, Object.keys(M).filter((k) => M[k].tipo === tipo).map(fila).filter(Boolean)]).filter(([, xs]) => xs.length);
      const tabla = (xs) => `<table class="t"><thead><tr><th class="i">Serie</th><th>Último</th><th>1D</th><th>1M</th><th>12M</th><th>90 sesiones</th><th class="i">Mueve a</th><th class="i">Al</th></tr></thead><tbody>${xs.map((x) => `
        <tr class="clic ${x.k === sel ? 'sel' : ''}" data-ir="#/macro/${x.k}"><td class="i"><b class="acc">${esc(x.k)}</b> <span class="nombre">${esc(x.n)}</span></td>
        <td>${x.tipo === 'tasa' ? F.num(x.ult, 3) + '%' : F.precio(x.ult)}</td>
        ${[x.d1, x.m1, x.a1].map((v, i) => `<td>${x.tipo === 'tasa' ? `<span class="${F.cls(v)}">${N.esNum(v) ? (v > 0 ? '+' : v < 0 ? '−' : '') + F.num(Math.abs(v), 0) + ' pb' : '—'}</span>` : UI.cambio(v, i ? 1 : 2)}</td>`).join('')}
        <td>${N.spark(x.spk, { w: 90, h: 18 })}</td>
        <td class="i mueve">${x.mueve.slice(0, 3).map((t) => `<span class="chip info" data-ir="#/eq/${t}">${esc(t)}</span>`).join(' ')}${x.mueve.length > 3 ? ` <span class="dim" title="${esc(x.mueve.slice(3).join(', '))}">+${x.mueve.length - 3}</span>` : ''}</td>
        <td class="i dim">${F.fechaCorta(x.fecha)}</td></tr>`).join('')}</tbody></table>`;
      cont.innerHTML = `${UI.titulo('Macro y mercados', 'Índices, divisas, tasas y materias primas que mueven a las emisoras del fondo')}
        <div class="rejilla g2">${grupos.map(([n, xs]) => UI.panel(n, tabla(xs), { p0: true })).join('')}</div>
        <div class="rejilla g21" style="margin-top:8px">
          ${UI.panel(`${esc(sel)} · ${esc((M[sel] || {}).n || '')}`, '<div class="graf medio" id="mGraf"></div>', { nota: esc(N.fuente((M[sel] || {}).fuente || '')) })}
          ${UI.panel('Qué emisoras se mueven con esta serie', '<div id="mSens1"></div>', { p0: true, nota: 'correlación de rendimientos diarios · 12 meses' })}
        </div>
        ${UI.panel('Matriz de sensibilidad', '<div id="mMatriz"></div>', { p0: true, nota: 'correlación diaria a 12 meses de cada emisora con cada factor · verde = se mueven juntos', clase: 'ancho' })}
        ${!Object.keys(M).some((k) => M[k].fuente === 'Banxico') ? '<p class="dim" style="font-size:10.5px;margin-top:6px">Tasa objetivo, TIIE, CETES e inflación de Banxico aparecen al agregar el secreto <b>BANXICO_TOKEN</b> en el repositorio (token gratuito del SIE).</p>' : ''}`;
      Local.guardar('macro:sel', sel);
      const s = M[sel];
      if (s) N.G.lineas($('#mGraf', cont), [{ titulo: sel, datos: s.d.map((f, i) => ({ time: f, value: s.c[i] })).filter((x) => N.esNum(x.value)) }], { area: true });
      // sensibilidad
      const factores = FACTORES.filter((k) => M[k]);
      const filas = D.emisoras(false).map((e) => {
        const se = serieEmisora(e.t), o = { t: e.t, sector: e.sector };
        factores.forEach((k) => { const [x, y] = rendimientosAlineados(se, M[k]); o[k] = correl(x, y); });
        return o;
      });
      const uno = filas.filter((f) => N.esNum(f[sel])).sort((a, b) => b[sel] - a[sel]);
      $('#mSens1', cont).innerHTML = M[sel] && factores.includes(sel)
        ? `<table class="t"><tbody>${[...uno.slice(0, 6), ...uno.slice(-4)].map((f) => `<tr class="clic" data-ir="#/eq/${f.t}"><td class="i">${UI.sym(f.t)}</td><td style="width:50%"><span class="barra-mini" style="width:${(Math.abs(f[sel]) * 100).toFixed(0)}%;background:${f[sel] >= 0 ? 'var(--pos)' : 'var(--neg)'}"></span></td><td>${F.num(f[sel], 2)}</td></tr>`).join('')}</tbody></table>`
        : '<div class="vacio">Elija un factor de la matriz (dólar, cobre, oro, plata, petróleo, gas, bono de EUA, S&P 500 o real).</div>';
      UI.tabla($('#mMatriz', cont), [
        { k: 't', t: 'Emisora', i: true, f: (x) => UI.sym(x.t) }, { k: 'sector', t: 'Sector', i: true, cls: () => 'sec' },
        ...factores.map((k) => ({ k, t: k, f: (x) => `<span style="display:inline-block;min-width:44px;padding:0 4px;border-radius:2px;background:${colorCorr(x[k])}">${N.esNum(x[k]) ? F.num(x[k], 2) : '—'}</span>` })),
      ], filas, { orden: factores.includes(sel) ? sel : null, alClic: (t) => App.ir(`#/eq/${t}`) });
    },
  });

  // ───────────────────────── FILTRO ─────────────────────────
  const PRESETS = {
    qvm: { n: 'QVM en vivo', d: 'Las mejor calificadas con el modelo del fondo', c: [], orden: 'qvm' },
    valor: { n: 'Valor', d: 'P/U bajo con dividendo', c: [['pe', '<=', 12], ['rend_dividendo', '>=', 3]], orden: 'pe' },
    calidad: { n: 'Calidad', d: 'ROE alto y deuda baja', c: [['roe', '>=', 15], ['deuda_neta_uafida', '<=', 2]], orden: 'roe' },
    momentum: { n: 'Momentum', d: 'Tendencia de 12 meses y arriba de su PM 200', c: [['momentum_12_1', '>=', 10], ['vs_sma200', '>=', 0]], orden: 'momentum_12_1' },
    dividendos: { n: 'Dividendos', d: 'Rendimiento por dividendo alto', c: [['rend_dividendo', '>=', 4]], orden: 'rend_dividendo' },
    defensivas: { n: 'Defensivas', d: 'Beta baja y volatilidad baja', c: [['beta_1a', '<=', 0.8], ['volatilidad', '<=', 25]], orden: 'volatilidad' },
    sobrevendidas: { n: 'Sobrevendidas', d: 'RSI debajo de 35', c: [['rsi14', '<=', 35]], orden: 'rsi14' },
    maximos: { n: 'Cerca de máximos', d: 'A menos de 5% del máximo de 52 semanas', c: [['dist_maximo', '>=', -5]], orden: 'dist_maximo' },
  };
  App.registrar('filtro', {
    titulo: () => 'Filtro',
    pintar(cont) {
      const defs = (D.kpisArch && D.kpisArch.definiciones) || {};
      const fam = (D.kpisArch && D.kpisArch.familias) || {};
      const st = Local.leer('filtro', { preset: 'qvm', c: [], sector: '' });
      const opciones = Object.entries(defs).sort((a, b) => (a[1].familia || '').localeCompare(b[1].familia || '') || a[1].nombre.localeCompare(b[1].nombre))
        .map(([k, d]) => `<option value="${k}">${esc((fam[d.familia] || d.familia || '') + ' · ' + d.nombre)}</option>`).join('');
      const sectores = [...new Set(D.emisoras(false).map((e) => e.sector))].sort();
      cont.innerHTML = `${UI.titulo('Filtro de emisoras', 'Combine KPIs para encontrar ideas · los porcentajes se escriben en %, los múltiplos en veces')}
        <div class="graf-barra">${Object.entries(PRESETS).map(([k, p]) => `<button class="btn sm ${st.preset === k ? 'on' : ''}" data-p="${k}" title="${esc(p.d)}">${esc(p.n.toUpperCase())}</button>`).join('')}</div>
        <div class="rejilla g12">
          ${UI.panel('Criterios', `<div id="fCrit"></div><div class="graf-barra" style="margin-top:8px"><button class="btn sm" id="fMas">+ CRITERIO</button>
            <select id="fSec"><option value="">Todos los sectores</option>${sectores.map((s) => `<option ${st.sector === s ? 'selected' : ''}>${esc(s)}</option>`).join('')}</select></div>
            <p class="dim" style="font-size:10.5px;margin-top:8px">${esc((PRESETS[st.preset] || {}).d || 'Filtro personalizado')}. El orden «QVM» usa la calificación compuesta (Quality 40 · Value 10 · Momentum 50) calculada con datos públicos.</p>`)}
          ${UI.panel('Resultados', '<div id="fRes"></div>', { p0: true, nota: '<span id="fN"></span>' })}
        </div>`;
      const crit = $('#fCrit', cont);
      const dibujarCriterios = () => {
        crit.innerHTML = st.c.map(([k, op, v], i) => `<div class="criterio" data-i="${i}"><select data-c="k">${opciones}</select>
          <select data-c="op"><option value=">=">≥</option><option value="<=">≤</option></select><input data-c="v" type="number" step="any" value="${v}">
          <button class="btn sm" data-c="x" aria-label="Quitar criterio">✕</button></div>`).join('') || '<div class="dim">Sin criterios: se muestran todas.</div>';
        $$('.criterio', crit).forEach((row) => {
          const i = +row.dataset.i; const [k, op] = st.c[i];
          $('[data-c="k"]', row).value = k; $('[data-c="op"]', row).value = op;
          row.addEventListener('change', () => { st.c[i] = [$('[data-c="k"]', row).value, $('[data-c="op"]', row).value, parseFloat($('[data-c="v"]', row).value)]; st.preset = ''; correr(); });
          $('[data-c="x"]', row).addEventListener('click', () => { st.c.splice(i, 1); st.preset = ''; dibujarCriterios(); correr(); });
        });
      };
      const correr = () => {
        Local.guardar('filtro', st);
        const cols = [...new Set(st.c.map((c) => c[0]))];
        const filas = D.emisoras(false).filter((e) => !st.sector || e.sector === st.sector).map((e) => {
          const o = { t: e.t, sector: e.sub, cp: D.cot(e.t).cp, qvm: ((D.kp(e.t) || {}).qvm || {}).z };
          cols.forEach((k) => { o[k] = D.valor(e.t, k); });
          o.ok = st.c.every(([k, op, v]) => {
            const x = D.valor(e.t, k); if (!N.esNum(x) || !N.esNum(v)) return false;
            const u = (defs[k] || {}).unidad; const val = u === '%' ? x * 100 : x;
            return op === '>=' ? val >= v : val <= v;
          });
          return o;
        }).filter((o) => o.ok);
        $('#fN', cont).textContent = `${filas.length} de ${D.emisoras(false).length}`;
        const orden = (PRESETS[st.preset] || {}).orden || cols[0] || 'qvm';
        UI.tabla($('#fRes', cont), [
          { k: 't', t: 'Emisora', i: true, f: (x) => UI.sym(x.t, { nombre: true }) }, { k: 'sector', t: 'Subsector', i: true, cls: () => 'sec' },
          { k: 'cp', t: 'Hoy', f: (x) => UI.cambio(x.cp) },
          { k: 'qvm', t: 'QVM z', f: (x) => `<span class="${F.cls(x.qvm)}">${N.esNum(x.qvm) ? F.num(x.qvm, 2) : '—'}</span>` },
          ...cols.map((k) => ({ k, t: esc((defs[k] || {}).nombre || k).slice(0, 26), f: (x) => F.kpi(x[k], (defs[k] || {}).unidad) })),
        ], filas, { orden, dir: (defs[orden] || {}).mejor === 'bajo' ? 1 : -1, alClic: (t) => App.ir(`#/eq/${t}/kpis`) });
      };
      $$('[data-p]', cont).forEach((b) => b.addEventListener('click', () => { st.preset = b.dataset.p; st.c = PRESETS[b.dataset.p].c.map((x) => x.slice()); Local.guardar('filtro', st); App.pintar(); }));
      $('#fMas', cont).addEventListener('click', () => { st.c.push(['roe', '>=', 10]); st.preset = ''; dibujarCriterios(); correr(); });
      $('#fSec', cont).addEventListener('change', (ev) => { st.sector = ev.target.value; correr(); });
      if (st.preset && PRESETS[st.preset] && !st.c.length) st.c = PRESETS[st.preset].c.map((x) => x.slice());
      dibujarCriterios(); correr();
    },
  });

  // ───────────────────────── COMPARAR ─────────────────────────
  const FILAS_COMP = ['rend_ytd', 'rend_1a', 'volatilidad', 'beta_1a', 'max_caida', 'crec_ventas', 'margen_uafida', 'margen_neto', 'roe', 'roic',
    'deuda_neta_uafida', 'margen_flujo_libre', 'pe', 've_uafida', 'p_vl', 'rend_dividendo', 'momentum_12_1', 'rsi14'];
  App.registrar('comp', {
    titulo: () => 'Comparar',
    pintar(cont, args) {
      let ts = (args[0] || '').split(',').map((t) => t.toUpperCase()).filter((t) => D.U[t]);
      if (!ts.length) ts = Local.leer('comp', ['FEMSAUBD', 'KOFUBL', 'AC', 'WALMEX']).filter((t) => D.U[t]);
      Local.guardar('comp', ts);
      const dias = Local.leer('comp:dias', 252);
      cont.innerHTML = `${UI.titulo('Comparar emisoras', 'Rendimiento normalizado a 100 y KPIs lado a lado')}
        <div class="graf-barra">${ts.map((t) => `<span class="chip acc">${esc(t)} <button data-q="${t}" aria-label="Quitar ${esc(t)}">✕</button></span>`).join('')}
          <select id="cAdd"><option value="">+ agregar emisora</option>${D.emisoras().filter((e) => !ts.includes(e.t)).map((e) => `<option value="${e.t}">${e.t} · ${esc(e.n)}</option>`).join('')}</select>
          <span class="sep"></span>${[[63, '3M'], [126, '6M'], [252, '1A'], [504, '2A']].map(([d, n]) => `<button class="btn sm ${dias === d ? 'on' : ''}" data-d="${d}">${n}</button>`).join('')}
          <span class="sep"></span><button class="btn sm" id="cIpc" title="Agrega el ETF del índice de referencia">+ MEXTRAC</button></div>
        <div class="rejilla g21">${UI.panel('Rendimiento base 100', '<div class="graf" id="cGraf" style="height:340px"></div>')}
          ${UI.panel('Correlación entre ellas', '<div id="cCorr"></div>', { p0: true, nota: 'rendimientos diarios del periodo' })}</div>
        ${UI.panel('KPIs lado a lado', '<div id="cTab"></div>', { p0: true, nota: 'en ámbar el mejor de cada renglón' })}`;
      const ir = (lista) => App.ir(`#/comp/${lista.join(',')}`);
      $$('[data-q]', cont).forEach((b) => b.addEventListener('click', () => ir(ts.filter((t) => t !== b.dataset.q))));
      $('#cAdd', cont).addEventListener('change', (ev) => { if (ev.target.value) ir([...ts, ev.target.value].slice(0, 8)); });
      $$('[data-d]', cont).forEach((b) => b.addEventListener('click', () => { Local.guardar('comp:dias', +b.dataset.d); App.pintar(); }));
      $('#cIpc', cont).addEventListener('click', () => { if (!ts.includes('MEXTRAC')) ir([...ts, 'MEXTRAC']); });
      const fechas = D.fechas(dias + 1);
      const series = ts.map((t) => {
        const s = D.serie(t, dias + 1); const base = s.find(N.esNum);
        return { titulo: t, datos: fechas.map((f, i) => (N.esNum(s[i]) && base ? { time: f, value: (s[i] / base) * 100 } : null)).filter(Boolean) };
      });
      N.G.lineas($('#cGraf', cont), series);
      const rets = ts.map((t) => { const s = D.serie(t, dias + 1); return s.slice(1).map((x, i) => (s[i] && x ? x / s[i] - 1 : 0)); });
      $('#cCorr', cont).innerHTML = `<table class="t"><thead><tr><th></th>${ts.map((t) => `<th>${esc(t)}</th>`).join('')}</tr></thead><tbody>${ts.map((a, i) => `<tr><td class="i acc">${esc(a)}</td>${ts.map((b, j) => {
        const r = i === j ? 1 : correl(rets[i], rets[j]);
        return `<td style="background:${i === j ? 'transparent' : colorCorr(r)}">${N.esNum(r) ? F.num(r, 2) : '—'}</td>`; }).join('')}</tr>`).join('')}</tbody></table>`;
      const defs = (D.kpisArch && D.kpisArch.definiciones) || {};
      const filas = FILAS_COMP.filter((k) => ts.some((t) => N.esNum(D.valor(t, k))));
      $('#cTab', cont).innerHTML = `<div class="tabla-env"><table class="t"><thead><tr><th class="i">KPI</th>${ts.map((t) => `<th>${UI.sym(t)}</th>`).join('')}</tr></thead><tbody>${filas.map((k) => {
        const d = defs[k] || {}; const vals = ts.map((t) => D.valor(t, k));
        const validos = vals.filter(N.esNum);
        const mejor = d.mejor === 'neutral' || !validos.length ? null : d.mejor === 'bajo' ? Math.min(...validos) : Math.max(...validos);
        return `<tr><td class="i dim">${esc(d.nombre || k)}</td>${vals.map((v) => `<td class="${v === mejor ? 'acc' : ''}">${esc(F.kpi(v, d.unidad))}</td>`).join('')}</tr>`;
      }).join('')}</tbody></table></div>`;
    },
  });
})(window.NST);
