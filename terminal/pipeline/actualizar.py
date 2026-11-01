#!/usr/bin/env python3
"""Pipeline de datos de North Star Terminal. Sustituye al vigilante: corre solo en GitHub Actions.

    python terminal/pipeline/actualizar.py --modo rapido     # cotizaciones e intradía (cada 15 min)
    python terminal/pipeline/actualizar.py --modo completo   # todo: velas, estados, KPIs, noticias, macro
    python terminal/pipeline/actualizar.py --modo semilla    # sin red: datos iniciales desde los CSV del repo

Reglas que protegen los datos:
  · Cada símbolo se descarga por separado; si uno falla se conserva lo que ya estaba publicado.
  · Si la cobertura de cotizaciones queda debajo del 50% no se sobrescribe nada.
  · Todo lo que falló queda escrito en estado.json, que la terminal muestra en la barra de estado.
"""
from __future__ import annotations

import argparse
import csv
import io
import logging
import os
import sys
import time
from datetime import date, datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import fichas as F  # noqa: E402
import kpis as K  # noqa: E402
import portafolio as P  # noqa: E402
import universo as U  # noqa: E402
from util import (CDMX, ahora_utc, escribir_json, estado_mercado, etiqueta_trimestre, fecha_cdmx, leer_json,  # noqa: E402
                  limpiar, num)

log = logging.getLogger("terminal")
VERSION = 1


class Corrida:
    def __init__(self, datos: str, modo: str):
        self.datos = os.path.abspath(datos)
        self.modo = modo
        self.inicio = time.time()
        self.errores: list[str] = []
        self.avisos: list[str] = []
        self.cobertura: dict[str, str] = {}
        self.escritos: list[str] = []
        self.fuentes: set[str] = set()

    def ruta(self, *partes: str) -> str:
        return os.path.join(self.datos, *partes)

    def leer(self, nombre: str, defecto=None):
        return leer_json(self.ruta(nombre), defecto)

    def escribir(self, nombre: str, datos, compacto: bool = True):
        if escribir_json(self.ruta(nombre), datos, compacto):
            self.escritos.append(nombre)

    def error(self, texto: str):
        log.warning(texto)
        self.errores.append(texto[:300])


# ───────────────────────────── piezas ─────────────────────────────

def cotizaciones(c: Corrida) -> dict:
    """Cotización e intradía de emisoras e instrumentos macro."""
    import fuente_yahoo as Y
    simbolos = U.mapa_yahoo()
    inverso = {y: t for t, y in simbolos.items()}
    ok, err = Y.en_paralelo(Y.cotizacion_intradia, list(simbolos.values()), hilos=6)
    previo = c.leer("cotizaciones.json", {}) or {}
    q_prev = previo.get("q", {})
    emis = {e["t"] for e in U.emisoras()}
    frescos = {inverso[y]: v for y, v in ok.items()}
    n_emis = sum(1 for t in frescos if t in emis)
    c.cobertura["cotizaciones"] = f"{n_emis}/{len(emis)}"
    for y, e in err.items():
        c.avisos.append(f"cotización {inverso.get(y, y)}: {e}")
    if n_emis < 0.5 * len(emis):
        c.error(f"Cobertura de cotizaciones insuficiente ({n_emis}/{len(emis)}); se conserva lo publicado")
        return q_prev
    c.fuentes.add("Yahoo Finance")
    q = dict(q_prev)
    barras = {}
    for t, v in frescos.items():
        barras[t] = v.pop("barras", [])
        v["c"] = (v["p"] - v["a"]) if v.get("a") else None
        v["cp"] = (v["p"] / v["a"] - 1) if v.get("a") else None
        v["fuente"] = "Yahoo Finance"
        q[t] = limpiar(v)
    for t in q:
        if t not in frescos and t in q_prev:
            q[t]["conservado"] = True
    hoy = max((b[-1][0][:10] for b in barras.values() if b), default=None)
    c.escribir("cotizaciones.json", {"generado": ahora_utc().isoformat(), "q": q})
    if hoy:
        intr = {t: b for t, b in barras.items() if b and b[-1][0][:10] == hoy}
        c.escribir("intradia.json", {"fecha": hoy, "s": intr})
    legado_cotizaciones(c, q)
    return q


