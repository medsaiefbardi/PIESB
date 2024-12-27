import pandas as pd
import os
import json

CLEANED_DIR = "data/cleaned"
OUTPUT_DIR = "data/cleaned"

def generate_json():
    # Chemins des fichiers clusterisés
    programs_cleaned = os.path.join(CLEANED_DIR, "programs_cleaned.csv")
    referentiel_cleaned = os.path.join(CLEANED_DIR, "referentiel_cleaned.csv")

    # Chargement des données clusterisées
    programs_df = pd.read_csv(programs_cleaned)
    referentiel_df = pd.read_csv(referentiel_cleaned)

    # Création du répertoire de sortie si nécessaire
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Génération des fichiers JSON pour les programmes
    programs_output_file = os.path.join(OUTPUT_DIR, "programs.json")
    with open(programs_output_file, "w", encoding="utf-8") as f:
        json.dump(programs_df.to_dict(orient="records"), f, indent=4, ensure_ascii=False)

    # Génération des fichiers JSON pour le référentiel
    referentiel_output_file = os.path.join(OUTPUT_DIR, "referentiel.json")
    with open(referentiel_output_file, "w", encoding="utf-8") as f:
        json.dump(referentiel_df.to_dict(orient="records"), f, indent=4, ensure_ascii=False)

    print(f"Fichiers JSON générés avec succès :\n- {programs_output_file}\n- {referentiel_output_file}")

if __name__ == "__main__":
    generate_json()
