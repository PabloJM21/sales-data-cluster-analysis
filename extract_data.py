import os
import requests
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment
API_KEY = os.getenv('DATAGOV_API_KEY')

# Base API endpoint
#endpoint = "http://api.census.gov/data/timeseries/eits/marts"
endpoint = "http://api.census.gov/data/timeseries/eits/advm3"

# Add the variables you want to retrieve in the 'get' parameter (without 'time')
years = ['2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022','2023','2024']

# Initialize an empty list to hold all data
all_data = []

for year in years:
    params = {
        'get': 'data_type_code,seasonally_adj,category_code,cell_value,time_slot_id',  # Specify valid variables
        'for': 'us',
        'time': year,  # Specify the time filter for each year
        'key': API_KEY  # Your API key
    }

    # Make the GET request to the API
    response = requests.get(endpoint, params=params)

    # Print the raw response text to diagnose the issue
    print("Raw Response:")
    print(response.text)

    # Check if the request was successful
    if response.status_code == 200:
        try:
            # Try to parse the JSON response
            data = response.json()
            print(f"Data extraction successful for year {year}!")

            # Check if this is the first year
            if len(all_data) == 0:
                # Include all data including headers
                all_data.extend(data)
            else:
                # Skip headers by excluding the first row (data[0])
                all_data.extend(data[1:])  # Append data without the headers





        except json.JSONDecodeError:
            print("Failed to parse JSON. Response might not be in JSON format.")
    else:
        print(f"Failed to fetch data for year {year}: {response.status_code}")
        print(response.text)

# Create the data directory if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

# Save all the collected data to a single JSON file
file_path = 'data/raw_data.json'
with open(file_path, 'w') as f:
    json.dump(all_data, f)

print(f"All data saved to '{file_path}'.")
