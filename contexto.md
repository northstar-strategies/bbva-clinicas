---
fecha_corte: 2026-11-12
hora_publicacion: 2026-11-13 11:51 CDMX
fuente_precios: Price Close
version: v7.0
dias_habiles_desde_dia0: 18
tablero: https://northstar-strategies.github.io/bbva-clinicas/
---

# North Star Strategies · estado del fondo al jue 12-nov-2026

## Cómo leer este archivo

- North Star Strategies es un fondo de acciones mexicanas del programa ITESM-BBVA. Su benchmark es el MEXTRAC09, el ETF que replica el S&P/BMV IPC CompMX Rentable ESG Tilted TR.
- El día 0 es el cierre del vie 16-oct-2026. Nada anterior cuenta como rendimiento ni como alfa.
- Las cifras salen del tracker de Excel, replicado en Python y cuadrado a diferencia 0. Alfa = rendimiento de la cartera menos el del MEXTRAC09, en puntos base (pb).
- Si `fecha_corte` tiene más de un día hábil de antigüedad, el dato está viejo: dilo antes de usarlo.

## Resumen

- Valor del portafolio: $10,870,656.31
- Caja: $14,597.98 (0.13% del portafolio)

| | Día (jue 12-nov) | Semana (desde vie 6-nov) | Desde el día 0 | Desde el día 0 con la penalización de 30 pb |
|---|---:|---:|---:|---:|
| Cartera | -0.31% | +1.61% | +4.92% | +4.62% |
| MEXTRAC09 | -0.38% | +1.45% | +8.19% | +8.19% |
| Alfa | +6.63 pb | +16.14 pb | -326.71 pb | -356.71 pb |

## Cumplimiento

| Regla | Valor | Límite | Estado |
|---|---:|---|---|
| Beta ex ante | 0.91 | 0.70 a 1.30 | OK |
| Tracking error ex ante, anual | 5.92% | máximo 10% | OK |
| Caja | 0.13% | 0% a 5% | OK |
| Desviación máxima por emisora (FEMSAUBD) | 7.78 pp | ±10 pp | OK |

Tracking error realizado desde el día 0, anual: 7.64% (informativo).

## Alertas

- Stop-loss de GMEXICOB: Vigilar (-2.22 σ de TE, -0.98 σ propias).
- Stop-loss de BBAJIOO: Vigilar (-2.12 σ de TE, -0.49 σ propias).
- Stop-loss de PEOLES: Vigilar (-2.73 σ de TE, -1.58 σ propias).
- Precio de último hecho, no Price Close, el mié 21-oct: MEXTRAC.
- Caja negativa (sobregiro) en 4 cierres, del mié 21-oct al lun 26-oct. Ya está corregida.

## Posiciones

