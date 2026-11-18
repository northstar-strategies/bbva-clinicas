---
fecha_corte: 2026-11-17
hora_publicacion: 2026-11-18 09:55 CDMX
fuente_precios: Price Close
version: v7.0
dias_habiles_desde_dia0: 20
tablero: https://northstar-strategies.github.io/bbva-clinicas/
---

# North Star Strategies · estado del fondo al mar 17-nov-2026

## Cómo leer este archivo

- North Star Strategies es un fondo de acciones mexicanas del programa ITESM-BBVA. Su benchmark es el MEXTRAC09, el ETF que replica el S&P/BMV IPC CompMX Rentable ESG Tilted TR.
- El día 0 es el cierre del vie 16-oct-2026. Nada anterior cuenta como rendimiento ni como alfa.
- Las cifras salen del tracker de Excel, replicado en Python y cuadrado a diferencia 0. Alfa = rendimiento de la cartera menos el del MEXTRAC09, en puntos base (pb).
- Si `fecha_corte` tiene más de un día hábil de antigüedad, el dato está viejo: dilo antes de usarlo.

## Resumen

- Valor del portafolio: $10,709,840.53
- Caja: $8,510.42 (0.08% del portafolio)

| | Día (mar 17-nov) | Semana (desde vie 13-nov) | Desde el día 0 | Desde el día 0 con la penalización de 30 pb |
|---|---:|---:|---:|---:|
| Cartera | -0.98% | -0.98% | +3.37% | +3.07% |
| MEXTRAC09 | -0.90% | -0.90% | +6.63% | +6.63% |
| Alfa | -7.59 pb | -7.59 pb | -326.05 pb | -356.05 pb |

## Cumplimiento

| Regla | Valor | Límite | Estado |
|---|---:|---|---|
| Beta ex ante | 0.91 | 0.70 a 1.30 | OK |
| Tracking error ex ante, anual | 5.91% | máximo 10% | OK |
| Caja | 0.08% | 0% a 5% | OK |
| Desviación máxima por emisora (FEMSAUBD) | 7.89 pp | ±10 pp | OK |

Tracking error realizado desde el día 0, anual: 7.27% (informativo).

## Alertas

- Stop-loss de BBAJIOO: Vigilar (-1.90 σ de TE, -0.65 σ propias).
- Stop-loss de PEOLES: Vigilar (-2.71 σ de TE, -1.77 σ propias).
- Stop-loss de GMEXICOB: Vigilar (-2.43 σ de TE, -1.38 σ propias).
- Precio de último hecho, no Price Close, el mié 21-oct: MEXTRAC.
- Caja negativa (sobregiro) en 4 cierres, del mié 21-oct al lun 26-oct. Ya está corregida.

## Posiciones

