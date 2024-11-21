import pandas as pd
import geopandas as gpd
import requests
import time
from shapely.geometry import Point

# Define the user-agent for the Nominatim API
USER_AGENT = "tribal_casinoSet_1.0"

# Step 1: Geocode an address using Nominatim API
def geocode_address(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': address,
        'format': 'json',
        'addressdetails': 1
    }
    headers = {
        'User-Agent': USER_AGENT
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        time.sleep(1)  # Delay to respect rate limits
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()
        if data:
            location = data[0]
            return location['lat'], location['lon']
        else:
            return None, None
    except requests.RequestException as e:
        print(f"Error during geocoding request: {e}")
        return None, None

# Step 2: Find counties within the radius
def get_counties_within_radius(lat, lon, radius_miles, gdf_counties):
    radius_degrees = radius_miles / 69.0  # Convert miles to degrees
    point = Point(lon, lat)
    buffered_point = point.buffer(radius_degrees)
    counties_within_radius = gdf_counties[gdf_counties.geometry.intersects(buffered_point)]
    return counties_within_radius

# Step 3: Extract FIPS codes
def get_fips_codes(counties_within_radius):
    return counties_within_radius['GEOID'].tolist()  # Replace 'GEOID' with the correct FIPS column name

# Step 4: Main function to process a CSV of addresses
def process_addresses_from_csv(input_csv, output_csv, gdf_counties):
    # Read CSV of addresses
    df_addresses = pd.read_csv(input_csv)
    
    # List to store results
    results = []

    # Iterate over each address
    for index, row in df_addresses.iterrows():
        address = row['Address                                                               ']  # Adjust column name if needed
        print(f"Processing address: {address}")
        
        lat, lon = geocode_address(address)
        if lat is not None and lon is not None:
            # Get counties within 30-mile radius
            counties_within_30 = get_counties_within_radius(lat, lon, 30, gdf_counties)
            fips_30 = get_fips_codes(counties_within_30)
            
            # Get counties within 100-mile radius
            counties_within_100 = get_counties_within_radius(lat, lon, 100, gdf_counties)
            fips_100 = get_fips_codes(counties_within_100)
            
            # Remove overlapping counties from 100-mile radius
            fips_control_counties = list(set(fips_100) - set(fips_30))
            
            results.append({
                'Address                                                               ': address,
                'latitude': lat,
                'longitude': lon,
                'fips_codes_30_mile': fips_30,
                'casino_control_counties': fips_control_counties
            })
        else:
            print(f"Could not geocode address: {address}")
            results.append({
                'Address                                                               ': address,
                'latitude': None,
                'longitude': None,
                'fips_codes_30_mile': None,
                'casino_control_counties': None
            })

    # Convert results to a DataFrame and save to CSV
    df_results = pd.DataFrame(results)
    df_results.to_csv(output_csv, index=False)
    print(f"Results saved to {output_csv}")

# Step 5: Load county boundaries
gdf_counties = gpd.read_file('cb_2018_us_county_500k/cb_2018_us_county_500k.shp')

# Step 6: Run the process on the input CSV file
process_addresses_from_csv('addresses_savedOut.csv', 'addresses_LatLong_FIPS.csv', gdf_counties)
