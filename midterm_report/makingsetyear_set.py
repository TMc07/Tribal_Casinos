import pandas as pd

stfip = pd.read_csv('state_and_county_fips_master.csv',encoding='ISO-8859-1')
stfip_cleaned = stfip.dropna(subset=['state'])

#Going to expand the above set to the stfip year level
yeardf = pd.DataFrame({'Year': range(1970,2018)})
stfip_cleaned['key'] = 1
yeardf['key'] = 1

# Perform the cross join
decadeSt = pd.merge(stfip_cleaned, yeardf, on='key').drop('key', axis=1)

#decadeSt = stfip_cleaned.merge(yeardf,how='cross')
decadeSt.to_csv('stateYear.csv',index=False)

ladlong_CasinoSpec_expandedbyFips = pd.read_csv("FipsCode_Expanded_set_09_28_24.csv")

CasinoSpec_byYear = ladlong_CasinoSpec_expandedbyFips.merge(decadeSt,how='cross')

CasinoSpec_byYear.to_csv('CasinoSpec_byYear.csv',index=False)