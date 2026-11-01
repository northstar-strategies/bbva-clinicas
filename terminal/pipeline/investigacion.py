"""Investigación del equipo (investigacion/*.md) convertida en datos para la terminal.

El documento de KPIs operativos y catalizadores se escribe en Markdown, con una sección por
emisora («#### 2.1 FEMSA (FEMSAUBD) — Nivel 1 · ...») que trae, en este orden y con etiquetas
en negritas: (a) modelo de negocio y KPIs, (b) tabla de KPIs, (c) narrativa, (d) catalizadores
históricos, (e) prospectivos, (f) consenso y (g) fuentes. Las emisoras de Nivel 2 y 3 vienen en
tablas compactas. Este módulo lo separa por emisora sin perder el orden ni el texto original,
para que la ficha lo muestre tal cual y el servidor MCP lo pueda citar.

Solo biblioteca estándar.
"""
from __future__ import annotations

import glob
import os
import re
import unicodedata

from universo import EMISORAS, RAIZ

CARPETA = os.path.join(RAIZ, "investigacion")
TICKERS = {e[0] for e in EMISORAS}

# Formas en que el texto nombra a las emisoras (siglas cortas y nombres comunes).
ALIAS = {
    "GMEXICO": "GMEXICOB", "GMÉXICO": "GMEXICOB", "GRUPO MÉXICO": "GMEXICOB", "GMXT": "GMEXICOB",
    "GFNORTE": "GFNORTEO", "BANORTE": "GFNORTEO", "BBAJIO": "BBAJIOO", "BANBAJÍO": "BBAJIOO",
    "VOLAR": "VOLARA", "VOLARIS": "VOLARA", "CHDRAUI": "CHDRAUIB", "CHEDRAUI": "CHDRAUIB", "LIVEPOL": "LIVEPOLC1",
    "LIVERPOOL": "LIVEPOLC1", "KIMBER": "KIMBERA", "BIMBO": "BIMBOA", "GRUMA": "GRUMAB", "CEMEX": "CEMEXCPO",
    "OMA": "OMAB", "ASUR": "ASURB", "GAP": "GAPB", "AMX": "AMXB", "KOF": "KOFUBL", "FEMSA": "FEMSAUBD",
    "OXXO": "FEMSAUBD", "BMV": "BOLSAA", "MEGACABLE": "MEGACPO", "TELEVISA": "TLEVISACPO", "PEÑOLES": "PEOLES",
    "SIGMA": "SIGMAFA", "GCARSO": "GCARSOA1", "LACOMER": "LACOMERUBC", "QUÁLITAS": "Q", "WALMART": "WALMEX",
    "VESTA": "VESTA", "ORBIA": "ORBIA", "ALPEK": "ALPEKA", "ALSEA": "ALSEA", "CUERVO": "CUERVO", "BECLE": "CUERVO",
    "INBURSA": "GFINBURO", "GENTERA": "GENTERA", "PINFRA": "PINFRA", "MEGA": "MEGACPO",
}

# Etiqueta en negritas → clave canónica de la sección.
CLAVES = [
    ("modelo", "modelo"), ("tabla", "tabla"), ("narrativa", "narrativa"), ("catalizadores historicos", "historicos"),
    ("prospectivos", "prospectivos"), ("consenso", "consenso"), ("fuente", "fuentes"), ("lectura", "lectura"),
    ("juicio", "juicio"), ("nota de calidad", "calidad"), ("discrepancias", "calidad"), ("kpis", "kpis"),
    ("catalizadores", "catalizadores"), ("datos", "datos"), ("senal", "senal"), ("3t26", "resultado"),
]


def _plano(s: str) -> str:
    s = unicodedata.normalize("NFD", s or "").encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", s).strip().lower()


def clave_de(etiqueta: str | None) -> str:
    e = _plano(re.sub(r"^\(?[a-g](?:[–-][a-g])?\)\s*", "", etiqueta or ""))
    for prefijo, clave in CLAVES:
        if e.startswith(prefijo):
            return clave
    return "texto"


def tickers_en(texto: str) -> list[str]:
    """Emisoras mencionadas en un texto (claves de pizarra, siglas o nombres), en orden de aparición."""
    out: list[str] = []
    for m in re.finditer(r"[A-Za-zÁÉÍÓÚÑáéíóúñ&][A-Za-zÁÉÍÓÚÑáéíóúñ&0-9]*(?:\s+México)?", texto or ""):
        w = m.group(0)
        cand = None
        if w in TICKERS:
            cand = w
        elif w.upper() in ALIAS and (w.isupper() or w[0].isupper()):
            cand = ALIAS[w.upper()]
        if cand and cand not in out:
            out.append(cand)
    return out


