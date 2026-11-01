"""Pruebas del pipeline sin red: un yfinance falso devuelve tablas con la misma forma que el real
(partidas × fechas, de la más nueva a la más vieja) para validar conversiones y KPIs.

    python -m pytest terminal/pipeline/pruebas -q        (o)        python terminal/pipeline/pruebas/test_pipeline.py
"""
from __future__ import annotations

import json
import math
import os
import shutil
import sys
import tempfile
import types
from datetime import datetime, timedelta, timezone

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))

import pandas as pd  # noqa: E402

import actualizar as A  # noqa: E402
import fuente_noticias as N  # noqa: E402
import fuente_yahoo as Y  # noqa: E402
import kpis as K  # noqa: E402
import universo as U  # noqa: E402

TRIMESTRES = [pd.Timestamp(x) for x in ("2026-06-30", "2026-03-31", "2025-12-31", "2025-09-30", "2025-06-30")]
ANIOS = [pd.Timestamp(x) for x in ("2025-12-31", "2024-12-31", "2023-12-31", "2022-12-31")]


def _df(filas: dict, columnas: list) -> pd.DataFrame:
    return pd.DataFrame({c: {k: v[i] for k, v in filas.items()} for i, c in enumerate(columnas)}).astype(float)


class TickerFalso:
    def __init__(self, simbolo: str):
        self.s = simbolo
        self.banco = simbolo in ("GFNORTEO.MX", "BBAJIOO.MX")

    # precios
    def history(self, period="1mo", interval="1d", **_):
        tz = "America/Mexico_City"
        if interval == "5m":
            idx = pd.date_range("2026-10-30 08:30", periods=12, freq="5min", tz=tz)
            base = 100.0
            return pd.DataFrame({"Open": base, "High": base + 1, "Low": base - 1,
                                 "Close": [base + i * 0.1 for i in range(12)], "Volume": 1000}, index=idx)
        n = 1300
        idx = pd.bdate_range(end="2026-10-30", periods=n, tz=tz)
        cierre = [100 * math.exp(0.0003 * i + 0.01 * math.sin(i / 7)) for i in range(n)]
        df = pd.DataFrame({"Open": cierre, "High": [c * 1.01 for c in cierre], "Low": [c * 0.99 for c in cierre],
                           "Close": cierre, "Adj Close": cierre, "Volume": 250000, "Dividends": 0.0,
                           "Stock Splits": 0.0}, index=idx)
        df.iloc[-100, df.columns.get_loc("Dividends")] = 1.5
        df.iloc[-5, df.columns.get_loc("Close")] = float("nan")           # una fila mala
        return df

    def get_history_metadata(self):
        return {"regularMarketPrice": 101.1, "previousClose": 100.0, "regularMarketDayHigh": 101.5,
                "regularMarketDayLow": 99.2, "regularMarketVolume": 123456, "fiftyTwoWeekHigh": 120.0,
                "fiftyTwoWeekLow": 80.0, "currency": "MXN", "regularMarketTime": 1793390400}

    # fundamentales
    @property
    def info(self):
        return {"longName": "Empresa de prueba", "currency": "MXN",
                "financialCurrency": "USD" if self.s == "GMEXICOB.MX" else "MXN",
                "marketCap": 500e9, "sharesOutstanding": 5e9, "trailingPE": 15.0, "exDividendDate": 1790000000,
                "companyOfficers": [{"name": "Dir. General", "title": "CEO"}], "sector": "Consumer Defensive",
                "returnOnEquity": 0.2, "recommendationMean": 2.1, "numberOfAnalystOpinions": 12}

    def get_income_stmt(self, freq="yearly"):
        if freq == "trailing":
            return _df({"TotalRevenue": [400e9], "NetIncomeCommonStockholders": [40e9], "EBITDA": [80e9]},
                       [pd.Timestamp("2026-06-30")])
        cols = TRIMESTRES if freq == "quarterly" else ANIOS
        k = 1 if freq == "quarterly" else 4
        ventas = [100e9 * k * (1 - 0.02 * i) for i in range(len(cols))]
        filas = {
            "TotalRevenue": ventas,
            "CostOfRevenue": [v * 0.6 for v in ventas],
            "GrossProfit": [v * 0.4 for v in ventas],
            "OperatingIncome": [v * 0.12 for v in ventas],
            "EBITDA": [v * 0.2 for v in ventas],
            "NetIncomeCommonStockholders": [v * 0.1 for v in ventas],
            "InterestExpense": [v * 0.02 for v in ventas],
            "TaxProvision": [v * 0.03 for v in ventas],
            "PretaxIncome": [v * 0.13 for v in ventas],
            "SellingGeneralAndAdministration": [v * 0.25 for v in ventas],
        }
        if self.banco:
            filas["NetInterestIncome"] = [v * 0.5 for v in ventas]
            filas["ProvisionForDoubtfulAccounts"] = [v * 0.08 for v in ventas]
        return _df(filas, cols)

    def get_balance_sheet(self, freq="yearly"):
        cols = TRIMESTRES if freq == "quarterly" else ANIOS
        filas = {
            "TotalAssets": [900e9] * len(cols), "StockholdersEquity": [300e9] * len(cols),
            "TotalDebt": [150e9] * len(cols), "CashCashEquivalentsAndShortTermInvestments": [50e9] * len(cols),
            "CurrentAssets": [200e9] * len(cols), "CurrentLiabilities": [160e9] * len(cols),
            "Inventory": [40e9] * len(cols), "AccountsReceivable": [30e9] * len(cols),
            "AccountsPayable": [50e9] * len(cols),
        }
        if self.banco:
            filas["NetLoan"] = [600e9 * (1 - 0.02 * i) for i in range(len(cols))]
        df = _df(filas, cols)
        df.loc["Inventory", cols[-1]] = float("nan")                        # hueco típico de Yahoo
        return df

    def get_cash_flow(self, freq="yearly"):
        if freq == "trailing":
            return _df({"OperatingCashFlow": [60e9], "CapitalExpenditure": [-20e9], "FreeCashFlow": [40e9],
                        "CashDividendsPaid": [-15e9]}, [pd.Timestamp("2026-06-30")])
        cols = TRIMESTRES if freq == "quarterly" else ANIOS
        return _df({"OperatingCashFlow": [15e9] * len(cols), "CapitalExpenditure": [-5e9] * len(cols),
                    "FreeCashFlow": [10e9] * len(cols), "CashDividendsPaid": [-4e9] * len(cols)}, cols)

    def get_valuation_measures(self, freq="quarterly", periods=5):
        return pd.DataFrame({"Current": [14.0, 2.0, 8.0], "6/30/2026": [13.0, 1.9, 7.5], "3/31/2026": [12.0, 1.8, 7.0]},
                            index=["Trailing P/E", "Price/Book", "Enterprise Value/EBITDA"])

    @property
    def calendar(self):
        return {"Earnings Date": [datetime(2026, 10, 28).date()], "Ex-Dividend Date": datetime(2026, 11, 15).date(),
                "Earnings Average": 1.2}

    @property
    def recommendations(self):
        return pd.DataFrame([{"period": "0m", "strongBuy": 3, "buy": 5, "hold": 4, "sell": 1, "strongSell": 0}])

    @property
    def analyst_price_targets(self):
        return {"current": 101.1, "high": 140.0, "low": 90.0, "mean": 120.0, "median": 118.0}

    def get_news(self, count=10):
        return [{"content": {"title": "Empresa sube 3% tras reporte", "pubDate": "2026-10-30T15:00:00Z",
                             "provider": {"displayName": "Reuters"}, "canonicalUrl": {"url": "https://x"}}}]


