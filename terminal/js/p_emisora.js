/* North Star Terminal · EMISORA: la ficha completa, con pestañas */
'use strict';
(function (N) {
  const { F, esc, $, $$, D, UI, App, Local } = N;

  const PESTANAS = [
    ['resumen', 'Resumen', 'DES'], ['grafica', 'Gráfica', 'GP'], ['financieros', 'Financieros', 'FA'], ['kpis', 'KPIs', 'KPI'],
    ['pares', 'Pares y valuación', 'RV'], ['noticias', 'Noticias', 'N'], ['tesis', 'Tesis del equipo', 'TESIS'], ['dividendos', 'Dividendos', 'DVD'],
  ];
  const BLOQUE = { ACTIVA: 'acc', REPRESENTATIVA: 'info', ETF: 'pos', FUERA: '' };

  function encabezado(t) {
    const e = D.U[t] || {}, q = D.cot(t), f = D.ficha(t), lg = D.logo(t);
    const marca = (e.n || t).replace(/[^A-Za-zÁÉÍÓÚÑ ]/g, '').trim().split(/\s+/).map((w) => w[0]).join('').slice(0, 3).toUpperCase();
    const pos = D.port && D.port.actual && D.port.actual.posiciones.find((x) => x.t === t);
    return `<div class="eq-h">
      <div class="lg"><b>${esc(marca)}</b>${lg ? `<img src="${lg}" alt="" onerror="this.remove()">` : ''}</div>
      <div style="min-width:0"><h2>${esc(f.nombre || e.nombre || e.n || t)}</h2>
        <div class="tk">${esc(t)} <span>· ${esc(e.sector || '')} · ${esc(e.sub || '')} · BMV</span></div>
        <div class="chips" style="margin-top:5px">
          <span class="chip ${BLOQUE[e.bloque] || ''}">${esc(e.bloque === 'FUERA' ? 'FUERA DEL FONDO' : e.bloque || '')}</span>
          ${e.peso_indice ? `<span class="chip">Índice ${F.pct(e.peso_indice)}</span>` : '<span class="chip">Fuera del índice</span>'}
          ${pos ? `<span class="chip acc">En cartera ${F.pct(pos.peso)}</span>` : ''}
          ${f.recomendacion ? `<span class="chip warn">${esc(f.recomendacion)}</span>` : ''}
        </div></div>
      <div class="px"><div class="p">${F.precio(q.p)}</div>
        <div class="c ${F.cls(q.cp)}">${F.flecha(q.cp)} ${q.c != null ? F.num(q.c, 2) : ''} (${F.pctS(q.cp)})</div>
        <div class="t">${q.ts ? F.fechaHora(q.ts) : ''} · ${esc(q.fuente || '')}</div></div>
    </div>`;
  }

  // ───────────── RESUMEN ─────────────
  function resumen(cont, t) {
    const q = D.cot(t), inf = D.info(t), f = D.ficha(t), an = (D.cal.analistas || {})[t] || {};
    const k = (c) => D.kpi(t, c);
    const vk = (c) => { const x = k(c); return x ? F.kpi(x.valor, x.unidad, x.moneda) : 'n/d'; };
    const obj = (an.objetivo && an.objetivo.mean) || inf.targetMeanPrice;
    const pot = obj && q.p ? obj / q.p - 1 : null;
    const datos = [
      ['Apertura', F.precio(q.ab)], ['Máximo / mínimo del día', `${F.precio(q.max)} / ${F.precio(q.min)}`],
      ['Volumen', F.vol(q.v)], ['Importe operado', F.dinero(q.p && q.v ? q.p * q.v : null)],
      ['Rango 52 semanas', `${F.precio(q.lo52 || inf.fiftyTwoWeekLow)} – ${F.precio(q.hi52 || inf.fiftyTwoWeekHigh)}`],
      ['Valor de mercado', F.dinero(inf.marketCap)], ['Valor de la empresa', F.dinero(inf.enterpriseValue)],
      ['P/U (UDM)', vk('pe')], ['VE/UAFIDA', vk('ve_uafida')], ['Precio / valor en libros', vk('p_vl')],
      ['Rendimiento por dividendo', vk('rend_dividendo')], ['ROE', vk('roe')], ['Margen neto', vk('margen_neto')],
      ['Deuda neta / UAFIDA', vk('deuda_neta_uafida')], ['Beta 1 año (IPC)', vk('beta_1a')], ['Volatilidad anual', vk('volatilidad')],
      ['Rendimiento en el año', vk('rend_ytd')], ['Rendimiento 12 meses', vk('rend_1a')],
      ['Consenso', inf.recommendationKey ? `${esc(String(inf.recommendationKey).replace('_', ' ').toUpperCase())} · ${F.num(inf.recommendationMean, 1)}` : 'n/d'],
      ['Precio objetivo promedio', obj ? `${F.precio(obj)} <span class="${F.cls(pot)}">(${F.pctS(pot, 1)})</span>` : 'n/d'],
      ['Analistas', inf.numberOfAnalystOpinions ? F.ent(inf.numberOfAnalystOpinions) : 'n/d'],
      ['Empleados', inf.fullTimeEmployees ? F.ent(inf.fullTimeEmployees) : 'n/d'],
    ];
    const desc = f.descripcion || inf.longBusinessSummary || '';
    const rec = an.recomendaciones;
    let consenso = '<div class="vacio">Sin consenso publicado en Yahoo Finance.</div>';
    if (rec) {
      const tot = rec.strongBuy + rec.buy + rec.hold + rec.sell + rec.strongSell;
      if (tot) {
        const seg = [['strongBuy', 'Compra fuerte', 'var(--pos)'], ['buy', 'Compra', '#5fe0a0'], ['hold', 'Mantener', 'var(--neu)'], ['sell', 'Venta', '#ff8a96'], ['strongSell', 'Venta fuerte', 'var(--neg)']];
        consenso = `<div style="display:flex;height:12px;border-radius:2px;overflow:hidden">${seg.map(([c, , col]) => rec[c] ? `<i style="flex:${rec[c]};background:${col}" title="${rec[c]}"></i>` : '').join('')}</div>
          <div class="chips" style="margin-top:6px">${seg.map(([c, n]) => `<span class="chip">${n} ${rec[c]}</span>`).join('')}</div>
          ${an.objetivo ? `<table class="t" style="margin-top:6px"><tbody><tr><td class="i dim">Objetivo bajo / promedio / alto</td><td>${F.precio(an.objetivo.low)} / <b>${F.precio(an.objetivo.mean)}</b> / ${F.precio(an.objetivo.high)}</td></tr></tbody></table>` : ''}`;
      }
    }
    const pos = D.port && D.port.actual && D.port.actual.posiciones.find((x) => x.t === t);
    const ef = D.port && D.port.actual && D.port.actual.pesos_efectivos ? D.port.actual.pesos_efectivos[t] : null;
    const dev = D.port && D.port.actual && D.port.actual.desviacion ? D.port.actual.desviacion[t] : null;
    const posicion = `<table class="t"><tbody>
      ${pos ? `<tr><td class="i dim">Títulos</td><td>${F.ent(pos.titulos)}</td></tr><tr><td class="i dim">Valor</td><td>${F.pesos(pos.valor)}</td></tr>
      <tr><td class="i dim">Costo promedio</td><td>${F.precio(pos.costo_promedio)}</td></tr><tr><td class="i dim">Ganancia o pérdida</td><td>${UI.num(pos.pyg, F.pesos)} ${UI.cambio(pos.pyg_pct)}</td></tr>
      <tr><td class="i dim">Peso directo</td><td>${F.pct(pos.peso)}</td></tr>` : '<tr><td class="i dim" colspan="2">Sin posición directa</td></tr>'}
      <tr><td class="i dim">Peso efectivo (con el ETF desglosado)</td><td>${F.pct(ef)}</td></tr>
      <tr><td class="i dim">Peso en el índice</td><td>${F.pct((D.U[t] || {}).peso_indice)}</td></tr>
      <tr><td class="i dim">Desviación contra el índice</td><td class="${F.cls(dev)}">${F.pp(dev)}</td></tr></tbody></table>`;
    const evs = D.eventosDe(t).filter((e) => e.fecha >= new Date().toISOString().slice(0, 10)).slice(0, 4);
    cont.innerHTML = `<div class="rejilla g21">
      <div class="rejilla" style="align-content:start">
        ${UI.panel('Datos clave', `<div class="datos-clave">${datos.map(([a, b]) => `<div class="dc"><div class="k">${a}</div><div class="v">${b}</div></div>`).join('')}</div>`, { p0: true })}
        ${UI.panel('Perfil de la compañía', desc ? `<div class="texto">${desc.split('\n').map((p) => `<p>${esc(p)}</p>`).join('')}</div>
          <div class="chips" style="margin-top:8px">${f.sitio || inf.website ? `<a class="chip info" href="${esc(/^https?:/.test(f.sitio || '') ? f.sitio : 'https://' + (f.sitio || String(inf.website || '').replace(/^https?:\/\//, '')))}" target="_blank" rel="noopener">${esc(f.sitio || inf.website)}</a>` : ''}
          ${(inf.directivos || []).slice(0, 3).map((x) => `<span class="chip">${esc(x.nombre)} · ${esc(x.cargo || '')}</span>`).join('')}</div>` : '<div class="vacio">Sin descripción.</div>')}
        ${UI.panel('Últimas noticias', D.noticiasDe(t, 5).map((n) => N.Noticias.tarjeta(n, { corta: true })).join('') || '<div class="vacio">Sin noticias recientes.</div>', { p0: true, acciones: `<a class="btn sm" data-ir="#/eq/${t}/noticias">N ›</a>` })}
      </div>
      <div class="rejilla" style="align-content:start">
        ${UI.panel('Seis meses', '<div class="graf medio" id="eqMini"></div>', { acciones: `<a class="btn sm" data-ir="#/eq/${t}/grafica">GP ›</a>` })}
        ${UI.panel('Posición en el fondo', posicion, { p0: true })}
        ${UI.panel('Consenso de analistas', consenso, { nota: 'Yahoo Finance' })}
        ${UI.panel('Próximos eventos', evs.length ? `<table class="t"><tbody>${evs.map((e) => `<tr><td class="i">${F.fecha(e.fecha)}</td><td class="i" style="white-space:normal">${esc(e.tipo)} · ${esc(e.titulo)}</td></tr>`).join('')}</tbody></table>` : '<div class="vacio">Sin eventos próximos.</div>', { p0: true })}
      </div></div>`;
    D.velas(t).then((v) => {
      const el = $('#eqMini', cont); if (!v || !el || !el.isConnected) return;
      const n = Math.min(v.d.length, 126);
      N.G.lineas(el, [{ titulo: t, datos: v.d.slice(-n).map((f2, i) => ({ time: f2, value: v.c[v.c.length - n + i] })) }], { area: true });
    });
  }

  // ───────────── GRÁFICA ─────────────
  function grafica(cont, t) {
    const pref = Local.leer('graf', { rango: 180, capas: ['sma50', 'sma200'], inf: 'rsi' });
    const rangos = [['1D', 'intra'], ['1M', 31], ['3M', 92], ['6M', 183], ['1A', 366], ['3A', 1096], ['5A', 1827], ['MÁX', 0]];
    const capas = [['sma20', 'PM 20'], ['sma50', 'PM 50'], ['sma200', 'PM 200'], ['ema21', 'EMA 21'], ['bb', 'Bollinger'], ['ipc', 'vs IPC']];
    cont.innerHTML = `<div class="graf-barra">
        ${rangos.map(([n, d]) => `<button class="btn sm ${String(pref.rango) === String(d) ? 'on' : ''}" data-r="${d}">${n}</button>`).join('')}
        <span class="sep"></span>${capas.map(([k, n]) => `<button class="btn sm ${pref.capas.includes(k) ? 'on' : ''}" data-c="${k}">${n}</button>`).join('')}
        <span class="sep"></span>${[['', 'Sin panel'], ['rsi', 'RSI 14'], ['macd', 'MACD']].map(([k, n]) => `<button class="btn sm ${pref.inf === k ? 'on' : ''}" data-i="${k}">${n}</button>`).join('')}
      </div>
      <div class="panel"><div class="panel-b" style="padding:4px"><div class="graf" id="gPrin"><div class="graf-leyenda" id="gLey"></div></div>
      <div class="graf bajo" id="gInf" hidden></div></div></div>
      <p class="dim" style="margin-top:6px;font-size:10.5px">Velas diarias sin ajustar por dividendos · rueda del ratón para acercar · arrastre para desplazarse · fuente: <span id="gFuente">—</span></p>`;
    const guardar = () => Local.guardar('graf', pref);
    $$('[data-r]', cont).forEach((b) => b.addEventListener('click', () => { pref.rango = b.dataset.r === 'intra' ? 'intra' : +b.dataset.r; guardar(); grafica(cont, t); }));
    $$('[data-c]', cont).forEach((b) => b.addEventListener('click', () => {
      const k = b.dataset.c; pref.capas = pref.capas.includes(k) ? pref.capas.filter((x) => x !== k) : [...pref.capas, k];
      guardar(); b.classList.toggle('on'); if (ctrl) ctrl.alternar(k, pref.capas.includes(k));
    }));
    $$('[data-i]', cont).forEach((b) => b.addEventListener('click', () => { pref.inf = b.dataset.i; guardar(); $$('[data-i]', cont).forEach((x) => x.classList.toggle('on', x === b)); if (ctrl) ctrl.inferior(pref.inf); }));
    let ctrl = null;
    if (pref.rango === 'intra') {
      const s = (D.intradia.s || {})[t] || [];
      $('#gFuente', cont).textContent = `barras de 5 minutos del ${F.fecha(D.intradia.fecha)}`;
      if (s.length < 2) { $('#gPrin', cont).innerHTML = '<div class="vacio">Sin intradía para esta emisora en la última sesión.</div>'; return; }
      N.G.lineas($('#gPrin', cont), [{ titulo: t, datos: s.map((x) => ({ time: Math.floor(new Date(x[0]) / 1000) - 6 * 3600, value: x[1] })) }], { area: true });
      return;
    }
    Promise.all([D.velas(t), D.velas('IPC')]).then(([v, ipc]) => {
      const el = $('#gPrin', cont); if (!el || !el.isConnected) return;
      if (!v) { el.innerHTML = '<div class="vacio">Sin velas para esta emisora.</div>'; return; }
      $('#gFuente', cont).textContent = v.fuente || 'Yahoo Finance';
      ctrl = N.G.velas(el, v, { bajo: $('#gInf', cont), ipc });
      if (!ctrl) return;
      pref.capas.forEach((k) => ctrl.alternar(k, true));
      ctrl.inferior(pref.inf);
      ctrl.rango(pref.rango);
      const ley = $('#gLey', cont);
      ctrl.ch.subscribeCrosshairMove((p) => {
        const x = p && p.seriesData && p.seriesData.get(ctrl.sv);
        if (!x) { ley.innerHTML = ''; return; }
        const i = v.d.indexOf(p.time);
        const vol = i >= 0 && v.v ? v.v[i] : null;
        ley.innerHTML = `<b class="acc">${esc(t)}</b><span>${F.fecha(p.time)}</span><span>A <b>${F.precio(x.open)}</b></span><span>M <b>${F.precio(x.high)}</b></span><span>m <b>${F.precio(x.low)}</b></span><span>C <b class="${x.close >= x.open ? 'pos' : 'neg'}">${F.precio(x.close)}</b></span>${vol ? `<span>Vol <b>${F.vol(vol)}</b></span>` : ''}`;
      });
    });
  }

  // ───────────── FINANCIEROS ─────────────
  const ETQ = {
    resultados: { TotalRevenue: 'Ingresos totales', OperatingRevenue: 'Ingresos de operación', CostOfRevenue: 'Costo de ventas', GrossProfit: 'Utilidad bruta',
      SellingGeneralAndAdministration: 'Gastos de venta y administración', OperatingExpense: 'Gastos de operación', TotalExpenses: 'Gastos totales',
      OperatingIncome: 'Utilidad de operación', EBITDA: 'UAFIDA', NormalizedEBITDA: 'UAFIDA normalizada', EBIT: 'UAII (EBIT)',
      ReconciledDepreciation: 'Depreciación y amortización', InterestExpense: 'Gasto por intereses', InterestIncome: 'Ingreso por intereses',
      NetInterestIncome: 'Margen financiero', ProvisionForDoubtfulAccounts: 'Estimación preventiva para riesgos crediticios',
      NetPolicyholderBenefitsAndClaims: 'Siniestros y beneficios', PretaxIncome: 'Utilidad antes de impuestos', TaxProvision: 'Impuestos',
      NetIncome: 'Utilidad neta', NetIncomeCommonStockholders: 'Utilidad neta mayoritaria', MinorityInterests: 'Participación minoritaria',
      DilutedEPS: 'UPA diluida', BasicEPS: 'UPA básica', DilutedAverageShares: 'Acciones promedio diluidas (M)', BasicAverageShares: 'Acciones promedio (M)' },
    balance: { TotalAssets: 'Activos totales', CurrentAssets: 'Activo circulante', CashAndCashEquivalents: 'Efectivo y equivalentes',
      CashCashEquivalentsAndShortTermInvestments: 'Efectivo e inversiones de corto plazo', Receivables: 'Cuentas por cobrar', AccountsReceivable: 'Clientes',
      Inventory: 'Inventarios', NetPPE: 'Propiedad, planta y equipo', GoodwillAndOtherIntangibleAssets: 'Crédito mercantil e intangibles',
      InvestmentProperties: 'Propiedades de inversión', NetLoan: 'Cartera de crédito neta', TotalLiabilitiesNetMinorityInterest: 'Pasivos totales',
      CurrentLiabilities: 'Pasivo circulante', AccountsPayable: 'Proveedores', Payables: 'Cuentas por pagar', CurrentDebt: 'Deuda de corto plazo',
      LongTermDebt: 'Deuda de largo plazo', TotalDebt: 'Deuda total', NetDebt: 'Deuda neta', CapitalLeaseObligations: 'Arrendamientos',
      StockholdersEquity: 'Capital contable mayoritario', CommonStockEquity: 'Capital común', TotalEquityGrossMinorityInterest: 'Capital contable total',
      MinorityInterest: 'Participación no controladora', InvestedCapital: 'Capital invertido', WorkingCapital: 'Capital de trabajo',
      TangibleBookValue: 'Valor en libros tangible', OrdinarySharesNumber: 'Acciones en circulación (M)', ShareIssued: 'Acciones emitidas (M)',
      RetainedEarnings: 'Utilidades retenidas' },
    flujo: { OperatingCashFlow: 'Flujo de operación', CapitalExpenditure: 'Inversiones de capital (CAPEX)', FreeCashFlow: 'Flujo libre',
      InvestingCashFlow: 'Flujo de inversión', FinancingCashFlow: 'Flujo de financiamiento', CashDividendsPaid: 'Dividendos pagados',
      CommonStockDividendPaid: 'Dividendos comunes', RepurchaseOfCapitalStock: 'Recompra de acciones', IssuanceOfDebt: 'Emisión de deuda',
      RepaymentOfDebt: 'Pago de deuda', DepreciationAndAmortization: 'Depreciación y amortización', ChangeInWorkingCapital: 'Cambio en capital de trabajo',
      InterestPaidCFO: 'Intereses pagados (operación)', InterestPaidCFF: 'Intereses pagados (financiamiento)' },
  };
  const RESALTAR = new Set(['TotalRevenue', 'GrossProfit', 'OperatingIncome', 'EBITDA', 'NetIncomeCommonStockholders', 'TotalAssets', 'TotalDebt',
    'StockholdersEquity', 'OperatingCashFlow', 'FreeCashFlow']);
  function financieros(cont, t) {
    const pref = Local.leer('fin', { e: 'resultados', f: 'trimestral' });
    cont.innerHTML = '<div class="cargando">Cargando estados financieros</div>';
    D.estados(t).then((est) => {
      if (!cont.isConnected) return;
      const barra = `<div class="graf-barra">${[['resultados', 'Estado de resultados'], ['balance', 'Balance'], ['flujo', 'Flujo de efectivo']].map(([k, n]) => `<button class="btn sm ${pref.e === k ? 'on' : ''}" data-e="${k}">${n}</button>`).join('')}
        <span class="sep"></span>${[['trimestral', 'Trimestral'], ['anual', 'Anual']].map(([k, n]) => `<button class="btn sm ${pref.f === k ? 'on' : ''}" data-f="${k}">${n}</button>`).join('')}</div>`;
      const tabla = est && est[pref.e] && est[pref.e][pref.f];
      if (!tabla) {
        cont.innerHTML = barra + `<div class="vacio">Todavía no hay estados financieros de ${esc(t)}.<br>Los descarga GitHub Actions de Yahoo Finance al cierre de cada día hábil${t === 'MEXTRAC' ? '; un ETF no publica estados.' : '.'}</div>`;
      } else {
        const per = tabla.periodos;
        const etiqueta = (p) => (pref.f === 'trimestral' ? `${Math.floor((+p.slice(5, 7) - 1) / 3) + 1}T${p.slice(2, 4)}` : p.slice(0, 4));
        const mon = est.moneda || 'MXN';
        const filas = Object.keys(ETQ[pref.e]).filter((k) => tabla.filas[k]).map((k) => {
          const xs = tabla.filas[k];
          const esUPA = /EPS$/.test(k);
          const fmt = (x) => (esUPA ? F.num(x, 2) : F.millones(x, Math.abs(x) < 1e8 ? 1 : 0));
          const ult = xs[xs.length - 1], comp = pref.f === 'trimestral' ? xs[xs.length - 5] : xs[xs.length - 2];
          const g = N.esNum(ult) && N.esNum(comp) && comp !== 0 ? (ult - comp) / Math.abs(comp) : null;
          return `<tr class="${RESALTAR.has(k) ? 'res' : ''}"><td class="i" style="${RESALTAR.has(k) ? 'color:var(--txt);font-weight:600' : 'color:var(--txt-2)'}">${ETQ[pref.e][k]}</td>
            ${xs.map((x) => `<td class="${N.esNum(x) && x < 0 ? 'neg' : ''}">${N.esNum(x) ? fmt(x) : '—'}</td>`).join('')}
            <td>${UI.cambio(g, 1)}</td><td>${N.barras(xs.map((v, i) => ({ p: etiqueta(per[i]), v })), { w: 70, h: 18 })}</td></tr>`;
        }).join('');
        cont.innerHTML = barra + UI.panel(`${{ resultados: 'Estado de resultados', balance: 'Balance general', flujo: 'Flujo de efectivo' }[pref.e]} · ${pref.f}`,
          `<div class="tabla-env"><table class="t"><thead><tr><th class="i">Millones de ${esc(mon)}</th>${per.map((p) => `<th>${etiqueta(p)}</th>`).join('')}<th>${pref.f === 'trimestral' ? 'a/a' : 'vs año previo'}</th><th>Tendencia</th></tr></thead><tbody>${filas}</tbody></table></div>`,
          { p0: true, nota: `Yahoo Finance · ${mon}${(est.avisos || []).length ? ' · faltaron: ' + esc(est.avisos.join(', ')) : ''}` });
      }
      $$('[data-e]', cont).forEach((b) => b.addEventListener('click', () => { pref.e = b.dataset.e; Local.guardar('fin', pref); financieros(cont, t); }));
      $$('[data-f]', cont).forEach((b) => b.addEventListener('click', () => { pref.f = b.dataset.f; Local.guardar('fin', pref); financieros(cont, t); }));
    });
  }

  // ───────────── PARES ─────────────
  function pares(cont, t) {
    const k = D.kp(t) || {};
    const lista = [t, ...(k.pares || [])];
    const sector = (D.U[t] || {}).sector;
    const mismos = D.emisoras(false).filter((e) => e.sector === sector && !lista.includes(e.t)).map((e) => e.t);
    const todos = [...lista, ...mismos];
    const cols = [['pe', 'P/U'], ['ve_uafida', 'VE/UAFIDA'], ['p_vl', 'P/VL'], ['rend_dividendo', 'Div.'], ['roe', 'ROE'], ['margen_neto', 'Mg. neto'],
      ['margen_uafida', 'Mg. UAFIDA'], ['crec_ventas', 'Crec. ingresos'], ['deuda_neta_uafida', 'DN/UAFIDA'], ['beta_1a', 'Beta'], ['rend_1a', '12M']];
    const filas = todos.map((u) => ({ t: u, p: D.precio(u), cp: D.cot(u).cp, grupo: lista.includes(u) ? 'par' : 'sector',
      ...Object.fromEntries(cols.map(([c]) => [c, D.valor(u, c)])) }));
    const med = (c) => { const xs = filas.filter((f) => f.t !== t && f.grupo === 'par').map((f) => f[c]).filter(N.esNum).sort((a, b) => a - b); return xs.length ? xs[Math.floor(xs.length / 2)] : null; };
    const unidad = (c) => D.def(c).unidad || 'x';
    cont.innerHTML = `<div class="rejilla g21">
      ${UI.panel('Comparables', '<div id="parT"></div>', { p0: true, nota: `pares: ${(k.pares || []).join(', ') || '—'} · resto del sector ${esc(sector || '')}` })}
      ${UI.panel('ROE contra precio / valor en libros', '<div id="parG"></div>', { nota: 'todo el universo · resaltados los pares' })}
    </div>
    <div class="rejilla g2" style="margin-top:8px">${UI.panel('P/U contra su propia historia', '<div id="parH1"></div>', { nota: 'trimestral · Yahoo Finance' })}
      ${UI.panel('VE/UAFIDA contra su propia historia', '<div id="parH2"></div>', { nota: 'trimestral · Yahoo Finance' })}</div>`;
    UI.tabla($('#parT', cont), [
      { k: 't', t: 'Emisora', i: true, f: (x) => UI.sym(x.t) + (x.grupo === 'sector' ? ' <span class="dim">sector</span>' : '') },
      { k: 'p', t: 'Precio', f: (x) => F.precio(x.p) }, { k: 'cp', t: 'Hoy', f: (x) => UI.cambio(x.cp) },
      ...cols.map(([c, n]) => ({ k: c, t: n, f: (x) => F.kpi(x[c], unidad(c)) })),
    ], filas, { alClic: (u) => App.ir(`#/eq/${u}/pares`), sel: (x) => x.t === t,
      pie: `<tr><td class="i dim">Mediana de pares</td><td></td><td></td>${cols.map(([c]) => `<td>${F.kpi(med(c), unidad(c))}</td>`).join('')}</tr>` });
    // dispersión
    const pts = D.emisoras(false).map((e) => ({ t: e.t, x: D.valor(e.t, 'roe'), y: D.valor(e.t, 'p_vl') })).filter((p) => N.esNum(p.x) && N.esNum(p.y) && p.y < 15 && p.x > -0.5 && p.x < 1);
    const g = $('#parG', cont);
    if (pts.length < 3) g.innerHTML = '<div class="vacio">Faltan datos de ROE y P/VL (llegan con la descarga diaria de estados financieros).</div>';
    else {
      const W = 420, H = 260, m = 34;
      const xs = pts.map((p) => p.x), ys = pts.map((p) => p.y);
      const x0 = Math.min(0, ...xs), x1 = Math.max(...xs), y0 = 0, y1 = Math.max(...ys);
      const px = (x) => m + ((x - x0) / (x1 - x0 || 1)) * (W - m - 10), py = (y) => H - m + 10 - ((y - y0) / (y1 - y0 || 1)) * (H - m - 10);
      g.innerHTML = `<svg viewBox="0 0 ${W} ${H}" width="100%" role="img" aria-label="Dispersión de ROE contra P/VL">
        <line x1="${m}" y1="${H - m + 10}" x2="${W - 10}" y2="${H - m + 10}" stroke="var(--line-3)"/><line x1="${m}" y1="10" x2="${m}" y2="${H - m + 10}" stroke="var(--line-3)"/>
        <text x="${W - 10}" y="${H - 6}" fill="var(--txt-3)" font-size="9" text-anchor="end">ROE ${F.pct(x1, 0)}</text><text x="${m + 2}" y="18" fill="var(--txt-3)" font-size="9">P/VL ${F.num(y1, 1)}x</text>
        ${pts.map((p) => { const on = lista.includes(p.t); return `<g data-ir="#/eq/${p.t}/pares" style="cursor:pointer"><circle cx="${px(p.x).toFixed(1)}" cy="${py(p.y).toFixed(1)}" r="${p.t === t ? 6 : on ? 4.5 : 3}" fill="${p.t === t ? 'var(--acc)' : on ? 'var(--info)' : 'var(--line-3)'}"><title>${p.t}: ROE ${F.pct(p.x, 1)} · P/VL ${F.num(p.y, 2)}x</title></circle>
          ${on ? `<text x="${(px(p.x) + 7).toFixed(1)}" y="${(py(p.y) + 3).toFixed(1)}" fill="var(--txt-2)" font-size="9">${p.t}</text>` : ''}</g>`; }).join('')}</svg>`;
    }
    const mh = D.multiplos[t];
    [['pe', '#parH1'], ['ve_uafida', '#parH2']].forEach(([c, sel]) => {
      const el = $(sel, cont), fila = mh && mh.filas && mh.filas[c];
      if (!fila || fila.filter(N.esNum).length < 2) { el.innerHTML = '<div class="vacio">Sin historia de múltiplos.</div>'; return; }
      const serie = fila.map((v, i) => ({ p: `${Math.floor((+mh.periodos[i].slice(5, 7) - 1) / 3) + 1}T${mh.periodos[i].slice(2, 4)}`, v }));
      const vals = fila.filter(N.esNum); const prom = vals.reduce((a, b) => a + b, 0) / vals.length;
      el.innerHTML = `<div style="display:flex;align-items:flex-end;gap:14px;flex-wrap:wrap">${N.barras(serie, { w: 260, h: 70, unidad: 'x' })}
        <table class="t" style="width:auto"><tbody><tr><td class="i dim">Actual</td><td>${F.kpi(mh.actual && mh.actual[c], 'x')}</td></tr><tr><td class="i dim">Promedio del periodo</td><td>${F.kpi(prom, 'x')}</td></tr>
        <tr><td class="i dim">Mínimo / máximo</td><td>${F.kpi(Math.min(...vals), 'x')} / ${F.kpi(Math.max(...vals), 'x')}</td></tr></tbody></table></div>`;
    });
  }

  // ───────────── TESIS ─────────────
  function tesis(cont, t) {
    const f = D.ficha(t);
    if (!Object.keys(f).length) { cont.innerHTML = '<div class="vacio">Sin ficha del equipo. Se arma sola con el bloque === ' + esc(t) + ' === de empresas.txt.</div>'; return; }
    const z = f.factores_z || {};
    const barra = (n, v) => `<div class="factor"><span>${n}</span><span class="eje">${N.esNum(v) ? `<i style="${v >= 0 ? 'left:50%' : `left:${50 + Math.max(-50, v * 16.6)}%`};width:${Math.min(50, Math.abs(v) * 16.6)}%;background:${v >= 0 ? 'var(--pos)' : 'var(--neg)'}"></i>` : ''}</span><b class="${F.cls(v)}">${N.esNum(v) ? (v > 0 ? '+' : '') + F.num(v, 2) : '—'}</b></div>`;
    const lst = (xs, c) => (xs && xs.length ? `<ul class="lista ${c}">${xs.map((x) => `<li>${esc(x)}</li>`).join('')}</ul>` : '<div class="vacio">—</div>');
    const datos = [['Recomendación', f.recomendacion], ['Convicción', f.conviccion], ['Señal del modelo', f.senal_modelo], ['Bloque', f.bloque],
      ['Peso objetivo', f.peso_objetivo], ['Peso en el índice', f.peso_indice], ['Peso efectivo', f.peso_efectivo], ['Desviación', f.desviacion]].filter(([, v]) => v);
    cont.innerHTML = `<div class="rejilla g21">
      <div class="rejilla" style="align-content:start">
        ${UI.panel('Nuestra tesis', f.tesis ? `<div class="texto">${f.tesis.split('\n').map((p) => `<p>${esc(p)}</p>`).join('')}</div>` : '<div class="vacio">—</div>')}
        <div class="rejilla g2">${UI.panel('Catalizadores', lst(f.catalizadores, 'pos'))}${UI.panel('Riesgos', lst(f.riesgos, 'neg'))}</div>
        ${f.fortalezas ? UI.panel('Fortalezas', lst(f.fortalezas, '')) : ''}
      </div>
      <div class="rejilla" style="align-content:start">
        ${UI.panel('Postura en el fondo', `<table class="t"><tbody>${datos.map(([k, v]) => `<tr><td class="i dim">${k}</td><td style="white-space:normal">${esc(v)}</td></tr>`).join('')}</tbody></table>`, { p0: true })}
        ${UI.panel('Factores del modelo QVM', `${barra('Quality', z.quality)}${barra('Value', z.value)}${barra('Momentum', z.momentum)}${barra('z del ciclo', z.z_ciclo)}
          <p class="dim" style="margin-top:6px;font-size:10.5px">${esc(f.factores || '')}</p>`, { nota: 'del equipo · empresas.txt' })}
        ${UI.panel('Datos de mercado de la ficha', `<table class="t"><tbody>${[['Rango 52 semanas', f.rango_52s], ['En el año', f.ytd], ['1 año', f.rend_1a], ['3 años', f.rend_3a], ['5 años', f.rend_5a], ['Beta 5 años', f.beta_5a], ['Volatilidad anual', f.volatilidad_anual], ['R² contra el índice', f.r2_vs_indice]]
          .filter(([, v]) => v).map(([k, v]) => `<tr><td class="i dim">${k}</td><td>${esc(v)}</td></tr>`).join('')}</tbody></table>`, { p0: true, nota: 'capturados por el equipo con Refinitiv' })}
      </div></div>`;
  }

  // ───────────── DIVIDENDOS ─────────────
  function dividendos(cont, t) {
    cont.innerHTML = '<div class="cargando">Cargando</div>';
    D.velas(t).then((v) => {
      if (!cont.isConnected) return;
      const divs = ((v && v.div) || []).slice().sort((a, b) => b[0].localeCompare(a[0]));
      if (!divs.length) { cont.innerHTML = '<div class="vacio">Sin dividendos registrados en el periodo.</div>'; return; }
      const hoy = new Date().toISOString().slice(0, 10);
      const hace = new Date(); hace.setFullYear(hace.getFullYear() - 1);
      const udm = divs.filter((d) => d[0] <= hoy && d[0] > hace.toISOString().slice(0, 10)).reduce((a, d) => a + d[1], 0);
      const porAnio = {}; divs.forEach((d) => { if (d[0] <= hoy) porAnio[d[0].slice(0, 4)] = (porAnio[d[0].slice(0, 4)] || 0) + d[1]; });
      const anios = Object.keys(porAnio).sort();
      const p = D.precio(t);
      cont.innerHTML = `<div class="rejilla g12">
        ${UI.panel('Resumen', `<table class="t"><tbody><tr><td class="i dim">Pagado en los últimos 12 meses</td><td>${F.precio(udm)}</td></tr>
          <tr><td class="i dim">Rendimiento sobre el precio actual</td><td>${F.pct(p ? udm / p : null)}</td></tr>
          ${divs.filter((d) => d[0] > hoy).map((d) => `<tr><td class="i dim">Anunciado · ex ${F.fecha(d[0])}</td><td class="acc">${F.precio(d[1])}</td></tr>`).join('')}</tbody></table>
          <div style="margin-top:10px">${N.barras(anios.map((a) => ({ p: a, v: porAnio[a] })), { w: 300, h: 80 })}</div><p class="dim" style="font-size:10.5px">Pago anual por acción · ${anios[0]}–${anios[anios.length - 1]}</p>`)}
        ${UI.panel('Historial', `<table class="t"><thead><tr><th class="i">Fecha ex</th><th>Monto por acción</th><th>Sobre el precio de hoy</th></tr></thead><tbody>${divs.slice(0, 40).map((d) => `<tr><td class="i">${F.fecha(d[0])}${d[0] > hoy ? ' <span class="chip acc">próximo</span>' : ''}</td><td>${F.num(d[1], 4)}</td><td>${F.pct(p ? d[1] / p : null)}</td></tr>`).join('')}</tbody></table>`, { p0: true, nota: esc(v.fuente || '') })}
      </div>`;
    });
  }

  App.registrar('eq', {
    titulo: (a) => a[0] || 'Emisora',
    pintar(cont, args) {
      const t = args[0];
      if (!D.U[t]) { cont.innerHTML = `<div class="aviso-barra">No encuentro la emisora «${esc(t)}». Escriba su clave en la línea de comandos.</div>`; return; }
      const p = (args[1] || 'resumen').toLowerCase();
      const pest = PESTANAS.find((x) => x[0] === p) ? p : 'resumen';
      cont.innerHTML = `${encabezado(t)}<nav class="pest">${PESTANAS.map(([k, n, c]) => `<button class="${k === pest ? 'on' : ''} ${k === 'kpis' ? 'nuevo' : ''}" data-ir="#/eq/${t}/${k}">${n}<b>${c}</b></button>`).join('')}</nav><div id="eqCuerpo"></div>`;
      const cuerpo = $('#eqCuerpo', cont);
      ({ resumen, grafica, financieros, kpis: (c, x) => N.KPIs.pintar(c, x), pares, noticias: (c, x) => N.Noticias.lista(c, D.noticiasDe(x, 200), { sinEmisora: true }), tesis, dividendos }[pest])(cuerpo, t);
    },
    refrescar(cont, args) {
      // Solo se actualiza el encabezado para no reiniciar gráficas ni pestañas.
      const h = $('.eq-h', cont); if (h && D.U[args[0]]) h.outerHTML = encabezado(args[0]);
    },
  });
})(window.NST);