def _tabla(lineas: list[str]) -> dict:
    def celdas(l: str) -> list[str]:
        l = l.strip()
        if l.startswith("|"):
            l = l[1:]
        if l.endswith("|"):
            l = l[:-1]
        return [c.strip() for c in l.split("|")]
    filas = [celdas(l) for l in lineas if not re.match(r"^\s*\|?\s*:?-{3,}", l)]
    cols = filas[0] if filas else []
    return {"cols": cols, "filas": [f + [""] * (len(cols) - len(f)) for f in filas[1:]]}


def _etiqueta(parrafo: str) -> tuple[str | None, str]:
    """«**(a) Modelo y KPIs.** texto» → ("(a) Modelo y KPIs", "texto")."""
    m = re.match(r"^\*\*(.+?)\*\*\s*[:.]?\s*(.*)$", parrafo, re.S)
    if not m:
        return None, parrafo
    etq = m.group(1).strip().rstrip(".:").strip()
    return etq, m.group(2).strip()


def _juicio(texto: str) -> str | None:
    m = re.search(r"\*\*Juicio:\*\*\s*(.+?)(?=\s\*\*[A-ZÁÉÍÓÚ][^*]{2,40}[:.]\*\*|$)", texto, re.S)
    return m.group(1).strip() if m else None


def _bloques(lineas: list[str]) -> list[dict]:
    """Párrafos, tablas y listas de un tramo de Markdown, en orden."""
    out: list[dict] = []
    i = 0
    while i < len(lineas):
        l = lineas[i]
        if not l.strip() or l.strip() == "---":
            i += 1
            continue
        if l.lstrip().startswith("|"):
            j = i
            while j < len(lineas) and lineas[j].lstrip().startswith("|"):
                j += 1
            out.append({"tipo": "tabla", **_tabla(lineas[i:j])})
            i = j
            continue
        if re.match(r"^\s*(?:[-*]|\d+\.)\s+", l) and not re.match(r"^\*\*", l.strip()):
            items: list[dict] = []
            j = i
            while j < len(lineas) and (re.match(r"^\s*(?:[-*]|\d+\.)\s+", lineas[j]) or (lineas[j].startswith("  ") and lineas[j].strip())):
                nivel = (len(lineas[j]) - len(lineas[j].lstrip())) // 2
                txt = re.sub(r"^\s*(?:[-*]|\d+\.)\s+", "", lineas[j]).strip()
                if nivel and items:
                    items[-1].setdefault("sub", []).append(txt)
                else:
                    items.append({"md": txt})
                j += 1
            for it in items:
                etq, resto = _etiqueta(it["md"])
                if etq and len(etq) < 60:
                    it["etiqueta"], it["md"] = etq, resto
            out.append({"tipo": "lista", "items": items})
            i = j
            continue
        j = i
        while j < len(lineas) and lineas[j].strip() and not lineas[j].lstrip().startswith("|") and not re.match(r"^\s*[-*]\s+", lineas[j]) \
                and not lineas[j].startswith("#"):
            j += 1
        texto = " ".join(x.strip() for x in lineas[i:j])
        if texto.startswith("*") and not texto.startswith("**") and out and out[-1]["tipo"] == "tabla":
            out[-1]["nota"] = texto.strip("* ").strip()
        else:
            etq, resto = _etiqueta(texto)
            out.append({"tipo": "texto", "etiqueta": etq, "md": resto if etq else texto})
        i = max(j, i + 1)
    return out


def _encabezado(titulo: str) -> dict:
    """«2.1 FEMSA (FEMSAUBD) — Nivel 1 · 15.3% cartera / 10.5% índice» → partes."""
    t = re.sub(r"^\d+(?:\.\d+)*\s*", "", titulo).strip()
    nivel = re.search(r"Nivel\s+(\d)", t)
    partes = [x.strip() for x in re.split(r"\s+—\s+", t)]
    if re.match(r"^Nivel\s+\d$", partes[0]) and len(partes) > 1:      # «Nivel 3 — Volaris (VOLARA)»
        partes = [partes[1], partes[0]] + partes[2:]
    nombre = re.sub(r"\s*\([A-Z0-9&]+\)\s*$", "", partes[0]).strip()
    resto = " — ".join(partes[1:])
    return {"nombre": nombre, "nivel": int(nivel.group(1)) if nivel else None, "encabezado": resto}


