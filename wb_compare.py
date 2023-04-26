# hydrolakes
# perl
# glakes
# Yukon_Flats_Basin-buffered_mask_0669616

import os
import glob
import pandas as pd
import geopandas as gpd
import cartopy.crs as ccrs
from shapely.geometry import box

data_folder = "C:/Vote Data"
# (minx, miny, maxx, maxy) = (74.38, 62.18, 74.48, 62.3) # russia, overlap with Pi paper
(minx, miny, maxx, maxy) = (-146.11, 66.18, -146.03, 66.22)
bbox = box(minx, miny, maxx, maxy)
bbox_gpd = gpd.GeoDataFrame(geometry=[bbox], crs=4326)
bbox_gpd.to_file("bbox.gpkg", driver="GPKG")

path_hydrolakes = data_folder + "/hydrolakes_data/HydroLAKES_polys_v10_shp/HydroLAKES_polys_v10.shp"
gpd_hydrolakes = gpd.read_file(path_hydrolakes, bbox = (minx, miny, maxx, maxy))
gpd_hydrolakes.to_file("hydrolakes.gpkg", driver="GPKG")

if not os.path.exists("perl.gpkg"):
    path_perl = data_folder + "/perl/waterbodies"
    f_perl = glob.glob(path_perl + "/*.shp")
    gpd_perl_all = pd.concat([gpd.read_file(x) for x in f_perl]).to_crs(4326)
    gpd_perl_all.to_file("perl_all.gpkg", driver="GPKG")
    gpd_perl = gpd.read_file("perl_all.gpkg", bbox = (minx, miny, maxx, maxy))
    # os.remove("perl_all.gpkg")
    gpd_perl.to_file("perl.gpkg", driver="GPKG")
gpd_perl = gpd.read_file("perl.gpkg")

path_glakes = data_folder + "/GLAKES/GLAKES/GLAKES_na2.shp"
gpd_glakes = gpd.read_file(path_glakes, bbox = (minx, miny, maxx, maxy))
gpd_glakes.to_file("glakes.gpkg", driver="GPKG")
