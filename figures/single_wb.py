# hydrolakes id: 398476
# glakes id: 2044484
# perl id: 1130
# wbextractor id: "28.0"
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import box
from matplotlib.gridspec import GridSpec

gpd_hydrolakes = gpd.read_file("data/hydrolakes.gpkg")
gpd_glakes = gpd.read_file("data/glakes.gpkg")
gpd_wbextractor = gpd.read_file("data/wbextractor.gpkg")
gpd_perl = gpd.read_file("data/perl.gpkg")
gpd_perl["id"] = [x for x in range(gpd_perl.shape[0])]

bnds = gpd_perl[gpd_perl["id"] == 1130].total_bounds
crs = gpd_perl.crs
bnds_gdf = gpd.GeoDataFrame({"idx": [1], "geometry": [box(*np.array(bnds))]}, crs=crs)

# ---
plt.close()
fig = plt.figure()
gs = GridSpec(2, 3, figure=fig)
# vertical, horizontal
ax1 = fig.add_subplot(gs[0:1, 0])
ax2a = fig.add_subplot(gs[0, 1])
ax2b = fig.add_subplot(gs[0, 2])
ax2c = fig.add_subplot(gs[1, 1])
ax2d = fig.add_subplot(gs[1, 2])

bnds_gdf.plot(ax=ax2a, color="white")
gpd_hydrolakes[gpd_hydrolakes["Hylak_id"] == 398476].plot(
    ax=ax2a, edgecolor="black", facecolor="yellow"
)
ax2a.set_title("HydroLAKES")
ax2a.axis("off")

bnds_gdf.plot(ax=ax2b, color="white")
gpd_perl[gpd_perl["id"] == 1130].plot(ax=ax2b, edgecolor="black", facecolor="green")
ax2b.set_title("PeRL")
ax2b.axis("off")

bnds_gdf.plot(ax=ax2c, color="white")
gpd_glakes[gpd_glakes["Lake_id"] == 2044484].plot(
    ax=ax2c, edgecolor="black", facecolor="pink"
)
ax2c.set_title("GLAKES")
ax2c.axis("off")

bnds_gdf.plot(ax=ax2d, color="white")
gpd_wbextractor[gpd_wbextractor["id"] == "28.0"].plot(
    ax=ax2d, edgecolor="black", facecolor="blue"
)
ax2d.set_title("wbextractor")
ax2d.axis("off")

image = plt.imread("figures/satview.png")
satview = ax1.imshow(image, extent=[0, 2, 2, 0])
ax1.set_title("Imagery (ESRI)", y=1.1)
ax1.axis("off")

# plt.tight_layout()
plt.subplots_adjust(wspace=0, hspace=0.35)

# --- lines
# horizontal
# line = plt.Line2D([0.5, 0.95], [0.4, 0.4], transform=fig.transFigure, color="black")
# fig.add_artist(line)
# # vertical
# line = plt.Line2D([0.7, 0.7], [0.7, 0.1], transform=fig.transFigure, color="black")
# fig.add_artist(line)

# --- arrows
# ax1.annotate("Test 2", xy=(0.5, 1.), xycoords=ax1,
#                   xytext=(0.5,1.1), textcoords=(ax1, "axes fraction"),
#                   va="bottom", ha="center",
#                   arrowprops=dict(arrowstyle="->"))

# ---
plt.savefig("figures/single_wb.pdf", bbox_inches="tight")
