import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import argparse

# Set up an ArgumentParser instance
parser = argparse.ArgumentParser(description="Perform clustering and PCA on sales data with optional orthogonal transformation.")

# Add argument for the number of clusters
parser.add_argument("--number_clusters", type=int, required=True, help="The number of clusters to form.")

# Add argument for the number of components
parser.add_argument("--number_components", type=int, required=True, help="The number of components to form.")

# Add argument for the optional orthogonal transformation
parser.add_argument('--standardize', action='store_true',
                    help="Apply category standardization")

# Parse arguments
args = parser.parse_args()

# Now both args.number_clusters and args.orthogonal_transform are available for use
print(f"Number of clusters: {args.number_clusters}")
print(f"Number of components: {args.number_components}")
print(f"Category standardization enabled: {args.standardize}")



data_dir = 'data/processed'
time_series_data = {}
start_pandemic = '2020-01-01'
for filename in os.listdir(data_dir):
    if filename.endswith('.csv'):
        filepath = os.path.join(data_dir, filename)
        # Load each CSV file
        df = pd.read_csv(filepath)
        # Set the 'time' column as the index for easier filtering
        df.set_index('time', inplace=True)
        df = df.loc[start_pandemic:].dropna()
        df.reset_index(inplace=True)
        df['ED'] = df['VS'] / df['NO']
        # Assuming the CSV has one column with the time series values
        branch_name = filename.split('.')[0]
        time_series_data[branch_name] = df['ED']  # Store the values as a numpy array







#Handle Missing Values
for branch in time_series_data:
    series = time_series_data[branch]
    # Fill NaN values with the mean of the series
    time_series_data[branch] = np.where(np.isnan(series), np.nanmean(series), series)

#Standardize data

df_time_series = pd.DataFrame(time_series_data)
df_time_series = df_time_series.transpose() # Transpose to make each branch a row
scaler = StandardScaler()
standardized_data = scaler.fit_transform(df_time_series)




if args.standardize:
    standardized_data = standardized_data.transpose()
    standardized_data = scaler.fit_transform(standardized_data)
    standardized_data = standardized_data.transpose()
    print("Branch standardization transformation applied.")


#Apply PCA
number_components=args.number_components
pca = PCA(n_components=number_components)
principal_components = pca.fit_transform(standardized_data)

# Create a DataFrame with the principal components
pca_df = pd.DataFrame(principal_components, columns=['PC1', 'PC2', 'PC3'], index=df_time_series.index)


#Analyze explained variance
explained_variance = pca.explained_variance_ratio_
print("Explained variance by each component:", explained_variance)
cumulative_explained_variance = np.cumsum(explained_variance)
print("Cumulative Explained Variance:", cumulative_explained_variance)

# Use the parsed argument in your clustering function
number_clusters = args.number_clusters
#Cluster the PCA transformed data
random_seed = 42
kmeans = KMeans(n_clusters=number_clusters, random_state=random_seed)  # Choose the number of clusters based on your analysis
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
if args.standardize:
    plt.savefig(f'ED_clusters_standardize.png')
else:
    plt.savefig(f'ED_clusters.png')

plt.show()




def plot_clusters(clusters, time_series_data, start_date, frequency='MS'):
    # Create a time index based on the start date and frequency
    time_index = pd.date_range(start=start_pandemic, periods=len(next(iter(time_series_data.values()))), freq=frequency)

    for cluster_id, branches in clusters.items():
        plt.figure(figsize=(12, 8))  # Set the figure size for each cluster plot

        # Plot each branch's ED time series within this cluster
        for branch in branches:
            # Check if the branch exists in the time series data
            if branch in time_series_data:
                plt.plot(time_index, time_series_data[branch], label=branch)

        # Adding title, legend, and labels
        plt.title(f'Effective Demand Time Series for Cluster {cluster_id}')
        plt.xlabel('Date')
        plt.ylabel('Effective Demand (ED)')
        plt.legend(loc='best')  # Place the legend in the best location
        plt.grid(True)  # Add grid lines to the plot
        plt.tight_layout()  # Automatically adjust subplot parameters to give specified padding
        if args.standardize:
            plt.savefig(f'ED_cluster{cluster_id}_standardize.png')
        else:
            plt.savefig(f'ED_cluster{cluster_id}.png')
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

plot_clusters(cluster_dict, time_series_data, start_pandemic)










