from flask import Flask, jsonify
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/recommend', methods=['GET'])
def get_recommendations():
    try:
        # Remplacez le chemin si nécessaire pour correspondre à l'emplacement exact de votre fichier JSON.
        data = pd.read_json("data/cleaned/programs_clustered.json")
        return jsonify(data.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
