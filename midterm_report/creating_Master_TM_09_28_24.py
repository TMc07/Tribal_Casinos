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
#print(ladlong_CasinoSpec.columns)

# Convert the 'fips_codes' column from string representation of lists to actual lists
ladlong_CasinoSpec['fips_codes'] = ladlong_CasinoSpec['fips_codes'].apply(lambda x: eval(x) if isinstance(x, str) else x)

# Use explode to create a new row for each FIPS code
ladlong_CasinoSpec_expandedbyFips = ladlong_CasinoSpec.explode('fips_codes')

# Verify the output
#print(ladlong_CasinoSpec_expandedbyFips.head)

ladlong_CasinoSpec_expandedbyFips.to_csv("FipsCode_Expanded_set_09_28_24.csv",index=False)

#Going to expand the above set to the stfip year level

yeardf = pd.DataFrame({'Year': range(1960,2018)})

CasinoSpec_byYear = ladlong_CasinoSpec_expandedbyFips.merge(yeardf,how='cross')


CasinoSpec_byYear.to_csv('CasinoSpec_byYear.csv',index=False)

##Going to start cutting the subsets of data to allow for merges to master
##Education here
edu_set = pd.read_csv('Education.csv',encoding='ISO-8859-1')

#print(edu_set.columns)
edu_counts = edu_set[~edu_set['Attribute'].str.contains('Percent', na=False)]
edu_counts2 = edu_counts[~edu_counts['Attribute'].str.contains('Code', na=False)]

def assign_year(attribute):
    # Check for specific year patterns in the string
    if '1970' in attribute:
        return 1970
    elif '1980' in attribute:
        return 1980
    elif '1990' in attribute:
        return 1990
    elif '2000' in attribute:
        return 2000
    elif '2008-12' in attribute:
        return 2010
    elif '2018-22' in attribute:
        return 2017

edu_counts2['Year'] = edu_counts2['Attribute'].apply(assign_year)
edu_counts2.to_csv('education_by_decade.csv',index=False)

## Income Here
income_set = pd.read_csv('Income.csv',encoding='ISO-8859-1')
#print(income_set.columns)
income_set2 = income_set[income_set['LineCode'] != 1]
income_population = income_set2[income_set2['LineCode'] == 2].copy()
income_percap = income_set2[income_set2['LineCode'] == 3].copy()

income_pop_long = pd.melt(income_population, id_vars=['GeoFIPS', 'GeoName', 'Region', 'TableName'], 
                             var_name='Year', value_name='Population', value_vars=[str(year) for year in range(1969, 2023)])
#print(income_pop_long.columns)
income_percap_long = pd.melt(income_percap, id_vars=['GeoFIPS', 'GeoName', 'Region', 'TableName'],  
                         var_name='Year',  value_name='PerCapitaIncome',  value_vars=[str(year) for year in range(1969, 2023)])
#print(income_percap_long.columns)
income_set_Long = pd.merge(income_pop_long, income_percap_long, on = ['GeoFIPS', 'Year'], how='inner')

#print(income_set_Long.columns)
income_longfix = pd.DataFrame(income_set_Long)
income_longfix['GeoFIPS'] = income_longfix['GeoFIPS'].str.replace(r'["\s]','',regex=True)
income_longfix = income_longfix.drop(columns = ['Region_x','TableName_x','GeoName_y','Region_y','TableName_y'])
income_longfix.to_csv('Income_structured4Merge.csv',index=False)


## Doing Education Here

def categorize_education(attribute):
    if 'Less than a high school diploma' in attribute:
        return 'no_hs_degree'
    elif 'High school diploma' in attribute or 'Some college' in attribute or 'Four years of college' in attribute or "Bachelor's degree" in attribute:
        return 'hs_degree_or_more'

# def categorize_college_educ(attribute):
#     if 'Four years of college' in attribute or "Bachelor's degree" in attribute or 'Some college':
#         return 'college_experience'
    
# Apply the function to the 'Attribute' column to create 'education_level'
edu_counts2['education_level'] = edu_counts2['Attribute'].apply(categorize_education)

# edu_counts2['college_status'] = edu_counts2['Attribute'].apply(categorize_college_educ)

# 2. Group by 'Year' and 'education_level' to sum
education_newgroups = edu_counts2.groupby(['FIPS Code','Year', 'education_level'], as_index=False).agg({'Value': 'sum'})

