"""Acceso a Yahoo Finance mediante yfinance.

Cada función devuelve estructuras simples (listas y diccionarios) listas para JSON y
nunca deja escapar una excepción de un solo símbolo: quien llama decide qué hacer
con lo que faltó. yfinance se importa al usarse para que el resto del pipeline (y las
pruebas) funcionen sin tenerlo instalado.
"""
from __future__ import annotations

import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime, timezone
from typing import Any, Callable

from util import limpiar, num

log = logging.getLogger("terminal.yahoo")
_yf = None

# Partidas que se conservan de cada estado financiero (claves de Yahoo, sin espacios).
PARTIDAS = {
    "resultados": [
        "TotalRevenue", "OperatingRevenue", "CostOfRevenue", "GrossProfit", "SellingGeneralAndAdministration",
        "OperatingExpense", "TotalExpenses", "OperatingIncome", "EBITDA", "NormalizedEBITDA", "EBIT",
        "ReconciledDepreciation", "InterestExpense", "InterestIncome", "NetInterestIncome",
        "ProvisionForDoubtfulAccounts", "NetPolicyholderBenefitsAndClaims", "PretaxIncome", "TaxProvision",
        "NetIncome", "NetIncomeCommonStockholders", "MinorityInterests", "DilutedEPS", "BasicEPS",
        "DilutedAverageShares", "BasicAverageShares",
    ],
    "balance": [
        "TotalAssets", "CurrentAssets", "CashAndCashEquivalents", "CashCashEquivalentsAndShortTermInvestments",
        "Receivables", "AccountsReceivable", "Inventory", "NetPPE", "GoodwillAndOtherIntangibleAssets",
        "InvestmentProperties", "NetLoan", "TotalLiabilitiesNetMinorityInterest", "CurrentLiabilities",
        "AccountsPayable", "Payables", "CurrentDebt", "LongTermDebt", "TotalDebt", "NetDebt",
        "CapitalLeaseObligations", "StockholdersEquity", "CommonStockEquity", "TotalEquityGrossMinorityInterest",
        "MinorityInterest", "InvestedCapital", "WorkingCapital", "TangibleBookValue", "OrdinarySharesNumber",
        "ShareIssued", "RetainedEarnings",
    ],
    "flujo": [
        "OperatingCashFlow", "CapitalExpenditure", "FreeCashFlow", "InvestingCashFlow", "FinancingCashFlow",
        "CashDividendsPaid", "CommonStockDividendPaid", "RepurchaseOfCapitalStock", "IssuanceOfDebt",
        "RepaymentOfDebt", "DepreciationAndAmortization", "ChangeInWorkingCapital", "InterestPaidCFO",
        "InterestPaidCFF",
    ],
}

CAMPOS_INFO = [
    # perfil
    "longName", "shortName", "sector", "industry", "website", "irWebsite", "longBusinessSummary",
    "fullTimeEmployees", "country", "city",
    # mercado
    "currency", "financialCurrency", "marketCap", "enterpriseValue", "sharesOutstanding", "floatShares",
    "impliedSharesOutstanding", "beta", "fiftyTwoWeekHigh", "fiftyTwoWeekLow", "fiftyDayAverage",
    "twoHundredDayAverage", "averageVolume", "averageVolume10days", "52WeekChange", "heldPercentInsiders",
    "heldPercentInstitutions",
    # valuación
    "trailingPE", "forwardPE", "priceToBook", "priceToSalesTrailing12Months", "enterpriseToRevenue",
    "enterpriseToEbitda", "trailingPegRatio",
    # dividendos
    "dividendRate", "dividendYield", "trailingAnnualDividendRate", "trailingAnnualDividendYield", "payoutRatio",
    "fiveYearAvgDividendYield", "exDividendDate", "lastDividendValue", "lastDividendDate",
    # rentabilidad y crecimiento
    "profitMargins", "grossMargins", "operatingMargins", "ebitdaMargins", "returnOnAssets", "returnOnEquity",
    "revenueGrowth", "earningsGrowth", "earningsQuarterlyGrowth",
    # balance y flujo
    "totalCash", "totalCashPerShare", "totalDebt", "debtToEquity", "currentRatio", "quickRatio", "totalRevenue",
    "revenuePerShare", "grossProfits", "ebitda", "netIncomeToCommon", "operatingCashflow", "freeCashflow",
    "bookValue", "trailingEps", "forwardEps",
    # analistas
    "recommendationKey", "recommendationMean", "numberOfAnalystOpinions", "targetMeanPrice", "targetHighPrice",
    "targetLowPrice", "targetMedianPrice", "averageAnalystRating",
    # gobierno corporativo (ISS, escala 1 = bajo riesgo a 10 = alto)
    "auditRisk", "boardRisk", "compensationRisk", "shareHolderRightsRisk", "overallRisk",
]
_FECHAS_EPOCH = {"exDividendDate", "lastDividendDate"}


