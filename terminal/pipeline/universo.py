"""Universo de la terminal: las 37 emisoras que analiza el fondo, el ETF de referencia,
los índices y los indicadores macro que las mueven.

Para agregar una emisora basta una fila en EMISORAS (y, si se quiere, su bloque
=== TICKER === en empresas.txt). El símbolo de Yahoo Finance es el que usa el pipeline
para descargar todo lo demás.
"""
from __future__ import annotations

import json
import os

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# ticker, símbolo Yahoo, nombre corto, sector, subsector, grupo de KPIs, logo, búsqueda de noticias
EMISORAS = [
    ("AC", "AC.MX", "Arca Continental", "Consumo frecuente", "Bebidas", "bebidas",
     "Arca_Continental_logo.svg", '"Arca Continental"'),
    ("ALPEKA", "ALPEKA.MX", "Alpek", "Materiales", "Químicos", "quimicos",
     "Alpek_1_Positivo.svg", 'Alpek'),
    ("ALSEA", "ALSEA.MX", "Alsea", "Consumo discrecional", "Restaurantes", "restaurantes",
     "Alsea_1_Positivo.svg", 'Alsea'),
    ("AMXB", "AMXB.MX", "América Móvil", "Comunicaciones", "Telecomunicaciones", "telecom",
     "Logo_de_América_Móvil (2).svg", '"América Móvil"'),
    ("ASURB", "ASURB.MX", "ASUR", "Industriales", "Aeropuertos", "aeropuertos",
     "Grupo_Aeroportuario_del_Sureste_logo.svg", '"Grupo Aeroportuario del Sureste"'),
    ("BBAJIOO", "BBAJIOO.MX", "BanBajío", "Financieros", "Bancos", "bancos",
     "Logo_de_BanBajío.svg", 'BanBajío'),
    ("BIMBOA", "BIMBOA.MX", "Grupo Bimbo", "Consumo frecuente", "Alimentos", "alimentos",
     "BIMBOA.MX.svg", '"Grupo Bimbo"'),
    ("BOLSAA", "BOLSAA.MX", "Grupo BMV", "Financieros", "Infraestructura de mercados", "bolsa",
     "BMV_1_Positivo.svg", '"Grupo BMV" OR "Bolsa Mexicana de Valores"'),
    ("CEMEXCPO", "CEMEXCPO.MX", "Cemex", "Materiales", "Cemento", "cemento",
     "CX_BIG.svg", 'Cemex'),
    ("CHDRAUIB", "CHDRAUIB.MX", "Chedraui", "Consumo frecuente", "Autoservicio", "autoservicio",
     "Logo_de_Cherdraui.svg", 'Chedraui'),
    ("CUERVO", "CUERVO.MX", "Becle · José Cuervo", "Consumo frecuente", "Destilados", "destilados",
     "Cuervo_1_Positivo.svg", 'Becle OR "José Cuervo"'),
    ("FEMSAUBD", "FEMSAUBD.MX", "FEMSA", "Consumo frecuente", "Comercio y bebidas", "comercio_proximidad",
     "FEMSA_Logo.svg", 'FEMSA OR OXXO'),
    ("GAPB", "GAPB.MX", "GAP", "Industriales", "Aeropuertos", "aeropuertos",
     "Grupo_Aeroportuario_del_Pacífico_logo.jpg", '"Grupo Aeroportuario del Pacífico"'),
    ("GCARSOA1", "GCARSOA1.MX", "Grupo Carso", "Industriales", "Conglomerado", "conglomerado",
     "Logo_de_Grupo_Carso.svg", '"Grupo Carso"'),
    ("GCC", "GCC.MX", "GCC", "Materiales", "Cemento", "cemento",
     "Cementos_Chihuahua_GCC_1_Positivo.svg", '"GCC" cemento'),
    ("GENTERA", "GENTERA.MX", "Gentera", "Financieros", "Microfinanzas", "microfinanzas",
     "Logo_de_Gentera.svg", 'Gentera OR "Compartamos Banco"'),
    ("GFINBURO", "GFINBURO.MX", "Inbursa", "Financieros", "Bancos", "bancos",
     "Inbursa_1_Positivo.svg", '"Grupo Financiero Inbursa" OR "Banco Inbursa"'),
    ("GFNORTEO", "GFNORTEO.MX", "Banorte", "Financieros", "Bancos", "bancos",
     "Banorte_logo.svg", 'Banorte'),
    ("GMEXICOB", "GMEXICOB.MX", "Grupo México", "Materiales", "Minería", "mineria",
     "Logo_de_Grupo_México.svg", '"Grupo México"'),
    ("GRUMAB", "GRUMAB.MX", "Gruma", "Consumo frecuente", "Alimentos", "alimentos",
     "Gruma_logo-en.svg", 'Gruma'),
    ("KIMBERA", "KIMBERA.MX", "Kimberly-Clark de México", "Consumo frecuente", "Cuidado personal y del hogar",
     "consumo_hogar", "Kimberly-Clark_logo.svg", '"Kimberly-Clark de México"'),
    ("KOFUBL", "KOFUBL.MX", "Coca-Cola FEMSA", "Consumo frecuente", "Bebidas", "bebidas",
     "coca-cola-femsa.svg", '"Coca-Cola FEMSA"'),
    ("LABB", "LABB.MX", "Genomma Lab", "Salud", "Farmacéutica y cuidado personal", "farma",
     "Genomma_Lab_1_Positivo.svg", '"Genomma Lab"'),
    ("LACOMERUBC", "LACOMERUBC.MX", "La Comer", "Consumo frecuente", "Autoservicio", "autoservicio",
     "La_Comer_1_Positivo.svg", '"La Comer" supermercados'),
    ("LIVEPOLC1", "LIVEPOLC-1.MX", "Liverpool", "Consumo discrecional", "Tiendas departamentales", "departamental",
     "Liverpool_1_Positivo.svg", '"El Puerto de Liverpool"'),
    ("MEGACPO", "MEGACPO.MX", "Megacable", "Comunicaciones", "Cable y banda ancha", "telecom",
     "Megacable.svg", 'Megacable'),
    ("OMAB", "OMAB.MX", "OMA", "Industriales", "Aeropuertos", "aeropuertos",
     "Grupo_Aeroportuario_Centro_Norte_logo.svg", '"Grupo Aeroportuario Centro Norte" OR "OMA" aeropuertos'),
    ("ORBIA", "ORBIA.MX", "Orbia", "Materiales", "Químicos", "quimicos",
     "Orbia_1_Positivo.svg", 'Orbia'),
    ("PEOLES", "PE&OLES.MX", "Peñoles", "Materiales", "Minería", "mineria",
     "Penoles_1_Positivo.svg", 'Peñoles'),
    ("PINFRA", "PINFRA.MX", "Pinfra", "Industriales", "Autopistas", "autopistas",
     "logo pinfra.jpg", 'Pinfra'),
    ("Q", "Q.MX", "Quálitas", "Financieros", "Seguros", "seguros",
     "Qualitas_idMifArUl3_0.svg", 'Quálitas'),
    ("RA", "RA.MX", "Regional · Banregio", "Financieros", "Bancos", "bancos",
     "Logo_de_Banregio.svg", 'Banregio'),
    ("SIGMAFA", "SIGMAFA.MX", "Sigma Foods", "Consumo frecuente", "Alimentos", "alimentos",
     "SigmaFoods_2.png", '"Sigma Foods" OR "Sigma Alimentos"'),
    ("TLEVISACPO", "TLEVISACPO.MX", "Televisa", "Comunicaciones", "Telecom y medios", "telecom",
     "Logo_de_Grupo_Televisa.svg", 'Televisa OR izzi'),
    ("VESTA", "VESTA.MX", "Vesta", "Bienes raíces", "Inmobiliario industrial", "inmobiliario_industrial",
     "vesta logo.png", '"Corporación Inmobiliaria Vesta" OR "Vesta" parques industriales'),
    ("VOLARA", "VOLARA.MX", "Volaris", "Industriales", "Aerolíneas", "aerolinea",
     "Volaris_1_Positivo.svg", 'Volaris'),
    ("WALMEX", "WALMEX.MX", "Walmart de México", "Consumo frecuente", "Autoservicio", "autoservicio",
     "Walmart_México_y_Centroamérica_logo_(2025).svg", 'Walmex OR "Walmart de México"'),
]