| Emisora | Títulos | Precio | Valor | Peso | Peso en el benchmark | Peso activo | Rendimiento del día | Rendimiento desde el día 0 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| MEXTRAC09 | 38,326 | $72.51 | $2,779,018.26 | 25.94% | es el benchmark | +0.00 pp | -0.90% | +6.63% |
| FEMSAUBD | 6,921 | $242.32 | $1,677,096.72 | 15.65% | 10.61% | +7.89 pp | -0.58% | +3.69% |
| GMEXICOB | 5,301 | $212.83 | $1,128,211.83 | 10.53% | 7.84% | +4.38 pp | -3.47% | -12.92% |
| KOFUBL | 3,638 | $222.50 | $809,455.00 | 7.56% | 8.21% | +1.57 pp | -0.34% | +1.40% |
| BOLSAA | 16,440 | $38.78 | $637,543.20 | 5.95% | 0.00% | +5.87 pp | +0.36% | +3.80% |
| GAPB | 1,435 | $428.59 | $615,026.65 | 5.74% | 10.63% | -2.10 pp | -2.26% | +19.33% |
| AMXB | 23,149 | $23.81 | $551,177.69 | 5.14% | 10.70% | -2.73 pp | +1.06% | +13.75% |
| GFNORTEO | 2,430 | $202.00 | $490,860.00 | 4.58% | 8.89% | -1.97 pp | -1.72% | -1.47% |
| PINFRA | 1,233 | $309.62 | $381,761.46 | 3.56% | 0.63% | +3.15 pp | -0.11% | +4.53% |
| AC | 1,481 | $240.00 | $355,440.00 | 3.32% | 7.79% | -2.47 pp | -1.55% | +15.42% |
| WALMEX | 6,439 | $55.08 | $354,660.12 | 3.31% | 7.92% | -2.50 pp | +0.36% | +13.08% |
| BBAJIOO | 5,399 | $55.79 | $301,210.21 | 2.81% | 1.68% | +1.57 pp | +0.34% | -3.56% |
| MEGACPO | 3,980 | $58.00 | $230,840.00 | 2.15% | 0.61% | +1.73 pp | -1.48% | +2.11% |
| ASURB | 427 | $496.51 | $212,009.77 | 1.98% | 6.06% | -2.49 pp | -0.77% | +12.11% |
| PEOLES | 181 | $744.90 | $134,826.90 | 1.26% | 0.00% | +1.22 pp | -2.16% | -17.19% |
| OMAB | 170 | $248.19 | $42,192.30 | 0.39% | 3.91% | -2.50 pp | -1.86% | +17.14% |
| Efectivo | | | $8,510.42 | 0.08% | 0.00% | | | |

Peso = posición directa al cierre. Peso activo = peso con el MEXTRAC09 abierto en sus emisoras menos el peso en el benchmark. El rendimiento desde el día 0 es el del precio de la emisora, aunque se haya comprado después.

## Quién hizo el alfa

- Hoy sumaron: BOLSAA +7.43 pb, CEMEXCPO +3.57 pb, GAPB +2.92 pb. Restaron: GMEXICOB -11.88 pb, AMXB -5.41 pb, KIMBERA -4.99 pb.
- Desde el día 0 sumaron: GFNORTEO +17.35 pb, KIMBERA +13.35 pb, CEMEXCPO +8.64 pb. Restaron: GMEXICOB -103.13 pb, PEOLES -37.45 pb, GAPB -28.90 pb.

| Pieza | Hoy (mar 17-nov) | Desde el día 0 |
|---|---:|---:|
| Emisoras | -8.69 pb | -321.06 pb |
| Efectivo | +0.12 pb | -3.89 pb |
| MEXTRAC09 contra su canasta (o estimado) | +1.00 pb | -0.25 pb |
| Operaciones (ejecución contra cierre) | +0.00 pb | +0.52 pb |
| Comisión e IVA | -0.02 pb | -1.38 pb |
| Total = alfa | -7.59 pb | -326.05 pb |

Por sector (Brinson-Fachler). Asignación: por pesar distinto que el benchmark. Selección: por escoger mejores o peores acciones. Interacción: por cargar más justo donde se escogió mejor o peor. Los días se enlazan con Cariño.

| Sector | Asignación hoy | Selección hoy | Interacción hoy | Asignación desde el día 0 | Selección desde el día 0 | Interacción desde el día 0 |
|---|---:|---:|---:|---:|---:|---:|
| Consumo básico | -0.34 pb | -8.86 pb | +0.11 pb | +0.24 pb | -82.43 pb | -1.23 pb |
| Financieras | -1.06 pb | +9.52 pb | +2.14 pb | -18.79 pb | +0.33 pb | +0.64 pb |
| Industriales | +3.16 pb | +3.73 pb | -0.77 pb | -40.96 pb | -40.42 pb | +8.80 pb |
| Materiales | -13.28 pb | +2.23 pb | +1.13 pb | -101.79 pb | -20.01 pb | -10.13 pb |
| Servicios de comunicación | -2.76 pb | -5.85 pb | +0.73 pb | -6.90 pb | -13.47 pb | +1.52 pb |
| Inmobiliario | +1.50 pb | +0.00 pb | +0.00 pb | +3.55 pb | +0.00 pb | +0.00 pb |
| Efectivo | +0.12 pb | +0.00 pb | +0.00 pb | -3.89 pb | +0.00 pb | +0.00 pb |

