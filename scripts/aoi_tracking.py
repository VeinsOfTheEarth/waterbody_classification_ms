# python scripts/aoi_tracking.py --n_aois 2
import os
import glob
import argparse
import itertools
import geopandas as gpd

parser = argparse.ArgumentParser()
parser.add_argument("--n_aois", default=[1], nargs=1, type=int)
args = parser.parse_args()
n_aois = args.n_aois[0]


def get_completed():
    res = glob.glob("data/*/data/wb_all.gpkg")
    res = [os.path.dirname(x).replace("data", "").replace("/", "") for x in res]
    return res


def get_todo():
    todo = gpd.read_file(
        "data/CubeSat_Arctic_Boreal_LakeArea_1667/data/Yukon_Flats_Basin_Lakes/Yukon_Flats_Basin_Lakes.shp",
        dtype={"Tile": str},  # dtype specification does not work!!
    )
    todo = ["0" + str(x) for x in todo["Tile"].unique()]
    todo = [
        x
        for x in itertools.compress(
            todo, [not os.path.exists("data/" + x) for x in todo]
        )
    ]
    done = get_completed()
    not_done = [x for x in set(todo) - set(done)]
    return not_done


todo = get_todo()
for i in range(n_aois):
    print("sbatch -J " + todo[i] + " sbatch.sh " + todo[i])
