"""Portafolio del fondo reconstruido desde operaciones.csv, sin el tracker de Excel.

Reproduce la contabilidad del tracker: efectivo por fecha de operación, valor =
Σ títulos × cierre + efectivo, rendimiento diario V(t)/V(t-1) − 1, acumulado desde la
fecha del portafolio de referencia y benchmark = precio del MEXTRAC09 (estimado con la
canasta del índice los días en que el ETF no opera).

La atribución del alfa por posición replica la del tracker (atribucion_diaria.csv) al
centavo: aporte_i = (w_i + w_ETF·b_i − b_i) × (r_i − r_B), más los efectos de efectivo,
premio del ETF contra su canasta, operaciones intradía y comisiones; los días se ligan
con Cariño para que la suma cuadre con el alfa acumulado.
"""
from __future__ import annotations

import math
from collections import defaultdict

from util import desv, limpiar, num

COMPRAS = {"ASIGNACIÓN", "ASIGNACION", "COMPRA"}


def _entero(v) -> int:
    x = num(v)
    return int(round(x)) if x is not None else 0


def posiciones_al(ops: list[dict], fecha: str, capital: float) -> tuple[dict, float, dict]:
    """Títulos, efectivo y costo promedio con las operaciones hasta `fecha` (inclusive)."""
    tit: dict[str, int] = defaultdict(int)
    costo: dict[str, float] = defaultdict(float)     # costo total vigente (método de costo promedio)
    realizado: dict[str, float] = defaultdict(float)
    caja = capital
    for o in sorted(ops, key=lambda x: (x.get("fecha", ""), x.get("hora", ""))):
        if (o.get("fecha") or "") > fecha:
            continue
        s, tipo, q, px = o.get("simbolo"), (o.get("tipo") or "").upper(), _entero(o.get("titulos")), num(o.get("precio")) or 0
        gastos = (num(o.get("comision")) or 0) + (num(o.get("iva")) or 0)
        if tipo in COMPRAS:
            tit[s] += q
            costo[s] += q * px + gastos
        elif tipo == "VENTA":
            if tit[s] > 0:
                prom = costo[s] / tit[s]
                realizado[s] += q * px - gastos - q * prom
                costo[s] -= q * prom
            tit[s] -= q
        caja += num(o.get("caja")) or 0
    pos = {s: q for s, q in tit.items() if q}
    prom = {s: costo[s] / tit[s] for s in pos if tit[s] > 0}
    return pos, caja, {"costo_promedio": prom, "realizado": dict(realizado)}


def estimar_benchmark(fechas: list[str], cierres: dict[str, dict], pesos: dict[str, float],
                      sin_operacion: set[str], etf: str = "MEXTRAC") -> dict[str, float]:
    """Precio del ETF por fecha; los días sin operación se estima con el rendimiento de la canasta."""
    total = sum(pesos.values()) or 1
    w = {s: p / total for s, p in pesos.items()}
    out: dict[str, float] = {}
    previo = None
    for i, f in enumerate(fechas):
        px = num(cierres.get(f, {}).get(etf))
        if px is not None and f not in sin_operacion:
            out[f] = px
        elif previo is not None and i > 0:
            f0 = fechas[i - 1]
            r, cubierto = 0.0, 0.0
            for s, ws in w.items():
                a, b = num(cierres.get(f0, {}).get(s)), num(cierres.get(f, {}).get(s))
                if a and b:
                    r += ws * (b / a - 1)
                    cubierto += ws
            out[f] = previo * (1 + (r / cubierto if cubierto else 0))
        elif px is not None:
            out[f] = px
        if f in out:
            previo = out[f]
    return out


