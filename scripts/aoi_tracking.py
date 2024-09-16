# python scripts/aoi_tracking.py --n_aois 2
import os
import glob
import argparse
import itertools
import geopandas as gpd

parser = argparse.ArgumentParser()
parser.add_argument("--n_aois", default=[1], nargs=1, type=int)
parser.add_argument("--return_incomplete", default=False, action="store_true")
args = parser.parse_args()
n_aois = args.n_aois[0]
return_incomplete = args.return_incomplete


def folder_exists(x):
    return os.path.exists("data/" + x)


def get_completed():
    res = glob.glob("data/*/data/wb_all.gpkg")
    res = [os.path.dirname(x).replace("data", "").replace("/", "") for x in res]
    return res


def get_todo(incomplete=False):
    # # read from shp
    todo = gpd.read_file(
        "data/CubeSat_Arctic_Boreal_LakeArea_1667/data/Yukon_Flats_Basin_Lakes/Yukon_Flats_Basin_Lakes.shp",
        dtype={"Tile": str},  # dtype specification does not work!!
    )
    todo = ["0" + str(x) for x in todo["Tile"].unique()]
    breakpoint()

    # # read from tifs
    # todo = glob.glob(
    #     "data/CubeSat_Arctic_Boreal_LakeArea_1667/data/Yukon_Flats_Basin-buffered_mask_*.tif"
    # )
    # todo = [
    #     x.replace(
    #         "data/CubeSat_Arctic_Boreal_LakeArea_1667/data/Yukon_Flats_Basin-buffered_mask_",
    #         "",
    #     ).replace(".tif", "")
    #     for x in todo
    # ]

    # write all todos to txt file
    os.remove("todos.txt")
    fl = open("todos.txt", "a")
    [fl.write(x + "\n") for x in todo]
    fl.close()

    if not incomplete:
        todo = [
            x
            for x in itertools.compress(
                todo, [not os.path.exists("data/" + x) for x in todo]
            )
        ]
    done = get_completed()
    not_done = [x for x in set(todo) - set(done)]

    if incomplete:
        f_exists = [folder_exists(x) for x in not_done]
        aoi_incomplete = [x for x in itertools.compress(not_done, f_exists)]
        return aoi_incomplete

    return not_done


todo = get_todo(return_incomplete)
if return_incomplete:
    for i in range(len(todo)):
        print("sbatch -J " + todo[i] + " sbatch.sh " + todo[i])
else:
    for i in range(n_aois):
        print("sbatch -J " + todo[i] + " sbatch.sh " + todo[i])
