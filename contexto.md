---
fecha_corte: 2026-11-20
hora_publicacion: 2026-11-20 22:08 CDMX
fuente_precios: último hecho en MEXTRAC; Price Close en el resto
version: v7.0
dias_habiles_desde_dia0: 23
tablero: https://northstar-strategies.github.io/bbva-clinicas/
---

# North Star Strategies · estado del fondo al vie 20-nov-2026

## Cómo leer este archivo

- North Star Strategies es un fondo de acciones mexicanas del programa ITESM-BBVA. Su benchmark es el MEXTRAC09, el ETF que replica el S&P/BMV IPC CompMX Rentable ESG Tilted TR.
- El día 0 es el cierre del vie 16-oct-2026. Nada anterior cuenta como rendimiento ni como alfa.
- Las cifras salen del tracker de Excel, replicado en Python y cuadrado a diferencia 0. Alfa = rendimiento de la cartera menos el del MEXTRAC09, en puntos base (pb).
- Si `fecha_corte` tiene más de un día hábil de antigüedad, el dato está viejo: dilo antes de usarlo.

## Resumen

- Valor del portafolio: $10,533,197.13
- Caja: $8,517.62 (0.08% del portafolio)

| | Día (vie 20-nov) | Semana (desde vie 13-nov) | Desde el día 0 | Desde el día 0 con la penalización de 30 pb |
|---|---:|---:|---:|---:|
| Cartera | -0.13% | -2.56% | +1.73% | +1.43% |
| MEXTRAC09 | +0.26% | -1.59% | +5.90% | +5.90% |
| Alfa | -39.38 pb | -97.18 pb | -416.49 pb | -446.49 pb |

## Cumplimiento

| Regla | Valor | Límite | Estado |
|---|---:|---|---|
| Beta ex ante | 0.90 | 0.70 a 1.30 | OK |
| Tracking error ex ante, anual | 5.84% | máximo 10% | OK |
| Caja | 0.08% | 0% a 5% | OK |
| Desviación máxima por emisora (FEMSAUBD) | 8.02 pp | ±10 pp | OK |

Tracking error realizado desde el día 0, anual: 6.81% (informativo).

## Alertas

- Stop-loss de GMEXICOB: Vigilar (-3.11 σ de TE, -2.08 σ propias).
- Stop-loss de PEOLES: Vigilar (-3.67 σ de TE, -2.75 σ propias).
- Stop-loss de BBAJIOO: Vigilar (-2.13 σ de TE, -1.07 σ propias).
- Precio de último hecho, no Price Close, el mié 21-oct: MEXTRAC.
- Precio de último hecho, no Price Close, el jue 19-nov: MEXTRAC.
- Precio de último hecho, no Price Close, el vie 20-nov: MEXTRAC.
- Caja negativa (sobregiro) en 4 cierres, del mié 21-oct al lun 26-oct. Ya está corregida.

## Posiciones

