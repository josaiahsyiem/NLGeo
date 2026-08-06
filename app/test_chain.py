import json
from agents.analysis_agent import run_flood_extent_analysis, compute_flood_exposure

plan = {"uploaded_files": ["/data/uploads/bolivia_test.tif"]}
r = run_flood_extent_analysis("map flood extent", plan, {})
exp = compute_flood_exposure(r["output_raster"], "/tmp/quadrants.geojson")
r["exposure_ranking"] = exp["ranking"]
print(json.dumps(r, indent=2)[:1200])
