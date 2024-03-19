import sys
import pandas as pd


sys.path.append("scripts")
import utils

dt = pd.read_csv("data/query_ids_quality.txt", header=None)
dt.columns = ["image_id"]

def fmt_line(x):
    # x = dt.iloc[0].values[0]
    x_list = x.split("_")
    return "_".join(x_list[0:(len(x_list)-1)])

dt["image_id"] = [fmt_line(x) for x in dt["image_id"]]

utils.pdf_table(dt, path_pdf="figures/table_image-list.pdf", headers=["Image ID"], maxcolwidths=30)
