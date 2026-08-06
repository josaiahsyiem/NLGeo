import json as _j
from tools.llm_client import smart_chat
from tools.ndma_rag import retrieve_ndma
import json
from agents.analysis_agent import run_flood_extent_analysis, compute_flood_exposure

plan = {"uploaded_files": ["/data/uploads/bolivia_test.tif"]}
r = run_flood_extent_analysis("map flood extent", plan, {})

if not r.get("success"):
    print("FLOOD STEP FAILED:", r)
    raise SystemExit(1)

exp = compute_flood_exposure(r["output_raster"], "/tmp/quadrants.geojson")
r["exposure_ranking"] = exp["ranking"]
print(json.dumps(r, indent=2)[:1200])

docs = retrieve_ndma(
    "immediate flood response priorities evacuation relief", k=3)
ctx = "\n\n".join(f"[{d['source']}] {d['text'][:600]}" for d in docs)
rec = smart_chat(
    "You are a disaster-response assistant. Base recommendations ONLY on the "
    "NDMA excerpts provided, citing source names. Be concrete and brief.",
    f"Flood: {r['summary']}\nRanking: {_j.dumps(exp['ranking'][:4])}\n\n"
    f"Excerpts:\n{ctx}\n\nGive 3-4 prioritized recommendations.",
    call_name="ndma_recommendations")
print("\n=== RECOMMENDATIONS ===\n", rec)