def instalar_yf_falso(falla: set[str] | None = None):
    falla = falla or set()

    class Modulo(types.SimpleNamespace):
        def Ticker(self, s):  # noqa: N802
            if s in falla:
                raise ConnectionError(f"simulado: {s} no respondió")
            return TickerFalso(s)

    Y._yf = Modulo()


def test_conversiones_y_kpis():
    instalar_yf_falso()
    q = Y.cotizacion_intradia("WALMEX.MX")
    assert q["p"] == 101.1 and q["a"] == 100.0 and len(q["barras"]) == 12
    v = Y.velas("WALMEX.MX")
    assert len(v["d"]) == 1299 and v["div"] and v["d"] == sorted(v["d"])       # quitó la fila con NaN
    est = Y.estados("FEMSAUBD.MX")
    assert est["resultados"]["trimestral"]["periodos"][0] == "2025-06-30"       # cronológico
    assert len(est["resultados"]["trimestral"]["filas"]["TotalRevenue"]) == 5
    inf = Y.info("FEMSAUBD.MX")
    assert inf["exDividendDate"].startswith("2026-") and inf["directivos"][0]["cargo"] == "CEO"
    ks = {k["clave"]: k for k in K.financieros("FEMSAUBD", "comercio_proximidad", est, inf, 101.1)}
    # ventas del último trimestre 100 contra 92 del mismo trimestre del año anterior
    assert abs(ks["crec_ventas"]["valor"] - (100 / 92 - 1)) < 1e-6
    assert abs(ks["margen_neto"]["valor"] - 0.1) < 1e-6                        # UDM trailing: 40/400
    assert abs(ks["deuda_neta_uafida"]["valor"] - (100e9 / 80e9)) < 1e-6
    assert abs(ks["flujo_libre"]["valor"] - 40e9) < 1
    assert ks["roe"]["valor"] and 0.1 < ks["roe"]["valor"] < 0.2
    val = {k["clave"]: k for k in K.valuacion("FEMSAUBD", "comercio_proximidad", est, inf, 101.1, 1.0, 3.0,
                                                Y.multiplos_historicos("FEMSAUBD.MX"))}
    assert val["pe"]["valor"] == 15.0 and val["pe"]["detalle"]["fuente"] == "múltiplo reportado (cifras por acción)"   # coherente con el cálculo
    assert val["pe"]["serie"][-1]["p"] == "2T26"
    banco = {k["clave"]: k for k in K.financieros("GFNORTEO", "bancos", Y.estados("GFNORTEO.MX"), inf, 100)}
    assert banco["costo_riesgo"]["valor"] > 0 and "margen_bruto" not in banco
    ev = Y.eventos("FEMSAUBD.MX")
    assert ev["reporte"] == ["2026-10-28"] and ev["recomendaciones"]["buy"] == 5 and ev["objetivo"]["mean"] == 120