# El ETF de réplica del índice de referencia del fondo.
ETF = ("MEXTRAC", "MEXTRAC09.MX", "MEXTRAC 09", "ETF", "Índice de referencia", "etf", "mextrac.svg", None)

# Índices, divisas, tasas y materias primas. "mueve" = emisoras sensibles a la serie.
MACRO = [
    # clave, símbolo Yahoo, nombre, tipo, unidad, emisoras que mueve
    ("IPC", "^MXX", "S&P/BMV IPC", "indice", "pts", []),
    ("SP500", "^GSPC", "S&P 500", "indice", "pts", []),
    ("NASDAQ", "^IXIC", "Nasdaq Composite", "indice", "pts", []),
    ("BOVESPA", "^BVSP", "Bovespa (Brasil)", "indice", "pts", ["FEMSAUBD", "KOFUBL", "AMXB"]),
    ("VIX", "^VIX", "VIX · volatilidad implícita", "indice", "pts", []),
    ("USDMXN", "MXN=X", "Dólar en pesos", "divisa", "MXN", ["AMXB", "GMEXICOB", "PEOLES", "ORBIA", "ALPEKA",
                                                            "CEMEXCPO", "BOLSAA", "GAPB", "ASURB", "VESTA", "CUERVO"]),
    ("EURMXN", "EURMXN=X", "Euro en pesos", "divisa", "MXN", ["ALSEA", "AMXB", "CEMEXCPO"]),
    ("BRLMXN", "BRLMXN=X", "Real brasileño en pesos", "divisa", "MXN", ["FEMSAUBD", "KOFUBL", "AMXB"]),
    ("DXY", "DX-Y.NYB", "Índice dólar (DXY)", "divisa", "pts", []),
    ("UST10", "^TNX", "Bono de EUA a 10 años", "tasa", "%", ["GFNORTEO", "BBAJIOO", "GFINBURO", "RA", "VESTA"]),
    ("UST3M", "^IRX", "Letra de EUA a 3 meses", "tasa", "%", []),
    ("COBRE", "HG=F", "Cobre (USD por libra)", "materia", "USD", ["GMEXICOB"]),
    ("ORO", "GC=F", "Oro (USD por onza)", "materia", "USD", ["PEOLES"]),
    ("PLATA", "SI=F", "Plata (USD por onza)", "materia", "USD", ["PEOLES"]),
    ("BRENT", "BZ=F", "Petróleo Brent (USD)", "materia", "USD", ["ALPEKA", "ORBIA", "VOLARA"]),
    ("WTI", "CL=F", "Petróleo WTI (USD)", "materia", "USD", ["VOLARA", "ALPEKA"]),
    ("GASNAT", "NG=F", "Gas natural (USD por MMBtu)", "materia", "USD", ["ALPEKA", "ORBIA", "CEMEXCPO", "GCC"]),
    ("MAIZ", "ZC=F", "Maíz (centavos por bushel)", "materia", "USc", ["GRUMAB"]),
    ("TRIGO", "ZW=F", "Trigo (centavos por bushel)", "materia", "USc", ["BIMBOA", "GRUMAB"]),
    ("AZUCAR", "SB=F", "Azúcar (centavos por libra)", "materia", "USc", ["KOFUBL", "AC"]),
]

