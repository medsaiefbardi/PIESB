import pandas as pd
import os

# Chemins
CLEANED_DATA_DIR = "data/cleaned"
TRANSFORMED_DATA_DIR = "data/cleaned"

# Charger les fichiers nettoyés
programs_cleaned = os.path.join(CLEANED_DATA_DIR, "programs_cleaned.csv")
referentiel_cleaned = os.path.join(CLEANED_DATA_DIR, "referentiel_cleaned.csv")

programs_df = pd.read_csv(programs_cleaned)
referentiel_df = pd.read_csv(referentiel_cleaned)

programs_df["Competence_Count"] = programs_df["Competences"].apply(lambda x: len(eval(x)) if isinstance(x, str) else 0)
referentiel_df["Competence_Count"] = referentiel_df["Competences"].apply(lambda x: len(x.split(";")) if isinstance(x, str) else 0)

# Sauvegarder les fichiers transformés
os.makedirs(TRANSFORMED_DATA_DIR, exist_ok=True)
programs_transformed = os.path.join(TRANSFORMED_DATA_DIR, "programs_transformed.csv")
referentiel_transformed = os.path.join(TRANSFORMED_DATA_DIR, "referentiel_transformed.csv")

programs_df.to_csv(programs_transformed, index=False)
referentiel_df.to_csv(referentiel_transformed, index=False)

print(f"Fichiers transformés sauvegardés dans {TRANSFORMED_DATA_DIR}")
