# TODO: collect wb(s) from multiple wb_all aois
import sys
import numpy as np
import pandas as pd
import geopandas as gpd

sys.path.append(".")
from src import utils

pd.set_option("display.max_columns", None)

# read selected aois from data/wb_all.zip
path_zip = "data/wb_all.zip"
aois = ["0670116", "0769611"]


def aoi_health_check(aoi, path_zip):
    # check that the distribution and counts are not ridiculous
    res = {"aoi": aoi}
    path_in = "{}!data/{}/data/wb_all.gpkg".format(path_zip, aoi)
    gdf = gpd.read_file(path_in)

    res.update({"npolys": gdf.shape[0]})
    res.update({"median": round(np.quantile([x for x in gdf.area], 0.5), 2)})
    res.update({"q1": round(np.quantile([x for x in gdf.area], 0.1), 2)})

    return {"stats": res}


def make_fabric(aois, path_zip):
    # merge wbs that intersect (or touch?) aoi boundaries
    zipfiles = ["{}!data/{}/data/wb_all.gpkg".format(path_zip, aoi) for aoi in aois]
    wb_all = [(gpd.read_file(x)) for x in zipfiles]
    for i in range(len(wb_all)):
        wb_all[i]["idx"] = aois[i]
    
    wb_all_bbox = utils.make_bbox_gdf(pd.concat(wb_all).reset_index(drop=True))
    aoi_boundaries = gpd.read_file("data/cubeSat_buffered_mask_tiles.gpkg")

    breakpoint()
    # TODO: limit the read of aoi_boundaries to wb_all_bbox bounds

    # use wb_all centroids to find matching aoi_boundary

    # split out wb(s) that touch aoi_boundary

    # remove wb(s) below an area threshold

    # ---

    # get all pairs of touching aoi boundaries

    # for each pair, evaluate those with an "on_boundary" flag for touching

    # merge those that touch

    # remove original wb(s) corresponding to each merge from parent wb_all members

    # ---

    # concat modified wb_all members and on_boundary merges

    return None


aoi_health_check(aois[0], path_zip=path_zip)["stats"]
make_fabric(aois, path_zip)