def test_conversion_moneda_en_valuacion():
    instalar_yf_falso()
    est = Y.estados("GMEXICOB.MX")
    inf = dict(Y.info("GMEXICOB.MX"), trailingPE=None)
    sin = {k["clave"]: k["valor"] for k in K.valuacion("GMEXICOB", "mineria", est, inf, 100, 1.0, None, None)}
    con = {k["clave"]: k["valor"] for k in K.valuacion("GMEXICOB", "mineria", est, inf, 100, 18.0, None, None)}
    assert abs(sin["pe"] / con["pe"] - 18.0) < 1e-4
    # Si el P/U de Yahoo discrepa 18 veces del propio (moneda sin convertir), gana el cálculo propio.
    inf2 = dict(inf, trailingPE=12.5)
    con2 = {k["clave"]: k for k in K.valuacion("GMEXICOB", "mineria", est, inf2, 100, 18.0, None, None)}
    assert con2["pe"]["detalle"]["fuente"] == "cálculo de la terminal" and abs(con2["pe"]["valor"] - con["pe"]) < 1e-9


def test_corrida_completa_con_fallas():
    """Modo completo con dos símbolos caídos: no se cae y conserva lo previo."""
    instalar_yf_falso(falla={"AC.MX", "^MXX"})
    tmp = tempfile.mkdtemp()
    try:
        assert A.correr("semilla", tmp) == 0
        previo_ac = json.load(open(os.path.join(tmp, "velas", "AC.json")))
        # sin red para noticias
        N.buscar = lambda *a, **k: [{"titulo": "Cemex gana contrato", "url": "u", "fuente": "El Financiero",
                                     "fecha_utc": datetime.now(timezone.utc).isoformat(), "tono": "positiva"}]
        assert A.correr("completo", tmp) == 0
        estado = json.load(open(os.path.join(tmp, "estado.json")))
        assert any("AC" in a for a in estado["avisos"])
        assert json.load(open(os.path.join(tmp, "velas", "AC.json")))["d"] == previo_ac["d"]   # conservado
        kp = json.load(open(os.path.join(tmp, "kpis.json")))
        assert kp["emisoras"]["FEMSAUBD"]["kpis"] and kp["definiciones"]["roe"]["nombre"].startswith("ROE")
        assert kp["emisoras"]["FEMSAUBD"]["ultimo_trimestre"] == "2T26"
        port = json.load(open(os.path.join(tmp, "portafolio.json")))
        assert port["actual"]["posiciones"] and port["serie"]
        noticias = json.load(open(os.path.join(tmp, "noticias.json")))["items"]
        assert any(n["origen"] == "google" for n in noticias) and any(n["origen"] == "equipo" for n in noticias)
        assert A.correr("rapido", tmp) == 0
        cot = json.load(open(os.path.join(tmp, "cotizaciones.json")))
        assert cot["q"]["WALMEX"]["p"] == 101.1 and cot["q"]["AC"].get("conservado")
        assert os.path.exists(os.path.join(tmp, "legado", "cotizaciones.csv"))
    finally:
        shutil.rmtree(tmp)


