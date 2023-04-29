import pandas as pd
import geopandas as gpd
import folium 
import matplotlib.pyplot as plt

#from pysal.lib import weights  
import segregation as seg

import folium 
import matplotlib.pyplot as plt
from pysal.lib import weights  
import segregation as seg
from IPython.display import display

single_var_1 = "j_1979_1995"
single_var_2 = "we_housing_cooperative"
total_pop_var = "households_total_units"


df_zensus_bremen[total_pop_var] = df_zensus_bremen[total_pop_var].astype(int) # do this in utils
df_zensus_bremen[single_var_1] = df_zensus_bremen[single_var_1].astype(int)
df_zensus_bremen[single_var_2] = df_zensus_bremen[single_var_2].astype(int)

# A-spatial segregation index     
int1 = seg.singlegroup.Interaction(data = df_zensus_bremen, group_pop_var = single_var_1, total_pop_var = total_pop_var)
int2 = seg.singlegroup.Interaction(data = df_zensus_bremen, group_pop_var = single_var_2, total_pop_var = total_pop_var)

print("Interaction of owner category %s: %.2f and Interaction of owner category %s: %.2f" %(single_var_1, int1.statistic, single_var_2, int2.statistic))


zensus_bremen_grid = gpd.read_file("D:/ifo_hack/ifoHack_DLR_Challenge_Data/2 Zensus/Zensus_Bremen_Grid_100m.gpkg")
idx_column = "Grid_Code"


wr = weights.contiguity.Queen.from_dataframe(zensus_bremen_grid, geom_col = "geometry", ids = idx_column )    
zensus_bremen_grid_copy = zensus_bremen_grid[~zensus_bremen_grid[idx_column].isin(wr.islands)].copy()

m = zensus_bremen_grid.explore(height=500, width=1000, color="gray", name="Zensus Grid Cells 100mx100m")
m = zensus_bremen_grid_copy.explore(m=m, color="blue", name="Zensus Grid Cells (filtered)")

folium.LayerControl().add_to(m)
plt.show()


dint1 = seg.singlegroup.DistanceDecayInteraction(data = zensus_bremen_grid_copy, group_pop_var = single_var_1, total_pop_var = total_pop_var)
dint2 = seg.singlegroup.DistanceDecayInteraction(data = zensus_bremen_grid_copy, group_pop_var = single_var_2, total_pop_var = total_pop_var)
    
print("Interaction (spatial) of age category %s: %.2f and Interaction (spatial) of age category %s: %.2f" %(single_var_1, dint1.statistic, 
                                                                                                            single_var_2, dint2.statistic))

zensus_bremen_grid_copy[single_var_1 + "_perc"] = [x * 100 / y if y != 0 else 0 for (x,y) in zip(zensus_bremen_grid_copy[single_var_1], zensus_bremen_grid_copy[total_pop_var])]
 
m = zensus_bremen_grid_copy.explore(height=500, width=1000, name="Seniors > 65yo",
                             column = single_var_1 + "_perc", scheme = "EqualInterval", cmap = "inferno", legend = True)


folium.LayerControl().add_to(m)
display(m)