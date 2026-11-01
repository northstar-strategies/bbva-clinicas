# North Star Terminal

Terminal financiera del **Fondo de Inversión ITESM-BBVA** (North Star Strategies) para las 37 emisoras de la BMV que analiza el fondo y el ETF MEXTRAC 09. La idea viene de [FinceptTerminal](https://github.com/Fincept-Corporation/FinceptTerminal) y de Bloomberg: línea de comandos, teclas de función, datos densos y fichas completas. Está hecha desde cero como página web, enfocada en el fondo y **sin necesidad del vigilante**.

- **Abrir:** `https://northstar-strategies.github.io/bbva-clinicas/terminal/`, o desde el menú lateral del tablero en **North Star Terminal**.
- **Se actualiza sola:** GitHub Actions descarga los datos en la nube y los publica en la rama `datos`. No hace falta tener ninguna computadora encendida.

```
 GitHub Actions (nube)                        rama «datos»                          navegador
 ┌──────────────────────────┐   cada 15 min   ┌──────────────────────┐   cada 1 min   ┌────────────────────┐
 │ terminal/pipeline        │ ──────────────▶ │ terminal/datos/*.json │ ◀───────────── │ terminal/ (página) │
 │  Yahoo Finance           │   y al cierre   │  cotizaciones, velas, │                │ index.html (tablero│
 │  Google Noticias         │                 │  estados, KPIs,       │                │  actual, pestaña   │
 │  Banxico (opcional)      │                 │  noticias, macro,     │                │  KPIs y precios)   │
 │  empresas.txt, noticias, │                 │  portafolio           │ ◀───────────── │ servidor MCP       │
 │  operaciones.csv (main)  │                 └──────────────────────┘                │  (Claude)          │
 └──────────────────────────┘                                                         └────────────────────┘
```

## Qué trae

| Comando | Tecla | Pantalla |
|---|---|---|
| `PANEL` | F2 | Índices, mapa de calor por sector (1D a 1A), el fondo hoy contra el MEXTRAC, ganadoras, perdedoras, más operadas, noticias y eventos |
| `MERCADO` · `TOP` | F3 | Monitor del universo: precio, cambio, rangos del día y de 52 semanas, rendimientos, P/U, VE/UAFIDA, dividendo, valor de mercado |
| `FEMSAUBD` | F4 | **Ficha de la emisora** con pestañas: Resumen (`DES`), Gráfica (`GP`), Financieros (`FA`), **KPIs (`KPI`)**, Pares y valuación (`RV`), Noticias (`N`), Tesis del equipo (`TESIS`) y Dividendos (`DVD`) |
| `PORT` | F6 | Portafolio del fondo: valor, posiciones, peso efectivo con el ETF desglosado, desviación contra el índice, riesgo ex ante y revisión de la política de inversión |
| `N` | F7 | Noticias del equipo, de LSEG y de Google Noticias, con tono positivo, negativo o neutral |
| `ECO` | F8 | Divisas, tasas, índices y materias primas, con la **matriz de sensibilidad** de cada emisora al dólar, cobre, oro, plata, petróleo, gas y tasas de EUA |
| `EQS` | F9 | Filtro por KPIs con preajustes (QVM en vivo, valor, calidad, momentum, dividendos, defensivas, sobrevendidas, cerca de máximos) |
| `COMP A B C` | F10 | Compara emisoras: rendimiento base 100, correlaciones y KPIs lado a lado |
| `W` | | Listas de seguimiento y alertas de precio (se guardan en el navegador) |
| `CAL` | | Calendario de reportes, dividendos y eventos |
| `MCP` | | Cómo preguntarle a Claude con los datos de la terminal |
| `SYS` | | Estado de los datos: última corrida, cobertura, errores y avisos |

La línea de comandos entiende claves y nombres: `banorte kpi`, `femsa gp`, `COMP FEMSAUBD KOFUBL AC`, `N GFNORTEO`. Atajos: `/` o `Ctrl+K` para escribir, `↑ ↓ Tab` para las sugerencias, `Esc` para volver al panel. El botón **TEMA** cambia entre ámbar (estilo terminal) y marino (colores del fondo).

## La pestaña de KPIs

Está en la ficha de la terminal y también en la ficha del tablero actual (`index.html`, pestaña **KPIs**).

1. **Lo esencial:** los indicadores que más importan según el tipo de empresa. Para bancos son MIN, eficiencia, costo de riesgo y crecimiento de la cartera; para las demás, crecimiento, márgenes, ROE, ROIC, deuda y valuación.
2. **KPIs operativos del sector:** los que captura el equipo de los reportes trimestrales (VMT de OXXO, volumen de KOF, cash cost de Grupo México, MIN e IMOR de BanBajío, tráfico de Pinfra…), más el catálogo de lo que conviene vigilar en cada sector.
3. **Calculados por el pipeline** con los estados financieros de Yahoo Finance: crecimiento, márgenes, rentabilidad, balance y liquidez, flujo, indicadores bancarios o de seguros, valuación (también contra su propia historia), rendimiento en bolsa, riesgo, técnico y liquidez.
4. **Factores QVM:** los del modelo del equipo junto a una aproximación con datos públicos de hoy.

Cada KPI trae su valor, el periodo, una mini gráfica trimestral, la tendencia, la mediana de sus **pares** y del **universo**, su percentil, y la fórmula con lo que mide (botón `i`). Si le das clic al valor se abre el ranking de las 37 emisoras para ese indicador. El borde verde o rojo dice si está mejor o peor que la mediana de sus pares.

**Capturar KPIs operativos:** en `empresas.txt`, dentro del bloque de la emisora:

```
=== FEMSAUBD ===
kpis:
  - Ventas mismas tiendas OXXO México | +9.5% | 2T26 | ticket +7.4%, tráfico +2.0% | Crecimiento orgánico
  - Margen operativo OXXO México | 10.0% | 2T26 | +10 pb a/a | Rentabilidad del negocio principal
```

Formato: `nombre | valor | periodo | tendencia | por qué importa`. Al guardar el archivo en `main`, Actions recalcula y la terminal y el tablero lo muestran.

## Sin vigilante: cuándo se actualiza

El workflow `.github/workflows/terminal-datos.yml` corre:

- **Cada 15 minutos, de lunes a viernes, durante la sesión** (modo rápido): cotizaciones, intradía y portafolio. La BMV opera de 9:30 a 16:00 hora de Nueva York: de 7:30 a 14:00 CDMX con el horario de verano de EUA y de 8:30 a 15:00 sin él. El cron cubre los dos horarios.
- **A las 6:20 y a las 16:40 CDMX** (modo completo): velas de cinco años, estados financieros, múltiplos, consenso de analistas, KPIs, factores, noticias y macro.
- **Cada vez que cambian en `main`** `empresas.txt`, `noticias.txt`, `operaciones.csv`, `parametros.json` o `calendario.csv`.
- **A mano**, desde *Actions → Terminal · datos → Run workflow*.

La rama `datos` guarda un solo commit que se reemplaza en cada corrida, así que no crece ni ensucia el historial de `main`. Si una fuente falla, se conserva lo último publicado y el error queda en `estado.json`; la terminal lo muestra en la barra inferior y en `SYS`.

El tablero actual también aprovecha esta rama: lee el `cotizaciones.csv` que publica Actions y usa el corte más reciente entre ese y el del vigilante. Con el vigilante apagado, sus precios siguen al día. La pestaña de KPIs de sus fichas lee los mismos `kpis.json`.

## Portafolio sin el tracker

`portafolio.json` se reconstruye desde `operaciones.csv` y `parametros.json` con la misma contabilidad del tracker de Excel:

- efectivo por fecha de operación;
- valor = títulos × cierre + efectivo;
- rendimiento diario V(t)/V(t−1) − 1, acumulado desde el portafolio de referencia;
- benchmark = precio del MEXTRAC09, estimado con la canasta del índice los días en que no opera;
- TE ex post = desviación de la diferencia diaria × √252.

Con los cierres de Refinitiv reproduce **al centavo** la serie de `rendimientos.csv`: valor, rendimiento, MEXTRAC y TE coinciden a seis decimales del 19 al 30 de octubre. Para registrar una operación nueva basta agregar su renglón a `operaciones.csv`.

## Fuentes

| Dato | Fuente |
|---|---|
| Cotizaciones, intradía de 5 min, velas diarias, dividendos | Yahoo Finance (biblioteca `yfinance`) |
| Estados financieros trimestrales y anuales, múltiplos históricos, consenso y precio objetivo | Yahoo Finance |
| Noticias automáticas en español | RSS de Google Noticias |
| Tasa objetivo, TIIE, CETES, FIX, inflación | Banxico SIE. Es opcional: hay que agregar el secreto `BANXICO_TOKEN` (token gratuito) en *Settings → Secrets and variables → Actions* |
| Tesis, catalizadores, riesgos, KPIs operativos y factores | `empresas.txt` (equipo) |
| Noticias curadas y de LSEG | `noticias.txt` (equipo y vigilante) |
| Operaciones, pesos y parámetros del fondo | `operaciones.csv`, `parametros.json` |
| Primera carga (semilla) | Histórico de LSEG Refinitiv que ya está en el repositorio (`historico.csv`, `ohlc.csv`, `macro.csv`…) |

Cuando la emisora reporta en dólares (Grupo México, Peñoles, Orbia…), los múltiplos convierten sus estados a pesos con el USD/MXN del día.

## IA · MCP

`terminal/mcp/servidor_mcp.py` expone los datos como herramientas MCP (Model Context Protocol) para Claude Desktop, Claude Code o cualquier cliente MCP. Solo usa la biblioteca estándar de Python.

```bash
claude mcp add north-star -- python3 terminal/mcp/servidor_mcp.py
```

Herramientas: `buscar_emisora`, `cotizacion`, `ficha`, `kpis`, `ranking_kpi`, `filtrar`, `noticias`, `portafolio`, `macro`, `estados_financieros`, `comparar` y `estado_datos`. Por omisión descarga los JSON de la rama `datos`. Con `--local carpeta` lee una copia local.

## Puesta en marcha (una sola vez)

1. Fusionar esta rama con `main`. GitHub Pages ya publica `main`, así que la terminal queda en `/terminal/`.
2. En *Settings → Actions → General*, confirmar que Actions está habilitado. El workflow pide sus propios permisos de escritura (`contents: write`).
3. En *Actions → Terminal · datos → Run workflow*, correr la primera vez en modo **completo**. Crea la rama `datos` con la semilla de Refinitiv y la primera descarga de Yahoo. Desde ahí corre solo.
4. Opcional: el secreto `BANXICO_TOKEN` para las series de Banxico.

## Desarrollo local

```bash
python3 terminal/pipeline/actualizar.py --modo semilla      # datos de prueba sin red en terminal/datos/ (ignorada por git)
python3 -m http.server 8000                                 # en la raíz del repositorio
# abrir http://localhost:8000/terminal/
pip install -r terminal/pipeline/requirements.txt pytest
python -m pytest terminal/pipeline/pruebas -q               # pipeline con un yfinance simulado
python3 terminal/mcp/prueba_mcp.py                          # servidor MCP
```

```
terminal/
├── index.html, css/, js/       la página (sin compilación: HTML, CSS y JavaScript)
├── pipeline/                   descarga y cálculo (Python; lo corre GitHub Actions)
│   ├── actualizar.py           orquestador: --modo rapido | completo | semilla
│   ├── fuente_yahoo.py, fuente_noticias.py, fuente_banxico.py
│   ├── kpis.py                 KPIs, catálogo por sector, comparación contra pares, QVM
│   ├── portafolio.py           reconstrucción del fondo desde operaciones.csv
│   ├── fichas.py, universo.py, util.py
│   └── pruebas/
└── mcp/                        servidor MCP y su prueba
```

## Notas y límites

- Yahoo Finance publica los precios de la BMV con unos minutos de retraso y a veces deja huecos. El pipeline reintenta y conserva el último dato bueno. Si una emisora no responde, su precio aparece marcado con `*`.
- Algunos KPIs bancarios y de seguros son **aproximaciones con datos públicos**: el margen financiero sobre activos aproxima el MIN y los siniestros sobre ingresos aproximan la siniestralidad. Los oficiales (MIN, IMOR, ICAP, índice combinado) van como KPIs operativos en `empresas.txt`.
- El QVM en vivo es una aproximación del modelo M-tilt para ver si la señal sigue vigente entre rebalanceos; la referencia es el modelo del equipo.
- **Licencias:** el código es original; no copia código de FinceptTerminal (AGPL-3.0), y «Fincept» es marca de Fincept Corporation. Las gráficas usan [Lightweight Charts](https://github.com/tradingview/lightweight-charts) de TradingView (Apache-2.0, con su logotipo de atribución).
