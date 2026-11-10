---
fecha_corte: 2026-11-10
hora_publicacion: 2026-11-10 17:10 CDMX
fuente_precios: último hecho en VOLARA; Price Close en el resto
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

- Valor del portafolio: $10,868,676.27
- Caja: $39,681.18 (0.37% del portafolio)

| | Día (mar 10-nov) | Semana (desde vie 6-nov) | Desde el día 0 | Desde el día 0 con la penalización de 30 pb |
|---|---:|---:|---:|---:|
| Cartera | +0.88% | +1.59% | +4.90% | +4.60% |
| MEXTRAC09 | +0.81% | +1.37% | +8.10% | +8.10% |
| Alfa | +7.54 pb | +22.57 pb | -319.80 pb | -349.80 pb |

## Cumplimiento

| Regla | Valor | Límite | Estado |
|---|---:|---|---|
| Beta ex ante | 0.91 | 0.70 a 1.30 | OK |
| Tracking error ex ante, anual | 5.94% | máximo 10% | OK |
| Caja | 0.37% | 0% a 5% | OK |
| Desviación máxima por emisora (FEMSAUBD) | 7.86 pp | ±10 pp | OK |

Tracking error realizado desde el día 0, anual: 8.07% (informativo).

## Alertas

- Stop-loss de BBAJIOO: Vigilar (-2.57 σ de TE, -0.86 σ propias).
- Stop-loss de PEOLES: Vigilar (-2.58 σ de TE, -1.40 σ propias).
- Stop-loss de GMEXICOB: Vigilar (-2.38 σ de TE, -1.07 σ propias).
- Precio de último hecho, no Price Close, el mié 21-oct: MEXTRAC.
- Precio de último hecho, no Price Close, el mar 10-nov: VOLARA.
- Caja negativa (sobregiro) en 4 cierres, del mié 21-oct al lun 26-oct. Ya está corregida.

## Posiciones

| Emisora | Títulos | Precio | Valor | Peso | Peso en el benchmark | Peso activo | Rendimiento del día | Rendimiento desde el día 0 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| MEXTRAC09 | 38,326 | $73.51 | $2,817,344.26 | 25.92% | es el benchmark | +0.00 pp | +0.81% | +8.10% |
| FEMSAUBD | 6,921 | $246.93 | $1,709,002.53 | 15.72% | 10.62% | +7.86 pp | +1.90% | +5.66% |
| GMEXICOB | 5,301 | $222.46 | $1,179,260.46 | 10.85% | 8.37% | +4.65 pp | -0.50% | -8.98% |
| KOFUBL | 3,638 | $223.22 | $812,074.36 | 7.47% | 8.04% | +1.51 pp | +2.67% | +1.73% |
| BOLSAA | 16,440 | $38.14 | $627,021.60 | 5.77% | 0.00% | +5.77 pp | +1.33% | +2.09% |
| GAPB | 1,372 | $449.05 | $616,096.60 | 5.67% | 10.95% | -2.44 pp | +2.79% | +24.76% |
| AMXB | 22,894 | $24.02 | $549,913.88 | 5.06% | 10.58% | -2.78 pp | -0.62% | +14.74% |
| GFNORTEO | 2,430 | $209.81 | $509,838.30 | 4.69% | 9.08% | -2.04 pp | +0.24% | +2.34% |
| PINFRA | 1,233 | $304.49 | $375,436.17 | 3.45% | 0.60% | +3.01 pp | +0.93% | +2.80% |
| WALMEX | 6,439 | $54.57 | $351,376.23 | 3.23% | 7.64% | -2.42 pp | -0.04% | +10.87% |
| AC | 1,469 | $236.05 | $346,757.45 | 3.19% | 7.61% | -2.45 pp | +1.61% | +13.54% |
| BBAJIOO | 5,399 | $55.41 | $299,158.59 | 2.75% | 1.65% | +1.53 pp | -0.75% | -4.22% |
| MEGACPO | 3,980 | $59.42 | $236,491.60 | 2.18% | 0.61% | +1.72 pp | -0.08% | +4.61% |
| ASURB | 427 | $498.03 | $212,658.81 | 1.96% | 5.95% | -2.45 pp | +0.77% | +12.45% |
| PEOLES | 181 | $790.45 | $143,071.45 | 1.32% | 0.00% | +1.32 pp | -3.58% | -12.12% |
| OMAB | 170 | $255.84 | $43,492.80 | 0.40% | 3.98% | -2.54 pp | +0.54% | +20.75% |
| Efectivo | | | $39,681.18 | 0.37% | 0.00% | | | |

