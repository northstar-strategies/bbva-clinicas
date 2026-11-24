---
fecha_corte: 2026-11-24
hora_publicacion: 2026-11-24 15:57 CDMX
fuente_precios: Price Close
version: v7.0
dias_habiles_desde_dia0: 25
tablero: https://northstar-strategies.github.io/bbva-clinicas/
---

# North Star Strategies · estado del fondo al mar 24-nov-2026

## Cómo leer este archivo

- North Star Strategies es un fondo de acciones mexicanas del programa ITESM-BBVA. Su benchmark es el MEXTRAC09, el ETF que replica el S&P/BMV IPC CompMX Rentable ESG Tilted TR.
- El día 0 es el cierre del vie 16-oct-2026. Nada anterior cuenta como rendimiento ni como alfa.
- Las cifras salen del tracker de Excel, replicado en Python y cuadrado a diferencia 0. Alfa = rendimiento de la cartera menos el del MEXTRAC09, en puntos base (pb).
- Si `fecha_corte` tiene más de un día hábil de antigüedad, el dato está viejo: dilo antes de usarlo.

## Resumen

- Valor del portafolio: $10,627,086.69
- Caja: $8,596.99 (0.08% del portafolio)

| | Día (mar 24-nov) | Semana (desde vie 20-nov) | Desde el día 0 | Desde el día 0 con la penalización de 30 pb |
|---|---:|---:|---:|---:|
| Cartera | +0.20% | +0.89% | +2.57% | +2.27% |
| MEXTRAC09 | +0.65% | +0.97% | +6.93% | +6.93% |
| Alfa | -45.53 pb | -8.07 pb | -435.33 pb | -465.33 pb |

## Cumplimiento

| Regla | Valor | Límite | Estado |
|---|---:|---|---|
| Beta ex ante | 0.91 | 0.70 a 1.30 | OK |
| Tracking error ex ante, anual | 5.76% | máximo 10% | OK |
| Caja | 0.08% | 0% a 5% | OK |
| Desviación máxima por emisora (FEMSAUBD) | 7.98 pp | ±10 pp | OK |

Tracking error realizado desde el día 0, anual: 6.86% (informativo).

## Alertas

- Stop-loss de BBAJIOO: Vigilar (-1.83 σ de TE, -0.65 σ propias).
- Stop-loss de PEOLES: Vigilar (-3.59 σ de TE, -2.61 σ propias).
- Stop-loss de GMEXICOB: Vigilar (-3.36 σ de TE, -2.22 σ propias).
- Precio de último hecho, no Price Close, el mié 21-oct: MEXTRAC.
- Caja negativa (sobregiro) en 4 cierres, del mié 21-oct al lun 26-oct. Ya está corregida.

## Posiciones

| Emisora | Títulos | Precio | Valor | Peso | Peso en el benchmark | Peso activo | Rendimiento del día | Rendimiento desde el día 0 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| MEXTRAC09 | 38,326 | $72.71 | $2,786,683.46 | 26.22% | es el benchmark | +0.00 pp | +0.65% | +6.93% |
| FEMSAUBD | 6,921 | $242.44 | $1,677,927.24 | 15.79% | 10.58% | +7.98 pp | +0.34% | +3.74% |
| GMEXICOB | 5,328 | $187.57 | $999,372.96 | 9.40% | 7.16% | +4.12 pp | -5.47% | -22.86% |
| KOFUBL | 3,638 | $228.03 | $829,573.14 | 7.81% | 8.34% | +1.66 pp | +1.72% | +3.92% |
| GAPB | 1,435 | $441.88 | $634,097.80 | 5.97% | 10.93% | -2.10 pp | +4.01% | +22.86% |
| BOLSAA | 16,440 | $37.94 | $623,733.60 | 5.87% | 0.00% | +5.87 pp | -0.50% | +1.55% |
| AMXB | 23,149 | $23.98 | $555,113.02 | 5.22% | 10.72% | -2.68 pp | +0.71% | +14.55% |
| GFNORTEO | 2,430 | $198.98 | $483,521.40 | 4.55% | 8.74% | -1.90 pp | +0.42% | -2.95% |
| PINFRA | 1,243 | $318.54 | $395,945.22 | 3.73% | 0.64% | +3.26 pp | +1.98% | +8.38% |
| AC | 1,481 | $249.10 | $368,917.10 | 3.47% | 8.15% | -2.54 pp | +1.48% | +19.77% |
| WALMEX | 6,506 | $53.61 | $348,786.66 | 3.28% | 7.61% | -2.33 pp | -1.92% | +10.10% |
| BBAJIOO | 5,399 | $55.52 | $299,752.48 | 2.82% | 1.67% | +1.59 pp | +2.15% | -4.03% |
| ASURB | 427 | $542.42 | $231,613.34 | 2.18% | 6.58% | -2.67 pp | +2.14% | +22.48% |
| MEGACPO | 3,980 | $56.24 | $223,835.20 | 2.11% | 0.59% | +1.67 pp | +0.05% | -0.99% |
| PEOLES | 181 | $644.98 | $116,741.38 | 1.10% | 0.00% | +1.10 pp | -3.75% | -28.30% |
| OMAB | 170 | $252.21 | $42,875.70 | 0.40% | 3.98% | -2.53 pp | +1.16% | +22.00% |
| Efectivo | | | $8,596.99 | 0.08% | 0.00% | | | |

