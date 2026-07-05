import pandas as pd
import sqlite3
import os
import urllib.request

def download_data(url, output_path):
    print(f"Downloading data from {url}...")
    urllib.request.urlretrieve(url, output_path)
    print("Download complete.")

def main():
    # File paths
    url = 'https://raw.githubusercontent.com/treselle-systems/customer_churn_analysis/master/WA_Fn-UseC_-Telco-Customer-Churn.csv'
    raw_data_path = 'raw_churn.csv'
    db_path = 'churn.db'
    queries_path = 'queries/cleaning_queries.sql'
    cleaned_data_path = 'cleaned_churn.csv'

    # 1. Download data
    if not os.path.exists(raw_data_path):
        download_data(url, raw_data_path)
    
    print("Loading data into pandas...")
    df = pd.read_csv(raw_data_path)

    # 2. Connect to SQLite and load raw data
    print("Connecting to SQLite and loading raw data...")
    conn = sqlite3.connect(db_path)
    df.to_sql('raw_churn', conn, if_exists='replace', index=False)

    # 3. Execute SQL cleaning script
    print("Executing SQL cleaning script...")
    with open(queries_path, 'r') as f:
        sql_script = f.read()

    # SQLite script execution can handle multiple statements with executescript
    cursor = conn.cursor()
    cursor.executescript(sql_script)
    conn.commit()

    # 4. Extract cleaned data and save for the ML layer
    print("Extracting cleaned data...")
    cleaned_df = pd.read_sql_query("SELECT * FROM churn_cleaned", conn)
    cleaned_df.to_csv(cleaned_data_path, index=False)
    print(f"Cleaned data saved to {cleaned_data_path}")
    
    conn.close()

if __name__ == "__main__":
    main()
