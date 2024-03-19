import sys
import pandas as pd


sys.path.append("scripts")
import utils

dt = pd.read_csv("data/torchwbtype_metrics.csv")
dt["description"]

utils.pdf_table(
    dt,
    path_pdf="figures/table_metric-list.pdf",
    maxcolwidths=50,
    headers=["Metric", "Description"],
)
