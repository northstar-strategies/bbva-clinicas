---
fecha_corte: 2026-11-11
hora_publicacion: 2026-11-11 17:57 CDMX
fuente_precios: último hecho en CUERVO; Price Close en el resto
version: v7.0
dias_habiles_desde_dia0: 17
tablero: https://northstar-strategies.github.io/bbva-clinicas/
---

# North Star Strategies · estado del fondo al mié 11-nov-2026

## Cómo leer este archivo

- North Star Strategies es un fondo de acciones mexicanas del programa ITESM-BBVA. Su benchmark es el MEXTRAC09, el ETF que replica el S&P/BMV IPC CompMX Rentable ESG Tilted TR.
- El día 0 es el cierre del vie 16-oct-2026. Nada anterior cuenta como rendimiento ni como alfa.
- Las cifras salen del tracker de Excel, replicado en Python y cuadrado a diferencia 0. Alfa = rendimiento de la cartera menos el del MEXTRAC09, en puntos base (pb).
- Si `fecha_corte` tiene más de un día hábil de antigüedad, el dato está viejo: dilo antes de usarlo.

## Resumen

- Valor del portafolio: $10,905,121.25
- Caja: $45,862.56 (0.42% del portafolio)

| | Día (mié 11-nov) | Semana (desde vie 6-nov) | Desde el día 0 | Desde el día 0 con la penalización de 30 pb |
|---|---:|---:|---:|---:|
| Cartera | +0.34% | +1.93% | +5.26% | +4.96% |
| MEXTRAC09 | +0.46% | +1.83% | +8.60% | +8.60% |
| Alfa | -12.72 pb | +9.75 pb | -334.62 pb | -364.62 pb |

## Cumplimiento

| Regla | Valor | Límite | Estado |
|---|---:|---|---|
| Beta ex ante | 0.91 | 0.70 a 1.30 | OK |
| Tracking error ex ante, anual | 5.93% | máximo 10% | OK |
| Caja | 0.42% | 0% a 5% | OK |
| Desviación máxima por emisora (FEMSAUBD) | 7.81 pp | ±10 pp | OK |

Tracking error realizado desde el día 0, anual: 7.81% (informativo).

## Alertas

- Stop-loss de BBAJIOO: Vigilar (-2.41 σ de TE, -0.65 σ propias).
- Stop-loss de GMEXICOB: Vigilar (-2.35 σ de TE, -1.02 σ propias).
- Stop-loss de PEOLES: Vigilar (-2.62 σ de TE, -1.41 σ propias).
- Precio de último hecho, no Price Close, el mié 21-oct: MEXTRAC.
- Precio de último hecho, no Price Close, el mié 11-nov: CUERVO.
- Caja negativa (sobregiro) en 4 cierres, del mié 21-oct al lun 26-oct. Ya está corregida.

## Posiciones

| Emisora | Títulos | Precio | Valor | Peso | Peso en el benchmark | Peso activo | Rendimiento del día | Rendimiento desde el día 0 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| MEXTRAC09 | 38,326 | $73.85 | $2,830,375.10 | 25.95% | es el benchmark | +0.00 pp | +0.46% | +8.60% |
| FEMSAUBD | 6,921 | $246.29 | $1,704,573.09 | 15.63% | 10.56% | +7.81 pp | -0.26% | +5.39% |
| GMEXICOB | 5,301 | $222.88 | $1,181,486.88 | 10.83% | 8.36% | +4.64 pp | +0.19% | -8.81% |
| KOFUBL | 3,638 | $225.01 | $818,586.38 | 7.51% | 8.08% | +1.52 pp | +0.80% | +2.54% |
| BOLSAA | 16,440 | $38.27 | $629,158.80 | 5.77% | 0.00% | +5.77 pp | +0.34% | +2.44% |
| GAPB | 1,372 | $445.50 | $611,226.00 | 5.60% | 10.83% | -2.41 pp | -0.79% | +23.82% |
| AMXB | 22,894 | $24.05 | $550,600.70 | 5.05% | 10.56% | -2.77 pp | +1.25% | +14.88% |
| GFNORTEO | 2,430 | $212.96 | $517,492.80 | 4.75% | 9.19% | -2.06 pp | +1.50% | +3.87% |
| PINFRA | 1,233 | $306.44 | $377,840.52 | 3.46% | 0.60% | +3.02 pp | +0.64% | +3.45% |
| AC | 1,469 | $237.69 | $349,166.61 | 3.20% | 7.65% | -2.46 pp | +0.69% | +14.32% |
| WALMEX | 6,439 | $53.78 | $346,289.42 | 3.18% | 7.51% | -2.38 pp | -1.45% | +9.26% |
| BBAJIOO | 5,399 | $55.93 | $301,966.07 | 2.77% | 1.66% | +1.54 pp | +0.94% | -3.32% |
| MEGACPO | 3,980 | $59.80 | $238,004.00 | 2.18% | 0.62% | +1.73 pp | +0.64% | +5.28% |
| ASURB | 427 | $506.05 | $216,083.35 | 1.98% | 6.03% | -2.49 pp | +1.61% | +14.26% |
| PEOLES | 181 | $786.07 | $142,278.67 | 1.30% | 0.00% | +1.30 pp | -0.55% | -12.61% |
| OMAB | 170 | $259.59 | $44,130.30 | 0.40% | 4.02% | -2.57 pp | +1.47% | +22.52% |
| Efectivo | | | $45,862.56 | 0.42% | 0.00% | | | |

Peso = posición directa al cierre. Peso activo = peso con el MEXTRAC09 abierto en sus emisoras menos el peso en el benchmark. El rendimiento desde el día 0 es el del precio de la emisora, aunque se haya comprado después.

