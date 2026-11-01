"""Lectura de los archivos que escribe el equipo a mano: empresas.txt (fichas) y
noticias.txt. Replica el mismo formato que entiende el tablero (index.html):

  · Bloques === TICKER === con campos «clave: valor».
  · Textos largos en líneas indentadas con dos espacios.
  · Listas con guion: catalizadores, riesgos, fortalezas y kpis.
  · kpis: una línea por KPI con «nombre | valor | periodo | tendencia | por qué importa».
"""
from __future__ import annotations

import csv
import os
import re
import unicodedata

from universo import RAIZ, emisoras

LISTAS = ("catalizadores", "riesgos", "fortalezas", "kpis")
_CAMPO = re.compile(r"^([A-Za-záéíóúñÁÉÍÓÚÑ_0-9]+)\s*:\s*(.*)$")
_CITA = re.compile(r"\s*\[cite:\s*[\d,\s]*\]", re.I)


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower().strip())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9_]", "", s)


def _sin_comentarios(txt: str) -> str:
    return "\n".join(l for l in txt.replace("\r", "").split("\n") if not re.match(r"^\s*#", l))


def campos(bloque: str) -> dict:
    o: dict = {}
    clave, buf = None, []

    def cerrar():
        nonlocal clave, buf
        if clave:
            t = "\n".join(buf).strip()
            if t:
                o[clave] = t
        clave, buf = None, []

    for l in bloque.split("\n"):
        if re.match(r"^\s{2,}\S", l) and clave is not None:
            buf.append(l.strip())
            continue
        m = _CAMPO.match(l)
        if m:
            cerrar()
            clave = _norm(m.group(1))
            buf = [m.group(2)] if m.group(2) else []
            continue
        if l.strip() and clave:
            buf.append(l.strip())
    cerrar()
    return o


def _simbolo(s: str) -> str:
    s = (s or "").strip().upper().replace(".MX", "")
    alias = {"PE&OLES": "PEOLES", "PENOLES": "PEOLES", "LIVEPOLC-1": "LIVEPOLC1", "MEXTRAC09": "MEXTRAC"}
    return alias.get(s, s)


def parse_kpi(linea: str) -> dict | None:
    partes = [p.strip() for p in linea.split("|")]
    if not partes or not partes[0]:
        return None
    partes += [""] * (5 - len(partes))
    nombre, valor, periodo, tendencia, porque = partes[:5]
    return {"nombre": nombre, "valor": valor or None, "periodo": periodo or None,
            "tendencia": tendencia or None, "porque": porque or None}


def leer_fichas(ruta: str | None = None) -> dict:
    ruta = ruta or os.path.join(RAIZ, "empresas.txt")
    try:
        with open(ruta, encoding="utf-8") as f:
            txt = _sin_comentarios(f.read())
    except FileNotFoundError:
        return {}
    validos = {e["t"] for e in emisoras()}
    partes = re.split(r"^===\s*([A-Za-z0-9&._-]+)\s*===\s*$", txt, flags=re.M)
    out = {}
    for i in range(1, len(partes), 2):
        t = _simbolo(partes[i])
        if t not in validos:
            continue
        f = campos(partes[i + 1] if i + 1 < len(partes) else "")
        for k in LISTAS:
            if k in f:
                items = [re.sub(r"^-\s*", "", x).strip() for x in f[k].split("\n")]
                f[k] = [x for x in items if x]
        if "kpis" in f:
            f["kpis"] = [k for k in (parse_kpi(x) for x in f["kpis"]) if k]
        if "factores" in f:
            f["factores_z"] = _factores(f["factores"])
        out[t] = f
    return out


def _factores(texto: str) -> dict:
    """'Quality +1.35, Value +0.41, Momentum +1.17; z del ciclo +1.71, percentil 91.9%' → números."""
    z = {}
    for clave, patron in (("quality", r"Quality\s*([+\-−]?\d+(?:\.\d+)?)"),
                          ("value", r"Value\s*([+\-−]?\d+(?:\.\d+)?)"),
                          ("momentum", r"Momentum\s*([+\-−]?\d+(?:\.\d+)?)"),
                          ("z_ciclo", r"z del ciclo\s*([+\-−]?\d+(?:\.\d+)?)"),
                          ("percentil", r"percentil\s*([+\-−]?\d+(?:\.\d+)?)")):
        m = re.search(patron, texto, re.I)
        if m:
            z[clave] = float(m.group(1).replace("−", "-"))
    return z


def leer_noticias_equipo(ruta: str | None = None) -> list[dict]:
    """noticias.txt: bloques separados por '---'. Incluye las que bajó el vigilante desde LSEG."""
    ruta = ruta or os.path.join(RAIZ, "noticias.txt")
    try:
        with open(ruta, encoding="utf-8") as f:
            txt = _CITA.sub("", f.read())
    except FileNotFoundError:
        return []
    bloques, cur = [], []
    for l in txt.replace("\r", "").split("\n"):
        if re.match(r"^---+\s*$", l):
            if cur:
                bloques.append("\n".join(cur))
            cur = []
            continue
        if re.match(r"^\s*#", l):
            continue
        cur.append(l)
    if cur:
        bloques.append("\n".join(cur))
    out = []
    for b in bloques:
        f = campos(b)
        if not f.get("titulo"):
            continue
        fecha = (f.get("fecha") or "").replace("T", " ")
        ident = f.get("id") or f"equipo:{f.get('fecha', '')}:{f['titulo'][:60]}"
        out.append({
            "id": ident,
            "fecha": fecha[:16],
            "t": _simbolo(f.get("emisora", "")) or "MERCADO",
            "titulo": f["titulo"],
            "fuente": f.get("fuente", ""),
            "tono": (f.get("tono") or "neutral").lower(),
            "impacto": (f.get("impacto") or "").lower(),
            "url": f.get("url", ""),
            "resumen": (f.get("resumen") or "").replace("\n", " "),
            "origen": "lseg" if ident.startswith("lseg:") else "equipo",
        })
    return out


def leer_csv(nombre: str) -> list[dict]:
    try:
        with open(os.path.join(RAIZ, nombre), newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return []
