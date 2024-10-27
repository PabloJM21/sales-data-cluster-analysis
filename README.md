# ETL Pipeline for Manufacturers’ Shipments, Inventories, and Orders

This project is an ETL pipeline that extracts data from a public API and transforms it for better analysis.

The data extracted from the API corresponds to Manufacturers’ Shipments, Inventories, and Orders from the U.S. Census Bureau. 

A more accurate description of the dataset can be found here: https://api.census.gov/data/timeseries/eits/advm3.html.

The ETL pipeline is divided into two main stages:

1. **Raw data Extraction**:  
   Raw data is extracted from the U.S. Census Bureau API, covering the last five years of Manufacturers’ Shipments, Inventories, and Orders data. This data is stored in a JSON file for the next stage.

2. **Extraction, transformation and loading**:  
   The extracted data is filtered to retain only seasonally adjusted records containing the measurements (not percentual changes). The data is then reorganized such that the cell values are separated by time and data type, which are:   
   - Value of Shipments (VS)  
   - New Orders (NO)  
   - Unfilled Orders (UO)  
   - Total Inventories (TI)
  
   Finally, the data is saved into several csv files, each corresponding to a manufacture category. This categories are listed in 

   This structure allows for easy comparison of the evolution of monthly percentual changes across different manufacturing categories for each data type.

# Data variables

The data extracted contains the following variables:

- `data_type_code`: The code corresponding to the data types, starting with "MPC" for the montlhy percentual change.
- `seasonally_adj`: Denotes whether the outcome has been seasonally adjusted. 
- `category_code`: Indicates the manufacture category.
- `cell_value`: The outcome of the corresponding data type.
- `time`: Indicates the year and month. 






## Project Directory Structure

```plaintext
sales-data-etl/
├── data/
│   ├── raw_data.json                  # Raw data extracted from the API
│   └── processed/                     # Processed CSV files
│       ├── MPCVS_data.csv             # CSV file for Value of Shipments
│       ├── MPCNO_data.csv             # CSV file for New Orders
│       ├── MPCUO_data.csv             # CSV file for Unfilled Orders
│       └── MPCTI_data.csv             # CSV file for Total Inventories
│
├── extract_data.py                    # Script to extract the raw data from the API corresponding to the last 5 years
├── run_etl.py                         # Script for the etl pipeline. Filters, transforms and loads data into four csv files.

```

## Setup Instructions

### Prerequisites
- Python 3.8 or above
- MySQL 
- API Key from Data.gov (sign up [here](https://api.data.gov/signup/))

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/PabloJM21/sales-data-etl.git
    cd sales-data-etl
    ```

2. Install required Python libraries:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your environment variables:
    Create a `.env` file in the root directory and add your Data.gov API key:
    ```bash
    DATAGOV_API_KEY=your_api_key_here
    ```

4. Run the ETL pipeline:
    1. **Retrieve data** from the API:
       ```bash
       python extract_data.py
       ```
    2. **Extract, Transform and Load** the raw data:
       ```bash
       run_etl.py
       ```
