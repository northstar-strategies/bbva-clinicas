"""Utilidades comunes del pipeline: archivos, fechas, números y estadística básica.

Todo es biblioteca estándar para que el servidor MCP y las pruebas puedan importarlo
sin instalar nada.
"""
from __future__ import annotations

import json
import math
import os
import tempfile
from datetime import date, datetime, timedelta, timezone
from statistics import median
from typing import Any, Iterable, Sequence

# México no tiene horario de verano desde 2022: la BMV opera siempre en UTC-6.
CDMX = timezone(timedelta(hours=-6), "CDMX")
APERTURA_BMV = (8, 30)
CIERRE_BMV = (15, 0)


# ───────────────────────────── archivos ─────────────────────────────

def leer_json(ruta: str, defecto: Any = None) -> Any:
    try:
        with open(ruta, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return defecto


def escribir_json(ruta: str, datos: Any, compacto: bool = True) -> bool:
    """Escribe de forma atómica. Devuelve True si el contenido cambió.

    Comparar antes de escribir evita commits vacíos cuando Yahoo repite el dato.
    """
    os.makedirs(os.path.dirname(ruta) or ".", exist_ok=True)
    if compacto:
        texto = json.dumps(datos, ensure_ascii=False, separators=(",", ":"), allow_nan=False, default=_json_default)
    else:
        texto = json.dumps(datos, ensure_ascii=False, indent=1, allow_nan=False, default=_json_default)
    texto += "\n"
    try:
        with open(ruta, encoding="utf-8") as f:
            if f.read() == texto:
                return False
    except FileNotFoundError:
        pass
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(ruta) or ".", suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(texto)
    os.replace(tmp, ruta)
    return True


def _json_default(o: Any) -> Any:
    if isinstance(o, (datetime, date)):
        return o.isoformat()
    if hasattr(o, "item"):           # escalares de numpy
        return o.item()
    raise TypeError(f"No serializable: {type(o)}")


# ───────────────────────────── números ─────────────────────────────

def num(v: Any) -> float | None:
    """Convierte a float finito o None (NaN, inf, cadenas vacías y basura → None)."""
    if v is None or isinstance(v, bool):
        return None
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


def redondear(v: Any, d: int = 4) -> float | None:
    x = num(v)
    return None if x is None else round(x, d)


def limpiar(o: Any, d: int = 6) -> Any:
    """Redondea floats de forma recursiva y cambia NaN/inf por None, para JSON válido."""
    if isinstance(o, float):
        return round(o, d) if math.isfinite(o) else None
    if isinstance(o, dict):
        return {k: limpiar(v, d) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [limpiar(v, d) for v in o]
    if hasattr(o, "item") and not isinstance(o, (str, bytes)):
        try:
            return limpiar(o.item(), d)
        except Exception:
            return None
    return o


def div(a: Any, b: Any) -> float | None:
    a, b = num(a), num(b)
    if a is None or b is None or b == 0:
        return None
    return a / b


def crecimiento(nuevo: Any, viejo: Any) -> float | None:
    """Cambio relativo. Si la base es negativa se usa su valor absoluto para que el signo tenga sentido."""
    n, v = num(nuevo), num(viejo)
    if n is None or v is None or v == 0:
        return None
    return (n - v) / abs(v)


def mediana(valores: Iterable[Any]) -> float | None:
    xs = [x for x in (num(v) for v in valores) if x is not None]
    return median(xs) if xs else None


def percentil_de(valor: Any, valores: Sequence[Any]) -> float | None:
    """Fracción del universo que queda por debajo (0 a 1)."""
    x = num(valor)
    xs = sorted(v for v in (num(y) for y in valores) if v is not None)
    if x is None or len(xs) < 3:
        return None
    menores = sum(1 for v in xs if v < x)
    iguales = sum(1 for v in xs if v == x)
    return (menores + 0.5 * iguales) / len(xs)


def zscores(valores: dict[str, Any], winsor: float = 3.0) -> dict[str, float]:
    """z-score del universo, acotado a ±winsor para que un dato extremo no domine."""
    xs = {k: num(v) for k, v in valores.items()}
    xs = {k: v for k, v in xs.items() if v is not None}
    if len(xs) < 4:
        return {}
    m = sum(xs.values()) / len(xs)
    var = sum((v - m) ** 2 for v in xs.values()) / (len(xs) - 1)
    sd = math.sqrt(var)
    if sd == 0:
        return {k: 0.0 for k in xs}
    return {k: max(-winsor, min(winsor, (v - m) / sd)) for k, v in xs.items()}


def media(xs: Sequence[float]) -> float | None:
    return sum(xs) / len(xs) if xs else None


def desv(xs: Sequence[float]) -> float | None:
    if len(xs) < 2:
        return None
    m = sum(xs) / len(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def covarianza(a: Sequence[float], b: Sequence[float]) -> float | None:
    n = min(len(a), len(b))
    if n < 2:
        return None
    a, b = a[-n:], b[-n:]
    ma, mb = sum(a) / n, sum(b) / n
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / (n - 1)


# ───────────────────────────── fechas ─────────────────────────────

def ahora_utc() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def iso(dt: datetime | None) -> str | None:
    return dt.isoformat() if dt else None


def etiqueta_trimestre(fecha: str | date) -> str:
    """'2026-06-30' → '2T26' (convención de los reportes en México)."""
    if isinstance(fecha, str):
        fecha = date.fromisoformat(fecha[:10])
    t = (fecha.month - 1) // 3 + 1
    return f"{t}T{fecha.year % 100:02d}"


def etiqueta_anio(fecha: str | date) -> str:
    if isinstance(fecha, str):
        fecha = date.fromisoformat(fecha[:10])
    return f"{fecha.year}"


def estado_mercado(momento: datetime | None = None, feriados: Iterable[str] = ()) -> dict:
    """Estado de la BMV en hora de Ciudad de México."""
    m = (momento or ahora_utc()).astimezone(CDMX)
    hoy = m.date().isoformat()
    minutos = m.hour * 60 + m.minute
    abre = APERTURA_BMV[0] * 60 + APERTURA_BMV[1]
    cierra = CIERRE_BMV[0] * 60 + CIERRE_BMV[1]
    if m.weekday() >= 5:
        estado, texto = "cerrado", "Fin de semana"
    elif hoy in set(feriados):
        estado, texto = "cerrado", "Día inhábil en la BMV"
    elif minutos < abre:
        estado, texto = "preapertura", "Abre a las 8:30"
    elif minutos < cierra:
        estado, texto = "abierto", "Sesión continua hasta las 15:00"
    else:
        estado, texto = "cerrado", "Sesión terminada"
    return {"estado": estado, "texto": texto, "hora_cdmx": m.strftime("%Y-%m-%d %H:%M"), "fecha": hoy}


def fecha_cdmx(dt: datetime) -> str:
    return dt.astimezone(CDMX).date().isoformat()