def legado_cotizaciones(c: Corrida, q: dict):
    """cotizaciones.csv con el formato del tablero actual (simbolo,precio,anterior,fecha_hora)."""
    emis = [e["t"] for e in U.emisoras()]
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["simbolo", "precio", "anterior", "fecha_hora"])
    for t in sorted(emis):
        v = q.get(t)
        if v and v.get("p"):
            w.writerow([t, f"{v['p']:.4f}", f"{v['a']:.4f}" if v.get("a") else "", v.get("ts") or ""])
    ruta = c.ruta("legado", "cotizaciones.csv")
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    nuevo = buf.getvalue()
    viejo = open(ruta, encoding="utf-8").read() if os.path.exists(ruta) else ""
    if nuevo != viejo:
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(nuevo)
        c.escritos.append("legado/cotizaciones.csv")


def velas(c: Corrida) -> dict[str, dict]:
    import fuente_yahoo as Y
    simbolos = U.mapa_yahoo()
    inverso = {y: t for t, y in simbolos.items()}
    ok, err = Y.en_paralelo(lambda y: Y.velas(y, "5y"), list(simbolos.values()), hilos=5)
    out = {}
    for y, v in ok.items():
        t = inverso[y]
        if len(v["d"]) < 30:
            c.avisos.append(f"velas {t}: solo {len(v['d'])} días; se conserva lo previo")
            continue
        v["fuente"] = "Yahoo Finance"
        out[t] = v
        c.escribir(f"velas/{t}.json", {"t": t, **v})
    for y, e in err.items():
        c.avisos.append(f"velas {inverso.get(y, y)}: {e}")
    c.cobertura["velas"] = f"{len(out)}/{len(simbolos)}"
    # Lo que no llegó se toma del archivo previo (semilla o corrida anterior)
    for t in simbolos:
        if t not in out:
            previo = c.leer(f"velas/{t}.json")
            if previo and previo.get("d"):
                out[t] = previo
    return out


def fundamentales(c: Corrida) -> tuple[dict, dict, dict, dict]:
    import fuente_yahoo as Y
    emis = [e for e in U.emisoras() if e["t"] != "MEXTRAC"]
    ys = [e["y"] for e in emis]
    por_y = {e["y"]: e["t"] for e in emis}
    info_ok, info_err = Y.en_paralelo(Y.info, ys, hilos=4)
    previo = c.leer("fundamentales.json", {}) or {}
    info = dict(previo.get("emisoras", {}))
    for y, v in info_ok.items():
        info[por_y[y]] = v
    for y, e in info_err.items():
        c.avisos.append(f"info {por_y[y]}: {e}")
    c.cobertura["fundamentales"] = f"{len(info_ok)}/{len(ys)}"
    if info_ok:
        c.fuentes.add("Yahoo Finance")
        c.escribir("fundamentales.json", {"generado": ahora_utc().isoformat(), "emisoras": info})

    est_ok, est_err = Y.en_paralelo(Y.estados, ys, hilos=3)
    estados = {}
    for e in emis:
        t, y = e["t"], e["y"]
        if y in est_ok:
            estados[t] = {"t": t, "moneda": (info.get(t) or {}).get("financialCurrency"), "generado": ahora_utc().isoformat(),
                          **est_ok[y]}
            c.escribir(f"estados/{t}.json", estados[t])
        else:
            if y in est_err:
                c.avisos.append(f"estados {t}: {est_err[y]}")
            prev = c.leer(f"estados/{t}.json")
            if prev:
                estados[t] = prev
    c.cobertura["estados"] = f"{len(est_ok)}/{len(ys)}"

    mult_ok, _ = Y.en_paralelo(Y.multiplos_historicos, ys, hilos=3)
    multiplos = {por_y[y]: v for y, v in mult_ok.items()}
    prev_m = (c.leer("multiplos.json", {}) or {}).get("emisoras", {})
    for t, v in prev_m.items():
        multiplos.setdefault(t, v)
    if mult_ok:
        c.escribir("multiplos.json", {"generado": ahora_utc().isoformat(), "emisoras": multiplos})

    ev_ok, _ = Y.en_paralelo(Y.eventos, ys, hilos=3)
    eventos = {por_y[y]: v for y, v in ev_ok.items()}
    return info, estados, multiplos, eventos