def leer(ruta: str) -> dict:
    with open(ruta, encoding="utf-8") as f:
        lineas = f.read().replace("\r\n", "\n").split("\n")
    doc: dict = {"archivo": os.path.relpath(ruta, RAIZ).replace(os.sep, "/"), "titulo": "", "corte": None, "alcance": None,
                 "metodologia": None, "tldr": [], "hallazgos": [], "contexto": [], "resumen": {}, "macro": [],
                 "recomendaciones": [], "caveats": [], "emisoras": {}}
    # Secciones por encabezado
    secciones: list[tuple[int, str, list[str]]] = []
    actual: tuple[int, str, list[str]] = (0, "", [])
    for l in lineas:
        m = re.match(r"^(#{1,4})\s+(.*)$", l)
        if m:
            secciones.append(actual)
            actual = (len(m.group(1)), m.group(2).strip(), [])
        else:
            actual[2].append(l)
    secciones.append(actual)

    sector = ""
    for nivel, titulo, cuerpo in secciones:
        tp = _plano(titulo)
        bloques = _bloques(cuerpo)
        if nivel == 1:
            doc["titulo"] = titulo
            for b in bloques:
                if b["tipo"] != "texto":
                    continue
                txt = (b.get("etiqueta") or "") + " " + b["md"]
                mc = re.search(r"\*\*Fecha de corte:\*\*\s*([^·]+)", "**" + txt) or re.search(r"Fecha de corte:?\s*([^·]+)", txt)
                if mc:
                    doc["corte"] = mc.group(1).strip(" *")
                    ma = re.search(r"Alcance:\*?\*?\s*(.+)$", b["md"])
                    doc["alcance"] = ma.group(1).strip() if ma else b["md"]
                elif (b.get("etiqueta") or "").lower().startswith("nota metodol"):
                    doc["metodologia"] = b["md"]
            continue
        if nivel == 2 and tp.startswith("tl;dr"):
            doc["tldr"] = [it["md"] if not it.get("etiqueta") else f"**{it['etiqueta']}.** {it['md']}"
                           for b in bloques if b["tipo"] == "lista" for it in b["items"]]
            continue
        if nivel == 2 and tp.startswith("key findings"):
            doc["hallazgos"] = [(f"**{it['etiqueta']}:** " if it.get("etiqueta") else "") + it["md"]
                                for b in bloques if b["tipo"] == "lista" for it in b["items"]]
            continue
        if nivel == 2 and tp.startswith("resumen ejecutivo"):
            for b in bloques:
                if b["tipo"] == "tabla":
                    for f in b["filas"]:
                        t = f[0].strip("* ")
                        if t in TICKERS:
                            doc["resumen"][t] = dict(zip(["t", "sector", "nivel", "kpis", "tendencia", "catalizador"], [t] + f[1:6]))
                elif b["tipo"] == "texto" and b["md"].startswith("*"):
                    doc["nota_resumen"] = b["md"].strip("* ")
            continue
        if nivel == 2 and "catalizadores macro" in tp:
            for b in bloques:
                if b["tipo"] == "tabla":
                    for f in b["filas"]:
                        doc["macro"].append({"catalizador": f[0].strip("* "), "estado": f[1], "afectadas": f[2],
                                             "emisoras": tickers_en(f[2])})
            continue
        if nivel == 2 and tp.startswith("recommendations"):
            doc["recomendaciones"] = [it["md"] if not it.get("etiqueta") else f"**{it['etiqueta']}:** {it['md']}"
                                      for b in bloques if b["tipo"] == "lista" for it in b["items"]]
            continue
        if nivel == 2 and tp.startswith("caveats"):
            doc["caveats"] = [it["md"] if not it.get("etiqueta") else f"**{it['etiqueta']}:** {it['md']}"
                              for b in bloques if b["tipo"] == "lista" for it in b["items"]]
            continue
        if nivel == 3:
            sector = re.sub(r"^\d+\.\s*", "", titulo).split("—")[0].strip()
            if "contexto" in tp:
                doc["contexto"] = bloques
                continue
        if nivel in (3, 4):
            ts = [t for t in tickers_en(titulo) if t in TICKERS]
            if nivel == 4 and len(ts) == 1:
                t = ts[0]
                enc = _encabezado(titulo)
                piezas = []
                for b in bloques:
                    b["clave"] = clave_de(b.get("etiqueta")) if b["tipo"] == "texto" else b["tipo"]
                    piezas.append(b)
                # Una etiqueta sola («(b) Tabla de KPIs») titula la tabla que sigue.
                for k, b in enumerate(piezas[:-1]):
                    if b["tipo"] == "texto" and b["clave"] == "tabla" and not b["md"] and piezas[k + 1]["tipo"] == "tabla":
                        piezas[k + 1]["titulo"] = re.sub(r"^\([a-g]\)\s*", "", b["etiqueta"] or "")
                piezas = [b for b in piezas if not (b["tipo"] == "texto" and b["clave"] == "tabla" and not b["md"])]
                texto_todo = " ".join(b.get("md", "") for b in piezas if b["tipo"] == "texto")
                texto_todo += " " + " ".join(it["md"] for b in piezas if b["tipo"] == "lista" for it in b["items"])
                juicios = [it["md"] for b in piezas if b["tipo"] == "lista" for it in b["items"] if clave_de(it.get("etiqueta")) == "juicio"]
                modelo = next((b["md"] for b in piezas if b.get("clave") == "modelo"), None)
                kpis_lista = next((it["md"] for b in piezas if b["tipo"] == "lista" for it in b["items"] if clave_de(it.get("etiqueta")) == "kpis"), None)
                doc["emisoras"][t] = {
                    "t": t, "seccion": sector, "titulo": titulo, **enc, "piezas": piezas, "modelo": modelo or kpis_lista,
                    "juicio": _juicio(texto_todo) or (juicios[0] if juicios else None), "tablas": [b for b in piezas if b["tipo"] == "tabla"],
                }
                continue
            # Tablas compactas (Nivel 2 y 3): una fila por emisora.
            for b in bloques:
                if b["tipo"] != "tabla":
                    continue
                cols = [_plano(c) for c in b["cols"]]
                for f in b["filas"]:
                    tf = tickers_en(f[0])
                    if not tf:
                        continue
                    t = tf[0]
                    fila = dict(zip(b["cols"], f))
                    peso = re.search(r"\(([\d.]+%)\)", f[0])
                    reg = doc["emisoras"].setdefault(t, {"t": t, "seccion": sector, "titulo": f[0], "nombre": re.sub(r"\s*\(.*\)$", "", f[0]).strip(),
                                                         "nivel": 3 if "nivel 3" in tp else 2 if "nivel 2" in tp else None,
                                                         "encabezado": "", "piezas": [], "modelo": None, "juicio": None, "tablas": []})
                    reg["compacto"] = {c: v for c, v in fila.items() if c != b["cols"][0]}
                    kp = next((v for c, v in fila.items() if _plano(c).startswith("kpis")), None)
                    if kp and not reg.get("modelo"):
                        reg["modelo"] = f"KPIs a monitorear: {kp}."
                    if peso and not reg["encabezado"]:
                        reg["encabezado"] = f"{peso.group(1)} del índice"
                    _ = cols
    # Lo transversal que toca a cada emisora
    for t, e in doc["emisoras"].items():
        e["resumen"] = doc["resumen"].get(t)
        e["macro"] = [m for m in doc["macro"] if t in m["emisoras"]]
        e["recomendaciones"] = [r for r in doc["recomendaciones"] if t in tickers_en(r)]
        if e.get("nivel") is None and e["resumen"]:
            try:
                e["nivel"] = int(e["resumen"]["nivel"])
            except (TypeError, ValueError):
                pass
    for t, r in doc["resumen"].items():
        if t not in doc["emisoras"]:
            doc["emisoras"][t] = {"t": t, "nombre": t, "nivel": int(r["nivel"]) if str(r.get("nivel", "")).isdigit() else None,
                                  "seccion": r.get("sector"), "titulo": t, "encabezado": "", "piezas": [], "modelo": None,
                                  "juicio": None, "tablas": [], "resumen": r,
                                  "macro": [m for m in doc["macro"] if t in m["emisoras"]],
                                  "recomendaciones": [x for x in doc["recomendaciones"] if t in tickers_en(x)]}
    return doc


def leer_todo(carpeta: str = CARPETA) -> dict:
    """Todas las investigaciones de la carpeta; la más reciente (por fecha de corte en el nombre o del archivo) primero."""
    docs = []
    for ruta in sorted(glob.glob(os.path.join(carpeta, "*.md"))):
        if os.path.basename(ruta).lower() == "readme.md":
            continue
        try:
            docs.append(leer(ruta))
        except Exception as e:  # un documento mal formado no debe tumbar la corrida
            docs.append({"archivo": os.path.relpath(ruta, RAIZ), "error": f"{type(e).__name__}: {e}", "emisoras": {}})
    return {"documentos": docs}
