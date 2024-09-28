import pandas as pd

ladlong = pd.read_csv('LadLong_finalAddress.csv', encoding='ISO-8859-1')

#print("this is ladlong",ladlong.columns)
casinoSpec = pd.read_csv('tribal_casinos_TM_09_28_2024.csv')

casinoSpec['State'] = casinoSpec['State '].str.strip()
casinoSpec['Casino_Name'] = casinoSpec['Casino_Name                                                 '].str.strip()
#print("This is casinoSpec",casinoSpec.columns)

ladlong_CasinoSpec = pd.merge(ladlong,casinoSpec, on = ['State ','Casino_Name                                                 '], how = 'inner')

#Going to remove extra stuff here
ladlong_CasinoSpec.drop(columns=['Address                                                               ','Work Phone   ','Work Fax                  ','Email Address                                                                         ','Casino_Name                                                 ', 'State ' ], inplace = True)


ladlong_CasinoSpec.to_csv('ladlong_CasinoSpec.csv', index = False)
print(ladlong_CasinoSpec.columns)

# Convert the 'fips_codes' column from string representation of lists to actual lists
ladlong_CasinoSpec['fips_codes'] = ladlong_CasinoSpec['fips_codes'].apply(lambda x: eval(x) if isinstance(x, str) else x)

# Use explode to create a new row for each FIPS code
ladlong_CasinoSpec_expandedbyFips = ladlong_CasinoSpec.explode('fips_codes')

# Verify the output
print(ladlong_CasinoSpec_expandedbyFips.head)

ladlong_CasinoSpec_expandedbyFips.to_csv("FipsCode_Expanded_set_09_28_24.csv",index=False)








##Going to start cutting the subsets of data to allow for merges to master