# mamba activate C:\Users\jsta\miniconda3\envs\vote
import geopandas as gpd

from VotE import sql_ops as sops
from VotE import pg_table_metadata as pmd

bbox = gpd.read_file("data/bbox.gpkg")

sops.intersections(bbox.geometry.values[0], pmd.osm_rivers()).to_file(
    "data/osm.gpkg", driver="GPKG"
)
