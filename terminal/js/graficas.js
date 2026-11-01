/* North Star Terminal · gráficas
   Envoltura de TradingView Lightweight Charts (velas, volumen, líneas) más indicadores
   técnicos calculados aquí mismo: promedios móviles, Bollinger, RSI y MACD. */
'use strict';
(function (N) {
  const { F, esNum } = N;
  const LW = () => window.LightweightCharts;

  const I = {
    sma(xs, n) { const o = []; let s = 0; for (let i = 0; i < xs.length; i++) { s += xs[i]; if (i >= n) s -= xs[i - n]; o.push(i >= n - 1 ? s / n : null); } return o; },
    ema(xs, n) { const k = 2 / (n + 1), o = []; let e = null; xs.forEach((x, i) => { e = e === null ? x : x * k + e * (1 - k); o.push(i >= n - 1 ? e : null); }); return o; },
    bollinger(xs, n = 20, k = 2) {
      const m = I.sma(xs, n), sup = [], inf = [];
      xs.forEach((_, i) => {
        if (m[i] === null) { sup.push(null); inf.push(null); return; }
        let s = 0; for (let j = i - n + 1; j <= i; j++) s += (xs[j] - m[i]) ** 2;
        const d = Math.sqrt(s / n); sup.push(m[i] + k * d); inf.push(m[i] - k * d);
      });
      return { m, sup, inf };
    },
    rsi(xs, n = 14) {
      const o = new Array(xs.length).fill(null); if (xs.length <= n) return o;
      let g = 0, p = 0;
      for (let i = 1; i <= n; i++) { const d = xs[i] - xs[i - 1]; g += Math.max(d, 0); p += Math.max(-d, 0); }
      g /= n; p /= n; o[n] = p === 0 ? 100 : 100 - 100 / (1 + g / p);
      for (let i = n + 1; i < xs.length; i++) {
        const d = xs[i] - xs[i - 1]; g = (g * (n - 1) + Math.max(d, 0)) / n; p = (p * (n - 1) + Math.max(-d, 0)) / n;
        o[i] = p === 0 ? 100 : 100 - 100 / (1 + g / p);
      }
      return o;
    },
    macd(xs, a = 12, b = 26, c = 9) {
      const ea = I.ema(xs, a), eb = I.ema(xs, b);
      const m = xs.map((_, i) => (ea[i] !== null && eb[i] !== null ? ea[i] - eb[i] : null));
      const ini = m.findIndex((x) => x !== null);
      const sen = new Array(xs.length).fill(null);
      if (ini >= 0) { const e = I.ema(m.slice(ini), c); e.forEach((x, i) => { sen[ini + i] = x; }); }
      return { m, sen, hist: m.map((x, i) => (x !== null && sen[i] !== null ? x - sen[i] : null)) };
    },
  };

  function colores() {
    const cs = getComputedStyle(document.documentElement);
    const v = (k) => cs.getPropertyValue(k).trim();
    return { fondo: v('--panel'), txt: v('--txt-2'), linea: v('--line'), linea2: v('--line-2'), acc: v('--acc'),
      pos: v('--pos'), neg: v('--neg'), info: v('--info'), warn: v('--warn'), txt3: v('--txt-3') };
  }

  const activas = new Set();

  function crear(el, extra = {}) {
    if (!LW()) { el.innerHTML = '<div class="vacio">No cargó la librería de gráficas (sin conexión a jsDelivr).</div>'; return null; }
    const c = colores();
    const ch = LW().createChart(el, Object.assign({
      autoSize: true,
      layout: { background: { type: 'solid', color: c.fondo }, textColor: c.txt, fontFamily: 'JetBrains Mono, monospace', fontSize: 10.5 },
      grid: { vertLines: { color: c.linea }, horzLines: { color: c.linea } },
      rightPriceScale: { borderColor: c.linea2 },
      timeScale: { borderColor: c.linea2, rightOffset: 3, minBarSpacing: 0.3 },
      crosshair: { mode: LW().CrosshairMode.Normal },
      localization: { locale: 'es-MX', priceFormatter: (p) => F.num(p, Math.abs(p) < 10 ? 3 : 2) },
    }, extra));
    activas.add(ch);
    return ch;
  }

  function limpiar() { activas.forEach((ch) => { try { ch.remove(); } catch (e) { /* ya no existe */ } }); activas.clear(); }

  const serie = (fechas, xs) => fechas.map((f, i) => (esNum(xs[i]) ? { time: f, value: xs[i] } : null)).filter(Boolean);

  /** Velas con volumen e indicadores. Devuelve un control para cambiar rango e indicadores. */
  function velas(el, v, { bajo = null, ipc = null } = {}) {
    const ch = crear(el); if (!ch) return null;
    const c = colores();
    const d = v.d, cierre = v.c;
    const sv = ch.addCandlestickSeries({ upColor: c.pos, downColor: c.neg, borderVisible: false, wickUpColor: c.pos, wickDownColor: c.neg });
    sv.setData(d.map((f, i) => ({ time: f, open: v.o[i], high: v.h[i], low: v.l[i], close: cierre[i] })));
    const hayVol = (v.v || []).some((x) => x > 0);
    let vol = null;
    if (hayVol) {
      vol = ch.addHistogramSeries({ priceFormat: { type: 'volume' }, priceScaleId: 'vol', lastValueVisible: false, priceLineVisible: false });
      ch.priceScale('vol').applyOptions({ scaleMargins: { top: 0.82, bottom: 0 } });
      vol.setData(d.map((f, i) => ({ time: f, value: v.v[i] || 0, color: cierre[i] >= (v.o[i] || cierre[i]) ? 'rgba(31,214,122,.35)' : 'rgba(255,77,94,.35)' })));
    }
    sv.priceScale().applyOptions({ scaleMargins: { top: 0.06, bottom: hayVol ? 0.2 : 0.06 } });
    const capas = {};
    const definiciones = {
      sma20: () => [ch.addLineSeries({ color: c.info, lineWidth: 1, priceLineVisible: false, lastValueVisible: false })].map((s) => (s.setData(serie(d, I.sma(cierre, 20))), s)),
      sma50: () => [ch.addLineSeries({ color: c.acc, lineWidth: 1, priceLineVisible: false, lastValueVisible: false })].map((s) => (s.setData(serie(d, I.sma(cierre, 50))), s)),
      sma200: () => [ch.addLineSeries({ color: '#c77dff', lineWidth: 1, priceLineVisible: false, lastValueVisible: false })].map((s) => (s.setData(serie(d, I.sma(cierre, 200))), s)),
      ema21: () => [ch.addLineSeries({ color: c.warn, lineWidth: 1, lineStyle: 2, priceLineVisible: false, lastValueVisible: false })].map((s) => (s.setData(serie(d, I.ema(cierre, 21))), s)),
      bb: () => {
        const b = I.bollinger(cierre);
        return [b.sup, b.m, b.inf].map((xs, i) => {
          const s = ch.addLineSeries({ color: i === 1 ? c.txt3 : 'rgba(60,200,255,.55)', lineWidth: 1, lineStyle: i === 1 ? 2 : 0, priceLineVisible: false, lastValueVisible: false });
          s.setData(serie(d, xs)); return s;
        });
      },
      ipc: () => {
        if (!ipc) return [];
        const m = new Map(ipc.d.map((f, i) => [f, ipc.c[i]]));
        const ini = d.find((f) => m.has(f)); if (!ini) return [];
        const base = m.get(ini), b0 = cierre[d.indexOf(ini)];
        const s = ch.addLineSeries({ color: '#9aa3ad', lineWidth: 1, priceLineVisible: false, lastValueVisible: false, title: 'IPC' });
        s.setData(d.filter((f) => m.has(f)).map((f) => ({ time: f, value: (m.get(f) / base) * b0 })));
        return [s];
      },
    };
    function alternar(clave, on) {
      if (on && !capas[clave]) capas[clave] = definiciones[clave]();
      if (!on && capas[clave]) { capas[clave].forEach((s) => ch.removeSeries(s)); delete capas[clave]; }
    }
    // Panel inferior (RSI o MACD) en una segunda gráfica sincronizada.
    let inf = null, modoInf = null;
    function inferior(modo) {
      if (!bajo) return;
      if (inf) { activas.delete(inf); inf.remove(); inf = null; }
      modoInf = modo; bajo.hidden = !modo;
      if (!modo) return;
      inf = crear(bajo, { timeScale: { visible: false, borderColor: c.linea2 } });
      if (modo === 'rsi') {
        const s = inf.addLineSeries({ color: c.acc, lineWidth: 1, priceLineVisible: false });
        s.setData(serie(d, I.rsi(cierre)));
        s.createPriceLine({ price: 70, color: c.neg, lineWidth: 1, lineStyle: 2, axisLabelVisible: true, title: '' });
        s.createPriceLine({ price: 30, color: c.pos, lineWidth: 1, lineStyle: 2, axisLabelVisible: true, title: '' });
      } else {
        const m = I.macd(cierre);
        const h = inf.addHistogramSeries({ priceLineVisible: false, lastValueVisible: false });
        h.setData(d.map((f, i) => (m.hist[i] === null ? null : { time: f, value: m.hist[i], color: m.hist[i] >= 0 ? 'rgba(31,214,122,.6)' : 'rgba(255,77,94,.6)' })).filter(Boolean));
        const a = inf.addLineSeries({ color: c.info, lineWidth: 1, priceLineVisible: false, lastValueVisible: false });
        a.setData(serie(d, m.m));
        const b = inf.addLineSeries({ color: c.acc, lineWidth: 1, priceLineVisible: false, lastValueVisible: false });
        b.setData(serie(d, m.sen));
      }
      const r = ch.timeScale().getVisibleLogicalRange(); if (r) inf.timeScale().setVisibleLogicalRange(r);
    }
    ch.timeScale().subscribeVisibleLogicalRangeChange((r) => { if (inf && r) inf.timeScale().setVisibleLogicalRange(r); });
    function rango(dias) {
      if (!dias) { ch.timeScale().fitContent(); return; }
      const fin = d[d.length - 1];
      const ini = new Date(fin + 'T12:00:00'); ini.setDate(ini.getDate() - dias);
      const desde = d.find((f) => f >= ini.toISOString().slice(0, 10)) || d[0];
      ch.timeScale().setVisibleRange({ from: desde, to: fin });
    }
    return { ch, alternar, inferior, rango, sv, get modoInf() { return modoInf; } };
  }

  /** Varias líneas sobre un mismo eje (comparativos, portafolio contra benchmark, macro). */
  function lineas(el, series, { porcentaje = false, area = false } = {}) {
    const ch = crear(el, porcentaje ? { localization: { locale: 'es-MX', priceFormatter: (p) => F.num(p, 1) + (porcentaje === 'pct' ? '%' : '') } } : {});
    if (!ch) return null;
    const c = colores();
    const paleta = [c.acc, c.info, '#c77dff', c.pos, '#ff7aa2', c.warn, '#7ee0c3', '#b0b0b0'];
    const out = series.map((s, i) => {
      const color = s.color || paleta[i % paleta.length];
      const x = area && i === 0
        ? ch.addAreaSeries({ lineColor: color, topColor: color + '40', bottomColor: color + '05', lineWidth: 2, priceLineVisible: false, title: s.titulo || '' })
        : ch.addLineSeries({ color, lineWidth: s.grosor || (i === 0 ? 2 : 1), lineStyle: s.punteada ? 2 : 0, priceLineVisible: false, title: s.titulo || '' });
      x.setData(s.datos);
      return x;
    });
    ch.timeScale().fitContent();
    return { ch, series: out };
  }

  N.I = I;
  N.G = { crear, velas, lineas, limpiar, colores };
})(window.NST);