def test_tono_y_palabras():
    assert N.tono("Walmex sube 4% y supera estimados")[0] == "positiva"
    assert N.tono("Peñoles cae tras recorte de producción")[0] == "negativa"
    assert N.palabras_clave('FEMSA OR OXXO') == ["femsa", "oxxo"]
    assert N.palabras_clave('"Grupo Bimbo"') == ["grupo bimbo"]
    assert N.palabras_clave('Megacable -Pereira -teleférico') == ["megacable"]
    assert N.excluidas('Megacable -Pereira -teleférico') == ["pereira", "teleferico"]
    assert N.es_ruido("Ven con nosotros al Estadio Banorte") and not N.es_ruido("Banorte eleva su guía de utilidad")


def test_trimestre_roto_y_crecimiento():
    """Un trimestre con ingresos negativos (dato roto de Yahoo) no debe producir crecimientos absurdos."""
    est = {"resultados": {"trimestral": {"periodos": ["2025-03-31", "2025-06-30", "2025-09-30", "2025-12-31", "2026-03-31", "2026-06-30"],
                                         "filas": {"TotalRevenue": [63406e6, -13555e6, None, 57788e6, 67892e6, 62586e6],
                                                   "NetIncomeCommonStockholders": [15288e6, -670e6, None, 15874e6, 15458e6, 15550e6]}},
                          "anual": {"periodos": ["2024-12-31", "2025-12-31"], "filas": {"TotalRevenue": [219384e6, 247467e6]}}}}
    ks = {k["clave"]: k for k in K.financieros("GFNORTEO", "bancos", est, {}, 200)}
    assert ks["crec_ventas"]["valor"] is None and ks["crec_utilidad"]["valor"] is None
    assert abs(ks["crec_ventas_udm"]["valor"] - (247467 / 219384 - 1)) < 1e-6 and ks["crec_ventas_udm"]["periodo"] == "2025"
    assert "eficiencia" not in ks
    # Trimestre más reciente publicado a medias (sin ingresos): se mide contra el último válido.
    est2 = {"resultados": {"trimestral": {"periodos": ["2025-06-30", "2025-09-30", "2025-12-31", "2026-03-31", "2026-06-30", "2026-09-30"],
                                          "filas": {"TotalRevenue": [100e6, 110e6, 120e6, 130e6, 115e6, None],
                                                    "NetIncomeCommonStockholders": [10e6, 11e6, 12e6, 13e6, 12e6, 9e6]}}}}
    ks2 = {k["clave"]: k for k in K.financieros("BOLSAA", "bolsa", est2, {}, 30)}
    assert abs(ks2["crec_ventas"]["valor"] - 0.15) < 1e-9 and ks2["crec_ventas"]["periodo"] == "2T26"
    assert K.ultimo_valido(est2) == 4
    # Trimestre faltante en la lista de Yahoo: el a/a se busca por fecha, no por posición.
    est3 = {"resultados": {"trimestral": {"periodos": ["2025-03-31", "2025-06-30", "2025-12-31", "2026-03-31", "2026-06-30", "2026-09-30"],
                                          "filas": {"TotalRevenue": [90e6, 100e6, 120e6, 95e6, 110e6, 130e6]}}},
            "balance": {"trimestral": {"periodos": ["2025-06-30", "2025-12-31", "2026-06-30"],
                                       "filas": {"NetLoan": [500e6, 520e6, 560e6], "TotalAssets": [900e6, 950e6, 1000e6]}}}}
    ks3 = {k["clave"]: k for k in K.financieros("RA", "bancos", est3, {}, 100)}
    assert ks3["crec_ventas"]["valor"] is None                                     # 3T25 no viene: no se inventa
    s3 = {x["p"]: x["v"] for x in ks3["crec_ventas"]["serie"]}
    assert s3["2T26"] == 110e6
    assert abs(ks3["crec_cartera"]["valor"] - (560 / 500 - 1)) < 1e-9               # 2T26 contra 2T25 por fecha
    assert K._consecutivos(["2025-12-31", "2026-03-31", "2026-06-30", "2026-09-30"], 4)
    assert not K._consecutivos(["2025-06-30", "2025-12-31", "2026-03-31", "2026-06-30"], 4)
    from util import crecimiento
    assert crecimiento(10, -5) is None and crecimiento(10, 0) is None and abs(crecimiento(12, 10) - 0.2) < 1e-12


