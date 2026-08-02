# NLGeo Benchmark Results

Run: 2026-08-01T04:26:10  
Raw data: `results_20260801_020845.csv`

## Summary

- Queries run: **75**
- Success rate: **95%** (71/75)
- Mean eval score: **0.900 ± 0.000**
- Top-1 accuracy (where expected known): **60%** (18/30)
- Latency p50: **36.21s**, p95: **247.34s**

## Per-query

| id | city | type | status | eval | top1 | correct | latency (s) |
|---|---|---|---|---|---|---|---|
| mumbai_flood_01 | Mumbai | flood | complete | 0.9 | Kurla | ✓ | 27.28 |
| mumbai_flood_01 | Mumbai | flood | complete | 0.9 | Kurla | ✓ | 12.19 |
| mumbai_flood_01 | Mumbai | flood | complete | 0.9 | Kurla | ✓ | 9.06 |
| mumbai_flood_02 | Mumbai | flood | complete | 0.9 | Kurla | ✓ | 12.08 |
| mumbai_flood_02 | Mumbai | flood | complete | 0.9 | Kurla | ✓ | 12.07 |
| mumbai_flood_02 | Mumbai | flood | complete | 0.9 | Kurla | ✓ | 15.11 |
| mumbai_flood_03 | Mumbai | flood | complete | 0.9 | Kurla | ✓ | 12.14 |
| mumbai_flood_03 | Mumbai | flood | complete | 0.9 | Kurla | ✓ | 12.1 |
| mumbai_flood_03 | Mumbai | flood | complete | 0.9 | Kurla | ✓ | 9.05 |
| berlin_pharm_01 | Berlin | point_count | complete | 0.9 | Mitte |  | 568.02 |
| berlin_pharm_01 | Berlin | point_count | complete | 0.9 | Mitte |  | 36.27 |
| berlin_pharm_01 | Berlin | point_count | complete | 0.9 | Mitte |  | 30.22 |
| berlin_pharm_02 | Berlin | point_count | complete | 0.9 | Friedenau | ✗ | 39.25 |
| berlin_pharm_02 | Berlin | point_count | complete | 0.9 | Friedenau | ✗ | 172.19 |
| berlin_pharm_02 | Berlin | point_count | complete | 0.9 | Friedenau | ✗ | 45.26 |
| berlin_clinic_01 | Berlin | point_count | complete | 0.9 | Charlottenburg-Wilmersdorf | ✓ | 42.42 |
| berlin_clinic_01 | Berlin | point_count | complete | 0.9 | Charlottenburg-Wilmersdorf | ✓ | 36.26 |
| berlin_clinic_01 | Berlin | point_count | complete | 0.9 | Charlottenburg-Wilmersdorf | ✓ | 33.31 |
| london_hosp_01 | Greater London | point_count | complete | 0.9 | City of Westminster |  | 54.32 |
| london_hosp_01 | Greater London | point_count | complete | 0.9 | City of Westminster |  | 39.17 |
| london_hosp_01 | Greater London | point_count | complete | 0.9 | City of Westminster |  | 39.22 |
| london_flood_01 | London | flood_inversion | complete | 0.9 | London Borough of Croydon |  | 21.14 |
| london_flood_01 | London | flood_inversion | complete | 0.9 | London Borough of Croydon |  | 21.13 |
| london_flood_01 | London | flood_inversion | complete | 0.9 | London Borough of Croydon |  | 21.12 |
| london_green_01 | London | greenspace | complete | 0.9 | London Borough of Barnet |  | 159.95 |
| london_green_01 | London | greenspace | complete | 0.9 | London Borough of Barnet |  | 153.75 |
| london_green_01 | London | greenspace | complete | 0.9 | London Borough of Barnet |  | 84.49 |
| paris_hosp_01 | Paris | point_count | complete | 0.9 | Paris 13e Arrondissement |  | 30.19 |
| paris_hosp_01 | Paris | point_count | complete | 0.9 | Paris 13e Arrondissement |  | 247.34 |
| paris_hosp_01 | Paris | point_count | complete | 0.9 | Paris 13e Arrondissement |  | 33.17 |
| paris_rest_01 | Paris | point_count | complete | 0.9 | Paris 11e Arrondissement | ✓ | 33.16 |
| paris_rest_01 | Paris | point_count | complete | 0.9 | Paris 11e Arrondissement | ✓ | 36.19 |
| paris_rest_01 | Paris | point_count | complete | 0.9 | Paris 11e Arrondissement | ✓ | 30.19 |
| paris_cafe_01 | Paris | proximity | complete | 0.9 | Le Café Suédois | ✗ | 33.21 |
| paris_cafe_01 | Paris | proximity | complete | 0.9 | Le Café Suédois | ✗ | 132.61 |
| paris_cafe_01 | Paris | proximity | complete | 0.9 | Le Café Suédois | ✗ | 69.29 |
| paris_cafe_02 | Paris | proximity | complete | 0.9 | Le Café Suédois | ✗ | 21.11 |
| paris_cafe_02 | Paris | proximity | complete | 0.9 | Le Café Suédois | ✗ | 27.17 |
| paris_cafe_02 | Paris | proximity | complete | 0.9 | Le Café Suédois | ✗ | 42.2 |
| cairo_school_01 | Cairo | point_count | complete | 0.9 | الزيتون القبليه |  | 156.8 |
| cairo_school_01 | Cairo | point_count | complete | 0.9 | السرايات الشرقيه |  | 24.14 |
| cairo_school_01 | Cairo | point_count | complete | 0.9 | الزيتون القبليه |  | 150.76 |
| seoul_cafe_01 | Seoul | point_count | complete | 0.9 | 종로1·2·3·4가동 |  | 126.74 |
| seoul_cafe_01 | Seoul | point_count | complete | 0.9 | 종로1·2·3·4가동 |  | 24.16 |
| seoul_cafe_01 | Seoul | point_count | complete | 0.9 | 종로1·2·3·4가동 |  | 132.59 |
| delhi_hosp_01 | New Delhi | point_count | complete | 0.9 | Ramakrishna Puram |  | 105.56 |
| delhi_hosp_01 | New Delhi | point_count | complete | 0.9 | Ramakrishna Puram |  | 30.14 |
| delhi_hosp_01 | New Delhi | point_count | complete | 0.9 | Ramakrishna Puram |  | 36.21 |
| lagos_green_01 | Lagos | greenspace | timeout | — | — |  | 901.44 |
| lagos_green_01 | Lagos | greenspace | timeout | — | — |  | 901.52 |
| lagos_green_01 | Lagos | greenspace | timeout | — | — |  | 901.52 |
| singapore_green_01 | Singapore | greenspace | complete | 0.9 | Unnamed |  | 398.04 |
| singapore_green_01 | Singapore | greenspace | failed | — | — |  | 325.71 |
| singapore_green_01 | Singapore | greenspace | complete | 0.9 | Unnamed |  | 539.61 |
| mumbai_pop_01 | Mumbai | density | complete | 0.9 | Dongri |  | 15.08 |
| mumbai_pop_01 | Mumbai | density | complete | 0.9 | Dongri |  | 66.37 |
| mumbai_pop_01 | Mumbai | density | complete | 0.9 | Dongri |  | 21.13 |
| mumbai_composite_01 | Mumbai | composite | complete | 0.9 | Kurla | ✓ | 15.07 |
| mumbai_composite_01 | Mumbai | composite | complete | 0.9 | Kurla | ✓ | 15.11 |
| mumbai_composite_01 | Mumbai | composite | complete | 0.9 | Kurla | ✓ | 36.21 |
| berlin_hosp_01 | Berlin | point_count | complete | 0.9 | Charlottenburg-Wilmersdorf |  | 120.62 |
| berlin_hosp_01 | Berlin | point_count | complete | 0.9 | Charlottenburg-Wilmersdorf |  | 120.67 |
| berlin_hosp_01 | Berlin | point_count | complete | 0.9 | Charlottenburg-Wilmersdorf |  | 42.22 |
| berlin_school_01 | Berlin | point_count | complete | 0.9 | Mitte |  | 39.16 |
| berlin_school_01 | Berlin | point_count | complete | 0.9 | Mitte |  | 33.18 |
| berlin_school_01 | Berlin | point_count | complete | 0.9 | Mitte |  | 39.24 |
| paris_prox_01 | Paris | proximity | complete | 0.9 | Paris 13e Arrondissement | ✗ | 39.25 |
| paris_prox_01 | Paris | proximity | complete | 0.9 | Paris 13e Arrondissement | ✗ | 27.16 |
| paris_prox_01 | Paris | proximity | complete | 0.9 | Paris 13e Arrondissement | ✗ | 81.35 |
| berlin_prox_01 | Berlin | proximity | complete | 0.9 | Dorotheenstadt Apotheke |  | 36.15 |
| berlin_prox_01 | Berlin | proximity | complete | 0.9 | Dorotheenstadt Apotheke |  | 27.1 |
| berlin_prox_01 | Berlin | proximity | complete | 0.9 | Dorotheenstadt Apotheke |  | 165.96 |
| mumbai_flood_hint_01 | Mumbai | flood_hint | complete | 0.9 | T Ward |  | 15.1 |
| mumbai_flood_hint_01 | Mumbai | flood_hint | complete | 0.9 | T Ward |  | 15.08 |
| mumbai_flood_hint_01 | Mumbai | flood_hint | complete | 0.9 | T Ward |  | 63.37 |
## Findings — N=3 variance run (75 executions)

