/* North Star Terminal · núcleo
   Espacio de nombres global NST, formatos es-MX, utilidades de DOM, almacenamiento
   local seguro y mini gráficas SVG. Sin dependencias. */
'use strict';
window.NST = window.NST || {};
(function (N) {
  const nf = (d) => new Intl.NumberFormat('es-MX', { minimumFractionDigits: d, maximumFractionDigits: d });
  const NF = { 0: nf(0), 1: nf(1), 2: nf(2), 3: nf(3), 4: nf(4) };
  const esNum = (x) => typeof x === 'number' && isFinite(x);

  const F = {
    num(x, d = 2) { return esNum(x) ? (NF[d] || nf(d)).format(x) : '—'; },
    ent(x) { return esNum(x) ? NF[0].format(Math.round(x)) : '—'; },
    pct(x, d = 2) { return esNum(x) ? NF[d].format(x * 100) + '%' : '—'; },
    pctS(x, d = 2) { return esNum(x) ? (x > 0 ? '+' : x < 0 ? '−' : '') + NF[d].format(Math.abs(x * 100)) + '%' : '—'; },
    pp(x, d = 2) { return esNum(x) ? (x > 0 ? '+' : x < 0 ? '−' : '') + NF[d].format(Math.abs(x * 100)) + ' pp' : '—'; },
    /** Puntos base con signo (1 pb = 0.01%). */
    pb(x, d = 1) { if (!esNum(x)) return '—'; const v = x * 1e4; return (v > 0.05 ? '+' : v < -0.05 ? '−' : '') + NF[d].format(Math.abs(v)) + ' pb'; },
    precio(x) { if (!esNum(x)) return '—'; const a = Math.abs(x); return NF[a >= 1000 ? 2 : a >= 1 ? 2 : 4].format(x); },
    /** Montos grandes con la convención de los reportes en México: MDP (millones de pesos) o MDD (de dólares). */
    dinero(x, m = '') {
      if (!esNum(x)) return '—';
      const a = Math.abs(x), s = x < 0 ? '−' : '';
      const usd = m === 'USD', pre = usd ? 'US$' : m && m !== 'MXN' ? m + ' ' : '$';
      if (a >= 1e6) return s + pre + NF[a >= 1e8 ? 0 : 1].format(a / 1e6) + (usd ? ' MDD' : m && m !== 'MXN' ? ' M' : ' MDP');
      if (a >= 1e3) return s + pre + NF[0].format(a);
      return s + pre + NF[2].format(a);
    },
    pesos(x) { return esNum(x) ? (x < 0 ? '−$' : '$') + NF[2].format(Math.abs(x)) : '—'; },
    millones(x, d = 0) { return esNum(x) ? NF[d].format(x / 1e6) : '—'; },
    veces(x, d = 1) { return esNum(x) ? NF[d].format(x) + 'x' : '—'; },
    vol(x) {
      if (!esNum(x)) return '—';
      if (x >= 1e9) return NF[2].format(x / 1e9) + ' MM';
      if (x >= 1e6) return NF[2].format(x / 1e6) + ' M';
      if (x >= 1e3) return NF[1].format(x / 1e3) + ' mil';
      return NF[0].format(x);
    },
    cls(x) { return !esNum(x) || Math.abs(x) < 1e-12 ? 'neu' : x > 0 ? 'pos' : 'neg'; },
    flecha(x) { return !esNum(x) || Math.abs(x) < 1e-12 ? '■' : x > 0 ? '▲' : '▼'; },
    fecha(iso) {
      if (!iso) return '—';
      const d = new Date(String(iso).length <= 10 ? iso + 'T12:00:00' : iso);
      return isNaN(d) ? String(iso) : d.toLocaleDateString('es-MX', { day: '2-digit', month: 'short', year: 'numeric' }).replace('.', '');
    },
    fechaCorta(iso) {
      if (!iso) return '—';
      const d = new Date(String(iso).length <= 10 ? iso + 'T12:00:00' : iso);
      return isNaN(d) ? String(iso) : d.toLocaleDateString('es-MX', { day: '2-digit', month: 'short' }).replace('.', '');
    },
    hora(iso) {
      const d = new Date(iso);
      return isNaN(d) ? '—' : d.toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit', timeZone: 'America/Mexico_City' });
    },
    fechaHora(iso) {
      const d = new Date(iso);
      return isNaN(d) ? '—' : d.toLocaleString('es-MX', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit', timeZone: 'America/Mexico_City' }).replace('.', '');
    },
    hace(iso) {
      const d = new Date(iso); if (isNaN(d)) return '—';
      const s = (Date.now() - d) / 1000;
      if (s < 90) return 'hace un momento';
      if (s < 3600) return `hace ${Math.round(s / 60)} min`;
      if (s < 86400) return `hace ${Math.round(s / 3600)} h`;
      return `hace ${Math.round(s / 86400)} días`;
    },
    /** Valor de un KPI según su unidad. */
    kpi(v, u, moneda) {
      if (!esNum(v)) return 'n/d';
      if (u === '%') return F.pct(v, Math.abs(v) >= 10 ? 0 : 1);
      if (u === 'x') return F.veces(v, Math.abs(v) >= 100 ? 0 : Math.abs(v) >= 10 ? 1 : 2);
      if (u === 'dinero') return F.dinero(v, moneda);
      if (u === 'días') return F.num(v, 0) + ' días';
      if (u === 'pts') return F.num(v, 1);
      return F.num(v, 2);
    },
  };

  /** Etiqueta pública de la fuente de un dato. Los precios y estados se descargan de un agregador
      público de mercado; la terminal los presenta por su naturaleza (diferidos, reportados), no por marca. */
  const fuente = (s) => String(s ?? '').replace(/Yahoo Finance|Yahoo/gi, 'Mercado · diferido').replace(/\(fecha estimada por Mercado · diferido\)/g, '(fecha estimada)');
  const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const $ = (sel, raiz = document) => raiz.querySelector(sel);
  const $$ = (sel, raiz = document) => Array.from(raiz.querySelectorAll(sel));

  /** localStorage puede no existir (ventanas privadas, vistas previas): todo pasa por aquí. */
  const Local = {
    leer(k, def) { try { const v = localStorage.getItem('nst:' + k); return v == null ? def : JSON.parse(v); } catch (e) { return def; } },
    guardar(k, v) { try { localStorage.setItem('nst:' + k, JSON.stringify(v)); return true; } catch (e) { return false; } },
  };

  const Bus = (() => {
    const m = {};
    return {
      on(ev, fn) { (m[ev] = m[ev] || []).push(fn); },
      emit(ev, x) { (m[ev] || []).forEach((fn) => { try { fn(x); } catch (e) { console.error(ev, e); } }); },
    };
  })();

  /** Mini gráfica de línea en SVG. */
  function spark(valores, { w = 80, h = 22, color, area = true, base = null } = {}) {
    const xs = (valores || []).filter(esNum);
    if (xs.length < 2) return `<svg class="spk" width="${w}" height="${h}" aria-hidden="true"></svg>`;
    const min = Math.min(...xs), max = Math.max(...xs), r = max - min || 1;
    const paso = w / (xs.length - 1);
    const pts = xs.map((v, i) => [i * paso, h - 2 - ((v - min) / r) * (h - 4)]);
    const d = pts.map((p, i) => (i ? 'L' : 'M') + p[0].toFixed(1) + ' ' + p[1].toFixed(1)).join('');
    const sube = xs[xs.length - 1] >= (base ?? xs[0]);
    const c = color || (sube ? 'var(--pos)' : 'var(--neg)');
    const relleno = area ? `<path d="${d}L${w} ${h}L0 ${h}Z" fill="${c}" opacity=".12"/>` : '';
    return `<svg class="spk" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" preserveAspectRatio="none" aria-hidden="true">${relleno}<path d="${d}" fill="none" stroke="${c}" stroke-width="1.3" vector-effect="non-scaling-stroke"/></svg>`;
  }

  /** Barras verticales pequeñas (series trimestrales de KPIs). */
  function barras(serie, { w = 92, h = 26, unidad } = {}) {
    const xs = (serie || []).map((s) => (esNum(s.v) ? s.v : null));
    const val = xs.filter((x) => x !== null);
    if (val.length < 2) return '';
    const max = Math.max(...val.map(Math.abs)) || 1;
    const bw = w / xs.length;
    const cero = val.some((v) => v < 0) ? h / 2 : h - 1;
    const esc_ = val.some((v) => v < 0) ? h / 2 - 1 : h - 2;
    const rects = xs.map((v, i) => {
      if (v === null) return '';
      const alto = Math.max(1, (Math.abs(v) / max) * esc_);
      const y = v >= 0 ? cero - alto : cero;
      const ult = i === xs.length - 1;
      return `<rect x="${(i * bw + 1).toFixed(1)}" y="${y.toFixed(1)}" width="${Math.max(1, bw - 2).toFixed(1)}" height="${alto.toFixed(1)}" fill="${ult ? 'var(--acc)' : 'var(--line-3)'}"><title>${esc(serie[i].p)}: ${esc(F.kpi(v, unidad))}</title></rect>`;
    }).join('');
    return `<svg class="spk" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" aria-hidden="false" role="img">${rects}</svg>`;
  }

  /** Color de fondo para el mapa de calor según el cambio (escala simétrica). */
  function calor(x, tope = 0.03) {
    if (!esNum(x)) return '#262626';
    const t = Math.max(-1, Math.min(1, x / tope));
    if (t >= 0) return `rgb(${Math.round(20 + 10 * (1 - t))},${Math.round(60 + 110 * t)},${Math.round(45 + 50 * t)})`;
    return `rgb(${Math.round(70 + 150 * -t)},${Math.round(40 - 10 * -t)},${Math.round(45 - 5 * -t)})`;
  }

  function toast(texto, ms = 4500) {
    let c = $('#toast');
    if (!c) { c = document.createElement('div'); c.id = 'toast'; c.className = 'toast'; c.setAttribute('role', 'status'); document.body.appendChild(c); }
    const d = document.createElement('div'); d.innerHTML = texto; c.appendChild(d);
    setTimeout(() => d.remove(), ms);
  }

  Object.assign(N, { F, esc, $, $$, Local, Bus, spark, barras, calor, toast, esNum, fuente });
})(window.NST);
