from flask import Flask
from flask_cors import CORS
from routes.competence_routes import competence_bp
from routes.suggestion_routes import suggestion_bp
from routes.referentiel_routes import referentiel_bp
from routes.similar_programs import similar_bp  

app = Flask(__name__)
CORS(app)

# Enregistrer les routes
app.register_blueprint(competence_bp, url_prefix="/competences")
app.register_blueprint(referentiel_bp, url_prefix="/referentiels")
app.register_blueprint(suggestion_bp, url_prefix="/suggestions")
app.register_blueprint(similar_bp,url_prefix="/similar-programs")

if __name__ == "__main__":
    app.run(debug=True)