def serie_diaria(ops: list[dict], cierres: dict[str, dict], capital: float, referencia: str,
                 pesos_indice: dict[str, float], sin_operacion: set[str] | None = None) -> list[dict]:
    """Valor del fondo al cierre de cada día desde la fecha de referencia."""
    fechas = sorted(f for f in cierres if f >= referencia)
    if not fechas:
        return []
    bench = estimar_benchmark(sorted(cierres), cierres, pesos_indice, sin_operacion or set())
    filas = []
    for f in fechas:
        pos, caja, _ = posiciones_al(ops, f, capital)
        valor, faltan = caja, []
        for s, q in pos.items():
            px = num(cierres[f].get(s))
            if px is None:
                # sin cierre ese día: último precio conocido
                previos = [g for g in sorted(cierres) if g < f and num(cierres[g].get(s)) is not None]
                px = num(cierres[previos[-1]].get(s)) if previos else None
                faltan.append(s)
            if px is not None:
                valor += q * px
        filas.append({"f": f, "valor": valor, "efectivo": caja, "bench": bench.get(f), "sin_cierre": faltan})
    base_v, base_b = filas[0]["valor"], filas[0]["bench"]
    out, activos = [], []
    for i, x in enumerate(filas):
        if i == 0:
            continue
        p = filas[i - 1]
        rd = x["valor"] / p["valor"] - 1 if p["valor"] else None
        bd = x["bench"] / p["bench"] - 1 if x["bench"] and p["bench"] else None
        ad = rd - bd if rd is not None and bd is not None else None
        if ad is not None:
            activos.append(ad)
        ra = x["valor"] / base_v - 1 if base_v else None
        ba = x["bench"] / base_b - 1 if x["bench"] and base_b else None
        sd = desv(activos)
        out.append({
            "f": x["f"], "dia": i, "valor": x["valor"], "efectivo": x["efectivo"],
            "rend_dia": rd, "bench_dia": bd, "activo_dia": ad,
            "rend_acum": ra, "bench_acum": ba, "activo_acum": ra - ba if ra is not None and ba is not None else None,
            "te_expost": sd * math.sqrt(252) if sd is not None and len(activos) >= 3 else None,
            "sin_cierre": x["sin_cierre"] or None,
        })
    return [limpiar(r) for r in out]


def foto_actual(ops: list[dict], capital: float, cotiz: dict[str, dict], pesos_indice: dict[str, float],
                bloques: dict[str, str], hoy: str) -> dict:
    """Posiciones valuadas con la última cotización disponible."""
    pos, caja, extra = posiciones_al(ops, hoy, capital)
    filas, valor, valor_prev = [], caja, caja
    for s, q in sorted(pos.items()):
        c = cotiz.get(s) or {}
        px, prev = num(c.get("p")), num(c.get("a")) or num(c.get("p"))
        if px is None:
            continue
        mv, mv_prev = q * px, q * (prev or px)
        valor += mv
        valor_prev += mv_prev
        prom = extra["costo_promedio"].get(s)
        filas.append({
            "t": s, "titulos": q, "precio": px, "anterior": prev, "valor": mv,
            "cambio_dia": px / prev - 1 if prev else None, "aporte_dia": mv - mv_prev,
            "costo_promedio": prom, "pyg": (px - prom) * q if prom else None,
            "pyg_pct": px / prom - 1 if prom else None, "bloque": bloques.get(s, ""),
            "realizado": extra["realizado"].get(s),
        })
    for f in filas:
        f["peso"] = f["valor"] / valor if valor else None
    w_etf = next((f["peso"] for f in filas if f["t"] == "MEXTRAC"), 0) or 0
    total_idx = sum(pesos_indice.values()) or 1
    look = defaultdict(float)
    for f in filas:
        if f["t"] != "MEXTRAC" and f["peso"]:
            look[f["t"]] += f["peso"]
    for s, w in pesos_indice.items():
        look[s] += w_etf * w / total_idx
    desviacion = {s: look.get(s, 0) - pesos_indice.get(s, 0) / total_idx for s in set(look) | set(pesos_indice)}
    return limpiar({
        "valor": valor, "valor_previo": valor_prev, "efectivo": caja, "efectivo_pct": caja / valor if valor else None,
        "rend_dia": valor / valor_prev - 1 if valor_prev else None,
        "posiciones": sorted(filas, key=lambda f: -(f["valor"] or 0)),
        "pesos_efectivos": dict(look), "desviacion": desviacion,
        "realizado_total": sum(extra["realizado"].values()),
    })


