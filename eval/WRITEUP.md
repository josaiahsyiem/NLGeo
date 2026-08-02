# My LLM Judge Gave Everything 0.9 — What Actually Evaluating an LLM Agent Taught Me

*Building NLGeo, an autonomous natural-language GIS agent, taught me plenty about geospatial pipelines. But the most valuable lessons came at the end, when I stopped adding features and started measuring. This is a short account of what a real evaluation harness revealed — including the moment I discovered my LLM judge had been rubber-stamping everything, and the ablation that showed my core architectural bet was the difference between a working system and a broken one.*

---

## The system, briefly

NLGeo answers questions like *"Which Mumbai wards have the highest flood-exposed population?"* or *"cafes within 2km of Paris city centre"* and returns a ranked, interactive map. Under the hood: FastAPI and Celery, live OpenStreetMap retrieval via the Overpass API, PostGIS, a Qdrant vector memory that caches verified analyses, and an LLM (Llama-3.3-70B via Groq) that plans queries and — when nothing else fits — writes geospatial Python that runs in a sandbox with up to five self-correcting attempts.

The design bet that matters for this story: **deterministic-first**. The research systems NLGeo builds on (LLM-Geo, GISclaw, GTChain, GIS Copilot) route every query through LLM code generation. NLGeo inverts that: fifty-plus recognised query types run through hand-written, verified spatial code, and the LLM is the fallback, not the default. I believed this bought accuracy, speed, and independence from rate limits. For months, that belief was an argument. Then I measured it.

## Building the benchmark

The eval harness is deliberately boring: a versioned JSONL file of 25 queries across 9 cities and 8 query types — ground-truth flood analysis, point counts, density, composites, proximity, inversions, non-Latin-script cities — each with an expected top-ranked answer where one is knowable. A runner submits each query to the live system, polls to completion, extracts the ranked results, and scores top-1 correctness, latency, and the system's own LLM-judge score. Three repetitions per query, 75 executions, memory cleared to a defined state first.

Headline numbers: **95% task success, 87.5% top-1 accuracy on checkable queries, p50 latency 36 seconds** steady-state. Good numbers. But the numbers were the least interesting output.

## Finding 1: my LLM judge was decorative

Every completed query in the system gets scored 0–1 by an LLM judge against four criteria — does it answer the question, are the values realistic, does it make geographic sense, are the columns present. Across 71 completed executions, the judge's score was **0.900 ± 0.000**. Not *roughly* 0.9. Exactly 0.9, every single time — for correct answers, for results at the wrong administrative granularity, and later, for answers that were flatly wrong against ground truth.

The judge wasn't evaluating; it was vibing. It turned out to discriminate only at the extremes — malformed outputs occasionally earned a 0.1 — but a wrong-yet-plausible ranking was indistinguishable, by judge score, from a correct one. All the discriminative power in my evaluation came from the boring part: fixed expected answers and a hand-built QGIS ground truth. If I'd shipped the judge score as my accuracy metric, I'd have been reporting a constant.

I suspect this failure mode is common in agent systems that self-report quality. The judge is useful as a smoke test. It is not a metric. If your eval's variance is zero, you don't have an eval.

## Finding 2: the ablation

The real experiment: what does deterministic-first actually buy? I audited the codebase, gated all 22 deterministic branches behind a `SKIP_DETERMINISTIC` flag (an audit script found branches I'd forgotten existed — the first "LLM-only" run leaked deterministic code through an ungated path, which is its own lesson about verifying your experimental condition inside the running container), cleared the memory between arms, and ran the same 12 representative queries both ways. I ran the LLM-only arm twice — once on my normal network and once on a mobile hotspot — because the first run failed so heavily I needed to exclude a network confound. Retrieval succeeded in seconds in both; the failures were all in code generation.

The result was not subtle.

| | LLM-only (2 runs, 24 executions) | Deterministic-first |
|---|---|---|
| Completed | 21% | **100%** |
| Correct vs ground truth / expectations | 4% | **100%** |
| Reproducible across runs | No | Yes |

The LLM arm's failures were genuine code-generation failures: silent zero-value spatial joins, `result is None`, import errors, raster misuse — after successful data retrieval, with error-memory injection and re-planning firing exactly as designed, five attempts each. And the failures weren't even stable: *which* queries succeeded changed between the two runs. The composite query passed once and failed once. LLM-only wasn't just less accurate; it was non-reproducible.

The most instructive single row: the ground-truth flood query. Deterministic mode answers it correctly in nine seconds, every time. LLM-only mode *completed* it in both runs — and produced the wrong ranking both times, which the judge scored 0.9, same as the right answer. A confidently wrong result, undetectable by self-evaluation, caught only by external ground truth. That one row justifies the entire benchmark.

My honest caveat: this measures the marginal value of the deterministic layer *within my system*, using the same prompts as my fallback path. A system engineered exclusively around LLM generation might tune further and do better. But the papers this field builds on treat LLM-generated GIS code as the default execution model, and at least in my hands, removing the deterministic layer collapsed task success from 100% to 21%. The architecture isn't an optimisation. It's load-bearing.

## Finding 3: the benchmark caught bugs I didn't know I had

Within its first fifty executions, the harness surfaced, with evidence: a cache-reuse bug in which a proximity query silently reused a cached per-district count result for the same city and feature (same top-1, wrong analysis type — my memory system's type-gating was insufficient); answers that depended on what had run *before* them, because a stored generic-path result could outrank the authoritative deterministic path for an identically-worded query; run-to-run nondeterminism in which administrative granularity London resolved to; live-OSM data drift that silently invalidated month-old expected answers; and a performance regression that turned a 17-second greenspace query into a 900-second timeout. One of these I've fixed; one I've deliberately left failing in the benchmark as a regression guard until its fix lands. None of them were visible from using the system by hand. All of them were visible from running the same 25 queries three times and looking.

## What I'd tell past me

Write the eval before you think you need it — mine paid for itself in the first afternoon. Trust external ground truth over self-evaluation; one hand-built QGIS benchmark did more evaluative work than every judge call combined. Verify your experimental condition inside the running system, not in your config file. Treat expectations on live data as perishable. And measure your architectural beliefs: mine happened to survive contact with the data, but I only know that because I let the data take a shot at it.

---

*NLGeo is on GitHub — [github.com/josaiahsyiem/NLGeo](https://github.com/josaiahsyiem/NLGeo) — including the benchmark (`eval/benchmark.jsonl`), the runner, full results (`eval/RESULTS.md`), and the ablation report (`eval/ABLATION.md`). The whole evaluation reproduces with one command.*