| Emisora | Títulos | Precio | Valor | Peso | Peso en el benchmark | Peso activo | Rendimiento del día | Rendimiento desde el día 0 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| MEXTRAC09 | 38,326 | $73.57 | $2,819,643.82 | 25.94% | es el benchmark | +0.00 pp | -0.38% | +8.19% |
| FEMSAUBD | 6,921 | $243.83 | $1,687,547.43 | 15.52% | 10.56% | +7.78 pp | -1.00% | +4.33% |
| GMEXICOB | 5,301 | $223.02 | $1,182,229.02 | 10.88% | 8.30% | +4.59 pp | +0.06% | -8.75% |
| KOFUBL | 3,638 | $219.91 | $800,032.58 | 7.36% | 8.10% | +1.51 pp | -2.27% | +0.22% |
| BOLSAA | 16,440 | $38.71 | $636,392.40 | 5.85% | 0.00% | +5.90 pp | +1.15% | +3.61% |
| GAPB | 1,435 | $441.88 | $634,097.80 | 5.83% | 10.72% | -2.14 pp | -0.81% | +22.86% |
| AMXB | 22,894 | $23.76 | $543,961.44 | 5.00% | 10.45% | -2.75 pp | -1.21% | +13.51% |
| GFNORTEO | 2,430 | $212.63 | $516,690.90 | 4.75% | 9.09% | -2.04 pp | -0.15% | +3.71% |
| PINFRA | 1,233 | $310.13 | $382,390.29 | 3.52% | 0.62% | +3.08 pp | +1.20% | +4.70% |
| AC | 1,481 | $243.07 | $359,986.67 | 3.31% | 7.86% | -2.51 pp | +2.26% | +16.89% |
| WALMEX | 6,439 | $54.30 | $349,637.70 | 3.22% | 7.76% | -2.47 pp | +0.97% | +10.32% |
| BBAJIOO | 5,399 | $56.36 | $304,287.64 | 2.80% | 1.67% | +1.55 pp | +0.77% | -2.58% |
| MEGACPO | 3,980 | $60.32 | $240,073.60 | 2.21% | 0.62% | +1.73 pp | +0.87% | +6.20% |
| ASURB | 427 | $507.40 | $216,659.80 | 1.99% | 6.01% | -2.48 pp | +0.27% | +14.57% |
| PEOLES | 181 | $769.04 | $139,196.24 | 1.28% | 0.00% | +1.24 pp | -2.17% | -14.50% |
| OMAB | 170 | $254.30 | $43,231.00 | 0.40% | 3.94% | -2.52 pp | -2.04% | +20.03% |
| Efectivo | | | $14,597.98 | 0.13% | 0.00% | | | |

Peso = posición directa al cierre. Peso activo = peso con el MEXTRAC09 abierto en sus emisoras menos el peso en el benchmark. El rendimiento desde el día 0 es el del precio de la emisora, aunque se haya comprado después.

## Quién hizo el alfa

- Hoy sumaron: BOLSAA +8.82 pb, PINFRA +4.78 pb, OMAB +4.27 pb. Restaron: AC -6.43 pb, FEMSAUBD -4.84 pb, WALMEX -3.21 pb.
- Desde el día 0 sumaron: KIMBERA +16.62 pb, GFNORTEO +9.66 pb, TLEVISACPO +8.42 pb. Restaron: GMEXICOB -88.93 pb, PEOLES -35.66 pb, FEMSAUBD -33.46 pb.

| Pieza | Hoy (jue 12-nov) | Desde el día 0 |
|---|---:|---:|
| Emisoras | +0.51 pb | -331.50 pb |
| Efectivo | +0.05 pb | -4.16 pb |
| MEXTRAC09 contra su canasta (o estimado) | +6.07 pb | +9.80 pb |
| Operaciones (ejecución contra cierre) | +0.00 pb | +0.53 pb |
| Comisión e IVA | +0.00 pb | -1.38 pb |
| Total = alfa | +6.63 pb | -326.71 pb |

Por sector (Brinson-Fachler). Asignación: por pesar distinto que el benchmark. Selección: por escoger mejores o peores acciones. Interacción: por cargar más justo donde se escogió mejor o peor. Los días se enlazan con Cariño.

| Sector | Asignación hoy | Selección hoy | Interacción hoy | Asignación desde el día 0 | Selección desde el día 0 | Interacción desde el día 0 |
|---|---:|---:|---:|---:|---:|---:|
| Consumo básico | -0.11 pb | -22.90 pb | +0.15 pb | +1.08 pb | -80.06 pb | -1.30 pb |
| Financieras | +0.71 pb | +8.13 pb | +1.68 pb | -11.06 pb | -23.26 pb | -4.52 pb |
| Industriales | +1.19 pb | +8.29 pb | -1.74 pb | -46.64 pb | -48.73 pb | +10.53 pb |
| Materiales | +1.11 pb | -0.17 pb | -0.09 pb | -86.79 pb | -21.37 pb | -10.81 pb |
| Servicios de comunicación | +1.10 pb | +4.58 pb | -0.57 pb | -4.56 pb | -3.66 pb | +0.31 pb |
| Inmobiliario | -0.87 pb | +0.00 pb | +0.00 pb | -0.64 pb | +0.00 pb | +0.00 pb |
| Efectivo | +0.05 pb | +0.00 pb | +0.00 pb | -4.16 pb | +0.00 pb | +0.00 pb |

