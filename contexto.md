---
fecha_corte: 2026-11-13
hora_publicacion: 2026-11-17 16:39 CDMX
fuente_precios: Price Close
version: v7.0
dias_habiles_desde_dia0: 19
tablero: https://northstar-strategies.github.io/bbva-clinicas/
---

# North Star Strategies · estado del fondo al vie 13-nov-2026

## Cómo leer este archivo

- North Star Strategies es un fondo de acciones mexicanas del programa ITESM-BBVA. Su benchmark es el MEXTRAC09, el ETF que replica el S&P/BMV IPC CompMX Rentable ESG Tilted TR.
- El día 0 es el cierre del vie 16-oct-2026. Nada anterior cuenta como rendimiento ni como alfa.
- Las cifras salen del tracker de Excel, replicado en Python y cuadrado a diferencia 0. Alfa = rendimiento de la cartera menos el del MEXTRAC09, en puntos base (pb).
- Si `fecha_corte` tiene más de un día hábil de antigüedad, el dato está viejo: dilo antes de usarlo.

## Resumen

- Valor del portafolio: $10,815,603.85
- Caja: $14,597.98 (0.13% del portafolio)

| | Día (vie 13-nov) | Semana (desde vie 6-nov) | Desde el día 0 | Desde el día 0 con la penalización de 30 pb |
|---|---:|---:|---:|---:|
| Cartera | -0.51% | +1.09% | +4.39% | +4.09% |
| MEXTRAC09 | -0.54% | +0.90% | +7.60% | +7.60% |
| Alfa | +3.73 pb | +19.84 pb | -321.02 pb | -351.02 pb |

## Cumplimiento

| Regla | Valor | Límite | Estado |
|---|---:|---|---|
| Beta ex ante | 0.91 | 0.70 a 1.30 | OK |
| Tracking error ex ante, anual | 5.93% | máximo 10% | OK |
| Caja | 0.13% | 0% a 5% | OK |
| Desviación máxima por emisora (FEMSAUBD) | 7.78 pp | ±10 pp | OK |

Tracking error realizado desde el día 0, anual: 7.46% (informativo).

## Alertas

- Stop-loss de PEOLES: Vigilar (-2.68 σ de TE, -1.62 σ propias).
- Stop-loss de BBAJIOO: Vigilar (-2.20 σ de TE, -0.73 σ propias).
- Stop-loss de GMEXICOB: Vigilar (-2.22 σ de TE, -1.07 σ propias).
- Precio de último hecho, no Price Close, el mié 21-oct: MEXTRAC.
- Caja negativa (sobregiro) en 4 cierres, del mié 21-oct al lun 26-oct. Ya está corregida.

## Posiciones

| Emisora | Títulos | Precio | Valor | Peso | Peso en el benchmark | Peso activo | Rendimiento del día | Rendimiento desde el día 0 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| MEXTRAC09 | 38,326 | $73.17 | $2,804,313.42 | 25.93% | es el benchmark | +0.00 pp | -0.54% | +7.60% |
| FEMSAUBD | 6,921 | $243.73 | $1,686,855.33 | 15.60% | 10.56% | +7.78 pp | -0.04% | +4.29% |
| GMEXICOB | 5,301 | $220.49 | $1,168,817.49 | 10.81% | 8.35% | +4.62 pp | -1.13% | -9.78% |
| KOFUBL | 3,638 | $223.25 | $812,183.50 | 7.51% | 8.10% | +1.51 pp | +1.52% | +1.74% |
| BOLSAA | 16,440 | $38.64 | $635,241.60 | 5.87% | 0.00% | +5.87 pp | -0.18% | +3.43% |
| GAPB | 1,435 | $438.48 | $629,218.80 | 5.82% | 10.77% | -2.16 pp | -0.77% | +21.96% |
| AMXB | 23,149 | $23.56 | $545,390.44 | 5.04% | 10.45% | -2.70 pp | -0.84% | +12.56% |
| GFNORTEO | 2,430 | $205.54 | $499,462.20 | 4.62% | 8.96% | -2.02 pp | -3.33% | +0.25% |
| PINFRA | 1,233 | $309.95 | $382,168.35 | 3.53% | 0.61% | +3.08 pp | -0.06% | +4.64% |
| AC | 1,481 | $243.78 | $361,038.18 | 3.34% | 7.92% | -2.53 pp | +0.29% | +17.23% |
| WALMEX | 6,439 | $54.88 | $353,372.32 | 3.27% | 7.74% | -2.46 pp | +1.07% | +11.50% |
| BBAJIOO | 5,399 | $55.60 | $300,184.40 | 2.78% | 1.66% | +1.54 pp | -1.35% | -3.89% |
| MEGACPO | 3,980 | $58.87 | $234,302.60 | 2.17% | 0.61% | +1.71 pp | -2.40% | +3.64% |
| ASURB | 427 | $500.38 | $213,662.26 | 1.98% | 6.03% | -2.49 pp | -1.38% | +12.98% |
| PEOLES | 181 | $761.38 | $137,809.78 | 1.27% | 0.00% | +1.27 pp | -1.00% | -15.36% |
| OMAB | 170 | $252.90 | $42,993.00 | 0.40% | 3.96% | -2.53 pp | -0.55% | +19.37% |
| Efectivo | | | $14,597.98 | 0.13% | 0.00% | | | |

