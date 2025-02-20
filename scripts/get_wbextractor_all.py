# TODO: collect wb(s) from multiple wb_all aois
import sys
import glob
import itertools
import numpy as np
import xarray as xr
import pandas as pd
import geopandas as gpd
from shapely.geometry import box

sys.path.append(".")
from src import utils

pd.set_option("display.max_columns", None)

# read selected aois from data/wb_all.zip
path_zip = "data/wb_all.zip"
# aois = ["0670116", "0769611"]
aois = ["0670116"]


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
    wb_all = [(gpd.read_file(x).to_crs(3995)) for x in zipfiles]
    for i in range(len(wb_all)):
        wb_all[i]["idx"] = aois[i]

    wb_all_bbox = utils.make_bbox_gdf(pd.concat(wb_all).reset_index(drop=True))

    flist_aoi_tifs = glob.glob(
        "data/CubeSat_Arctic_Boreal_LakeArea_1667/data/Yukon_Flats_Basin-buffered_mask_*"
    )
    flist_aoi_tifs = list(
        itertools.compress(
            flist_aoi_tifs, [any([aoi in x for aoi in aois]) for x in flist_aoi_tifs]
        )
    )

    def get_tif_bbox(fname, aoi):
        crs = str(xr.open_dataset(fname, engine="rasterio").rio.crs).split(":")[1]
        bounds = xr.open_dataset(fname, engine="rasterio").rio.bounds()
        return gpd.GeoDataFrame(
            {"aoi": aoi}, geometry=[box(*bounds)], index=[0], crs=crs
        ).to_crs(3995)

    aoi_bboxs = [get_tif_bbox(flist_aoi_tifs[i], aois[i]) for i in range(len(aois))]

    # ---
    pd.concat(aoi_bboxs).reset_index(drop=True).to_file(
        "test.gpkg", layer="aoi_boundaries"
    )
    wb_all_bbox.to_file("test.gpkg", layer="wb_all_bbox")
    pd.concat(wb_all).to_file("test.gpkg", layer="wb_all")
    # # mapview test.gpkg "aoi_boundaries,wb_all" ""
    # ---

    # breakpoint()

    # split out wb(s) that touch aoi_boundary
    gpd.sjoin(wb_all[0], gpd.GeoDataFrame(geometry=[aoi_bboxs[0].exterior[0]]))
    breakpoint()

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
