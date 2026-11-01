"""¿Cuánto se mueve el precio si cambia un KPI? Dos respuestas que se complementan.

1. Fundamental (puente de valuación). Cada driver de investigacion/drivers.json se traduce en
   cambio de UAFIDA (o de utilidad en financieras) y luego en precio con el múltiplo constante:
       Δprecio/precio = (VE/capital) × ΔUAFIDA/UAFIDA          con VE/UAFIDA constante
       Δprecio/precio = Δutilidad/utilidad                      con P/U constante (bancos, seguros)
   VE/capital («apalancamiento del capital») = VE/UAFIDA ÷ (VE/UAFIDA − deuda neta/UAFIDA).
   Es lineal: sirve para movimientos moderados y supone que el mercado no cambia el múltiplo.

2. Empírica (betas de mercado). Regresión de los rendimientos semanales de la acción contra el IPC
   y un factor a la vez (dólar, cobre, oro, tasas de EUA, petróleo...), con dos años de historia:
       r_acción = α + β_IPC · r_IPC + β_factor · r_factor + ε
   β_factor es la sensibilidad al factor una vez descontado el mercado. Se reporta su estadístico t
   y cuánto R² agrega el factor sobre el IPC solo.

Solo biblioteca estándar.
"""
from __future__ import annotations

import json
import math
import os
from datetime import date

from universo import RAIZ
from util import num

RUTA_DRIVERS = os.path.join(RAIZ, "investigacion", "drivers.json")
FINANCIERAS = {"bancos", "microfinanzas", "seguros"}

# Factores para las betas: clave en macro.json → (nombre, se mide en cambio absoluto en pp en vez de %).
FACTORES = {
    "USDMXN": ("Dólar en pesos", False), "COBRE": ("Cobre", False), "ORO": ("Oro", False), "PLATA": ("Plata", False),
    "BRENT": ("Petróleo Brent", False), "GASNAT": ("Gas natural", False), "UST10": ("Bono de EUA a 10 años", True),
    "SP500": ("S&P 500", False), "BRLMXN": ("Real brasileño", False), "MAIZ": ("Maíz", False), "TRIGO": ("Trigo", False),
    "AZUCAR": ("Azúcar", False), "EURMXN": ("Euro en pesos", False),
}


def leer_drivers(ruta: str = RUTA_DRIVERS) -> dict:
    try:
        with open(ruta, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"emisoras": {}, "sector": {}}


# ───────────────────────────── base de valuación ─────────────────────────────

def _ultimo(est: dict | None, hoja: str, fila: str) -> float | None:
    t = ((est or {}).get(hoja) or {}).get("trimestral") or {}
    xs = (t.get("filas") or {}).get(fila) or []
    for x in reversed(xs):
        if num(x) is not None:
            return num(x)
    return None


