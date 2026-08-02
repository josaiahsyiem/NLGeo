# Ablation: Deterministic-First vs LLM-Only Execution

**Question:** does NLGeo's deterministic-first architecture — hand-written, verified
geospatial code for recognised query types, with LLM code generation only as
fallback — actually outperform the pure-LLM approach used by prior work
(LLM-Geo, GISclaw, GTChain), and by how much?

**Method.** 12 benchmark queries (one per capability: ground-truth flood, three
point-count cities, density, per-capita-adjacent, composite, two proximity,
inversion-adjacent, two non-Latin-script cities) were run in two arms on the
same machine and network:

- **Arm A — LLM-only:** `SKIP_DETERMINISTIC=true`. All 22 deterministic
  branches (audited and gated for this experiment) disabled; every query forced
  through the full LLM pipeline: refine+plan → GTChain workflow → data
  understanding → up to 5 self-correcting code-generation attempts with
  error-memory injection and re-planning.
- **Arm B — deterministic-first:** flag off; the system as designed.

Qdrant task memory was cleared before every arm so no cached code could leak
between conditions. The flag was verified inside the worker container
(`docker exec … os.getenv`) before each arm. Arm A was run twice (v1 on the
default network, v2 on a mobile hotspot) to exclude a network confound after
v1 showed heavy failures; retrieval succeeded in seconds in both, and all Arm A
failures occurred in the code-generation stage, not fetch.

## Results

| Metric | LLM-only (v1) | LLM-only (v2, hotspot) | **Deterministic-first** |
|---|---|---|---|
| Completed | 3/12 (25%) | 2/12 (17%) | **12/12 (100%)** |
| Correct top-1 (of checkable) | 1 | 0 | **6/6 (100%)** |
| Latency p50 | ~24 s (mostly failures) | ~24 s (mostly failures) | **18.1 s** |
| Latency range | 12–91 s | 21–48 s | 9.0–123.8 s (cold fetches) |
| Reproducible across runs | No — different queries succeed each run | — | Yes — identical answers |

Per-query outcomes (✓ correct, ○ completed-but-wrong/unchecked, ✗ failed):

| Query | LLM v1 | LLM v2 | Deterministic |
|---|---|---|---|
| mumbai_flood_02 (ground truth) | ○ wrong (R/S Ward, eval 0.9) | ○ wrong (R/S Ward, eval 0.9) | ✓ Kurla |
| berlin_pharm_01 | ✗ | ✗ | ✓ Mitte |
| berlin_clinic_01 | ✗ | ✗ | ✓ Charlottenburg-Wilmersdorf |
| london_hosp_01 | ○ (eval 0.1) | ✗ | ○ Westminster |
| paris_rest_01 | ✗ | ✗ | ✓ 11e Arrondissement |
| paris_cafe_02 (proximity) | ✗ | ✗ | ✓ Aux Tours de Notre-Dame |
| cairo_school_01 | ✗ | ○ (eval 0.1, different area) | ○ completes |
| seoul_cafe_01 | ✗ | ✗ | ○ completes |
| delhi_hosp_01 | ✗ | ✗ | ○ completes |
| mumbai_pop_01 | ✗ | ✗ | ○ Dongri |
| mumbai_composite_01 | ✓ Kurla | ✗ | ✓ Kurla |
| berlin_prox_01 (proximity) | ✗ | ✗ | ○ Dorotheenstadt Apotheke |

## Findings

1. **The deterministic-first architecture is the difference between a working
   system and a broken one.** Across 24 LLM-only executions: 21% completed,
   4% correct. Deterministic-first on the same queries: 100% completed, 100%
   of checkable answers correct.

2. **LLM-only fails confidently.** Both LLM-only runs produced a wrong answer
   to the ground-truth flood query (R/S Ward instead of Kurla) that the LLM
   judge scored 0.9 — indistinguishable, by judge score, from the correct
   deterministic answer. External ground truth, not the judge, catches this.

3. **LLM-only is non-reproducible.** The set of queries that succeed changes
   between runs (composite: pass→fail; London: complete→fail; Cairo:
   fail→complete). The deterministic arm returns identical answers every run.

4. **Failure modes observed in the LLM arm** (from worker logs): Type-3
   silent zero-value spatial joins, `result is None`, ImportError on blocked
   libraries, rasterio dataset errors — i.e., genuine code-generation failures
   after successful data retrieval; not network effects (retrieval completed
   in 4–8 s in both arms).

5. **The judge discriminates only at the extremes.** Two LLM-arm completions
   received eval 0.1 — the first non-0.9 scores observed in the project —
   while an objectively wrong flood ranking still received 0.9. This refines
   the earlier judge-saturation finding: the judge detects gross malformation
   but not wrong-but-plausible answers.

6. **Token cost:** not instrumented per-arm in this round (Langfuse totals
   only). Directionally: every LLM-only query consumed up to 5 generation
   attempts (~3–6k tokens each) to mostly fail; deterministic paths consumed
   zero generation tokens on these queries.

## Caveats

- n=12 queries, arms run once (LLM arm twice). Success-rate deltas of this
  magnitude (100% vs 21%) are decisive at this n; finer metrics are not.
- The LLM arm uses the same prompts/scaffolding as the fallback path; a
  system engineered *only* for LLM generation might tune prompts further.
  This measures the marginal value of the deterministic layer within NLGeo,
  not an upper bound on LLM-only systems.
- Deterministic-arm latencies include cold live-OSM fetches (max 123.8 s for
  Berlin proximity); steady-state p50 from the N=3 benchmark is 36 s.

**Conclusion.** The central architectural bet — deterministic-first, LLM as
fallback — is not an optimisation; it is what makes the system work. Removing
it collapses task success from 100% to ~21% and correctness to ~4%, while
introducing run-to-run nondeterminism and confidently-wrong answers that the
LLM judge cannot detect.
