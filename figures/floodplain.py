# wbpopulate --folder 0669616 --tag 0669616 --aoi ~/data/CubeSat_Arctic_Boreal_LakeArea_1667/data/Yukon_Flats_Basin-buffered_mask_0669616.tif --model ../torchwbtype/torchwbtype/data
import os
import glob
import pandas as pd
import geopandas as gpd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from shapely.geometry import box
import cartopy.feature as cfeature


data_folder = "C:/Vote Data"
# (minx, miny, maxx, maxy) = (74.38, 62.18, 74.48, 62.3) # russia, overlap with Pi paper
(minx, miny, maxx, maxy) = (-146.11, 66.18, -146.03, 66.22)
bbox = box(minx, miny, maxx, maxy)
bbox_gpd = gpd.GeoDataFrame(geometry=[bbox], crs=4326)
bbox_gpd.to_file("data/bbox.gpkg", driver="GPKG")

path_hydrolakes = (
    data_folder + "/hydrolakes_data/HydroLAKES_polys_v10_shp/HydroLAKES_polys_v10.shp"
)
gpd_hydrolakes = gpd.read_file(path_hydrolakes, bbox=(minx, miny, maxx, maxy))
gpd_hydrolakes.to_file("data/hydrolakes.gpkg", driver="GPKG")

if not os.path.exists("data/perl.gpkg"):
    path_perl = data_folder + "/perl/waterbodies"
    f_perl = glob.glob(path_perl + "/*.shp")
    gpd_perl_all = pd.concat([gpd.read_file(x) for x in f_perl]).to_crs(4326)
    gpd_perl_all.to_file("data/perl_all.gpkg", driver="GPKG")
    gpd_perl = gpd.read_file("data/perl_all.gpkg", bbox=(minx, miny, maxx, maxy))
    # os.remove("perl_all.gpkg")
    gpd_perl.to_file("data/perl.gpkg", driver="GPKG")
gpd_perl = gpd.read_file("data/perl.gpkg")

path_glakes = data_folder + "/GLAKES/GLAKES/GLAKES_na2.shp"
gpd_glakes = gpd.read_file(path_glakes, bbox=(minx, miny, maxx, maxy))
gpd_glakes.to_file("data/glakes.gpkg", driver="GPKG")

# gpd.read_file("data/wb_all_0669616.gpkg").to_crs(4326).to_file("data/wb_all_0669616_4326.gpkg", driver="GPKG")
gpd_wbextractor = gpd.read_file(
    "data/wb_all_0669616_4326.gpkg", bbox=(minx, miny, maxx, maxy)
)
gpd_wbextractor.to_file("data/wbextractor.gpkg", driver="GPKG")

# ---

fig, (ax1, ax2, ax3) = plt.subplots(1, 3)

gpd_perl.plot(ax=ax1, legend=True, legend_kwds={"shrink": 0.6}, color="green")
gpd_hydrolakes.plot(ax=ax1, legend=True, legend_kwds={"shrink": 0.6}, color="yellow")
ax1.set_title("Medium resolution \n (HydroLAKES)")
ax1.axis("off")

gpd_perl.plot(ax=ax2, legend=True, legend_kwds={"shrink": 0.6}, color="green")
gpd_glakes.plot(ax=ax2, legend=True, legend_kwds={"shrink": 0.6}, color="pink")
ax2.set_title("Medium resolution \n (GLAKES)")
ax2.axis("off")

gpd_perl.plot(ax=ax3, legend=True, legend_kwds={"shrink": 0.6}, color="green")
gpd_wbextractor.plot(ax=ax3, legend=True, legend_kwds={"shrink": 0.6}, color="blue")
ax3.set_title("High resolution \n (wbextractor)")
ax3.axis("off")

plt.tight_layout()
plt.show()

plt.savefig("figures/floodplain.pdf", bbox_inches="tight")
