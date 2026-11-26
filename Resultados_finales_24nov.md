---
title: Resultados finales · North Star Strategies
fecha_corte: 2026-11-24
estado: final
---

# Resultados finales al 24-nov-2026 · North Star Strategies (ITESM-BBVA)

Periodo de gestión cerrado · del cierre del 16-oct al cierre del 24-nov-2026 · 25 sesiones (el 2 y el 16-nov fueron inhábiles).
Cifras **finales**: salen del tracker (libro oficial), replicadas en Python y en la hoja Cierre de Excel. No dependen de precios en vivo ni de corridas posteriores del vigilante.

## Marcador

La cartera pasó de $10,360,497.91 a $10,628,154.33: +2.5834%, una ganancia de $267,656.42.

| Referencia | Papel | Rend. referencia | Mismo capital en la referencia | Alfa bruto | Alfa penalizado (−30 pb) | Veredicto |
|---|---|---:|---:|---:|---:|---|
| NAV | **Oficial** | +6.8824% | $713,046.03 | -429.89 pb | -459.89 pb | Perdimos por 4.30 pp |
| Precio | Comparativa (ejercicio) | +6.9265% | $717,616.84 | -434.30 pb | -464.30 pb | Perdimos por 4.34 pp |
| Índice | Comparativa (ejercicio) | +7.0390% | $729,276.44 | -445.56 pb | -475.56 pb | Perdimos por 4.46 pp |

## Resumen en 30 segundos

- **Cómo nos fue:** contra el NAV del MEXTRAC09, la referencia oficial, perdimos 429.89 pb (459.89 pb con la penalización): la cartera ganó +2.58% y el NAV +6.88%.
- **Qué más pesó:** GMEXICOB (-158.50 pb), PEOLES (-55.41 pb) y ASURB (-36.14 pb); la asignación sectorial explica -235.91 pb y la selección -191.86 pb.
- **Qué funcionó:** GFNORTEO (+20.93 pb) y la semana del 6 al 13-nov (+46.17 pb); costos bajos (-1.39 pb) y ejecución contra cierre +0.55 pb.

## Métricas lado a lado

| Métrica | NAV | Precio | Índice |
|---|---:|---:|---:|
| Hit ratio diario | 24% | 36% | 28% |
| Hit ratio semanal | 17% | 17% | 17% |
| Racha a favor / en contra (días) | 2 / 6 | 3 / 5 | 2 / 5 |
| Mejor día relativo | +35.61 pb | +76.29 pb | +27.08 pb |
| Peor día relativo | -70.46 pb | -158.01 pb | -70.28 pb |
| Ganancia prom. días a favor | +13.58 pb | +22.72 pb | +14.14 pb |
| Pérdida prom. días en contra | -25.99 pb | -38.81 pb | -29.24 pb |
| TE del periodo (σ×√25) | 1.23% | 2.16% | 1.37% |
| TE anualizado (σ×√252) | 3.91% | 6.86% | 4.36% |
| IR efectiva (alfa ÷ TE del periodo) | -3.49 | -2.01 | -3.24 |
| IR anualizada (referencia) | -10.62 | -6.12 | -9.87 |
| Beta ex post | 0.846 | 0.726 | 0.821 |
| Alfa de Jensen anual (Cetes 28 = 6.23%) | -32.09% | -25.02% | -31.78% |
| Correlación / R² | 0.938 / 0.880 | 0.795 / 0.633 | 0.925 / 0.856 |
| Captura al alza / a la baja | 0.69 / 1.15 | 0.65 / 1.06 | 0.68 / 1.16 |
| Caída máxima relativa | -4.02% | -4.06% | -4.16% |
| Beta ex ante (1 año) | 0.937 | 0.906 | 0.980 |
| TE ex ante (1 año) | 4.33% | 5.76% | 3.61% |
| VaR relativo histórico 95% 1 día | 0.39% ($41,266.71) | 0.54% ($57,481.52) | 0.37% ($39,069.55) |
| VaR relativo paramétrico 95% 1 día | 0.45% ($47,684.50) | 0.60% ($63,405.92) | 0.37% ($39,746.86) |
| Estadístico t del alfa diario | -3.34 | -1.93 | -3.11 |
| Intervalo bootstrap 95% del alfa | [-692, -184] pb | [-901, -30] pb | [-741, -173] pb |

**Absolutas de la cartera:** rendimiento +2.58%, volatilidad anualizada 10.14%, Sharpe 1.97 y Sortino 2.89 contra Cetes 28 (6.23%), caída máxima -3.41% (pico 2026-11-11, valle 2026-11-20, sin recuperar al 24-nov), VaR 95% a 1 día histórico 1.48% ($156,857.61) y paramétrico 1.61% ($170,714.65), CVaR 1.83% ($194,514.56).