def yf():
    """Importa yfinance una sola vez y lo configura para que las excepciones lleguen hasta aquí."""
    global _yf
    if _yf is None:
        import yfinance  # noqa: WPS433 (importación tardía a propósito)
        try:
            yfinance.config.debug.hide_exceptions = False
            yfinance.config.network.retries = 2
        except Exception:  # versiones viejas sin config
            pass
        _yf = yfinance
    return _yf


def reintentar(fn: Callable[[], Any], intentos: int = 3, espera: float = 3.0, etiqueta: str = "") -> Any:
    ultimo = None
    for i in range(1, intentos + 1):
        try:
            return fn()
        except Exception as e:  # red, límite de peticiones, JSON incompleto
            ultimo = e
            nombre = type(e).__name__
            pausa = espera * i * (4 if "RateLimit" in nombre or "429" in str(e) else 1)
            if i < intentos:
                log.info("%s: intento %d falló (%s: %s); reintento en %.0fs", etiqueta, i, nombre, str(e)[:120], pausa)
                time.sleep(pausa)
    raise ultimo  # type: ignore[misc]


def en_paralelo(fn: Callable[[str], Any], claves: list[str], hilos: int = 6) -> tuple[dict, dict]:
    """Corre fn(clave) en paralelo. Devuelve (resultados, errores)."""
    ok, errores = {}, {}
    with ThreadPoolExecutor(max_workers=hilos) as ex:
        futuros = {ex.submit(fn, c): c for c in claves}
        for fu in as_completed(futuros):
            c = futuros[fu]
            try:
                r = fu.result()
                if r is not None:
                    ok[c] = r
                else:
                    errores[c] = "sin datos"
            except Exception as e:
                errores[c] = f"{type(e).__name__}: {str(e)[:160]}"
    return ok, errores


def _fecha(idx: Any) -> str:
    if hasattr(idx, "date"):
        return idx.date().isoformat()
    return str(idx)[:10]


# ───────────────────────────── precios ─────────────────────────────

def cotizacion_intradia(simbolo: str) -> dict | None:
    """Barras de 5 minutos de la última sesión y la cotización que reporta Yahoo en el meta."""
    def pedir():
        t = yf().Ticker(simbolo)
        h = t.history(period="1d", interval="5m", auto_adjust=False, prepost=False)
        try:
            meta = t.get_history_metadata() or {}
        except Exception:
            meta = getattr(t, "history_metadata", {}) or {}
        return h, meta

    h, meta = reintentar(pedir, etiqueta=f"intradía {simbolo}")
    barras = []
    if h is not None and len(h):
        for idx, fila in h.iterrows():
            c = num(fila.get("Close"))
            if c is None:
                continue
            ts = idx.tz_convert("UTC") if getattr(idx, "tzinfo", None) else idx
            barras.append([ts.strftime("%Y-%m-%dT%H:%M:%SZ"), round(c, 4), int(num(fila.get("Volume")) or 0)])
    precio = num(meta.get("regularMarketPrice")) or (barras[-1][1] if barras else None)
    if precio is None:
        return None
    anterior = num(meta.get("previousClose")) or num(meta.get("chartPreviousClose"))
    apertura = num(h.iloc[0]["Open"]) if h is not None and len(h) else None
    ts = meta.get("regularMarketTime")
    if isinstance(ts, (int, float)):
        ts = datetime.fromtimestamp(ts, timezone.utc).isoformat()
    elif isinstance(ts, datetime):
        ts = ts.astimezone(timezone.utc).isoformat()
    vol = num(meta.get("regularMarketVolume"))
    if vol is None and barras:
        vol = sum(b[2] for b in barras)
    return limpiar({
        "p": precio,
        "a": anterior,
        "ab": apertura,
        "max": num(meta.get("regularMarketDayHigh")),
        "min": num(meta.get("regularMarketDayLow")),
        "v": vol,
        "hi52": num(meta.get("fiftyTwoWeekHigh")),
        "lo52": num(meta.get("fiftyTwoWeekLow")),
        "m": meta.get("currency"),
        "ts": ts,
        "barras": barras,
    })


