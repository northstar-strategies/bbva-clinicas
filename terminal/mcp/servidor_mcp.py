#!/usr/bin/env python3
"""Servidor MCP de North Star Terminal.

Expone los datos de la terminal (los mismos JSON que publica GitHub Actions en la rama
«datos») como herramientas para Claude Desktop, Claude Code o cualquier cliente MCP.
Solo usa la biblioteca estándar: no hay que instalar nada.

    claude mcp add north-star -- python3 terminal/mcp/servidor_mcp.py
    python3 terminal/mcp/servidor_mcp.py --local terminal/datos      # copia local de los datos
    python3 terminal/mcp/servidor_mcp.py --repo usuario/otro-repo    # otro repositorio

Transporte: stdio con JSON-RPC 2.0 (un mensaje por línea), como pide la especificación MCP.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import unicodedata
import urllib.request
from datetime import datetime, timedelta, timezone

VERSIONES = ["2025-11-25", "2025-06-18", "2025-03-26", "2024-11-05"]
REPO = "northstar-strategies/bbva-clinicas"
TTL = 300  # segundos que se reutiliza un archivo descargado

INSTRUCCIONES = (
    "Datos de North Star Terminal: las 37 emisoras de la BMV que analiza el Fondo de Inversión ITESM-BBVA "
    "(North Star Strategies) y el ETF MEXTRAC 09, su índice de referencia. Las claves de emisora son las de la BMV "
    "(FEMSAUBD, GMEXICOB, GFNORTEO...). Si el usuario da un nombre, usa buscar_emisora primero. Los porcentajes vienen "
    "en fracción (0.123 = 12.3%) salvo donde se indique. UDM = últimos doce meses. Responde en español."
)


# ───────────────────────────── datos ─────────────────────────────

class Datos:
    def __init__(self, local: str | None, repo: str):
        self.local = local
        self.base = f"https://raw.githubusercontent.com/{repo}/datos/terminal/datos/"
        self._cache: dict[str, tuple[float, object]] = {}

    def json(self, nombre: str):
        ahora = time.time()
        if nombre in self._cache and ahora - self._cache[nombre][0] < TTL:
            return self._cache[nombre][1]
        if self.local:
            with open(os.path.join(self.local, nombre), encoding="utf-8") as f:
                datos = json.load(f)
        else:
            req = urllib.request.Request(self.base + nombre, headers={"User-Agent": "NorthStarTerminal-MCP/1.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                datos = json.load(r)
        self._cache[nombre] = (ahora, datos)
        return datos

    def opcional(self, nombre: str, defecto=None):
        """Archivos que pueden no existir todavía (p. ej. antes de la primera corrida completa)."""
        try:
            return self.json(nombre)
        except Exception:
            return defecto if defecto is not None else {}

    def universo(self) -> list[dict]:
        return self.json("universo.json")["emisoras"]

    def U(self) -> dict[str, dict]:
        return {e["t"]: e for e in self.universo()}

    def q(self) -> dict:
        return self.json("cotizaciones.json").get("q", {})

    def kpis(self) -> dict:
        return self.json("kpis.json")


def _plano(s: str) -> str:
    s = unicodedata.normalize("NFD", str(s).lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def resolver(d: Datos, texto: str) -> str:
    """Clave BMV a partir de una clave o un nombre ('femsa' → FEMSAUBD)."""
    t = str(texto or "").strip().upper().replace(".MX", "")
    U = d.U()
    if t in U:
        return t
    alias = {"PE&OLES": "PEOLES", "PENOLES": "PEOLES", "PEÑOLES": "PEOLES", "LIVEPOLC-1": "LIVEPOLC1", "MEXTRAC09": "MEXTRAC"}
    if t in alias:
        return alias[t]
    q = _plano(texto)
    for e in U.values():
        if e["t"].startswith(t) or _plano(e["n"]).startswith(q) or q in _plano(e.get("nombre", "")):
            return e["t"]
    raise ValueError(f"No reconozco la emisora «{texto}». Usa buscar_emisora para ver las opciones.")


# ───────────────────────────── formato ─────────────────────────────

def fuente(s) -> str:
    """Etiqueta pública de la fuente (los datos ya publicados pueden traer el nombre del agregador)."""
    import re
    return re.sub(r"Yahoo Finance|Yahoo", "Mercado · diferido", str(s or ""), flags=re.I)


def pb(x, d=1):
    return "n/d" if x is None else f"{x * 1e4:+.{d}f} pb"


def pct(x, d=2):
    return "n/d" if x is None else f"{x * 100:+.{d}f}%"


def kfmt(v, unidad, moneda=None):
    if v is None:
        return "n/d"
    if unidad == "%":
        return f"{v * 100:.1f}%"
    if unidad == "x":
        return f"{v:.2f}x"
    if unidad == "dinero":
        return f"{'US$' if moneda == 'USD' else '$'}{v / 1e6:,.0f} {'MDD' if moneda == 'USD' else 'MDP'}"
    if unidad == "días":
        return f"{v:.0f} días"
    return f"{v:,.2f}"


def tabla(cab: list[str], filas: list[list]) -> str:
    out = ["| " + " | ".join(cab) + " |", "|" + "---|" * len(cab)]
    out += ["| " + " | ".join("" if c is None else str(c) for c in f) + " |" for f in filas]
    return "\n".join(out)


def kpis_de(d: Datos, t: str) -> list[dict]:
    k = d.kpis()
    defs = k.get("definiciones", {})
    return [{**defs.get(x["clave"], {}), **x} for x in (k.get("emisoras", {}).get(t) or {}).get("kpis", [])]


# ───────────────────────────── herramientas ─────────────────────────────

def h_buscar(d, a):
    q = _plano(a.get("texto", ""))
    filas = [[e["t"], e["n"], e["sector"], e["sub"], e["bloque"]] for e in d.universo()
             if not q or q in _plano(e["t"] + " " + e["n"] + " " + e.get("nombre", "") + " " + e["sector"] + " " + e["sub"])]
    return tabla(["Clave", "Nombre", "Sector", "Subsector", "Bloque en el fondo"], filas) if filas else "Sin coincidencias."


def h_cotizacion(d, a):
    ts = a.get("emisoras") or []
    if isinstance(ts, str):
        ts = [x for x in ts.replace(",", " ").split() if x]
    U, q = d.U(), d.q()
    claves = [resolver(d, t) if t.upper() not in q else t.upper() for t in ts] if ts else list(U)
    filas = []
    for t in claves:
        x = q.get(t, {})
        filas.append([t, U.get(t, {}).get("n", t), x.get("p"), pct(x.get("cp")), x.get("min"), x.get("max"), x.get("lo52"), x.get("hi52"),
                      x.get("ts", "")[:16], fuente(x.get("fuente", ""))])
    return tabla(["Clave", "Nombre", "Último", "Cambio", "Mín. día", "Máx. día", "Mín. 52s", "Máx. 52s", "Hora (UTC)", "Fuente"], filas)


def h_ficha(d, a):
    t = resolver(d, a.get("emisora"))
    e = d.U()[t]
    f = d.opcional("fichas.json").get("emisoras", {}).get(t, {})
    inf = d.opcional("fundamentales.json").get("emisoras", {}).get(t, {})
    q = d.q().get(t, {})
    port = d.opcional("portafolio.json").get("actual", {})
    pos = next((p for p in port.get("posiciones", []) if p["t"] == t), None)
    k = {x["clave"]: x for x in kpis_de(d, t)}
    lineas = [f"# {f.get('nombre') or e['n']} ({t})", f"{e['sector']} · {e['sub']} · bloque en el fondo: {e['bloque']} · peso en el índice {e['peso_indice'] * 100:.2f}%",
              f"Precio {q.get('p')} ({pct(q.get('cp'))}) · corte {q.get('ts', '')}"]
    if f.get("recomendacion"):
        lineas.append(f"Postura del equipo: {f['recomendacion']}" + (f" · convicción {f['conviccion']}" if f.get("conviccion") else ""))
    if f.get("descripcion") or inf.get("longBusinessSummary"):
        lineas += ["", "## Perfil", f.get("descripcion") or inf.get("longBusinessSummary")]
    claves = ["pe", "ve_uafida", "p_vl", "rend_dividendo", "roe", "margen_neto", "margen_uafida", "deuda_neta_uafida", "crec_ventas",
              "rend_ytd", "rend_1a", "volatilidad", "beta_1a"]
    lineas += ["", "## Datos clave", tabla(["KPI", "Valor", "Mediana de pares"], [[k[c]["nombre"], kfmt(k[c].get("valor"), k[c].get("unidad")),
                                                                                    kfmt(k[c].get("mediana_sector"), k[c].get("unidad"))] for c in claves if c in k])]
    if inf.get("recommendationKey"):
        lineas.append(f"Consenso de analistas: {inf['recommendationKey']} ({inf.get('numberOfAnalystOpinions', '?')} analistas), "
                      f"precio objetivo promedio {inf.get('targetMeanPrice')}")
    if pos:
        lineas += ["", f"## Posición en el fondo", f"{pos['titulos']:,} títulos · valor ${pos['valor']:,.2f} · peso {pos['peso'] * 100:.2f}% · "
                   f"G/P {pct(pos.get('pyg_pct'))} · desviación contra el índice {port.get('desviacion', {}).get(t, 0) * 100:+.2f} pp"]
    for sec, clave in (("Tesis", "tesis"), ("Catalizadores", "catalizadores"), ("Riesgos", "riesgos")):
        v = f.get(clave)
        if v:
            lineas += ["", f"## {sec}", "\n".join(f"- {x}" for x in v) if isinstance(v, list) else v]
    return "\n".join(lineas)


def h_kpis(d, a):
    t = resolver(d, a.get("emisora"))
    fam = a.get("familia")
    k = d.kpis()
    info = (k.get("emisoras", {}).get(t) or {})
    ks = [x for x in kpis_de(d, t) if not fam or x.get("familia") == fam]
    familias = k.get("familias", {})
    filas = [[familias.get(x.get("familia"), x.get("familia")), x.get("nombre"), kfmt(x.get("valor"), x.get("unidad"), x.get("moneda")), x.get("periodo") or "",
              kfmt(x.get("mediana_sector"), x.get("unidad"), x.get("moneda")), kfmt(x.get("mediana_universo"), x.get("unidad"), x.get("moneda")),
              "" if x.get("percentil") is None else f"{x['percentil'] * 100:.0f}", x.get("tendencia") or "", x.get("formula") or ""] for x in ks]
    out = [f"KPIs de {t} · último trimestre {info.get('ultimo_trimestre')} · pares: {', '.join(info.get('pares', []))}",
           tabla(["Familia", "KPI", "Valor", "Periodo", "Mediana pares", "Mediana universo", "Percentil", "Tendencia", "Fórmula"], filas)]
    ops = info.get("operativos") or []
    if ops:
        out += ["", "KPIs operativos capturados por el equipo:",
                tabla(["KPI", "Valor", "Periodo", "Tendencia", "Por qué importa"], [[o.get("nombre"), o.get("valor"), o.get("periodo"), o.get("tendencia"), o.get("porque")] for o in ops])]
    if info.get("qvm"):
        z = info["qvm"]
        out.append(f"\nQVM en vivo: Quality {z.get('quality')}, Value {z.get('value')}, Momentum {z.get('momentum')}, z compuesto {z.get('z')} (rango {z.get('rango')})")
    return "\n".join(out)


def _valor(d, t, clave):
    for x in (d.kpis().get("emisoras", {}).get(t) or {}).get("kpis", []):
        if x["clave"] == clave:
            return x.get("valor")
    return None


def h_ranking(d, a):
    clave = a.get("kpi")
    defs = d.kpis().get("definiciones", {})
    if clave not in defs:
        return "KPI desconocido. Opciones: " + ", ".join(f"{k} ({v['nombre']})" for k, v in sorted(defs.items()))
    df = defs[clave]
    xs = [(e["t"], _valor(d, e["t"], clave)) for e in d.universo() if e["t"] != "MEXTRAC"]
    xs = [x for x in xs if x[1] is not None]
    asc = a.get("orden") == "asc" or (a.get("orden") is None and df.get("mejor") == "bajo")
    xs.sort(key=lambda x: x[1], reverse=not asc)
    n = int(a.get("n") or 10)
    return f"{df['nombre']} ({df.get('formula', '')})\n" + tabla(["#", "Clave", "Valor"], [[i + 1, t, kfmt(v, df.get("unidad"))] for i, (t, v) in enumerate(xs[:n])])


def h_filtrar(d, a):
    defs = d.kpis().get("definiciones", {})
    crit = a.get("criterios") or []
    sector = a.get("sector")
    filas = []
    for e in d.universo():
        if e["t"] == "MEXTRAC" or (sector and _plano(sector) not in _plano(e["sector"] + " " + e["sub"])):
            continue
        ok, vals = True, []
        for c in crit:
            k, op, v = c.get("kpi"), c.get("op", ">="), float(c.get("valor"))
            x = _valor(d, e["t"], k)
            u = defs.get(k, {}).get("unidad")
            xv = None if x is None else (x * 100 if u == "%" else x)
            if xv is None or not (xv >= v if op == ">=" else xv <= v):
                ok = False
                break
            vals.append(kfmt(x, u))
        if ok:
            filas.append([e["t"], e["n"], e["sub"], *vals])
    cab = ["Clave", "Nombre", "Subsector", *[f"{defs.get(c['kpi'], {}).get('nombre', c['kpi'])} {c.get('op', '>=')} {c['valor']}" for c in crit]]
    return f"{len(filas)} emisoras cumplen (los porcentajes se comparan en %):\n" + tabla(cab, filas)


def h_noticias(d, a):
    items = d.json("noticias.json").get("items", [])
    t = resolver(d, a["emisora"]) if a.get("emisora") and str(a["emisora"]).upper() != "MERCADO" else (a.get("emisora") or "").upper() or None
    dias = int(a.get("dias") or 7)
    limite = (datetime.now(timezone.utc) - timedelta(days=dias)).strftime("%Y-%m-%d")
    xs = [n for n in items if (not t or n.get("t") == t) and (n.get("fecha") or "") >= limite][: int(a.get("n") or 15)]
    if not xs:
        return "Sin noticias en ese periodo."
    return "\n".join(f"- {n['fecha']} · {n.get('t')} · {n['titulo']} ({n.get('fuente', '')}; tono {n.get('tono', 'neutral')})"
                     + (f"\n  {n['resumen'][:280]}" if n.get("resumen") else "") + (f"\n  {n['url']}" if n.get("url") else "") for n in xs)


def h_portafolio(d, a):
    p = d.json("portafolio.json")
    act, serie = p.get("actual", {}), p.get("serie", [])
    u = serie[-1] if serie else {}
    lineas = [f"Valor ${act.get('valor', 0):,.2f} · efectivo ${act.get('efectivo', 0):,.2f} ({(act.get('efectivo_pct') or 0) * 100:.2f}%)",
              f"Hoy: cartera {pct(act.get('rend_dia'))} vs MEXTRAC {pct(act.get('bench_dia'))}",
              f"Acumulado desde {p.get('referencia')}: cartera {pct(u.get('rend_acum'))} vs MEXTRAC {pct(u.get('bench_acum'))} "
              f"(diferencia {(u.get('activo_acum') or 0) * 100:+.2f} pp) · TE ex post {(u.get('te_expost') or 0) * 100:.2f}%", "",
              tabla(["Clave", "Bloque", "Títulos", "Precio", "Valor", "Peso", "Desv. vs índice", "G/P %"],
                    [[x["t"], x.get("bloque"), f"{x['titulos']:,}", x.get("precio"), f"${x['valor']:,.0f}", f"{x['peso'] * 100:.2f}%",
                      f"{act.get('desviacion', {}).get(x['t'], 0) * 100:+.2f} pp" if x["t"] != "MEXTRAC" else "", pct(x.get("pyg_pct"))]
                     for x in act.get("posiciones", [])]),
              "", "Últimos días:", tabla(["Fecha", "Valor", "Cartera", "MEXTRAC", "Dif. acum."],
                                          [[r["f"], f"${r['valor']:,.0f}", pct(r.get("rend_dia")), pct(r.get("bench_dia")),
                                            f"{(r.get('activo_acum') or 0) * 100:+.2f} pp"] for r in serie[-int(a.get('dias') or 10):]])]
    return "\n".join(lineas)


def h_macro(d, a):
    M = d.json("macro.json").get("series", {})
    q = d.q()
    pedidas = [s.upper() for s in (a.get("series") or [])] or list(M)
    filas = []
    for k in pedidas:
        s = M.get(k)
        if not s:
            continue
        ult = (q.get(k) or {}).get("p") or s["c"][-1]
        r = lambda n: (ult / s["c"][-1 - n] - 1) if len(s["c"]) > n and s["c"][-1 - n] else None  # noqa: E731
        filas.append([k, s["n"], ult, pct((q.get(k) or {}).get("cp")), pct(r(21)), pct(r(252)), ", ".join(s.get("mueve", [])), s["d"][-1]])
    return tabla(["Serie", "Nombre", "Último", "1D", "1M", "12M", "Mueve a", "Fecha"], filas)


def h_estados(d, a):
    t = resolver(d, a.get("emisora"))
    est = d.opcional(f"estados/{t}.json")
    if not est:
        return f"Todavía no hay estados financieros de {t}: llegan con la descarga diaria de GitHub Actions."
    e, fr = a.get("estado", "resultados"), a.get("frecuencia", "trimestral")
    tb = (est.get(e) or {}).get(fr)
    if not tb:
        return f"Sin {e} {fr} para {t}."
    per = tb["periodos"]
    filas = [[k, *[("" if v is None else f"{v / 1e6:,.1f}" if "EPS" not in k else f"{v:.2f}") for v in vs]] for k, vs in tb["filas"].items()]
    return f"{t} · {e} {fr} · millones de {est.get('moneda') or 'MXN'} (UPA en unidades)\n" + tabla(["Partida", *per], filas)


def h_comparar(d, a):
    ts = [resolver(d, t) for t in (a.get("emisoras") or [])]
    defs = d.kpis().get("definiciones", {})
    claves = a.get("kpis") or ["rend_ytd", "rend_1a", "volatilidad", "beta_1a", "crec_ventas", "margen_uafida", "margen_neto", "roe", "deuda_neta_uafida", "pe", "ve_uafida", "p_vl", "rend_dividendo"]
    return tabla(["KPI", *ts], [[defs.get(c, {}).get("nombre", c), *[kfmt(_valor(d, t, c), defs.get(c, {}).get("unidad")) for t in ts]] for c in claves])


def h_atribucion(d, a):
    p = d.json("portafolio.json")
    at = p.get("atribucion") or {}
    if not at.get("posiciones"):
        return "Todavía no hay atribución: se calcula con operaciones.csv en cada corrida del pipeline."
    grupo = (a.get("grupo") or "").lower()
    n = int(a.get("n") or 40)
    c = at.get("componentes", {})
    suma = lambda est: sum(x["aporte"] for x in at["posiciones"] if x["estado"] == est)  # noqa: E731
    lineas = [f"Alfa acumulado del {at['desde']} al {at['hasta']} ({at['dias']} días): {pb(at['alfa'])} "
              f"(cartera {pct(at['rend'])} vs MEXTRAC {pct(at['bench'])}).",
              f"= abiertas {pb(suma('abierta'))} + cerradas {pb(suma('cerrada'))} + solo vía índice {pb(suma('indice'))} "
              f"+ efectivo {pb(c.get('efectivo'))} + premio del ETF {pb(c.get('etf'))} + operaciones {pb(c.get('operaciones'))} "
              f"+ comisiones {pb(c.get('comisiones'))}" + (f" + sin explicar {pb(c.get('residual'))}" if abs(c.get("residual") or 0) > 1e-6 else ""),
              f"Método: {at.get('metodo', '')} Pesos del índice: {at.get('pesos_benchmark', '')}."]
    if at.get("verificacion"):
        v = at["verificacion"]
        lineas.append(f"Verificado contra el tracker de Excel: {v['comparados']} aportes diarios, diferencia máxima {v['max_dif'] * 1e4:.4f} pb.")
    for est, titulo in (("abierta", "Posiciones abiertas"), ("cerrada", "Posiciones cerradas"), ("indice", "Solo vía índice (subponderadas por no tenerlas directo)")):
        if grupo and not est.startswith(grupo[:4]):
            continue
        xs = [x for x in at["posiciones"] if x["estado"] == est and (est != "indice" or abs(x["aporte"]) > 5e-7)][:n]
        lineas += ["", f"## {titulo}", tabla(["Clave", "Aporte al alfa", "Peso activo", "Peso efectivo", "Índice", "Rend. total", "G/P total"],
                                             [[x["t"], pb(x["aporte"]), f"{(x.get('activo') or 0) * 100:+.2f} pp", f"{(x.get('peso_lt') or 0) * 100:.2f}%",
                                               f"{(x.get('peso_b') or 0) * 100:.2f}%", pct(x.get("rend")),
                                               "" if est == "indice" else f"${x.get('pyg_total') or 0:,.0f}"] for x in xs]) if xs else "Ninguna."]
    if not grupo or grupo.startswith("vent"):
        vs = at.get("ventas") or []
        lineas += ["", "## Ventas (cierres parciales o totales)", tabla(["Fecha", "Clave", "Motivo", "Títulos", "Precio", "Costo prom.", "Realizado", "Quedan"],
                   [[x["f"], x["t"], x.get("motivo", ""), f"{x['titulos']:,}", f"{x['precio']:.2f}", f"{x['costo_promedio']:.2f}", f"${x['realizado']:,.2f}",
                     "cerrada" if x.get("cierre_total") else f"{x.get('queda', 0):,}"] for x in vs]) if vs else "Sin ventas."]
    return "\n".join(lineas)


def _investigacion(d, t=None):
    docs = d.opcional("investigacion.json").get("documentos", [])
    if t is None:
        return docs[0] if docs else None
    for doc in docs:
        if t in (doc.get("emisoras") or {}):
            return doc, doc["emisoras"][t]
    return None, None


def h_investigacion(d, a):
    if not a.get("emisora"):
        doc = _investigacion(d)
        if not doc:
            return "Sin documentos en investigacion/."
        out = [f"# {doc.get('titulo')}", f"Corte: {doc.get('corte')} · {doc.get('alcance') or ''} · archivo {doc.get('archivo')}", "", "## TL;DR",
               *[f"- {x}" for x in doc.get("tldr", [])], "", "## Hallazgos", *[f"- {x}" for x in doc.get("hallazgos", [])], "", "## Catalizadores macro",
               tabla(["Catalizador", "Estado", "Emisoras afectadas"], [[m["catalizador"], m["estado"][:300], m["afectadas"]] for m in doc.get("macro", [])]),
               "", "## Recomendaciones", *[f"- {x}" for x in doc.get("recomendaciones", [])], "", "## Limitaciones", *[f"- {x}" for x in doc.get("caveats", [])]]
        return "\n".join(out)
    t = resolver(d, a["emisora"])
    doc, e = _investigacion(d, t)
    if not e:
        return f"La investigación no cubre {t}."
    out = [f"# {e.get('nombre')} ({t}) · Nivel {e.get('nivel') or '—'} · {e.get('encabezado') or ''}", f"Investigación al {doc.get('corte')} · {doc.get('archivo')}"]
    r = e.get("resumen") or {}
    if r:
        out.append(f"KPIs clave: {r.get('kpis')} · tendencia 4 años: {r.get('tendencia')} · catalizador de corto plazo: {r.get('catalizador')}")
    for p in e.get("piezas", []):
        if p["tipo"] == "tabla":
            out += ["", f"### {p.get('titulo') or 'Tabla de KPIs'}", tabla(p["cols"], p["filas"])] + ([f"Nota: {p['nota']}"] if p.get("nota") else [])
        elif p["tipo"] == "lista":
            out += [f"- {(it.get('etiqueta') + ': ') if it.get('etiqueta') else ''}{it['md']}" + "".join(f"\n  - {x}" for x in it.get("sub", [])) for it in p["items"]]
        else:
            out += ["", (f"**{p['etiqueta']}.** " if p.get("etiqueta") else "") + p["md"]]
    if e.get("compacto"):
        out += ["", tabla(["Campo", "Valor"], [[k, v] for k, v in e["compacto"].items()])]
    if e.get("macro"):
        out += ["", "Catalizadores macro que la tocan:", *[f"- {m['catalizador']}: {m['afectadas']}" for m in e["macro"]]]
    if e.get("recomendaciones"):
        out += ["", "Recomendaciones del documento que la mencionan:", *[f"- {x}" for x in e["recomendaciones"]]]
    return "\n".join(out)


def h_sensibilidad(d, a):
    t = resolver(d, a.get("emisora"))
    s = (d.opcional("sensibilidad.json").get("emisoras") or {}).get(t) or {}
    m, mk = s.get("modelo"), s.get("mercado")
    if not m and not mk:
        return f"Sin sensibilidades para {t} (se calculan en la corrida completa)."
    precio = (d.q().get(t) or {}).get("p") or ((m or {}).get("base") or {}).get("precio")
    out = [f"# Sensibilidad de {t} · precio {precio}"]
    if m:
        b = m.get("base") or {}
        out.append(f"Base: {'utilidad con P/U constante' if b.get('tipo') == 'utilidad' else 'UAFIDA con VE/UAFIDA constante'}; "
                   f"cada 1% de la base mueve el precio {b.get('L') or 1:.2f}%." + (f" {m['segmentos']}" if m.get("segmentos") else ""))
        if m.get("nota"):
            out.append(m["nota"])
        out.append(tabla(["Driver", "Estado actual", "Movimiento", "Efecto en la base", "Efecto en el precio", "Precio implícito", "Fórmula"],
                         [[x["n"], x.get("actual", ""), f"{x.get('paso')} {x.get('unidad')}",
                           pct((x.get("e_base") or 0) * x.get("paso", 1)) if x.get("e_base") is not None else "n/d",
                           pct(x.get("efecto_paso")) if x.get("efecto_paso") is not None else "n/d",
                           f"{precio * (1 + x['efecto_paso']):.2f}" if x.get("efecto_paso") is not None and precio else "",
                           x.get("formula", "")] for x in m.get("drivers", [])]))
        esc = a.get("escenario") or {}
        if esc:
            ds = {x["id"]: x for x in m.get("drivers", [])}
            dp = sum((ds[k].get("e_precio") or 0) * float(v) for k, v in esc.items() if k in ds)
            db = sum((ds[k].get("e_base") or 0) * float(v) for k, v in esc.items() if k in ds)
            fuera = [k for k in esc if k not in ds]
            out.append(f"Escenario {esc}: base {pct(db)} · precio {pct(dp)}" + (f" → {precio * (1 + dp):.2f}" if precio else "")
                       + (f" (drivers desconocidos: {', '.join(fuera)}; opciones: {', '.join(ds)})" if fuera else ""))
    if mk and mk.get("ipc"):
        out += ["", f"Mercado ({mk['semanas']} semanas): beta IPC {mk['ipc']['beta']:.2f} (R² {mk['ipc']['r2'] * 100:.0f}%).",
                tabla(["Factor", "Beta neta del IPC", "t", "Beta simple", "Semana típica", "Clave"],
                      [[f["n"], f"{f['beta']:.2f}", f"{f['t']:.1f}" if f.get("t") is not None else "", f"{f['beta_simple']:.2f}" if f.get("beta_simple") is not None else "",
                        f"±{abs(f['efecto_1sd']) * 100:.1f}%" if f.get("efecto_1sd") is not None else "", "sí" if f.get("relevante") else ""]
                       for f in mk.get("factores", [])[:10]])]
    return "\n".join(out)


def h_estado(d, a):
    e = d.json("estado.json")
    return json.dumps({k: e.get(k) for k in ("generado", "modo", "mercado", "fuentes", "cobertura", "errores", "n_avisos", "ultimo_completo", "ultimo_rapido")},
                      ensure_ascii=False, indent=1)


def _p(desc, **props):
    req = [k for k, v in props.items() if v.pop("_req", False)]
    return {"description": desc, "inputSchema": {"type": "object", "properties": props, "required": req, "additionalProperties": False}}


EMISORA = {"type": "string", "description": "Clave BMV (FEMSAUBD) o nombre (femsa)", "_req": True}
HERRAMIENTAS = {
    "buscar_emisora": (h_buscar, _p("Busca emisoras del universo por clave, nombre o sector.", texto={"type": "string", "description": "Texto a buscar; vacío lista todas"})),
    "cotizacion": (h_cotizacion, _p("Última cotización (precio, cambio, rangos) de una o varias emisoras o series macro.",
                                    emisoras={"type": "array", "items": {"type": "string"}, "description": "Claves o nombres; vacío = todas"})),
    "ficha": (h_ficha, _p("Ficha completa de una emisora: perfil, datos clave, consenso, posición en el fondo, tesis, catalizadores y riesgos.", emisora=dict(EMISORA))),
    "kpis": (h_kpis, _p("Todos los KPIs de una emisora (crecimiento, márgenes, rentabilidad, balance, flujo, valuación, mercado, riesgo) contra la mediana de sus pares y del universo, más los KPIs operativos del equipo y los factores QVM.",
                        emisora=dict(EMISORA), familia={"type": "string", "description": "Opcional: crecimiento, margenes, rentabilidad, balance, flujo, bancario, seguros, valuacion, mercado, riesgo, tecnico, liquidez"})),
    "ranking_kpi": (h_ranking, _p("Ordena el universo por un KPI (clave como roe, pe, margen_uafida, deuda_neta_uafida, rend_1a, volatilidad...).",
                                  kpi={"type": "string", "_req": True}, n={"type": "integer", "description": "Cuántas (10 por omisión)"},
                                  orden={"type": "string", "enum": ["asc", "desc"], "description": "Por omisión, de mejor a peor"})),
    "filtrar": (h_filtrar, _p("Filtra emisoras con criterios sobre KPIs. Porcentajes en % (ROE ≥ 15 = 15%), múltiplos en veces.",
                              criterios={"type": "array", "_req": True, "items": {"type": "object", "properties": {"kpi": {"type": "string"}, "op": {"type": "string", "enum": [">=", "<="]}, "valor": {"type": "number"}}, "required": ["kpi", "valor"]}},
                              sector={"type": "string", "description": "Opcional: filtra por sector o subsector"})),
    "noticias": (h_noticias, _p("Noticias recientes (equipo, LSEG y Google Noticias) de una emisora o del mercado.",
                                emisora={"type": "string", "description": "Clave, nombre o MERCADO; vacío = todas"}, dias={"type": "integer"}, n={"type": "integer"})),
    "portafolio": (h_portafolio, _p("Portafolio del fondo: valor, posiciones, pesos, desviaciones contra el índice y rendimiento contra el MEXTRAC.",
                                    dias={"type": "integer", "description": "Días de la serie a mostrar"})),
    "macro": (h_macro, _p("Divisas, tasas, índices y materias primas, con las emisoras que mueve cada serie.",
                          series={"type": "array", "items": {"type": "string"}, "description": "USDMXN, COBRE, ORO, UST10, IPC...; vacío = todas"})),
    "estados_financieros": (h_estados, _p("Estado de resultados, balance o flujo de una emisora, trimestral o anual.", emisora=dict(EMISORA),
                                          estado={"type": "string", "enum": ["resultados", "balance", "flujo"]}, frecuencia={"type": "string", "enum": ["trimestral", "anual"]})),
    "comparar": (h_comparar, _p("Compara KPIs de varias emisoras lado a lado.", emisoras={"type": "array", "items": {"type": "string"}, "_req": True},
                                kpis={"type": "array", "items": {"type": "string"}, "description": "Claves de KPI; vacío = selección estándar"})),
    "atribucion_alfa": (h_atribucion, _p("Contribución al alfa (contra el MEXTRAC) de cada posición: abiertas, cerradas, solo vía índice, ventas realizadas y efectos de efectivo, premio del ETF, operaciones y comisiones. Cuadra con el alfa acumulado y se verifica contra el tracker.",
                                         grupo={"type": "string", "description": "Opcional: abiertas, cerradas, indice o ventas"}, n={"type": "integer", "description": "Máximo de renglones por grupo"})),
    "investigacion": (h_investigacion, _p("Investigación del equipo (KPIs operativos 2022–3T26 y catalizadores): de una emisora (modelo de negocio, tabla de KPIs, narrativa, catalizadores, consenso, juicio, fuentes) o, sin emisora, el resumen del documento (TL;DR, hallazgos, catalizadores macro, recomendaciones).",
                                          emisora={"type": "string", "description": "Clave o nombre; vacío = resumen del documento"})),
    "sensibilidad": (h_sensibilidad, _p("Drivers de valor de una emisora y cuánto movería el precio un cambio en cada uno (puente de valuación a múltiplo constante), más las betas semanales contra el IPC, dólar, cobre, oro, tasas, etc. Acepta un escenario para combinarlos.",
                                        emisora=dict(EMISORA), escenario={"type": "object", "description": "Opcional: {id_driver: movimiento en su unidad}, p. ej. {\"precio_cu\": -10, \"fx\": 5}"})),
    "estado_datos": (h_estado, _p("Cuándo se actualizaron los datos de la terminal, con qué fuentes y qué falló.")),
}


# ───────────────────────────── protocolo ─────────────────────────────

def responder(id_, resultado=None, error=None):
    msg = {"jsonrpc": "2.0", "id": id_}
    if error:
        msg["error"] = error
    else:
        msg["result"] = resultado
    sys.stdout.write(json.dumps(msg, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def manejar(d: Datos, msg: dict):
    metodo, id_, params = msg.get("method"), msg.get("id"), msg.get("params") or {}
    if id_ is None:                       # notificación (initialized, cancelled...): no se responde
        return
    if metodo == "initialize":
        pedida = params.get("protocolVersion")
        responder(id_, {"protocolVersion": pedida if pedida in VERSIONES else VERSIONES[1],
                        "capabilities": {"tools": {"listChanged": False}},
                        "serverInfo": {"name": "north-star-terminal", "title": "North Star Terminal", "version": "1.0.0"},
                        "instructions": INSTRUCCIONES})
    elif metodo == "ping":
        responder(id_, {})
    elif metodo == "tools/list":
        responder(id_, {"tools": [{"name": n, **spec} for n, (_, spec) in HERRAMIENTAS.items()]})
    elif metodo == "tools/call":
        nombre, args = params.get("name"), params.get("arguments") or {}
        if nombre not in HERRAMIENTAS:
            responder(id_, error={"code": -32602, "message": f"Herramienta desconocida: {nombre}"})
            return
        try:
            texto = HERRAMIENTAS[nombre][0](d, args)
            responder(id_, {"content": [{"type": "text", "text": texto}], "isError": False})
        except Exception as e:  # el error vuelve al modelo como resultado, para que pueda corregir la llamada
            responder(id_, {"content": [{"type": "text", "text": f"Error: {type(e).__name__}: {e}"}], "isError": True})
    else:
        responder(id_, error={"code": -32601, "message": f"Método no soportado: {metodo}"})


def main():
    ap = argparse.ArgumentParser(description="Servidor MCP de North Star Terminal")
    aqui = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--local", help="carpeta con los JSON de la terminal (por omisión se descargan de GitHub)")
    ap.add_argument("--repo", default=os.environ.get("NST_REPO", REPO))
    a = ap.parse_args()
    local = a.local
    if not local and os.path.exists(os.path.join(aqui, "..", "datos", "estado.json")) and os.environ.get("NST_LOCAL") == "1":
        local = os.path.join(aqui, "..", "datos")
    d = Datos(local, a.repo)
    for linea in sys.stdin:
        linea = linea.strip()
        if not linea:
            continue
        try:
            msg = json.loads(linea)
        except json.JSONDecodeError:
            responder(None, error={"code": -32700, "message": "JSON inválido"})
            continue
        for m in (msg if isinstance(msg, list) else [msg]):
            manejar(d, m)


if __name__ == "__main__":
    main()
