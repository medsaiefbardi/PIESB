import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

TRANSFORMED_DIR = "data/cleaned"

def visualize_data():
    programs_df = pd.read_csv(f"{TRANSFORMED_DIR}/programs_transformed.csv")
    referentiel_df = pd.read_csv(f"{TRANSFORMED_DIR}/referentiel_transformed.csv")

    # Visualisation : Histogrammes
    plt.figure(figsize=(12, 6))
    sns.histplot(programs_df["Competence_Count"], kde=True, label="Programs", color="blue")
    sns.histplot(referentiel_df["Competence_Count"], kde=True, label="Referentiel", color="orange")
    plt.legend()
    plt.title("Distribution des compétences par module")
    plt.show()
if __name__ == "__main__":
    visualize_data()
