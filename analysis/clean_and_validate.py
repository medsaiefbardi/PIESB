import pandas as pd
import os
import ast

# Chemins vers les fichiers
RAW_DATA_DIR = "data/raw"
CLEANED_DATA_DIR = "data/cleaned"

def load_and_clean_data(file_name, column_name):
    # Charger les données
    file_path = os.path.join(RAW_DATA_DIR, file_name)
    df = pd.read_csv(file_path)

    # Nettoyer les données
    df[column_name] = df[column_name].str.strip().str.lower()
    df = df.drop_duplicates()
    df = df.dropna()

    return df

def clean_and_validate_referentiel(file_path):
    df = pd.read_csv(file_path)

    # Nettoyage des colonnes
    df["Competences"] = df["Competences"].fillna("").str.replace(r"; A PHP Error.*", "", regex=True)
    df["Metiers"] = df["Metiers"].fillna("").str.replace(r"; A PHP Error.*", "", regex=True)

    # Suppression des doublons
    df = df.drop_duplicates()

    # Validation des données
    df = df.dropna()

    return df
def clean_column(dataframe, column_name):
    def safe_eval(value):
        if isinstance(value, str):
            try:
                return ast.literal_eval(value)
            except (ValueError, SyntaxError):
                # Si la chaîne n'est pas une liste/dictionnaire, la transformer en liste d'une seule chaîne
                return [value.strip()]
        return []

    dataframe[column_name] = dataframe[column_name].apply(safe_eval)
    return dataframe

# Charger et nettoyer les données
programs_df = load_and_clean_data("programs.csv", "Competences")
if __name__ == "__main__":
    referentiel_file = os.path.join(RAW_DATA_DIR, "referentiel.csv")
    referentiel_cleaned_file = os.path.join(CLEANED_DATA_DIR, "referentiel_cleaned.csv")

    referentiel_df = clean_and_validate_referentiel(referentiel_file)
    referentiel_df = clean_column(referentiel_df, "Competences")

    referentiel_df.to_csv(referentiel_cleaned_file, index=False)
    print(f"Fichier nettoyé sauvegardé : {referentiel_cleaned_file}")

# Sauvegarder les fichiers nettoyés
programs_cleaned_path = os.path.join(CLEANED_DATA_DIR, "programs_cleaned.csv")

programs_df.to_csv(programs_cleaned_path, index=False)

print(f"Fichiers nettoyés sauvegardés dans {CLEANED_DATA_DIR}")
