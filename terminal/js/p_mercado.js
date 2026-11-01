/* North Star Terminal · MERCADO: monitor de cotizaciones del universo */
'use strict';
(function (N) {
  const { F, esc, $, $$, D, UI, App, Local } = N;

  function filas() {
    return D.emisoras().map((e) => {
      const q = D.cot(e.t), inf = D.info(e.t);
      return {
        t: e.t, n: e.n, sector: e.sector, sub: e.sub, bloque: e.bloque, peso: e.peso_indice,
        p: q.p, c: q.c, cp: q.cp, v: q.v, imp: q.p && q.v ? q.p * q.v : null, max: q.max, min: q.min,
        hi52: q.hi52 || inf.fiftyTwoWeekHigh, lo52: q.lo52 || inf.fiftyTwoWeekLow,
        r1m: D.rend(e.t, 21), ytd: D.rendYTD(e.t), r1a: D.rend(e.t, 252),
        pe: D.valor(e.t, 'pe'), ev: D.valor(e.t, 've_uafida'), dy: D.valor(e.t, 'rend_dividendo'),
        mc: inf.marketCap, cartera: D.enCartera(e.t), conservado: q.conservado,
      };
    });
  }

  App.registrar('mercado', {
    titulo: () => 'Mercado',
    pintar(cont, args) {
      const sectores = [...new Set(D.emisoras().map((e) => e.sector))].sort();
      const f = Local.leer('mercado:filtro', { sector: '', q: '', cartera: false });
      cont.innerHTML = `${UI.titulo('Monitor de mercado', `Último corte ${D.qGenerado ? F.fechaHora(D.qGenerado) : '—'} · clic en una fila para abrir la ficha`)}
        <div class="graf-barra">
          <input id="mq" placeholder="Buscar emisora…" value="${esc(f.q)}" style="width:190px">
          <span class="sep"></span>
          <button class="btn sm ${!f.sector ? 'on' : ''}" data-s="">TODOS</button>
          ${sectores.map((s) => `<button class="btn sm ${f.sector === s ? 'on' : ''}" data-s="${esc(s)}">${esc(s.toUpperCase())}</button>`).join('')}
          <span class="sep"></span>
          <button class="btn sm ${f.cartera ? 'on' : ''}" id="mCart">EN CARTERA</button>
        </div>
        <div class="panel"><div class="panel-b p0" id="mTabla"></div></div>`;
      const cols = [
        { k: 't', t: 'Emisora', i: true, f: (x) => `${UI.sym(x.t)}${x.cartera ? ' <span class="chip acc" title="Posición en el fondo">FONDO</span>' : ''}`, v: (x) => x.t },
        { k: 'n', t: 'Nombre', i: true, f: (x) => `<span class="nombre">${esc(x.n)}</span>`, v: (x) => x.n },
        { k: 'p', t: 'Último', f: (x) => `${F.precio(x.p)}${x.conservado ? ' <span class="warn" title="La fuente no respondió en la última corrida: precio anterior">*</span>' : ''}` },
        { k: 'c', t: 'Cambio', f: (x) => UI.num(x.c, (v) => F.num(v, 2)) },
        { k: 'cp', t: '%', f: (x) => UI.cambio(x.cp) },
        { k: 'rd', t: 'Rango día', f: (x) => UI.rango(x.min, x.max, x.p), v: (x) => (x.max > x.min ? (x.p - x.min) / (x.max - x.min) : null) },
        { k: 'imp', t: 'Importe', f: (x) => F.dinero(x.imp), title: 'precio × volumen del día' },
        { k: 'r52', t: '52 semanas', f: (x) => UI.rango(x.lo52, x.hi52, x.p), v: (x) => (x.hi52 > x.lo52 ? (x.p - x.lo52) / (x.hi52 - x.lo52) : null) },
        { k: 'r1m', t: '1M', f: (x) => UI.cambio(x.r1m, 1) },
        { k: 'ytd', t: 'Año', f: (x) => UI.cambio(x.ytd, 1) },
        { k: 'r1a', t: '12M', f: (x) => UI.cambio(x.r1a, 1) },
        { k: 'spk', t: '30 días', f: (x) => N.spark(D.serie(x.t, 30), { w: 74, h: 18 }), v: (x) => x.r1m },
        { k: 'pe', t: 'P/U', f: (x) => F.kpi(x.pe, 'x') },
        { k: 'ev', t: 'VE/UAFIDA', f: (x) => F.kpi(x.ev, 'x') },
        { k: 'dy', t: 'Div.', f: (x) => F.kpi(x.dy, '%') },
        { k: 'mc', t: 'Valor mdo.', f: (x) => F.dinero(x.mc) },
        { k: 'sector', t: 'Sector', i: true, cls: () => 'sec', f: (x) => esc(x.sub) },
      ];
      const orden = args[0] === 'cambio' ? 'cp' : Local.leer('mercado:orden', 'peso');
      let tabla;
      const aplicar = () => {
        const q = f.q.toUpperCase();
        const xs = filas().filter((x) => (!f.sector || x.sector === f.sector) && (!f.cartera || x.cartera) &&
          (!q || x.t.includes(q) || x.n.toUpperCase().includes(q)));
        if (!tabla) tabla = UI.tabla($('#mTabla', cont), cols, xs, { orden: orden === 'peso' ? null : orden, alClic: (t) => App.ir(`#/eq/${t}`) });
        else tabla.repintar(xs);
        Local.guardar('mercado:filtro', f);
      };
      aplicar();
      $('#mq', cont).addEventListener('input', (ev) => { f.q = ev.target.value; aplicar(); });
      $$('[data-s]', cont).forEach((b) => b.addEventListener('click', () => { f.sector = b.dataset.s; Local.guardar('mercado:filtro', f); App.pintar(); }));
      $('#mCart', cont).addEventListener('click', () => { f.cartera = !f.cartera; Local.guardar('mercado:filtro', f); App.pintar(); });
      this._tabla = () => tabla && tabla.repintar(filas());
    },
    refrescar() { App.pintar(); },
  });
})(window.NST);