def velas(simbolo: str, periodo: str = "5y") -> dict | None:
    """Velas diarias sin ajustar (O, H, L, C, volumen) más dividendos y splits."""
    def pedir():
        return yf().Ticker(simbolo).history(period=periodo, interval="1d", auto_adjust=False, actions=True)

    h = reintentar(pedir, etiqueta=f"velas {simbolo}")
    if h is None or not len(h):
        return None
    d, o, hi, lo, c, v, div, spl = [], [], [], [], [], [], [], []
    for idx, fila in h.iterrows():
        cierre = num(fila.get("Close"))
        if cierre is None or cierre <= 0:
            continue
        f = _fecha(idx)
        d.append(f)
        c.append(round(cierre, 4))
        o.append(round(num(fila.get("Open")) or cierre, 4))
        hi.append(round(num(fila.get("High")) or cierre, 4))
        lo.append(round(num(fila.get("Low")) or cierre, 4))
        v.append(int(num(fila.get("Volume")) or 0))
        dv = num(fila.get("Dividends"))
        if dv:
            div.append([f, round(dv, 6)])
        sp = num(fila.get("Stock Splits"))
        if sp:
            spl.append([f, sp])
    if not d:
        return None
    return {"d": d, "o": o, "h": hi, "l": lo, "c": c, "v": v, "div": div, "split": spl}


# ───────────────────────────── fundamentales ─────────────────────────────

def info(simbolo: str) -> dict | None:
    datos = reintentar(lambda: yf().Ticker(simbolo).info, etiqueta=f"info {simbolo}")
    if not datos or len(datos) < 5:
        return None
    out = {}
    for k in CAMPOS_INFO:
        v = datos.get(k)
        if v is None:
            continue
        if k in _FECHAS_EPOCH and isinstance(v, (int, float)):
            v = datetime.fromtimestamp(v, timezone.utc).date().isoformat()
        if k == "longBusinessSummary" and isinstance(v, str):
            v = v[:1500]
        out[k] = v
    oficiales = datos.get("companyOfficers") or []
    out["directivos"] = [{"nombre": x.get("name"), "cargo": x.get("title")} for x in oficiales[:6] if x.get("name")]
    return limpiar(out)


def _tabla(df: Any, claves: list[str]) -> dict | None:
    """DataFrame de yfinance (partidas × fechas, de la más nueva a la más vieja) → JSON cronológico."""
    if df is None or not hasattr(df, "columns") or df.empty:
        return None
    columnas = sorted(df.columns)  # cronológico
    periodos = [_fecha(c) for c in columnas]
    filas = {}
    for k in claves:
        if k in df.index:
            valores = [num(df.at[k, c]) for c in columnas]
            if any(v is not None for v in valores):
                filas[k] = valores
    if not filas:
        return None
    return {"periodos": periodos, "filas": filas}


def estados(simbolo: str) -> dict | None:
    t = yf().Ticker(simbolo)
    out, errores = {}, []
    pedidos = [
        ("resultados", "trimestral", lambda: t.get_income_stmt(freq="quarterly")),
        ("resultados", "anual", lambda: t.get_income_stmt(freq="yearly")),
        ("resultados", "udm", lambda: t.get_income_stmt(freq="trailing")),
        ("balance", "trimestral", lambda: t.get_balance_sheet(freq="quarterly")),
        ("balance", "anual", lambda: t.get_balance_sheet(freq="yearly")),
        ("flujo", "trimestral", lambda: t.get_cash_flow(freq="quarterly")),
        ("flujo", "anual", lambda: t.get_cash_flow(freq="yearly")),
        ("flujo", "udm", lambda: t.get_cash_flow(freq="trailing")),
    ]
    for estado, freq, fn in pedidos:
        try:
            tabla = _tabla(reintentar(fn, intentos=2, etiqueta=f"{estado}/{freq} {simbolo}"), PARTIDAS[estado])
            if tabla:
                out.setdefault(estado, {})[freq] = tabla
        except Exception as e:
            errores.append(f"{estado}/{freq}: {type(e).__name__}")
    if not out:
        return None
    if errores:
        out["avisos"] = errores
    return limpiar(out)