# Series de Banxico (requieren el secreto BANXICO_TOKEN; sin él se omiten).
BANXICO = [
    ("TASA_OBJETIVO", "SF61745", "Tasa objetivo de Banxico", "%"),
    ("TIIE28", "SF43783", "TIIE a 28 días", "%"),
    ("CETES28", "SF43936", "CETES a 28 días", "%"),
    ("FIX", "SF43718", "Tipo de cambio FIX", "MXN"),
    ("INPC", "SP1", "INPC (índice general)", "pts"),
]

GRUPOS = {
    "autoservicio": "Autoservicio", "departamental": "Tiendas departamentales",
    "comercio_proximidad": "Comercio de proximidad", "bebidas": "Bebidas", "alimentos": "Alimentos",
    "destilados": "Destilados", "consumo_hogar": "Productos de consumo", "restaurantes": "Restaurantes",
    "farma": "Farmacéutica", "aeropuertos": "Aeropuertos", "aerolinea": "Aerolínea",
    "autopistas": "Autopistas", "conglomerado": "Conglomerado", "bancos": "Bancos",
    "microfinanzas": "Microfinanzas", "seguros": "Seguros", "bolsa": "Infraestructura de mercados",
    "telecom": "Telecomunicaciones", "mineria": "Minería", "cemento": "Cemento",
    "quimicos": "Químicos", "inmobiliario_industrial": "Inmobiliario industrial", "etf": "ETF",
}

