/* North Star Terminal · capa de datos
   Lee los JSON que publica GitHub Actions en la rama «datos». No necesita el vigilante:
   la página revisa estado.json cada minuto y recarga solo lo que cambió. */
'use strict';
(function (N) {
  const { Local, Bus } = N;
  const RAMA = 'datos';
  const RUTA = 'terminal/datos/';

  function repoActual() {
    const forzado = new URLSearchParams(location.search).get('repo');
    if (forzado) return forzado;
    if (/\.github\.io$/i.test(location.hostname)) {
      const duenio = location.hostname.split('.')[0];
      const repo = location.pathname.split('/').filter(Boolean)[0];
      if (repo) return `${duenio}/${repo}`;
    }
    return 'northstar-strategies/bbva-clinicas';
  }

  const local = location.protocol === 'file:' || /^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname);

  function candidatos() {
    const qs = new URLSearchParams(location.search).get('datos');
    const guardado = Local.leer('datos', '');
    const raw = `https://raw.githubusercontent.com/${repoActual()}/${RAMA}/${RUTA}`;
    const lista = [];
    if (qs) lista.push(qs.endsWith('/') ? qs : qs + '/');
    if (guardado) lista.push(guardado);
    if (local) lista.push('./datos/');
    lista.push(raw);
    if (!local) lista.push('./datos/');
    return [...new Set(lista)];
  }

  async function pedir(url, ms = 15000) {
    const c = new AbortController();
    const t = setTimeout(() => c.abort(), ms);
    try {
      const r = await fetch(url, { cache: 'no-store', signal: c.signal });
      if (!r.ok) throw new Error(`${r.status} ${url}`);
      return await r.json();
    } finally { clearTimeout(t); }
  }

  const D = {
    repo: repoActual(), base: null, estado: null, universo: null, U: {}, lista: [], q: {}, intradia: {},
    kpisArch: null, fund: {}, fichas: {}, noticias: [], macro: {}, cierres: null, cal: { eventos: [], analistas: {} },
    port: null, multiplos: {}, investigacion: [], sens: {}, sensMeta: {}, _velas: {}, _estados: {}, cargado: false, error: null, version: '',

    async iniciar() {
      for (const base of candidatos()) {
        try {
          const est = await pedir(base + 'estado.json?t=' + Date.now(), 9000);
          if (est && est.generado) { this.base = base; this.estado = est; break; }
        } catch (e) { /* siguiente candidato */ }
      }
      if (!this.base) {
        this.error = 'No se encontraron los datos de la terminal. Si es la primera vez, corre el workflow «Terminal · datos» en GitHub Actions para crear la rama datos.';
        Bus.emit('datos:error', this.error);
        return false;
      }
      await this.cargarTodo();
      this.cargado = true;
      Bus.emit('datos', { inicial: true });
      setInterval(() => this.refrescar(), 60000);
      document.addEventListener('visibilitychange', () => { if (!document.hidden) this.refrescar(); });
      return true;
    },

    url(nombre, version) { return this.base + nombre + '?v=' + encodeURIComponent(version || this.version || Date.now()); },

    async cargarRapido() {
      const [cot, intr, port, fichas] = await Promise.allSettled([
        pedir(this.base + 'cotizaciones.json?t=' + Date.now()),
        pedir(this.base + 'intradia.json?t=' + Date.now()),
        pedir(this.base + 'portafolio.json?t=' + Date.now()),
        pedir(this.base + 'fichas.json?t=' + Date.now()),
      ]);
      if (cot.status === 'fulfilled') {
        this.q = cot.value.q || {}; this.qSemilla = !!cot.value.semilla;
        // El corte es la hora de la última operación reportada, no la de la corrida.
        const ts = this.lista.map((e) => (this.q[e.t] || {}).ts).filter(Boolean).map((x) => new Date(x)).filter((d) => !isNaN(d));
        this.qGenerado = ts.length ? new Date(Math.max(...ts)).toISOString() : cot.value.generado;
      }
      if (intr.status === 'fulfilled') this.intradia = intr.value || {};
      if (port.status === 'fulfilled') this.port = port.value;
      if (fichas.status === 'fulfilled') this.fichas = fichas.value.emisoras || {};
    },

    async cargarTodo() {
      this.version = this.estado.ultimo_completo || this.estado.generado;
      const v = this.version;
      const nombres = ['universo', 'kpis', 'fundamentales', 'noticias', 'macro', 'cierres', 'calendario', 'multiplos', 'investigacion', 'sensibilidad'];
      const res = await Promise.allSettled(nombres.map((n) => pedir(this.url(n + '.json', v))));
      const r = Object.fromEntries(nombres.map((n, i) => [n, res[i].status === 'fulfilled' ? res[i].value : null]));
      if (r.universo) {
        this.universo = r.universo;
        this.lista = r.universo.emisoras || [];
        this.U = Object.fromEntries(this.lista.map((e) => [e.t, e]));
      }
      this.kpisArch = r.kpis;
      this.fund = (r.fundamentales && r.fundamentales.emisoras) || {};
      this.noticias = (r.noticias && r.noticias.items) || [];
      this.macro = (r.macro && r.macro.series) || {};
      this.cierres = r.cierres;
      this.cal = r.calendario || { eventos: [], analistas: {} };
      this.multiplos = (r.multiplos && r.multiplos.emisoras) || {};
      this.investigacion = (r.investigacion && r.investigacion.documentos) || [];
      this.sens = (r.sensibilidad && r.sensibilidad.emisoras) || {};
      this.sensMeta = r.sensibilidad || {};
      this._velas = {}; this._estados = {};
      this._idx = null;
      await this.cargarRapido();
    },

    async refrescar() {
      if (!this.base || document.hidden) return;
      let est;
      try { est = await pedir(this.base + 'estado.json?t=' + Date.now(), 9000); } catch (e) { Bus.emit('datos:offline', e); return; }
      if (!est || est.generado === this.estado.generado) { Bus.emit('datos:igual', est); return; }
      const completo = est.ultimo_completo !== this.estado.ultimo_completo;
      this.estado = est;
      if (completo) await this.cargarTodo(); else await this.cargarRapido();
      Bus.emit('datos', { completo });
    },

    async velas(t) {
      if (this._velas[t]) return this._velas[t];
      const p = pedir(this.url(`velas/${encodeURIComponent(t)}.json`)).catch(() => null);
      this._velas[t] = p;
      return p;
    },
    async estados(t) {
      if (this._estados[t]) return this._estados[t];
      const p = pedir(this.url(`estados/${encodeURIComponent(t)}.json`)).catch(() => null);
      this._estados[t] = p;
      return p;
    },

    // ── consultas ──
    emisoras(incluirEtf = true) { return this.lista.filter((e) => incluirEtf || e.t !== 'MEXTRAC'); },
    cot(t) { return this.q[t] || {}; },
    precio(t) { return this.cot(t).p; },
    ficha(t) { return this.fichas[t] || {}; },
    info(t) { return this.fund[t] || {}; },
    nombre(t) { const e = this.U[t]; return (e && e.n) || (this.macro[t] && this.macro[t].n) || t; },
    kp(t) { return (this.kpisArch && this.kpisArch.emisoras && this.kpisArch.emisoras[t]) || null; },
    def(clave) { return (this.kpisArch && this.kpisArch.definiciones && this.kpisArch.definiciones[clave]) || {}; },
    /** KPI con su definición (nombre, fórmula, unidad...). */
    kpi(t, clave) {
      const k = this.kp(t); if (!k) return null;
      const x = (k.kpis || []).find((y) => y.clave === clave);
      return x ? Object.assign({}, this.def(clave), x) : null;
    },
    valor(t, clave) { const k = this.kpi(t, clave); return k ? k.valor : null; },

    /** Índice fecha → posición en la matriz de cierres. */
    serie(t, n) {
      const c = this.cierres; if (!c || !c.s || !c.s[t]) return [];
      const s = c.s[t]; return n ? s.slice(-n) : s;
    },
    fechas(n) { const c = this.cierres; if (!c) return []; return n ? c.d.slice(-n) : c.d; },
    /** Rendimiento sobre n sesiones con la cotización más reciente. */
    rend(t, sesiones) {
      const s = this.serie(t); if (s.length <= sesiones) return null;
      const p = this.precio(t) || s[s.length - 1];
      const base = s[s.length - 1 - sesiones];
      return base ? p / base - 1 : null;
    },
    rendYTD(t) {
      const c = this.cierres; if (!c) return null;
      const anio = new Date().getFullYear();
      let i = c.d.findIndex((f) => f >= `${anio}-01-01`);
      if (i <= 0) return null;
      const base = (c.s[t] || [])[i - 1];
      const p = this.precio(t) || (c.s[t] || [])[c.d.length - 1];
      return base && p ? p / base - 1 : null;
    },
    noticiasDe(t, n = 50) { return this.noticias.filter((x) => x.t === t).slice(0, n); },
    eventosDe(t) { return (this.cal.eventos || []).filter((e) => String(e.t || '').split(/\s+/).includes(t)); },
    enCartera(t) { const p = this.port && this.port.actual; return !!(p && p.posiciones.find((x) => x.t === t)); },
    /** Investigación del equipo sobre la emisora: la del documento más reciente que la cubra. */
    inv(t) {
      for (const d of this.investigacion || []) { const e = d.emisoras && d.emisoras[t]; if (e) return Object.assign({ doc: d }, e); }
      return null;
    },
    /** Puente de valuación (drivers) y betas de mercado de la emisora. */
    sensDe(t) { return (this.sens && this.sens[t]) || null; },
    /** Aporte de la emisora al alfa del fondo (atribución ligada desde la fecha de referencia). */
    atrib(t) { const a = this.port && this.port.atribucion; return (a && (a.posiciones || []).find((x) => x.t === t)) || null; },
    logo(t) {
      const e = this.U[t]; if (!e || !e.logo) return null;
      return '../' + encodeURIComponent(e.logo);
    },
  };

  N.D = D;
  N.repoActual = repoActual;
})(window.NST);
