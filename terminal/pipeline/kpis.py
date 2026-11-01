"""KPIs de cada emisora.

Tres familias:
  1. Financieros, calculados de los estados de Yahoo (UDM = últimos doce meses).
  2. De mercado, calculados de las velas diarias (rendimiento, riesgo, liquidez, técnico).
  3. Operativos del sector, que el equipo captura en empresas.txt (kpis:) más un catálogo
     por sector con lo que conviene vigilar y por qué.

Cada KPI sale con su fórmula, el periodo, la serie trimestral (para la mini gráfica) y su
posición contra el sector y contra el universo, para que la pestaña se pueda leer sola.
"""
from __future__ import annotations

import math
from datetime import date, timedelta

from universo import FINANCIERAS
from util import (covarianza, crecimiento, desv, div, etiqueta_trimestre, limpiar, media, mediana, num,
                  percentil_de, zscores)

# ───────────────────────────── catálogo operativo por sector ─────────────────────────────
# (nombre, por qué importa). Es la guía de qué buscar en cada reporte trimestral.
CATALOGO = {
    "autoservicio": [
        ("Ventas mismas tiendas (VMT)", "Crecimiento orgánico sin el efecto de las aperturas: el mejor termómetro del consumo."),
        ("Ticket promedio y tráfico", "Separa cuánto del crecimiento es precio (inflación) y cuánto es más clientes."),
        ("Tiendas nuevas y piso de venta", "Expansión: cuánto crecimiento viene de abrir unidades."),
        ("Margen bruto", "Poder de compra frente a proveedores y mezcla de formatos."),
        ("Margen UAFIDA", "Eficiencia operativa después de gastos de tienda y logística."),
        ("Penetración omnicanal", "Peso del comercio electrónico en las ventas."),
    ],
    "departamental": [
        ("Ventas mismas tiendas", "Termómetro del consumo discrecional de ingreso medio y alto."),
        ("Cartera de crédito propia", "Parte relevante de la utilidad viene del negocio de tarjetas."),
        ("Cartera vencida (IMOR)", "Calidad del crédito al consumo: anticipa provisiones."),
        ("Margen UAFIDA", "Rentabilidad combinada de comercio y crédito."),
        ("Ventas digitales", "Peso del canal en línea."),
    ],
    "comercio_proximidad": [
        ("VMT de OXXO México", "Crecimiento orgánico de la red de tiendas; motor principal de la utilidad."),
        ("Ticket y tráfico OXXO", "Distingue precio de afluencia; el tráfico venía cayendo."),
        ("Margen operativo OXXO", "Rentabilidad del negocio principal."),
        ("Tiendas netas abiertas", "Expansión de la red."),
        ("Usuarios Spin by OXXO / Spin Premia", "Ecosistema digital y de lealtad."),
        ("Deuda neta / UAFIDA", "Apalancamiento del grupo."),
    ],
    "bebidas": [
        ("Volumen (millones de cajas unidad)", "Crecimiento físico: aísla el efecto de precio."),
        ("Precio por caja unidad", "Capacidad de trasladar inflación al consumidor."),
        ("Margen bruto", "Costo de edulcorantes, PET y aluminio, y coberturas."),
        ("Margen UAFIDA", "Rentabilidad tras gastos de distribución."),
        ("Mezcla por región", "México contra Sudamérica o EUA: diversificación del resultado."),
    ],
    "alimentos": [
        ("Volumen", "Demanda física de sus productos."),
        ("Precio / mezcla", "Traslado de costos al anaquel."),
        ("Costo de materias primas", "Trigo, maíz, aceites, cárnicos: el principal riesgo de margen."),
        ("Margen UAFIDA", "Eficiencia de la operación integrada."),
        ("Ventas por región", "Peso de EUA y Europa frente a México; efecto cambiario."),
        ("Deuda neta / UAFIDA", "Holgura financiera."),
    ],
    "destilados": [
        ("Volumen (millones de cajas de 9 L)", "Demanda física, sobre todo en EUA y Canadá."),
        ("Precio / mezcla", "Peso de las marcas premium."),
        ("Margen bruto", "Costo del agave y efecto cambiario."),
        ("Inventarios", "Capital de trabajo atado en agave y producto añejado."),
    ],
    "consumo_hogar": [
        ("Volumen y precio", "Separan demanda de traslado de inflación."),
        ("Margen bruto", "Costo de celulosa, resinas y tipo de cambio."),
        ("Margen UAFIDA", "Rentabilidad tras gastos de venta."),
        ("Dividendo y recompras", "Retorno al accionista, central en la tesis."),
    ],
    "restaurantes": [
        ("Ventas mismas tiendas", "Demanda orgánica por marca y región."),
        ("Unidades abiertas", "Expansión de la red."),
        ("Ventas por región", "México, Europa y Sudamérica."),
        ("Margen UAFIDA pre-NIIF 16", "Rentabilidad sin el efecto contable de las rentas."),
        ("Deuda neta / UAFIDA", "El punto débil histórico de la emisora."),
    ],
    "farma": [
        ("Ventas por región", "México, Argentina, Brasil y EUA: efecto cambiario y de inflación."),
        ("Margen UAFIDA", "Escala y gasto en mercadotecnia."),
        ("Días de capital de trabajo", "Cuentas por cobrar e inventarios: conversión a flujo."),
        ("Flujo libre", "Capacidad de pagar dividendos y recomprar."),
    ],
    "aeropuertos": [
        ("Pasajeros totales", "El motor del ingreso; se publica cada mes."),
        ("Mezcla nacional / internacional", "El internacional paga tarifas más altas en dólares."),
        ("Ingreso aeronáutico por pasajero", "Tarifa máxima regulada y su actualización."),
        ("Ingreso no aeronáutico por pasajero", "Comercios, estacionamiento: crecimiento no regulado."),
        ("Margen UAFIDA ajustado", "Sin los ingresos de construcción."),
        ("Inversión del PMD", "Compromisos del Programa Maestro de Desarrollo."),
    ],
    "aerolinea": [
        ("ASM (capacidad)", "Asientos-milla disponibles: crecimiento de la oferta."),
        ("Factor de ocupación", "Qué tan llenos vuelan los aviones."),
        ("TRASM", "Ingreso total por asiento-milla: poder de precio."),
        ("CASM sin combustible", "Costo unitario controlable."),
        ("Costo de turbosina", "El principal costo variable."),
        ("Aviones en tierra", "Inspección de motores Pratt & Whitney."),
    ],
    "autopistas": [
        ("Tráfico promedio diario", "Aforo vehicular: motor de los ingresos por cuota."),
        ("Incremento tarifario", "Actualización por inflación de las cuotas."),
        ("Ingresos de concesiones", "El núcleo recurrente del negocio."),
        ("Margen UAFIDA", "Lo diluye el negocio de construcción."),
    ],
    "conglomerado": [
        ("Ingresos por división", "Comercial, industrial, infraestructura y energía."),
        ("Margen UAFIDA por división", "Dónde se genera el valor."),
        ("Cartera de obra", "Proyectos contratados de infraestructura."),
    ],
    "bancos": [
        ("Margen de interés neto (MIN)", "Lo que gana por prestar; sensible a la tasa de Banxico."),
        ("Crecimiento de la cartera", "Expansión del crédito."),
        ("Índice de morosidad (IMOR)", "Calidad de los activos."),
        ("Costo de riesgo", "Provisiones sobre cartera: lo que cuesta el crédito malo."),
        ("Índice de eficiencia", "Gastos sobre ingresos: menor es mejor."),
        ("ROE", "Rentabilidad sobre el capital."),
        ("ICAP", "Índice de capitalización: holgura regulatoria."),
    ],
    "microfinanzas": [
        ("Clientes", "Alcance de la base."),
        ("Cartera por país", "México contra Perú."),
        ("IMOR", "Calidad de los créditos grupales e individuales."),
        ("Costo de riesgo", "Provisiones sobre la cartera."),
        ("MIN", "Margen de interés neto: muy alto por diseño."),
        ("ROE", "Rentabilidad sobre el capital."),
    ],
    "seguros": [
        ("Primas emitidas", "Crecimiento del negocio."),
        ("Unidades aseguradas", "Base de vehículos asegurados."),
        ("Índice de siniestralidad", "Costo de los siniestros sobre las primas devengadas."),
        ("Índice combinado", "Siniestralidad más gastos: debajo de 100% hay utilidad técnica."),
        ("Producto financiero", "Rendimiento del portafolio de inversiones."),
        ("ROE", "Rentabilidad sobre el capital."),
    ],
    "bolsa": [
        ("Importe operado diario", "Volumen en capitales y derivados: ingreso transaccional."),
        ("Custodia en Indeval", "Ingreso recurrente ligado al valor de los activos."),
        ("Emisiones y colocaciones", "Listados nuevos de capital y deuda."),
        ("Margen UAFIDA", "Rentabilidad del modelo integrado."),
        ("Sensibilidad al USD/MXN", "Parte de los ingresos se cobra en dólares."),
    ],
    "telecom": [
        ("Suscriptores y adiciones netas", "Crecimiento de la base móvil y fija."),
        ("ARPU", "Ingreso promedio por usuario: poder de precio."),
        ("Churn", "Bajas mensuales: competencia."),
        ("CAPEX / ingresos", "Intensidad de inversión: libera flujo cuando baja."),
        ("Margen UAFIDA", "Rentabilidad de la red."),
        ("Deuda neta / UAFIDA", "Apalancamiento."),
    ],
    "mineria": [
        ("Producción de metal", "Cobre, plata, oro, zinc: el volumen."),
        ("Cash cost", "Costo por libra u onza neto de subproductos."),
        ("Precio realizado", "Lo que cobra contra la referencia internacional."),
        ("Margen UAFIDA", "Apalancamiento operativo al precio del metal."),
        ("CAPEX", "Proyectos de expansión."),
    ],
    "cemento": [
        ("Volumen de cemento, concreto y agregados", "Demanda de la construcción por región."),
        ("Precio", "Poder de fijación de precios."),
        ("Margen UAFIDA", "Energía y fletes son el costo clave."),
        ("Deuda neta / UAFIDA", "Desapalancamiento."),
        ("Ventas en EUA", "Exposición a la inversión en infraestructura de EUA."),
    ],
    "quimicos": [
        ("Volumen (toneladas)", "Demanda física."),
        ("UAFIDA comparable", "Sin efectos de inventario ni partidas únicas."),
        ("Margen de referencia", "PTA/PET o PVC/sosa: el ciclo de la industria."),
        ("Deuda neta / UAFIDA", "Holgura en la parte baja del ciclo."),
    ],
    "inmobiliario_industrial": [
        ("Área bruta rentable (ABR)", "Tamaño del portafolio de naves."),
        ("Ocupación", "Demanda de espacio; el nearshoring la sostiene."),
        ("Renta por pie cuadrado", "Precio de mercado de los contratos."),
        ("Spread de renovación", "Cuánto suben las rentas al renovar."),
        ("NOI y margen", "Ingreso neto operativo de las propiedades."),
        ("FFO por acción", "Flujo de la operación por acción."),
    ],
    "etf": [
        ("Prima o descuento contra el valor de la canasta", "Precio del ETF contra su valor teórico."),
        ("Error de seguimiento", "Qué tanto se separa del índice."),
    ],
}

