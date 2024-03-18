# https://stackoverflow.com/a/35705477/3362993
# https://scitools.org.uk/cartopy/docs/v0.13/examples/tick_labels.html
# https://coolum001.github.io/cartopylayout.html

import numpy as np
import geopandas as gpd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from matplotlib import gridspec
import cartopy.feature as cfeature
from shapely.geometry import Point
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter


def scale_bar(ax, length=None, location=(0.5, 0.05), linewidth=3):
    """
    ax is the axes to draw the scalebar on.
    length is the length of the scalebar in km.
    location is center of the scalebar in axis coordinates.
    (ie. 0.5 is the middle of the plot)
    linewidth is the thickness of the scalebar.
    """
    llx0, llx1, lly0, lly1 = ax.get_extent(ccrs.PlateCarree())
    # Make tmc horizontally centred on the middle of the map,
    # vertically at scale bar location
    sbllx = (llx1 + llx0) / 2
    sblly = lly0 + (lly1 - lly0) * location[1]
    tmc = ccrs.TransverseMercator(sbllx, sblly)
    tmc_text = ccrs.TransverseMercator(sbllx, sblly - 0.03)
    # Get the extent of the plotted area in coordinates in metres
    x0, x1, y0, y1 = ax.get_extent(tmc)
    # Turn the specified scalebar location into coordinates in metres
    sbx = x0 + (x1 - x0) * location[0]
    sby = y0 + (y1 - y0) * location[1]

    # Calculate a scale bar length if none has been given
    if not length:
        length = (x1 - x0) / 5000  # in km
        ndim = int(np.floor(np.log10(length)))  # number of digits in number
        length = round(length, -ndim)  # round to 1sf

        # Returns numbers starting with the list
        def scale_number(x):
            if str(x)[0] in ["1", "2", "5"]:
                return int(x)
            else:
                return scale_number(x - 10**ndim)

        length = scale_number(length)

    # Generate the x coordinate for the ends of the scalebar
    bar_xs = [sbx - length * 500, sbx + length * 500]
    ax.plot(bar_xs, [sby, sby], transform=tmc, color="k", linewidth=linewidth)
    # print(sby)
    ax.text(
        sbx,
        sby,
        str(length) + " km",
        transform=tmc_text,
        horizontalalignment="center",
        verticalalignment="top",
    )

aoi = gpd.read_file("data/bbox.gpkg", driver="GPKG")
extent = (-145.5, -148, 64.5, 66.5)

plt.close()
# fig, axs = plt.subplots(1, 2)
ncol = 2
nrow = 1
fig = plt.figure(figsize=(ncol + 3, nrow + 3))
axes = gridspec.GridSpec(nrow, ncol, wspace=0.0, hspace=0.0, top=1, right=0.9)
ax = plt.subplot(axes[0], xlabel="", projection=ccrs.PlateCarree())
ax.set_extent(extent, ccrs.PlateCarree())
# ---
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.RIVERS)
ax.text(
    -147.723056 + 0.2,
    64.843611 + 0.08,
    s="Fairbanks",
    color="grey",
    fontsize=10,
    horizontalalignment="center",
    bbox={"alpha": 0, "edgecolor": "none"}    
)
fairbanks_pnt = gpd.GeoDataFrame(geometry=[Point(-147.723056, 64.843611)], crs = aoi.crs)
fairbanks_pnt.plot(ax=ax, color="black")
aoi.plot(ax=ax, color="red")

# ---
ax.set_xticks([-145.5, -148], crs=ccrs.PlateCarree())
ax.set_yticks([64.5, 65, 65.5, 66, 66.5], crs=ccrs.PlateCarree())
lon_formatter = LongitudeFormatter(zero_direction_label=True)
lat_formatter = LatitudeFormatter()
ax.xaxis.set_major_formatter(lon_formatter)
ax.yaxis.set_major_formatter(lat_formatter)
# ---
scale_bar(ax, location=(0.5, 0.06), length=100)
# ---
left = 0.46
bottom = 0.85
width = 0.04
height = 0.25
rect = [left, bottom, width, height]
ax2 = plt.axes(rect)
# ax2.text(0.5, 0.0, "\u25B2 \nN ", ha="center", fontsize=20, family="Arial", rotation=0)
ax2.axis("off")
# ---
aoi = gpd.read_file("data/bbox.gpkg", driver="GPKG")
aoi_bounds = [x for x in aoi.bounds.iloc[0]]
extent = (aoi_bounds[0], aoi_bounds[2], aoi_bounds[1], aoi_bounds[3])
wb = gpd.read_file("data/perl.gpkg", driver="GPKG")

ax2 = plt.subplot(axes[1], xlabel="", projection=ccrs.PlateCarree())
ax2.set_extent(extent, ccrs.PlateCarree())
aoi.plot(ax=ax2, alpha=0)
ax2.add_feature(cfeature.LAND)
ax2.add_feature(cfeature.RIVERS)
wb.plot(ax=ax2)

# ---
# plt.show()
plt.savefig("figures/study_site.pdf", bbox_inches="tight")