## Operaciones de los últimos 5 días hábiles (desde el mar 10-nov)

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

- mar 17-nov · WALMEX · Dividendo de $0.5800 por acción. Fecha ex: mar 17-nov. Pago: mié 18-nov. Nos toca $3,734.62 por 6,439 títulos.
- mié 18-nov · CHINA EUA GMEXICOB · Evento: Cumbre de líderes de APEC en Shenzhen (18 y 19-nov); Sheinbaum en China del 16 al 20-nov
- jue 19-nov · ANTHROPIC EUA NVIDIA · Evento: IPO de Anthropic en Nasdaq (ANT): precio el 18-nov y cotiza el 19-nov
- jue 19-nov · CHINA EUA · Evento: Bilateral Trump–Xi y primera trilateral Trump–Xi–Putin
- mar 24-nov · OMAB · Dividendo de $6.2803 por acción. Fecha ex: mar 24-nov. Pago: mié 25-nov. Nos toca $1,067.64 por 170 títulos (estimado).
- vie 27-nov · ASURB · Dividendo de $10.0000 por acción. Fecha ex: vie 27-nov. Pago: lun 30-nov. Nos toca $4,270.00 por 427 títulos (estimado).

Para cobrar un dividendo hay que tener los títulos al cierre del día hábil anterior a la fecha ex. Solo se listan emisoras en cartera.

## Macro del mar 17-nov: lo que más se movió

| Serie | Valor | Cambio del día | Cambio en σ de 60 días | Mueve a |
|---|---:|---:|---:|---|
| S&P/BMV IPC | 70,388.9600 | -1.15% | -1.4 σ |  |
| Sol peruano en pesos | 5.3947 | -0.76% | -1.2 σ |  |
| S&P 500 (EUA) | 7,340.5300 | -1.03% | -1.1 σ |  |
| Peso argentino en pesos (×1,000) | 11.8634 | -0.71% | -1.0 σ |  |
| Euro en pesos | 20.2477 | -0.54% | -0.8 σ |  |

Las divisas van en pesos por unidad. La macro es contexto de la sesión, no causa demostrada.

## Titulares de la sesión

- mar 17-nov 15:25 · North Star · Nvidia 8-K, CBS, Reuters · NVIDIA: Nvidia le gana al consenso en su primer reporte sin Jensen Huang: ingresos de 115.8 mmd y guía de 130 mmd
- mar 17-nov 08:30 · North Star · S-1/A (SEC), Reuters, Bloomberg · ANTHROPIC: Anthropic fija su IPO en Nasdaq (ANT): rango de 70–78 USD, precio el 18-nov y cotiza el 19-nov
- mar 17-nov 15:14 · Reuters · MERCADO: Peso mexicano avanza atento a señales Fed, bolsa cae por tercera jornada
- mar 17-nov 09:34 · North Star · Bitácora · AMXB: North Star reinvierte el dividendo de América Móvil: compra de 255 AMXB a $23.79
- mar 17-nov 08:00 · North Star · Cancillería de China, Kremlin, Reuters, gob.mx · CHINA: Líderes en Shenzhen: APEC el 18 y 19-nov, Trump–Xi y trilateral con Putin el jueves; Sheinbaum en China

## Supuestos

- r_caja = 0%: no se sabe si BBVA invierte la caja en un fondo de liquidez.
- Fin de la gestión: vie 27-nov-2026 (por confirmar con BBVA).
- Comisión de 0.30% por operación más 16% de IVA sobre la comisión.
- Penalización de los profesores: 30 pb sobre el rendimiento final.
- Mandato: caja de 0% a 5%, tracking error máximo de 10%, beta de 0.70 a 1.30 y desviación máxima por emisora de ±10 pp.