FAMILIAS = {
    "crecimiento": "Crecimiento", "margenes": "Márgenes", "rentabilidad": "Rentabilidad",
    "balance": "Balance y liquidez", "flujo": "Flujo de efectivo", "bancario": "Indicadores bancarios",
    "seguros": "Indicadores de seguros", "valuacion": "Valuación", "mercado": "Rendimiento en bolsa",
    "riesgo": "Riesgo", "tecnico": "Técnico", "liquidez": "Liquidez",
}

# ───────────────────────────── utilidades sobre los estados ─────────────────────────────

def _fila(est: dict, estado: str, freq: str, clave: str) -> list:
    return ((est.get(estado) or {}).get(freq) or {}).get("filas", {}).get(clave) or []


def _periodos(est: dict, estado: str, freq: str) -> list[str]:
    return ((est.get(estado) or {}).get(freq) or {}).get("periodos") or []


def _ultimo(xs: list) -> float | None:
    for v in reversed(xs):
        if num(v) is not None:
            return num(v)
    return None


def _primera(est: dict, estado: str, freq: str, claves: tuple) -> list:
    for k in claves:
        f = _fila(est, estado, freq, k)
        if any(num(v) is not None for v in f):
            return f
    return []


def _udm(est: dict, estado: str, claves: tuple) -> float | None:
    """Últimos doce meses: el dato 'trailing' de Yahoo o la suma de los últimos cuatro trimestres."""
    for k in claves:
        v = _ultimo(_fila(est, estado, "udm", k))
        if v is not None:
            return v
    for k in claves:
        q = [num(x) for x in _fila(est, estado, "trimestral", k)]
        if len(q) >= 4 and all(x is not None for x in q[-4:]):
            return sum(q[-4:])
    for k in claves:
        v = _ultimo(_fila(est, estado, "anual", k))
        if v is not None:
            return v
    return None