Peso = posición directa al cierre. Peso activo = peso con el MEXTRAC09 abierto en sus emisoras menos el peso en el benchmark. El rendimiento desde el día 0 es el del precio de la emisora, aunque se haya comprado después.

## Quién hizo el alfa

- Hoy sumaron: FEMSAUBD +8.48 pb, AMXB +4.02 pb, KIMBERA +3.98 pb. Restaron: GMEXICOB -6.17 pb, PEOLES -6.05 pb, GAPB -4.73 pb.
- Desde el día 0 sumaron: KIMBERA +18.86 pb, GFNORTEO +12.39 pb, GENTERA +6.31 pb. Restaron: GMEXICOB -89.73 pb, GAPB -37.21 pb, BOLSAA -35.11 pb.

| Pieza | Hoy (mar 10-nov) | Desde el día 0 |
|---|---:|---:|
| Emisoras | +8.90 pb | -323.90 pb |
| Efectivo | -0.30 pb | -4.03 pb |
| MEXTRAC09 contra su canasta (o estimado) | +7.81 pb | +18.19 pb |
| Operaciones (ejecución contra cierre) | +0.00 pb | +0.76 pb |
| Comisión e IVA | +0.00 pb | -1.27 pb |
| Total = alfa | +16.41 pb | -310.26 pb |

Por sector (Brinson-Fachler). Asignación: por pesar distinto que el benchmark. Selección: por escoger mejores o peores acciones. Interacción: por cargar más justo donde se escogió mejor o peor. Los días se enlazan con Cariño.

| Sector | Asignación hoy | Selección hoy | Interacción hoy | Asignación desde el día 0 | Selección desde el día 0 | Interacción desde el día 0 |
|---|---:|---:|---:|---:|---:|---:|
| Consumo básico | -0.20 pb | +14.44 pb | -0.13 pb | +1.08 pb | -52.61 pb | -1.48 pb |
| Financieras | -2.20 pb | +4.88 pb | +1.02 pb | -14.62 pb | -26.35 pb | -5.13 pb |
| Industriales | -4.61 pb | +0.45 pb | -0.10 pb | -48.31 pb | -53.61 pb | +11.51 pb |
| Materiales | -8.09 pb | -0.39 pb | -0.20 pb | -85.40 pb | -22.27 pb | -11.27 pb |
| Servicios de comunicación | +2.02 pb | +0.63 pb | -0.08 pb | -5.02 pb | -9.88 pb | +1.08 pb |
| Inmobiliario | +1.45 pb | +0.00 pb | +0.00 pb | -1.64 pb | +0.00 pb | +0.00 pb |
| Efectivo | -0.30 pb | +0.00 pb | +0.00 pb | -4.03 pb | +0.00 pb | +0.00 pb |

## Operaciones de los últimos 5 días hábiles (desde el mié 4-nov)

| Fecha | Tipo | Emisora | Títulos | Precio | Comisión + IVA | Motivo |
|---|---|---|---:|---:|---:|---|
| vie 6-nov | Dividendo | GAPB | 1,372 | $20.80 | $0.00 | Dividendo en efectivo |

## Próximos eventos y dividendos (14 días)

- mar 10-nov · AMXB · Dividendo de $0.2700 por acción. Fecha ex: mar 10-nov. Pago: mié 11-nov. Nos toca $6,181.38 por 22,894 títulos (estimado).
- mar 17-nov · WALMEX · Dividendo de $0.5800 por acción. Fecha ex: mar 17-nov. Pago: mié 18-nov. Nos toca $3,734.62 por 6,439 títulos (estimado).

Para cobrar un dividendo hay que tener los títulos al cierre del día hábil anterior a la fecha ex. Solo se listan emisoras en cartera.

## Macro del mar 10-nov: lo que más se movió

| Serie | Valor | Cambio del día | Cambio en σ de 60 días | Mueve a |
|---|---:|---:|---:|---|
| Peso chileno en pesos (×1,000) | 18.9226 | -1.24% | -1.8 σ |  |
| Oro (dólares por onza) | 4,030.9300 | -2.61% | -1.7 σ | PEOLES |
| Bono M a 10 años (rendimiento %) | 9.1570 | +7 pb | +1.5 σ | GFNORTEO, BBAJIOO, GFINBURO |
| Plata (dólares por onza) | 51.5052 | -3.57% | -1.4 σ | PEOLES |
| Cobre (dólares por libra) | 6.2155 | -1.86% | -1.3 σ | GMEXICOB |

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
