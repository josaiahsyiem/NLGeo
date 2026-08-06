import json
import rasterio
from shapely.geometry import box
import geopandas as gpd
from agents.analysis_agent import compute_flood_exposure

MASK = "/data/processed/flood_extent_1786045795.tif"

with rasterio.open(MASK) as src:
    l, b, r, t = src.bounds
cx, cy = (l + r) / 2, (b + t) / 2
zones = gpd.GeoDataFrame({
    "name": ["NW", "NE", "SW", "SE"],
    "geometry": [box(l, cy, cx, t), box(cx, cy, r, t),
                 box(l, b, cx, cy), box(cx, b, r, cy)],
}, crs=src.crs)
zones.to_file("/tmp/quadrants.geojson", driver="GeoJSON")

print(json.dumps(compute_flood_exposure(MASK, "/tmp/quadrants.geojson"), indent=2))