def _udm_anterior(est: dict, estado: str, claves: tuple) -> float | None:
    """Doce meses que terminan un año antes (para crecimiento UDM): suma de los trimestres -8..-5."""
    for k in claves:
        q = [num(x) for x in _fila(est, estado, "trimestral", k)]
        if len(q) >= 8 and all(x is not None for x in q[-8:-4]):
            return sum(q[-8:-4])
    for k in claves:
        a = [num(x) for x in _fila(est, estado, "anual", k)]
        if len(a) >= 2 and a[-2] is not None:
            return a[-2]
    return None


def _saldo(est: dict, claves: tuple, atras: int = 0) -> float | None:
    """Saldo de balance más reciente (o el de hace `atras` trimestres)."""
    for k in claves:
        q = [num(x) for x in _fila(est, "balance", "trimestral", k)]
        q = [x for x in q if x is not None]
        if len(q) > atras:
            return q[-1 - atras]
    if atras == 0:
        for k in claves:
            v = _ultimo(_fila(est, "balance", "anual", k))
            if v is not None:
                return v
    return None


def _saldo_promedio(est: dict, claves: tuple) -> float | None:
    """Promedio del saldo actual y el de hace un año (o el anual previo)."""
    hoy = _saldo(est, claves)
    if hoy is None:
        return None
    for k in claves:
        q = [num(x) for x in _fila(est, "balance", "trimestral", k)]
        if len(q) >= 5 and q[-5] is not None:
            return (hoy + q[-5]) / 2
        a = [num(x) for x in _fila(est, "balance", "anual", k)]
        if len(a) >= 2 and a[-2] is not None:
            return (hoy + a[-2]) / 2
    return hoy


def _serie_trimestral(est: dict, fn) -> list[dict]:
    """Aplica fn(i) a cada trimestre disponible y devuelve [{p:'2T26', v:x}, ...]."""
    periodos = _periodos(est, "resultados", "trimestral")
    out = []
    for i, p in enumerate(periodos):
        try:
            v = fn(i)
        except (IndexError, TypeError, ZeroDivisionError):
            v = None
        out.append({"p": etiqueta_trimestre(p), "v": v})
    return out


def _q(est: dict, estado: str, claves: tuple, i: int) -> float | None:
    f = _primera(est, estado, "trimestral", claves)
    return num(f[i]) if i < len(f) else None


# Claves equivalentes en Yahoo (la primera que exista gana).
VENTAS = ("TotalRevenue", "OperatingRevenue")
UTIL_BRUTA = ("GrossProfit",)
UAFIDA = ("EBITDA", "NormalizedEBITDA")
UTIL_OPER = ("OperatingIncome", "EBIT")
UTIL_NETA = ("NetIncomeCommonStockholders", "NetIncome")
INTERESES = ("InterestExpense",)
DEPREC = ("ReconciledDepreciation",)
IMPUESTOS = ("TaxProvision",)
ANTES_IMP = ("PretaxIncome",)
ACTIVOS = ("TotalAssets",)
CAPITAL = ("StockholdersEquity", "CommonStockEquity")
DEUDA = ("TotalDebt",)
EFECTIVO = ("CashCashEquivalentsAndShortTermInvestments", "CashAndCashEquivalents")
ACT_CIRC = ("CurrentAssets",)
PAS_CIRC = ("CurrentLiabilities",)
INVENTARIO = ("Inventory",)
CXC = ("AccountsReceivable", "Receivables")
CXP = ("AccountsPayable", "Payables")
COSTO = ("CostOfRevenue",)
GASTOS = ("SellingGeneralAndAdministration", "OperatingExpense", "TotalExpenses")
CARTERA = ("NetLoan",)
MARGEN_FIN = ("NetInterestIncome",)
PROVISIONES = ("ProvisionForDoubtfulAccounts",)
SINIESTROS = ("NetPolicyholderBenefitsAndClaims",)
FLUJO_OPER = ("OperatingCashFlow",)
CAPEX = ("CapitalExpenditure",)
FLUJO_LIBRE = ("FreeCashFlow",)
DIVIDENDOS_PAG = ("CashDividendsPaid", "CommonStockDividendPaid")
RECOMPRAS = ("RepurchaseOfCapitalStock",)


def _k(clave, nombre, valor, unidad, familia, periodo=None, serie=None, formula=None, que=None,
       mejor="alto", detalle=None, tend=None, **extra):
    k = {"clave": clave, "nombre": nombre, "valor": valor, "unidad": unidad, "familia": familia,
         "periodo": periodo, "serie": serie or [], "formula": formula, "que": que, "mejor": mejor,
         "detalle": detalle, "tendencia": tend}
    k.update({c: v for c, v in extra.items() if v is not None})
    return k


def _tendencia(serie: list[dict], mejor: str = "alto") -> str | None:
    """Compara el último dato contra el de hace un año (o el primero disponible)."""
    vals = [s["v"] for s in serie if num(s.get("v")) is not None]
    if len(vals) < 2:
        return None
    ult, base = vals[-1], vals[-5] if len(vals) >= 5 else vals[0]
    if base == 0:
        return None
    cambio = (ult - base) / abs(base)
    if abs(cambio) < 0.02:
        return "estable"
    sube = ult > base
    return "mejora" if (sube and mejor == "alto") or (not sube and mejor == "bajo") else "empeora"


# ───────────────────────────── KPIs financieros ─────────────────────────────

