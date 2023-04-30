from rasterio.plot import show
import rasterio
from rasterio.plot import show_hist



def f(p: str):
    """with rasterio.open(p) as image:
        image_array = image.read()
    show(image_array)"""
    ds = rasterio.open(p)
    show((ds, 1), cmap="Greens")
    """show_hist(ds, bins=50, lw=0.0, stacked=False, alpha=0.3,
      histtype='stepfilled', title="Histogram")"""


if __name__ == "__main__":
    cities = ["Berlin", "Bremen", "Dresden", "Frankfurt_am_Main", "Köln"]
    for city in cities:
        p = f"res/data/DLR/6 Sentinel/Sentinel_{city}.tif"
        print(p)
        df = f(p=p)