def test_rsi_y_caida():
    assert K.rsi([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]) == 100.0
    assert abs(K.max_caida([100, 120, 90, 130]) - (90 / 120 - 1)) < 1e-12


# ───────────────────────────── atribución, investigación y sensibilidades ─────────────────────────────

def test_atribucion_cuadra_con_tracker():
    """Con las operaciones y cierres oficiales del repo, la atribución reproduce al tracker de Excel y cuadra con el alfa."""
    import fichas as F
    import portafolio as P
    from util import num
    par = U.leer_parametros()
    ops = F.leer_csv("operaciones.csv")
    hist = {r["fecha"]: r for r in F.leer_csv("historico.csv")}
    if not ops or not hist or not F.leer_csv("atribucion_diaria.csv"):
        return                                                    # repositorio sin datos del fondo
    pesos = par["pesos_indice"]
    ticks = set(pesos) | {o["simbolo"] for o in ops} | {"MEXTRAC"}
    cierres = {f: {t: num(r.get(t)) for t in ticks if num(r.get(t)) is not None} for f, r in hist.items() if f >= "2026-10-01"}
    sin_op = {f for f in cierres if num(hist[f].get("MEXTRAC")) is None}
    v = {}
    pt, at = A.tracker_atribucion()
    divs = A.dividendos_por_fecha(v, ticks)
    a = P.atribucion(ops, cierres, float(par["capital"]), par["fecha_referencia"], pesos, par.get("fecha_ref_indice"), sin_op,
                     divs, pt, at, par.get("bloques"), par.get("inicio"))
    serie = P.serie_diaria(ops, cierres, float(par["capital"]), par["fecha_referencia"], pesos, sin_op)
    assert abs(a["alfa"] - serie[-1]["activo_acum"]) < 1e-6                      # cuadra con la serie del fondo (6 decimales)
    assert abs(a["suma"] - a["alfa"]) < 1e-9                                    # Σ componentes = alfa
    assert abs(sum(x["aporte"] for x in a["posiciones"]) - a["componentes"]["emisoras"]) < 1e-6   # redondeo a 8 decimales
    assert a["verificacion"]["comparados"] > 300 and a["verificacion"]["max_dif"] < 1e-10   # igual al tracker
    assert abs(a["componentes"]["residual"]) < 1e-9
    estados = {x["estado"] for x in a["posiciones"]}
    assert "abierta" in estados and "indice" in estados
    ventas = a["ventas"]
    assert ventas and all(x["titulos"] > 0 for x in ventas)


