#!/usr/bin/env python
# coding: utf-8

# # Clustering Analysis
# This notebook focuses on analyzing and visualizing the clustering results.
# 
# ### Steps:
# 1. Load the clustered dataset.
# 2. Visualize clusters in 2D space.
# 3. Summarize and interpret the characteristics of each cluster.
# 

# # 2. Load Data

# In[1]:


import pandas as pd

# Path to the clustered dataset
CLUSTERED_DATA_PATH = "../data/processed/clustered_data.csv"

# Load the dataset
data = pd.read_csv(CLUSTERED_DATA_PATH)

# Display the first few rows
print(data.head())
print(f"Dataset shape: {data.shape}")


# ## 3. Visualizations
# a. Interactive Scatter Plot

# In[2]:


import pandas as pd
import plotly.express as px

# Path to the clustered dataset
CLUSTERED_DATA_PATH = "../data/processed/clustered_data.csv"

# Load the clustered dataset
data = pd.read_csv(CLUSTERED_DATA_PATH)

# Ensure the necessary columns are present
if 'moy_bac' not in data.columns or 'niveau_courant_et' not in data.columns or 'Cluster' not in data.columns:
    print("The required columns 'moy_bac', 'niveau_courant_et', and 'Cluster' are not available in the dataset.")
else:
    # Create the interactive scatter plot
    fig = px.scatter(
        data,
        x='moy_bac',  # Use moy_bac as the x-axis
        y='niveau_courant_et',  # Use niveau_courant_et as the y-axis
        color='Cluster',  # Cluster labels
        title='Clustering Visualization',
        labels={'moy_bac': 'Moy Bac', 'niveau_courant_et': 'Academic Level'},
        hover_data=['gouvernorat', 'resultat_annee_prec', 'sexe', 'classe_courante_et']
  # Add relevant columns to hover info
    )

    # Show the interactive plot
    fig.show()


# In[3]:


# Count the number of students in each cluster
cluster_sizes = data['Cluster'].value_counts()

# Create a bar chart
fig = px.bar(
    x=cluster_sizes.index,
    y=cluster_sizes.values,
    labels={'x': 'Cluster', 'y': 'Student Count'},
    title='Cluster Sizes',
    text=cluster_sizes.values
)

# Show the plot
fig.show()


# In[4]:


# Summarize key statistics for each cluster
cluster_summary = data.groupby('Cluster').agg({
    'moy_bac': ['mean', 'median'],
    'niveau_courant_et': lambda x: x.mode()[0],  # Most common academic level
    'gouvernorat': lambda x: x.mode()[0],  # Most common gouvernorat
}).reset_index()

# Display the summary
print("Cluster Characteristics Summary:")
print(cluster_summary)


# In[5]:


# Summarize key statistics for each cluster
cluster_summary = data.groupby('Cluster').agg({
    'moy_bac': ['mean', 'median'],
    'niveau_courant_et': lambda x: x.mode()[0],  # Most common academic level
    'gouvernorat': lambda x: x.mode()[0],  # Most common gouvernorat
}).reset_index()

# Rename columns for clarity
cluster_summary.columns = ['Cluster', 'Mean Moy Bac', 'Median Moy Bac', 'Most Common Academic Level', 'Most Common Gouvernorat']

# Display the summary
print("Cluster Characteristics Summary:")
print(cluster_summary)