def base_valuacion(t: str, grupo: str, kp: dict, info: dict, precio: float | None, usd: float | None,
                   est: dict | None, conf: dict) -> dict:
    """Números de partida: múltiplo, apalancamiento del capital, márgenes y montos UDM (en millones)."""
    fin = grupo in FINANCIERAS or conf.get("base") == "utilidad"
    moneda = info.get("financialCurrency") or "MXN"
    fx = usd if moneda == "USD" and usd else 1.0
    b: dict = {"tipo": "utilidad" if fin else "uafida", "moneda_reporte": moneda, "precio": precio}
    if fin:
        b["L"] = 1.0
        b["pe"] = kp.get("pe")
        u = num(conf.get("utilidad_base"))
        if u is None and num(info.get("netIncomeToCommon")):
            u = num(info.get("netIncomeToCommon")) * fx / 1e6
        b["utilidad"] = u
        b["utilidad_nota"] = conf.get("utilidad_nota") or "utilidad neta mayoritaria de los últimos 12 meses"
        cartera = num(conf.get("cartera"))
        if cartera is None:
            nl = _ultimo(est, "balance", "NetLoan")
            cartera = nl * fx / 1e6 if nl else None
        b["cartera"] = cartera
        b["cartera_nota"] = conf.get("cartera_nota") or "cartera neta del último balance"
        prim = num(info.get("totalRevenue"))
        b["primas"] = prim * fx / 1e6 if prim and grupo == "seguros" else None
        return b
    ve, dn = num(kp.get("ve_uafida")), num(kp.get("deuda_neta_uafida"))
    if ve is not None and dn is not None and ve - dn > 0.5:
        b["L"] = ve / (ve - dn)
        b["L_nota"] = f"VE/UAFIDA {ve:.1f}x ÷ (VE/UAFIDA − deuda neta/UAFIDA {dn:.1f}x)"
    else:
        mc, deuda, caja = num(info.get("marketCap")), num(info.get("totalDebt")), num(info.get("totalCash"))
        if mc and deuda is not None:
            b["L"] = (mc + (deuda - (caja or 0)) * fx) / mc
            b["L_nota"] = "(valor de mercado + deuda neta) ÷ valor de mercado"
    b["ve_uafida"] = ve
    m = num(kp.get("margen_uafida"))
    if m is None or not (0.02 < m < 0.95):
        m = num(info.get("ebitdaMargins"))
    b["margen_uafida"] = m if m and 0.02 < m < 0.95 else None
    mb = num(kp.get("margen_bruto")) or num(info.get("grossMargins"))
    b["margen_bruto"] = mb if mb and 0 < mb < 1 else None
    u = num(info.get("ebitda"))
    b["uafida_udm"] = u / 1e6 if u else None          # en la moneda del reporte
    b["moneda_uafida"] = moneda
    return b


# ───────────────────────────── drivers ─────────────────────────────

def drivers_por_defecto(grupo: str, moneda: str) -> list[dict]:
    if grupo in ("bancos", "microfinanzas"):
        return [
            {"id": "min", "n": "MIN (margen de interés neto)", "unidad": "pb", "tipo": "min", "paso": 10, "rango": [-50, 50],
             "porque": "Sensibilidad del margen financiero a Banxico."},
            {"id": "costo_riesgo", "n": "Costo de riesgo", "unidad": "pb", "tipo": "costo_riesgo", "paso": 10, "rango": [-40, 60],
             "porque": "Calidad de la cartera: cada punto base de pérdidas esperadas sale directo de la utilidad."},
            {"id": "cartera", "n": "Crecimiento de la cartera", "unidad": "pp", "tipo": "cartera", "spread": 0.04, "paso": 1, "rango": [-5, 5],
             "porque": "Volumen de crédito."},
        ]
    if grupo == "seguros":
        return [{"id": "siniestralidad", "n": "Índice de siniestralidad", "unidad": "pp", "tipo": "siniestralidad", "paso": 1, "rango": [-4, 4],
                 "porque": "Cada punto de siniestralidad sobre las primas devengadas sale de la utilidad técnica."}]
    if grupo == "etf":
        return []
    out = [
        {"id": "ingresos", "n": "Ingresos (volumen y precio)", "unidad": "%", "tipo": "ingresos", "peso": 1, "paso": 2, "rango": [-10, 10],
         "porque": "Crecimiento de las ventas con la estructura de costos actual."},
        {"id": "margen", "n": "Margen UAFIDA", "unidad": "pb", "tipo": "margen", "peso": 1, "paso": 50, "rango": [-200, 200],
         "porque": "Precio, mezcla y costos de insumos."},
    ]
    if moneda == "USD":
        out.append({"id": "fx", "n": "Tipo de cambio (dólar en pesos)", "unidad": "%", "tipo": "fx", "peso": 1.0, "paso": 5, "rango": [-10, 10],
                    "porque": "Reporta en dólares: el precio en pesos se mueve con el tipo de cambio."})
    return out


