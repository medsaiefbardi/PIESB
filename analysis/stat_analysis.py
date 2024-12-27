import pandas as pd
from scipy.stats import f_oneway, pearsonr

CLEANED_DIR = "data/cleaned/"

def analyze_statistics():
    # Charger les fichiers nettoyés
    programs_df = pd.read_csv(f"{CLEANED_DIR}programs_cleaned.csv")
    referentiel_df = pd.read_csv(f"{CLEANED_DIR}referentiel_cleaned.csv")

    # Gérer les valeurs incorrectes ou manquantes pour `programs_df`
    programs_df = programs_df.dropna(subset=["Competences"])
    programs_df["Competence_Count"] = programs_df["Competences"].apply(
        lambda x: len(eval(x)) if isinstance(x, str) else 0
    )

    # Gérer les valeurs incorrectes ou manquantes pour `referentiel_df`
    referentiel_df = referentiel_df.dropna(subset=["Competences"])
    referentiel_df["Competence_Count"] = referentiel_df["Competences"].apply(
        lambda x: len(x.split(";")) if isinstance(x, str) else 0
    )

    # Afficher les tailles des deux DataFrames
    print(f"Taille de programs_df : {len(programs_df)}")
    print(f"Taille de referentiel_df : {len(referentiel_df)}")

    # Test ANOVA
    anova_result = f_oneway(programs_df["Competence_Count"], referentiel_df["Competence_Count"])
    print(f"Résultats ANOVA : {anova_result}")

    # Vérifier si les longueurs correspondent
    if len(programs_df) == len(referentiel_df):
        # Calcul de corrélation
        correlation, p_value = pearsonr(programs_df["Competence_Count"], referentiel_df["Competence_Count"])
        print(f"Corrélation : {correlation}, p-valeur : {p_value}")
    else:
        # Fournir une alternative si les longueurs diffèrent
        print("Les longueurs des DataFrames diffèrent. Calcul de statistiques descriptives.")
        print("Statistiques programs_df :")
        print(programs_df["Competence_Count"].describe())
        print("Statistiques referentiel_df :")
        print(referentiel_df["Competence_Count"].describe())

if __name__ == "__main__":
    analyze_statistics()
