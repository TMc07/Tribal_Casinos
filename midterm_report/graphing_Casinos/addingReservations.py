import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

counties = gpd.read_file("tl_2024_us_county/tl_2024_us_county.shp")
points_df = pd.read_csv("Master_set_09_30_24.csv")
reservations = gpd.read_file("tl_2024_us_aiannh/tl_2024_us_aiannh.shp")

# Create a GeoDataFrame for your points
geometry = gpd.points_from_xy(points_df['long2ndrun'], points_df['lat2ndrun'])
points_gdf = gpd.GeoDataFrame(points_df, geometry=geometry)

# Set CRS and convert to EPSG:3857 for counties, reservations, and points
points_gdf.set_crs(epsg=4326, inplace=True)
counties = counties.to_crs(epsg=3857)
reservations = reservations.to_crs(epsg=3857)
points_gdf = points_gdf.to_crs(epsg=3857)

contiguous_us = counties[(counties['STATEFP'] != '15') & (counties['STATEFP'] != '02')]

# Check for empty geometries
print(counties.is_empty.sum())  # Should be 0
print(points_gdf.is_empty.sum())  # Should be 0

# Create a color map for the revGroup categories
color_map = {
    1: 'violet',
    2: 'yellow',
    3: 'salmon',
    4: 'cyan'
}

# Plot without basemap
fig, ax = plt.subplots(figsize=(15, 10))
counties.plot(ax=ax, color='lightgrey', edgecolor='black')

# Plot points based on revGroup values
for group, color in color_map.items():
    # Filter points by revGroup and plot them
    points_gdf[points_gdf['revGroup'] == group].plot(ax=ax, marker='o', color=color, markersize=1, label=f'Group {group}')

# Set title and legend
ax.set_title("Points on U.S. Counties by revGroup")
ax.legend(title='Revenue Group')


# Create a plot
fig, ax = plt.subplots(figsize=(15, 10))

# Plot all the U.S. counties
counties.plot(ax=ax, color='lightgrey', edgecolor='black')

# Plot the reservations
reservations.plot(ax=ax, color='lightblue', edgecolor='black', alpha=0.5, linewidth=1)
points_gdf['color'] = points_gdf['revGroup'].map(color_map)

# Set title and axis limits
ax.set_title("Casino Locations in U.S. Counties by revGroup with Native American Reservations")

# Save the figure
plt.savefig("US_casinos_with_reservations_plot.png", dpi=300, bbox_inches='tight')