def margen_incremental(d: dict, grupo: str, b: dict, sector: dict) -> tuple[float | None, str]:
    if num(d.get("margen_incremental")) is not None:
        return float(d["margen_incremental"]), "supuesto del equipo (drivers.json)"
    s = sector.get(grupo) or {}
    if num(s.get("margen_incremental")) is not None:
        return float(s["margen_incremental"]), f"supuesto del sector {grupo}"
    if num(s.get("factor_incremental")) is not None and b.get("margen_bruto"):
        return b["margen_bruto"] * float(s["factor_incremental"]), (f"margen bruto {b['margen_bruto']:.0%} × {float(s['factor_incremental']):.0%} "
                                                                    "(lo que no se va en gastos variables)")
    if b.get("margen_bruto"):
        return b["margen_bruto"] * 0.6, f"margen bruto {b['margen_bruto']:.0%} × 60%"
    return None, "sin margen bruto"


def elasticidad(d: dict, grupo: str, b: dict, sector: dict, macro_ult: dict, usd: float | None, impuestos: float) -> dict:
    """Cambio porcentual en la base (UAFIDA o utilidad) por UNA unidad del driver, con su fórmula."""
    tipo, out = d.get("tipo"), {}
    m = b.get("margen_uafida")
    peso = num(d.get("peso")) if num(d.get("peso")) is not None else 1.0
    e, formula = None, ""
    if tipo == "ingresos":
        mi, nota = margen_incremental(d, grupo, b, sector)
        if mi is not None and m:
            e = peso * mi / m / 100
            formula = f"1% de ingresos × peso {peso:.0%} × margen incremental {mi:.0%} ÷ margen UAFIDA {m:.1%}"
            out["margen_incremental"], out["margen_incremental_nota"] = mi, nota
    elif tipo == "margen":
        if m:
            e = peso / m / 10000
            formula = f"1 pb × peso {peso:.0%} ÷ margen UAFIDA {m:.1%}"
    elif tipo in ("uafida_segmento", "fx"):
        e = peso / 100
        formula = f"1% × participación en la UAFIDA {peso:.0%}"
    elif tipo in ("precio_volumen", "costo_unitario"):
        vol = num(d.get("volumen"))
        u = b.get("uafida_udm")
        if u and b.get("moneda_uafida") != d.get("moneda", "USD") and usd:
            u = u / usd if b.get("moneda_uafida") == "MXN" else u * usd
        if vol and u:
            if tipo == "precio_volumen":
                p = num(macro_ult.get(d.get("serie"))) if d.get("serie") else None
                p = p or num(d.get("precio_base"))
                fuga = num(d.get("fuga")) or 0
                if p:
                    e = 0.01 * p * vol * (1 - fuga) / 1e6 / u
                    out["precio_usado"] = p
                    formula = (f"1% × {p:,.2f} × {vol / 1e6:,.1f} M de unidades × (1 − {fuga:.0%}) ÷ UAFIDA UDM {u:,.0f} M")
            else:
                e = -vol / 1e6 / u
                formula = f"−1 {d.get('unidad', '')} × {vol / 1e6:,.1f} M de unidades ÷ UAFIDA UDM {u:,.0f} M"
    elif tipo in ("min", "costo_riesgo"):
        c, u = b.get("cartera"), b.get("utilidad")
        if c and u:
            e = (1 if tipo == "min" else -1) * 1e-4 * c * (1 - impuestos) / u
            formula = f"{'+' if tipo == 'min' else '−'}1 pb × cartera {c:,.0f} mdp × (1 − {impuestos:.0%}) ÷ utilidad {u:,.0f} mdp"
    elif tipo == "cartera":
        c, u, sp = b.get("cartera"), b.get("utilidad"), num(d.get("spread")) or 0.04
        if c and u:
            e = 0.01 * c * sp * (1 - impuestos) / u
            formula = f"1% de cartera {c:,.0f} mdp × margen neto {sp:.1%} × (1 − {impuestos:.0%}) ÷ utilidad {u:,.0f} mdp"
    elif tipo == "siniestralidad":
        pr, u = b.get("primas"), b.get("utilidad")
        if pr and u:
            e = -0.01 * pr * (1 - impuestos) / u
            formula = f"−1 pp × primas {pr:,.0f} mdp × (1 − {impuestos:.0%}) ÷ utilidad {u:,.0f} mdp"
    out["base"] = e
    out["formula"] = formula
    return out


