/* North Star Terminal · MODELO Y DRIVERS de la ficha, e historia de KPIs de la investigación
   1. Modelo de negocio y mezcla de segmentos (investigación 3T26 del equipo).
   2. Drivers de valor: estado actual y cuánto movería el precio un cambio en cada uno, con el
      puente de valuación a múltiplo constante (pipeline/sensibilidad.py, investigacion/drivers.json).
   3. Simulador de escenarios con los mismos coeficientes.
   4. Sensibilidad empírica: betas semanales contra el IPC y factores macro.
   5. Catalizadores, juicio y fuentes de la investigación. */
'use strict';
(function (N) {
  const { F, esc, $, $$, D, UI } = N;

  // ───────────── Markdown mínimo y seguro (negritas, cursivas, ligas como citas numeradas) ─────────────
  function md(texto, citas) {
    let s = esc(texto || '');
    s = s.replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g, (m, et, url) => {
      if (!citas) return `<a href="${url}" target="_blank" rel="noopener">${et}</a>`;
      citas.n += 1;
      let dom = ''; try { dom = new URL(url.replace(/&amp;/g, '&')).hostname.replace(/^www\./, ''); } catch (e) { dom = et; }
      return `<a class="cita" href="${url}" target="_blank" rel="noopener" title="${et} · ${esc(dom)}">${citas.n}</a>`;
    });
    s = s.replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>').replace(/(^|[\s(])\*([^*\s][^*]*?)\*(?=[\s).,;:]|$)/g, '$1<i>$2</i>');
    return s;
  }
  const nv = (s) => md(s).replace(/\bn\.v\.(?=\s|$|[;,)])/g, '<span class="nv" title="no verificado en la investigación">n.v.</span>');

  function tablaInv(tb, citas) {
    const titulo = tb.titulo ? `<div class="inv-tt">${esc(tb.titulo)}</div>` : '';
    return `${titulo}<div class="tabla-env"><table class="t inv-tabla"><thead><tr>${tb.cols.map((c, i) => `<th class="${i ? '' : 'i'}">${esc(c)}</th>`).join('')}</tr></thead>
      <tbody>${tb.filas.map((f) => `<tr>${f.map((c, i) => `<td class="${i ? '' : 'i'}">${nv(c)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>
      ${tb.nota ? `<p class="dim inv-nota">${md(tb.nota, citas)}</p>` : ''}`;
  }

  const ETQ = { modelo: 'Modelo de negocio y KPIs', narrativa: 'Narrativa', historicos: 'Catalizadores históricos', prospectivos: 'Prospectivos y riesgos',
    consenso: 'Consenso', fuentes: 'Fuentes', lectura: 'Lectura', calidad: 'Calidad de las fuentes', resultado: '3T26', kpis: 'KPIs', catalizadores: 'Catalizadores', datos: 'Datos', senal: 'Señal' };

  function piezaHTML(p, citas) {
    if (p.tipo === 'tabla') return tablaInv(p, citas);
    if (p.tipo === 'lista') {
      return `<ul class="lista inv-lista">${p.items.map((it) => `<li>${it.etiqueta ? `<b>${esc(it.etiqueta)}:</b> ` : ''}${md(it.md, citas)}
        ${(it.sub || []).length ? `<ul class="lista">${it.sub.map((x) => `<li>${md(x, citas)}</li>`).join('')}</ul>` : ''}</li>`).join('')}</ul>`;
    }
    const etq = p.etiqueta ? p.etiqueta.replace(/^\(([a-g](?:[–-][a-g])?)\)\s*/, '') : '';
    return `<p>${etq ? `<b class="acc">${esc(etq)}.</b> ` : ''}${md(p.md, citas)}</p>`;
  }

  // ───────────── glosario: qué mide cada KPI operativo y por qué importa en nuestro análisis ─────────────
  const GLOSARIO = [
    [/VMT|mismas tiendas|comparables/i, 'VMT · ventas mismas tiendas', 'Ventas de tiendas con más de un año abiertas.',
      'Separa el crecimiento orgánico del que viene de abrir tiendas. Es el primer dato que mueve el precio de un minorista el día del reporte y el que valida (o tumba) la tesis de consumo.'],
    [/tr[aá]fico\s*\/\s*ticket|^tr[aá]fico|ticket/i, 'Tráfico y ticket', 'La VMT descompuesta: clientes que entran (tráfico) y gasto promedio (ticket).',
      'Crecer por tráfico es de mejor calidad que por precio: indica ganancia de participación y no solo inflación.'],
    [/aperturas|tiendas OXXO|unidades|hogares pasados/i, 'Aperturas y red', 'Crecimiento de la red de puntos de venta.',
      'Crecimiento inorgánico: requiere capex y tarda en madurar, por eso aporta menos margen que la VMT.'],
    [/margen.*(EBITDA|UAFIDA)|EBITDA.*margen|UAFIDA.*margen/i, 'Margen UAFIDA', 'Cuánto de cada peso vendido se vuelve flujo operativo.',
      'Con el múltiplo constante, un punto base de margen mueve la UAFIDA en 1/margen puntos base: en empresas de margen bajo (autoservicio) el efecto se multiplica. Es parte de Quality en nuestro modelo QVM.'],
    [/margen bruto/i, 'Margen bruto', 'Ventas menos costo de lo vendido, sobre ventas.', 'Refleja precio, mezcla y costo de insumos (edulcorantes, PET, aluminio, celulosa); anticipa el margen UAFIDA.'],
    [/margen operativo|utilidad de operaci[oó]n/i, 'Margen y utilidad de operación', 'Utilidad después de gastos de operación.', 'Muestra si el crecimiento de ventas se convierte en utilidad (apalancamiento operativo).'],
    [/volumen|cajas unidad|cajas de 9/i, 'Volumen', 'Unidades vendidas (cajas, toneladas, litros).', 'Junto con el precio por unidad determina el ingreso; en bebidas lo mueven el IEPS, el clima y el consumo.'],
    [/edulcorantes|PET|insumos|celulosa|aluminio/i, 'Costo de insumos', 'Precio de las materias primas principales.', 'Es el principal costo variable: explica la mayor parte del cambio en el margen bruto.'],
    [/producci[oó]n de cobre|cobre.*\(t\)|cobre minad/i, 'Producción de cobre', 'Toneladas o libras producidas.', 'Volumen × (precio − cash cost) es la UAFIDA minera; la guía 2026 de GMéxico se recortó.'],
    [/precio.*cobre|cobre.*US\$/i, 'Precio del cobre', 'Precio promedio realizado por libra.', 'Es el driver dominante de Grupo México: la utilidad del 3T26 sube por precio, no por volumen.'],
    [/cash cost/i, 'Cash cost', 'Costo de producir una libra neto de subproductos.', 'Ser el productor de menor costo protege el margen cuando el precio baja.'],
    [/oro|plata|plomo|zinc/i, 'Producción y precio de metales', 'Onzas o toneladas producidas y precio realizado.', 'Para Peñoles, precio × volumen de oro y plata explica la UAFIDA; los precios tienen alta volatilidad.'],
    [/pasajeros|tr[aá]fico.*aeropuerto|Canc[uú]n/i, 'Pasajeros', 'Tráfico de pasajeros nacionales e internacionales.',
      'Con costos casi fijos, cada pasajero adicional llega casi completo a la UAFIDA; el internacional paga tarifas en dólares.'],
    [/no aero|comercial por pasajero|ingreso comercial/i, 'Ingresos no aeronáuticos', 'Comercios, estacionamientos, carga y servicios por pasajero.', 'Crecen sin depender de la tarifa regulada: son la palanca de margen de los aeropuertos.'],
    [/IFRIC/i, 'Margen ex-IFRIC 12', 'Margen sin los ingresos de construcción (IFRIC 12).', 'La construcción se registra con margen casi nulo y diluye el margen reportado; sin ella se ve la rentabilidad real de operar.'],
    [/TPDA/i, 'TPDA', 'Tráfico promedio diario de vehículos en las autopistas.', 'Volumen × tarifa indexada a la inflación: crecimiento orgánico con costos fijos.'],
    [/^ROE|ROE /i, 'ROE', 'Utilidad neta sobre capital.', 'Mide cuánto gana el banco por cada peso de los accionistas; es Quality en el modelo QVM y lo que justifica el múltiplo P/VL.'],
    [/MIN|margen financiero|margen de inter[eé]s/i, 'MIN · margen de interés neto', 'Ingreso por intereses neto sobre activos productivos.', 'Mide la sensibilidad a Banxico: un ciclo de recortes lo comprime, sobre todo en carteras a tasa variable.'],
    [/IMOR|morosidad/i, 'IMOR · índice de morosidad', 'Cartera vencida sobre cartera total.', 'Anticipa el costo de riesgo: la calidad del crecimiento en consumo.'],
    [/costo de riesgo/i, 'Costo de riesgo', 'Estimaciones preventivas sobre cartera promedio.', 'Cada punto base sale directo de la utilidad.'],
    [/eficiencia/i, 'Índice de eficiencia', 'Gastos sobre ingresos.', 'Menor es mejor: libera utilidad sin necesidad de crecer.'],
    [/cartera/i, 'Cartera de crédito', 'Saldo de préstamos.', 'El volumen compensa la presión de tasas; su mezcla (consumo vs empresarial) define el riesgo.'],
    [/captaci[oó]n|dep[oó]sitos/i, 'Captación', 'Depósitos de clientes.', 'Fondeo barato: protege el MIN.'],
    [/ICAP/i, 'ICAP', 'Índice de capitalización.', 'Holgura para crecer y pagar dividendos.'],
    [/ingresos por servicio|ARPU|pospago|prepago|servicios m[oó]viles|servicios fijos/i, 'Ingresos por servicio y ARPU', 'Ingreso recurrente por cliente.', 'En telecom la UAFIDA crece más rápido que los servicios (apalancamiento operativo).'],
    [/adiciones netas|suscriptores|RGU|banda ancha|video|l[ií]neas/i, 'Suscriptores y RGUs', 'Base de clientes y servicios contratados.', 'Volumen recurrente; con la red ya construida, el margen incremental es alto.'],
    [/capex/i, 'Capex', 'Inversión en activos fijos.', 'Menos capex con la misma UAFIDA = más flujo libre: la tesis de Megacable.'],
    [/deuda neta|apalancamiento/i, 'Deuda neta / UAFIDA', 'Años de UAFIDA para pagar la deuda.', 'Limita el margen de error y el pago de dividendos; es Quality (con signo negativo) en el modelo QVM.'],
    [/custodia|Indeval|AUC/i, 'Activos en custodia', 'Valor custodiado por Indeval.', 'Las cuotas se cobran sobre el valor: crecen con el mercado y con el dólar.'],
    [/siniestralidad|combinado|primas|unidades aseguradas/i, 'Siniestralidad y primas', 'Siniestros sobre primas devengadas.', 'Cada punto de siniestralidad mueve la utilidad técnica de forma desproporcionada.'],
    [/ABR|ocupaci[oó]n|renta|NOI|FFO/i, 'ABR, ocupación y renta', 'Superficie rentable, porcentaje ocupado y renta por m².', 'Definen el NOI y el FFO: el flujo que se reparte y con el que se valúa una inmobiliaria.'],
    [/ASM|factor de ocupaci[oó]n|TRASM|CASM/i, 'Capacidad y rentabilidad por asiento', 'Asientos-milla, ocupación e ingreso y costo por asiento-milla.', 'La diferencia TRASM − CASM es el margen de la aerolínea; la turbosina y los motores en tierra lo mueven.'],
    [/utilidad neta|UPA/i, 'Utilidad neta y UPA', 'Lo que queda para los accionistas.', 'Base del P/U; la sorpresa contra el consenso explica la reacción del precio el día del reporte.'],
    [/ingresos|ventas/i, 'Ingresos', 'Ventas del periodo.', 'Volumen × precio: el punto de partida de la UAFIDA.'],
  ];
  function glosarioDe(nombres) {
    const vistos = new Set(), out = [];
    for (const n of nombres) {
      const g = GLOSARIO.find(([re]) => re.test(n));
      if (g && !vistos.has(g[1])) { vistos.add(g[1]); out.push(g); }
    }
    return out;
  }

  // ───────────── formatos de los drivers ─────────────
  function mov(x, u) {
    if (!N.esNum(x)) return '—';
    const s = x > 0 ? '+' : x < 0 ? '−' : '';
    const a = Math.abs(x);
    if (u === 'pb') return `${s}${F.num(a, 0)} pb`;
    if (u === 'pp') return `${s}${F.num(a, a < 1 ? 1 : 0)} pp`;
    if (u === 'US$/lb') return `${s}US$${F.num(a, 2)}/lb`;
    return `${s}${F.num(a, a < 1 ? 1 : 0)}%`;
  }
  const pasoSlider = (u, r) => (u === 'pb' ? 5 : u === 'US$/lb' ? 0.05 : Math.abs((r || [0, 10])[1] - (r || [0, 10])[0]) > 20 ? 1 : 0.5);

  function baseTexto(b) {
    if (!b) return '';
    if (b.tipo === 'utilidad') {
      return `Base: utilidad de ${F.num(b.utilidad, 0)} mdp (${esc(b.utilidad_nota || '')}) con P/U constante${N.esNum(b.pe) ? ` (${F.veces(b.pe)})` : ''}. ${b.cartera ? `Cartera: ${F.num(b.cartera, 0)} mdp (${esc(b.cartera_nota || '')}). ` : ''}Impuestos supuestos: ${F.pct(D.sensMeta.impuestos || 0.3, 0)}.`;
    }
    return `Base: UAFIDA con VE/UAFIDA constante${N.esNum(b.ve_uafida) ? ` (${F.veces(b.ve_uafida)})` : ''}; margen UAFIDA ${F.pct(b.margen_uafida, 1)}${N.esNum(b.margen_bruto) ? `, margen bruto ${F.pct(b.margen_bruto, 1)}` : ''}. Cada 1% de UAFIDA mueve el precio ${F.num(b.L, 2)}% (VE/capital: ${esc(b.L_nota || '')}).`;
  }

  // ───────────── la pestaña ─────────────
  function pintar(cont, t) {
    const inv = D.inv(t), s = D.sensDe(t) || {}, mod = s.modelo, mk = s.mercado;
    const precio = D.precio(t) || (mod && mod.base && mod.base.precio);
    if (t === 'MEXTRAC') {
      const doc = (D.investigacion || [])[0];
      cont.innerHTML = UI.panel('El benchmark', doc && doc.contexto ? `<div class="texto inv">${doc.contexto.map((p) => piezaHTML(p, { n: 0 })).join('')}</div>` : '<div class="vacio">Sin contexto del índice en la investigación.</div>');
      return;
    }
    const citas = { n: 0 };
    const r = (inv && inv.resumen) || {};
    const modeloTxt = inv && inv.modelo ? md(inv.modelo, citas) : esc(D.ficha(t).descripcion || D.info(t).longBusinessSummary || '');
    const lectura = inv ? (inv.piezas || []).filter((p) => ['lectura', 'narrativa', 'resultado'].includes(p.clave)) : [];
    const chips = [r.sector && `<span class="chip">${esc(r.sector)}</span>`, (inv && inv.nivel) && `<span class="chip acc">Nivel ${inv.nivel}</span>`,
      r.tendencia && `<span class="chip ${/mejora/i.test(r.tendencia) ? 'pos' : /deterioro/i.test(r.tendencia) ? 'neg' : ''}">Tendencia: ${esc(r.tendencia)}</span>`].filter(Boolean).join('');
    const panelModelo = UI.panel('Modelo de negocio', `<div class="texto inv">
        ${chips ? `<div class="chips" style="margin-bottom:8px">${chips}</div>` : ''}
        ${modeloTxt ? `<p>${modeloTxt}</p>` : '<p class="dim">Sin descripción.</p>'}
        ${mod && mod.segmentos ? `<p><b class="acc">Mezcla.</b> ${md(mod.segmentos)}</p>` : ''}
        ${r.kpis ? `<p><b class="acc">KPIs que vigilamos.</b> ${esc(r.kpis)}</p>` : ''}
        ${r.catalizador ? `<p><b class="acc">Catalizador de corto plazo.</b> ${md(r.catalizador)}</p>` : ''}
      </div>`, { nota: inv ? `investigación al ${esc(inv.doc.corte || '')}` : 'ficha del equipo' });

    // Drivers
    let panelDrivers = '', panelSim = '';
    const ds = (mod && mod.drivers) || [];
    if (ds.length) {
      const base = mod.base || {};
      const filas = ds.map((d, i) => {
        const eb = N.esNum(d.e_base) ? d.e_base * d.paso : null, ep = d.efecto_paso;
        return `<tr><td class="i drv"><b>${esc(d.n)}</b><div class="solo-cel">${mov(d.paso, d.unidad)} ⇒ precio <b class="${F.cls(ep)}">${N.esNum(ep) ? F.pctS(ep, 1) : 'n/a'}</b></div>${d.porque ? `<div class="dim">${esc(d.porque)}</div>` : ''}</td>
          <td class="i drv-act">${d.actual ? md(d.actual) : '<span class="dim">—</span>'}</td>
          <td>${mov(d.paso, d.unidad)}</td>
          <td class="${F.cls(eb)}">${N.esNum(eb) ? F.pctS(eb, 1) : '—'}</td>
          <td><b class="${F.cls(ep)}">${N.esNum(ep) ? F.pctS(ep, 1) : 'n/a'}</b></td>
          <td>${N.esNum(ep) && N.esNum(precio) ? F.precio(precio * (1 + ep)) : '—'}</td>
          <td><button class="btn sm" type="button" data-fx="${i}" aria-label="Ver fórmula">ƒ</button></td></tr>
          <tr class="fx-fila" data-fxf="${i}" hidden><td colspan="7" class="i fx">${esc(d.formula || '')}${d.margen_incremental_nota ? ` · margen incremental: ${esc(d.margen_incremental_nota)}` : ''}${d.volumen_nota ? ` · volumen: ${esc(d.volumen_nota)}` : ''}${d.fuga_nota ? ` · ${esc(d.fuga_nota)}` : ''}${d.peso_nota ? ` · peso: ${esc(d.peso_nota)}` : ''}${d.spread_nota ? ` · ${esc(d.spread_nota)}` : ''}</td></tr>`;
      }).join('');
      panelDrivers = UI.panel('Drivers de valor: cuánto mueve el precio cada KPI', `
        ${mod.nota ? `<div class="aviso-barra">${esc(mod.nota)}</div>` : ''}
        <div class="tabla-env"><table class="t drivers"><thead><tr><th class="i">Driver</th><th class="i">Estado actual</th><th>Movimiento</th>
          <th title="${base.tipo === 'utilidad' ? 'cambio en la utilidad' : 'cambio en la UAFIDA'}">${base.tipo === 'utilidad' ? 'Utilidad' : 'UAFIDA'}</th><th>Precio</th><th>Precio implícito</th><th></th></tr></thead>
          <tbody>${filas}</tbody></table></div>
        <p class="dim inv-nota">${baseTexto(base)} Precio actual ${F.precio(precio)}. Supuestos editables en <b>investigacion/drivers.json</b>.</p>`,
      { p0: true, nota: mod.configurado ? 'drivers del equipo · investigación 3T26' : 'marco sectorial (sin drivers propios todavía)' });
      panelSim = UI.panel('Simulador de escenarios', `<div class="sim" id="sim">
          ${ds.map((d, i) => { const rg = d.rango || [-(d.paso * 3), d.paso * 3]; return `<label class="sim-f"><span class="sim-n">${esc(d.n)}</span>
            <input type="range" min="${rg[0]}" max="${rg[1]}" step="${pasoSlider(d.unidad, rg)}" value="0" data-sim="${i}" ${N.esNum(d.e_precio) ? '' : 'disabled'} aria-label="${esc(d.n)}">
            <output data-simv="${i}">0</output></label>`; }).join('')}
          <div class="sim-res" id="simRes"></div>
          <div class="chips" style="margin-top:6px"><button class="btn sm" type="button" id="simCero">Reiniciar</button></div>
        </div>`, { nota: 'lineal · múltiplo constante' });
    }

    // Sensibilidad de mercado
    let panelMk = '';
    if (mk && mk.ipc) {
      const fs = (mk.factores || []).filter((f) => f.relevante || Math.abs(f.t || 0) >= 2).slice(0, 8);
      const resto = (mk.factores || []).filter((f) => !fs.includes(f));
      const fila = (f) => `<tr><td class="i">${esc(f.n)}${f.relevante ? ' <span class="chip acc">clave</span>' : ''}</td>
        <td class="${F.cls(f.beta)}">${F.num(f.beta, 2)}</td><td class="${Math.abs(f.t || 0) >= 2 ? '' : 'dim'}">${F.num(f.t, 1)}</td>
        <td class="dim">${F.num(f.beta_simple, 2)}</td>
        <td>${N.esNum(f.efecto_1sd) ? `±${F.num(Math.abs(f.efecto_1sd) * 100, 1)}%` : '—'}</td></tr>`;
      panelMk = UI.panel('Sensibilidad de mercado (empírica)', `
        <table class="t kv"><tbody><tr><td class="i dim">Beta contra el IPC</td><td><b>${F.num(mk.ipc.beta, 2)}</b> <span class="dim">(t ${F.num(mk.ipc.t, 1)} · R² ${F.pct(mk.ipc.r2, 0)})</span></td></tr></tbody></table>
        <div class="tabla-env"><table class="t"><thead><tr><th class="i">Factor</th><th title="por cada 1% del factor (o 1 pp en tasas), descontando el IPC">β neta</th><th>t</th><th title="beta sin descontar el IPC">β simple</th><th title="efecto de una semana típica del factor (1 desviación estándar)">1σ sem.</th></tr></thead>
          <tbody>${fs.map(fila).join('') || '<tr><td colspan="5" class="i dim">Ningún factor es significativo.</td></tr>'}</tbody></table></div>
        ${resto.length ? `<p class="dim inv-nota">Sin efecto significativo: ${resto.map((f) => esc(f.n)).join(', ')}.</p>` : ''}
        <p class="dim inv-nota">Regresión de ${mk.semanas} rendimientos semanales: acción = α + β·IPC + β·factor. La beta neta dice cuánto se mueve la acción por cada 1% del factor (en tasas, por cada punto porcentual) ya descontado el mercado. |t| ≥ 2 = significativa. El mercado suele reaccionar menos que el modelo fundamental porque descuenta que los precios de las materias primas y las tasas regresan a su promedio.</p>`,
      { p0: true, nota: `${mk.semanas} semanas` });
    }

    // Catalizadores y juicio
    let panelCat = '';
    if (inv) {
      const pz = (k) => (inv.piezas || []).filter((p) => p.clave === k || (p.tipo === 'lista' && k === 'prospectivos' && (inv.piezas[inv.piezas.indexOf(p) - 1] || {}).clave === 'prospectivos'));
      const hist = pz('historicos'), pros = pz('prospectivos'), cons = pz('consenso');
      const macro = inv.macro || [];
      panelCat = UI.panel('Catalizadores', `<div class="texto inv">
        ${hist.map((p) => piezaHTML(p, citas)).join('')}${pros.map((p) => piezaHTML(p, citas)).join('')}
        ${macro.length ? `<div class="inv-tt">Catalizadores macro que la tocan</div><table class="t kv"><tbody>${macro.map((m) => `<tr><td class="i"><b>${esc(m.catalizador)}</b></td><td class="i">${md(m.afectadas, citas)}</td></tr>`).join('')}</tbody></table>` : ''}
        ${cons.map((p) => piezaHTML(p, citas)).join('')}
        ${!hist.length && !pros.length && inv.compacto ? Object.entries(inv.compacto).map(([k, v]) => `<p><b class="acc">${esc(k)}.</b> ${nv(v)}</p>`).join('') : ''}
      </div>`);
    }
    const panelJuicio = inv && (inv.juicio || (inv.recomendaciones || []).length) ? UI.panel('Juicio de la investigación', `<div class="texto inv">
        ${inv.juicio ? `<p>${md(inv.juicio, citas)}</p>` : ''}
        ${(inv.recomendaciones || []).length ? `<div class="inv-tt">Recomendaciones del documento que la mencionan</div><ul class="lista">${inv.recomendaciones.map((x) => `<li>${md(x, citas)}</li>`).join('')}</ul>` : ''}
      </div>`, { clase: 'juicio' }) : '';
    const panelLectura = lectura.length ? UI.panel('Lectura del trimestre', `<div class="texto inv">${lectura.map((p) => piezaHTML(p, citas)).join('')}</div>`) : '';
    const fuentes = inv ? (inv.piezas || []).filter((p) => p.clave === 'fuentes' || p.clave === 'calidad') : [];
    const panelFuentes = inv ? UI.panel('Fuentes', `<div class="texto inv">${fuentes.map((p) => piezaHTML(p, citas)).join('')}
        <p class="dim">Documento: <a href="https://github.com/${esc(D.repo)}/blob/main/${esc(inv.doc.archivo)}" target="_blank" rel="noopener">${esc(inv.doc.archivo)}</a> · corte ${esc(inv.doc.corte || '')}.
        Las cifras marcadas <span class="nv">n.v.</span> no se verificaron en fuente primaria. Los números en superíndice son las ligas a cada fuente.</p></div>`) : '';

    cont.innerHTML = `<div class="rejilla g21">
      <div class="rejilla" style="align-content:start">${panelModelo}${panelDrivers}${panelLectura}${panelCat}</div>
      <div class="rejilla" style="align-content:start">${panelSim}${panelMk}${panelJuicio}${panelFuentes}</div></div>
      ${!inv && !ds.length ? '<div class="vacio">Sin investigación ni drivers para esta emisora todavía.</div>' : ''}`;

    $$('[data-fx]', cont).forEach((b) => b.addEventListener('click', () => { const f = $(`[data-fxf="${b.dataset.fx}"]`, cont); f.hidden = !f.hidden; }));
    const sim = $('#sim', cont);
    if (sim) {
      const calc = () => {
        let db = 0, dp = 0;
        $$('[data-sim]', sim).forEach((inp) => {
          const d = ds[+inp.dataset.sim], x = +inp.value;
          $(`[data-simv="${inp.dataset.sim}"]`, sim).textContent = mov(x, d.unidad);
          if (N.esNum(d.e_base)) db += d.e_base * x;
          if (N.esNum(d.e_precio)) dp += d.e_precio * x;
        });
        const b = (mod && mod.base) || {};
        $('#simRes', sim).innerHTML = `<div class="sim-tot"><span class="dim">${b.tipo === 'utilidad' ? 'Utilidad' : 'UAFIDA'}</span><b class="${F.cls(db)}">${F.pctS(db, 1)}</b></div>
          <div class="sim-tot"><span class="dim">Precio</span><b class="${F.cls(dp)}">${F.pctS(dp, 1)}</b></div>
          <div class="sim-tot"><span class="dim">Precio implícito</span><b>${N.esNum(precio) ? F.precio(precio * (1 + dp)) : '—'}</b><span class="dim">vs ${F.precio(precio)}</span></div>`;
      };
      $$('[data-sim]', sim).forEach((inp) => inp.addEventListener('input', calc));
      $('#simCero', sim).addEventListener('click', () => { $$('[data-sim]', sim).forEach((inp) => { inp.value = 0; }); calc(); });
      calc();
    }
  }

  // ───────────── para la pestaña de KPIs: historia y por qué importan ─────────────
  function historia(t) {
    const inv = D.inv(t), kp = D.kp(t), s = D.sensDe(t) || {}, mod = s.modelo;
    const citas = { n: 0 };
    const tablas = (inv && inv.tablas) || [];
    // Serie trimestral de los KPIs financieros que calcula el pipeline
    const conSerie = ((kp && kp.kpis) || []).map((x) => Object.assign({}, D.def(x.clave), x)).filter((k) => (k.serie || []).filter((p) => N.esNum(p.v)).length >= 3);
    const periodos = [...new Set(conSerie.flatMap((k) => k.serie.filter((p) => N.esNum(p.v)).map((p) => p.p)))];
    const ordenP = (p) => { const m = /^(\d)T(\d\d)$/.exec(p); return m ? +m[2] * 10 + +m[1] : 0; };
    periodos.sort((a, b) => ordenP(a) - ordenP(b));
    const QVM = { roe: 'Quality · 40% del modelo', margen_neto: 'Quality · 40% del modelo', deuda_neta_uafida: 'Quality (resta)', pe: 'Value · 10% (como rendimiento de utilidades)', p_vl: 'Value · 10%', rend_dividendo: 'Value · 10%' };
    const fmtSerie = (k, v) => (k.serie_nombre ? F.dinero(v, (kp && kp.moneda_reporte) || 'MXN') : F.kpi(v, k.unidad));
    const histFin = conSerie.length ? `<div class="tabla-env"><table class="t"><thead><tr><th class="i">KPI</th>${periodos.map((p) => `<th>${esc(p)}</th>`).join('')}<th class="i">En nuestro análisis</th></tr></thead><tbody>
      ${conSerie.map((k) => { const m = Object.fromEntries(k.serie.map((p) => [p.p, p.v])); return `<tr><td class="i">${esc(k.serie_nombre || k.nombre)}</td>${periodos.map((p) => `<td>${N.esNum(m[p]) ? fmtSerie(k, m[p]) : '<span class="dim">—</span>'}</td>`).join('')}
        <td class="i dim nota-larga">${esc(QVM[k.clave] || (k.familia === 'margenes' ? 'Quality: calidad de la utilidad' : k.familia === 'crecimiento' ? 'Tesis: que el crecimiento sea orgánico' : k.familia === 'valuacion' ? 'Value' : ''))}</td></tr>`; }).join('')}
      </tbody></table></div>` : '';
    // Por qué importan: drivers cuantificados + glosario de los KPIs de la investigación
    const nombres = [...tablas.flatMap((tb) => tb.filas.map((f) => f[0])), ...String((inv && inv.resumen && inv.resumen.kpis) || '').split(',')];
    const glos = glosarioDe(nombres);
    const ds = (mod && mod.drivers) || [];
    const porque = `${ds.length ? `<div class="inv-tt">Cuánto pesan en el precio (puente de valuación)</div><ul class="lista">${ds.map((d) => `<li><b>${esc(d.n)}</b>: ${mov(d.paso, d.unidad)} ⇒ precio <b class="${F.cls(d.efecto_paso)}">${N.esNum(d.efecto_paso) ? F.pctS(d.efecto_paso, 1) : 'n/a'}</b> a múltiplo constante. <span class="dim">${esc(d.porque || '')}</span></li>`).join('')}</ul>` : ''}
      ${glos.length ? `<div class="inv-tt">Qué mide cada uno y por qué lo seguimos</div><table class="t kv glosario"><tbody>${glos.map(([, n, que, pq]) => `<tr><td class="i"><b>${esc(n)}</b><div class="dim">${esc(que)}</div></td><td class="i">${esc(pq)}</td></tr>`).join('')}</tbody></table>` : ''}
      ${inv && inv.modelo ? `<p class="inv-nota"><b class="acc">Según la investigación:</b> ${md(inv.modelo, citas)}</p>` : ''}`;
    if (!tablas.length && !histFin && !ds.length && !glos.length) return '';
    return `<div class="kpi-sec"><h3>Historia de KPIs <span class="nota">${inv ? `investigación 3T26 del equipo (corte ${esc(inv.doc.corte || '')}) y estados financieros trimestrales` : 'estados financieros trimestrales'}</span></h3>
      <div class="rejilla g21">
        <div class="rejilla" style="align-content:start">
          ${tablas.length ? UI.panel('KPIs operativos 2022 → 3T26', tablas.map((tb) => tablaInv(tb, citas)).join('') + `<p class="dim inv-nota"><span class="nv">n.v.</span> = no verificado en fuente primaria durante la investigación (no se rellenó con estimaciones). <a data-ir="#/eq/${t}/modelo">Ver modelo, drivers y catalizadores ›</a></p>`, { p0: true }) : ''}
          ${!tablas.length && inv && inv.compacto ? UI.panel('Marco de KPIs de la investigación', `<table class="t kv"><tbody>${Object.entries(inv.compacto).map(([k, v]) => `<tr><td class="i dim">${esc(k)}</td><td class="i">${nv(v)}</td></tr>`).join('')}</tbody></table>`, { p0: true, nota: `Nivel ${inv.nivel || '—'}: marco de KPIs, sin datos verificados` }) : ''}
          ${UI.panel('Historia anual de KPIs financieros', '<div id="histAnual"><div class="cargando">Cargando estados anuales</div></div>', { p0: true, nota: 'estados financieros anuales · completa los años que la investigación marca n.v.' })}
          ${histFin ? UI.panel('Historia trimestral de KPIs financieros', histFin, { p0: true, nota: 'calculados de los estados financieros' }) : ''}
        </div>
        ${UI.panel('Por qué son relevantes en nuestro análisis', `<div class="texto inv">${porque}</div>`)}
      </div></div>`;
  }

  // Historia anual (2021–2025) con los estados financieros que publica el pipeline por emisora.
  function llenarHistoria(cont, t) {
    const el = $('#histAnual', cont); if (!el) return;
    D.estados(t).then((est) => {
      if (!el.isConnected) return;
      const r = est && est.resultados && est.resultados.anual, b = est && est.balance && est.balance.anual;
      if (!r || !r.periodos || r.periodos.length < 2) { el.innerHTML = '<div class="vacio">Sin estados anuales para esta emisora.</div>'; return; }
      const per = r.periodos, anios = per.map((p) => p.slice(0, 4)), mon = est.moneda || 'MXN';
      const fila = (hoja, ...claves) => { for (const k of claves) { const xs = hoja && hoja.filas && hoja.filas[k]; if (xs && xs.some(N.esNum)) return xs; } return per.map(() => null); };
      const alinear = (hoja, xs) => per.map((p) => { const i = hoja && hoja.periodos ? hoja.periodos.indexOf(p) : -1; return i >= 0 ? xs[i] : null; });
      const ing = fila(r, 'TotalRevenue', 'OperatingRevenue'), ua = fila(r, 'EBITDA', 'NormalizedEBITDA'), neta = fila(r, 'NetIncomeCommonStockholders', 'NetIncome');
      const mf = fila(r, 'NetInterestIncome');
      const cap = alinear(b, fila(b, 'StockholdersEquity', 'CommonStockEquity')), deuda = alinear(b, fila(b, 'TotalDebt'));
      const caja = alinear(b, fila(b, 'CashCashEquivalentsAndShortTermInvestments', 'CashAndCashEquivalents'));
      const div0 = (a, c) => (N.esNum(a) && N.esNum(c) && c !== 0 ? a / c : null);
      const banco = ['bancos', 'microfinanzas', 'seguros'].includes((D.U[t] || {}).grupo);
      const filas = [
        ['Ingresos', ing, 'dinero'], ['Crecimiento de ingresos', ing.map((x, i) => (i ? div0(x - ing[i - 1], Math.abs(ing[i - 1] || 0)) : null)), 'pct'],
        ...(banco ? [['Margen financiero', mf, 'dinero']] : [['UAFIDA', ua, 'dinero'], ['Margen UAFIDA', ua.map((x, i) => div0(x, ing[i])), 'pct']]),
        ['Utilidad neta mayoritaria', neta, 'dinero'], ['Margen neto', neta.map((x, i) => div0(x, ing[i])), 'pct'],
        ['ROE', neta.map((x, i) => (i && N.esNum(cap[i]) && N.esNum(cap[i - 1]) ? div0(x, (cap[i] + cap[i - 1]) / 2) : div0(x, cap[i]))), 'pct'],
        ...(banco ? [] : [['Deuda neta / UAFIDA', ua.map((x, i) => (N.esNum(deuda[i]) && N.esNum(x) && x > 0 ? (deuda[i] - (caja[i] || 0)) / x : null)), 'x']]),
      ];
      const i22 = anios.indexOf('2022'), i25 = anios.indexOf('2025');
      const cagr = (xs) => (i22 >= 0 && i25 > i22 && xs[i22] > 0 && xs[i25] > 0 ? (xs[i25] / xs[i22]) ** (1 / (i25 - i22)) - 1 : null);
      const fmt = (v, u) => (!N.esNum(v) ? '<span class="dim">—</span>' : u === 'dinero' ? F.dinero(v, mon) : u === 'pct' ? `<span class="${v < 0 ? 'neg' : ''}">${F.pct(v, 1)}</span>` : F.veces(v, 2));
      el.innerHTML = `<div class="tabla-env"><table class="t"><thead><tr><th class="i">${esc(mon)}</th>${anios.map((a) => `<th>${a}</th>`).join('')}<th title="crecimiento anual compuesto 2022–2025">CAGR 22–25</th><th>Tendencia</th></tr></thead><tbody>
        ${filas.map(([n, xs, u]) => `<tr><td class="i">${n}</td>${xs.map((v) => `<td>${fmt(v, u)}</td>`).join('')}<td>${u === 'dinero' ? fmt(cagr(xs), 'pct') : ''}</td>
          <td>${N.barras(xs.map((v, i) => ({ p: anios[i], v })), { w: 70, h: 18, unidad: u === 'pct' ? '%' : u === 'x' ? 'x' : 'dinero' })}</td></tr>`).join('')}
        </tbody></table></div>`;
    });
  }

  N.Modelo = { pintar, historia, llenarHistoria, md };
})(window.NST);
