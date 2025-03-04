import pandas as pd

input_file = 'TreatedSet_Ready2Merge_11_16_24.csv'  # Replace with your file name
output_prefix = 'TreatedSet_Part_'  # Prefix for output files
chunk_size = 1_000  # Number of rows per smaller CSV

# Split the CSV into smaller files
def split_csv(input_file, output_prefix, chunk_size):
    chunk_iter = pd.read_csv(input_file, chunksize=chunk_size, encoding='ISO-8859-1')
    file_index = 1  # Start file index

    for chunk in chunk_iter:
        output_file = f"{output_prefix}{file_index}.csv"
        chunk.to_csv(output_file, index=False)
        print(f"Saved: {output_file}")
        file_index += 1

# Execute the function
split_csv(input_file, output_prefix, chunk_size)

input_file = 'ControlSet_Ready2Merge_11_16_2024.csv'  # Replace with your file name
output_prefix = 'ControlSet_Part_'  # Prefix for output files
chunk_size = 1_000  # Number of rows per smaller CSV

# Split the CSV into smaller files
def split_csv(input_file, output_prefix, chunk_size):
    chunk_iter = pd.read_csv(input_file, chunksize=chunk_size, encoding='ISO-8859-1')
    file_index = 1  # Start file index

    for chunk in chunk_iter:
        output_file = f"{output_prefix}{file_index}.csv"
        chunk.to_csv(output_file, index=False)
        print(f"Saved: {output_file}")
        file_index += 1

# Execute the function
split_csv(input_file, output_prefix, chunk_size)

file_list = [
    'TreatedSet_Part_1.csv', 'TreatedSet_Part_2.csv', 'TreatedSet_Part_3.csv',
    'ControlSet_Part_1.csv', 'ControlSet_Part_2.csv', 'ControlSet_Part_3.csv',
    'ControlSet_Part_4.csv', 'ControlSet_Part_5.csv', 'ControlSet_Part_6.csv',
    'ControlSet_Part_7.csv', 'ControlSet_Part_8.csv', 'ControlSet_Part_9.csv',
    'ControlSet_Part_10.csv', 'ControlSet_Part_11.csv', 'ControlSet_Part_12.csv'
]
year_range = range(1970, 2018)  # Define the 30-year range

# Create a DataFrame for the year range
year_df = pd.DataFrame({'Year': year_range})
year_df['key'] = 1  # Add a key column for the cross join

# Process each file
for file in file_list:
    # Read the file
    print(f"Processing {file}...")
    df = pd.read_csv(file, encoding='ISO-8859-1')
    
    # Add a key column for the cross join
    df['key'] = 1
    
    # Perform the cross join with the year range
    expanded_df = pd.merge(df, year_df, on='key')
    expanded_df = expanded_df.drop('key', axis=1)  # Drop the key column
    
    # Save the expanded data back to the file
    expanded_file_name = file.replace('.csv', '_Expanded.csv')  # Add a suffix to indicate expansion
    expanded_df.to_csv(expanded_file_name, index=False)
    print(f"Saved expanded file: {expanded_file_name}")

    expanded_files = [
    'TreatedSet_Part_1_Expanded.csv', 'TreatedSet_Part_2_Expanded.csv', 'TreatedSet_Part_3_Expanded.csv',
    'ControlSet_Part_1_Expanded.csv', 'ControlSet_Part_2_Expanded.csv', 'ControlSet_Part_3_Expanded.csv',
    'ControlSet_Part_4_Expanded.csv', 'ControlSet_Part_5_Expanded.csv', 'ControlSet_Part_6_Expanded.csv',
    'ControlSet_Part_7_Expanded.csv', 'ControlSet_Part_8_Expanded.csv', 'ControlSet_Part_9_Expanded.csv',
    'ControlSet_Part_10_Expanded.csv', 'ControlSet_Part_11_Expanded.csv', 'ControlSet_Part_12_Expanded.csv'
]

# Output file for the merged dataset
output_file = 'CasinoSpec_byYear.csv'


# Create or overwrite the output file by appending data
with open(output_file, 'w') as f_out:
    for i, file in enumerate(expanded_files):
        print(f"Merging {file}...")
        df = pd.read_csv(file, encoding='ISO-8859-1')
        
        # For the first file, write the header
        if i == 0:
            df.to_csv(f_out, index=False)
        else:
            # Append to the file without writing the header again
            df.to_csv(f_out, index=False, header=False)


print(f"All files merged into {output_file}")
print(df.columns)
df = pd.read_csv('CasinoSpec_byYear.csv',encoding='ISO-8859-1')
print(df.columns)
df = df.rename(columns={'fips_codes_30_mile                                                                                                               ': 'GeoFIPS'})
df.to_csv('CasinoSpec_byYear.csv', index=False)