def modelo_emisora(t: str, grupo: str, kp: dict, info: dict, precio: float | None, usd: float | None,
                   est: dict | None, cfg: dict, macro_ult: dict) -> dict:
    conf = (cfg.get("emisoras") or {}).get(t) or {}
    sector = cfg.get("sector") or {}
    impuestos = num(cfg.get("impuestos")) or 0.30
    b = base_valuacion(t, grupo, kp, info, precio, usd, est, conf)
    ds = conf.get("drivers") or drivers_por_defecto(grupo, b.get("moneda_reporte") or "MXN")
    salida = []
    L = b.get("L")
    aplica = b["tipo"] == "utilidad" or (b.get("margen_uafida") and L and 0.5 < L < 4)
    for d in ds:
        el = elasticidad(d, grupo, b, sector, macro_ult, usd, impuestos)
        e_base = el.get("base")
        e_precio = None
        if e_base is not None and aplica:
            e_precio = e_base * (L if b["tipo"] == "uafida" else 1.0)
        paso = num(d.get("paso")) or 1
        fila = {k: v for k, v in d.items() if k not in ("volumen",)}
        fila.update({"e_base": e_base, "e_precio": e_precio, "formula": el.get("formula"),
                     "efecto_paso": e_precio * paso if e_precio is not None else None,
                     "precio_paso": precio * (1 + e_precio * paso) if (e_precio is not None and precio) else None})
        for k in ("margen_incremental", "margen_incremental_nota", "precio_usado"):
            if k in el:
                fila[k] = el[k]
        if d.get("volumen"):
            fila["volumen_m"] = num(d["volumen"]) / 1e6
        salida.append(fila)
    nota = None
    if not aplica:
        nota = ("El modelo fundamental no aplica: la UAFIDA es muy baja o negativa, o el apalancamiento del capital es extremo. "
                "Use la sensibilidad empírica.")
    return {"base": b, "drivers": salida, "segmentos": conf.get("segmentos"), "configurado": bool(conf), "nota": nota}


# ───────────────────────────── betas empíricas ─────────────────────────────

def _semanal(fechas: list[str], valores: list) -> dict[tuple, float]:
    """Último dato de cada semana ISO."""
    out: dict[tuple, float] = {}
    for f, v in zip(fechas, valores):
        x = num(v)
        if x is None or x <= 0:
            continue
        y, w, _ = date.fromisoformat(f).isocalendar()
        out[(y, w)] = x
    return out


def _ols(y: list[float], xs: list[list[float]]) -> dict | None:
    """Mínimos cuadrados con constante. Devuelve coeficientes, errores estándar y R²."""
    n, k = len(y), len(xs) + 1
    if n < k + 10:
        return None
    X = [[1.0] + [x[i] for x in xs] for i in range(n)]
    xtx = [[sum(X[r][a] * X[r][b_] for r in range(n)) for b_ in range(k)] for a in range(k)]
    xty = [sum(X[r][a] * y[r] for r in range(n)) for a in range(k)]
    inv = _inversa(xtx)
    if inv is None:
        return None
    beta = [sum(inv[a][b_] * xty[b_] for b_ in range(k)) for a in range(k)]
    res = [y[r] - sum(beta[a] * X[r][a] for a in range(k)) for r in range(n)]
    sse = sum(e * e for e in res)
    my = sum(y) / n
    sst = sum((v - my) ** 2 for v in y) or 1e-12
    s2 = sse / (n - k)
    se = [math.sqrt(max(inv[a][a] * s2, 0)) for a in range(k)]
    return {"b": beta, "se": se, "r2": 1 - sse / sst, "n": n}