def noticias(c: Corrida) -> None:
    import fuente_noticias as N
    items, vistos = [], set()

    def agregar(x: dict, t: str, origen: str):
        k = N.clave_titulo(x["titulo"])
        if k in vistos:
            return
        vistos.add(k)
        try:
            dt = datetime.fromisoformat(str(x["fecha_utc"]).replace("Z", "+00:00"))
            fecha = dt.astimezone(CDMX).strftime("%Y-%m-%d %H:%M")
        except ValueError:
            fecha = str(x.get("fecha_utc", ""))[:16].replace("T", " ")
        tono = x.get("tono") or N.tono(x["titulo"])[0]
        items.append({"id": f"{origen}:{k}", "fecha": fecha, "t": t, "titulo": x["titulo"], "fuente": x.get("fuente", ""),
                      "url": x.get("url", ""), "tono": tono, "impacto": "", "resumen": x.get("resumen", ""),
                      "origen": origen, "tono_auto": True})

    # Primero las del equipo: tienen prioridad cuando el titular se repite.
    for n in F.leer_noticias_equipo():
        k = N.clave_titulo(n["titulo"])
        if k not in vistos:
            vistos.add(k)
            items.append(n)
    ok_g = 0
    for e in U.emisoras(incluir_etf=False):
        try:
            for x in N.buscar(e["q"], dias=30, maximo=10, filtrar=N.palabras_clave(e["q"])):
                agregar(x, e["t"], "google")
            ok_g += 1
        except Exception as ex:
            c.avisos.append(f"noticias {e['t']}: {type(ex).__name__}")
        time.sleep(0.6)
    for q in N.MERCADO:
        try:
            for x in N.buscar(q, dias=7, maximo=12):
                agregar(x, "MERCADO", "google")
        except Exception as ex:
            c.avisos.append(f"noticias mercado: {type(ex).__name__}")
    c.cobertura["noticias"] = f"{ok_g}/{len(U.EMISORAS)}"
    if ok_g:
        c.fuentes.add("Google Noticias")
    if ok_g == 0:
        previo = (c.leer("noticias.json", {}) or {}).get("items", [])
        auto = [n for n in previo if n.get("origen") in ("google", "yahoo")]
        for n in auto:
            k = N.clave_titulo(n["titulo"])
            if k not in vistos:
                vistos.add(k)
                items.append(n)
    limite = (date.today() - timedelta(days=120)).isoformat()
    items = [n for n in items if (n.get("fecha") or "") >= limite or n.get("origen") == "equipo"]
    items.sort(key=lambda n: n.get("fecha") or "", reverse=True)
    c.escribir("noticias.json", {"generado": ahora_utc().isoformat(), "items": items[:1500]})


def macro_banxico(c: Corrida, macro: dict) -> None:
    import fuente_banxico as B
    if not os.environ.get("BANXICO_TOKEN"):
        return
    try:
        datos = B.series([s for (_, s, _, _) in U.BANXICO])
    except Exception as e:
        c.avisos.append(f"Banxico: {type(e).__name__}: {str(e)[:100]}")
        return
    for clave, serie, nombre, unidad in U.BANXICO:
        puntos = datos.get(serie)
        if not puntos:
            continue
        if clave == "INPC":       # inflación anual a partir del índice mensual
            idx = dict(puntos)
            fechas = sorted(idx)
            infl = []
            for f in fechas:
                y, m, d = f.split("-")
                f0 = f"{int(y) - 1}-{m}-{d}"
                if f0 in idx:
                    infl.append([f, (idx[f] / idx[f0] - 1) * 100])
            if infl:
                macro["INFLACION"] = {"n": "Inflación anual (INPC)", "u": "%", "tipo": "tasa", "mueve": [],
                                      "d": [p[0] for p in infl], "c": [round(p[1], 3) for p in infl], "fuente": "Banxico"}
            continue
        macro[clave] = {"n": nombre, "u": unidad, "tipo": "tasa" if unidad == "%" else "divisa", "mueve": [],
                        "d": [p[0] for p in puntos], "c": [p[1] for p in puntos], "fuente": "Banxico"}
    c.fuentes.add("Banxico")


