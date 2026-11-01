"""Series del SIE de Banxico. Opcional: solo corre si existe el secreto BANXICO_TOKEN
(se obtiene gratis en https://www.banxico.org.mx/SieAPIRest/service/v1/token).
"""
from __future__ import annotations

import json
import os
import urllib.request
from datetime import date, timedelta

URL = "https://www.banxico.org.mx/SieAPIRest/service/v1/series/{ids}/datos/{ini}/{fin}"


def series(ids: list[str], dias: int = 800) -> dict[str, list[list]]:
    token = os.environ.get("BANXICO_TOKEN", "").strip()
    if not token:
        return {}
    fin = date.today()
    ini = fin - timedelta(days=dias)
    url = URL.format(ids=",".join(ids), ini=ini.isoformat(), fin=fin.isoformat())
    req = urllib.request.Request(url, headers={"Bmx-Token": token, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        datos = json.load(r)
    out = {}
    for s in (datos.get("bmx") or {}).get("series", []):
        puntos = []
        for d in s.get("datos") or []:
            try:
                dd, mm, aa = d["fecha"].split("/")
                v = float(str(d["dato"]).replace(",", ""))
            except (KeyError, ValueError):
                continue                     # "N/E" = no existe
            puntos.append([f"{aa}-{mm}-{dd}", v])
        if puntos:
            out[s.get("idSerie")] = sorted(puntos)
    return out