education_newgroups = education_newgroups.pivot_table(index=['FIPS Code', 'Year'], 
                                           columns='education_level', 
                                           values='Value', 
                                           fill_value=0).reset_index()

education_newgroups.columns.name = None  # Remove the name of the columns index
education_newgroups.rename(columns={
    'hs_degree_or_more': 'hs_degree_or_more',
    'no_hs_degree': 'no_hs_degree'
}, inplace=True)

education_newgroups.to_csv('education_4merge.csv',index=False)
#Crime set done in stata opening it here
Crime_set = pd.read_csv('CrimeSet_collapsed_yearStfips_09_28_24.csv',encoding='ISO-8859-1')

### 
#Master Set Formation
###

# Education set is education_newgroups
# Income set is income_longfix
# Crime set is Crime_set
# Casino set is CasinoSpec_byYear

# print(education_newgroups.columns)
# print(income_longfix.columns)
# print(Crime_set.columns)
# print(CasinoSpec_byYear.columns)
yearexpansion = []
education_newgroups['Year'] = education_newgroups['Year'].astype(int)

for i, row in education_newgroups.iterrows():
    start_year = int(row['Year'])
    end_year = start_year + 9 
    for year in range(start_year, end_year + 1):
        yearexpansion.append({
            'FIPS Code': row['FIPS Code'],
            'Year': year,
            'hs_degree_or_more': row['hs_degree_or_more'],
            'no_hs_degree': row['no_hs_degree']
        })

education_newgroups = pd.DataFrame(yearexpansion)

education_newgroups.to_csv("removeme.csv")

education_newgroups = education_newgroups.rename(columns = {'FIPS Code':'GeoFIPS'})
Crime_set = Crime_set.rename(columns = {'year':'Year', 'fips_state_county_code':'GeoFIPS'})
CasinoSpec_byYear = CasinoSpec_byYear.rename(columns={'fips_codes':'GeoFIPS'})

#Converting datatypes
CasinoSpec_byYear['GeoFIPS'] = CasinoSpec_byYear['GeoFIPS'].astype(str)
education_newgroups['GeoFIPS'] = education_newgroups['GeoFIPS'].astype(str)
income_longfix['GeoFIPS'] = income_longfix['GeoFIPS'].astype(str)
Crime_set['GeoFIPS'] = Crime_set['GeoFIPS'].astype(str)

CasinoSpec_byYear['Year'] = CasinoSpec_byYear['Year'].astype(int)
education_newgroups['Year'] = education_newgroups['Year'].astype(int)
income_longfix['Year'] = income_longfix['Year'].astype(int)
Crime_set['Year'] = Crime_set['Year'].astype(int)

CasinoSpec_byYear['GeoFIPS'] = CasinoSpec_byYear['GeoFIPS'].astype(float).astype(int)
education_newgroups['GeoFIPS'] = education_newgroups['GeoFIPS'].astype(float).astype(int)
income_longfix['GeoFIPS'] = income_longfix['GeoFIPS'].astype(float).astype(int)
Crime_set['GeoFIPS'] = Crime_set['GeoFIPS'].astype(float).astype(int)

#have to fix the years I am using 
Crime_final_set = Crime_set[Crime_set['Year']>= 1970]
income_final_set1 = income_longfix[income_longfix['Year']>= 1970]
Casino_final_set1 = CasinoSpec_byYear[CasinoSpec_byYear['Year']>= 1970]
income_final_set = income_final_set1[income_final_set1['Year']<= 2017]
Casino_final_set = Casino_final_set1[Casino_final_set1['Year']<= 2017]
educ_final_set = education_newgroups[education_newgroups['Year']<= 2017]


print(Casino_final_set.dtypes)
print(educ_final_set.dtypes)
print(income_final_set.dtypes)
print(Crime_final_set.dtypes)

Master_set_09_28_24 = Casino_final_set.merge(educ_final_set, on=['Year',"GeoFIPS"], how = 'left').merge(income_final_set, on=['Year',"GeoFIPS"], how = 'left').merge(Crime_final_set, on=['Year',"GeoFIPS"], how = 'left')

Master_set_09_28_24.to_csv('Master_set_09_28_24.csv', index=False)