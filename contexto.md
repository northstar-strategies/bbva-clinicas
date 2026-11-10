---
fecha_corte: 2026-11-10
hora_publicacion: 2026-11-10 15:30 CDMX
fuente_precios: último hecho en AC, ALPEKA, ALSEA, AMXB, ASURB, BBAJIOO, BIMBOA, BOLSAA, CEMEXCPO, CHDRAUIB, CUERVO, FEMSAUBD, GAPB, GCARSOA1, GCC, GENTERA, GFINBURO, GFNORTEO, GMEXICOB, GRUMAB, IPC, KIMBERA, KOFUBL, LABB, LACOMERUBC, LIVEPOLC1, MEGACPO, MEXTRAC, OMAB, ORBIA, PEOLES, PINFRA, Q, RA, SIGMAFA, TLEVISACPO, VESTA, VOLARA, WALMEX; Price Close en el resto
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

- Valor del portafolio: $10,875,905.85
- Caja: $45,862.56 (0.42% del portafolio)

| | Día (mar 10-nov) | Semana (desde vie 6-nov) | Desde el día 0 | Desde el día 0 con la penalización de 30 pb |
|---|---:|---:|---:|---:|
| Cartera | +0.95% | +1.66% | +4.97% | +4.67% |
| MEXTRAC09 | +0.81% | +1.37% | +8.10% | +8.10% |
| Alfa | +14.25 pb | +29.32 pb | -312.82 pb | -342.82 pb |

## Cumplimiento

| Regla | Valor | Límite | Estado |
|---|---:|---|---|
| Beta ex ante | 0.91 | 0.70 a 1.30 | OK |
| Tracking error ex ante, anual | 5.93% | máximo 10% | OK |
| Caja | 0.42% | 0% a 5% | OK |
| Desviación máxima por emisora (FEMSAUBD) | 7.84 pp | ±10 pp | OK |

Tracking error realizado desde el día 0, anual: 8.01% (informativo).

## Alertas

- Stop-loss de BBAJIOO: Vigilar (-2.58 σ de TE, -0.87 σ propias).
- Stop-loss de PEOLES: Vigilar (-2.58 σ de TE, -1.40 σ propias).
- Stop-loss de GMEXICOB: Vigilar (-2.40 σ de TE, -1.09 σ propias).
- Precio de último hecho, no Price Close, el mié 21-oct: MEXTRAC.
- Precio de último hecho, no Price Close, el mar 10-nov: AC, ALPEKA, ALSEA, AMXB, ASURB, BBAJIOO, BIMBOA, BOLSAA, CEMEXCPO, CHDRAUIB, CUERVO, FEMSAUBD, GAPB, GCARSOA1, GCC, GENTERA, GFINBURO, GFNORTEO, GMEXICOB, GRUMAB, IPC, KIMBERA, KOFUBL, LABB, LACOMERUBC, LIVEPOLC1, MEGACPO, MEXTRAC, OMAB, ORBIA, PEOLES, PINFRA, Q, RA, SIGMAFA, TLEVISACPO, VESTA, VOLARA, WALMEX.
- Caja negativa (sobregiro) en 4 cierres, del mié 21-oct al lun 26-oct. Ya está corregida.

## Posiciones