# ───────────────────────────── atribución del alfa por posición ─────────────────────────────

def _carino(r: float, b: float) -> float:
    """Coeficiente de Cariño: convierte aportes aritméticos de un periodo en aportes logarítmicos."""
    if abs(r - b) < 1e-12:
        return 1 / (1 + r)
    return (math.log1p(r) - math.log1p(b)) / (r - b)


def _cierres_arrastrados(cierres: dict[str, dict], fechas: list[str], simbolos: set[str]) -> dict[str, dict]:
    """Cierre por fecha y símbolo; si un día no hubo cierre se usa el último conocido (igual que serie_diaria)."""
    out, ultimo = {}, {}
    for f in sorted(cierres):
        for s in simbolos:
            x = num(cierres[f].get(s))
            if x is not None:
                ultimo[s] = x
        if f in fechas:
            out[f] = dict(ultimo)
    return out


def pesos_benchmark(fechas: list[str], px: dict[str, dict], oficiales: dict[str, dict[str, float]],
                    base: dict[str, float], fecha_base: str | None, cierres: dict[str, dict]) -> tuple[dict, str]:
    """Pesos del índice al inicio de cada día de `fechas[1:]` (es decir, al cierre del día anterior).

    Los días que registró el tracker usan sus pesos (atribucion_diaria.csv). Los demás se arrastran
    con el rendimiento de precio del día previo, que es como el tracker los mueve. Sin tracker se
    parte de los pesos del índice del archivo de parámetros, arrastrados desde su fecha de referencia.
    """
    total = sum(base.values()) or 1
    cur: dict[str, float] | None = None
    if not oficiales or fechas[1] not in oficiales:
        cur = {s: w / total for s, w in base.items()}
        if fecha_base:
            todas = sorted(cierres)
            p0 = _cierres_arrastrados(cierres, [f for f in todas if f >= fecha_base][:1], set(base))
            p1 = _cierres_arrastrados(cierres, [fechas[0]], set(base))
            a, z = next(iter(p0.values()), {}), p1.get(fechas[0], {})
            x = {s: w * (z[s] / a[s] if a.get(s) and z.get(s) else 1) for s, w in cur.items()}
            t = sum(x.values()) or 1
            cur = {s: v / t for s, v in x.items()}
    out, uso_tracker = {}, 0
    for i in range(1, len(fechas)):
        f, f0 = fechas[i], fechas[i - 1]
        if f in oficiales:
            cur = dict(oficiales[f])
            uso_tracker += 1
        elif i > 1 and cur is not None:
            fa = fechas[i - 2]
            x = {s: w * (px[f0].get(s, 0) / px[fa][s] if px[fa].get(s) and px[f0].get(s) else 1) for s, w in cur.items()}
            t = sum(x.values()) or 1
            cur = {s: v / t for s, v in x.items()}
        out[f] = cur or {}
    fuente = (f"tracker (atribucion_diaria.csv) en {uso_tracker} de {len(fechas) - 1} días; el resto, arrastrados con precios"
              if uso_tracker else "pesos del índice de parametros.json arrastrados con precios")
    return out, fuente