Peso = posición directa al cierre. Peso activo = peso con el MEXTRAC09 abierto en sus emisoras menos el peso en el benchmark. El rendimiento desde el día 0 es el del precio de la emisora, aunque se haya comprado después.

## Quién hizo el alfa

- Hoy sumaron: WALMEX +6.22 pb, PINFRA +4.25 pb, BBAJIOO +2.33 pb. Restaron: GMEXICOB -26.53 pb, GAPB -6.94 pb, BOLSAA -6.79 pb.
- Desde el día 0 sumaron: GFNORTEO +20.98 pb, KIMBERA +13.79 pb, CEMEXCPO +10.24 pb. Restaron: GMEXICOB -158.45 pb, PEOLES -55.42 pb, ASURB -36.05 pb.

| Pieza | Hoy (mar 24-nov) | Desde el día 0 |
|---|---:|---:|
| Emisoras | -43.15 pb | -430.97 pb |
| Efectivo | -0.05 pb | -3.92 pb |
| MEXTRAC09 contra su canasta (o estimado) | -2.33 pb | +0.40 pb |
| Operaciones (ejecución contra cierre) | +0.00 pb | +0.55 pb |
| Comisión e IVA | +0.00 pb | -1.40 pb |
| Total = alfa | -45.53 pb | -435.33 pb |

Por sector (Brinson-Fachler). Asignación: por pesar distinto que el benchmark. Selección: por escoger mejores o peores acciones. Interacción: por cargar más justo donde se escogió mejor o peor. Los días se enlazan con Cariño.

| Sector | Asignación hoy | Selección hoy | Interacción hoy | Asignación desde el día 0 | Selección desde el día 0 | Interacción desde el día 0 |
|---|---:|---:|---:|---:|---:|---:|
| Consumo básico | +0.07 pb | +4.28 pb | -0.03 pb | -0.29 pb | -82.21 pb | -1.29 pb |
| Financieras | +1.01 pb | -6.25 pb | -1.51 pb | -23.17 pb | -5.93 pb | -0.87 pb |
| Industriales | -10.05 pb | +1.31 pb | -0.27 pb | -61.06 pb | -45.60 pb | +9.83 pb |
| Materiales | -24.11 pb | -4.57 pb | -2.32 pb | -153.01 pb | -33.59 pb | -17.04 pb |
| Servicios de comunicación | -0.05 pb | -1.33 pb | +0.16 pb | -6.79 pb | -18.67 pb | +2.14 pb |
| Inmobiliario | +0.50 pb | +0.00 pb | +0.00 pb | +6.56 pb | +0.00 pb | +0.00 pb |
| Efectivo | -0.05 pb | +0.00 pb | +0.00 pb | -3.92 pb | +0.00 pb | +0.00 pb |

## Operaciones de los últimos 5 días hábiles (desde el mié 18-nov)

| Fecha | Tipo | Emisora | Títulos | Precio | Comisión + IVA | Motivo |
|---|---|---|---:|---:|---:|---|
| jue 19-nov | Compra | WALMEX | 67 | $55.02 | $12.83 | Reinversión del dividendo |
| jue 19-nov | Compra | PINFRA | 7 | $309.00 | $7.53 | Reinversión del dividendo |
| jue 19-nov | Compra | PINFRA | 3 | $309.00 | $3.22 | Reinversión del dividendo |
| lun 23-nov | Dividendo en acciones | GMEXICOB | 27 | $0.00 | $0.00 | Dividendo en especie |
| mié 18-nov | Dividendo | PINFRA | 1,233 | $2.49 | $0.00 | Dividendo en efectivo |
| mié 18-nov | Dividendo | WALMEX | 6,439 | $0.58 | $0.00 | Dividendo en efectivo |
| lun 23-nov | Dividendo | GMEXICOB | 5,301 | $0.01 | $0.00 | Fracción del dividendo en acciones |