def _inversa(m: list[list[float]]) -> list[list[float]] | None:
    k = len(m)
    a = [row[:] + [1.0 if i == j else 0.0 for j in range(k)] for i, row in enumerate(m)]
    for c in range(k):
        p = max(range(c, k), key=lambda r: abs(a[r][c]))
        if abs(a[p][c]) < 1e-14:
            return None
        a[c], a[p] = a[p], a[c]
        piv = a[c][c]
        a[c] = [v / piv for v in a[c]]
        for r in range(k):
            if r != c:
                f = a[r][c]
                a[r] = [vr - f * vc for vr, vc in zip(a[r], a[c])]
    return [row[k:] for row in a]


def betas_mercado(cierres: dict, macro: dict, mueve: dict[str, list[str]], semanas: int = 104) -> dict:
    """Sensibilidad semanal de cada emisora al IPC y a cada factor macro (controlando por el IPC)."""
    if not cierres or not cierres.get("d") or "IPC" not in (cierres.get("s") or {}):
        return {}
    d = cierres["d"]
    sem = {t: _semanal(d, s) for t, s in cierres["s"].items()}
    fac = {k: _semanal(macro[k]["d"], macro[k]["c"]) for k in FACTORES if k in macro and macro[k].get("d")}
    claves = sorted(sem["IPC"])[-(semanas + 1):]

    def rend(serie: dict, absoluto: bool = False) -> list[float | None]:
        out = []
        for a, b_ in zip(claves[:-1], claves[1:]):
            x0, x1 = serie.get(a), serie.get(b_)
            out.append(None if not x0 or not x1 else (x1 - x0 if absoluto else x1 / x0 - 1))
        return out

    r_ipc = rend(sem["IPC"])
    r_fac = {k: rend(v, FACTORES[k][1]) for k, v in fac.items()}
    sd_fac = {}
    for k, xs in r_fac.items():
        v = [x for x in xs if x is not None]
        if len(v) > 20:
            mu = sum(v) / len(v)
            sd_fac[k] = math.sqrt(sum((x - mu) ** 2 for x in v) / (len(v) - 1))
    out = {}
    for t, serie in sem.items():
        if t == "IPC":
            continue
        r = rend(serie)
        idx = [i for i in range(len(r)) if r[i] is not None and r_ipc[i] is not None]
        if len(idx) < 40:
            continue
        base = _ols([r[i] for i in idx], [[r_ipc[i] for i in idx]])
        if not base:
            continue
        fila = {"semanas": len(idx), "ipc": {"beta": base["b"][1], "t": base["b"][1] / base["se"][1] if base["se"][1] else None,
                                             "r2": base["r2"]}, "factores": []}
        for k, rf in r_fac.items():
            j = [i for i in idx if rf[i] is not None]
            if len(j) < 40:
                continue
            m2 = _ols([r[i] for i in j], [[r_ipc[i] for i in j], [rf[i] for i in j]])
            m1 = _ols([r[i] for i in j], [[r_ipc[i] for i in j]])
            m0 = _ols([r[i] for i in j], [[rf[i] for i in j]])
            if not m2 or not m1:
                continue
            bf, se = m2["b"][2], m2["se"][2]
            tt = bf / se if se else None
            fila["factores"].append({
                "clave": k, "n": FACTORES[k][0], "absoluto": FACTORES[k][1], "beta": bf, "t": tt,
                "beta_simple": m0["b"][1] if m0 else None, "t_simple": (m0["b"][1] / m0["se"][1]) if m0 and m0["se"][1] else None,
                "r2_simple": m0["r2"] if m0 else None,
                "r2_extra": m2["r2"] - m1["r2"], "sd_factor": sd_fac.get(k),
                "efecto_1sd": bf * sd_fac[k] if k in sd_fac else None,
                "relevante": (t in mueve.get(k, [])) or (tt is not None and abs(tt) >= 2.5),
            })
        fila["factores"].sort(key=lambda x: -abs(x["t"] or 0))
        out[t] = fila
    return out