> [!warning] 25 días no bastan
> El estadístico t y el intervalo por remuestreo (10,000 remuestreos, semilla 20261124) dicen que el resultado fue consistentemente negativo en estos 25 días, pero con tan pocos datos no se puede separar habilidad de suerte. Las cifras anualizadas son solo de referencia.

## Puente entre referencias

- Alfa contra NAV = alfa contra Índice + (R_Índice − R_NAV): -429.89 pb = -445.56 pb + +15.67 pb. Es la diferencia de seguimiento del ETF (comisiones, efectivo, réplica e impuestos); no hay datos para repartirla entre esas causas.
- Alfa contra NAV = alfa contra Precio + (R_Precio − R_NAV): -429.89 pb = -434.30 pb + +4.41 pb. Es el cambio en el premio del precio sobre el NAV: el 16-oct el precio era igual al NAV y el 24-nov quedó 0.04% arriba.
- Los dos puentes cierran en cero cada día y en el acumulado (`cierre/puente.csv`). El precio estimado de los días sin movimiento solo cambia el camino diario: en el acumulado el precio con y sin estimado da lo mismo porque el 24-nov el ETF operó.

## De dónde salió el resultado (contra NAV, Brinson-Hood-Beebower enlazado con Cariño)

| Pieza | pb | $ |
|---|---:|---:|
| Timing de mercado (efectivo contra acciones) | -7.87 pb | $-8,156.71 |
| Asignación sectorial | -235.91 pb | $-244,412.05 |
| Selección (stock picking) | -191.86 pb | $-198,773.10 |
| Interacción | -6.08 pb | $-6,295.69 |
| Premio o descuento de nuestro MEXTRAC09 contra su canasta | -2.79 pb | $-2,887.83 |
| Canasta del MEXTRAC09 contra el NAV | +15.45 pb | $16,009.62 |
| Operaciones (ejecución contra cierre) | +0.55 pb | $567.98 |
| Comisión e IVA | -1.39 pb | $-1,441.83 |
| Redondeo al centavo de dividendos | -0.00 pb |  |
| Total = alfa contra NAV | -429.89 pb |  |

Timing de mercado = efectivo contra acciones; la sobre y subponderación por sector es asignación. El renglón del MEXTRAC09 se separa en el premio de nuestro ETF contra su canasta y la canasta contra el NAV. Los dividendos entran una vez, en la fecha en que cuentan para la cartera.

| Sector | Asignación | Selección | Interacción | Total |
|---|---:|---:|---:|---:|
| Consumo básico | +4.16 pb | -82.51 pb | -1.28 pb | -79.63 pb |
| Consumo discrecional | +0.00 pb | +0.00 pb | +0.00 pb | +0.00 pb |
| Financieras | -23.13 pb | -5.91 pb | -0.87 pb | -29.91 pb |
| Industriales | -63.40 pb | -51.19 pb | +10.96 pb | -103.63 pb |
| Inmobiliario | +6.56 pb | +0.00 pb | +0.00 pb | +6.56 pb |
| Materiales | -153.08 pb | -33.57 pb | -17.03 pb | -203.68 pb |
| Salud | +0.00 pb | +0.00 pb | +0.00 pb | +0.00 pb |
| Servicios de comunicación | -7.01 pb | -18.67 pb | +2.14 pb | -23.54 pb |
| Efectivo | -7.87 pb | +0.00 pb | +0.00 pb | -7.87 pb |

**Las 10 emisoras de mayor efecto**

