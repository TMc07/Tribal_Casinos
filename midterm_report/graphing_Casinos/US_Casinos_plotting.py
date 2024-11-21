import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

counties = gpd.read_file("tl_2024_us_county/tl_2024_us_county.shp")
points_df = pd.read_csv("Master_set_09_30_24.csv")

#GeoDataFrame for points
geometry = gpd.points_from_xy(points_df['long2ndrun'], points_df['lat2ndrun'])
points_gdf = gpd.GeoDataFrame(points_df, geometry=geometry)
points_gdf.loc[points_gdf['seatsslots'] < 20, 'revGroup'] = 5

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
    4: 'cyan' ,
    5: 'red'
}

# Plot without basemap
fig, ax = plt.subplots(figsize=(15, 10))
counties.plot(ax=ax, color='lightgrey', edgecolor='black')

# Create a dictionary for custom labels
custom_labels = {
    1: "0-4 Million",
    2: "5-14 Million",
    3: "15-45 Million",
    4: "46-750 Million",
    5: "Gas Station Casino"
}

# Plot points based on revGroup values with custom labels
for group, color in color_map.items():
    label = custom_labels.get(group, f"Group {group}")  # Fetch custom label
    points_gdf[points_gdf['revGroup'] == group].plot(ax=ax, marker='o', color=color, markersize=1, label=label)

# Create custom legend handles with larger markers
legend_handles = [
    mpatches.Patch(color=color_map[group], label=label) 
    for group, label in custom_labels.items()
]
ax.legend(handles=legend_handles, title="Revenue Group", fontsize='medium', title_fontsize='large', handleheight=2.0, handlelength=2.0)

# Set axis limits to zoom in on the desired regions
ax.set_xlim(-2.0e7, -0.5)
ax.set_ylim(0.3, 1.2e7)

# Set title and axis limits
ax.set_title("Points in Western States by revGroup")

# Save the figure
plt.savefig("States_wReservations_Casino_plot.png", dpi=300, bbox_inches='tight')

## Doing Oklahoma
oklahoma_counties = counties[counties['STATEFP'] == '40']
oklahoma_points = points_gdf[points_gdf['state_x'] == 'OK']

fig, ax = plt.subplots(figsize=(10, 10))
oklahoma_counties.plot(ax=ax, color='lightgrey', edgecolor='black')

# Map the colors to the points
oklahoma_points['color'] = oklahoma_points['revGroup'].map(color_map)

# Plot points based on revGroup colors
oklahoma_points.plot(ax=ax, marker='o', color=oklahoma_points['color'], markersize=20)

# Set title and axis limits to zoom in on Oklahoma
ax.set_title("Points in Oklahoma by revGroup")
# Save the figure
plt.savefig("oklahoma_casinos_plot1.png", dpi=300, bbox_inches='tight')

## Doing Alaska
Alaska_counties = counties[counties['STATEFP'] == '02']
Alaska_points = points_gdf[points_gdf['state_x'] == 'AK']
ax.set_xlim(-2.0e7, -1)
ax.set_ylim(0.3, 1.2e7)

Alaska_counties.plot(ax=ax, color='lightgrey', edgecolor='black')

# Map the colors to the points
Alaska_points['color'] = Alaska_points['revGroup'].map(color_map)

# Plot points based on revGroup colors
Alaska_points.plot(ax=ax, marker='o', color=Alaska_points['color'], markersize=10)

# Set title and axis limits to zoom in on Alaska
ax.set_title("Points in Alaska by revGroup")
# Save the figure
plt.savefig("Alaska_casinos_plot.png", dpi=300, bbox_inches='tight')


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

plt.savefig("WesternUnion.png", dpi=300, bbox_inches='tight')


