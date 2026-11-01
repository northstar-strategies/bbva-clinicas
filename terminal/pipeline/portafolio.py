"""Portafolio del fondo reconstruido desde operaciones.csv, sin el tracker de Excel.

Reproduce la contabilidad del tracker: efectivo por fecha de operación, valor =
Σ títulos × cierre + efectivo, rendimiento diario V(t)/V(t-1) − 1, acumulado desde la
fecha del portafolio de referencia y benchmark = precio del MEXTRAC09 (estimado con la
canasta del índice los días en que el ETF no opera).
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
