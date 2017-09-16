# coding: utf-8
import geopandas as gpd
import matplotlib
matplotlib.use('Agg') # Use the matplot display as a backend

import matplotlib.pyplot as plt # import after the use function

# matplotlib.rc('font', **font)
matplotlib.rcParams.update({'font.size': 1})


# Read the shape files into the dataframes
world = gpd.read_file('data/world_m.shp')
cities = gpd.read_file('data/cities.shp')

# normalize the crs of the cities
cities = cities.to_crs(world.crs)

cities['coords'] = cities['geometry'].apply(lambda x: x.representative_point().coords[:])
cities['coords'] = [coords[0] for coords in cities['coords']]
N = len(cities)
cmap = plt.cm.get_cmap('hsv', N+1)


# Save the figures
fig, ax = plt.subplots()
ax.set_aspect('equal')
# Plot the world with white bg and black edges
world.plot(ax=ax, edgecolor='black', linewidth=0.5)
cities.plot(ax=ax, marker='o',color='red', markersize=0.15)
# Annotate cities
for idx, row in cities.iterrows():
    plt.annotate(s=row['name'], xy=row['coords'], horizontalalignment='center', verticalalignment='top', color=cmap(idx))

# Save the damn map into pdf
plt.savefig('output/map.pdf')
