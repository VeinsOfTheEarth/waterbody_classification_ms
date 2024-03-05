import geopandas as gpd

dt = gpd.read_file("data/wb_all_0669616.gpkg")

# number of recurrent polygons in the AOI
print(dt.shape[0])

# range of polygons areas (in km2)
print((min(dt.area) / 1e6, max(dt.area) / 1e6))
