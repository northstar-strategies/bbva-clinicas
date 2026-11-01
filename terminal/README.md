# North Star Terminal

Terminal financiera del **Fondo de Inversión ITESM-BBVA** (North Star Strategies) para las 37 emisoras de la BMV que analiza el fondo y el ETF MEXTRAC 09. La idea viene de [FinceptTerminal](https://github.com/Fincept-Corporation/FinceptTerminal) y de Bloomberg: línea de comandos, teclas de función, datos densos y fichas completas. Está hecha desde cero como página web, enfocada en el fondo y **sin necesidad del vigilante**.

- **Abrir:** `https://northstar-strategies.github.io/bbva-clinicas/terminal/`, o desde el menú lateral del tablero en **North Star Terminal**.
- **Se actualiza sola:** GitHub Actions descarga los datos en la nube y los publica en la rama `datos`. No hace falta tener ninguna computadora encendida.

```
 GitHub Actions (nube)                        rama «datos»                          navegador
 ┌──────────────────────────┐   cada 15 min   ┌──────────────────────┐   cada 1 min   ┌────────────────────┐
 │ terminal/pipeline        │ ──────────────▶ │ terminal/datos/*.json │ ◀───────────── │ terminal/ (página) │
 │  precios diferidos y     │   y al cierre   │  cotizaciones, velas, │                │ index.html (tablero│
 │  estados financieros     │                 │  estados, KPIs,       │                │  actual, pestaña   │
 │  Google Noticias         │                 │  noticias, macro,     │                │  KPIs y precios)   │
 │  Banxico (opcional)      │                 │  portafolio y alfa,   │ ◀───────────── │ servidor MCP       │
 │  empresas.txt, investig.,│                 │  investigación,       │                │  (Claude)          │
 │  operaciones.csv (main)  │                 │  sensibilidades       │                └────────────────────┘
 └──────────────────────────┘                 └──────────────────────┘
```

## Qué trae

| Comando | Tecla | Pantalla |
|---|---|---|
| `PANEL` | F2 | Índices, mapa de calor por sector (1D a 1A), el fondo hoy contra el MEXTRAC, ganadoras, perdedoras, más operadas, noticias y eventos |
| `MERCADO` · `TOP` | F3 | Monitor del universo: precio, cambio, rangos del día y de 52 semanas, rendimientos, P/U, VE/UAFIDA, dividendo, valor de mercado |
| `FEMSAUBD` | F4 | **Ficha de la emisora** con pestañas: Resumen (`DES`), Gráfica (`GP`), Financieros (`FA`), **KPIs (`KPI`)** con su historia, **Modelo y drivers (`MOD`)**, Pares y valuación (`RV`), Noticias (`N`), Tesis del equipo (`TESIS`) y Dividendos (`DVD`) |
| `PORT` | F6 | Portafolio del fondo: valor, posiciones, **contribución al alfa de cada posición** (abiertas, cerradas, solo vía índice y ventas), peso efectivo con el ETF desglosado, desviación contra el índice, riesgo ex ante y revisión de la política de inversión |
| `N` | F7 | Noticias del equipo, de LSEG y de Google Noticias, con tono positivo, negativo o neutral |
| `ECO` | F8 | Divisas, tasas, índices y materias primas, con la **matriz de sensibilidad** de cada emisora al dólar, cobre, oro, plata, petróleo, gas y tasas de EUA |
| `EQS` | F9 | Filtro por KPIs con preajustes (QVM en vivo, valor, calidad, momentum, dividendos, defensivas, sobrevendidas, cerca de máximos) |
| `COMP A B C` | F10 | Compara emisoras: rendimiento base 100, correlaciones y KPIs lado a lado |
| `W` | | Listas de seguimiento y alertas de precio (se guardan en el navegador) |
| `CAL` | | Calendario de reportes, dividendos y eventos |
| `MCP` | | Cómo preguntarle a Claude con los datos de la terminal |
| `SYS` | | Estado de los datos: última corrida, cobertura, errores y avisos |

La línea de comandos entiende claves y nombres: `banorte kpi`, `gmexico mod`, `femsa gp`, `COMP FEMSAUBD KOFUBL AC`, `N GFNORTEO`. Atajos: `/` o `Ctrl+K` para escribir, `↑ ↓ Tab` para las sugerencias, `Esc` para volver al panel. El botón **TEMA** cambia entre ámbar (estilo terminal) y marino (colores del fondo).

## La pestaña de KPIs

Está en la ficha de la terminal y también en la ficha del tablero actual (`index.html`, pestaña **KPIs**).

1. **Lo esencial:** los indicadores que más importan según el tipo de empresa. Para bancos son MIN, eficiencia, costo de riesgo y crecimiento de la cartera; para las demás, crecimiento, márgenes, ROE, ROIC, deuda y valuación.
2. **Historia de KPIs** (solo en la terminal): las tablas de KPIs operativos 2022 → 3T26 de la investigación del equipo (lo no verificado aparece como «n.v.», nunca rellenado), la historia **anual 2021–2025** de ingresos, UAFIDA, márgenes, utilidad, ROE y deuda neta/UAFIDA con su CAGR, y la historia **trimestral** de los KPIs financieros. Al lado, **por qué son relevantes en nuestro análisis**: cuánto movería el precio cada driver (ver *Modelo y drivers*), qué mide cada KPI operativo y en qué factor del modelo QVM entra cada uno.
3. **KPIs operativos del sector:** los que captura el equipo de los reportes trimestrales (VMT de OXXO, volumen de KOF, cash cost de Grupo México, MIN e IMOR de BanBajío, tráfico de Pinfra…), más el catálogo de lo que conviene vigilar en cada sector.
4. **Calculados por el pipeline** con los estados financieros reportados: crecimiento, márgenes, rentabilidad, balance y liquidez, flujo, indicadores bancarios o de seguros, valuación (también contra su propia historia), rendimiento en bolsa, riesgo, técnico y liquidez.
5. **Factores QVM:** los del modelo del equipo junto a una aproximación con datos públicos de hoy.

Cada KPI trae su valor, el periodo, una mini gráfica trimestral, la tendencia, la mediana de sus **pares** y del **universo**, su percentil, y la fórmula con lo que mide (botón `i`). Si le das clic al valor se abre el ranking de las 37 emisoras para ese indicador. El borde verde o rojo dice si está mejor o peor que la mediana de sus pares.

**Capturar KPIs operativos:** en `empresas.txt`, dentro del bloque de la emisora:

```
=== FEMSAUBD ===
kpis:
  - Ventas mismas tiendas OXXO México | +9.5% | 2T26 | ticket +7.4%, tráfico +2.0% | Crecimiento orgánico
  - Margen operativo OXXO México | 10.0% | 2T26 | +10 pb a/a | Rentabilidad del negocio principal
```

Formato: `nombre | valor | periodo | tendencia | por qué importa`. Al guardar el archivo en `main`, Actions recalcula y la terminal y el tablero lo muestran.

## Modelo y drivers: cuánto mueve el precio cada KPI

Pestaña `MOD` de la ficha (`gmexico mod`). Junta la investigación con la valuación:

- **Modelo de negocio** y mezcla de segmentos según la investigación 3T26 (por ejemplo, OXXO México es 36.8% de los ingresos de FEMSA; el cobre, 74.3% de las ventas de Americas Mining).
- **Drivers de valor**: para cada uno, su estado actual (3T26), un movimiento típico y el efecto en UAFIDA (o utilidad) y en el **precio a múltiplo constante**, con la fórmula a la vista (botón `ƒ`). El puente es:
  - no financieras: `Δprecio = (VE/capital) × ΔUAFIDA/UAFIDA`, con VE/capital = VE/UAFIDA ÷ (VE/UAFIDA − deuda neta/UAFIDA);
  - bancos y seguros: `Δprecio = Δutilidad/utilidad` con P/U constante (MIN y costo de riesgo sobre la cartera, después de impuestos).
  - Ejemplos con los datos del 1-nov-2026: cobre +10% ⇒ Grupo México +9.9%; +1 pp de VMT de OXXO ⇒ FEMSA +1.3%; +10 pb de MIN ⇒ Banorte +1.4%; +2% de pasajeros ⇒ GAP +3.1%.
- **Simulador**: barras para combinar drivers y ver la UAFIDA, el precio y el precio implícito del escenario.
- **Sensibilidad de mercado (empírica)**: regresión de 104 rendimientos semanales contra el IPC y cada factor (dólar, cobre, oro, plata, petróleo, gas, tasas de EUA, S&P 500, real, granos, azúcar). La beta neta descuenta el mercado; se marca si es significativa (|t| ≥ 2). Que el mercado reaccione menos que el modelo es normal: descuenta que los precios de materias primas y las tasas regresan a su promedio.
- **Catalizadores, juicio y fuentes** de la investigación, con las ligas originales numeradas.

Los drivers y sus supuestos están en **`investigacion/drivers.json`** (participación del segmento, margen incremental, volumen, regalías…). Se pueden editar en GitHub: la siguiente corrida recalcula todo. Las 15 emisoras de Nivel 1 tienen drivers propios; las demás usan un marco sectorial (ingresos, margen y tipo de cambio si reportan en dólares).

## Investigación del equipo

Los documentos de investigación van en **`investigacion/`** en Markdown (hoy, `KPIs_operativos_y_catalizadores_3T26.md`). `pipeline/investigacion.py` los separa por emisora respetando el formato del documento: encabezado `#### N.M Nombre (CLAVE) — Nivel X · …`, etiquetas en negritas **(a) Modelo**, **(b) Tabla de KPIs**, **(c) Narrativa**, **(d) Catalizadores históricos**, **(e) Prospectivos**, **(f) Consenso**, **(g) Fuentes**, más las tablas compactas de Nivel 2 y 3, el resumen ejecutivo, los catalizadores macro, las recomendaciones y las limitaciones. Para actualizarla basta subir la nueva versión del archivo (o uno nuevo con el mismo formato) a `main`.

## Contribución al alfa por posición

En `PORT`, el panel **Contribución al alfa por posición** descompone la diferencia acumulada contra el MEXTRAC con el mismo método del tracker de Excel (`atribucion_diaria.csv`):

- por emisora, `aporte = (w_directo + w_ETF·b − b) × (r − r_MEXTRAC)` con pesos al cierre del día anterior, rendimiento total (el dividendo entra el día ex) y pesos del índice `b` del tracker, arrastrados con los precios después de su último registro;
- efectos que no son de una emisora: **efectivo** (caja que no rinde), **premio del ETF** contra su canasta, **operaciones del día** (comprar abajo o vender arriba del cierre) y **comisiones**;
- los días se ligan con **Cariño**, así que la suma de todos los renglones da exactamente el alfa acumulado.

Se agrupa en **abiertas** (lo que el fondo tiene hoy), **cerradas** (lo que se vendió por completo, con lo que aportó mientras se tuvo), **solo vía índice** (emisoras que solo se tienen a través del ETF y quedan subponderadas) y **ventas**, con la utilidad realizada contra el costo promedio. Con los cierres de Refinitiv reproduce los 333 aportes diarios del tracker (19–29 de octubre) con diferencia máxima de 5 × 10⁻¹³; la ficha de cada emisora muestra su aporte en «Posición en el fondo».

## Sin vigilante: cuándo se actualiza

El workflow `.github/workflows/terminal-datos.yml` corre:

- **Cada 15 minutos, de lunes a viernes, durante la sesión** (modo rápido): cotizaciones, intradía y portafolio. La BMV opera de 9:30 a 16:00 hora de Nueva York: de 7:30 a 14:00 CDMX con el horario de verano de EUA y de 8:30 a 15:00 sin él. El cron cubre los dos horarios.
- **A las 6:20 y a las 16:40 CDMX** (modo completo): velas de cinco años, estados financieros, múltiplos, consenso de analistas, KPIs, factores, noticias y macro.
- **Cada vez que cambian en `main`** `empresas.txt`, `noticias.txt`, `operaciones.csv`, `parametros.json`, `calendario.csv`, `atribucion_diaria.csv` o los dividendos; si cambia la investigación (`investigacion/`) o el código del pipeline, corre el modo completo.
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
| Cotizaciones, intradía de 5 min, velas diarias, dividendos | Precios de mercado diferidos (unos minutos), descargados con la biblioteca abierta `yfinance` |
| Estados financieros trimestrales y anuales, múltiplos históricos, consenso y precio objetivo | Estados financieros reportados por las emisoras, por la misma vía |
| Investigación: KPIs operativos 2022–3T26, catalizadores, drivers | `investigacion/` (equipo) |
| Noticias automáticas en español | RSS de Google Noticias |
| Tasa objetivo, TIIE, CETES, FIX, inflación | Banxico SIE. Es opcional: hay que agregar el secreto `BANXICO_TOKEN` (token gratuito) en *Settings → Secrets and variables → Actions* |
| Tesis, catalizadores, riesgos, KPIs operativos y factores | `empresas.txt` (equipo) |
| Noticias curadas y de LSEG | `noticias.txt` (equipo y vigilante) |
| Operaciones, pesos y parámetros del fondo | `operaciones.csv`, `parametros.json`; pesos del índice día a día de `atribucion_diaria.csv` (tracker) |
| Primera carga (semilla) | Histórico de LSEG Refinitiv que ya está en el repositorio (`historico.csv`, `ohlc.csv`, `macro.csv`…) |

Cuando la emisora reporta en dólares (Grupo México, Peñoles, Orbia…), los múltiplos convierten sus estados a pesos con el USD/MXN del día.

## IA · MCP

`terminal/mcp/servidor_mcp.py` expone los datos como herramientas MCP (Model Context Protocol) para Claude Desktop, Claude Code o cualquier cliente MCP. Solo usa la biblioteca estándar de Python.

```bash
claude mcp add north-star -- python3 terminal/mcp/servidor_mcp.py
```

Herramientas: `buscar_emisora`, `cotizacion`, `ficha`, `kpis`, `ranking_kpi`, `filtrar`, `noticias`, `portafolio`, **`atribucion_alfa`**, **`investigacion`**, **`sensibilidad`** (acepta un escenario, p. ej. `{"precio_cu": -10, "fx": 5}`), `macro`, `estados_financieros`, `comparar` y `estado_datos`. Por omisión descarga los JSON de la rama `datos`. Con `--local carpeta` lee una copia local.

## Puesta en marcha (una sola vez)

1. Fusionar esta rama con `main`. GitHub Pages ya publica `main`, así que la terminal queda en `/terminal/`.
2. En *Settings → Actions → General*, confirmar que Actions está habilitado. El workflow pide sus propios permisos de escritura (`contents: write`).
3. En *Actions → Terminal · datos → Run workflow*, correr la primera vez en modo **completo**. Crea la rama `datos` con la semilla de Refinitiv y la primera descarga de mercado. Desde ahí corre solo.
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
│   ├── portafolio.py           reconstrucción del fondo y atribución del alfa por posición
│   ├── investigacion.py        lee investigacion/*.md y lo separa por emisora
│   ├── sensibilidad.py         puente de valuación por driver y betas contra factores macro
│   ├── fichas.py, universo.py, util.py
│   └── pruebas/
└── mcp/                        servidor MCP y su prueba
investigacion/                  documentos del equipo (Markdown) y drivers.json
```

## Notas y límites

- Los precios de la BMV llegan con unos minutos de retraso y a veces con huecos. El pipeline reintenta y conserva el último dato bueno. Si una emisora no responde, su precio aparece marcado con `*`.
- A veces falta un trimestre o llega a medias. Las comparaciones contra el año anterior se buscan **por fecha**: si falta el trimestre base, el KPI queda «n/d» en lugar de comparar contra otro trimestre, y en «Lo esencial» se muestra el crecimiento de 12 meses. Los trimestres con ingresos negativos o vacíos se descartan.
- Algunos KPIs bancarios y de seguros son **aproximaciones con datos públicos**: el margen financiero sobre activos aproxima el MIN y los siniestros sobre ingresos aproximan la siniestralidad. El índice de eficiencia bancario no se calcula porque los gastos de operación publicados mezclan partidas. Los oficiales (MIN, IMOR, eficiencia, ICAP, índice combinado) van como KPIs operativos en `empresas.txt`.
- Los múltiplos (P/U, P/VL, VE/UAFIDA) son los reportados, que salen de cifras por acción; si difieren más de 3 veces del cálculo propio (señal de que la fuente no convirtió dólares a pesos, como en Grupo México), se usa el propio. La fuente aparece en el detalle de cada KPI.
- Las sensibilidades fundamentales son lineales y suponen múltiplo constante: sirven para movimientos moderados y para comparar drivers, no como precio objetivo. Los márgenes incrementales son supuestos explícitos en `investigacion/drivers.json`.
- El QVM en vivo es una aproximación del modelo M-tilt para ver si la señal sigue vigente entre rebalanceos; la referencia es el modelo del equipo.
- **Licencias:** el código es original; no copia código de FinceptTerminal (AGPL-3.0), y «Fincept» es marca de Fincept Corporation. Las gráficas usan [Lightweight Charts](https://github.com/tradingview/lightweight-charts) de TradingView (Apache-2.0, con su logotipo de atribución).