# ───────────────────────────── derivados ─────────────────────────────

def armar_cierres(v: dict[str, dict], sesiones: int = 520) -> dict:
    """Matriz de cierres alineados (emisoras + IPC) para comparativos, correlaciones y riesgo."""
    claves = [e["t"] for e in U.emisoras()] + ["IPC"]
    fechas = set()
    for t in claves:
        if t in v:
            fechas.update(v[t]["d"][-sesiones - 30:])
    fechas = sorted(fechas)[-sesiones:]
    series = {}
    for t in claves:
        if t not in v:
            continue
        m = dict(zip(v[t]["d"], v[t]["c"]))
        previo, fila = None, []
        for f in fechas:
            x = m.get(f)
            if x is None:
                x = previo                      # día sin cierre: se arrastra el último
            fila.append(x)
            if x is not None:
                previo = x
        series[t] = fila
    return {"d": fechas, "s": series}


def armar_macro(v: dict[str, dict], previo: dict) -> dict:
    out = dict(previo or {})
    for (clave, _y, nombre, tipo, unidad, mueve) in U.MACRO:
        if clave in v:
            d, c = v[clave]["d"][-520:], v[clave]["c"][-520:]
            out[clave] = {"n": nombre, "u": unidad, "tipo": tipo, "mueve": mueve, "d": d, "c": c,
                          "fuente": v[clave].get("fuente", "Yahoo Finance")}
    return out


def sumar_sesion(vt: dict, cot: dict | None) -> dict:
    """Agrega a las velas la sesión de la cotización si es posterior al último cierre guardado."""
    p = num((cot or {}).get("p"))
    ts = (cot or {}).get("ts")
    if not p or not ts:
        return vt
    try:
        dia = fecha_cdmx(datetime.fromisoformat(str(ts).replace("Z", "+00:00")))
    except ValueError:
        return vt
    if dia <= vt["d"][-1]:
        return vt
    vols = list(vt.get("v") or [])
    return {**vt, "d": vt["d"] + [dia], "c": vt["c"] + [p],
            "v": vols + [int(num((cot or {}).get("v")) or 1)] if vols else vols}


def dividendos_12m(v: dict | None, hoy: date) -> float | None:
    if not v or not v.get("div"):
        return None
    limite, hoy_s = (hoy - timedelta(days=365)).isoformat(), hoy.isoformat()
    return sum(x[1] for x in v["div"] if limite < x[0] <= hoy_s) or None


