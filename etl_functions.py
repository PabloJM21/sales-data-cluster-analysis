import pandas as pd
import json
import os
from datetime import datetime

def extract_data(raw_data):
    # Collect the data in a list of dictionaries
    data = []
    for row in raw_data[1:]:  # Assuming raw_data[0] contains headers or irrelevant info
        data_type_code, seasonally_adj, category_code, cell_value, _, time, _ = row
        # Append each row's data as a dictionary
        data.append({
            "seasonally_adj": seasonally_adj,
            "data_type_code": data_type_code,
            "category_code": category_code,
            "cell_value": float(cell_value),
            "time": datetime.strptime(time, '%Y-%m')
        })

    # Create a DataFrame from the collected data
    return pd.DataFrame(data)

def transform_load_data(df):
    # Create a directory for the CSV files if it doesn't exist
    output_dir = 'data/processed'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Group by 'category_code' and create a CSV file for each group
    for category, group in df.groupby('category_code'):
        # Pivot the table for each unique category
        transformed_df = group.pivot(index='time', columns='data_type_code', values='cell_value')
        transformed_df.sort_index(inplace=True)

        # Save the transformed DataFrame to a CSV file
        file_path = os.path.join(output_dir, f'{category}_data.csv')
        transformed_df.to_csv(file_path)

        print(f"Data for {category} saved to {file_path}")




