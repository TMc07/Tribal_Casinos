import pandas as pd

# Read and clean the fips data
stfip = pd.read_csv('state_and_county_fips_master.csv', encoding='ISO-8859-1')
stfip_cleaned = stfip.dropna(subset=['state'])

# Create the year DataFrame
years = range(1970, 2018)

# Create a list of tuples combining each state with each year
combined_data = []
for _, row in stfip_cleaned.iterrows():
    for year in years:
        combined_data.append({'State': row['state'], 'fips_codes': row['fips'], 'Year': year})

# Create a DataFrame from the combined data
decadeSt = pd.DataFrame(combined_data)

# Save the result to a CSV file
decadeSt.to_csv('stateYear.csv', index=False)

# Read the expanded fips data
ladlong_CasinoSpec_expandedbyfips = pd.read_csv("FipsCode_Expanded_set_09_28_24.csv")

# Combine CasinoSpec data by year without cross join
CasinoSpec_byYear = ladlong_CasinoSpec_expandedbyfips.merge(decadeSt, on='fips_codes', how='outer')

# Save the combined result to a CSV file
CasinoSpec_byYear.to_csv('CasinoSpec_byYear.csv', index=False)