FINANCIERAS = {"bancos", "microfinanzas", "seguros"}


def emisoras(incluir_etf: bool = True) -> list[dict]:
    filas = EMISORAS + ([ETF] if incluir_etf else [])
    return [
        {"t": t, "y": y, "n": n, "sector": s, "sub": sub, "grupo": g, "logo": logo, "q": q}
        for (t, y, n, s, sub, g, logo, q) in filas
    ]


def mapa_yahoo() -> dict[str, str]:
    """Ticker interno → símbolo de Yahoo, para emisoras e instrumentos macro."""
    m = {e["t"]: e["y"] for e in emisoras()}
    m.update({c: y for (c, y, *_r) in MACRO})
    return m


def leer_parametros() -> dict:
    try:
        with open(os.path.join(RAIZ, "parametros.json"), encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def universo_json(fichas: dict | None = None) -> dict:
    """Metadatos que consume la terminal: nombre, sector, bloque en el fondo y peso en el índice."""
    par = leer_parametros()
    bloques = par.get("bloques", {})
    pesos = par.get("pesos_indice", {})
    fichas = fichas or {}
    filas = []
    for e in emisoras():
        f = fichas.get(e["t"], {})
        filas.append({
            "t": e["t"], "y": e["y"], "n": e["n"],
            "nombre": f.get("nombre") or e["n"],
            "sector": e["sector"], "sub": e["sub"], "grupo": e["grupo"], "grupo_n": GRUPOS.get(e["grupo"], e["grupo"]),
            "logo": e["logo"],
            "bloque": bloques.get(e["t"], "FUERA"),
            "peso_indice": pesos.get(e["t"], 0.0),
            "financiera": e["grupo"] in FINANCIERAS,
        })
    return {
        "emisoras": filas,
        "macro": [{"t": c, "y": y, "n": n, "tipo": tipo, "unidad": u, "mueve": mv} for (c, y, n, tipo, u, mv) in MACRO],
        "banxico": [{"t": c, "serie": s, "n": n, "unidad": u} for (c, s, n, u) in BANXICO],
        "grupos": GRUPOS,
        "fondo": {
            "nombre": "Fondo de Inversión ITESM-BBVA · North Star Strategies",
            "benchmark": "MEXTRAC",
            "modelo": par.get("modelo"),
            "inicio": par.get("inicio"), "fin": par.get("fin"),
            "fecha_referencia": par.get("fecha_referencia"),
            "capital": par.get("capital"),
            "cetes28": par.get("cetes28"),
            "comision_pct": par.get("comision_pct"), "iva_pct": par.get("iva_pct"),
            "feriados": par.get("feriados", []),
            "pesos_indice": pesos,
        },
    }