| Emisora | Títulos | Precio | Valor | Peso | Peso en el benchmark | Peso activo | Rendimiento del día | Rendimiento desde el día 0 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| MEXTRAC09 | 38,326 | $72.01 | $2,759,855.26 | 26.20% | es el benchmark | +0.00 pp | +0.26% | +5.90% |
| FEMSAUBD | 6,921 | $241.94 | $1,674,466.74 | 15.90% | 10.69% | +8.02 pp | -0.71% | +3.53% |
| GMEXICOB | 5,301 | $192.25 | $1,019,117.25 | 9.68% | 7.43% | +4.20 pp | +1.34% | -20.52% |
| KOFUBL | 3,638 | $222.92 | $810,982.96 | 7.70% | 8.25% | +1.61 pp | -0.74% | +1.59% |
| BOLSAA | 16,440 | $37.45 | $615,678.00 | 5.85% | 0.00% | +5.85 pp | -0.74% | +0.24% |
| GAPB | 1,435 | $423.21 | $607,306.35 | 5.77% | 10.60% | -2.05 pp | -1.73% | +17.90% |
| AMXB | 23,149 | $23.87 | $552,566.63 | 5.25% | 10.80% | -2.72 pp | +0.76% | +14.03% |
| GFNORTEO | 2,430 | $196.45 | $477,373.50 | 4.53% | 8.73% | -1.91 pp | -1.43% | -4.18% |
| PINFRA | 1,243 | $311.49 | $387,182.07 | 3.68% | 0.63% | +3.21 pp | +0.85% | +6.00% |
| AC | 1,481 | $245.01 | $362,859.81 | 3.44% | 8.12% | -2.54 pp | +2.24% | +17.81% |
| WALMEX | 6,506 | $54.48 | $354,446.88 | 3.37% | 7.83% | -2.41 pp | -1.47% | +11.87% |
| BBAJIOO | 5,399 | $54.20 | $292,625.80 | 2.78% | 1.65% | +1.56 pp | -1.56% | -6.31% |
| MEGACPO | 3,980 | $56.30 | $224,074.00 | 2.13% | 0.60% | +1.69 pp | -1.19% | -0.88% |
| ASURB | 427 | $522.99 | $223,316.73 | 2.12% | 6.42% | -2.62 pp | +2.54% | +18.09% |
| PEOLES | 181 | $641.95 | $116,192.95 | 1.10% | 0.00% | +1.10 pp | -1.75% | -28.63% |
| OMAB | 170 | $243.42 | $41,381.40 | 0.39% | 3.89% | -2.47 pp | -1.18% | +14.89% |
| Efectivo | | | $8,517.62 | 0.08% | 0.00% | | | |

Peso = posición directa al cierre. Peso activo = peso con el MEXTRAC09 abierto en sus emisoras menos el peso en el benchmark. El rendimiento desde el día 0 es el del precio de la emisora, aunque se haya comprado después.

## Quién hizo el alfa

- Hoy sumaron: GMEXICOB +4.47 pb, WALMEX +4.25 pb, GAPB +4.20 pb. Restaron: FEMSAUBD -7.80 pb, BOLSAA -5.92 pb, ASURB -5.82 pb.
- Desde el día 0 sumaron: GFNORTEO +21.39 pb, KIMBERA +13.67 pb, CEMEXCPO +12.19 pb. Restaron: GMEXICOB -139.45 pb, PEOLES -54.39 pb, BOLSAA -32.90 pb.

| Pieza | Hoy (vie 20-nov) | Desde el día 0 |
|---|---:|---:|
| Emisoras | -15.78 pb | -394.91 pb |
| Efectivo | -0.02 pb | -3.80 pb |
| MEXTRAC09 contra su canasta (o estimado) | -23.59 pb | -16.93 pb |
| Operaciones (ejecución contra cierre) | +0.00 pb | +0.54 pb |
| Comisión e IVA | +0.00 pb | -1.39 pb |
| Total = alfa | -39.38 pb | -416.49 pb |

Por sector (Brinson-Fachler). Asignación: por pesar distinto que el benchmark. Selección: por escoger mejores o peores acciones. Interacción: por cargar más justo donde se escogió mejor o peor. Los días se enlazan con Cariño.

| Sector | Asignación hoy | Selección hoy | Interacción hoy | Asignación desde el día 0 | Selección desde el día 0 | Interacción desde el día 0 |
|---|---:|---:|---:|---:|---:|---:|
| Consumo básico | +0.06 pb | -12.45 pb | +0.06 pb | -0.39 pb | -84.67 pb | -1.27 pb |
| Financieras | -4.37 pb | -0.74 pb | -0.18 pb | -25.34 pb | -4.24 pb | -0.45 pb |
| Industriales | +2.27 pb | +0.78 pb | -0.16 pb | -47.08 pb | -41.08 pb | +8.91 pb |
| Materiales | +3.51 pb | -0.39 pb | -0.20 pb | -137.25 pb | -29.46 pb | -14.94 pb |
| Servicios de comunicación | -0.46 pb | -3.31 pb | +0.40 pb | -7.68 pb | -18.30 pb | +2.09 pb |
| Inmobiliario | -0.60 pb | +0.00 pb | +0.00 pb | +6.25 pb | +0.00 pb | +0.00 pb |
| Efectivo | -0.02 pb | +0.00 pb | +0.00 pb | -3.80 pb | +0.00 pb | +0.00 pb |