def test_atribucion_posicion_cerrada():
    """Una emisora que se vende completa pasa a «cerrada» y conserva su aporte mientras se tuvo."""
    import portafolio as P
    ops = [{"fecha": "2026-01-02", "simbolo": "AAA", "tipo": "COMPRA", "titulos": "100", "precio": "10", "caja": "-1000"},
           {"fecha": "2026-01-02", "simbolo": "MEXTRAC", "tipo": "COMPRA", "titulos": "100", "precio": "10", "caja": "-1000"},
           {"fecha": "2026-01-06", "simbolo": "AAA", "tipo": "VENTA", "titulos": "100", "precio": "12", "caja": "1200"}]
    px = {"2026-01-02": (10, 10, 10), "2026-01-05": (11, 10.2, 10.1), "2026-01-06": (12, 10.4, 10.3), "2026-01-07": (12.5, 10.5, 10.6)}
    cierres = {f: {"AAA": a, "BBB": b, "MEXTRAC": m} for f, (a, b, m) in px.items()}
    pesos = {"AAA": 0.5, "BBB": 0.5}
    a = P.atribucion(ops, cierres, 2000.0, "2026-01-02", pesos, None, set(), {}, None, None, {}, "2026-01-02")
    serie = P.serie_diaria(ops, cierres, 2000.0, "2026-01-02", pesos, set())
    assert abs(a["alfa"] - serie[-1]["activo_acum"]) < 1e-12
    fila = {x["t"]: x for x in a["posiciones"]}
    assert fila["AAA"]["estado"] == "cerrada" and fila["BBB"]["estado"] == "indice"
    assert fila["AAA"]["dias_tenencia"] == 2 and abs(fila["AAA"]["pyg_realizado"] - 200) < 1e-9
    assert a["ventas"][0]["cierre_total"] is True
    assert abs(a["suma"] - a["alfa"]) < 1e-12


def test_dividendos_se_suman_y_no_se_duplican():
    v = {"FEMSAUBD": {"div": [["2026-10-15", 3.0]]}, "AC": {"div": [["2026-10-27", 2.0], ["2011-01-03", 1.0]]}}
    d = A.dividendos_por_fecha(v, {"FEMSAUBD", "AC"})
    if not A.F.leer_csv("dividendos.csv"):
        return
    assert abs(d["2026-10-14"]["FEMSAUBD"] - (2.014925 + 1.188)) < 1e-9      # dos pagos el mismo día se suman
    assert "2026-10-15" not in d or "FEMSAUBD" not in d["2026-10-15"]         # el de las velas, a ±3 días, no se duplica
    assert d["2026-10-27"]["AC"] == 2.0 and d["2011-01-03"]["AC"] == 1.0       # sin registro de Refinitiv: se toma de las velas


