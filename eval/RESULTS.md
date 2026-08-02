# NLGeo Benchmark Results

Run: 2026-08-02T11:36:53  
Raw data: `results_20260802_113102.csv`

## Summary

- Queries run: **12**
- Success rate: **17%** (2/12)
- Mean eval score: **0.500 ± 0.566**
- Top-1 accuracy (where expected known): **0%** (0/1)
- Latency p50: **24.12s**, p95: **24.12s**

## Per-query

| id | city | type | status | eval | top1 | correct | latency (s) |
|---|---|---|---|---|---|---|---|
| mumbai_flood_02 | Mumbai | flood | complete | 0.9 | R/S Ward | ✗ | 21.25 |
| berlin_pharm_01 | Berlin | point_count | failed | — | — |  | 24.24 |
| berlin_clinic_01 | Berlin | point_count | failed | — | — |  | 33.26 |
| london_hosp_01 | Greater London | point_count | failed | — | — |  | 42.28 |
| paris_rest_01 | Paris | point_count | failed | — | — |  | 21.12 |
| paris_cafe_02 | Paris | proximity | failed | — | — |  | 24.11 |
| cairo_school_01 | Cairo | point_count | complete | 0.1 | البستان |  | 24.12 |
| seoul_cafe_01 | Seoul | point_count | failed | — | — |  | 24.18 |
| delhi_hosp_01 | New Delhi | point_count | failed | — | — |  | 48.28 |
| mumbai_pop_01 | Mumbai | density | failed | — | — |  | 24.18 |
| mumbai_composite_01 | Mumbai | composite | failed | — | — |  | 33.18 |
| berlin_prox_01 | Berlin | proximity | failed | — | — |  | 30.21 |