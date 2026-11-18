---
fecha_corte: 2026-11-18
hora_publicacion: 2026-11-18 10:01 CDMX
fuente_precios: PRELIMINAR 18-nov · cotizaciones de Workspace 09:52 (se sustituye con el Price Close después del cierre)
version: v7.0
dias_habiles_desde_dia0: 21
tablero: https://northstar-strategies.github.io/bbva-clinicas/
---

**Aviso: el 18-nov es PRELIMINAR (bolsa abierta).** Cotizaciones de Workspace de las 09:52. El 17-nov ya es cierre oficial (Price Close; alfa acumulado −326.1 pb). La réplica en Python da lo mismo que el tracker recalculado (al 18-nov, alfa acumulado −354.0 pb).

# North Star Strategies · estado del fondo al mié 18-nov-2026

## Cómo leer este archivo

- North Star Strategies es un fondo de acciones mexicanas del programa ITESM-BBVA. Su benchmark es el MEXTRAC09, el ETF que replica el S&P/BMV IPC CompMX Rentable ESG Tilted TR.
- El día 0 es el cierre del vie 16-oct-2026. Nada anterior cuenta como rendimiento ni como alfa.
- Las cifras salen del tracker de Excel, replicado en Python y cuadrado a diferencia 0. Alfa = rendimiento de la cartera menos el del MEXTRAC09, en puntos base (pb).
- Si `fecha_corte` tiene más de un día hábil de antigüedad, el dato está viejo: dilo antes de usarlo.

## Resumen

- Valor del portafolio: $10,589,458.25
- Caja: $12,245.04 (0.12% del portafolio)

| | Día (mié 18-nov) | Semana (desde vie 13-nov) | Desde el día 0 | Desde el día 0 con la penalización de 30 pb |
|---|---:|---:|---:|---:|
| Cartera | -1.12% | -2.09% | +2.21% | +1.91% |
| MEXTRAC09 | -0.83% | -1.72% | +5.75% | +5.75% |
| Alfa | -29.66 pb | -36.89 pb | -354.01 pb | -384.01 pb |

## Cumplimiento

| Regla | Valor | Límite | Estado |
|---|---:|---|---|
| Beta ex ante | 0.91 | 0.70 a 1.30 | OK |
| Tracking error ex ante, anual | 5.88% | máximo 10% | OK |
| Caja | 0.12% | 0% a 5% | OK |
| Desviación máxima por emisora (FEMSAUBD) | 7.89 pp | ±10 pp | OK |

Tracking error realizado desde el día 0, anual: 7.10% (informativo).

## Alertas

- Stop-loss de BBAJIOO: Vigilar (-1.86 σ de TE, -0.79 σ propias).
- Stop-loss de PEOLES: Vigilar (-2.91 σ de TE, -2.05 σ propias).
- Stop-loss de GMEXICOB: Vigilar (-2.74 σ de TE, -1.75 σ propias).
- Precio de último hecho, no Price Close, el mié 21-oct: MEXTRAC.
- Caja negativa (sobregiro) en 4 cierres, del mié 21-oct al lun 26-oct. Ya está corregida.

## Posiciones

