# TODO: collect wb(s) from multiple wb_all aois
import pandas as pd
import geopandas as gpd

# read selected aois from data/wb_all.zip
path_zip = "data/wb_all.zip"
aois = ["0670116", "0769611"]
zipfiles = ["{}!data/{}/data/wb_all.gpkg".format(path_zip, aoi) for aoi in aois]
wb_all = pd.concat([gpd.read_file(x) for x in zipfiles])


def aoi_health_check():
    # check that the distribution and counts are not ridiculous
    return None

def make_fabric():
    # merge wbs that intersect (or touch?) aoi boundaries
    return None
