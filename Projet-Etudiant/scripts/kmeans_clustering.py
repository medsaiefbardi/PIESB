import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
import os

# Paths
CLEANED_DATA_PATH = (
    "C:/Users/Skander/Desktop/Projet-Etudiant/data/processed/updated_cleaned_data.csv"
)
OUTPUT_PLOTS_PATH = "./outputs/clustering_plots/"


# Create necessary directories
def create_directories():
    os.makedirs(OUTPUT_PLOTS_PATH, exist_ok=True)
    os.makedirs("./data/processed", exist_ok=True)


# Load the cleaned dataset
def load_cleaned_data(file_path):
    try:
        data = pd.read_csv(file_path)
        print("Cleaned data loaded successfully! Shape:", data.shape)
        return data
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None


# Handle outliers in the dataset
def handle_outliers(data):
    print("\n--- Handling Outliers ---\n")
    initial_shape = data.shape

    # Remove rows where 'moy_bac' > 20
    data = data[data["moy_bac"] <= 20]
    print(f"Removed outliers. Shape before: {initial_shape}, after: {data.shape}")
    return data


# Preprocess the data for clustering
def preprocess_data(data):
    print("\n--- Preprocessing Data ---\n")

    # Select features for clustering
    selected_features = ["moy_bac", "niveau_courant_et", "gouvernorat"]
    data = data[selected_features]

    # One-hot encode categorical features (e.g., gouvernorat)
    categorical_features = ["gouvernorat"]
    numerical_features = ["moy_bac", "niveau_courant_et"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numerical_features),
            ("cat", OneHotEncoder(), categorical_features),
        ]
    )

    # Transform the data
    data_transformed = preprocessor.fit_transform(data)
    print(
        "Data preprocessing completed. Shape of transformed data:",
        data_transformed.shape,
    )
    return data_transformed


# Perform K-Means clustering
def perform_kmeans(data, n_clusters):
    print(f"\n--- Performing K-Means with {n_clusters} clusters ---\n")
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(data)
    print("Clustering completed.")
    return clusters, kmeans


# Visualize clustering results using PCA
def visualize_clusters_pca(data, clusters):
    print("\n--- Visualizing Clusters with PCA ---\n")
    pca = PCA(n_components=2)
    reduced_data = pca.fit_transform(data)

    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        x=reduced_data[:, 0],
        y=reduced_data[:, 1],
        hue=clusters,
        palette="viridis",
        s=100,
    )
    plt.title("K-Means Clustering with PCA")
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.legend(title="Cluster")
    plt.savefig(os.path.join(OUTPUT_PLOTS_PATH, "kmeans_clusters_pca.png"))
    plt.show()
    print("PCA-based clustering visualization saved.")


if __name__ == "__main__":
    # Step 1: Create directories
    create_directories()

    # Step 2: Load cleaned data
    cleaned_data = load_cleaned_data(CLEANED_DATA_PATH)

    if cleaned_data is not None:
        # Step 3: Handle outliers
        cleaned_data = handle_outliers(cleaned_data)

        # Step 4: Preprocess the data
        processed_data = preprocess_data(cleaned_data)

        # Step 5: Perform K-Means clustering
        n_clusters = 3  # Specify the number of clusters
        clusters, kmeans_model = perform_kmeans(processed_data, n_clusters)

        # Step 6: Add cluster labels to the dataset
        cleaned_data["Cluster"] = clusters
        print("Cluster labels added to the dataset.")

        # Step 7: Save the clustered data
        cleaned_data.to_csv("./data/processed/clustered_data.csv", index=False)
        print("Clustered data saved successfully!")

        # Step 8: Visualize clustering results using PCA
        visualize_clusters_pca(processed_data, clusters)
