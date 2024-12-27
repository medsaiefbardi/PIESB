from flask import Blueprint, jsonify, request
from models.recommendations import load_data, get_recommendations

competence_bp = Blueprint("competences", __name__)

# Charger les données une fois au démarrage
data_path = "../data/cleaned/programs_clustered.json"
data = load_data(data_path)

@competence_bp.route("/recommend", methods=["GET"])
def recommend():
    competence = request.args.get("competence")
    if not competence:
        return jsonify({"error": "Veuillez fournir une compétence pour la recherche"}), 400
    try:
        recommendations = get_recommendations(data, competence)
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

