---
fecha_corte: 2026-11-18
hora_publicacion: 2026-11-18 18:04 CDMX
fuente_precios: Price Close
version: v7.0
dias_habiles_desde_dia0: 21
tablero: https://northstar-strategies.github.io/bbva-clinicas/
---

**Aviso: la réplica en Python no está cuadrada a 0 contra esta versión del tracker. Las cifras del día son preliminares.**

# North Star Strategies · estado del fondo al mié 18-nov-2026

## Cómo leer este archivo

- North Star Strategies es un fondo de acciones mexicanas del programa ITESM-BBVA. Su benchmark es el MEXTRAC09, el ETF que replica el S&P/BMV IPC CompMX Rentable ESG Tilted TR.
- El día 0 es el cierre del vie 16-oct-2026. Nada anterior cuenta como rendimiento ni como alfa.
- Las cifras salen del tracker de Excel, replicado en Python y cuadrado a diferencia 0. Alfa = rendimiento de la cartera menos el del MEXTRAC09, en puntos base (pb).
- Si `fecha_corte` tiene más de un día hábil de antigüedad, el dato está viejo: dilo antes de usarlo.

## Resumen

- Valor del portafolio: $10,552,837.83
- Caja: $12,245.04 (0.12% del portafolio)

| | Día (mié 18-nov) | Semana (desde vie 13-nov) | Desde el día 0 | Desde el día 0 con la penalización de 30 pb |
|---|---:|---:|---:|---:|
| Cartera | -1.47% | -2.43% | +1.86% | +1.56% |
| MEXTRAC09 | -1.14% | -2.04% | +5.41% | +5.41% |
| Alfa | -32.13 pb | -39.32 pb | -355.53 pb | -385.53 pb |

## Cumplimiento

| Regla | Valor | Límite | Estado |
|---|---:|---|---|
| Beta ex ante | 0.90 | 0.70 a 1.30 | OK |
| Tracking error ex ante, anual | 5.87% | máximo 10% | OK |
| Caja | 0.12% | 0% a 5% | OK |
| Desviación máxima por emisora (FEMSAUBD) | 7.94 pp | ±10 pp | OK |

Tracking error realizado desde el día 0, anual: 7.11% (informativo).

## Alertas

- Stop-loss de BBAJIOO: Vigilar (-1.80 σ de TE, -0.79 σ propias).
- Stop-loss de PEOLES: Vigilar (-3.26 σ de TE, -2.41 σ propias).
- Stop-loss de GMEXICOB: Vigilar (-2.90 σ de TE, -1.92 σ propias).
- Precio de último hecho, no Price Close, el mié 21-oct: MEXTRAC.
- Caja negativa (sobregiro) en 4 cierres, del mié 21-oct al lun 26-oct. Ya está corregida.

## Posiciones

| Emisora | Títulos | Precio | Valor | Peso | Peso en el benchmark | Peso activo | Rendimiento del día | Rendimiento desde el día 0 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| MEXTRAC09 | 38,326 | $71.68 | $2,747,207.68 | 26.03% | es el benchmark | +0.00 pp | -1.14% | +5.41% |
| FEMSAUBD | 6,921 | $241.24 | $1,669,622.04 | 15.82% | 10.66% | +7.94 pp | -0.45% | +3.23% |
| GMEXICOB | 5,301 | $199.37 | $1,056,860.37 | 10.01% | 7.71% | +4.32 pp | -6.32% | -18.42% |
| KOFUBL | 3,638 | $224.85 | $818,004.30 | 7.75% | 8.32% | +1.59 pp | +1.06% | +2.47% |
| BOLSAA | 16,440 | $37.73 | $620,281.20 | 5.88% | 0.00% | +5.88 pp | -2.71% | +0.99% |
| GAPB | 1,435 | $430.24 | $617,394.40 | 5.85% | 10.78% | -2.12 pp | +0.38% | +19.77% |
| AMXB | 23,149 | $23.63 | $547,010.87 | 5.18% | 10.69% | -2.73 pp | -0.76% | +12.90% |
| GFNORTEO | 2,430 | $198.06 | $481,285.80 | 4.56% | 8.81% | -1.95 pp | -1.95% | -3.39% |
| PINFRA | 1,233 | $305.92 | $377,199.36 | 3.57% | 0.62% | +3.12 pp | -1.20% | +3.28% |
| WALMEX | 6,439 | $54.60 | $351,569.40 | 3.33% | 7.85% | -2.48 pp | +0.18% | +12.11% |
| AC | 1,481 | $235.53 | $348,819.93 | 3.31% | 7.81% | -2.47 pp | -1.86% | +13.29% |
| BBAJIOO | 5,399 | $55.28 | $298,456.72 | 2.83% | 1.69% | +1.58 pp | -0.91% | -4.44% |
| MEGACPO | 3,980 | $57.97 | $230,720.60 | 2.19% | 0.62% | +1.73 pp | -0.05% | +2.06% |
| ASURB | 427 | $493.23 | $210,609.21 | 2.00% | 6.06% | -2.49 pp | -0.66% | +11.37% |
| PEOLES | 181 | $684.31 | $123,860.11 | 1.17% | 0.00% | +1.17 pp | -8.13% | -23.92% |
| OMAB | 170 | $245.24 | $41,690.80 | 0.40% | 3.92% | -2.50 pp | -1.19% | +15.75% |
| Efectivo | | | $12,245.04 | 0.12% | 0.00% | | | |