def financieros(t: str, grupo: str, est: dict | None, info: dict | None, precio: float | None,
                fx_financiera: float = 1.0) -> list[dict]:
    """KPIs de los estados. fx_financiera convierte la moneda del reporte a la de cotización
    (ej. Grupo México reporta en dólares y cotiza en pesos)."""
    est = est or {}
    info = info or {}
    out: list[dict] = []
    fin = grupo in FINANCIERAS
    moneda = info.get("financialCurrency") or info.get("currency") or "MXN"
    per_q = _periodos(est, "resultados", "trimestral")
    ult_q = etiqueta_trimestre(per_q[-1]) if per_q else None

    ventas_udm = _udm(est, "resultados", VENTAS)
    ventas_ant = _udm_anterior(est, "resultados", VENTAS)
    neta_udm = _udm(est, "resultados", UTIL_NETA)
    neta_ant = _udm_anterior(est, "resultados", UTIL_NETA)
    uafida_udm = _udm(est, "resultados", UAFIDA)
    oper_udm = _udm(est, "resultados", UTIL_OPER)
    bruta_udm = _udm(est, "resultados", UTIL_BRUTA)

    # ── Crecimiento
    def g_yoy(claves):
        def fn(i):
            if i < 4:
                return None
            return crecimiento(_q(est, "resultados", claves, i), _q(est, "resultados", claves, i - 4))
        return fn

    s_ventas = _serie_trimestral(est, g_yoy(VENTAS))
    v_q = s_ventas[-1]["v"] if s_ventas else None
    if v_q is None and ventas_udm is not None and ventas_ant:
        v_q = crecimiento(ventas_udm, ventas_ant)
    out.append(_k("crec_ventas", "Crecimiento de ingresos (a/a)", v_q, "%", "crecimiento", ult_q,
                  [{"p": s["p"], "v": _q(est, "resultados", VENTAS, i)} for i, s in enumerate(s_ventas)],
                  "ingresos del trimestre ÷ mismo trimestre del año anterior − 1",
                  "Cuánto crece el negocio frente al año pasado, sin efectos de estacionalidad.",
                  serie_nombre="Ingresos por trimestre", moneda=moneda))
    out.append(_k("crec_ventas_udm", "Crecimiento de ingresos UDM", crecimiento(ventas_udm, ventas_ant), "%",
                  "crecimiento", "UDM", formula="ingresos de los últimos 12 meses ÷ los 12 meses previos − 1",
                  que="Crecimiento anual suavizado: elimina el ruido de un solo trimestre."))
    anual = [num(x) for x in _primera(est, "resultados", "anual", VENTAS)]
    anual = [x for x in anual if x is not None]
    if len(anual) >= 3 and anual[0] > 0 and anual[-1] > 0:
        n = len(anual) - 1
        out.append(_k("cagr_ventas", f"Crecimiento anual compuesto de ingresos ({n} años)",
                      (anual[-1] / anual[0]) ** (1 / n) - 1, "%", "crecimiento", f"{n} años",
                      formula=f"(ingresos del último año ÷ ingresos de hace {n} años)^(1/{n}) − 1",
                      que="Ritmo de crecimiento de mediano plazo."))
    s_neta = _serie_trimestral(est, g_yoy(UTIL_NETA))
    out.append(_k("crec_utilidad", "Crecimiento de la utilidad neta (a/a)", s_neta[-1]["v"] if s_neta else None,
                  "%", "crecimiento", ult_q,
                  [{"p": s["p"], "v": _q(est, "resultados", UTIL_NETA, i)} for i, s in enumerate(s_neta)],
                  "utilidad neta del trimestre ÷ mismo trimestre del año anterior − 1",
                  "Si la utilidad crece más que los ingresos, la empresa está ganando eficiencia.",
                  serie_nombre="Utilidad neta por trimestre", moneda=moneda))
    if not fin:
        s_uaf = _serie_trimestral(est, g_yoy(UAFIDA))
        out.append(_k("crec_uafida", "Crecimiento de la UAFIDA (a/a)", s_uaf[-1]["v"] if s_uaf else None, "%",
                      "crecimiento", ult_q, formula="UAFIDA del trimestre ÷ mismo trimestre del año anterior − 1",
                      que="Crecimiento de la generación operativa de caja antes de inversiones."))

    # ── Márgenes (series trimestrales)
    def margen(claves):
        return lambda i: div(_q(est, "resultados", claves, i), _q(est, "resultados", VENTAS, i))

    if not fin:
        for clave, nombre, claves, udm, formula, que in (
            ("margen_bruto", "Margen bruto", UTIL_BRUTA, bruta_udm, "utilidad bruta UDM ÷ ingresos UDM",
             "Lo que queda después del costo de ventas: poder de precio y de compra."),
            ("margen_uafida", "Margen UAFIDA", UAFIDA, uafida_udm, "UAFIDA UDM ÷ ingresos UDM",
             "Rentabilidad operativa antes de depreciación: comparable entre empresas."),
            ("margen_operativo", "Margen operativo", UTIL_OPER, oper_udm, "utilidad de operación UDM ÷ ingresos UDM",
             "Rentabilidad después de todos los gastos de operación."),
        ):
            s = _serie_trimestral(est, margen(claves))
            out.append(_k(clave, nombre, div(udm, ventas_udm) if udm is not None else (s[-1]["v"] if s else None),
                          "%", "margenes", "UDM", s, formula, que, tend=_tendencia(s)))
    s_mn = _serie_trimestral(est, margen(UTIL_NETA))
    out.append(_k("margen_neto", "Margen neto", div(neta_udm, ventas_udm), "%", "margenes", "UDM", s_mn,
                  "utilidad neta ÷ ingresos", "Cuántos centavos de utilidad deja cada peso vendido.",
                  tend=_tendencia(s_mn)))

    # ── Rentabilidad
    cap_prom = _saldo_promedio(est, CAPITAL)
    act_prom = _saldo_promedio(est, ACTIVOS)
    roe = div(neta_udm, cap_prom)
    if roe is None:
        roe = num(info.get("returnOnEquity"))
    out.append(_k("roe", "ROE · rendimiento sobre el capital", roe, "%", "rentabilidad", "UDM",
                  formula="utilidad neta UDM ÷ capital contable promedio",
                  que="Cuánto gana la empresa por cada peso de los accionistas. Arriba de 15% es bueno en México."))
    roa = div(neta_udm, act_prom)
    if roa is None:
        roa = num(info.get("returnOnAssets"))
    out.append(_k("roa", "ROA · rendimiento sobre activos", roa, "%", "rentabilidad", "UDM",
                  formula="utilidad neta UDM ÷ activos totales promedio",
                  que="Rentabilidad de todo el balance, sin importar cómo se financia."))
    if not fin:
        imp, antes = _udm(est, "resultados", IMPUESTOS), _udm(est, "resultados", ANTES_IMP)
        tasa = div(imp, antes)
        tasa = min(max(tasa, 0.0), 0.45) if tasa is not None else 0.30
        deuda, efectivo, capital = _saldo(est, DEUDA), _saldo(est, EFECTIVO), _saldo(est, CAPITAL)
        invertido = None
        if capital is not None:
            invertido = capital + (deuda or 0) - (efectivo or 0)
        roic = div(oper_udm * (1 - tasa), invertido) if oper_udm is not None and invertido and invertido > 0 else None
        out.append(_k("roic", "ROIC · rendimiento sobre el capital invertido", roic, "%", "rentabilidad", "UDM",
                      formula=f"utilidad de operación UDM × (1 − tasa de impuestos {tasa:.0%}) ÷ (capital + deuda − efectivo)",
                      que="Si supera el costo de capital (≈ 11–13% en México), la empresa crea valor."))
        rot = div(ventas_udm, act_prom)
        out.append(_k("rotacion_activos", "Rotación de activos", rot, "x", "rentabilidad", "UDM",
                      formula="ingresos UDM ÷ activos totales promedio",
                      que="Cuántos pesos vende por cada peso de activos: eficiencia del capital."))

    # ── Balance y liquidez
    deuda, efectivo = _saldo(est, DEUDA), _saldo(est, EFECTIVO)
    capital = _saldo(est, CAPITAL)
    if not fin:
        deuda_neta = (deuda - (efectivo or 0)) if deuda is not None else None
        out.append(_k("deuda_neta_uafida", "Deuda neta / UAFIDA", div(deuda_neta, uafida_udm), "x", "balance",
                      ult_q, formula="(deuda total − efectivo) ÷ UAFIDA UDM", mejor="bajo",
                      que="Años de UAFIDA para pagar la deuda. Debajo de 2x es cómodo; negativo = caja neta."))
        out.append(_k("deuda_capital", "Deuda / capital", div(deuda, capital), "x", "balance", ult_q,
                      formula="deuda total ÷ capital contable", mejor="bajo",
                      que="Qué tanto del financiamiento viene de acreedores frente a accionistas."))
        intereses = _udm(est, "resultados", INTERESES)
        cob = div(oper_udm, abs(intereses)) if intereses else None
        out.append(_k("cobertura_intereses", "Cobertura de intereses", cob, "x", "balance", "UDM",
                      formula="utilidad de operación UDM ÷ gasto por intereses UDM",
                      que="Veces que la operación paga los intereses. Debajo de 3x es señal de alerta."))
        out.append(_k("razon_circulante", "Razón circulante", div(_saldo(est, ACT_CIRC), _saldo(est, PAS_CIRC)), "x",
                      "balance", ult_q, formula="activo circulante ÷ pasivo circulante",
                      que="Capacidad de cubrir las obligaciones de corto plazo."))
        # Ciclo de conversión de efectivo
        costo_udm = _udm(est, "resultados", COSTO)
        dias_inv = div(_saldo(est, INVENTARIO), costo_udm)
        dias_cxc = div(_saldo(est, CXC), ventas_udm)
        dias_cxp = div(_saldo(est, CXP), costo_udm)
        if dias_cxc is not None:
            ciclo = (dias_inv or 0) * 365 + dias_cxc * 365 - (dias_cxp or 0) * 365
            out.append(_k("ciclo_efectivo", "Ciclo de conversión de efectivo", ciclo, "días", "balance", ult_q,
                          formula="días de inventario + días de cobro − días de pago", mejor="bajo",
                          que="Días que tarda un peso invertido en operar en regresar como efectivo.",
                          detalle={"inventario": dias_inv * 365 if dias_inv is not None else None,
                                   "cobro": dias_cxc * 365,
                                   "pago": dias_cxp * 365 if dias_cxp is not None else None}))

    # ── Flujo
    fo = _udm(est, "flujo", FLUJO_OPER)
    capex = _udm(est, "flujo", CAPEX)
    fl = _udm(est, "flujo", FLUJO_LIBRE)
    if fl is None and fo is not None and capex is not None:
        fl = fo + capex                      # Yahoo reporta el CAPEX con signo negativo
    if not fin:
        out.append(_k("flujo_libre", "Flujo libre UDM", fl, "dinero", "flujo", "UDM",
                      formula="flujo de operación − CAPEX (últimos 12 meses)",
                      que="El efectivo que queda para dividendos, recompras o pagar deuda.", moneda=moneda))
        out.append(_k("margen_flujo_libre", "Margen de flujo libre", div(fl, ventas_udm), "%", "flujo", "UDM",
                      formula="flujo libre UDM ÷ ingresos UDM",
                      que="Cuánto de cada peso vendido se convierte en efectivo disponible."))
        out.append(_k("conversion_caja", "Conversión de utilidad a flujo", div(fl, neta_udm), "x", "flujo", "UDM",
                      formula="flujo libre UDM ÷ utilidad neta UDM",
                      que="Cerca o arriba de 1x indica utilidades de calidad, respaldadas por efectivo."))
        out.append(_k("capex_ventas", "Intensidad de inversión (CAPEX / ingresos)",
                      div(abs(capex), ventas_udm) if capex is not None else None, "%", "flujo", "UDM",
                      formula="CAPEX UDM ÷ ingresos UDM", mejor="bajo",
                      que="Qué tanto reinvierte para sostener o crecer el negocio."))
    divs = _udm(est, "flujo", DIVIDENDOS_PAG)
    if divs is not None:
        out.append(_k("payout", "Pago de dividendos (payout)", div(abs(divs), neta_udm), "%", "flujo", "UDM",
                      formula="dividendos pagados UDM ÷ utilidad neta UDM",
                      que="Qué parte de la utilidad regresa al accionista en efectivo."))

    # ── Específicos de financieras
    if grupo in ("bancos", "microfinanzas"):
        mf = _udm(est, "resultados", MARGEN_FIN)
        out.append(_k("min_activos", "Margen financiero / activos", div(mf, act_prom), "%", "bancario", "UDM",
                      formula="margen financiero (ingresos − gastos por intereses) UDM ÷ activos promedio",
                      que="Aproximación al margen de interés neto (MIN) con datos públicos."))
        gastos = _udm(est, "resultados", ("SellingGeneralAndAdministration",))
        out.append(_k("eficiencia", "Índice de eficiencia", div(gastos, ventas_udm), "%", "bancario", "UDM",
                      formula="gastos de administración UDM ÷ ingresos totales UDM", mejor="bajo",
                      que="Cuánto cuesta generar cada peso de ingreso. Debajo de 45% es muy eficiente."))
        prov = _udm(est, "resultados", PROVISIONES)
        cart = _saldo_promedio(est, CARTERA)
        out.append(_k("costo_riesgo", "Costo de riesgo", div(prov, cart), "%", "bancario", "UDM",
                      formula="estimación preventiva para riesgos crediticios UDM ÷ cartera neta promedio",
                      mejor="bajo", que="Lo que se reserva por créditos que podrían no pagarse."))
        cart_hoy, cart_ant = _saldo(est, CARTERA), _saldo(est, CARTERA, 4)
        out.append(_k("crec_cartera", "Crecimiento de la cartera (a/a)", crecimiento(cart_hoy, cart_ant), "%",
                      "bancario", ult_q, formula="cartera neta ÷ cartera de hace un año − 1",
                      que="Ritmo al que el banco expande el crédito."))
        out.append(_k("capital_activos", "Capital / activos", div(capital, _saldo(est, ACTIVOS)), "%", "bancario",
                      ult_q, formula="capital contable ÷ activos totales",
                      que="Colchón de capital (aproximación al apalancamiento regulatorio)."))
    if grupo == "seguros":
        sin = _udm(est, "resultados", SINIESTROS)
        out.append(_k("siniestralidad", "Índice de siniestralidad (aprox.)", div(sin, ventas_udm), "%", "seguros",
                      "UDM", formula="siniestros y beneficios UDM ÷ ingresos UDM", mejor="bajo",
                      que="Costo de los siniestros sobre lo que se cobra. Clave en seguros de autos."))
    return [limpiar(k) for k in out]