- **GMEXICOB** (Materiales): restó 158.5 pb: la tuvimos con más peso que el benchmark (12.0% contra 7.6% al cierre) y se quedó atrás al NAV (-23.3% desde el día 0 contra +6.9%).
- **PEOLES** (Materiales): restó 55.4 pb: la tuvimos con más peso que el benchmark (1.1% contra 0.0% al cierre) y se quedó atrás al NAV (-28.3% desde el día 0 contra +6.9%).
- **ASURB** (Industriales): restó 36.1 pb: la tuvimos con menos peso que el benchmark (3.8% contra 6.5% al cierre) y le ganó al NAV (+22.5% desde el día 0 contra +6.9%).
- **GAPB** (Industriales): restó 35.1 pb: la tuvimos con menos peso que el benchmark (8.5% contra 10.6% al cierre) y le ganó al NAV (+17.3% desde el día 0 contra +6.9%).
- **OMAB** (Industriales): restó 33.9 pb: la tuvimos con menos peso que el benchmark (1.4% contra 4.0% al cierre) y le ganó al NAV (+19.0% desde el día 0 contra +6.9%).
- **BOLSAA** (Financieras): restó 31.0 pb: la tuvimos con más peso que el benchmark (5.9% contra 0.0% al cierre) y se quedó atrás al NAV (+1.6% desde el día 0 contra +6.9%).
- **AC** (Consumo básico): restó 29.8 pb: la tuvimos con menos peso que el benchmark (5.5% contra 8.1% al cierre) y le ganó al NAV (+18.8% desde el día 0 contra +6.9%).
- **FEMSAUBD** (Consumo básico): restó 23.6 pb: la tuvimos con más peso que el benchmark (18.5% contra 10.6% al cierre) y se quedó atrás al NAV (+3.7% desde el día 0 contra +6.9%).
- **BIMBOA** (Consumo básico): restó 21.4 pb: la tuvimos con menos peso que el benchmark (0.6% contra 2.4% al cierre) y le ganó al NAV (+21.2% desde el día 0 contra +6.9%).
- **GFNORTEO** (Financieras): sumó 20.9 pb: la tuvimos con menos peso que el benchmark (6.8% contra 8.8% al cierre) y se quedó atrás al NAV (-2.9% desde el día 0 contra +6.9%).

Concentración: la emisora de mayor efecto explica 37% del alfa; las 3 primeras 58% y las 5 primeras 74%.

**Por semana (contra NAV)**

| Semana | Cartera | NAV | Alfa | Qué sumó y qué restó (pb del día, sin enlazar) |
|---|---:|---:|---:|---|
| 2026-10-16 a 2026-10-23 | +1.83% | +3.38% | -155.17 pb | Sumaron: KIMBERA +14.7, GENTERA +4.4, CEMEXCPO +3.6 · Restaron: GMEXICOB -51.1, BOLSAA -25.5, PEOLES -18.7 |
| 2026-10-23 a 2026-10-30 | -0.66% | +0.27% | -92.96 pb | Sumaron: GFNORTEO +5.3, TLEVISACPO +5.2, KIMBERA +4.9 · Restaron: FEMSAUBD -14.6, BOLSAA -12.8, OMAB -12.1 |
| 2026-10-30 a 2026-11-06 | +2.08% | +3.09% | -101.37 pb | Sumaron: GFNORTEO +6.9, PEOLES +4.5, MEGACPO +4.0 · Restaron: GMEXICOB -29.0, PINFRA -9.9, WALMEX -9.8 |
| 2026-11-06 a 2026-11-13 | +1.09% | +0.63% | +46.17 pb | Sumaron: BOLSAA +14.2, KOFUBL +6.6, KIMBERA +6.2 · Restaron: PEOLES -9.4, AC -7.6, ASURB -2.3 |
| 2026-11-13 a 2026-11-20 | -2.61% | -1.89% | -72.41 pb | Sumaron: PINFRA +10.0, FEMSAUBD +9.1, CEMEXCPO +6.8 · Restaron: GMEXICOB -49.2, PEOLES -17.9, ASURB -16.1 |
| 2026-11-20 a 2026-11-24 | +0.90% | +1.30% | -39.47 pb | Sumaron: WALMEX +7.0, PINFRA +3.1, BIMBOA +2.4 · Restaron: GMEXICOB -15.6, OMAB -12.1, FEMSAUBD -8.7 |

Mercado: el 24-nov el cobre cayó cerca de 5% y la plata cerca de 5% (LSEG, Kitco, Investing.com); GMEXICOB cayó 5.5% y PEÑOLES 3.7% ese día. Una coincidencia de fechas no prueba causa.

## Autopsia de la gestión

- **Escalera de decisiones:** la asignación de BBVA sin tocar desde el 16-oct habría hecho +2.5664%; la cartera real +2.5834%. Las operaciones, ya con costos y dividendos, sumaron +1.70 pb.
- **Escenarios hipotéticos:** el QVM alterno del 2-oct (hoja WhatIf_Modelo) habría hecho +0.46%. No existe un escenario de la cartera objetivo del M-tilt a lo largo del tiempo, y armarlo exigiría reglas nuevas: queda como limitación.
- **Ranking de decisiones (en retrospectiva, al 24-nov contra no hacerlas):** 79 operaciones en `cierre/decisiones.csv`; las de la semana de construcción (12 al 16-oct) se miden desde el cierre del 16-oct.
  - Mejores: 2026-10-15 venta 110 GMEXICOB (Construcción) $6,144.95; 2026-10-14 venta 100 GMEXICOB (Construcción) $5,586.31; 2026-10-16 compra 307 FEMSAUBD (Construcción) $2,683.18; 2026-10-16 compra 304 FEMSAUBD (Construcción) $2,656.96; 2026-10-16 compra 158 FEMSAUBD (Construcción) $1,380.92.
  - Peores: 2026-10-14 venta 1518 AMXB (Construcción) $-4,675.44; 2026-10-14 venta 20 GAPB (Construcción) $-1,721.80; 2026-10-14 venta 39 AC (Construcción) $-1,616.16; 2026-10-16 compra 580 BBAJIOO (Construcción) $-1,351.40; 2026-10-27 venta 500 AMXB (Corrección de sobregiro) $-968.96.
