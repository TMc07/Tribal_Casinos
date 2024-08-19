import pandas as pd

# Load the CSV file
df = pd.read_csv('tribal_casinos_TM_08_11_2024.csv')

# Add new columns with default values (you can customize these)
df['Seats'] = None
df['Open_Date'] = None
df['SquareFeet'] = None
df['Renovation_Expansion_completeDate'] = None
df['CasinoWebsiteLink'] = None
df['Cost'] = None

# Save the updated DataFrame to a new CSV file
df.to_csv('tribal_casinos_TM_08_11_2024_updated.csv', index=False)

print("New columns added and CSV file updated.")