def armar_kpis(c: Corrida, v: dict, info: dict, estados: dict, multiplos: dict, fichas: dict, q: dict) -> dict:
    emis = U.emisoras()
    usd = num((q.get("USDMXN") or {}).get("p"))
    if usd is None and "USDMXN" in v:
        usd = v["USDMXN"]["c"][-1]
    ref = dict(zip(v["IPC"]["d"], v["IPC"]["c"])) if "IPC" in v else None
    cetes = (U.leer_parametros() or {}).get("cetes28")
    hoy = date.today()
    por_emisora, salida = {}, {}
    for e in emis:
        t, g = e["t"], e["grupo"]
        inf, est = info.get(t) or {}, estados.get(t)
        precio = num((q.get(t) or {}).get("p")) or (v[t]["c"][-1] if t in v else None)
        fx = 1.0
        if inf.get("financialCurrency") and inf.get("currency") and inf["financialCurrency"] != inf["currency"]:
            if inf["financialCurrency"] == "USD" and inf["currency"] == "MXN" and usd:
                fx = usd
            else:
                c.avisos.append(f"kpis {t}: moneda de reporte {inf['financialCurrency']} sin conversión")
        fin = K.financieros(t, g, est, inf, precio, fx) if t != "MEXTRAC" else []
        val = K.valuacion(t, g, est, inf, precio, fx, dividendos_12m(v.get(t), hoy), multiplos.get(t)) if t != "MEXTRAC" else []
        mer = K.mercado(t, v.get(t), ref, cetes)
        por_emisora[t] = fin + val + mer
        per_q = ((est or {}).get("resultados", {}).get("trimestral", {}) or {}).get("periodos") or []
        salida[t] = {
            "grupo": g, "grupo_n": U.GRUPOS.get(g, g),
            "ultimo_trimestre": etiqueta_trimestre(per_q[K.ultimo_valido(est)]) if per_q and K.ultimo_valido(est) is not None else None,
            "moneda_reporte": inf.get("financialCurrency"),
            "operativos": (fichas.get(t) or {}).get("kpis", []),
            "factores_equipo": (fichas.get(t) or {}).get("factores_z"),
        }
    pares = {e["t"]: U.pares_de(e["t"]) for e in emis}
    K.comparar(por_emisora, pares)
    qvm = K.factores_qvm({t: ks for t, ks in por_emisora.items() if t != "MEXTRAC"})
    # Lo descriptivo (nombre, fórmula, para qué sirve) va una sola vez en «definiciones».
    defs: dict[str, dict] = {}
    estaticos = ("nombre", "unidad", "familia", "formula", "que", "mejor")
    for t, ks in por_emisora.items():
        valores = []
        for k in ks:
            d = defs.setdefault(k["clave"], {c: k.get(c) for c in estaticos})
            fila = {c: v_ for c, v_ in k.items() if c not in estaticos and v_ not in (None, [], {})}
            if k.get("formula") and k["formula"] != d.get("formula"):
                fila["formula"] = k["formula"]
            if num(k.get("valor")) is None and not k.get("serie"):
                continue
            valores.append(fila)
        salida[t]["kpis"] = valores
        salida[t]["qvm"] = qvm.get(t)
        salida[t]["pares"] = pares.get(t, [])
    return {"generado": ahora_utc().isoformat(), "definiciones": defs, "catalogo": K.CATALOGO, "grupos": U.GRUPOS,
            "familias": K.FAMILIAS, "emisoras": salida}


def armar_calendario(eventos: dict) -> dict:
    out = []
    for r in F.leer_csv("calendario.csv"):
        if r.get("fecha"):
            out.append({"fecha": r["fecha"], "t": r.get("emisora", ""), "tipo": r.get("tipo", ""),
                        "titulo": r.get("titulo", ""), "fuente": r.get("fuente", "equipo")})
    vistos = {(x["fecha"], x["t"], x["tipo"]) for x in out}
    limite = (date.today() - timedelta(days=45)).isoformat()      # Yahoo deja la última fecha aunque sea vieja
    for t, ev in (eventos or {}).items():
        for f in ev.get("reporte") or []:
            if f >= limite and (f, t, "Reporte trimestral") not in vistos:
                out.append({"fecha": f, "t": t, "tipo": "Reporte trimestral", "titulo": "Reporte de resultados (fecha estimada por Yahoo)",
                            "fuente": "Yahoo Finance"})
        if ev.get("ex_dividendo") and ev["ex_dividendo"] >= limite:
            out.append({"fecha": ev["ex_dividendo"], "t": t, "tipo": "Dividendo", "titulo": "Fecha ex-dividendo",
                        "fuente": "Yahoo Finance"})
    out.sort(key=lambda x: x["fecha"])
    return {"generado": ahora_utc().isoformat(), "eventos": out,
            "analistas": {t: {k: ev.get(k) for k in ("recomendaciones", "objetivo", "upa_estimada", "ventas_estimadas") if ev.get(k)}
                          for t, ev in (eventos or {}).items()}}


