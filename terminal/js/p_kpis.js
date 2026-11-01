/* North Star Terminal · pestaña de KPIs de la ficha
   1. Tablero con los KPIs que más importan según el tipo de empresa.
   2. KPIs operativos del sector: los que captura el equipo en empresas.txt, más el
      catálogo de lo que conviene vigilar en ese sector.
   3. KPIs financieros, de valuación y de mercado calculados por el pipeline, cada uno
      contra la mediana de sus pares y del universo, con su fórmula a la vista.
   4. Factores QVM del equipo contra la aproximación con datos públicos.
   Clic en cualquier KPI: ranking de las 37 emisoras para ese indicador. */
'use strict';
(function (N) {
  const { F, esc, $, $$, D, UI } = N;

  const ORDEN = ['crecimiento', 'margenes', 'rentabilidad', 'balance', 'flujo', 'bancario', 'seguros', 'valuacion', 'mercado', 'riesgo', 'tecnico', 'liquidez'];
  const DESTACADOS = {
    general: ['crec_ventas', 'margen_uafida', 'roe', 'roic', 'deuda_neta_uafida', 'margen_flujo_libre', 'pe', 've_uafida'],
    bancos: ['roe', 'min_activos', 'costo_riesgo', 'crec_cartera', 'capital_activos', 'p_vl', 'pe', 'rend_dividendo'],
    microfinanzas: ['roe', 'min_activos', 'costo_riesgo', 'crec_cartera', 'capital_activos', 'p_vl', 'pe', 'rend_dividendo'],
    seguros: ['roe', 'crec_ventas', 'siniestralidad', 'margen_neto', 'p_vl', 'pe', 'rend_dividendo', 'beta_1a'],
    etf: ['rend_ytd', 'rend_1a', 'volatilidad', 'beta_1a', 'max_caida', 'importe_diario', 'sharpe', 'rsi14'],
  };
  const TEND = { mejora: ['▲', 'pos', 'mejora'], empeora: ['▼', 'neg', 'empeora'], estable: ['■', 'neu', 'estable'] };

  /** ¿Mejor o peor que la referencia (pares si los hay, si no el universo)? */
  function calificar(k) {
    if (!N.esNum(k.valor) || k.mejor === 'neutral') return '';
    const ref = N.esNum(k.mediana_sector) ? k.mediana_sector : k.mediana_universo;
    if (!N.esNum(ref) || ref === k.valor) return '';
    const mejor = k.mejor === 'bajo' ? k.valor < ref : k.valor > ref;
    return mejor ? 'mejor' : 'peor';
  }

  function tarjeta(t, k) {
    const cal = calificar(k);
    const tend = k.tendencia && TEND[k.tendencia];
    const serie = (k.serie || []).filter((s) => N.esNum(s.v));
    const pct = N.esNum(k.percentil) ? Math.round(k.percentil * 100) : null;
    const detalle = k.clave === 'ciclo_efectivo' && k.detalle
      ? `Inventario ${F.num(k.detalle.inventario, 0)} d · cobro ${F.num(k.detalle.cobro, 0)} d · pago ${F.num(k.detalle.pago, 0)} d`
      : k.clave === 'vs_sma200' && k.detalle ? `PM 50 ${F.precio(k.detalle.sma50)} · PM 200 ${F.precio(k.detalle.sma200)}${k.detalle.cruce ? ` · cruce ${esc(k.detalle.cruce)}` : ''}`
        : k.clave === 'dist_maximo' && k.detalle ? `Máximo ${F.precio(k.detalle.maximo)} · mínimo ${F.precio(k.detalle.minimo)}` : '';
    const extra = [k.detalle && k.detalle.nota ? esc(k.detalle.nota) : '', k.detalle && k.detalle.fuente ? `Fuente: ${esc(k.detalle.fuente)}` : '']
      .filter(Boolean).map((x) => `<div style="margin-top:3px">${x}</div>`).join('');
    return `<div class="kpi ${cal}" data-k="${esc(k.clave)}">
      <div class="k"><span>${esc(k.nombre || k.clave)}</span><button type="button" aria-label="Qué mide y cómo se calcula" data-exp>i</button></div>
      <div class="fila"><div><div class="v ${k.unidad === '%' && /^(crec|rend|momentum|vs_|dist|max_caida)/.test(k.clave) ? F.cls(k.valor) : ''}" data-rank title="Ver el ranking del universo">${esc(F.kpi(k.valor, k.unidad, k.moneda))}</div>
        <div class="p">${esc(k.periodo || '')}${tend ? ` <span class="tend ${tend[1]}">${tend[0]} ${tend[2]}</span>` : ''}</div></div>
        <div>${serie.length > 1 ? N.barras(k.serie, { w: 84, h: 26, unidad: k.serie_nombre ? 'dinero' : k.unidad }) : ''}</div></div>
      <div class="cmp"><span>pares <b>${esc(F.kpi(k.mediana_sector, k.unidad, k.moneda))}</b></span><span>universo <b>${esc(F.kpi(k.mediana_universo, k.unidad, k.moneda))}</b></span></div>
      ${pct !== null ? `<div class="pct" title="Percentil ${pct} en el universo (100 = el mejor)"><i style="width:${pct}%"></i></div>` : ''}
      <div class="exp">${esc(k.que || '')}${k.formula ? `<code>${esc(k.formula)}</code>` : ''}${k.serie_nombre ? `<div class="dim" style="margin-top:3px">Barras: ${esc(k.serie_nombre)}</div>` : ''}${detalle ? `<div style="margin-top:3px">${detalle}</div>` : ''}${extra}${pct !== null ? `<div class="dim" style="margin-top:3px">Percentil ${pct} de ${D.emisoras(false).length} emisoras · 100 = el mejor</div>` : ''}</div>
    </div>`;
  }

  // ¿Un KPI del catálogo ya está capturado? Se comparan palabras clave, expandiendo siglas (VMT, MIN, IMOR...).
  const ABR = { vmt: 'ventas mismas tiendas', min: 'margen interes neto', imor: 'morosidad', asm: 'capacidad asientos', abr: 'area bruta rentable' };
  const VACIAS = new Set(['del', 'las', 'los', 'por', 'con', 'sin', 'para', 'que', 'una', 'sobre', 'contra']);
  const fichas = (s) => String(s || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9 ]/g, ' ')
    .split(/\s+/).filter((w) => w.length > 2 && !VACIAS.has(w)).flatMap((w) => (ABR[w] ? ABR[w].split(' ') : [w]));
  function capturado(nombreCat, capturados) {
    const t = fichas(nombreCat); if (!t.length) return false;
    return capturados.some((c) => { const u = new Set(fichas([c.nombre, c.valor, c.tendencia].join(' '))); return t.filter((w) => u.has(w)).length / t.length >= 0.5; });
  }

  function operativos(t, kp) {
    const e = D.U[t] || {};
    const cat = ((D.kpisArch && D.kpisArch.catalogo) || {})[e.grupo] || [];
    const capturados = (kp && kp.operativos) || [];
    const pendientes = cat.filter(([n]) => !capturado(n, capturados));
    const tarjeta = (c) => `<div class="kpi-op"><div class="k">${esc(c.nombre)}</div><div class="v">${esc(c.valor || 'n/d')}</div>
      <div class="p">${esc([c.periodo, c.tendencia].filter(Boolean).join(' · '))}</div>${c.porque ? `<div class="w">${esc(c.porque)}</div>` : ''}</div>`;
    const porCapturar = ([n, w]) => `<div class="kpi-op pendiente"><div class="k">${esc(n)}</div><div class="v">por capturar</div><div class="w">${esc(w)}</div></div>`;
    const cuerpo = capturados.length
      ? `<div class="kpis">${capturados.map(tarjeta).join('')}</div>${pendientes.length ? `<p class="dim" style="font-size:10.5px;margin-top:6px">También conviene vigilar en ${esc(e.grupo_n || 'el sector')}: ${pendientes.map(([n, w]) => `<span title="${esc(w)}" class="chip">${esc(n)}</span>`).join(' ')}</p>` : ''}`
      : `<div class="kpis">${cat.map(porCapturar).join('') || '<div class="vacio">Sin catálogo para este sector.</div>'}</div>`;
    return `<div class="kpi-sec"><h3>KPIs operativos · ${esc(e.grupo_n || e.sub || '')} <span class="nota">${capturados.length ? `${capturados.length} capturados por el equipo de los reportes trimestrales` : 'catálogo de lo que conviene vigilar en el sector'}</span></h3>
      ${cuerpo}
      <p class="dim" style="font-size:10.5px;margin-top:6px">Para capturar o actualizar uno, agrega una línea en el bloque <b class="acc">=== ${esc(t)} ===</b> de <b>empresas.txt</b>:
      <code class="acc">kpis:</code> seguido de <code class="acc">- nombre | valor | periodo | tendencia | por qué importa</code>. La terminal y el tablero lo leen solos.</p></div>`;
  }

  function factores(t, kp) {
    const eq = (kp && kp.factores_equipo) || {};
    const vivo = (kp && kp.qvm) || {};
    if (!Object.keys(eq).length && !Object.keys(vivo).length) return '';
    const fila = (n, a, b) => {
      const barra = (v, col) => (N.esNum(v) ? `<i style="${v >= 0 ? 'left:50%' : `left:${50 + Math.max(-50, v * 16.6)}%`};width:${Math.min(50, Math.abs(v) * 16.6)}%;background:${col}"></i>` : '');
      return `<div class="factor"><span>${n}</span><span class="eje">${barra(a, 'var(--acc)')}</span><b class="${F.cls(a)}">${N.esNum(a) ? (a > 0 ? '+' : '') + F.num(a, 2) : '—'}</b></div>
        <div class="factor" style="margin-top:-3px"><span class="dim">en vivo</span><span class="eje">${barra(b, 'var(--info)')}</span><b class="dim">${N.esNum(b) ? (b > 0 ? '+' : '') + F.num(b, 2) : '—'}</b></div>`;
    };
    return `<div class="kpi-sec"><h3>Factores del modelo QVM · Quality 40 · Value 10 · Momentum 50 <span class="nota">ámbar = modelo del equipo (empresas.txt) · cian = aproximación con datos públicos de hoy</span></h3>
      <div class="rejilla g2"><div class="panel"><div class="panel-b">${fila('Quality', eq.quality, vivo.quality)}${fila('Value', eq.value, vivo.value)}${fila('Momentum', eq.momentum, vivo.momentum)}${fila('Compuesto', eq.z_ciclo, vivo.z)}</div></div>
      <div class="panel"><div class="panel-b"><table class="t"><tbody>
        <tr><td class="i dim">Percentil del equipo</td><td>${N.esNum(eq.percentil) ? F.num(eq.percentil, 1) + '%' : '—'}</td></tr>
        <tr><td class="i dim">Rango en vivo</td><td>${vivo.rango ? `${vivo.rango} de ${D.emisoras(false).length}` : '—'}</td></tr>
        <tr><td class="i dim">Percentil en vivo</td><td>${N.esNum(vivo.percentil) ? F.pct(vivo.percentil, 0) : '—'}</td></tr></tbody></table>
        <p class="dim" style="font-size:10.5px;margin-top:6px">En vivo: Quality = ROE, margen neto y deuda neta/UAFIDA; Value = rendimiento de utilidades, valor en libros/precio y dividendo; Momentum = 12-1 y 3 meses. Todo en z-scores del universo. Sirve para ver si la señal del modelo sigue vigente entre rebalanceos.</p></div></div></div></div>`;
  }

  function ranking(el, t, clave) {
    const def = D.def(clave);
    const xs = D.emisoras(false).map((e) => ({ t: e.t, v: D.valor(e.t, clave) })).filter((x) => N.esNum(x.v));
    if (!xs.length) { el.innerHTML = ''; return; }
    const bajo = def.mejor === 'bajo';
    xs.sort((a, b) => (bajo ? a.v - b.v : b.v - a.v));
    const max = Math.max(...xs.map((x) => Math.abs(x.v))) || 1;
    const pares = new Set(((D.kp(t) || {}).pares) || []);
    el.innerHTML = UI.panel(`Ranking · ${esc(def.nombre || clave)}`, `<table class="t"><tbody>${xs.map((x, i) => `<tr class="clic ${x.t === t ? 'sel' : ''}" data-ir="#/eq/${x.t}/kpis">
        <td class="i dim">${i + 1}</td><td class="i">${UI.sym(x.t)}${pares.has(x.t) ? ' <span class="chip info">par</span>' : ''}</td>
        <td style="width:45%"><span class="barra-mini" style="width:${(Math.abs(x.v) / max * 100).toFixed(1)}%;background:${x.t === t ? 'var(--acc)' : pares.has(x.t) ? 'var(--info)' : x.v < 0 ? 'var(--neg)' : 'var(--line-3)'}"></span></td>
        <td>${esc(F.kpi(x.v, def.unidad))}</td></tr>`).join('')}</tbody></table>`,
    { p0: true, nota: `${bajo ? 'menor es mejor' : def.mejor === 'neutral' ? 'sin dirección' : 'mayor es mejor'} · ${xs.length} emisoras`, acciones: '<button class="btn sm" data-cerrar>CERRAR</button>' });
    $('[data-cerrar]', el).addEventListener('click', () => { el.innerHTML = ''; });
    el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  function pintar(cont, t) {
    const kp = D.kp(t);
    const e = D.U[t] || {};
    if (!D.kpisArch) { cont.innerHTML = '<div class="vacio">Todavía no hay KPIs calculados. Los genera GitHub Actions en la corrida diaria.</div>'; return; }
    const kpis = ((kp && kp.kpis) || []).map((x) => Object.assign({}, D.def(x.clave), x));
    const porClave = Object.fromEntries(kpis.map((k) => [k.clave, k]));
    const tipo = DESTACADOS[e.grupo] ? e.grupo : 'general';
    // Si Yahoo no trae el trimestre de hace un año, el crecimiento a/a queda vacío: en lo esencial va el de 12 meses.
    const dest = DESTACADOS[tipo].map((c) => (c === 'crec_ventas' && !N.esNum((porClave[c] || {}).valor) ? porClave.crec_ventas_udm || porClave[c] : porClave[c])).filter(Boolean);
    const usados = new Set(dest.map((k) => k.clave));
    const fam = (D.kpisArch.familias) || {};
    const sinFin = !kpis.some((k) => ['crecimiento', 'margenes', 'rentabilidad', 'bancario'].includes(k.familia) && N.esNum(k.valor));
    const fuentes = `Último trimestre reportado <b class="acc">${esc((kp && kp.ultimo_trimestre) || 'n/d')}</b> · estados en <b>${esc((kp && kp.moneda_reporte) || 'MXN')}</b>
      · pares: ${((kp && kp.pares) || []).map((p) => `<a data-ir="#/eq/${p}/kpis">${esc(p)}</a>`).join(', ') || '—'} · calculado ${D.kpisArch.generado ? F.fechaHora(D.kpisArch.generado) : '—'}`;
    cont.innerHTML = `
      <div class="leyenda"><span>${fuentes}</span></div>
      <div class="leyenda"><span><i style="background:var(--pos)"></i>mejor que la mediana de sus pares</span><span><i style="background:var(--neg)"></i>peor que la mediana</span>
        <span><i style="background:var(--acc);height:3px"></i>percentil en el universo</span><span>UDM = últimos doce meses · <b class="acc">i</b> = qué mide y fórmula · clic en el valor = ranking</span></div>
      ${sinFin && t !== 'MEXTRAC' ? '<div class="aviso-barra info">Los KPIs de estados financieros llegan con la descarga diaria de Yahoo Finance (GitHub Actions). Mientras tanto se muestran los de mercado, calculados con el histórico.</div>' : ''}
      ${dest.length ? `<div class="kpi-sec"><h3>Lo esencial <span class="nota">${tipo === 'general' ? 'crecimiento, rentabilidad, deuda y valuación' : 'indicadores clave del sector'}</span></h3><div class="kpis">${dest.map((k) => tarjeta(t, k)).join('')}</div></div>` : ''}
      ${t !== 'MEXTRAC' ? operativos(t, kp) : ''}
      ${ORDEN.map((f) => {
        const ks = kpis.filter((k) => k.familia === f && !usados.has(k.clave));
        return ks.length ? `<div class="kpi-sec"><h3>${esc(fam[f] || f)}</h3><div class="kpis">${ks.map((k) => tarjeta(t, k)).join('')}</div></div>` : '';
      }).join('')}
      ${t !== 'MEXTRAC' ? factores(t, kp) : ''}
      <div id="kRank" style="margin-top:8px"></div>
      <p class="dim" style="font-size:10.5px;margin-top:8px">Fuentes: estados financieros, múltiplos y consenso de Yahoo Finance; precios del histórico de la terminal; KPIs operativos y factores del equipo (empresas.txt). Los múltiplos convierten la moneda del reporte a pesos cuando la emisora reporta en dólares.</p>`;
    $$('.kpi [data-exp]', cont).forEach((b) => b.addEventListener('click', () => b.closest('.kpi').classList.toggle('abierto')));
    $$('.kpi [data-rank]', cont).forEach((v) => { v.style.cursor = 'pointer'; v.addEventListener('click', () => ranking($('#kRank', cont), t, v.closest('.kpi').dataset.k)); });
  }

  N.KPIs = { pintar, tarjeta, calificar };
})(window.NST);
