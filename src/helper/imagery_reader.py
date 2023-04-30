import rasterio
from rasterio.plot import show
import rasterio.mask
import fiona


def f(p: str, p2: str):
    raster = rasterio.open(p)
    show((raster, 3), cmap="Reds", title=p.rsplit(".tif")[0].rsplit("_")[1])


if __name__ == "__main__":
    cities = ["Berlin", "Bremen", "Dresden", "Frankfurt_am_Main", "Köln"]
    for city in cities:
        p = f"res/data/DLR/6 Sentinel/Sentinel_{city}.tif"
        # p = f"res/data/DLR/7 WorldCover/WorldCover_{city}.tif"
        p2 = f"res/data/DLR/3 Neighborhoods/Neighborhoods_{city}.gpkg"
        print(p)
        df = f(p=p, p2=p2)
