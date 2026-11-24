---
fecha_corte: 2026-11-23
hora_publicacion: 2026-11-23 19:10 CDMX
fuente_precios: Price Close
version: v7.0
dias_habiles_desde_dia0: 24
tablero: https://northstar-strategies.github.io/bbva-clinicas/
---

# North Star Strategies · estado del fondo al lun 23-nov-2026

## Cómo leer este archivo

- North Star Strategies es un fondo de acciones mexicanas del programa ITESM-BBVA. Su benchmark es el MEXTRAC09, el ETF que replica el S&P/BMV IPC CompMX Rentable ESG Tilted TR.
- El día 0 es el cierre del vie 16-oct-2026. Nada anterior cuenta como rendimiento ni como alfa.
- Las cifras salen del tracker de Excel, replicado en Python y cuadrado a diferencia 0. Alfa = rendimiento de la cartera menos el del MEXTRAC09, en puntos base (pb).
- Si `fecha_corte` tiene más de un día hábil de antigüedad, el dato está viejo: dilo antes de usarlo.

## Resumen

- Valor del portafolio: $10,606,373.50
- Caja: $8,596.99 (0.08% del portafolio)

| | Día (lun 23-nov) | Semana (desde vie 20-nov) | Desde el día 0 | Desde el día 0 con la penalización de 30 pb |
|---|---:|---:|---:|---:|
| Cartera | +0.69% | +0.69% | +2.37% | +2.07% |
| MEXTRAC09 | +0.32% | +0.32% | +6.24% | +6.24% |
| Alfa | +37.53 pb | +37.53 pb | -386.21 pb | -416.21 pb |

## Cumplimiento

| Regla | Valor | Límite | Estado |
|---|---:|---|---|
| Beta ex ante | 0.91 | 0.70 a 1.30 | OK |
| Tracking error ex ante, anual | 5.87% | máximo 10% | OK |
| Caja | 0.08% | 0% a 5% | OK |
| Desviación máxima por emisora (FEMSAUBD) | 7.93 pp | ±10 pp | OK |

Tracking error realizado desde el día 0, anual: 6.94% (informativo).

## Alertas

- Stop-loss de GMEXICOB: Vigilar (-2.85 σ de TE, -1.83 σ propias).
- Stop-loss de PEOLES: Vigilar (-3.30 σ de TE, -2.40 σ propias).
- Stop-loss de BBAJIOO: Vigilar (-2.09 σ de TE, -1.00 σ propias).
- Precio de último hecho, no Price Close, el mié 21-oct: MEXTRAC.
- Caja negativa (sobregiro) en 4 cierres, del mié 21-oct al lun 26-oct. Ya está corregida.

## Posiciones

| Emisora | Títulos | Precio | Valor | Peso | Peso en el benchmark | Peso activo | Rendimiento del día | Rendimiento desde el día 0 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| MEXTRAC09 | 38,326 | $72.24 | $2,768,670.24 | 26.10% | es el benchmark | +0.00 pp | +0.32% | +6.24% |
| FEMSAUBD | 6,921 | $241.62 | $1,672,252.02 | 15.77% | 10.61% | +7.93 pp | -0.13% | +3.39% |
| GMEXICOB | 5,328 | $198.42 | $1,057,181.76 | 9.97% | 7.62% | +4.34 pp | +3.21% | -18.39% |
| KOFUBL | 3,638 | $224.17 | $815,530.46 | 7.69% | 8.25% | +1.60 pp | +0.56% | +2.16% |
| BOLSAA | 16,440 | $38.13 | $626,857.20 | 5.91% | 0.00% | +5.91 pp | +1.82% | +2.06% |
| GAPB | 1,435 | $424.83 | $609,631.05 | 5.75% | 10.57% | -2.06 pp | +0.38% | +18.33% |
| AMXB | 23,149 | $23.81 | $551,177.69 | 5.20% | 10.71% | -2.72 pp | -0.25% | +13.75% |
| GFNORTEO | 2,430 | $198.14 | $481,480.20 | 4.54% | 8.75% | -1.93 pp | +0.86% | -3.36% |
| PINFRA | 1,243 | $312.35 | $388,251.05 | 3.66% | 0.63% | +3.20 pp | +0.28% | +6.29% |
| AC | 1,481 | $245.47 | $363,541.07 | 3.43% | 8.08% | -2.55 pp | +0.19% | +18.03% |
| WALMEX | 6,506 | $54.66 | $355,617.96 | 3.35% | 7.81% | -2.42 pp | +0.33% | +12.23% |
| BBAJIOO | 5,399 | $54.35 | $293,435.65 | 2.77% | 1.65% | +1.55 pp | +0.28% | -6.05% |
| ASURB | 427 | $531.05 | $226,758.35 | 2.14% | 6.48% | -2.65 pp | +1.54% | +19.91% |
| MEGACPO | 3,980 | $56.21 | $223,715.80 | 2.11% | 0.59% | +1.67 pp | -0.16% | -1.04% |
| PEOLES | 181 | $670.11 | $121,289.91 | 1.14% | 0.00% | +1.14 pp | +4.39% | -25.50% |
| OMAB | 170 | $249.33 | $42,386.10 | 0.40% | 3.96% | -2.52 pp | +2.43% | +17.68% |
| Efectivo | | | $8,596.99 | 0.08% | 0.00% | | | |

