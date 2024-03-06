import geopandas as gpd


def get_stats(dt):
    # dt = pl.copy()
    # number of recurrent polygons in the AOI
    print(dt.shape[0])
    # range of polygons areas
    print((min(dt.area), max(dt.area)))  # m2
    print((min(dt.area) / 1e6, max(dt.area) / 1e6))  # km2


# ---
wb = gpd.read_file("data/wb_all_0669616.gpkg")
get_stats(wb)

# ---
pl = gpd.read_file("data/perl_clean.gpkg").to_crs(wb.crs)
get_stats(pl)

# ---
gl = gpd.read_file("data/glakes.gpkg").to_crs(wb.crs)
get_stats(gl)

# ---
hl = gpd.read_file("data/hydrolakes.gpkg").to_crs(wb.crs)
get_stats(hl)
