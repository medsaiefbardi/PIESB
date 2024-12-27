import os
from flask import Blueprint, jsonify, request
import pandas as pd

suggestion_bp = Blueprint("suggestions", __name__)

# Charger les données une seule fois au démarrage
DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/cleaned/programs_cleaned.csv")
try:
    competence_data = pd.read_csv(DATA_PATH)
    # Transformer les compétences en une liste exploitable
    competence_data["Competences"] = competence_data["Competences"].apply(eval)
except Exception as e:
    raise FileNotFoundError(f"Erreur lors du chargement du fichier CSV : {e}")

@suggestion_bp.route("/", methods=["GET"])
def suggest_competences():
    query = request.args.get("query", "").lower()
    print(f"Received query: {query}")  # Log de la requête
    try:
        if len(query) < 2:
            return jsonify([])  # Pas de suggestions pour les requêtes de moins de 3 caractères
        
        # Extraire toutes les compétences dans une seule liste
        all_competences = competence_data["Competences"].explode().dropna().unique()
        
        # Filtrer les compétences correspondant à la requête
        matching_suggestions = [comp for comp in all_competences if query in comp.lower()]
        print(f"Suggestions trouvées : {len(matching_suggestions)}")  # Log du résultat
        
        return jsonify(matching_suggestions)
    except Exception as e:
        print(f"Error: {str(e)}")  # Log de l'erreur
        return jsonify({"error": str(e)}), 500
