---
fecha_corte: 2026-11-10
hora_publicacion: 2026-11-10 15:22 CDMX
fuente_precios: Price Close
version: v7.0
dias_habiles_desde_dia0: 16
tablero: https://northstar-strategies.github.io/bbva-clinicas/
---

# North Star Strategies · estado del fondo al mar 10-nov-2026

## Cómo leer este archivo

- North Star Strategies es un fondo de acciones mexicanas del programa ITESM-BBVA. Su benchmark es el MEXTRAC09, el ETF que replica el S&P/BMV IPC CompMX Rentable ESG Tilted TR.
- El día 0 es el cierre del vie 16-oct-2026. Nada anterior cuenta como rendimiento ni como alfa.
- Las cifras salen del tracker de Excel, replicado en Python y cuadrado a diferencia 0. Alfa = rendimiento de la cartera menos el del MEXTRAC09, en puntos base (pb).
- Si `fecha_corte` tiene más de un día hábil de antigüedad, el dato está viejo: dilo antes de usarlo.

## Resumen

- Valor del portafolio: $10,782,920.74
- Caja: $45,862.56 (0.43% del portafolio)

| | Día (mar 10-nov) | Semana (desde vie 6-nov) | Desde el día 0 | Desde el día 0 con la penalización de 30 pb |
|---|---:|---:|---:|---:|
| Cartera | +0.09% | +0.79% | +4.08% | +3.78% |
| MEXTRAC09 | +0.12% | +0.67% | +7.36% | +7.36% |
| Alfa | -3.14 pb | +11.71 pb | -328.66 pb | -358.66 pb |

## Cumplimiento

| Regla | Valor | Límite | Estado |
|---|---:|---|---|
| Beta ex ante | 0.91 | 0.70 a 1.30 | OK |
| Tracking error ex ante, anual | 5.94% | máximo 10% | OK |
| Caja | 0.43% | 0% a 5% | OK |
| Desviación máxima por emisora (FEMSAUBD) | 7.78 pp | ±10 pp | OK |

Tracking error realizado desde el día 0, anual: 7.92% (informativo).

## Alertas

- Stop-loss de PEOLES: Vigilar (-2.07 σ de TE, -1.02 σ propias).
- Stop-loss de KOFUBL: Vigilar (-1.59 σ de TE, -0.15 σ propias).
- Stop-loss de BBAJIOO: Vigilar (-2.27 σ de TE, -0.71 σ propias).
- Stop-loss de GMEXICOB: Vigilar (-2.21 σ de TE, -1.02 σ propias).
- MEXTRAC estimado (el ETF no operó o repitió precio; se usó cierre anterior × (1 + canasta)): mar 10-nov.
- Precio de último hecho, no Price Close, el mié 21-oct: MEXTRAC.
- Caja negativa (sobregiro) en 4 cierres, del mié 21-oct al lun 26-oct. Ya está corregida.

## Posiciones

| Emisora | Títulos | Precio | Valor | Peso | Peso en el benchmark | Peso activo | Rendimiento del día | Rendimiento desde el día 0 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| MEXTRAC09 | 38,326 | $73.01 | $2,798,081.77 | 25.95% | es el benchmark | +0.00 pp | +0.12% | +7.36% |
| FEMSAUBD | 6,921 | $242.33 | $1,677,165.93 | 15.55% | 10.50% | +7.78 pp | +0.00% | +3.69% |
| GMEXICOB | 5,301 | $223.57 | $1,185,144.57 | 10.99% | 8.48% | +4.71 pp | +0.00% | -8.52% |
| KOFUBL | 3,638 | $217.42 | $790,973.96 | 7.34% | 7.90% | +1.49 pp | +0.00% | -0.92% |
| BOLSAA | 16,440 | $37.64 | $618,801.60 | 5.74% | 0.00% | +5.74 pp | +0.00% | +0.75% |
| GAPB | 1,372 | $436.86 | $599,371.92 | 5.56% | 10.73% | -2.39 pp | +0.00% | +21.53% |
| AMXB | 22,894 | $24.17 | $553,347.98 | 5.13% | 10.73% | -2.81 pp | +1.12% | +15.45% |
| GFNORTEO | 2,430 | $209.31 | $508,623.30 | 4.72% | 9.13% | -2.04 pp | +0.00% | +2.09% |
| PINFRA | 1,233 | $301.69 | $371,983.77 | 3.45% | 0.60% | +3.01 pp | +0.00% | +1.85% |
| WALMEX | 6,439 | $54.59 | $351,505.01 | 3.26% | 7.70% | -2.44 pp | +0.00% | +10.91% |
| AC | 1,469 | $232.31 | $341,263.39 | 3.16% | 7.55% | -2.43 pp | +0.00% | +11.76% |
| BBAJIOO | 5,399 | $55.83 | $301,426.17 | 2.80% | 1.67% | +1.56 pp | +0.00% | -3.49% |
| MEGACPO | 3,980 | $59.47 | $236,690.60 | 2.20% | 0.62% | +1.74 pp | +0.00% | +4.70% |
| ASURB | 427 | $494.23 | $211,036.21 | 1.96% | 5.96% | -2.45 pp | +0.00% | +11.59% |
| PEOLES | 181 | $819.80 | $148,383.80 | 1.38% | 0.00% | +1.38 pp | +0.00% | -8.86% |
| OMAB | 170 | $254.46 | $43,258.20 | 0.40% | 3.99% | -2.55 pp | +0.00% | +20.10% |
| Efectivo | | | $45,862.56 | 0.43% | 0.00% | | | |