- **Costos:** comisión $1,210.57 + IVA $193.68 = $1,404.25 en 37 operaciones; rotación 3.8% del valor promedio; costaron -1.39 pb.
- **Dividendos:** cobrados $44,543.47; por cobrar $1,067.64 (OMAB, ex 24-nov, pago 25-nov); reinvertidos $43,998.96; en acciones: GMEXICOB: 27 títulos (1 por cada 194) y $79.37 de fracción, 23-nov. ASURB (ex 27-nov) queda fuera.
- **Reglas tácticas:** días-emisora en «Vigilar» del stop-loss: {'OK': 127, 'Sin sobrepeso': 725, 'Vigilar': 73}; take-profit: {'OK': 200, 'Sin sobrepeso': 725}. Ningún stop-loss ni take-profit pasó de «Vigilar» a una orden: después del día 0 las 10 ventas fueron por corrección del sobregiro y las 27 compras, 19 de rebalanceo al modelo y 8 de reinversión de dividendos. Las señales se miden contra el precio del ETF, como se decidieron.
- **Cumplimiento día por día** (`cierre/cumplimiento_diario.csv`, TE y beta contra NAV): 4 incumplimientos, todos de efectivo: 2026-10-21, 2026-10-22, 2026-10-23, 2026-10-26. Causa: la compra de 307 FEMSAUBD del 16-oct no se había capturado y dejó la caja en −0.62%; se corrigió con las ventas del 27-oct. ETF, pasiva y activa, ±10 pp por emisora, TE y beta cumplieron todos los días.

## Lecciones

**Hechos.** El resultado lo explican la asignación sectorial y la selección; el sobrepeso en Materiales (GMEXICOB y PEÑOLES) restó más de 200 pb, y el subpeso en aeropuertos y consumo que subieron (ASURB, GAPB, OMAB, AC, BIMBOA) restó otros ~150 pb. Los costos y la ejecución fueron marginales.

**Interpretación.** Las apuestas activas estuvieron concentradas en pocas emisoras ligadas a metales; un límite de concentración por factor (no solo por emisora) y revisar antes las señales de «Vigilar» habrían reducido la pérdida. El sobregiro de octubre fue un error de captura: conciliar contra la plataforma el mismo día lo habría evitado.

## Cómo se calculó

- Rendimiento = valor al cierre ÷ valor al cierre del 16-oct − 1; la cartera se valúa a precio de mercado, incluido nuestro MEXTRAC09 (con estimado los días sin movimiento).
- Alfa bruto = rendimiento acumulado de la cartera − el de la referencia; penalizado = bruto − 30 pb una sola vez (la penalización es de la referencia oficial; en Precio e Índice es ejercicio comparativo).
- TE ex post = σ de los alfas diarios × √25 (periodo) o × √252 (anual). Ex ante: posición del 24-nov sobre 252 escenarios diarios. VaR paramétrico = 1.645 σ.
- Atribución: pesos al cierre anterior con el MEXTRAC abierto en su canasta (PCF del 21-oct); Brinson-Fachler por sector; días enlazados con Cariño. Ver notas/Metodología de atribución.
- **Fuentes:** NAV = LSEG TR.FundNAV (MEXTRAC09.MX), revisado día por día con su fecha. Precio = LSEG TR.PriceClose (el 21-oct sin Price Close: 69.10, último hecho). Índice = S&P/BMV IPC CompMx Trailing Income Equities ESG Tilted Index (MXN) TR, S&P Dow Jones Indices, indexId 92411421 (TH0000), rendimiento total bruto en pesos; LSEG no lo tiene («Index is not available on Lipper Database»). Cetes 28 = 6.23% (Banxico, 20-oct). El MEXTRAC09 no pagó distribuciones en el periodo.
- Por licencia, en `cierre/` se publican rendimientos y no los niveles diarios del NAV ni del índice.
- **Supuestos:** r_caja = 0%; dividendos con fecha ex dentro de la gestión y pago después cuentan como por cobrar el 24-nov.

## Archivos

`cierre/resumen_referencias.csv`, `diario_referencias.csv`, `puente.csv`, `atribucion_cierre.csv`, `portafolio_final.csv`, `decisiones.csv` y `cumplimiento_diario.csv`.
