import pandas as pd

ladlong = pd.read_csv('Addresses_ladLong_30_100_mileRadius.csv', encoding='ISO-8859-1')

#print("this is ladlong",ladlong.columns)
casinoSpec = pd.read_csv('tribal_casinos_TM_11_19_2024.csv')
casinoSpec['ID'] = range(1,len(casinoSpec)+1)
print(casinoSpec.columns)

casinoSpec['State'] = casinoSpec['State '].str.strip()
casinoSpec['Casino_Name'] = casinoSpec['Casino_Name                                                 '].str.strip()


ladlong_CasinoSpec = pd.merge(ladlong,casinoSpec, on = ['State ','Casino_Name                                                 '], how = 'inner')

#Going to remove extra stuff here
ladlong_CasinoSpec.drop(columns=['Address                                                               ','Work Phone   ','Work Fax                  ','Email Address                                                                         ','Casino_Name                                                 ', 'State ' ], inplace = True)


ladlong_CasinoSpec.to_csv('ladlong_CasinoSpec.csv', index = False)
print(ladlong_CasinoSpec.columns)
ladlong['fips_codes_30_mile'] = ladlong['fips_codes_30_mile                                                                                                               '].str.strip()
print(ladlong.columns)
# Convert the 'fips_codes_30_mile' column from string representation of lists to actual lists
ladlong_CasinoSpec['fips_codes_30_mile                                                                                                               '] = ladlong_CasinoSpec['fips_codes_30_mile                                                                                                               '].apply(lambda x: eval(x) if isinstance(x, str) else x)

# Use explode to create a new row for each FIPS code
ladlong_CasinoSpec_expandedbyFips = ladlong_CasinoSpec.explode('fips_codes_30_mile                                                                                                               ')

ladlong_CasinoSpec_expandedbyFips.to_csv("FipsCode_Expanded_set_11_16_24.csv",index=False)

ladlong_CasinoSpec['casino_control_counties'] = ladlong_CasinoSpec['casino_control_counties'].apply(lambda x: eval(x) if isinstance(x, str) else x)
ladlong_CasinoSpec_expandedbyFips = ladlong_CasinoSpec.explode('casino_control_counties')
# Verify the output
print(ladlong_CasinoSpec_expandedbyFips.head)

ladlong_CasinoSpec_expandedbyFips.to_csv("FipsCode_ControlCounties_set_11_16_24.csv",index=False)


ControlSet = pd.read_csv('FipsCode_ControlCounties_set_11_16_24.csv', encoding='ISO-8859-1')
print(ControlSet.columns)
ControlSet = ControlSet.drop(columns = ['fips_codes_30_mile                                                                                                               '])
ControlSet.to_csv("ControlSet_Ready2Merge_11_16_2024.csv", index = False)
TreatedSet = pd.read_csv('FipsCode_Expanded_set_11_16_24.csv', encoding='ISO-8859-1')
print(TreatedSet.columns)
TreatedSet = TreatedSet.drop(columns=['casino_control_counties'])
TreatedSet.to_csv("TreatedSet_Ready2Merge_11_16_24.csv", index = False)