## Operaciones de los últimos 5 días hábiles (desde el vie 6-nov)

| Fecha | Tipo | Emisora | Títulos | Precio | Comisión + IVA | Motivo |
|---|---|---|---:|---:|---:|---|
| mié 11-nov | Compra | AC | 12 | $238.73 | $9.96 | Reinversión del dividendo |
| mié 11-nov | Compra | GAPB | 18 | $449.07 | $28.13 | Reinversión del dividendo |
| mié 11-nov | Compra | GAPB | 14 | $449.07 | $21.88 | Reinversión del dividendo |
| mié 11-nov | Compra | GAPB | 31 | $449.07 | $48.44 | Reinversión del dividendo |
| vie 6-nov | Dividendo | GAPB | 1,372 | $20.80 | $0.00 | Dividendo en efectivo |
| mié 11-nov | Dividendo | AMXB | 22,894 | $0.27 | $0.00 | Dividendo en efectivo |

## Próximos eventos y dividendos (14 días)

- mar 17-nov · WALMEX · Dividendo de $0.5800 por acción. Fecha ex: mar 17-nov. Pago: mié 18-nov. Nos toca $3,734.62 por 6,439 títulos (estimado).
- mar 24-nov · OMAB · Dividendo de $6.2803 por acción. Fecha ex: mar 24-nov. Pago: mié 25-nov. Nos toca $1,067.64 por 170 títulos (estimado).

Para cobrar un dividendo hay que tener los títulos al cierre del día hábil anterior a la fecha ex. Solo se listan emisoras en cartera.

## Macro del jue 12-nov: lo que más se movió

| Serie | Valor | Cambio del día | Cambio en σ de 60 días | Mueve a |
|---|---:|---:|---:|---|
| Bono de EUA a 10 años (rendimiento %) | 5.1030 | +12 pb | +2.2 σ | GFNORTEO, BBAJIOO, GFINBURO |
| Oro (dólares por onza) | 3,876.3500 | -2.78% | -1.9 σ | PEOLES |
| Peso chileno en pesos (×1,000) | 18.6889 | -1.25% | -1.8 σ |  |
| Bono M a 10 años (rendimiento %) | 9.2780 | +7 pb | +1.5 σ | GFNORTEO, BBAJIOO, GFINBURO |
| Plata (dólares por onza) | 50.0063 | -3.25% | -1.3 σ | PEOLES |

Las divisas van en pesos por unidad. La macro es contexto de la sesión, no causa demostrada.

## Titulares de la sesión

- jue 12-nov 15:24 · Reuters · MERCADO: MERCADOS A.LATINA-Monedas retroceden en medio de fortaleza del dólar, expectativas de alza tasas Fed
- jue 12-nov 14:11 · Reuters · MERCADO: MERCADOS EMERGENTES-Los activos de Latinoamérica retroceden ante la volatilidad del petróleo y la fortaleza del dólar
- mié 11-nov 17:09 · Reuters · MERCADO: GLOBAL MARKETS-Stocks rise on tech gains; Nvidia falls after hours
- mié 11-nov 16:02 · Reuters · EUA: UPDATE 1-Mexico says crackdown on Asian steel shipments is paying off as US tariff talks advance
- jue 12-nov 11:05 · Reuters · BANXICO: EXCLUSIVA-Recorte tasa "confunde y refleja mensaje equivocado", dice subgobernador Heath de banco central México

## Supuestos

- r_caja = 0%: no se sabe si BBVA invierte la caja en un fondo de liquidez.
- Fin de la gestión: vie 27-nov-2026 (por confirmar con BBVA).
- Comisión de 0.30% por operación más 16% de IVA sobre la comisión.
- Penalización de los profesores: 30 pb sobre el rendimiento final.
- Mandato: caja de 0% a 5%, tracking error máximo de 10%, beta de 0.70 a 1.30 y desviación máxima por emisora de ±10 pp.