Peso = posición directa al cierre. Peso activo = peso con el MEXTRAC09 abierto en sus emisoras menos el peso en el benchmark. El rendimiento desde el día 0 es el del precio de la emisora, aunque se haya comprado después.

## Quién hizo el alfa

- Hoy sumaron: GFNORTEO +5.76 pb, FEMSAUBD +3.90 pb, KOFUBL +3.07 pb. Restaron: WALMEX -3.89 pb, MEGACPO -3.25 pb, GMEXICOB -2.75 pb.
- Desde el día 0 sumaron: KIMBERA +18.81 pb, GFNORTEO +15.74 pb, TLEVISACPO +8.25 pb. Restaron: GMEXICOB -91.40 pb, PEOLES -36.09 pb, GAPB -32.30 pb.

| Pieza | Hoy (vie 13-nov) | Desde el día 0 |
|---|---:|---:|
| Emisoras | +14.03 pb | -314.80 pb |
| Efectivo | +0.07 pb | -4.06 pb |
| MEXTRAC09 contra su canasta (o estimado) | -10.38 pb | -1.32 pb |
| Operaciones (ejecución contra cierre) | +0.00 pb | +0.52 pb |
| Comisión e IVA | +0.00 pb | -1.37 pb |
| Total = alfa | +3.73 pb | -321.02 pb |

Por sector (Brinson-Fachler). Asignación: por pesar distinto que el benchmark. Selección: por escoger mejores o peores acciones. Interacción: por cargar más justo donde se escogió mejor o peor. Los días se enlazan con Cariño.

| Sector | Asignación hoy | Selección hoy | Interacción hoy | Asignación desde el día 0 | Selección desde el día 0 | Interacción desde el día 0 |
|---|---:|---:|---:|---:|---:|---:|
| Consumo básico | -0.43 pb | +5.55 pb | -0.07 pb | +0.61 pb | -73.73 pb | -1.36 pb |
| Financieras | -6.40 pb | +12.48 pb | +2.67 pb | -17.83 pb | -9.85 pb | -1.64 pb |
| Industriales | +1.57 pb | +3.46 pb | -0.72 pb | -44.73 pb | -44.79 pb | +9.71 pb |
| Materiales | -2.08 pb | -1.25 pb | -0.64 pb | -88.56 pb | -22.59 pb | -11.44 pb |
| Servicios de comunicación | +0.50 pb | -3.47 pb | +0.42 pb | -4.01 pb | -7.34 pb | +0.75 pb |
| Inmobiliario | +2.46 pb | +0.00 pb | +0.00 pb | +1.98 pb | +0.00 pb | +0.00 pb |
| Efectivo | +0.07 pb | +0.00 pb | +0.00 pb | -4.06 pb | +0.00 pb | +0.00 pb |

## Operaciones de los últimos 5 días hábiles (desde el lun 9-nov)