def armar_portafolio(c: Corrida, v: dict, q: dict) -> None:
    par = U.leer_parametros()
    ops = F.leer_csv("operaciones.csv")
    if not ops or not par.get("capital"):
        return
    cap, ref = float(par["capital"]), par.get("fecha_referencia") or par.get("inicio")
    pesos = par.get("pesos_indice", {})
    tickers = {o["simbolo"] for o in ops} | set(pesos) | {"MEXTRAC"}
    cierres: dict[str, dict] = {}
    sin_op: set[str] = set()
    inicio = par.get("inicio") or ref
    for t in tickers:
        vt = v.get(t)
        if not vt:
            continue
        vols = vt.get("v") or []
        for i, (f, x) in enumerate(zip(vt["d"], vt["c"])):
            if f >= (date.fromisoformat(inicio) - timedelta(days=10)).isoformat():
                cierres.setdefault(f, {})[t] = x
                if t == "MEXTRAC" and vt.get("fuente", "").startswith("Yahoo") and i < len(vols) and vols[i] == 0:
                    sin_op.add(f)
    # Los días que ya registró el tracker se valúan con sus cierres oficiales de Refinitiv (historico.csv), para que
    # la serie cuadre al centavo con rendimientos.csv; los días posteriores, con las velas de Yahoo.
    oficiales = {r["fecha"]: r for r in F.leer_csv("historico.csv") if r.get("fecha", "") >= inicio}
    for f, fila in oficiales.items():
        cierres[f] = {t: num(fila.get(t)) for t in tickers if num(fila.get(t)) is not None}
        if num(fila.get("MEXTRAC")) is None:
            sin_op.add(f)
        else:
            sin_op.discard(f)
    hoy = fecha_cdmx(ahora_utc())
    serie = P.serie_diaria(ops, cierres, cap, ref, pesos, sin_op)
    mercado = estado_mercado(feriados=par.get("feriados", []))
    for fila in serie:
        fila["estado"] = "en curso" if fila["f"] == hoy and mercado["estado"] == "abierto" else "cierre"
    bloques = par.get("bloques", {})
    foto = P.foto_actual(ops, cap, q, pesos, bloques, hoy)
    mex = q.get("MEXTRAC") or {}
    foto["bench_dia"] = mex.get("cp")
    if foto.get("rend_dia") is not None and mex.get("cp") is not None:
        foto["activo_dia"] = foto["rend_dia"] - mex["cp"]
    c.escribir("portafolio.json", limpiar({
        "generado": ahora_utc().isoformat(), "capital": cap, "inicio": inicio, "referencia": ref,
        "fin": par.get("fin"), "benchmark": "MEXTRAC", "modelo": par.get("modelo"),
        "operaciones": len(ops), "ultima_operacion": max((o.get("fecha") or "") for o in ops),
        "actual": foto, "serie": serie,
        "politica": {"te_max": 0.10, "beta": [0.70, 1.30], "efectivo": [0.0, 0.05], "pasiva": [0.40, 0.60],
                     "desviacion_max_pp": 10},
    }))


# ───────────────────────────── semilla (sin red) ─────────────────────────────

