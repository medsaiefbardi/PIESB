from flask import Blueprint, jsonify
import pandas as pd
import os

similar_bp = Blueprint("similar_programs", __name__)

# Path to the data files
PROGRAMS_PATH = os.path.join(os.path.dirname(__file__), "../data/cleaned/programs.json")
REFERENTIEL_PATH = os.path.join(os.path.dirname(__file__), "../data/cleaned/referentiel.json")

try:
    programs_data = pd.read_json(PROGRAMS_PATH)
    referentiel_data = pd.read_json(REFERENTIEL_PATH)
except Exception as e:
    raise FileNotFoundError(f"Error loading data: {e}")

@similar_bp.route("/", methods=["GET"])
def find_similar_programs():
    similar_programs = []
    try:
        # Find common competencies between programs and referentiel
        for _, program in programs_data.iterrows():
            program_competences = set(eval(program["Competences"]))
            for _, referentiel in referentiel_data.iterrows():
                referentiel_competences = set(eval(referentiel["Competences"]))
                common = program_competences & referentiel_competences  # Find intersection
                if common:
                    similar_programs.append({
                        "Program": program.to_dict(),
                        "Referentiel": referentiel.to_dict(),
                        "CommonCompetences": list(common)
                    })
        return jsonify(similar_programs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500