| Fecha | Tipo | Emisora | Títulos | Precio | Comisión + IVA | Motivo |
|---|---|---|---:|---:|---:|---|
| mié 11-nov | Compra | AC | 12 | $238.73 | $9.96 | Reinversión del dividendo |
| mié 11-nov | Compra | GAPB | 18 | $449.07 | $28.13 | Reinversión del dividendo |
| mié 11-nov | Compra | GAPB | 14 | $449.07 | $21.88 | Reinversión del dividendo |
| mié 11-nov | Compra | GAPB | 31 | $449.07 | $48.44 | Reinversión del dividendo |
| mar 17-nov | Compra | AMXB | 255 | $23.79 | $21.11 | Reinversión del dividendo |
| mié 11-nov | Dividendo | AMXB | 22,894 | $0.27 | $0.00 | Dividendo en efectivo |

## Próximos eventos y dividendos (14 días)

- mar 17-nov · NVIDIA EUA · Evento: Nvidia reporta el 3T del año fiscal 2027 (después del cierre)
- mar 17-nov · WALMEX · Dividendo de $0.5800 por acción. Fecha ex: mar 17-nov. Pago: mié 18-nov. Nos toca $3,734.62 por 6,439 títulos (estimado).
- mié 18-nov · CHINA EUA GMEXICOB · Evento: Cumbre de líderes de APEC en Shenzhen (18 y 19-nov); Sheinbaum en China del 16 al 20-nov
- jue 19-nov · ANTHROPIC EUA NVIDIA · Evento: IPO de Anthropic en Nasdaq (ANT): precio el 18-nov y cotiza el 19-nov
- jue 19-nov · CHINA EUA · Evento: Bilateral Trump–Xi y primera trilateral Trump–Xi–Putin
- mar 24-nov · OMAB · Dividendo de $6.2803 por acción. Fecha ex: mar 24-nov. Pago: mié 25-nov. Nos toca $1,067.64 por 170 títulos (estimado).
- vie 27-nov · ASURB · Dividendo de $10.0000 por acción. Fecha ex: vie 27-nov. Pago: lun 30-nov. Nos toca $4,270.00 por 427 títulos (estimado).

Para cobrar un dividendo hay que tener los títulos al cierre del día hábil anterior a la fecha ex. Solo se listan emisoras en cartera.

## Macro del vie 13-nov: lo que más se movió

| Serie | Valor | Cambio del día | Cambio en σ de 60 días | Mueve a |
|---|---:|---:|---:|---|
| Cobre (dólares por libra) | 6.0595 | -2.03% | -1.4 σ | GMEXICOB |
| S&P/BMV IPC | 71,204.9800 | -0.84% | -1.1 σ |  |
| Plata (dólares por onza) | 48.7264 | -2.56% | -1.0 σ | PEOLES |
| Euro en pesos | 20.4211 | -0.62% | -1.0 σ |  |
| Bono de EUA a 10 años (rendimiento %) | 5.1530 | +5 pb | +0.9 σ | GFNORTEO, BBAJIOO, GFINBURO |

Las divisas van en pesos por unidad. La macro es contexto de la sesión, no causa demostrada.

## Titulares de la sesión

- vie 13-nov 09:20 · Reuters · MERCADO: Bolsa mexicana cae por segunda jornada tras alcanzar récord máximo
- vie 13-nov 09:58 · Reuters · MERCADO: MERCADOS EMERGENTES-Los mercados de divisas de Latinoamérica registran resultados dispares mientras los inversores evalúan la evolución de la situación regional y las perspectivas de las tasas de interés en EEUU
- vie 13-nov 08:19 · Reuters · EUA: ACTUALIZA 1-Secretario Tesoro EEUU se muestra optimista ante acuerdos comerciales con Canadá y México
- vie 13-nov 07:41 · Reuters · EUA: Secretario Tesoro EEUU, Bessent, se muestra optimista ante acuerdos comerciales con Canadá y México
- jue 12-nov 18:14 · EPOTIM · EUA: Nvidia CEO Resigns After Alleged Chinese Spy Affair; Trump Threatens Mexico Tariffs Over Migrant Caravan

## Supuestos

- r_caja = 0%: no se sabe si BBVA invierte la caja en un fondo de liquidez.
- Fin de la gestión: vie 27-nov-2026 (por confirmar con BBVA).
- Comisión de 0.30% por operación más 16% de IVA sobre la comisión.
- Penalización de los profesores: 30 pb sobre el rendimiento final.
- Mandato: caja de 0% a 5%, tracking error máximo de 10%, beta de 0.70 a 1.30 y desviación máxima por emisora de ±10 pp.