Peso = posición directa al cierre. Peso activo = peso con el MEXTRAC09 abierto en sus emisoras menos el peso en el benchmark. El rendimiento desde el día 0 es el del precio de la emisora, aunque se haya comprado después.

## Quién hizo el alfa

- Hoy sumaron: FEMSAUBD +5.46 pb, KOFUBL +3.36 pb, MEGACPO +1.86 pb. Restaron: GMEXICOB -23.36 pb, BOLSAA -9.30 pb, PEOLES -8.80 pb.
- Desde el día 0 sumaron: GFNORTEO +18.81 pb, KIMBERA +10.71 pb, CEMEXCPO +8.02 pb. Restaron: GMEXICOB -126.31 pb, PEOLES -46.20 pb, GAPB -31.93 pb.

| Pieza | Hoy (mié 18-nov) | Desde el día 0 |
|---|---:|---:|
| Emisoras | -42.27 pb | -361.25 pb |
| Efectivo | +0.09 pb | -3.74 pb |
| MEXTRAC09 contra su canasta (o estimado) | +10.05 pb | +10.31 pb |
| Operaciones (ejecución contra cierre) | +0.00 pb | +0.52 pb |
| Comisión e IVA | +0.00 pb | -1.36 pb |
| Total = alfa | -32.13 pb | -355.53 pb |

Por sector (Brinson-Fachler). Asignación: por pesar distinto que el benchmark. Selección: por escoger mejores o peores acciones. Interacción: por cargar más justo donde se escogió mejor o peor. Los días se enlazan con Cariño.

| Sector | Asignación hoy | Selección hoy | Interacción hoy | Asignación desde el día 0 | Selección desde el día 0 | Interacción desde el día 0 |
|---|---:|---:|---:|---:|---:|---:|
| Consumo básico | -0.54 pb | +1.10 pb | -0.02 pb | -0.33 pb | -80.21 pb | -1.23 pb |
| Financieras | -2.20 pb | -2.60 pb | -0.61 pb | -20.85 pb | -2.40 pb | -0.01 pb |
| Industriales | -3.91 pb | -0.81 pb | +0.17 pb | -44.52 pb | -40.75 pb | +8.86 pb |
| Materiales | -21.14 pb | -7.62 pb | -3.88 pb | -122.66 pb | -27.75 pb | -14.08 pb |
| Servicios de comunicación | -0.67 pb | +1.13 pb | -0.14 pb | -7.52 pb | -12.11 pb | +1.35 pb |
| Inmobiliario | -0.53 pb | +0.00 pb | +0.00 pb | +2.95 pb | +0.00 pb | +0.00 pb |
| Efectivo | +0.09 pb | +0.00 pb | +0.00 pb | -3.74 pb | +0.00 pb | +0.00 pb |

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

| Serie | Valor | Cambio del día | Cambio en σ de 60 días | Mueve a |
|---|---:|---:|---:|---|
| Cobre (dólares por libra) | 5.6625 | -5.25% | -3.6 σ | GMEXICOB |
| Dólar en pesos | 18.8365 | +2.31% | +3.5 σ |  |
| Euro en pesos | 20.6693 | +2.08% | +3.2 σ |  |
| Sol peruano en pesos | 5.4896 | +1.76% | +2.8 σ |  |
| Peso argentino en pesos (×1,000) | 12.0824 | +1.85% | +2.6 σ |  |

Las divisas van en pesos por unidad. La macro es contexto de la sesión, no causa demostrada.

## Titulares de la sesión

- mié 18-nov 15:34 · Reuters · MERCADO: Peso mexicano encabeza pérdidas entre monedas globales por expectativas de una Fed más restrictiva
- mié 18-nov 08:37 · Reuters · MERCADO: Bolsa mexicana perfila cuarta jornada de pérdidas tras alcanzar récord máximo
- mié 18-nov 14:19 · Reuters · MERCADO: MERCADOS A.LATINA-Monedas y bolsas caen ante expectativas de alzas tasas Fed
- mié 18-nov 08:30 · Reuters · PEOLES: Mexicana Industrias Peñoles firma acuerdo de energía renovable a 20 años con Atlas Renewable Energy
- mié 18-nov 06:52 · Reuters · MERCADO: GLOBAL MARKETS -Stocks slip as investors mull Nvidia earnings; Anthropic IPO to test AI boom

## Supuestos

- r_caja = 0%: no se sabe si BBVA invierte la caja en un fondo de liquidez.
- Fin de la gestión: vie 27-nov-2026 (por confirmar con BBVA).
- Comisión de 0.30% por operación más 16% de IVA sobre la comisión.
- Penalización de los profesores: 30 pb sobre el rendimiento final.
- Mandato: caja de 0% a 5%, tracking error máximo de 10%, beta de 0.70 a 1.30 y desviación máxima por emisora de ±10 pp.
