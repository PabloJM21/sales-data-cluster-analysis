import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt




data_dir = 'data/processed'
time_series_data = {}
time_series_data_plot = {}
start_date = '2020-01-01'
for filename in os.listdir(data_dir):
    if filename.endswith('.csv'):
        filepath = os.path.join(data_dir, filename)
        # Load each CSV file
        df = pd.read_csv(filepath)
        # Convert 'time' column to datetime
        #df['time'] = pd.to_datetime(df['time'])
        # Set the 'time' column as the index for easier filtering
        df.set_index('time', inplace=True)
        df = df.loc[start_date:].dropna()
        df.reset_index(inplace=True)
        print(df.head())
        df['ED']=(df['NO']-df['UO'])/(df['TI']+df['UO'])* (df['VS'] / df['NO'])
        # Assuming the CSV has one column with the time series values
        branch_name = filename.split('.')[0]
        time_series_data[branch_name] = df['ED']  # Store the values as a numpy array

        df_plot=pd.read_csv(filepath)
        df_plot['ED'] = (df_plot['NO'] - df_plot['UO']) / (df_plot['TI'] + df_plot['UO']) * (df_plot['VS'] / df_plot['NO'])
        branch_name = filename.split('.')[0]
        time_series_data_plot[branch_name] = df_plot['ED']





#Handle Missing Values
for branch in time_series_data:
    series = time_series_data[branch]
    # Fill NaN values with the mean of the series
    time_series_data[branch] = np.where(np.isnan(series), np.nanmean(series), series)

#Standardize data
df_time_series = pd.DataFrame(time_series_data)
df_time_series = df_time_series.transpose()  # Transpose to make each branch a row
scaler = StandardScaler()
standardized_data = scaler.fit_transform(df_time_series)


#Apply PCA
pca = PCA(n_components=2)  # Start with 2 components for visualization
principal_components = pca.fit_transform(standardized_data)

# Create a DataFrame with the principal components
pca_df = pd.DataFrame(principal_components, columns=['PC1', 'PC2'], index=df_time_series.index)


#Analyze explained variance
explained_variance = pca.explained_variance_ratio_
print("Explained variance by each component:", explained_variance)
cumulative_explained_variance = np.cumsum(explained_variance)
print("Cumulative Explained Variance:", cumulative_explained_variance)
#Cluster the PCA transformed data
kmeans = KMeans(n_clusters=3)  # Choose the number of clusters based on your analysis
clusters = kmeans.fit_predict(pca_df)
pca_df['Cluster'] = clusters


#Visualize clusters
plt.figure(figsize=(10, 8))
for cluster_id in np.unique(clusters):
    plt.scatter(pca_df[pca_df['Cluster'] == cluster_id]['PC1'],
                pca_df[pca_df['Cluster'] == cluster_id]['PC2'],
                label=f'Cluster {cluster_id}')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('Manufacturing Branch Clusters')
plt.legend()
#plt.savefig(f'effective_demand_clusters.png')
plt.show()

import matplotlib.pyplot as plt


# Assuming `clusters` is a dictionary with cluster IDs as keys and lists of branch names as values
# and `time_series_data` is a dictionary with branch names as keys and their ED time series data as values.

import matplotlib.pyplot as plt

def plot_clusters(clusters, time_series_data, start_date, frequency='MS'):
    # Create a time index based on the start date and frequency
    #time_index = pd.date_range(start=start_date, periods=len(next(iter(time_series_data.values()))), freq=frequency)
    time_index = pd.date_range(start='2000-01-01', periods=len(next(iter(time_series_data_plot.values()))), freq=frequency)

    for cluster_id, branches in clusters.items():
        plt.figure(figsize=(12, 8))  # Set the figure size for each cluster plot

        # Plot each branch's ED time series within this cluster
        for branch in branches:
            # Check if the branch exists in the time series data
            if branch in time_series_data:
                plt.plot(time_index, time_series_data_plot[branch], label=branch)

        # Adding title, legend, and labels
        plt.title(f'Effective Demand Time Series for Cluster {cluster_id}')
        plt.xlabel('Date')
        plt.ylabel('Effective Demand (ED)')
        plt.legend(loc='best')  # Place the legend in the best location
        plt.grid(True)  # Add grid lines to the plot
        plt.tight_layout()  # Automatically adjust subplot parameters to give specified padding
        #plt.savefig(f'effective_demand_cluster{cluster_id}.png')
        plt.show()  # Show the plot for the current cluster



# Call the function to generate the plots
from collections import defaultdict

# Suppose `branch_names` is a list of branch names corresponding to each label in `clusters`
# `clusters` is assumed to be a NumPy array where each element is a cluster label for each branch
cluster_dict = defaultdict(list)

# Read data and collect branch names
branch_names = []
for filename in os.listdir(data_dir):
    if filename.endswith('.csv'):
        branch_name = filename.split('.')[0]
        branch_names.append(branch_name)

# Populate the dictionary with branch names grouped by cluster labels
for branch, label in zip(branch_names, clusters):
    cluster_dict[label].append(branch)

# Now you can use the `cluster_dict` in the `plot_clusters` function

plot_clusters(cluster_dict, time_series_data, start_date)










