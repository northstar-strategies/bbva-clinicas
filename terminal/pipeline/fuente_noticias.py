"""Noticias automáticas en español desde el RSS de Google Noticias (sin llave de API),
con un clasificador de tono por léxico para pintar las tarjetas igual que las del equipo.
"""
from __future__ import annotations

import html
import logging
import re
import time
import unicodedata
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

log = logging.getLogger("terminal.noticias")
CABECERAS = {"User-Agent": "Mozilla/5.0 (compatible; NorthStarTerminal/1.0; +https://github.com/northstar-strategies)"}
RSS = "https://news.google.com/rss/search?q={q}&hl=es-419&gl=MX&ceid=MX:es-419"

MERCADO = [
    '"Bolsa Mexicana de Valores" OR "S&P/BMV IPC" OR "BMV" acciones',
    'Banxico tasa OR inflación México',
    '"peso mexicano" dólar',
]

_POS = """sube suben subio subieron alza alzas avanza avanzan avanzo gana ganan gano ganancia ganancias record
records crece crecen crecio crecimiento mejora mejoran mejoro supera superan supero repunta repunte dispara
disparan eleva elevan aumenta aumentan aumento incrementa incremento maximo maximos fortalece optimismo positivo
positiva positivos beneficio beneficios expansion aprueba impulsa impulso recupera recuperacion solido solidos
solida duplica triplica upgrade mejoracalificacion rebota rebote invierte inversion dividendo""".split()
_NEG = """cae caen cayo cayeron caida caidas pierde pierden perdio perdida perdidas desploma desplome desplomes
retrocede retroceso recorta recorte recortes reduce redujo disminuye disminuyo minimo minimos debil debilidad
preocupa preocupacion riesgo riesgos multa investigacion huelga crisis quiebra rebaja degrada negativo negativa
alerta advierte incertidumbre presion presiones contraccion suspende cancela retrasa sancion sanciones arancel
aranceles demanda litigio fraude downgrade hunde hunden tropieza desaceleracion recesion""".split()
_POS_S, _NEG_S = set(_POS), set(_NEG)


def _plano(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def tono(texto: str) -> tuple[str, int]:
    palabras = re.findall(r"[a-zñ]+", _plano(texto))
    p = sum(1 for w in palabras if w in _POS_S)
    n = sum(1 for w in palabras if w in _NEG_S)
    s = p - n
    return ("positiva" if s > 0 else "negativa" if s < 0 else "neutral"), s


def palabras_clave(consulta: str) -> list[str]:
    """'FEMSA OR OXXO' → ['femsa', 'oxxo']; '"Grupo Bimbo"' → ['grupo bimbo']."""
    frases = re.findall(r'"([^"]+)"', consulta)
    resto = re.sub(r'"[^"]+"', " ", consulta)
    sueltas = [w for w in re.findall(r"[\wÁÉÍÓÚÑáéíóúñ&]+", resto) if w.upper() not in {"OR", "AND"} and len(w) > 2]
    claves = [_plano(x) for x in frases] or [_plano(w) for w in sueltas[:2]]
    if frases and sueltas and sueltas[0][0].isupper():
        claves.append(_plano(sueltas[0]))
    return claves


def _pedir(url: str, intentos: int = 3) -> bytes:
    ultimo = None
    for i in range(1, intentos + 1):
        try:
            req = urllib.request.Request(url, headers=CABECERAS)
            with urllib.request.urlopen(req, timeout=25) as r:
                return r.read()
        except Exception as e:
            ultimo = e
            if i < intentos:
                time.sleep(2 * i)
    raise ultimo  # type: ignore[misc]


def buscar(consulta: str, dias: int = 30, maximo: int = 12, filtrar: list[str] | None = None) -> list[dict]:
    q = urllib.parse.quote(f"{consulta} when:{dias}d")
    crudo = _pedir(RSS.format(q=q))
    raiz = ET.fromstring(crudo)
    limite = datetime.now(timezone.utc) - timedelta(days=dias)
    out = []
    for it in raiz.iter("item"):
        titulo = html.unescape((it.findtext("title") or "").strip())
        fuente_el = it.find("source")
        fuente = (fuente_el.text or "").strip() if fuente_el is not None else ""
        if fuente and titulo.endswith(" - " + fuente):
            titulo = titulo[: -len(fuente) - 3].strip()
        if not titulo:
            continue
        try:
            fecha = parsedate_to_datetime(it.findtext("pubDate") or "").astimezone(timezone.utc)
        except (TypeError, ValueError):
            continue
        if fecha < limite:
            continue
        if filtrar and not any(k in _plano(titulo) for k in filtrar):
            continue
        t, s = tono(titulo)
        out.append({
            "titulo": titulo, "url": (it.findtext("link") or "").strip(), "fuente": fuente or "Google Noticias",
            "fecha_utc": fecha.replace(microsecond=0).isoformat(), "tono": t, "puntaje": s,
        })
        if len(out) >= maximo * 2:
            break
    out.sort(key=lambda x: x["fecha_utc"], reverse=True)
    return out[:maximo]


def clave_titulo(t: str) -> str:
    return re.sub(r"[^a-z0-9]", "", _plano(t))[:80]
