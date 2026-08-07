"""Flood mask (raster) -> web-ready GeoJSON polygons."""
import json

import geopandas as gpd
import rasterio
from rasterio import features
from shapely.geometry import shape

MASK = "/data/processed/majuli_flood_mask.tif"
OUT = "/data/processed/majuli_flood.geojson"
MIN_AREA_M2 = 50_000        # drop puddles under 5 hectares
SIMPLIFY_M = 30             # smooth jagged pixel edges

with rasterio.open(MASK) as src:
    mask = src.read(1)
    polys = [
        shape(geom)
        for geom, val in features.shapes(mask, transform=src.transform)
        if val == 1
    ]
    crs = src.crs

gdf = gpd.GeoDataFrame(geometry=polys, crs=crs)

# area filter + simplify in metric CRS, then to lat/lon for Leaflet
utm = gdf.estimate_utm_crs()
gdf = gdf.to_crs(utm)
gdf = gdf[gdf.area >= MIN_AREA_M2]
gdf["geometry"] = gdf.geometry.simplify(SIMPLIFY_M)
gdf = gdf.to_crs("EPSG:4326")

gdf.to_file(OUT, driver="GeoJSON")
size_mb = len(json.dumps(json.load(open(OUT)))) / 1e6
print(f"{len(gdf)} flood polygons -> {OUT} ({size_mb:.1f} MB)")