## Quién hizo el alfa

- Hoy sumaron: WALMEX +4.63 pb, GAPB +3.06 pb, TLEVISACPO +2.29 pb. Restaron: FEMSAUBD -5.67 pb, ASURB -2.82 pb, OMAB -2.55 pb.
- Desde el día 0 sumaron: KIMBERA +18.29 pb, GFNORTEO +10.19 pb, TLEVISACPO +7.73 pb. Restaron: GMEXICOB -91.44 pb, BOLSAA -36.00 pb, GAPB -34.11 pb.

| Pieza | Hoy (mié 11-nov) | Desde el día 0 |
|---|---:|---:|
| Emisoras | -7.51 pb | -333.20 pb |
| Efectivo | -0.17 pb | -4.22 pb |
| MEXTRAC09 contra su canasta (o estimado) | -5.04 pb | +3.32 pb |
| Operaciones (ejecución contra cierre) | +0.00 pb | +0.76 pb |
| Comisión e IVA | +0.00 pb | -1.28 pb |
| Total = alfa | -12.72 pb | -334.62 pb |

Por sector (Brinson-Fachler). Asignación: por pesar distinto que el benchmark. Selección: por escoger mejores o peores acciones. Interacción: por cargar más justo donde se escogió mejor o peor. Los días se enlazan con Cariño.

| Sector | Asignación hoy | Selección hoy | Interacción hoy | Asignación desde el día 0 | Selección desde el día 0 | Interacción desde el día 0 |
|---|---:|---:|---:|---:|---:|---:|
| Consumo básico | +0.10 pb | -2.77 pb | +0.02 pb | +1.19 pb | -55.77 pb | -1.46 pb |
| Financieras | +2.64 pb | -5.27 pb | -1.12 pb | -11.86 pb | -32.07 pb | -6.34 pb |
| Industriales | +0.40 pb | -3.73 pb | +0.82 pb | -48.08 pb | -57.80 pb | +12.44 pb |
| Materiales | -2.39 pb | +1.03 pb | +0.52 pb | -88.28 pb | -21.26 pb | -10.76 pb |
| Servicios de comunicación | -0.67 pb | +1.24 pb | -0.16 pb | -5.76 pb | -8.59 pb | +0.92 pb |
| Inmobiliario | +1.82 pb | +0.00 pb | +0.00 pb | +0.29 pb | +0.00 pb | +0.00 pb |
| Efectivo | -0.17 pb | +0.00 pb | +0.00 pb | -4.22 pb | +0.00 pb | +0.00 pb |

## Operaciones de los últimos 5 días hábiles (desde el jue 5-nov)

| Fecha | Tipo | Emisora | Títulos | Precio | Comisión + IVA | Motivo |
|---|---|---|---:|---:|---:|---|
| vie 6-nov | Dividendo | GAPB | 1,372 | $20.80 | $0.00 | Dividendo en efectivo |
| mié 11-nov | Dividendo | AMXB | 22,894 | $0.27 | $0.00 | Dividendo en efectivo |

## Próximos eventos y dividendos (14 días)

- mar 17-nov · WALMEX · Dividendo de $0.5800 por acción. Fecha ex: mar 17-nov. Pago: mié 18-nov. Nos toca $3,734.62 por 6,439 títulos (estimado).

Para cobrar un dividendo hay que tener los títulos al cierre del día hábil anterior a la fecha ex. Solo se listan emisoras en cartera.

## Macro del mié 11-nov: lo que más se movió

| Serie | Valor | Cambio del día | Cambio en σ de 60 días | Mueve a |
|---|---:|---:|---:|---|
| S&P 500 (EUA) | 7,619.3800 | +1.31% | +1.4 σ |  |
| Euro en pesos | 20.6100 | -0.83% | -1.3 σ |  |
| Bono M a 10 años (rendimiento %) | 9.2060 | +5 pb | +1.0 σ | GFNORTEO, BBAJIOO, GFINBURO |
| Oro (dólares por onza) | 3,987.2900 | -1.08% | -0.7 σ | PEOLES |
| Cobre (dólares por libra) | 6.2625 | +0.76% | +0.5 σ | GMEXICOB |

Las divisas van en pesos por unidad. La macro es contexto de la sesión, no causa demostrada.

## Titulares de la sesión

- mié 11-nov 15:07 · Reuters · MERCADO: Peso mexicano se estabiliza en torno a 18.60/dlr, bolsa toca nuevo récord máximo
- mié 11-nov 08:41 · CENAFT · MEGACPO: From Grupo México to Megacable: Seven Companies on the BMV Set Their Sights on Acquisitions
- mié 11-nov 14:00 · Reuters · EUA: México afirma que las medidas restrictivas contra las importaciones de acero asiático están dando sus frutos a medida que avanzan las negociaciones sobre aranceles con EEUU
- mié 11-nov 13:24 · Reuters · EUA: Migrants trek north through Mexico, buoyed by US election result
- mié 11-nov 09:12 · Reuters · MERCADO: MERCADOS A.LATINA-Monedas operan mixtas en medio de nueva alza del dólar a nivel global

## Supuestos

- r_caja = 0%: no se sabe si BBVA invierte la caja en un fondo de liquidez.
- Fin de la gestión: vie 27-nov-2026 (por confirmar con BBVA).
- Comisión de 0.30% por operación más 16% de IVA sobre la comisión.
- Penalización de los profesores: 30 pb sobre el rendimiento final.
- Mandato: caja de 0% a 5%, tracking error máximo de 10%, beta de 0.70 a 1.30 y desviación máxima por emisora de ±10 pp.
