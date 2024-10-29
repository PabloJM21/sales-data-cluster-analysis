# Time series clustering for Manufacturers’ Shipments, Inventories, and Orders

This project consists of a clustering analysis on time series data corresponding to different manufacture categories. The goal is to compare different methods and find the most effective clustering technique, that attends to relevant features and performs meaningful data agrupations.

The data is extracted from a public API and corresponds to Manufacturers’ Shipments, Inventories, and Orders from the U.S. Census Bureau. 

A more accurate description of the dataset can be found here: https://api.census.gov/data/timeseries/eits/advm3.html.



## Data variables

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
├──images/                             # All generated images
│ 
├── extract_data.py                    # Script to extract the raw data from the API from the year 2000 until now
├── run_etl.py                         # Script for the etl pipeline. Filters, transforms and loads data into four csv files
├── etl_functions.py                   # Contains the functions for the etl pipeline
├── Clustering.py                      # Performs the cluster analysis
```

## Setup Instructions

### Prerequisites
- Python 3.8 or above
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

## Retrieve data and perform ETL

The ETL pipeline is divided into two main stages:

1. **Raw data Extraction**:  
   Raw data is extracted from the U.S. Census Bureau API, covering the 21st century of Manufacturers’ Shipments, Inventories, and Orders data. This data is stored in a JSON file for the next stage.

2. **Extraction, transformation and loading**:  
   The extracted data is filtered to retain only seasonally adjusted records containing the measurements (not percentual changes). The data is then reorganized such that the cell values are separated by time and data type. These data types are:   
   - Value of Shipments (VS)  
   - New Orders (NO)  
   - Unfilled Orders (UO)  
   - Total Inventories (TI)
  
   Finally, the data is saved into several csv files, each corresponding to a manufacture category. This categories can be found here: https://www.census.gov/econ/currentdata/dbsearch?programCode=M3ADV&startYear=1992&endYear=2024&categories[]=MDM&dataType=NO&geoLevel=US&adjusted=1&notAdjusted=1&errorData=0

   This structure allows for easy comparison of the evolution of the cell values of different data types for each manufacturing category.

   To perform the two stages of the ETL pipeline run the following commands:

1. **Retrieve data** from the API:
    ```bash
    python extract_data.py
    ```

2. **Extract, Transform and Load** the data for further analysis:
    ```bash
    python run_etl.py
    ```

## Clustering Analysis Setup
The goal of the analysis is to cluster the univariate time series of the effective demand across all categories. The effective demand (ED) is calculated using the following formula:


$$
\text{Effective Demand} = \frac{\text{Value of Shipments}}{\text{New Orders}}
$$


For feasability, we will take into account the data recorded since 2020.

The analysis consists of two main stages. Before these stages, a preliminary standardization can be applied to the time series data, which is done individually for each category. This preliminary transformation allows the clustering algorithm to focus on capturing similar trends in the data, regardless of differences in their values and amplitude.
This transformation can be applied enabling the `--standardize` parameter.


1. **Principal component analysis (PCA)**:  
   For dimensionality reduction. The number of components can be set through the `--number_components` parameter.
2. **K-means Clustering**:  
   Selected for the cluster analysis. The number of clusters can be set through the `--number_clusters` parameter.


To perform the clustering analysis on the data, run the following command:

```bash
python Clustering.py --number_clusters <NUMBER_OF_CLUSTERS> --number_components <NUMBER_OF_COMPONENTS> --standardize
```
This will generate one image displaying each category in the first two components of the PCA subspace, and one image for each cluster displaying the time series data of the effective demand of the categories involved.
In addition, the confirmation of the parameters chosen is printed to the terminal, along with the explained and cumulative explained variance of the principal components.

## Clustering Analysis Results
In order to compare the effect of the orthogonal transformation, I performed the analysis with 5 clusters and 3 principal components for the two different settings (with and without the transformation). The terminal output was as follows:


We will discuss the results attending to the generated images.

Clusters without transformation
![Clusters without transformation](/images/ED_clusters.png)

Clusters with transformation
![Clusters with transformation](/images/ED_clusters_orthogonal.png)
As we see, instead of including many categories in the same cluster (cluster 0), these are divided among two clusters (clusters 0 and 4).
These clusters capture series with significantly different features:

Time series data from cluster 0 for orthogonal transformation
![Clusters with transformation](/images/ED_cluster0_orthogonal.png)

Time series data from cluster 4 for orthogonal transformation
![Clusters with transformation](/images/ED_cluster4_orthogonal.png)

This happens because the transformation assigns category 34S to cluster 0, which exhibits a similar trend to the others but is shifted up. On the other hand, without the transformation it would have been assigned to its own cluster (cluster 4). So one cluster is lost and all other series from the last plots are assigned to the same cluster. 




In conclusion, the transformation effectively captures similar trends without comparing the values. This allows for a more meaningful cluster criteria and a more efficient way of using the clusters.