# ───────────────────────────── KPIs de valuación ─────────────────────────────

def valuacion(t: str, grupo: str, est: dict | None, info: dict | None, precio: float | None,
              fx_financiera: float, divs_12m: float | None, hist_multiplos: dict | None) -> list[dict]:
    est = est or {}
    info = info or {}
    fin = grupo in FINANCIERAS
    mc = num(info.get("marketCap"))
    acciones = num(info.get("sharesOutstanding"))
    if precio and acciones and mc is None:
        mc = precio * acciones
    fx = fx_financiera or 1.0
    neta = _udm(est, "resultados", UTIL_NETA)
    ventas = _udm(est, "resultados", VENTAS)
    uafida = _udm(est, "resultados", UAFIDA)
    capital = _saldo(est, CAPITAL)
    deuda, efectivo = _saldo(est, DEUDA), _saldo(est, EFECTIVO)
    minoritario = _saldo(est, ("MinorityInterest",))
    fl = _udm(est, "flujo", FLUJO_LIBRE)
    conv = (lambda v: v * fx if v is not None else None)
    ve = None
    if mc is not None and not fin:
        ve = mc + conv(deuda or 0) - conv(efectivo or 0) + conv(minoritario or 0)
    hist = (hist_multiplos or {}).get("filas", {})

    def k(clave, nombre, valor, formula, que, mejor="bajo", clave_hist=None):
        serie = []
        if clave_hist and hist.get(clave_hist):
            per = (hist_multiplos or {}).get("periodos", [])
            serie = [{"p": etiqueta_trimestre(p), "v": v} for p, v in zip(per, hist[clave_hist])]
        return _k(clave, nombre, valor, "x" if clave not in ("rend_dividendo", "rend_utilidades", "rend_flujo") else "%",
                  "valuacion", "actual", serie, formula, que, mejor)

    pe = div(mc, conv(neta)) if neta and neta > 0 else None
    out = [k("pe", "Precio / utilidad (P/U)", pe, "valor de mercado ÷ utilidad neta UDM",
             "Años de utilidad que paga el mercado. Menor = más barata, si la utilidad es sostenible.", clave_hist="pe")]
    out.append(k("p_vl", "Precio / valor en libros", div(mc, conv(capital)) if capital and capital > 0 else None,
                 "valor de mercado ÷ capital contable", "Clave en bancos y aseguradoras.", clave_hist="p_vl"))
    if not fin:
        out.append(k("ve_uafida", "Valor empresa / UAFIDA", div(ve, conv(uafida)) if uafida and uafida > 0 else None,
                     "(valor de mercado + deuda − efectivo + minoritario) ÷ UAFIDA UDM",
                     "El múltiplo más usado para comparar empresas con distinta deuda.", clave_hist="ve_uafida"))
        out.append(k("ve_ventas", "Valor empresa / ventas", div(ve, conv(ventas)) if ventas else None,
                     "valor de la empresa ÷ ingresos UDM", "Útil cuando la utilidad es baja o volátil.",
                     clave_hist="ve_ventas"))
        out.append(k("rend_flujo", "Rendimiento de flujo libre", div(conv(fl), mc) if fl is not None else None,
                     "flujo libre UDM ÷ valor de mercado", "El flujo que «rinde» la acción a su precio actual.",
                     mejor="alto"))
    out.append(k("rend_utilidades", "Rendimiento de utilidades (inverso del P/U)", div(conv(neta), mc),
                 "utilidad neta UDM ÷ valor de mercado", "Se compara contra la tasa de CETES.", mejor="alto"))
    dy = div(divs_12m, precio) if divs_12m and precio else num(info.get("trailingAnnualDividendYield"))
    out.append(k("rend_dividendo", "Rendimiento por dividendo", dy, "dividendos pagados en 12 meses ÷ precio",
                 "Retorno en efectivo al accionista.", mejor="alto"))
    for kpi in out:
        kpi["detalle"] = {"valor_mercado": mc, "valor_empresa": ve, "moneda_reporte_a_cotizacion": fx}
    return [limpiar(x) for x in out]


