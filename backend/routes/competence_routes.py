import os
from flask import Blueprint, jsonify, request
import pandas as pd

competence_bp = Blueprint("competences", __name__)

# Load data files once at startup
PROGRAMS_PATH = os.path.join(os.path.dirname(__file__), "../data/cleaned/programs.json")
METIERS_PATH = os.path.join(os.path.dirname(__file__), "../data/cleaned/referentiel.json")

try:
    programs_data = pd.read_json(PROGRAMS_PATH)
    metiers_data = pd.read_json(METIERS_PATH)
except Exception as e:
    raise FileNotFoundError(f"Erreur lors du chargement des fichiers JSON : {e}")

@competence_bp.route("/recommend", methods=["GET"])
def recommend():
    competence = request.args.get("competence", "").lower()
    print(f"Received competence: {competence}")  # Log for the request

    try:
        # Filter programs based on the competence
        program_recommendations = programs_data[
            programs_data['Competences'].str.contains(competence, case=False, na=False)
        ]

        # Extract keywords from the competence string
        keywords = competence.split()

        print(f"Programs found: {len(program_recommendations)}")

        # Return both programs and métiers as a combined response
        response = {
            "programs": program_recommendations.to_dict(orient="records"),
            
        }
        return jsonify(response)

    except Exception as e:
        print(f"Error: {str(e)}")  # Log the error
        return jsonify({"error": str(e)}), 500
