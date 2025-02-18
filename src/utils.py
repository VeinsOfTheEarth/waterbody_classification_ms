import numpy as np
import geopandas as gpd
from shapely.geometry import box


def make_bbox_gdf(gdf, crs=3995):
    bnds = gdf.total_bounds
    in_crs = gdf.crs
    return gpd.GeoDataFrame({"idx": [1], "geometry": [box(*np.array(bnds))]}, crs=in_crs).to_crs(crs)