Peso = posición directa al cierre. Peso activo = peso con el MEXTRAC09 abierto en sus emisoras menos el peso en el benchmark. El rendimiento desde el día 0 es el del precio de la emisora, aunque se haya comprado después.

## Quién hizo el alfa

- Hoy sumaron: GMEXICOB +12.26 pb, BOLSAA +8.75 pb, PEOLES +4.49 pb. Restaron: OMAB -5.22 pb, FEMSAUBD -3.62 pb, ASURB -3.20 pb.
- Desde el día 0 sumaron: GFNORTEO +20.44 pb, KIMBERA +14.49 pb, CEMEXCPO +9.60 pb. Restaron: GMEXICOB -130.22 pb, PEOLES -49.96 pb, ASURB -31.79 pb.

| Pieza | Hoy (lun 23-nov) | Desde el día 0 |
|---|---:|---:|
| Emisoras | +14.61 pb | -384.35 pb |
| Efectivo | -0.03 pb | -3.85 pb |
| MEXTRAC09 contra su canasta (o estimado) | +22.93 pb | +2.82 pb |
| Operaciones (ejecución contra cierre) | +0.01 pb | +0.55 pb |
| Comisión e IVA | +0.00 pb | -1.39 pb |
| Total = alfa | +37.53 pb | -386.21 pb |

Por sector (Brinson-Fachler). Asignación: por pesar distinto que el benchmark. Selección: por escoger mejores o peores acciones. Interacción: por cargar más justo donde se escogió mejor o peor. Los días se enlazan con Cariño.

| Sector | Asignación hoy | Selección hoy | Interacción hoy | Asignación desde el día 0 | Selección desde el día 0 | Interacción desde el día 0 |
|---|---:|---:|---:|---:|---:|---:|
| Consumo básico | +0.04 pb | -1.21 pb | +0.01 pb | -0.37 pb | -86.31 pb | -1.25 pb |
| Financieras | +1.30 pb | +4.63 pb | +1.10 pb | -24.11 pb | +0.59 pb | +0.69 pb |
| Industriales | -2.93 pb | -5.32 pb | +1.06 pb | -50.36 pb | -46.78 pb | +10.06 pb |
| Materiales | +12.68 pb | +1.01 pb | +0.51 pb | -127.32 pb | -28.70 pb | -14.55 pb |
| Servicios de comunicación | +0.98 pb | +1.13 pb | -0.14 pb | -6.71 pb | -17.21 pb | +1.96 pb |
| Inmobiliario | -0.26 pb | +0.00 pb | +0.00 pb | +6.02 pb | +0.00 pb | +0.00 pb |
| Efectivo | -0.03 pb | +0.00 pb | +0.00 pb | -3.85 pb | +0.00 pb | +0.00 pb |

## Operaciones de los últimos 5 días hábiles (desde el mar 17-nov)

| Fecha | Tipo | Emisora | Títulos | Precio | Comisión + IVA | Motivo |
|---|---|---|---:|---:|---:|---|
| mar 17-nov | Compra | AMXB | 255 | $23.79 | $21.11 | Reinversión del dividendo |
| jue 19-nov | Compra | WALMEX | 67 | $55.02 | $12.83 | Reinversión del dividendo |
| jue 19-nov | Compra | PINFRA | 7 | $309.00 | $7.53 | Reinversión del dividendo |
| jue 19-nov | Compra | PINFRA | 3 | $309.00 | $3.22 | Reinversión del dividendo |
| lun 23-nov | Dividendo en acciones | GMEXICOB | 27 | $0.00 | $0.00 | Dividendo en especie |
| mié 18-nov | Dividendo | PINFRA | 1,233 | $2.49 | $0.00 | Dividendo en efectivo |
| mié 18-nov | Dividendo | WALMEX | 6,439 | $0.58 | $0.00 | Dividendo en efectivo |
| lun 23-nov | Dividendo | GMEXICOB | 5,301 | $0.01 | $0.00 | Fracción del dividendo en acciones |