def test_calendario_sin_dividendos_duplicados():
    ev = A.armar_calendario({"GAPB": {"ex_dividendo": "2026-11-05"}, "KOFUBL": {"ex_dividendo": "2099-01-01"}})
    if not any(e["t"] == "GAPB" and "ividendo" in e["tipo"] for e in ev["eventos"] if e.get("fuente") == "LSEG"):
        return
    gap = [e for e in ev["eventos"] if e["t"] == "GAPB" and e["fecha"] == "2026-11-05"]
    assert len(gap) == 1 and gap[0]["fuente"] == "LSEG"
    assert any(e["t"] == "KOFUBL" and e["fecha"] == "2099-01-01" for e in ev["eventos"])
    assert not any("Yahoo" in (e.get("fuente") or "") + (e.get("titulo") or "") for e in ev["eventos"])


def test_investigacion_por_emisora():
    import investigacion as INV
    docs = INV.leer_todo()["documentos"]
    if not docs:
        return
    d = docs[0]
    assert d["corte"] and len(d["emisoras"]) == 37 and len(d["resumen"]) == 37
    fem = d["emisoras"]["FEMSAUBD"]
    assert fem["nivel"] == 1 and fem["modelo"].startswith("El valor de FEMSA")
    assert fem["tablas"] and fem["tablas"][0]["cols"][0] == "KPI" and len(fem["tablas"][0]["filas"]) >= 10
    assert [p["clave"] for p in fem["piezas"] if p["tipo"] == "texto"][:2] == ["modelo", "narrativa"]
    assert d["emisoras"]["GAPB"]["juicio"].startswith("GAP es la mayor")
    assert d["emisoras"]["OMAB"]["juicio"]                                     # viene en una viñeta
    assert d["emisoras"]["VOLARA"]["nombre"] == "Volaris"                     # «Nivel 3 — Volaris (VOLARA)»
    assert d["emisoras"]["VESTA"]["compacto"] and d["emisoras"]["Q"]["modelo"]
    macro = {m["catalizador"]: m["emisoras"] for m in d["macro"]}
    assert "BBAJIOO" in macro["Tasa de Banxico"] and "GMEXICOB" in macro["Cobre y plata"]
    assert INV.tickers_en("GMéxico/Peñoles (costos en MXN), GAP/ASUR/OMA") == ["GMEXICOB", "PEOLES", "GAPB", "ASURB", "OMAB"]


