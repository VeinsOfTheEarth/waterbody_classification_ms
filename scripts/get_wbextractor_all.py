# TODO: collect wb(s) from multiple wb_all aois
import sys
import numpy as np
import pandas as pd
import geopandas as gpd

sys.path.append(".")
from src import utils

# read selected aois from data/wb_all.zip
path_zip = "data/wb_all.zip"
aois = ["0670116", "0769611"]
zipfiles = ["{}!data/{}/data/wb_all.gpkg".format(path_zip, aoi) for aoi in aois]

wb_all_bbox = pd.concat(
    [utils.make_bbox_gdf(gpd.read_file(x)) for x in zipfiles]
).reset_index(drop=True)
wb_all_bbox["idx"] = aois
wb_all_bbox.to_file("test_bbox.gpkg")


def aoi_health_check(aoi, path_zip):
    # check that the distribution and counts are not ridiculous
    res = {"aoi": aoi}
    path_in = "{}!data/{}/data/wb_all.gpkg".format(path_zip, aoi)
    gdf = gpd.read_file(path_in)
    
    res.update({"npolys": gdf.shape[0]})
    res.update({"median": round(np.quantile([x for x in gdf.area], 0.5), 2)})
    res.update({"q1": round(np.quantile([x for x in gdf.area], 0.1), 2)})
    
    return res


aoi_health_check(aois[0], path_zip=path_zip)


def make_fabric():
    # merge wbs that intersect (or touch?) aoi boundaries
    return None
