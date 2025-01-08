# python scripts/aoi_tracking.py --n_aois 2
import os
import glob
import argparse
import itertools
import geopandas as gpd

parser = argparse.ArgumentParser()
parser.add_argument("--n_aois", default=[1], nargs=1, type=int)
parser.add_argument("--return_incomplete", default=False, action="store_true")
parser.add_argument("--staged_tifs", default=False, action="store_true")
args = parser.parse_args()
n_aois = args.n_aois[0]
return_incomplete = args.return_incomplete
staged_tifs = args.staged_tifs


def get_status(aoi, silent=False):
    # aoi = "0669517"
    res = {
        "folder_exists": folder_exists(aoi),
        "has_tifs": has_tifs(aoi),
        "has_masks": has_masks(aoi),
        "has_gpkgs": has_gpkgs(aoi),
        "has_csvs": has_csvs(aoi),
    }
    if any([not x for x in res.values()]) and not silent:
        print(res)

    return [x for x in res.values()]


def folder_exists(x):
    return os.path.exists("data/" + x)


def has_tifs(x):
    return len(glob.glob("data/" + x + "/data/tif/*.tif")) > 0


def has_masks(aoi):
    return len(glob.glob("data/" + aoi + "/data/mask/*.png")) > 0


def has_gpkgs(aoi):
    return len(glob.glob("data/" + aoi + "/data/gpkg/*.gpkg")) > 0


def has_csvs(aoi):
    return len(glob.glob("data/" + aoi + "/data/csv/*.csv")) > 0


def get_completed():
    res = glob.glob("data/*/data/wb_all.gpkg")
    res = [os.path.dirname(x).replace("data", "").replace("/", "") for x in res]
    return res


def get_todo(staged_tifs=False, return_incomplete=False):
    todo = gpd.read_file(
        "data/CubeSat_Arctic_Boreal_LakeArea_1667/data/Yukon_Flats_Basin_Lakes/Yukon_Flats_Basin_Lakes.shp",
        dtype={"Tile": str},  # dtype specification does not work!!
    )
    todo = ["0" + str(x) for x in todo["Tile"].unique()]

    # write all todos to txt file
    os.remove("todos.txt")
    fl = open("todos.txt", "a")
    [fl.write(x + "\n") for x in todo]
    fl.close()

    todo = [
        x
        for x in itertools.compress(
            todo,
            [not os.path.exists("data/" + x + "/data/wb_all.gpkg") for x in todo],
        )
    ]
    done = get_completed()
    not_done = [x for x in set(todo) - set(done)]

    if not return_incomplete and not staged_tifs:
        # if not return_incomplete, not staged tifs, return all not_done without wb_all.gpkg
        return not_done

    if return_incomplete and not staged_tifs:
        # if return_incomplete and not staged_tifs, return those with at least tifs
        not_done = list(itertools.compress(not_done, [has_tifs(x) for x in not_done]))
        return not_done

    if return_incomplete and staged_tifs:
        # if return_incomplete and staged_tifs, return those that have at least masks
        not_done = list(itertools.compress(not_done, [has_masks(x) for x in not_done]))
        return not_done

    # if not return_incomplete, and staged tifs:
    #   print those without tifs
    missing_tifs = list(
        itertools.compress(
            not_done, [not get_status(x, silent=True)[1] for x in not_done]
        )
    )
    for missing_tif in missing_tifs:
        print(missing_tif + " is missing tifs")

    #   return those without any after tifs
    return list(
        itertools.compress(
            not_done, [sum(get_status(x, silent=True)) == 2 for x in not_done]
        )
    )


# --- main ---
todo = get_todo(staged_tifs, return_incomplete)
if return_incomplete and staged_tifs:
    try:
        os.remove("preflight.txt")
    except:
        pass
    fl = open("preflight.txt", "a")
    [fl.write(x + "\n") for x in todo]
    fl.close()
    for i in range(len(todo)):
        aoi = todo[i]
        print("sbatch -J " + aoi + " sbatch.sh " + aoi)
        get_status(aoi)
else:
    if len(todo) > 0:
        for i in range(n_aois):
            print("sbatch -J " + todo[i] + " sbatch.sh " + todo[i])