def test_sensibilidad_puente_de_valuacion():
    import sensibilidad as S
    cfg = {"impuestos": 0.30, "sector": {"aeropuertos": {"margen_incremental": 0.85}}, "emisoras": {
        "X": {"base": "uafida", "drivers": [
            {"id": "v", "n": "Ventas", "unidad": "%", "tipo": "ingresos", "peso": 0.5, "margen_incremental": 0.3, "paso": 1},
            {"id": "m", "n": "Margen", "unidad": "pb", "tipo": "margen", "peso": 1, "paso": 50},
            {"id": "c", "n": "Cobre", "unidad": "%", "tipo": "precio_volumen", "serie": "COBRE", "volumen": 1e9, "fuga": 0.1, "moneda": "USD", "paso": 10},
            {"id": "k", "n": "Cash cost", "unidad": "US$/lb", "tipo": "costo_unitario", "volumen": 1e9, "moneda": "USD", "paso": 0.1}]},
        "B": {"base": "utilidad", "utilidad_base": 1000, "cartera": 20000, "drivers": [
            {"id": "min", "n": "MIN", "unidad": "pb", "tipo": "min", "paso": 10},
            {"id": "c", "n": "Cartera", "unidad": "pp", "tipo": "cartera", "spread": 0.05, "paso": 1}]}}}
    kp = {"ve_uafida": 10.0, "deuda_neta_uafida": 2.0, "margen_uafida": 0.2, "margen_bruto": 0.4}
    m = S.modelo_emisora("X", "mineria", kp, {"ebitda": 4e9, "financialCurrency": "USD"}, 100.0, 20.0, None, cfg, {"COBRE": 5.0})
    L = 10 / 8
    d = {x["id"]: x for x in m["drivers"]}
    assert abs(m["base"]["L"] - L) < 1e-12
    assert abs(d["v"]["e_precio"] - L * 0.5 * 0.3 / 0.2 / 100) < 1e-12         # 1% de ventas
    assert abs(d["m"]["efecto_paso"] - L * 50 / 1e4 / 0.2) < 1e-12               # +50 pb de margen
    assert abs(d["c"]["e_base"] - 0.01 * 5.0 * 1e9 * 0.9 / 1e6 / 4000) < 1e-12  # 1% de precio × volumen
    assert d["k"]["e_base"] < 0 and abs(d["k"]["e_base"] + 1e9 / 1e6 / 4000) < 1e-12
    b = S.modelo_emisora("B", "bancos", {"pe": 9.0}, {}, 50.0, 20.0, None, cfg, {})
    db = {x["id"]: x for x in b["drivers"]}
    assert abs(db["min"]["e_precio"] - 1e-4 * 20000 * 0.7 / 1000) < 1e-12      # P/U constante
    assert abs(db["c"]["e_precio"] - 0.01 * 20000 * 0.05 * 0.7 / 1000) < 1e-12
    # UAFIDA casi nula: el modelo no se aplica
    z = S.modelo_emisora("Z", "aerolinea", {"ve_uafida": 90.0, "deuda_neta_uafida": 75.0, "margen_uafida": 0.01}, {}, 10.0, 20.0, None, cfg, {})
    assert z["nota"] and all(x["e_precio"] is None for x in z["drivers"])
    # El archivo del equipo es JSON válido y sus drivers tienen tipo conocido
    real = S.leer_drivers()
    tipos = {"ingresos", "margen", "uafida_segmento", "precio_volumen", "costo_unitario", "fx", "min", "costo_riesgo", "cartera", "siniestralidad"}
    for t, e in (real.get("emisoras") or {}).items():
        assert t in {x[0] for x in U.EMISORAS}, t
        for x in e["drivers"]:
            assert x["tipo"] in tipos and x.get("paso"), (t, x["id"])


def test_betas_recuperan_la_sensibilidad():
    import random
    import sensibilidad as S
    random.seed(7)
    fechas, ipc, cu, acc = [], [100.0], [4.0], [50.0]
    d0 = datetime(2024, 1, 1)
    for i in range(1, 760):
        dia = d0 + timedelta(days=i)
        if dia.weekday() >= 5:
            continue
        fechas.append(dia.strftime("%Y-%m-%d"))
        ri, rc = random.gauss(0, 0.01), random.gauss(0, 0.015)
        ipc.append(ipc[-1] * (1 + ri))
        cu.append(cu[-1] * (1 + rc))
        acc.append(acc[-1] * (1 + 0.9 * ri + 0.6 * rc + random.gauss(0, 0.004)))
    n = len(fechas)
    cierres = {"d": fechas, "s": {"IPC": ipc[1:n + 1], "GMEXICOB": acc[1:n + 1]}}
    macro = {"COBRE": {"d": fechas, "c": cu[1:n + 1]}}
    b = S.betas_mercado(cierres, macro, {"COBRE": ["GMEXICOB"]})
    f = b["GMEXICOB"]["factores"][0]
    assert f["clave"] == "COBRE" and abs(f["beta"] - 0.6) < 0.1 and f["t"] > 5 and f["relevante"]
    assert abs(b["GMEXICOB"]["ipc"]["beta"] - 0.9) < 0.25


if __name__ == "__main__":
    for nombre, fn in list(globals().items()):
        if nombre.startswith("test_"):
            fn()
            print("ok", nombre)