# ───────────────────────────── KPIs de mercado ─────────────────────────────

def _rend(c: list[float], dias: int) -> float | None:
    if len(c) <= dias:
        return None
    return c[-1] / c[-1 - dias] - 1


def _rendimientos(c: list[float]) -> list[float]:
    return [c[i] / c[i - 1] - 1 for i in range(1, len(c)) if c[i - 1] > 0]


def rsi(c: list[float], n: int = 14) -> float | None:
    if len(c) <= n:
        return None
    ganan, pierden = 0.0, 0.0
    for i in range(1, n + 1):
        d = c[i] - c[i - 1]
        ganan += max(d, 0)
        pierden += max(-d, 0)
    ganan, pierden = ganan / n, pierden / n
    for i in range(n + 1, len(c)):
        d = c[i] - c[i - 1]
        ganan = (ganan * (n - 1) + max(d, 0)) / n
        pierden = (pierden * (n - 1) + max(-d, 0)) / n
    if pierden == 0:
        return 100.0
    return 100 - 100 / (1 + ganan / pierden)


def max_caida(c: list[float]) -> float | None:
    if len(c) < 2:
        return None
    pico, peor = c[0], 0.0
    for x in c:
        pico = max(pico, x)
        peor = min(peor, x / pico - 1)
    return peor


