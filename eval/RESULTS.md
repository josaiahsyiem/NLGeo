# NLGeo Benchmark Results

Run: 2026-07-31T15:44:06  
Raw data: `results_20260731_144852.csv`

## Summary

- Queries run: **25**
- Success rate: **96%** (24/25)
- Mean eval score: **0.900 ± 0.000**
- Top-1 accuracy (where expected known): **60%** (9/15)
- Latency p50: **39.42s**, p95: **266.62s**

## Per-query

| id | city | type | status | eval | top1 | correct | latency (s) |
|---|---|---|---|---|---|---|---|
| mumbai_flood_01 | Mumbai | flood | complete | 0.9 | Kurla | ✓ | 12.15 |
| mumbai_flood_02 | Mumbai | flood | complete | 0.9 | Kurla | ✓ | 12.27 |
| mumbai_flood_03 | Mumbai | flood | complete | 0.9 | Kurla | ✓ | 12.13 |
| berlin_pharm_01 | Berlin | point_count | complete | 0.9 | Mitte | ✓ | 39.42 |
| berlin_pharm_02 | Berlin | point_count | complete | 0.9 | Friedenau | ✗ | 145.44 |
| berlin_clinic_01 | Berlin | point_count | complete | 0.9 | Charlottenburg-Wilmersdorf | ✓ | 39.42 |
| london_hosp_01 | Greater London | point_count | complete | 0.9 | City of Westminster | ✗ | 254.55 |
| london_flood_01 | London | flood_inversion | complete | 0.9 | London Borough of Croydon | ✗ | 21.17 |
| london_green_01 | London | greenspace | complete | 0.9 | London Borough of Barnet | ✗ | 266.62 |
| paris_hosp_01 | Paris | point_count | complete | 0.9 | Paris 13e Arrondissement |  | 163.57 |
| paris_rest_01 | Paris | point_count | complete | 0.9 | Paris 11e Arrondissement | ✓ | 39.42 |
| paris_cafe_01 | Paris | proximity | complete | 0.9 | Aux Tours de Notre-Dame | ✓ | 36.38 |
| paris_cafe_02 | Paris | proximity | complete | 0.9 | Aux Tours de Notre-Dame | ✓ | 45.45 |
| cairo_school_01 | Cairo | point_count | complete | 0.9 | السرايات الشرقيه |  | 51.58 |
| seoul_cafe_01 | Seoul | point_count | complete | 0.9 | 종로1·2·3·4가동 |  | 42.39 |
| delhi_hosp_01 | New Delhi | point_count | complete | 0.9 | Ramakrishna Puram | ✗ | 36.37 |
| lagos_green_01 | Lagos | greenspace | timeout | — | — |  | 902.68 |
| singapore_green_01 | Singapore | greenspace | complete | 0.9 | Unnamed |  | 757.49 |
| mumbai_pop_01 | Mumbai | density | complete | 0.9 | Dongri |  | 15.15 |
| mumbai_composite_01 | Mumbai | composite | complete | 0.9 | Kurla | ✓ | 12.11 |
| berlin_hosp_01 | Berlin | point_count | complete | 0.9 | Charlottenburg-Wilmersdorf |  | 42.45 |
| berlin_school_01 | Berlin | point_count | complete | 0.9 | Mitte |  | 60.63 |
| paris_prox_01 | Paris | proximity | complete | 0.9 | Paris 13e Arrondissement | ✗ | 254.89 |
| berlin_prox_01 | Berlin | proximity | complete | 0.9 | Dorotheenstadt Apotheke |  | 36.35 |
| mumbai_flood_hint_01 | Mumbai | flood_hint | complete | 0.9 | T Ward |  | 12.15 |

## Findings from this run

1. LLM judge saturates at 0.9 (std 0.000) regardless of correctness — non-discriminative; rank-based expectations carry the evaluation.
2. Memory reuse crossed query-type boundaries: "hospitals within 3km" (proximity) reused the cached "hospitals per arrondissement" (count) result for Paris. Third observed instance of memory-priority bug; type-gating insufficient.
3. London admin-boundary granularity is nondeterministic run-to-run (boroughs vs fine districts), making fixed top-1 expectations unstable for London.
4. Live-OSM drift: Westminster/Croydon leaders swapped since June (near-tie).
5. Greenspace fetch regression: Lagos 17s→902s timeout, Singapore 757s.