## Próximos eventos y dividendos (14 días)

- mar 24-nov · OMAB · Dividendo de $6.2803 por acción. Fecha ex: mar 24-nov. Pago: mié 25-nov. Nos toca $1,067.64 por 170 títulos (estimado).
- mié 25-nov · FED EUA · Evento: EUA, 07:30: PIB del 3T (segunda), PCE de octubre, bienes duraderos y solicitudes de desempleo; Libro Beige en la tarde
- jue 26-nov · BANXICO · Evento: Informe trimestral del 3T de Banxico; desempleo de octubre (INEGI)
- jue 26-nov · EUA MEXTRAC · Evento: Acción de Gracias: NYSE cerrada el jueves; el viernes 27 cierra a las 12:00 CDMX
- vie 27-nov · ASURB · Dividendo de $10.0000 por acción. Fecha ex: vie 27-nov. Pago: lun 30-nov. Nos toca $4,270.00 por 427 títulos (estimado).
- vie 27-nov · ASURB · Evento: Fecha ex del primer dividendo extraordinario de ASUR ($10.00 por acción, cupón 23); pago desde el 30-nov
- vie 27-nov · MERCADO · Evento: Último día de la gestión (Parámetros: 27-nov, por confirmar con BBVA); balanza comercial de octubre
- lun 30-nov · MERCADO · Evento: Entra en vigor la revisión de noviembre de MSCI (al cierre)
- lun 7-dic · KOFUBL · Dividendo de $1.9350 por acción. Fecha ex: lun 7-dic. Pago: mar 8-dic. Nos toca $7,039.53 por 3,638 títulos (estimado).
- mar 8-dic · WALMEX · Dividendo de $0.5800 por acción. Fecha ex: mar 8-dic. Pago: mié 9-dic. Nos toca $3,773.48 por 6,506 títulos (estimado).

Para cobrar un dividendo hay que tener los títulos al cierre del día hábil anterior a la fecha ex. Solo se listan emisoras en cartera.

## Macro del mar 24-nov: lo que más se movió

| Serie | Valor | Cambio del día | Cambio en σ de 60 días | Mueve a |
|---|---:|---:|---:|---|
| Plata (dólares por onza) | 40.7611 | -5.34% | -1.9 σ | PEOLES |
| Oro (dólares por onza) | 3,550.4900 | -2.24% | -1.4 σ | PEOLES |
| Bovespa (Brasil) | 164,089.8100 | -0.43% | -0.2 σ |  |
| S&P/BMV IPC | 69,301.4100 | -0.08% | -0.1 σ |  |

Las divisas van en pesos por unidad. La macro es contexto de la sesión, no causa demostrada.

## Titulares de la sesión

- mar 24-nov 15:21 · Reuters · MERCADO: Peso mexicano cierra con quinta caída al hilo, espera dato clave de inflación en EEUU
- mar 24-nov 10:51 · Reuters · BANXICO: SONDEO-Acciones brasileñas recuperarían parte de caída postelectoral en 2027, bolsa mexicana subiría
- lun 23-nov 16:25 · Reuters · MERCADO: GLOBAL MARKETS-Wall Street soars on Huang's return to Nvidia, Treasury yields rise
- mar 24-nov 09:14 · Reuters · MERCADO: MERCADOS A.LATINA-Mayoría de monedas caen pese a baja global del dólar, real brasileño se fortalece
- mar 24-nov 04:30 · Reuters · MERCADO: EMERGING MARKETS-EM stocks climb as Huang returns to Nvidia, but Europe muted

## Supuestos

- r_caja = 0%: no se sabe si BBVA invierte la caja en un fondo de liquidez.
- Fin de la gestión: vie 27-nov-2026 (por confirmar con BBVA).
- Comisión de 0.30% por operación más 16% de IVA sobre la comisión.
- Penalización de los profesores: 30 pb sobre el rendimiento final.
- Mandato: caja de 0% a 5%, tracking error máximo de 10%, beta de 0.70 a 1.30 y desviación máxima por emisora de ±10 pp.
