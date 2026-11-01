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
    assert val["pe"]["valor"] == 15.0 and val["pe"]["detalle"]["fuente"] == "Yahoo Finance"   # Yahoo, coherente con el cálculo
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


if __name__ == "__main__":
    for nombre, fn in list(globals().items()):
        if nombre.startswith("test_"):
            fn()
            print("ok", nombre)
