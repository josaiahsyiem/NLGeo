"""End-to-end FloodAgent run on the real 2024 Assam flood."""
import json
import os

from agents.analysis_agent import compute_flood_exposure
from tools.ndma_rag import retrieve_ndma
from tools.llm_client import smart_chat

MASK = "/data/processed/majuli_flood_mask.tif"
DISTRICTS = "/data/uploads/districts_aoi.geojson"
POP = "/data/uploads/india_pop_2024_aoi.tif"   # arrives with WorldPop

pop_path = POP if os.path.exists(POP) else None
print("population raster:", "FOUND" if pop_path else "not yet - ranking by area")

exp = compute_flood_exposure(MASK, DISTRICTS, pop_path=pop_path)
print(json.dumps(exp, indent=2))

docs = retrieve_ndma(
    "flood response priorities evacuation relief riverine flooding Assam", k=3)
ctx = "\n\n".join(f"[{d['source']}] {d['text'][:600]}" for d in docs)

summary = ("Flood extent mapped from Sentinel-2 imagery of the Brahmaputra "
           "around Majuli, Assam (2024-07-26) using U-Net segmentation: "
           "36.6% of the AOI inundated (~470 sq km).")

rec = smart_chat(
    "You are a disaster-response assistant for Indian authorities. Base every "
    "recommendation ONLY on the NDMA guideline excerpts provided, citing the "
    "source document for each. Be concrete and brief.",
    f"Situation: {summary}\n"
    f"District exposure ranking: {json.dumps(exp['ranking'])}\n\n"
    f"NDMA excerpts:\n{ctx}\n\n"
    "Give 4 prioritized response recommendations for the affected districts.",
    call_name="assam_ndma_recommendations")

print("\n=== ASSAM RESPONSE RECOMMENDATIONS ===\n", rec)
