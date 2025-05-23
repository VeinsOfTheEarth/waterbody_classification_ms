# TODO: collect wb(s) from multiple wb_all aois
import sys
import glob
import itertools
import subprocess
import numpy as np
import xarray as xr
import pandas as pd
import geopandas as gpd
from shapely.geometry import box

sys.path.append(".")
from src import utils

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)


def aoi_health_check(aoi, path_zip):
    # check that the distribution and counts are not ridiculous
    res = {"aoi": aoi}
    path_in = "{}!data/{}/data/wb_all.gpkg".format(path_zip, aoi)
    gdf = gpd.read_file(path_in)

    res.update({"npolys": gdf.shape[0]})
    res.update({"median": round(np.quantile([x for x in gdf.area], 0.5), 2)})
    res.update({"q1": round(np.quantile([x for x in gdf.area], 0.1), 2)})

    def _is_failing(res):
        res["npolys"] > 1
        # TODO: remove wb(s) below an area threshold

    return {"stats": res, "passes": _is_failing(res)}


def make_fabric(aois, path_zip):
    # merge wbs that intersect (or touch?) aoi boundaries
    zipfiles = ["{}!data/{}/data/wb_all.gpkg".format(path_zip, aoi) for aoi in aois]
    wb_all = [(gpd.read_file(x).to_crs(3995)) for x in zipfiles]

    # see torchwbtype.features.shapely_properties
    wb_all_clean = []
    for gdf_sub in wb_all:
        gdf_sub["arearatio"] = [
            round(gdf_shapely.area / gdf_shapely.oriented_envelope.area, 3)
            for gdf_shapely in gdf_sub.geometry
        ]
        gdf_sub = gdf_sub[gdf_sub["arearatio"] > 0.07]
        wb_all_clean.append(gdf_sub)
    wb_all = wb_all_clean

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
    aois_in_order = []
    for aoi in aois:
        aois_in_order.append(
            list(
                itertools.compress(flist_aoi_tifs, [aoi in ff for ff in flist_aoi_tifs])
            )[0]
        )
    flist_aoi_tifs = aois_in_order

    def get_tif_bbox(fname, aoi):
        crs = str(xr.open_dataset(fname, engine="rasterio").rio.crs).split(":")[1]
        bounds = xr.open_dataset(fname, engine="rasterio").rio.bounds()
        return gpd.GeoDataFrame(
            {"aoi": aoi}, geometry=[box(*bounds)], index=[0], crs=crs
        ).to_crs(3995)

    aoi_bboxs = [get_tif_bbox(flist_aoi_tifs[i], aois[i]) for i in range(len(aois))]
    # # get all pairs of touching aoi boundaries
    aoi_bboxs_gdf = gpd.GeoDataFrame(pd.concat(aoi_bboxs))
    aoi_pairs = aoi_bboxs_gdf.sjoin(
        aoi_bboxs_gdf[["aoi", "geometry"]], how="left", predicate="overlaps"
    )[["aoi_left", "aoi_right"]]
    swap = aoi_pairs["aoi_left"] < aoi_pairs["aoi_right"]
    aoi_pairs.loc[swap, ["aoi_left", "aoi_right"]] = aoi_pairs.loc[
        swap, ["aoi_right", "aoi_left"]
    ].values
    aoi_pairs = aoi_pairs.drop_duplicates(subset=["aoi_left", "aoi_right"])
    aoi_pairs = aoi_pairs[~pd.isna(aoi_pairs["aoi_right"])]

    # ---
    pd.concat(aoi_bboxs).reset_index(drop=True).to_file(
        "test.gpkg", layer="aoi_boundaries"
    )
    wb_all_bbox.to_file("test.gpkg", layer="wb_all_bbox")
    pd.concat(wb_all).to_file("test.gpkg", layer="wb_all")
    # # mapview test.gpkg "aoi_boundaries,wb_all" ""
    # ---

    # generate on_boundary flag for wb(s) that touch aoi_boundaries
    for i in range(len(wb_all)):
        on_boundary = gpd.sjoin(
            wb_all[i], gpd.GeoDataFrame(geometry=[aoi_bboxs[i].exterior[0]], crs=3995)
        )[["id", "val"]]
        on_boundary["on_boundary"] = 1
        if on_boundary.shape[0] > 0:
            wb_all[i] = pd.merge(wb_all[i], on_boundary, how="left")
        else:
            wb_all[i]["on_boundary"] = 0
        wb_all[i]["on_boundary"] = wb_all[i]["on_boundary"].fillna(0)
    # # debugging
    # test2 = wb_all[i][wb_all[i]["on_boundary"] == 1]
    # test2.to_file("test.gpkg", layer="on_boundary")
    # # mapview test.gpkg "aoi_boundaries,on_boundary" ""
    # for i in range(len(wb_all)):
    #     if wb_all[i][wb_all[i]["on_boundary"] == 1].shape[0] > 0:
    #         wb_all[i][wb_all[i]["on_boundary"] == 1].to_file(
    #             "test.gpkg", layer="on_boundary" + str(i)
    #         )
    # ---

    for i in range(aoi_pairs.shape[0]):
        # i = 0
        # 1. for each aoi pair, evaluate those with an "on_boundary" flag for touching
        left_idx = int(
            np.where(
                [aoi_pairs.iloc[[i]]["aoi_left"].values[0] == aoi for aoi in aois]
            )[0][0]
        )
        right_idx = int(
            np.where(
                [aoi_pairs.iloc[[i]]["aoi_right"].values[0] == aoi for aoi in aois]
            )[0][0]
        )
        left_on_boundary = wb_all[left_idx][wb_all[left_idx]["on_boundary"] == 1]
        right_on_boundary = wb_all[right_idx][wb_all[right_idx]["on_boundary"] == 1]
        on_boundary_aoi = left_on_boundary.sjoin(
            right_on_boundary
        )  # keeps left geom, throws away right

        # 2a. for those that share a date, remove the entire right aoi entry
        # TODO: a real evaluation, maybe keep right instead of left?
        date_sharing = on_boundary_aoi[
            on_boundary_aoi["date_left"] == on_boundary_aoi["date_right"]
        ].drop_duplicates()
        is_a_date_match = [
            date in [x for x in date_sharing["date_right"]]
            for date in wb_all[right_idx]["date"]
        ]
        # assert any(is_a_date_match)
        is_a_recurrence_match = [
            str(id_recurrence) in [str(x) for x in date_sharing["id_recurrence_right"]]
            for id_recurrence in wb_all[right_idx]["id_recurrence"]
        ]
        # assert any(is_a_recurrence_match)
        wb_all[right_idx] = wb_all[right_idx][
            [not (x and y) for (x, y) in zip(is_a_date_match, is_a_recurrence_match)]
        ]

        # 2b. for those that don't share a date, set the recurrence ids of the right aoi to the left
        not_date_sharing = on_boundary_aoi[
            on_boundary_aoi["date_left"] != on_boundary_aoi["date_right"]
        ]
        id_recurrence_map = not_date_sharing[
            ["id_recurrence_left", "id_recurrence_right"]
        ].drop_duplicates()
        id_recurrence_map = {
            x: y
            for (x, y) in zip(
                id_recurrence_map["id_recurrence_right"],
                id_recurrence_map["id_recurrence_left"],
            )
        }
        wb_all[right_idx]["id_recurrence"] = wb_all[right_idx]["id_recurrence"].replace(
            id_recurrence_map
        )
    # ---

    res = pd.concat(wb_all)
    res["area_post_fabric"] = res.area
    res.to_file("data/wb_fabric.gpkg")

    return res


# read selected aois from data/wb_all.zip
path_zip = "data/wb_all.zip"
# unzip -l data/wb_all.zip
run_cmd = (
    "unzip -l "
    + path_zip
    + " | sed '1,3d;$d' | sed '$d' | sort | tail -n +8 | awk '{ print $4 }'"
)
aois_in_zip = subprocess.run(run_cmd, stdout=subprocess.PIPE, shell=True)
aois_in_zip = [
    x.replace("data/", "").replace("/wb_all.gpkg", "")
    for x in aois_in_zip.stdout.decode("utf-8").split("\n")
]
aois_in_zip.sort()
aois_in_zip = list(itertools.compress(aois_in_zip, [len(x) > 0 for x in aois_in_zip]))
# aoi_health = [
#     pd.DataFrame(aoi_health_check(aoi, path_zip=path_zip)["stats"], index=[0])
#     for aoi in aois_in_zip
# ]
# pd.concat(aoi_health)

# aois = ["0670116", "0769611"]
# aois = ["0670116", "0670117"]
# aois = ["0669915", "0669916"]
aois = aois_in_zip[34:38]
make_fabric(aois, path_zip)
