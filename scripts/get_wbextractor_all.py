# TODO: collect wb(s) from multiple wb_all aois
import sys
import pandas as pd
import geopandas as gpd

sys.path.append(".")
from src import utils

# read selected aois from data/wb_all.zip
path_zip = "data/wb_all.zip"
aois = ["0670116", "0769611"]
zipfiles = ["{}!data/{}/data/wb_all.gpkg".format(path_zip, aoi) for aoi in aois]
wb_all = pd.concat(
    [utils.make_bbox_gdf(gpd.read_file(x)) for x in zipfiles]
).reset_index(drop=True)
wb_all["idx"] = aois
wb_all.to_file("test_bbox.gpkg")

# bnds_gdf = utils.make_bbox_gdf(wb_all)
# bnds_gdf.to_file("test_bbox.gpkg")


def aoi_health_check():
    # check that the distribution and counts are not ridiculous
    return None


def make_fabric():
    # merge wbs that intersect (or touch?) aoi boundaries
    return None