def libro_ventas(ops: list[dict]) -> list[dict]:
    """Ventas agrupadas por orden (fecha, símbolo, motivo) con su utilidad realizada contra el costo promedio."""
    tit: dict[str, int] = defaultdict(int)
    costo: dict[str, float] = defaultdict(float)
    grupos: dict[tuple, dict] = {}
    for o in sorted(ops, key=lambda x: (x.get("fecha", ""), x.get("hora", ""))):
        s, tipo, q, px = o.get("simbolo"), (o.get("tipo") or "").upper(), _entero(o.get("titulos")), num(o.get("precio")) or 0
        gastos = (num(o.get("comision")) or 0) + (num(o.get("iva")) or 0)
        if tipo in COMPRAS:
            tit[s] += q
            costo[s] += q * px + gastos
        elif tipo == "VENTA" and q:
            prom = costo[s] / tit[s] if tit[s] > 0 else px
            k = (o.get("fecha"), s, o.get("motivo") or "")
            g = grupos.setdefault(k, {"f": o.get("fecha"), "t": s, "motivo": o.get("motivo") or "", "bloque": o.get("bloque") or "",
                                      "titulos": 0, "importe": 0.0, "gastos": 0.0, "realizado": 0.0, "costo": 0.0})
            g["titulos"] += q
            g["importe"] += q * px
            g["gastos"] += gastos
            g["realizado"] += q * px - gastos - q * prom
            g["costo"] += q * prom
            if tit[s] > 0:
                costo[s] -= q * prom
            tit[s] -= q
            g["queda"] = tit[s]
    out = []
    for g in grupos.values():
        g["precio"] = g["importe"] / g["titulos"]
        g["costo_promedio"] = g["costo"] / g["titulos"]
        g["rend"] = g["realizado"] / g["costo"] if g["costo"] else None
        g["cierre_total"] = g["queda"] <= 0
        out.append(g)
    return sorted(out, key=lambda g: (g["f"], g["t"]))