## Próximos eventos y dividendos (14 días)

- mar 24-nov · MERCADO BANXICO · Evento: Inflación de la primera quincena de noviembre (INEGI, 06:00)
- mar 24-nov · OMAB · Dividendo de $6.2803 por acción. Fecha ex: mar 24-nov. Pago: mié 25-nov. Nos toca $1,067.64 por 170 títulos (estimado).
- mar 24-nov · OMAB · Evento: Fecha ex del dividendo de OMAB ($6.2803 por acción, cupón 15); registro 24-nov, pago 25-nov
- mié 25-nov · FED EUA · Evento: EUA, 07:30: PIB del 3T (segunda), PCE de octubre, bienes duraderos y solicitudes de desempleo; Libro Beige en la tarde
- jue 26-nov · BANXICO · Evento: Informe trimestral del 3T de Banxico; desempleo de octubre (INEGI)
- jue 26-nov · EUA MEXTRAC · Evento: Acción de Gracias: NYSE cerrada el jueves; el viernes 27 cierra a las 12:00 CDMX
- vie 27-nov · ASURB · Dividendo de $10.0000 por acción. Fecha ex: vie 27-nov. Pago: lun 30-nov. Nos toca $4,270.00 por 427 títulos (estimado).
- vie 27-nov · ASURB · Evento: Fecha ex del primer dividendo extraordinario de ASUR ($10.00 por acción, cupón 23); pago desde el 30-nov
- vie 27-nov · MERCADO · Evento: Último día de la gestión (Parámetros: 27-nov, por confirmar con BBVA); balanza comercial de octubre
- lun 30-nov · MERCADO · Evento: Entra en vigor la revisión de noviembre de MSCI (al cierre)
- lun 7-dic · KOFUBL · Dividendo de $1.9350 por acción. Fecha ex: lun 7-dic. Pago: mar 8-dic. Nos toca $7,039.53 por 3,638 títulos (estimado).

Para cobrar un dividendo hay que tener los títulos al cierre del día hábil anterior a la fecha ex. Solo se listan emisoras en cartera.

## Macro del lun 23-nov: lo que más se movió

| Serie | Valor | Cambio del día | Cambio en σ de 60 días | Mueve a |
|---|---:|---:|---:|---|
| S&P 500 (EUA) | 7,237.1700 | +4.73% | +4.3 σ |  |
| Cobre (dólares por libra) | 5.6230 | +2.97% | +1.8 σ | GMEXICOB |
| Oro (dólares por onza) | 3,631.6800 | +2.81% | +1.8 σ | PEOLES |
| Plata (dólares por onza) | 43.0599 | +4.55% | +1.7 σ | PEOLES |
| Bono M a 10 años (rendimiento %) | 9.2800 | -7 pb | -1.4 σ | GFNORTEO, BBAJIOO, GFINBURO |

Las divisas van en pesos por unidad. La macro es contexto de la sesión, no causa demostrada.

## Titulares de la sesión

- lun 23-nov 10:00 · North Star · Kitco, Capp Notes · PEOLES: El oro rebota 2.8% a ~3,635 USD y la plata 4.6% a ~43 USD tras su peor semana desde marzo; el petróleo cae ~3.5%
- lun 23-nov 09:00 · North Star · Aviso de derechos BMV, Bitácora · GMEXICOB: Grupo México entrega su dividendo en acciones: recibimos 27 GMEXICOB y $79.37 por la fracción
- sáb 21-nov 12:00 · North Star · El Imparcial, N+ · AMXB: Profeco: Telcel debe bonificar a los usuarios afectados por la falla del 20-nov
- lun 23-nov 14:42 · Reuters · MERCADO: MERCADOS A.LATINA-Monedas y bolsas cierran mixtas en sesión marcada por regreso de Huang a Nvidia
- lun 23-nov 15:50 · North Star · INEGI, Banxico, NYSE · MERCADO: Semana corta y último tramo de la gestión: inflación el martes, PCE el miércoles, Banxico el jueves y cierre el viernes 27

## Supuestos

- r_caja = 0%: no se sabe si BBVA invierte la caja en un fondo de liquidez.
- Fin de la gestión: vie 27-nov-2026 (por confirmar con BBVA).
- Comisión de 0.30% por operación más 16% de IVA sobre la comisión.
- Penalización de los profesores: 30 pb sobre el rendimiento final.
- Mandato: caja de 0% a 5%, tracking error máximo de 10%, beta de 0.70 a 1.30 y desviación máxima por emisora de ±10 pp.