def semilla(c: Corrida) -> tuple[dict, dict]:
    """Datos iniciales con lo último que bajó el vigilante desde Refinitiv (CSV del repo)."""
    hist = F.leer_csv("historico.csv")
    ohlc = {}
    for r in F.leer_csv("ohlc.csv"):
        ohlc[(r["fecha"], r["emisora"])] = r
    v: dict[str, dict] = {}
    claves = [e["t"] for e in U.emisoras()] + ["IPC"]
    for t in claves:
        d, o, h, l, cc, vol = [], [], [], [], [], []
        for r in hist:
            x = num(r.get(t))
            if x is None:
                continue
            f = r["fecha"]
            k = ohlc.get((f, t), {})
            d.append(f)
            cc.append(x)
            o.append(num(k.get("apertura")) or x)
            h.append(num(k.get("maximo")) or x)
            l.append(num(k.get("minimo")) or x)
            vol.append(0)
        if d:
            divs = [[r["fecha_ex"], float(r["dividendo"])] for r in F.leer_csv("dividendos_historicos.csv")
                    if r.get("simbolo") == t and num(r.get("dividendo"))]
            v[t] = {"d": d, "o": o, "h": h, "l": l, "c": cc, "v": vol, "div": sorted(divs), "split": [],
                    "fuente": "LSEG Refinitiv (semilla)"}
            if t != "IPC":
                c.escribir(f"velas/{t}.json", {"t": t, **v[t]})
    if "IPC" in v:
        c.escribir("velas/IPC.json", {"t": "IPC", **v["IPC"]})
    # Macro de Refinitiv
    mapa = {"USD": "USDMXN", "EUR": "EURMXN", "BRL": "BRLMXN", "COBRE": "COBRE", "ORO": "ORO", "PLATA": "PLATA",
            "BRENT": "BRENT", "UST10": "UST10", "SP500": "SP500", "BOVESPA": "BOVESPA", "MBONO10": "MBONO10"}
    meta = {cl: (n, tipo, u, mv) for (cl, _y, n, tipo, u, mv) in U.MACRO}
    meta["MBONO10"] = ("Bono M a 10 años", "tasa", "%", ["GFNORTEO", "BBAJIOO", "GFINBURO", "RA"])
    series: dict[str, dict] = {}
    for r in F.leer_csv("macro.csv"):
        clave = mapa.get(r.get("serie"))
        x = num(r.get("valor"))
        if clave and x is not None:
            series.setdefault(clave, {})[r["fecha"]] = x
    macro = {}
    for clave, puntos in series.items():
        n, tipo, u, mv = meta[clave]
        fechas = sorted(puntos)
        macro[clave] = {"n": n, "u": u, "tipo": tipo, "mueve": mv, "d": fechas, "c": [puntos[f] for f in fechas],
                        "fuente": "LSEG Refinitiv (semilla)"}
        v[clave] = {"d": fechas, "c": [puntos[f] for f in fechas]}
    if "IPC" in v:
        n, tipo, u, mv = meta["IPC"]
        macro["IPC"] = {"n": n, "u": u, "tipo": tipo, "mueve": mv, "d": v["IPC"]["d"][-520:], "c": v["IPC"]["c"][-520:],
                        "fuente": "LSEG Refinitiv (semilla)"}
    # Cotizaciones: último corte del vigilante
    q = {}
    for r in F.leer_csv("cotizaciones.csv"):
        p, a = num(r.get("precio")), num(r.get("anterior"))
        if p:
            q[r["simbolo"]] = limpiar({"p": p, "a": a, "c": p - a if a else None, "cp": p / a - 1 if a else None,
                                       "ts": r.get("fecha_hora"), "m": "MXN", "fuente": "LSEG Refinitiv (semilla)"})
    for clave in ("IPC", "USDMXN", "EURMXN", "BRLMXN", "COBRE", "ORO", "PLATA", "BRENT", "UST10", "SP500", "BOVESPA"):
        s = macro.get(clave)
        if s and len(s["c"]) >= 2:
            q[clave] = limpiar({"p": s["c"][-1], "a": s["c"][-2], "c": s["c"][-1] - s["c"][-2],
                                "cp": s["c"][-1] / s["c"][-2] - 1, "ts": s["d"][-1], "fuente": s["fuente"]})
    # Intradía
    intr, fecha_intr = {}, None
    filas = F.leer_csv("intradia.csv")
    if filas:
        fecha_intr = max(r["fecha_hora"][:10] for r in filas)
        for r in filas:
            if r["fecha_hora"][:10] != fecha_intr:
                continue
            ts = r["fecha_hora"].replace("+00:00", "Z")
            for t, x in r.items():
                if t != "fecha_hora" and num(x):
                    intr.setdefault(t, []).append([ts, float(x), 0])
    c.escribir("cotizaciones.json", {"generado": ahora_utc().isoformat(), "q": q, "semilla": True})
    if intr:
        c.escribir("intradia.json", {"fecha": fecha_intr, "s": intr})
    c.escribir("macro.json", {"generado": ahora_utc().isoformat(), "series": macro})
    c.fuentes.add("LSEG Refinitiv (semilla)")
    return v, q


# ───────────────────────────── principal ─────────────────────────────