| Emisora | Títulos | Precio | Valor | Peso | Peso en el benchmark | Peso activo | Rendimiento del día | Rendimiento desde el día 0 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| MEXTRAC09 | 38,326 | $71.91 | $2,756,022.66 | 26.03% | es el benchmark | +0.00 pp | -0.83% | +5.75% |
| FEMSAUBD | 6,921 | $240.78 | $1,666,438.38 | 15.74% | 10.61% | +7.89 pp | -0.64% | +3.03% |
| GMEXICOB | 5,301 | $203.39 | $1,078,170.39 | 10.18% | 7.84% | +4.38 pp | -4.44% | -16.78% |
| KOFUBL | 3,638 | $222.50 | $809,455.00 | 7.64% | 8.21% | +1.57 pp | +0.00% | +1.40% |
| BOLSAA | 16,440 | $37.81 | $621,596.40 | 5.87% | 0.00% | +5.87 pp | -2.50% | +1.20% |
| GAPB | 1,435 | $425.64 | $610,793.40 | 5.77% | 10.63% | -2.10 pp | -0.69% | +18.55% |
| AMXB | 23,149 | $23.72 | $549,094.28 | 5.19% | 10.70% | -2.73 pp | -0.38% | +13.32% |
| GFNORTEO | 2,430 | $200.38 | $486,923.40 | 4.60% | 8.89% | -1.97 pp | -0.80% | -2.26% |
| PINFRA | 1,233 | $310.11 | $382,365.63 | 3.61% | 0.63% | +3.15 pp | +0.16% | +4.69% |
| WALMEX | 6,439 | $55.20 | $355,432.80 | 3.36% | 7.92% | -2.50 pp | +1.27% | +13.33% |
| AC | 1,481 | $235.70 | $349,071.70 | 3.30% | 7.79% | -2.47 pp | -1.79% | +13.37% |
| BBAJIOO | 5,399 | $55.28 | $298,456.72 | 2.82% | 1.68% | +1.57 pp | -0.91% | -4.44% |
| MEGACPO | 3,980 | $58.01 | $230,879.80 | 2.18% | 0.61% | +1.73 pp | +0.02% | +2.13% |
| ASURB | 427 | $494.59 | $211,189.93 | 1.99% | 6.06% | -2.49 pp | -0.39% | +11.68% |
| PEOLES | 181 | $716.02 | $129,599.62 | 1.22% | 0.00% | +1.22 pp | -3.88% | -20.40% |
| OMAB | 170 | $245.43 | $41,723.10 | 0.39% | 3.91% | -2.50 pp | -1.11% | +15.84% |
| Efectivo | | | $12,245.04 | 0.12% | 0.00% | | | |

Peso = posición directa al cierre. Peso activo = peso con el MEXTRAC09 abierto en sus emisoras menos el peso en el benchmark. El rendimiento desde el día 0 es el del precio de la emisora, aunque se haya comprado después.

## Quién hizo el alfa

- Hoy sumaron: PINFRA +3.06 pb, AC +2.42 pb, FEMSAUBD +1.50 pb. Restaron: GMEXICOB -16.27 pb, BOLSAA -9.96 pb, WALMEX -5.22 pb.
- Desde el día 0 sumaron: GFNORTEO +17.13 pb, KIMBERA +11.52 pb, CEMEXCPO +8.48 pb. Restaron: GMEXICOB -119.21 pb, PEOLES -41.12 pb, GAPB -28.93 pb.

| Pieza | Hoy (mié 18-nov) | Desde el día 0 |
|---|---:|---:|
| Emisoras | -36.83 pb | -356.59 pb |
| Efectivo | +0.07 pb | -3.78 pb |
| MEXTRAC09 contra su canasta (o estimado) | +7.11 pb | +7.22 pb |
| Operaciones (ejecución contra cierre) | +0.00 pb | +0.52 pb |
| Comisión e IVA | +0.00 pb | -1.37 pb |
| Total = alfa | -29.66 pb | -354.01 pb |

Por sector (Brinson-Fachler). Asignación: por pesar distinto que el benchmark. Selección: por escoger mejores o peores acciones. Interacción: por cargar más justo donde se escogió mejor o peor. Los días se enlazan con Cariño.

| Sector | Asignación hoy | Selección hoy | Interacción hoy | Asignación desde el día 0 | Selección desde el día 0 | Interacción desde el día 0 |
|---|---:|---:|---:|---:|---:|---:|
| Consumo básico | -0.39 pb | -7.54 pb | +0.10 pb | -0.17 pb | -89.55 pb | -1.11 pb |
| Financieras | +0.26 pb | -9.06 pb | -2.12 pb | -18.33 pb | -9.19 pb | -1.60 pb |
| Industriales | -1.04 pb | +2.97 pb | -0.61 pb | -41.65 pb | -36.90 pb | +8.07 pb |
| Materiales | -14.91 pb | -3.50 pb | -1.78 pb | -116.45 pb | -23.49 pb | -11.91 pb |
| Servicios de comunicación | -0.59 pb | +1.36 pb | -0.17 pb | -7.45 pb | -11.91 pb | +1.33 pb |
| Inmobiliario | +0.18 pb | +0.00 pb | +0.00 pb | +3.71 pb | +0.00 pb | +0.00 pb |
| Efectivo | +0.07 pb | +0.00 pb | +0.00 pb | -3.78 pb | +0.00 pb | +0.00 pb |