Peso = posición directa al cierre. Peso activo = peso con el MEXTRAC09 abierto en sus emisoras menos el peso en el benchmark. El rendimiento desde el día 0 es el del precio de la emisora, aunque se haya comprado después.

## Quién hizo el alfa

- Hoy sumaron: OMAB +0.31 pb, ASURB +0.29 pb, WALMEX +0.29 pb. Restaron: AMXB -2.80 pb, FEMSAUBD -0.93 pb, BOLSAA -0.69 pb.
- Desde el día 0 sumaron: KIMBERA +14.78 pb, GFNORTEO +11.38 pb, GENTERA +5.97 pb. Restaron: GMEXICOB -83.16 pb, BOLSAA -38.72 pb, FEMSAUBD -31.95 pb.

| Pieza | Hoy (mar 10-nov) | Desde el día 0 |
|---|---:|---:|
| Emisoras | -3.10 pb | -334.17 pb |
| Efectivo | -0.04 pb | -3.79 pb |
| MEXTRAC09 contra su canasta (o estimado) | +0.00 pb | +9.81 pb |
| Operaciones (ejecución contra cierre) | +0.00 pb | +0.75 pb |
| Comisión e IVA | +0.00 pb | -1.26 pb |
| Total = alfa | -3.14 pb | -328.66 pb |

Por sector (Brinson-Fachler). Asignación: por pesar distinto que el benchmark. Selección: por escoger mejores o peores acciones. Interacción: por cargar más justo donde se escogió mejor o peor. Los días se enlazan con Cariño.

| Sector | Asignación hoy | Selección hoy | Interacción hoy | Asignación desde el día 0 | Selección desde el día 0 | Interacción desde el día 0 |
|---|---:|---:|---:|---:|---:|---:|
| Consumo básico | +0.04 pb | +0.00 pb | +0.00 pb | +1.35 pb | -67.37 pb | -1.30 pb |
| Financieras | -0.35 pb | +0.00 pb | +0.00 pb | -12.58 pb | -31.28 pb | -6.15 pb |
| Industriales | +0.58 pb | +0.00 pb | +0.00 pb | -42.64 pb | -53.65 pb | +11.52 pb |
| Materiales | -0.61 pb | +0.00 pb | +0.00 pb | -76.89 pb | -21.70 pb | -10.99 pb |
| Servicios de comunicación | -1.33 pb | -1.86 pb | +0.23 pb | -8.53 pb | -12.43 pb | +1.41 pb |
| Inmobiliario | +0.20 pb | +0.00 pb | +0.00 pb | -2.95 pb | +0.00 pb | +0.00 pb |
| Efectivo | -0.04 pb | +0.00 pb | +0.00 pb | -3.79 pb | +0.00 pb | +0.00 pb |

## Operaciones de los últimos 5 días hábiles (desde el mié 4-nov)

| Fecha | Tipo | Emisora | Títulos | Precio | Comisión + IVA | Motivo |
|---|---|---|---:|---:|---:|---|
| jue 5-nov | Dividendo | GAPB | 1,372 | $20.80 | $0.00 | Dividendo en efectivo |
| mar 10-nov | Dividendo | AMXB | 22,894 | $0.27 | $0.00 | Dividendo en efectivo |

## Próximos eventos y dividendos (14 días)

- mar 10-nov · AMXB · Dividendo de $0.2700 por acción. Fecha ex: mar 10-nov. Pago: mié 11-nov. Nos toca $6,181.38 por 22,894 títulos.
- mar 17-nov · WALMEX · Dividendo de $0.5800 por acción. Fecha ex: mar 17-nov. Pago: mié 18-nov. Nos toca $3,734.62 por 6,439 títulos (estimado).

Para cobrar un dividendo hay que tener los títulos al cierre del día hábil anterior a la fecha ex. Solo se listan emisoras en cartera.

## Macro del mar 10-nov: lo que más se movió

| Serie | Valor | Cambio del día | Cambio en σ de 60 días | Mueve a |
|---|---:|---:|---:|---|
| Oro (dólares por onza) | 4,030.9700 | -2.61% | -1.7 σ | PEOLES |
| Plata (dólares por onza) | 51.4926 | -3.59% | -1.4 σ | PEOLES |

Las divisas van en pesos por unidad. La macro es contexto de la sesión, no causa demostrada.

## Titulares de la sesión

- mar 10-nov 15:17 · Reuters · MERCADO: Peso mexicano retrocede tras datos de inflación EEUU, bolsa se mantiene cerca de su récord máximo
- mar 10-nov 09:07 · Reuters · MERCADO: MERCADOS A.LATINA-Retroceden tras IPC de EEUU que refuerza expectativas de alza de tasas de la Fed
- lun 9-nov 21:41 · CENAFT · BANXICO: BMV closes at all-time high following Volaris' 'takeoff'; Wall Street in the green due to AI
- lun 9-nov 16:27 · Reuters · MERCADO: GLOBAL MARKETS-Stocks jump as oil tumbles, Nvidia falls amid internal probe
- mar 10-nov 14:01 · Reuters · MERCADO: EMERGING MARKETS-Latam FX hits seven-month low as hot US inflation lifts dollar

## Supuestos

- r_caja = 0%: no se sabe si BBVA invierte la caja en un fondo de liquidez.
- Fin de la gestión: vie 27-nov-2026 (por confirmar con BBVA).
- Comisión de 0.30% por operación más 16% de IVA sobre la comisión.
- Penalización de los profesores: 30 pb sobre el rendimiento final.
- Mandato: caja de 0% a 5%, tracking error máximo de 10%, beta de 0.70 a 1.30 y desviación máxima por emisora de ±10 pp.