| Emisora | Títulos | Precio | Valor | Peso | Peso en el benchmark | Peso activo | Rendimiento del día | Rendimiento desde el día 0 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| MEXTRAC09 | 38,326 | $73.51 | $2,817,344.26 | 25.90% | es el benchmark | +0.00 pp | +0.81% | +8.10% |
| FEMSAUBD | 6,921 | $246.81 | $1,708,172.01 | 15.71% | 10.61% | +7.84 pp | +1.85% | +5.61% |
| GMEXICOB | 5,301 | $222.11 | $1,177,405.11 | 10.83% | 8.35% | +4.64 pp | -0.65% | -9.12% |
| KOFUBL | 3,638 | $223.03 | $811,383.14 | 7.46% | 8.03% | +1.51 pp | +2.58% | +1.64% |
| BOLSAA | 16,440 | $38.24 | $628,665.60 | 5.78% | 0.00% | +5.78 pp | +1.59% | +2.36% |
| GAPB | 1,372 | $449.07 | $616,124.04 | 5.67% | 10.94% | -2.44 pp | +2.79% | +24.77% |
| AMXB | 22,894 | $24.00 | $549,456.00 | 5.05% | 10.57% | -2.78 pp | +0.41% | +14.64% |
| GFNORTEO | 2,430 | $210.49 | $511,490.70 | 4.70% | 9.11% | -2.04 pp | +0.56% | +2.67% |
| PINFRA | 1,233 | $304.92 | $375,966.36 | 3.46% | 0.60% | +3.01 pp | +1.07% | +2.94% |
| WALMEX | 6,439 | $54.45 | $350,603.55 | 3.22% | 7.62% | -2.42 pp | -0.26% | +10.63% |
| AC | 1,469 | $236.74 | $347,771.06 | 3.20% | 7.63% | -2.46 pp | +1.91% | +13.87% |
| BBAJIOO | 5,399 | $55.38 | $298,996.62 | 2.75% | 1.64% | +1.53 pp | -0.81% | -4.27% |
| MEGACPO | 3,980 | $59.48 | $236,730.40 | 2.18% | 0.61% | +1.72 pp | +0.02% | +4.72% |
| ASURB | 427 | $499.84 | $213,431.68 | 1.96% | 5.97% | -2.46 pp | +1.14% | +12.86% |
| PEOLES | 181 | $789.96 | $142,982.76 | 1.31% | 0.00% | +1.31 pp | -3.64% | -12.18% |
| OMAB | 170 | $256.00 | $43,520.00 | 0.40% | 3.98% | -2.55 pp | +0.61% | +20.83% |
| Efectivo | | | $45,862.56 | 0.42% | 0.00% | | | |

Peso = posición directa al cierre. Peso activo = peso con el MEXTRAC09 abierto en sus emisoras menos el peso en el benchmark. El rendimiento desde el día 0 es el del precio de la emisora, aunque se haya comprado después.

## Quién hizo el alfa

- Hoy sumaron: FEMSAUBD +8.10 pb, BOLSAA +4.51 pb, KIMBERA +3.98 pb. Restaron: GMEXICOB -6.91 pb, PEOLES -6.13 pb, GAPB -4.74 pb.
- Desde el día 0 sumaron: KIMBERA +18.86 pb, GFNORTEO +11.73 pb, GENTERA +6.23 pb. Restaron: GMEXICOB -90.49 pb, GAPB -37.36 pb, BOLSAA -33.53 pb.

| Pieza | Hoy (mar 10-nov) | Desde el día 0 |
|---|---:|---:|
| Emisoras | +4.17 pb | -329.07 pb |
| Efectivo | -0.30 pb | -4.09 pb |
| MEXTRAC09 contra su canasta (o estimado) | +10.38 pb | +20.85 pb |
| Operaciones (ejecución contra cierre) | +0.00 pb | +0.76 pb |
| Comisión e IVA | +0.00 pb | -1.27 pb |
| Total = alfa | +14.25 pb | -312.82 pb |

Por sector (Brinson-Fachler). Asignación: por pesar distinto que el benchmark. Selección: por escoger mejores o peores acciones. Interacción: por cargar más justo donde se escogió mejor o peor. Los días se enlazan con Cariño.

| Sector | Asignación hoy | Selección hoy | Interacción hoy | Asignación desde el día 0 | Selección desde el día 0 | Interacción desde el día 0 |
|---|---:|---:|---:|---:|---:|---:|
| Consumo básico | -0.20 pb | +13.30 pb | -0.12 pb | +1.10 pb | -53.85 pb | -1.44 pb |
| Financieras | -1.42 pb | +4.38 pb | +0.92 pb | -13.80 pb | -26.89 pb | -5.23 pb |
| Industriales | -5.20 pb | +0.27 pb | -0.06 pb | -49.08 pb | -53.78 pb | +11.54 pb |
| Materiales | -8.87 pb | -0.31 pb | -0.16 pb | -86.20 pb | -22.20 pb | -11.24 pb |
| Servicios de comunicación | +0.63 pb | -0.79 pb | +0.10 pb | -6.52 pb | -11.38 pb | +1.28 pb |
| Inmobiliario | +1.71 pb | +0.00 pb | +0.00 pb | -1.38 pb | +0.00 pb | +0.00 pb |
| Efectivo | -0.30 pb | +0.00 pb | +0.00 pb | -4.09 pb | +0.00 pb | +0.00 pb |

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
