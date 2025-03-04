import pandas as pd


df = pd.read_csv('tribal_casinos_TM_09_05_2024_updated.csv')


df['Seats'] = None
df['Open_Date'] = None
df['SquareFeet'] = None
df['Renovation_Expansion_completeDate'] = None
df['CasinoWebsiteLink'] = None
df['Cost'] = None


print(df.columns)
df.to_csv('removeMe.csv', index=False)
address_set = df['Address                                                               ']
address_set.to_csv("addresses_savedOut.csv", index=False)
print("New columns added and CSV file updated.")