def alinear(a: dict, b: dict) -> tuple[list[float], list[float]]:
    """Dos series {fecha: precio} → rendimientos diarios en las fechas comunes."""
    fechas = sorted(set(a) & set(b))
    ra, rb = [], []
    for i in range(1, len(fechas)):
        f0, f1 = fechas[i - 1], fechas[i]
        if a[f0] and b[f0]:
            ra.append(a[f1] / a[f0] - 1)
            rb.append(b[f1] / b[f0] - 1)
    return ra, rb


def semanales(serie: dict) -> dict:
    """Último cierre de cada semana ISO."""
    out = {}
    for f in sorted(serie):
        y, w, _ = date.fromisoformat(f).isocalendar()
        out[(y, w)] = (f, serie[f])
    return {f: v for (f, v) in out.values()}


def mercado(t: str, v: dict | None, ref: dict | None, cetes: float | None) -> list[dict]:
    """Rendimientos, riesgo, liquidez y técnico, desde las velas diarias."""
    if not v or not v.get("c"):
        return []
    d, c, vol = v["d"], v["c"], v.get("v") or []
    serie = dict(zip(d, c))
    hoy = date.fromisoformat(d[-1])
    out = []

    def r_desde(f: date):
        previas = [x for x in d if x <= f.isoformat()]
        if not previas:
            return None
        return c[-1] / serie[previas[-1]] - 1

    out.append(_k("rend_1m", "Rendimiento 1 mes", _rend(c, 21), "%", "mercado", "21 sesiones",
                  formula="cierre de hoy ÷ cierre de hace 21 sesiones − 1"))
    out.append(_k("rend_3m", "Rendimiento 3 meses", _rend(c, 63), "%", "mercado", "63 sesiones",
                  formula="cierre de hoy ÷ cierre de hace 63 sesiones − 1"))
    out.append(_k("rend_ytd", "Rendimiento en el año", r_desde(date(hoy.year - 1, 12, 31)), "%", "mercado",
                  str(hoy.year), formula="cierre de hoy ÷ último cierre del año anterior − 1"))
    out.append(_k("rend_1a", "Rendimiento 12 meses", r_desde(hoy - timedelta(days=365)), "%", "mercado", "12 meses",
                  formula="cierre de hoy ÷ cierre de hace un año − 1"))
    out.append(_k("rend_3a", "Rendimiento 3 años", r_desde(hoy - timedelta(days=3 * 365)), "%", "mercado", "3 años",
                  formula="cierre de hoy ÷ cierre de hace tres años − 1"))
    # Momentum 12-1 (el factor M del modelo QVM): rendimiento de 12 meses saltando el último
    mom = None
    if len(c) > 252:
        mom = c[-22] / c[-253] - 1
    out.append(_k("momentum_12_1", "Momentum 12-1", mom, "%", "mercado", "12 meses sin el último",
                  formula="cierre de hace 21 sesiones ÷ cierre de hace 252 sesiones − 1",
                  que="El factor de momentum clásico: tendencia de un año sin el ruido del último mes."))
    r = _rendimientos(c[-253:])
    sd = desv(r)
    vol_a = sd * math.sqrt(252) if sd is not None else None
    out.append(_k("volatilidad", "Volatilidad anual", vol_a, "%", "riesgo", "12 meses", mejor="bajo",
                  formula="desviación estándar de los rendimientos diarios × √252",
                  que="Cuánto se mueve el precio en un año típico."))
    if ref:
        ra, rb = alinear({f: x for f, x in serie.items() if f >= (hoy - timedelta(days=366)).isoformat()}, ref)
        vb = desv(rb)
        beta = covarianza(ra, rb) / (vb ** 2) if vb else None
        out.append(_k("beta_1a", "Beta contra el IPC (diaria, 1 año)", beta, "x", "riesgo", "12 meses", mejor="bajo",
                      formula="cov(r emisora, r IPC) ÷ var(r IPC)",
                      que="Si el IPC sube 1%, cuánto se espera que se mueva la emisora."))
        sa, sb = semanales(serie), semanales(ref)
        ra5, rb5 = alinear({f: x for f, x in sa.items() if f >= (hoy - timedelta(days=5 * 366)).isoformat()}, sb)
        vb5 = desv(rb5)
        beta5 = covarianza(ra5, rb5) / (vb5 ** 2) if vb5 and len(ra5) > 52 else None
        out.append(_k("beta_5a", "Beta contra el IPC (semanal, 5 años)", beta5, "x", "riesgo", "5 años", mejor="bajo",
                      formula="cov(r semanal emisora, r semanal IPC) ÷ var(r semanal IPC)",
                      que="Misma medida que publica Refinitiv, con 260 semanas."))
        if ra and rb:
            corr = None
            sa_, sb_ = desv(ra), desv(rb)
            if sa_ and sb_:
                corr = covarianza(ra, rb) / (sa_ * sb_)
            out.append(_k("correlacion_ipc", "Correlación con el IPC", corr, "x", "riesgo", "12 meses",
                          formula="correlación de los rendimientos diarios", mejor="bajo",
                          que="Qué tanto diversifica frente al mercado mexicano."))
    out.append(_k("max_caida", "Caída máxima desde un pico (12 meses)", max_caida(c[-253:]), "%", "riesgo",
                  "12 meses", formula="mínimo de (precio ÷ máximo previo − 1)", mejor="alto",
                  que="La peor pérdida que sufrió quien compró en un máximo."))
    if vol_a and len(r) > 20:
        rf = cetes if cetes is not None else 0.07
        r1 = _rend(c, min(252, len(c) - 1))
        out.append(_k("sharpe", "Razón de Sharpe (12 meses)", (r1 - rf) / vol_a if r1 is not None else None, "x",
                      "riesgo", "12 meses", formula=f"(rendimiento 12 meses − CETES {rf:.2%}) ÷ volatilidad anual",
                      que="Rendimiento extra sobre CETES por unidad de riesgo."))
    ventana = c[-252:]
    alto, bajo = max(ventana), min(ventana)
    out.append(_k("dist_maximo", "Distancia al máximo de 52 semanas", c[-1] / alto - 1, "%", "tecnico", "52 semanas",
                  formula="precio ÷ máximo de 52 semanas − 1", detalle={"maximo": alto, "minimo": bajo}))
    sma50 = media(c[-50:]) if len(c) >= 50 else None
    sma200 = media(c[-200:]) if len(c) >= 200 else None
    out.append(_k("vs_sma200", "Precio contra su promedio de 200 días", c[-1] / sma200 - 1 if sma200 else None, "%",
                  "tecnico", "200 sesiones", formula="precio ÷ promedio móvil de 200 días − 1",
                  que="Arriba de cero, tendencia de largo plazo alcista.",
                  detalle={"sma50": sma50, "sma200": sma200,
                           "cruce": ("dorado" if sma50 and sma200 and sma50 > sma200 else "de la muerte")
                           if sma50 and sma200 else None}))
    out.append(_k("rsi14", "RSI de 14 días", rsi(c[-120:]), "pts", "tecnico", "14 sesiones",
                  formula="100 − 100 ÷ (1 + ganancia promedio ÷ pérdida promedio), suavizado de Wilder",
                  que="Arriba de 70, sobrecompra; debajo de 30, sobreventa.", mejor="neutral"))
    if vol:
        imp = [ci * vi for ci, vi in zip(c[-63:], vol[-63:]) if vi]
        out.append(_k("importe_diario", "Importe operado promedio (3 meses)", media(imp) if imp else None, "dinero",
                      "liquidez", "63 sesiones", formula="promedio de precio × volumen diario",
                      que="Liquidez: cuánto dinero cambia de manos al día. Define el costo de entrar y salir.",
                      moneda="MXN"))
    return [limpiar(k) for k in out]