def correr(modo: str, datos: str) -> int:
    c = Corrida(datos, modo)
    os.makedirs(c.datos, exist_ok=True)
    fichas = F.leer_fichas()
    c.escribir("universo.json", U.universo_json(fichas), compacto=False)
    c.escribir("fichas.json", {"generado": ahora_utc().isoformat(), "emisoras": fichas})
    par = U.leer_parametros()
    mercado = estado_mercado(feriados=par.get("feriados", []))

    v: dict = {}
    q: dict = {}
    if modo == "semilla":
        v, q = semilla(c)
        v = {t: sumar_sesion(x, q.get(t)) for t, x in v.items()}
        info, estados, multiplos, eventos = {}, {}, {}, {}
        c.escribir("cierres.json", armar_cierres(v))
        c.escribir("kpis.json", armar_kpis(c, v, info, estados, multiplos, fichas, q))
        c.escribir("calendario.json", armar_calendario({}))
        noticias_semilla(c)
        armar_portafolio(c, v, q)
    else:
        try:
            q = cotizaciones(c)
        except Exception as e:
            c.error(f"cotizaciones: {type(e).__name__}: {e}")
            q = (c.leer("cotizaciones.json", {}) or {}).get("q", {})
        if modo == "completo":
            try:
                v = velas(c)
            except Exception as e:
                c.error(f"velas: {type(e).__name__}: {e}")
            if not v:
                v = {t: x for t in U.mapa_yahoo() if (x := c.leer(f"velas/{t}.json"))}
            c.escribir("cierres.json", armar_cierres(v))
            macro = armar_macro(v, (c.leer("macro.json", {}) or {}).get("series", {}))
            macro_banxico(c, macro)
            c.escribir("macro.json", {"generado": ahora_utc().isoformat(), "series": macro})
            try:
                info, estados, multiplos, eventos = fundamentales(c)
            except Exception as e:
                c.error(f"fundamentales: {type(e).__name__}: {e}")
                info = (c.leer("fundamentales.json", {}) or {}).get("emisoras", {})
                estados = {}
                for em in U.emisoras():
                    previo_est = c.leer(f"estados/{em['t']}.json")
                    if previo_est:
                        estados[em["t"]] = previo_est
                multiplos = (c.leer("multiplos.json", {}) or {}).get("emisoras", {})
                eventos = {}
            c.escribir("kpis.json", armar_kpis(c, v, info, estados, multiplos, fichas, q))
            if eventos:
                c.escribir("calendario.json", armar_calendario(eventos))
            try:
                noticias(c)
            except Exception as e:
                c.error(f"noticias: {type(e).__name__}: {e}")
        else:
            # Modo rápido: velas del archivo más la sesión de la última cotización, para la serie del portafolio.
            v = {}
            for t in U.mapa_yahoo():
                vt = c.leer(f"velas/{t}.json")
                if vt and vt.get("d"):
                    v[t] = sumar_sesion(vt, q.get(t))
        try:
            armar_portafolio(c, v, q)
        except Exception as e:
            c.error(f"portafolio: {type(e).__name__}: {e}")

    previo = c.leer("estado.json", {}) or {}
    estado = {
        "version": VERSION,
        "generado": ahora_utc().isoformat(),
        "modo": modo,
        "mercado": mercado,
        "fuentes": sorted(c.fuentes),
        "cobertura": c.cobertura,
        "errores": c.errores,
        "avisos": c.avisos[:80],
        "n_avisos": len(c.avisos),
        "duracion_s": round(time.time() - c.inicio, 1),
        "escritos": len(c.escritos),
        "ultimo_completo": ahora_utc().isoformat() if modo in ("completo", "semilla") else previo.get("ultimo_completo"),
        "ultimo_rapido": ahora_utc().isoformat() if modo in ("rapido", "completo") else previo.get("ultimo_rapido"),
        "origen": os.environ.get("GITHUB_RUN_ID") and f"GitHub Actions · corrida {os.environ.get('GITHUB_RUN_ID')}" or "local",
    }
    escribir_json(c.ruta("estado.json"), estado, compacto=False)
    log.info("Modo %s · %d archivos actualizados · %d avisos · %d errores · %.1fs",
             modo, len(c.escritos), len(c.avisos), len(c.errores), estado["duracion_s"])
    for a in c.avisos[:40]:
        log.info("aviso: %s", a)
    return 0


def noticias_semilla(c: Corrida):
    items = F.leer_noticias_equipo()
    items.sort(key=lambda n: n.get("fecha") or "", reverse=True)
    c.escribir("noticias.json", {"generado": ahora_utc().isoformat(), "items": items})


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--modo", choices=["rapido", "completo", "semilla"], default="rapido")
    ap.add_argument("--datos", default=os.path.join(U.RAIZ, "terminal", "datos"),
                    help="carpeta de salida (en Actions, la copia de la rama de datos)")
    ap.add_argument("-v", "--detalle", action="store_true")
    a = ap.parse_args()
    logging.basicConfig(level=logging.DEBUG if a.detalle else logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S")
    return correr(a.modo, a.datos)


if __name__ == "__main__":
    sys.exit(main())
