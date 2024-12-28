import os
import pandas as pd
from flask import Blueprint, jsonify, request

referentiel_bp = Blueprint("referentiels", __name__)

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/cleaned/referentiel.json")
referentiel_data = pd.read_json(DATA_PATH)

@referentiel_bp.route("/related", methods=["GET"])
def get_related_metiers():
    program_keywords = request.args.get("keywords", "").lower().split(",")
    matching_metiers = referentiel_data[
        referentiel_data["Competences"].apply(
            lambda x: any(keyword in x.lower() for keyword in program_keywords)
        )
    ]
    return jsonify(matching_metiers.to_dict(orient="records"))
