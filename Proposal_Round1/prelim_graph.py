import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
codes_to_keep = [40085 , 48097]

intake_csv = pd.read_csv('Education.csv', encoding='ISO-8859-1')

sorted_df_1 = intake_csv[intake_csv['FIPS Code'].isin(codes_to_keep)]
sorted_df = sorted_df_1[sorted_df_1['Attribute'].str.contains('Percent of adults with a high school diploma only, \d{4}')]

sorted_df.to_csv("education_only_Winstar.csv", index = False)

income_csv = pd.read_csv('CAINC1__ALL_AREAS_1969_2022.csv', encoding='ISO-8859-1')
income_csv['GeoFIPS'] = income_csv['GeoFIPS'].str.replace('"', '')
income_csv['GeoFIPS'] = pd.to_numeric(income_csv['GeoFIPS'], errors='coerce')
income_csv = income_csv.dropna(subset=['GeoFIPS'])


soritng_county_income = income_csv[income_csv['GeoFIPS'].isin(codes_to_keep)]

soritng_county_income.to_csv("income_only_winstar.csv", index = False)
incomedf = pd.read_csv('income_only_winstar_percap.csv')
years = [year for year in range(1960, 2018)]
incomedf.columns = incomedf.columns.str.strip()
incomedf.columns = incomedf.columns.str.replace(r'\s+', ' ', regex=True)
#print(incomedf.columns.tolist())

incomedfset = incomedf[['GeoFIPS', 'GeoName','1969', '1970', '1971', '1972', '1973', '1974', '1975', '1976', '1977', '1978', '1979', '1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022']]
df_melted = incomedfset.melt(id_vars=['GeoFIPS', 'GeoName'], var_name='Year', value_name='Income')

soritng_county_income.set_index('GeoFIPS', inplace=True)
plt.figure(figsize=(12, 6))
fips_to_name = {
    40085: 'Love County',
    48097: 'Cooke'
}
df_melted['Description'] = df_melted['GeoFIPS'].map(fips_to_name)
sns.lineplot(data=df_melted, x='Year', y='Income', hue='Description', marker='o')

# Add title and labels
plt.xticks(rotation=45)  # Rotation for readability
plt.title('Per Capita Personal Income Over Years')
plt.xlabel('Year')
plt.ylabel('Income')
plt.tight_layout()
# Save the plot to a file
plt.savefig('Income_plot_Winstar.png', dpi=300, bbox_inches='tight')

###################EDUCATION

df_education = pd.read_csv('education_only_Winstar_andyear.csv')

df_education['Area name'] = df_education['FIPS Code '].map({40085: 'Love County', 48097: 'Cooke County'})

# Create a Seaborn lineplot
plt.figure(figsize=(12, 6))

# Plot with line markers
sns.lineplot(data=df_education, x='Year', y='Value       ', hue='Area name', marker='o')

# Set the labels for the plot
plt.xlabel('Year')
plt.ylabel('Highschool Only')
plt.title('Highschool Only Over Years by Area')

# Save the plot as a file
plt.savefig('Highschool_Only_over_years.png')

###############################################CRIME

df_crime = pd.read_csv('Winstar_community_Crime1960_2017.csv')

plt.figure(figsize=(12, 6))
df_crime['County Name'] = df_crime['fips_state_county_code'].map(fips_to_name)

# Plot with Seaborn
sns.lineplot(data=df_crime, x='year', y='total_sum', hue='County Name', marker='o')

# Set x-axis ticks to go by 1-year intervals
plt.xticks(rotation=45)  # Rotation for readability

# Set the labels and title
plt.xlabel('Year')
plt.ylabel('Total # of Crimes')
plt.title('Total # Of Crimes Across Years for Different FIPS Codes')

# Ensure everything fits within the figure area
plt.tight_layout()

# Save the plot as a file
plt.savefig('Crime_over_years.png')