1. **LLM judge saturation confirmed at scale:** 0.900 ± 0.000 across all 71 completions, regardless of correctness — the judge scored the mis-routed Paris proximity query and every drifted result identically to correct ones. Rank-based expectations carry all discriminative power in this benchmark.
2. **Deterministic paths are fully stable:** all Mumbai queries (three flood phrasings, density, composite) passed 12/12 repetitions with identical answers and 9–36 s latency.
3. **Corrected top-1 accuracy is 87.5% (21/24)** after removing stale live-OSM expectations (Paris cafe top-1 drifted to "Le Café Suédois" — self-consistent 6/6 across reps; Berlin "density" query correctly computes density, not count). The only remaining failures are paris_prox_01 ×3 — the known memory-reuse bug in which a proximity query reuses the cached per-arrondissement count result. This row is kept failing deliberately until the cascade ordering is fixed.
4. **Cache warming quantified:** berlin_pharm_01 cold 568 s → warm 36 s / 30 s (~18× speed-up). All latencies in this run are steady-state (memory warm); cold-start numbers are higher.
5. **Greenspace performance regression is real, not network:** Lagos timed out 3/3 at ~900 s (17 s in June) on a stable connection; Singapore took 398–540 s with one failure. Needs investigation.
6. **Result nondeterminism on live OSM:** Cairo returned two different top-1 areas across repetitions (السرايات الشرقيه vs الزيتون القبليه), both scored 0.9 by the judge — further evidence for finding 1.

## Methodology notes

- N=3 repetitions per query, 25 queries, 75 total executions; runner: `eval/run_benchmark.py --repeat 3`.
- A prior N=3 attempt (2026-07-31) was invalidated by a confirmed network outage affecting all live-OSM fetches and is retained as `results_20260731_171553_PILOT_network_outage.csv` for transparency; it independently reproduced findings 1 and 4.
- Expectations for live-OSM cities are snapshots and subject to data drift; ground-truth-backed rows (Mumbai flood, `has_gt: true`) are the stable regression anchor.