# ───────────────────────────── comparación contra pares ─────────────────────────────

def comparar(por_emisora: dict[str, list[dict]], sectores: dict[str, str]) -> None:
    """Agrega mediana del sector, mediana del universo y percentil a cada KPI (en el mismo dict)."""
    claves = {}
    for t, kpis in por_emisora.items():
        for k in kpis:
            claves.setdefault(k["clave"], {})[t] = k.get("valor")
    for t, kpis in por_emisora.items():
        sec = sectores.get(t)
        for k in kpis:
            valores = claves.get(k["clave"], {})
            pares = [v for u, v in valores.items() if sectores.get(u) == sec and u != t]
            k["mediana_sector"] = limpiar(mediana(pares)) if len(pares) >= 1 else None
            k["n_sector"] = len([p for p in pares if num(p) is not None])
            k["mediana_universo"] = limpiar(mediana(valores.values()))
            p = percentil_de(k.get("valor"), list(valores.values()))
            if p is not None and k.get("mejor") == "bajo":
                p = 1 - p
            k["percentil"] = limpiar(p, 3) if k.get("mejor") != "neutral" else None


# ───────────────────────────── factores QVM en vivo ─────────────────────────────

def factores_qvm(por_emisora: dict[str, list[dict]], pesos=(0.40, 0.10, 0.50)) -> dict[str, dict]:
    """Aproximación pública del modelo M-tilt del fondo (Quality 40 · Value 10 · Momentum 50).

    Quality  = z(ROE) + z(margen neto) − z(deuda neta/UAFIDA, solo no financieras)
    Value    = z(rendimiento de utilidades) + z(1/P-VL) + z(rendimiento por dividendo)
    Momentum = z(momentum 12-1) + z(rendimiento 6 meses aprox. con 3 meses)
    """
    def col(clave, invertir=False):
        out = {}
        for t, ks in por_emisora.items():
            for k in ks:
                if k["clave"] == clave and num(k.get("valor")) is not None:
                    v = num(k["valor"])
                    if invertir:
                        v = 1 / v if v else None
                    if v is not None:
                        out[t] = v
        return zscores(out)

    def combinar(*cols, signos=None):
        signos = signos or [1] * len(cols)
        ts = set().union(*[set(c) for c in cols])
        res = {}
        for t in ts:
            vals = [s * c[t] for c, s in zip(cols, signos) if t in c]
            if vals:
                res[t] = sum(vals) / len(vals)
        return zscores(res)

    q = combinar(col("roe"), col("margen_neto"), col("deuda_neta_uafida"), signos=[1, 1, -1])
    v = combinar(col("rend_utilidades"), col("p_vl", invertir=True), col("rend_dividendo"))
    m = combinar(col("momentum_12_1"), col("rend_3m"))
    out = {}
    for t in por_emisora:
        partes = [(q.get(t), pesos[0]), (v.get(t), pesos[1]), (m.get(t), pesos[2])]
        disp = [(z, w) for z, w in partes if z is not None]
        comp = sum(z * w for z, w in disp) / sum(w for _, w in disp) if disp else None
        out[t] = {"quality": q.get(t), "value": v.get(t), "momentum": m.get(t), "compuesto": comp}
    zc = zscores({t: x["compuesto"] for t, x in out.items() if x["compuesto"] is not None})
    orden = sorted(zc, key=lambda t: zc[t], reverse=True)
    for i, t in enumerate(orden):
        out[t]["z"] = zc[t]
        out[t]["rango"] = i + 1
        out[t]["percentil"] = 1 - i / max(1, len(orden) - 1)
    return limpiar(out)
