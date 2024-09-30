import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load the county shapefile
counties = gpd.read_file("tl_2024_us_county/tl_2024_us_county.shp")

# Step 2: Load your points dataset
# Assuming you have a CSV or DataFrame with 'longitude', 'latitude', and 'category' columns
points_df = pd.read_csv("Master_set_09_30_24.csv")

# Create a GeoDataFrame for your points
geometry = gpd.points_from_xy(points_df['long2ndrun'], points_df['lat2ndrun'])
points_gdf = gpd.GeoDataFrame(points_df, geometry=geometry)

contiguous_us = counties[(counties['STATEFP'] != '15') & (counties['STATEFP'] != '02')]
# Set CRS and convert to EPSG:3857
points_gdf.set_crs(epsg=4326, inplace=True)
counties = counties.to_crs(epsg=3857)
points_gdf = points_gdf.to_crs(epsg=3857)

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

# Set axis limits to zoom in on the desired regions
ax.set_xlim(-2.0e7, -0.5)  # Adjust these values based on your data range
ax.set_ylim(0.3, 1.2e7)        # Adjust these values based on your data range

# Save the figure
plt.savefig("us_casinos_plot_Grouping_one.png", dpi=300, bbox_inches='tight')


## Doing Oklahoma
oklahoma_counties = counties[counties['STATEFP'] == '40']
oklahoma_points = points_gdf[points_gdf['state_x'] == 'OK']

fig, ax = plt.subplots(figsize=(10, 10))
oklahoma_counties.plot(ax=ax, color='lightgrey', edgecolor='black')

# Map the colors to the points
oklahoma_points['color'] = oklahoma_points['revGroup'].map(color_map)

# Plot points based on revGroup colors
oklahoma_points.plot(ax=ax, marker='o', color=oklahoma_points['color'], markersize=10)

# Set title and axis limits to zoom in on Oklahoma
ax.set_title("Points in Oklahoma by revGroup")
# Save the figure
plt.savefig("oklahoma_casinos_plot.png", dpi=300, bbox_inches='tight')


#Western States
StateFipsList = ['08', '49', '32', '06', '04', '41', '53', '16', '30', '56','35']
StateAbrev = ['CO', 'UT', 'NV', 'CA', 'AZ', 'OR', 'WA', 'ID', 'MT','WY','NM']
fig, ax = plt.subplots(figsize=(15, 10))
# Plot each state on the same graph
# Loop through the states to plot the counties
for fips in StateFipsList:
    # Get counties for the state
    state_counties = counties[counties['STATEFP'] == str(fips)]

    # Plot the counties
    state_counties.plot(ax=ax, color='lightgrey', edgecolor='black')

# Now plot the points for all western states
for fips, abbrev in zip(StateFipsList, StateAbrev):
    # Get points for the state
    state_points = points_gdf[points_gdf['state_x'] == abbrev]

    # Map the colors to the points
    state_points['color'] = state_points['revGroup'].map(color_map)

    # Plot points based on revGroup colors
    state_points.plot(ax=ax, marker='o', color=state_points['color'], markersize=10)

# Set title and axis limits
ax.set_title("Points in Western States by revGroup")

# Save the figure
plt.savefig("West_States_casinos_plot.png", dpi=300, bbox_inches='tight')