def multiplos_historicos(simbolo: str) -> dict | None:
    """Múltiplos trimestrales que publica Yahoo (P/U, VE/UAFIDA, P/VL...) para comparar contra su propia historia."""
    try:
        df = reintentar(lambda: yf().Ticker(simbolo).get_valuation_measures(freq="quarterly", periods=12),
                        intentos=2, etiqueta=f"múltiplos {simbolo}")
    except Exception:
        return None
    if df is None or df.empty:
        return None
    etiquetas = {"Trailing P/E": "pe", "Forward P/E": "pe_fwd", "Price/Book": "p_vl", "Price/Sales": "p_ventas",
                 "Enterprise Value/EBITDA": "ve_uafida", "Enterprise Value/Revenue": "ve_ventas",
                 "Market Cap": "valor_mercado", "Enterprise Value": "valor_empresa"}
    cols = [c for c in df.columns if c != "Current"]
    fechas = []
    for c in cols:
        try:
            m, d, y = (int(x) for x in str(c).split("/"))
            fechas.append(date(y, m, d).isoformat())
        except ValueError:
            fechas.append(str(c))
    orden = sorted(range(len(cols)), key=lambda i: fechas[i])
    out = {"periodos": [fechas[i] for i in orden], "filas": {}, "actual": {}}
    for etq, clave in etiquetas.items():
        if etq not in df.index:
            continue
        out["actual"][clave] = num(df.at[etq, "Current"]) if "Current" in df.columns else None
        out["filas"][clave] = [num(df.at[etq, cols[i]]) for i in orden]
    return limpiar(out)


def eventos(simbolo: str) -> dict:
    """Calendario (reporte, dividendo), consenso de analistas y precio objetivo."""
    t = yf().Ticker(simbolo)
    out: dict = {}
    try:
        cal = reintentar(lambda: t.calendar, intentos=2, etiqueta=f"calendario {simbolo}") or {}
        fechas = cal.get("Earnings Date") or []
        out["reporte"] = [f.isoformat() if hasattr(f, "isoformat") else str(f) for f in fechas][:2]
        for k_yf, k in (("Ex-Dividend Date", "ex_dividendo"), ("Dividend Date", "pago_dividendo")):
            if cal.get(k_yf):
                v = cal[k_yf]
                out[k] = v.isoformat() if hasattr(v, "isoformat") else str(v)
        for k_yf, k in (("Earnings Average", "upa_estimada"), ("Revenue Average", "ventas_estimadas")):
            if num(cal.get(k_yf)) is not None:
                out[k] = num(cal[k_yf])
    except Exception as e:
        out["aviso_calendario"] = type(e).__name__
    try:
        rec = reintentar(lambda: t.recommendations, intentos=2, etiqueta=f"recomendaciones {simbolo}")
        if rec is not None and len(rec):
            fila = rec.iloc[0].to_dict()          # periodo 0m = mes en curso
            out["recomendaciones"] = {k: int(num(fila.get(k)) or 0)
                                      for k in ("strongBuy", "buy", "hold", "sell", "strongSell")}
    except Exception as e:
        out["aviso_recomendaciones"] = type(e).__name__
    try:
        obj = reintentar(lambda: t.analyst_price_targets, intentos=2, etiqueta=f"objetivo {simbolo}") or {}
        out["objetivo"] = {k: num(v) for k, v in obj.items() if num(v) is not None}
    except Exception as e:
        out["aviso_objetivo"] = type(e).__name__
    return limpiar(out)


def noticias_yahoo(simbolo: str, n: int = 8) -> list[dict]:
    try:
        items = reintentar(lambda: yf().Ticker(simbolo).get_news(count=n), intentos=2, etiqueta=f"noticias {simbolo}")
    except Exception:
        return []
    out = []
    for it in items or []:
        c = it.get("content") or it
        titulo = c.get("title")
        if not titulo:
            continue
        url = (c.get("canonicalUrl") or {}).get("url") or (c.get("clickThroughUrl") or {}).get("url") or c.get("link")
        fecha = c.get("pubDate") or c.get("displayTime") or ""
        if isinstance(c.get("providerPublishTime"), (int, float)):
            fecha = datetime.fromtimestamp(c["providerPublishTime"], timezone.utc).isoformat()
        out.append({
            "titulo": titulo, "url": url or "", "fecha_utc": str(fecha),
            "fuente": (c.get("provider") or {}).get("displayName") or c.get("publisher") or "Yahoo Finance",
            "resumen": (c.get("summary") or "")[:400],
        })
    return out
