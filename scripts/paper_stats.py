import pandas as pd
import geopandas as gpd


# --- get characteristics of each waterbody dataset
def get_stats(dt):
    # dt = pl.copy()
    # number of recurrent polygons in the AOI
    print(dt.shape[0])
    # range of polygons areas
    print((min(dt.area), max(dt.area)))  # m2
    print((min(dt.area) / 1e6, max(dt.area) / 1e6))  # km2

wb = gpd.read_file("data/wb_all_0669616.gpkg")
get_stats(wb)

pl = gpd.read_file("data/perl_clean.gpkg").to_crs(wb.crs)
get_stats(pl)

gl = gpd.read_file("data/glakes.gpkg").to_crs(wb.crs)
get_stats(gl)

hl = gpd.read_file("data/hydrolakes.gpkg").to_crs(wb.crs)
get_stats(hl)

# --- calculate our recurrence threshold
round(1/22, 2) * 100 # %

# --- waterbody splits/consolidation through time
len(pd.unique(wb["id"])) # 147 unique waterbodies

wb_group = wb.groupby("id").count().copy()
# 22 time steps
wb_group["geometry"].mean() # mean num. of unique configurations
wb_group["geometry"].max()
wb_group["geometry"].min()

# which wb has the highest num. of unique configs
wb_group['geometry'].idxmax()

# what % of wbs have only a single unique config?
round(sum(wb_group["geometry"] == 1) / wb_group.shape[0], 2) * 100