def atribucion(ops: list[dict], cierres: dict[str, dict], capital: float, referencia: str,
               pesos_indice: dict[str, float], fecha_ref_indice: str | None, sin_operacion: set[str] | None,
               dividendos: dict[str, dict[str, float]], oficiales: dict[str, dict[str, float]] | None = None,
               tracker: dict[str, dict[str, float]] | None = None, bloques: dict[str, str] | None = None,
               inicio: str | None = None) -> dict:
    """Aporte de cada posición (abierta, cerrada o solo vía índice) al alfa acumulado contra el MEXTRAC.

    dividendos: {fecha_ex: {símbolo: monto por acción}}; entran al rendimiento del día ex (rendimiento total).
    oficiales:  pesos del índice por fecha registrados por el tracker.
    tracker:    aportes del tracker por fecha y emisora, para verificar el cálculo.
    """
    fechas = sorted(f for f in cierres if f >= referencia)
    if len(fechas) < 2:
        return {}
    bloques = bloques or {}
    bench = estimar_benchmark(sorted(cierres), cierres, pesos_indice, sin_operacion or set())
    simbolos = set(pesos_indice) | {o.get("simbolo") for o in ops if o.get("simbolo")} | {s for d in (oficiales or {}).values() for s in d}
    px = _cierres_arrastrados(cierres, fechas, simbolos)
    pb, fuente_pb = pesos_benchmark(fechas, px, oficiales or {}, pesos_indice, fecha_ref_indice, cierres)

    dias, aportes, tuvo = [], defaultdict(dict), defaultdict(set)
    rend_i: dict[str, list[float]] = defaultdict(list)
    max_dif, n_ver = 0.0, 0
    for i in range(1, len(fechas)):
        f0, f = fechas[i - 1], fechas[i]
        p0, p1 = px[f0], px[f]
        pos0, caja0, _ = posiciones_al(ops, f0, capital)
        pos1, caja1, _ = posiciones_al(ops, f, capital)
        v0 = caja0 + sum(q * p0.get(s, 0) for s, q in pos0.items())
        v1 = caja1 + sum(q * p1.get(s, 0) for s, q in pos1.items())
        if not v0 or not bench.get(f) or not bench.get(f0):
            continue
        r_p, r_b = v1 / v0 - 1, bench[f] / bench[f0] - 1
        w = {s: q * p0.get(s, 0) / v0 for s, q in pos0.items() if s != "MEXTRAC"}
        w_etf = pos0.get("MEXTRAC", 0) * p0.get("MEXTRAC", 0) / v0
        w_c = caja0 / v0
        b = pb.get(f, {})
        div_f = dividendos.get(f, {})
        r = {s: (p1[s] + div_f.get(s, 0)) / p0[s] - 1 for s in set(w) | set(b) if p0.get(s) and p1.get(s)}
        r_bas = sum(b[s] * r.get(s, 0) for s in b)
        dia = {}
        for s in set(w) | set(b):
            if s == "MEXTRAC":
                continue
            a = (w.get(s, 0) + w_etf * b.get(s, 0) - b.get(s, 0)) * (r.get(s, 0) - r_b)
            dia[s] = a
            aportes[s][f] = a
            if pos0.get(s, 0) > 0:
                tuvo[s].add(f)
            if s in r:
                rend_i[s].append(r[s])
        ganancia_ops, gastos = 0.0, 0.0
        for o in ops:
            if o.get("fecha") != f:
                continue
            s, tipo, q, pr = o.get("simbolo"), (o.get("tipo") or "").upper(), _entero(o.get("titulos")), num(o.get("precio")) or 0
            if tipo in COMPRAS and p1.get(s):
                ganancia_ops += q * (p1[s] - pr)
            elif tipo == "VENTA" and p1.get(s):
                ganancia_ops += q * (pr - p1[s])
            if tipo in COMPRAS or tipo == "VENTA":
                gastos += (num(o.get("comision")) or 0) + (num(o.get("iva")) or 0)
        efe = w_c * (0 - r_b)
        etf = (1 - w_etf) * (r_bas - r_b)
        opr, com = ganancia_ops / v0, -gastos / v0
        emis = sum(dia.values())
        resid = (r_p - r_b) - (emis + efe + etf + opr + com)
        if tracker and f in tracker:
            for s, a in dia.items():
                if s in tracker[f]:
                    max_dif = max(max_dif, abs(a - tracker[f][s]))
                    n_ver += 1
        dias.append({"f": f, "rend": r_p, "bench": r_b, "alfa": r_p - r_b, "emisoras": emis, "efectivo": efe, "etf": etf,
                     "operaciones": opr, "comisiones": com, "residual": resid, "k": _carino(r_p, r_b),
                     "peso_etf": w_etf, "peso_caja": w_c, "canasta": r_bas})
    if not dias:
        return {}
    R = math.prod(1 + d["rend"] for d in dias) - 1
    B = math.prod(1 + d["bench"] for d in dias) - 1
    K = _carino(R, B)
    for d in dias:
        d["kk"] = d["k"] / K

    def ligado(serie: dict[str, float]) -> float:
        return sum(d["kk"] * serie.get(d["f"], 0) for d in dias)

    comp = {c: sum(d["kk"] * d[c] for d in dias) for c in ("emisoras", "efectivo", "etf", "operaciones", "comisiones", "residual")}
    ultimo = fechas[-1]
    pos_fin, caja_fin, extra = posiciones_al(ops, ultimo, capital)
    v_fin = caja_fin + sum(q * px[ultimo].get(s, 0) for s, q in pos_fin.items())
    w_etf_fin = pos_fin.get("MEXTRAC", 0) * px[ultimo].get("MEXTRAC", 0) / v_fin if v_fin else 0
    b_fin = pb.get(ultimo, {})
    divs_cobrados: dict[str, float] = defaultdict(float)
    for o in ops:
        if (o.get("tipo") or "").upper() == "DIVIDENDO":
            divs_cobrados[o.get("simbolo")] += num(o.get("caja")) or 0
    alguna_vez = set()
    corte = inicio or referencia
    for o in ops:
        if (o.get("tipo") or "").upper() in COMPRAS and (o.get("fecha") or "") >= corte:
            alguna_vez.add(o.get("simbolo"))
    filas = []
    for s in sorted(set(aportes) | set(pos_fin) - {"MEXTRAC"}):
        if s == "MEXTRAC":
            continue
        q = pos_fin.get(s, 0)
        estado = "abierta" if q > 0 else ("cerrada" if s in alguna_vez else "indice")
        serie_acum, acum = [], 0.0
        for d in dias:
            acum += d["kk"] * aportes[s].get(d["f"], 0)
            serie_acum.append(acum)
        precio = px[ultimo].get(s)
        prom = extra["costo_promedio"].get(s)
        no_real = (precio - prom) * q if (prom and precio and q > 0) else 0.0
        real = extra["realizado"].get(s, 0.0)
        peso = q * (precio or 0) / v_fin if v_fin and q > 0 else 0.0
        filas.append({
            "t": s, "estado": estado, "bloque": bloques.get(s, "INDICE" if estado == "indice" else ""), "titulos": q,
            "precio": precio, "peso": peso, "peso_b": b_fin.get(s, 0.0), "peso_lt": peso + w_etf_fin * b_fin.get(s, 0.0),
            "activo": peso + w_etf_fin * b_fin.get(s, 0.0) - b_fin.get(s, 0.0),
            "rend": math.prod(1 + x for x in rend_i[s]) - 1 if rend_i[s] else None,
            "aporte": ligado(aportes[s]),
            "aporte_tenencia": sum(d["kk"] * aportes[s].get(d["f"], 0) for d in dias if d["f"] in tuvo[s]),
            "dias_tenencia": len(tuvo[s]),
            "costo_promedio": prom, "pyg_no_realizado": no_real, "pyg_realizado": real,
            "dividendos": divs_cobrados.get(s, 0.0), "pyg_total": no_real + real + divs_cobrados.get(s, 0.0),
            "serie": serie_acum,
        })
    filas.sort(key=lambda x: -abs(x["aporte"]))
    efectos = [
        {"clave": "efectivo", "n": "Efectivo", "aporte": comp["efectivo"],
         "nota": "Caja que no rinde mientras el MEXTRAC se mueve: w_caja × (0 − r_MEXTRAC)."},
        {"clave": "etf", "n": "Premio del ETF contra su canasta", "aporte": comp["etf"],
         "nota": "Diferencia entre el precio del MEXTRAC y el rendimiento de las acciones de su índice: (1 − w_ETF) × (r_canasta − r_MEXTRAC)."},
        {"clave": "operaciones", "n": "Operaciones del día", "aporte": comp["operaciones"],
         "nota": "Comprar abajo o vender arriba del cierre del día de la operación."},
        {"clave": "comisiones", "n": "Comisiones e IVA", "aporte": comp["comisiones"], "nota": "Costo de operar."},
    ]
    if abs(comp["residual"]) > 1e-6:
        efectos.append({"clave": "residual", "n": "Sin explicar", "aporte": comp["residual"],
                        "nota": "Dividendos cobrados en fecha distinta a la ex o precios faltantes; debe ser casi cero."})
    return limpiar({
        "desde": referencia, "hasta": ultimo, "dias": len(dias), "fechas": [d["f"] for d in dias],
        "rend": R, "bench": B, "alfa": R - B, "componentes": comp,
        "suma": sum(comp.values()),
        "posiciones": filas, "efectos": efectos, "detalle": dias,
        "ventas": libro_ventas(ops),
        "pesos_benchmark": fuente_pb,
        "verificacion": {"comparados": n_ver, "max_dif": max_dif} if n_ver else None,
        "metodo": ("aporte_i = (w_i + w_ETF·b_i − b_i) × (r_i − r_MEXTRAC) con pesos al cierre previo y rendimiento total "
                   "(dividendo el día ex); días ligados con Cariño, así Σ aportes = alfa acumulado."),
    }, 8)
