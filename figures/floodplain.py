# wbpopulate --folder 0669616 --tag 0669616 --aoi ~/data/CubeSat_Arctic_Boreal_LakeArea_1667/data/Yukon_Flats_Basin-buffered_mask_0669616.tif --model ../torchwbtype/torchwbtype/data
import os
import glob
import numpy as np
import pandas as pd
import seaborn as sns
import geopandas as gpd
import contextily as cx
import matplotlib.pyplot as plt
from shapely.geometry import box

# import cartopy.crs as ccrs
# import cartopy.feature as cfeature

from wbextractor import blobs  # type: ignore


data_folder = "C:/Vote Data"
# (minx, miny, maxx, maxy) = (74.38, 62.18, 74.48, 62.3) # russia, overlap with Pi paper
(minx, miny, maxx, maxy) = (-146.11, 66.18, -146.03, 66.22)
bbox = box(minx, miny, maxx, maxy)
bbox_gpd = gpd.GeoDataFrame(geometry=[bbox], crs=4326)
bbox_gpd.to_file("data/bbox.gpkg", driver="GPKG")

osm_river = gpd.read_file("data/osm.gpkg")

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

plt.close()
fig, (ax1, ax2, ax3) = plt.subplots(1, 3)

gpd_perl.plot(ax=ax1, legend=True, legend_kwds={"shrink": 0.6}, color="green")
osm_river.plot(ax=ax1, color="blue")
gpd_hydrolakes.plot(ax=ax1, legend=True, legend_kwds={"shrink": 0.6}, color="yellow")
ax1.set_title("Medium resolution \n (HydroLAKES)")
ax1.set_xlim(([minx, maxx + 0.007]))
ax1.set_ylim(([miny, maxy]))
ax1.axis("off")

gpd_perl.plot(ax=ax2, legend=True, legend_kwds={"shrink": 0.6}, color="green")
osm_river.plot(ax=ax2, color="blue")
gpd_glakes.plot(ax=ax2, legend=True, legend_kwds={"shrink": 0.6}, color="pink")
ax2.set_title("Medium resolution \n (GLAKES)")
ax2.set_xlim(([minx, maxx + 0.007]))
ax2.set_ylim(([miny, maxy]))
ax2.axis("off")

gpd_perl.plot(ax=ax3, legend=True, legend_kwds={"shrink": 0.6}, color="green")
osm_river.plot(ax=ax3, color="blue")
gpd_wbextractor.plot(ax=ax3, legend=True, legend_kwds={"shrink": 0.6}, color="blue")
ax3.set_title("High resolution \n (wbextractor)")
ax3.set_xlim(([minx, maxx + 0.007]))
ax3.set_ylim(([miny, maxy]))
ax3.axis("off")

plt.tight_layout()
# plt.show()
plt.savefig("figures/floodplain.png", bbox_inches="tight")

# ---
test = gpd_perl[gpd_perl.area > float(np.quantile(gpd_perl.area, [0.1]))]
if not os.path.exists("data/perl_buffer.gpkg"):
    gpd_perl_buffer = test.to_crs(crs=32606).buffer(60).to_crs(4326)
    gpd_perl_buffer.to_file("data/perl_buffer.gpkg", driver="GPKG")
gpd_perl_buffer = gpd.read_file("data/perl_buffer.gpkg")
x = gpd.GeoDataFrame(
    {
        "id": [x for x in range(gpd_perl_buffer.shape[0])],
        "layer": 0,
        "geometry_filtered": test.geometry,
        "lake_prediction": 1,
    },
    geometry=gpd_perl_buffer.geometry,
)
gpkg, xwalk = blobs.consolidate_multiples(x)

dt = pd.concat(
    [
        pd.DataFrame({"source": "perl", "area": [x for x in gpkg.area]}),
        pd.DataFrame({"source": "glakes", "area": [x for x in gpd_glakes.area]}),
        pd.DataFrame(
            {"source": "hydrolakes", "area": [x for x in gpd_hydrolakes.area]}
        ),
        pd.DataFrame(
            {"source": "wbconvert", "area": [x for x in gpd_wbextractor.explode().area]}
        ),
    ]
)
sns.displot(
    dt.reset_index(drop=True),
    x="area",
    hue="source",
    kind="ecdf",
    height=2,
    aspect=3 / 2,
    palette=["green", "pink", "yellow", "blue"],
)
plt.xscale("log")
plt.savefig("figures/accuracy.png")
