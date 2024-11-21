import sqlite3
import pandas as pd

Treated = pd.read_csv('TreatedSet_Ready2Merge_11_16_24.csv', encoding='ISO-8859-1')
Control = pd.read_csv('ControlSet_Ready2Merge_11_16_2024.csv', encoding='ISO-8859-1')

def process_and_save_to_sqlite(dataset, database_name, table_name, chunk_size=5000):
    # Create a SQLite connection
    conn = sqlite3.connect(database_name)
    
    # Create the cursor object
    cur = conn.cursor()

    # Create a table for the dataset
    dataset.to_sql(table_name, conn, if_exists='replace', index=False)
    
    # Create the year dataframe
    yeardf = pd.DataFrame({'Year': range(1970, 2018)})
    yeardf['key'] = 1

    # Create the state FIPS dataframe
    stfip = pd.read_csv('state_and_county_fips_master.csv', encoding='ISO-8859-1')
    stfip_cleaned = stfip.dropna(subset=['state'])
    stfip_cleaned['key'] = 1

    # Save the cleaned state FIPS data to SQLite
    stfip_cleaned.to_sql('state_and_county_fips_master', conn, if_exists='replace', index=False)

    # Save the year dataframe to SQLite
    yeardf.to_sql('yeardf', conn, if_exists='replace', index=False)

    # Process in chunks to save memory
    for i in range(0, len(dataset), chunk_size):
        # Load the chunk from the dataset
        chunk = dataset.iloc[i:i + chunk_size]
        chunk['key'] = 1  # Add the key for cross join

        # Insert the chunk into the database
        chunk.to_sql(f'{table_name}_chunk', conn, if_exists='replace', index=False)

        # Perform the cross join with stfip and yeardf
        query = f"""
        SELECT a.*, b.*, c.Year
        FROM {table_name}_chunk AS a
        JOIN state_and_county_fips_master AS b ON a.key = b.key
        JOIN yeardf AS c ON a.key = c.key
        """
        
        # Execute the query and load the results into a new table
        result = pd.read_sql_query(query, conn)
        
        # Store the result into a new table
        result.to_sql(f'{table_name}_expanded', conn, if_exists='append', index=False)

    # Commit and close the connection
    conn.commit()
    conn.close()

# Process the Treated dataset
process_and_save_to_sqlite(Treated, 'casino_spec.db', 'treated')

# Process the Control dataset
process_and_save_to_sqlite(Control, 'casino_spec.db', 'control')