## Operaciones de los últimos 5 días hábiles (desde el vie 13-nov)

| Fecha | Tipo | Emisora | Títulos | Precio | Comisión + IVA | Motivo |
|---|---|---|---:|---:|---:|---|
| mar 17-nov | Compra | AMXB | 255 | $23.79 | $21.11 | Reinversión del dividendo |
| jue 19-nov | Compra | WALMEX | 67 | $55.02 | $12.83 | Reinversión del dividendo |
| jue 19-nov | Compra | PINFRA | 7 | $309.00 | $7.53 | Reinversión del dividendo |
| jue 19-nov | Compra | PINFRA | 3 | $309.00 | $3.22 | Reinversión del dividendo |
| mié 18-nov | Dividendo | PINFRA | 1,233 | $2.49 | $0.00 | Dividendo en efectivo |
| mié 18-nov | Dividendo | WALMEX | 6,439 | $0.58 | $0.00 | Dividendo en efectivo |

## Próximos eventos y dividendos (14 días)

- mar 24-nov · OMAB · Dividendo de $6.2803 por acción. Fecha ex: mar 24-nov. Pago: mié 25-nov. Nos toca $1,067.64 por 170 títulos (estimado).
- vie 27-nov · ASURB · Dividendo de $10.0000 por acción. Fecha ex: vie 27-nov. Pago: lun 30-nov. Nos toca $4,270.00 por 427 títulos (estimado).

Para cobrar un dividendo hay que tener los títulos al cierre del día hábil anterior a la fecha ex. Solo se listan emisoras en cartera.

## Macro del vie 20-nov: lo que más se movió

| Serie | Valor | Cambio del día | Cambio en σ de 60 días | Mueve a |
|---|---:|---:|---:|---|
| Cobre (dólares por libra) | 5.4610 | -2.87% | -1.8 σ | GMEXICOB |
| Peso colombiano en pesos (×1,000) | 5.4961 | -1.53% | -1.7 σ |  |
| Peso argentino en pesos (×1,000) | 12.1209 | -0.59% | -0.8 σ |  |
| Euro en pesos | 20.9963 | +0.38% | +0.5 σ |  |
| Dólar en pesos | 19.1450 | +0.37% | +0.5 σ |  |

Las divisas van en pesos por unidad. La macro es contexto de la sesión, no causa demostrada.

## Titulares de la sesión

- vie 20-nov 09:00 · North Star · Bloomberg Línea (Instagram) · PEOLES: El oro cae por debajo de 3,590 USD y va a su peor semana desde marzo (−7%)
- vie 20-nov 05:05 · North Star · FinanceFeeds (Kitco, MeltValue) · PEOLES: La plata cae a 42.38 USD, 64% abajo de su máximo de enero, junto con las bolsas
- vie 20-nov 15:16 · Reuters · AMXB: ACTUALIZA 2-ACTUALIZACIÓN 1-Los operadores de telefonía móvil mexicanos se enfrentan a cortes generalizados, según informan los usuarios
- vie 20-nov 09:55 · Reuters · COLOMBIA: Déficit fiscal de Colombia superará 7,6% del PIB en 2026: Ministro de Hacienda
- vie 20-nov 15:38 · Reuters · MERCADO: MERCADOS EMERGENTES-Los activos de Latinoamérica, afectados por el clima de aversión al riesgo a nivel mundial; las materias primas agravan las pérdidas

## Supuestos

- r_caja = 0%: no se sabe si BBVA invierte la caja en un fondo de liquidez.
- Fin de la gestión: vie 27-nov-2026 (por confirmar con BBVA).
- Comisión de 0.30% por operación más 16% de IVA sobre la comisión.
- Penalización de los profesores: 30 pb sobre el rendimiento final.
- Mandato: caja de 0% a 5%, tracking error máximo de 10%, beta de 0.70 a 1.30 y desviación máxima por emisora de ±10 pp.