## Operaciones de los últimos 5 días hábiles (desde el mié 11-nov)

| Fecha | Tipo | Emisora | Títulos | Precio | Comisión + IVA | Motivo |
|---|---|---|---:|---:|---:|---|
| mié 11-nov | Compra | AC | 12 | $238.73 | $9.96 | Reinversión del dividendo |
| mié 11-nov | Compra | GAPB | 18 | $449.07 | $28.13 | Reinversión del dividendo |
| mié 11-nov | Compra | GAPB | 14 | $449.07 | $21.88 | Reinversión del dividendo |
| mié 11-nov | Compra | GAPB | 31 | $449.07 | $48.44 | Reinversión del dividendo |
| mar 17-nov | Compra | AMXB | 255 | $23.79 | $21.11 | Reinversión del dividendo |
| mié 11-nov | Dividendo | AMXB | 22,894 | $0.27 | $0.00 | Dividendo en efectivo |
| mié 18-nov | Dividendo | WALMEX | 6,439 | $0.58 | $0.00 | Dividendo en efectivo |

## Próximos eventos y dividendos (14 días)

- jue 19-nov · ANTHROPIC EUA NVIDIA · Evento: IPO de Anthropic en Nasdaq (ANT): precio el 18-nov y cotiza el 19-nov
- jue 19-nov · CHINA EUA · Evento: Bilateral Trump–Xi y primera trilateral Trump–Xi–Putin
- mar 24-nov · OMAB · Dividendo de $6.2803 por acción. Fecha ex: mar 24-nov. Pago: mié 25-nov. Nos toca $1,067.64 por 170 títulos (estimado).
- vie 27-nov · ASURB · Dividendo de $10.0000 por acción. Fecha ex: vie 27-nov. Pago: lun 30-nov. Nos toca $4,270.00 por 427 títulos (estimado).

Para cobrar un dividendo hay que tener los títulos al cierre del día hábil anterior a la fecha ex. Solo se listan emisoras en cartera.

## Macro del mié 18-nov: lo que más se movió

Sin datos de macro para esta fecha.

## Titulares de la sesión

- mié 18-nov 08:37 · Reuters · MERCADO: Bolsa mexicana perfila cuarta jornada de pérdidas tras alcanzar récord máximo
- mié 18-nov 08:30 · Reuters · PEOLES: Mexicana Industrias Peñoles firma acuerdo de energía renovable a 20 años con Atlas Renewable Energy
- mié 18-nov 06:52 · Reuters · MERCADO: GLOBAL MARKETS -Stocks slip as investors mull Nvidia earnings; Anthropic IPO to test AI boom
- mié 18-nov 04:47 · Reuters · MERCADO: EMERGING MARKETS-EM stocks edge up after Nvidia results; South African assets fall post inflation
- mié 18-nov 08:25 · Reuters · EUA: ACTUALIZA 2-Sheinbaum dice hay avances en conversaciones comerciales tras reunión con Trump en China

## Supuestos

- r_caja = 0%: no se sabe si BBVA invierte la caja en un fondo de liquidez.
- Fin de la gestión: vie 27-nov-2026 (por confirmar con BBVA).
- Comisión de 0.30% por operación más 16% de IVA sobre la comisión.
- Penalización de los profesores: 30 pb sobre el rendimiento final.
- Mandato: caja de 0% a 5%, tracking error máximo de 10%, beta de 0.70 a 1.30 y desviación máxima por emisora de ±10 pp.
