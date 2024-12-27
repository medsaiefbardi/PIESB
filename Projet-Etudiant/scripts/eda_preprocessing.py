# Enhanced EDA and Data Preprocessing Script with Logging

import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import logging

# Configure logging
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_PATH = os.path.join(PROJECT_ROOT, "logs")
os.makedirs(LOG_PATH, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_PATH, "eda_preprocessing.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Paths
RAW_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "raw", "Base Etudiant.xls")
PROCESSED_DATA_PATH = os.path.join(
    PROJECT_ROOT, "data", "processed", "updated_cleaned_data.csv"
)
EDA_PLOTS_PATH = os.path.join(PROJECT_ROOT, "outputs", "eda_plots")
EDA_TABLES_PATH = os.path.join(PROJECT_ROOT, "outputs", "eda_tables")


# Create necessary directories if they don't exist
def create_directories():
    os.makedirs(os.path.join(PROJECT_ROOT, "data", "processed"), exist_ok=True)
    os.makedirs(EDA_PLOTS_PATH, exist_ok=True)
    os.makedirs(EDA_TABLES_PATH, exist_ok=True)


# Load the dataset
def load_data(file_path):
    try:
        data = pd.read_excel(file_path)
        logging.info("Data loaded successfully! Initial shape: %s", data.shape)
        return data
    except FileNotFoundError:
        logging.error("Error: File not found at %s", file_path)
        return None


# Perform data quality checks
def data_quality_checks(data):
    logging.info("--- Data Quality Checks ---")
    logging.info("Shape of dataset: %s", data.shape)
    logging.info("Columns: %s", list(data.columns))
    logging.info("Missing values:\n%s", data.isnull().sum())
    logging.info("Duplicate rows: %d", data.duplicated().sum())


# Generate basic statistics
def generate_statistics(data):
    logging.info("--- Dataset Statistics ---")
    logging.info("%s", data.describe(include="all"))


# Visualize missing values
def visualize_missing_values(data):
    plt.figure(figsize=(10, 6))
    sns.heatmap(data.isnull(), cbar=False, cmap="viridis")
    plt.title("Missing Values Heatmap")
    plt.savefig(os.path.join(EDA_PLOTS_PATH, "missing_values_heatmap.png"))
    plt.close()
    logging.info("Missing values heatmap saved!")


# Visualize distributions of key variables
def visualize_distributions(data, column):
    plt.figure(figsize=(10, 6))
    sns.histplot(data[column], kde=True, color="blue")
    plt.title(f"Distribution of {column}")
    plt.xlabel(column)
    plt.ylabel("Frequency")
    plt.savefig(os.path.join(EDA_PLOTS_PATH, f"distribution_{column}.png"))
    plt.close()
    logging.info("Distribution plot for %s saved!", column)


# Clean and preprocess the dataset
def clean_data(data):
    logging.info("--- Starting Data Cleaning ---")
    initial_shape = data.shape

    # Remove duplicate rows
    data = data.drop_duplicates()
    logging.info("Removed duplicates. New shape: %s", data.shape)

    # Handle missing values
    data["lieu_nais_et"] = data["lieu_nais_et"].fillna("Inconnu")
    data["date_bac"] = pd.to_datetime(data["date_bac"], errors="coerce")
    data["moy_bac"] = data["moy_bac"].fillna(data["moy_bac"].mean())

    # Convert date columns to datetime
    for col in ["date_nais_et", "date_entree_esp_et"]:
        data[col] = pd.to_datetime(data[col], errors="coerce")

    # Fill remaining missing values
    data["resultat_annee_prec"] = data["resultat_annee_prec"].fillna("Inconnu")
    data["gouvernorat"] = data["gouvernorat"].fillna("Inconnu")
    data["classe_prec_et"] = data["classe_prec_et"].fillna("Non Applicable")
    data["classe_sem1"] = data["classe_sem1"].fillna("Non Assigné")

    # Drop the 'score_final' column if it exists
    if "score_final" in data.columns:
        data = data.drop(columns=["score_final"])
        logging.info("'score_final' column removed.")

    # Drop invalid rows
    data = data.dropna(subset=["etab_bac", "classe_courante_et"])

    logging.info("Final shape after cleaning: %s", data.shape)
    logging.info("Columns retained: %s", list(data.columns))

    return data


# Save cleaned data
def save_cleaned_data(data, path):
    if data is not None and not data.empty:
        try:
            data.to_csv(path, index=False)
            logging.info("Cleaned data saved successfully to %s", path)
        except Exception as e:
            logging.error("Error while saving data: %s", e)
    else:
        logging.warning("Data is empty or invalid. Nothing to save.")


if __name__ == "__main__":
    # Step 1: Create directories
    create_directories()

    # Step 2: Load the data
    data = load_data(RAW_DATA_PATH)

    if data is not None:
        # Step 3: Perform data quality checks
        data_quality_checks(data)

        # Step 4: Generate statistics
        generate_statistics(data)

        # Step 5: Visualize missing values
        visualize_missing_values(data)

        # Step 6: Visualize distributions (e.g., moy_bac)
        if "moy_bac" in data.columns:
            visualize_distributions(data, "moy_bac")

        # Step 7: Clean the data
        data = clean_data(data)

        # Step 8: Save the cleaned data
        save_cleaned_data(data, PROCESSED_DATA_PATH)

        logging.info("EDA and Data Preprocessing completed. Outputs saved.")
