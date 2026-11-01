#!/usr/bin/env python3
"""Prueba de humo del servidor MCP: arma datos semilla, levanta el servidor y le habla por stdio."""
import json
import os
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))


def main():
    datos = tempfile.mkdtemp()
    subprocess.run([sys.executable, os.path.join(RAIZ, "terminal", "pipeline", "actualizar.py"), "--modo", "semilla", "--datos", datos],
                   check=True, capture_output=True)
    srv = subprocess.Popen([sys.executable, os.path.join(AQUI, "servidor_mcp.py"), "--local", datos],
                           stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    n = 0

    def pedir(metodo, params=None, notificacion=False):
        nonlocal n
        msg = {"jsonrpc": "2.0", "method": metodo, **({"params": params} if params is not None else {})}
        if not notificacion:
            n += 1
            msg["id"] = n
        srv.stdin.write(json.dumps(msg) + "\n")
        srv.stdin.flush()
        if notificacion:
            return None
        r = json.loads(srv.stdout.readline())
        assert r["id"] == n, r
        return r

    r = pedir("initialize", {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "prueba", "version": "0"}})
    assert r["result"]["protocolVersion"] == "2025-06-18" and "tools" in r["result"]["capabilities"]
    pedir("notifications/initialized", notificacion=True)
    herramientas = {t["name"]: t for t in pedir("tools/list")["result"]["tools"]}
    assert {"kpis", "ficha", "portafolio", "filtrar", "atribucion_alfa", "investigacion", "sensibilidad"} <= set(herramientas)
    for h in herramientas.values():
        assert h["inputSchema"]["type"] == "object" and h["description"]
    casos = [
        ("buscar_emisora", {"texto": "banco"}, "GFNORTEO"),
        ("cotizacion", {"emisoras": ["femsa", "USDMXN"]}, "FEMSAUBD"),
        ("ficha", {"emisora": "Peñoles"}, "PEOLES"),
        ("kpis", {"emisora": "GMEXICOB", "familia": "riesgo"}, "Volatilidad"),
        ("ranking_kpi", {"kpi": "rend_1a", "n": 5}, "| 1 |"),
        ("filtrar", {"criterios": [{"kpi": "volatilidad", "op": "<=", "valor": 25}]}, "emisoras cumplen"),
        ("noticias", {"emisora": "FEMSAUBD", "dias": 400, "n": 3}, "FEMSAUBD"),
        ("portafolio", {"dias": 3}, "MEXTRAC"),
        ("macro", {"series": ["USDMXN", "COBRE"]}, "USDMXN"),
        ("comparar", {"emisoras": ["FEMSAUBD", "KOFUBL"]}, "KOFUBL"),
        ("estados_financieros", {"emisora": "WALMEX"}, "WALMEX"),
        ("estado_datos", {}, "semilla"),
        ("atribucion_alfa", {}, "Alfa acumulado"),
        ("atribucion_alfa", {"grupo": "ventas"}, "Corrección de sobregiro"),
        ("investigacion", {}, "TL;DR"),
        ("investigacion", {"emisora": "femsa"}, "OXXO"),
        ("sensibilidad", {"emisora": "GMEXICOB", "escenario": {"precio_cu": -10}}, "Escenario"),
    ]
    for nombre, args, esperado in casos:
        r = pedir("tools/call", {"name": nombre, "arguments": args})["result"]
        texto = r["content"][0]["text"]
        assert not r["isError"], (nombre, texto)
        assert esperado in texto, (nombre, texto[:400])
        print(f"ok {nombre}")
    r = pedir("tools/call", {"name": "ficha", "arguments": {"emisora": "NOEXISTE"}})["result"]
    assert r["isError"]
    assert pedir("metodo/raro")["error"]["code"] == -32601
    srv.stdin.close()
    srv.wait(timeout=10)
    print("servidor MCP: todo bien")


if __name__ == "__main__":
    main()
