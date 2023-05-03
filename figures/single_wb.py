# hydrolakes id: 398476
# glakes id: 2044484
# perl id: 1130
# wbextractor id: "28.0"
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import box

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
fig, axs = plt.subplots(2, 2) # , constrained_layout=True
ax1 = axs[0, 0]
ax2 = axs[0, 1]
ax3 = axs[1, 0]
ax4 = axs[1, 1]

bnds_gdf.plot(ax=ax1, color="white")
gpd_hydrolakes[gpd_hydrolakes["Hylak_id"] == 398476].plot(ax=ax1,edgecolor="black", facecolor="yellow")
ax1.set_title("HydroLAKES")
ax1.axis("off")
# extent = ax1.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
# fig.savefig("test.png", bbox_inches=extent.expanded(1.1, 1.2))

bnds_gdf.plot(ax=ax2, color="white")
gpd_perl[gpd_perl["id"] == 1130].plot(ax=ax2, edgecolor="black", facecolor="green")
ax2.set_title("PeRL")
ax2.axis("off")

bnds_gdf.plot(ax=ax3, color="white")
gpd_glakes[gpd_glakes["Lake_id"] == 2044484].plot(ax=ax3, edgecolor="black", facecolor="pink")
ax3.set_title("GLAKES")
ax3.axis("off")

bnds_gdf.plot(ax=ax4, color="white")
gpd_wbextractor[gpd_wbextractor["id"] == "28.0"].plot(ax=ax4, edgecolor="black", facecolor="blue")
ax4.set_title("wbextractor (this study)")
ax4.axis("off")

# plt.tight_layout()
plt.subplots_adjust(wspace=-0.2)
plt.savefig("figures/single_wb.png", bbox_inches="tight")
