import pandas as pd
from scipy.stats import f_oneway, pearsonr
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import matplotlib.pyplot as plt
import os
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

# Répertoires et modèles
CLEANED_DIR = "data/cleaned/"
OUTPUT_DIR = "output/"
EMBEDDING_MODEL = "paraphrase-MiniLM-L6-v2"  # Modèle d'embedding pour la similarité sémantique

# Liste de stopwords en français (peut être étendue)
FRENCH_STOPWORDS = set([
    "de", "des", "et", "à", "la", "le", "les", "un", "une", "dans", "par", "avec",
    "pour", "sur", "en", "au", "aux", "du", "ou", "qui", "que", "dont", "est", "à"
])

# Créer le répertoire de sortie s'il n'existe pas
os.makedirs(OUTPUT_DIR, exist_ok=True)

def remove_stopwords(text, stopwords):
    """
    Supprime les stopwords d'une chaîne de texte.
    """
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stopwords]
    return ' '.join(filtered_words)

def analyze_statistics():
    """
    Analyse statistique des compétences entre programs_df et referentiel_df.
    """
    # Charger les fichiers nettoyés
    programs_df = pd.read_csv(f"{CLEANED_DIR}programs_cleaned.csv")
    referentiel_df = pd.read_csv(f"{CLEANED_DIR}referentiel_cleaned.csv")

    # Gérer les valeurs incorrectes ou manquantes pour `programs_df`
    programs_df = programs_df.dropna(subset=["Competences"])
    programs_df["Competences"] = programs_df["Competences"].apply(
        lambda x: remove_stopwords(' '.join(eval(x)), FRENCH_STOPWORDS) if isinstance(x, str) else ''
    )
    programs_df["Competence_Count"] = programs_df["Competences"].apply(
        lambda x: len(x.split()) if isinstance(x, str) else 0
    )

    # Gérer les valeurs incorrectes ou manquantes pour `referentiel_df`
    referentiel_df = referentiel_df.dropna(subset=["Competences"])
    referentiel_df["Competences"] = referentiel_df["Competences"].apply(
        lambda x: remove_stopwords(' '.join(x.split(";")), FRENCH_STOPWORDS) if isinstance(x, str) else ''
    )
    referentiel_df["Competence_Count"] = referentiel_df["Competences"].apply(
        lambda x: len(x.split()) if isinstance(x, str) else 0
    )

    # Test ANOVA
    anova_result = f_oneway(programs_df["Competence_Count"], referentiel_df["Competence_Count"])
    print(f"Résultats ANOVA : Statistique = {anova_result.statistic:.2f}, p-valeur = {anova_result.pvalue:.2e}")

    # Visualisation des données
    plt.figure(figsize=(10, 6))
    plt.hist(programs_df["Competence_Count"], bins=20, alpha=0.5, label="Programs")
    plt.hist(referentiel_df["Competence_Count"], bins=20, alpha=0.5, label="Referentiel")
    plt.title("Distribution des Compétences (après suppression des stopwords)")
    plt.xlabel("Nombre de Compétences")
    plt.ylabel("Fréquence")
    plt.legend()
    plt.savefig(f"{OUTPUT_DIR}distribution_competences_cleaned.png")
    plt.close()
    print(f"Graphique des distributions sauvegardé : {OUTPUT_DIR}distribution_competences_cleaned.png")

    # Corrélation
    if len(programs_df) != len(referentiel_df):
        print("Les longueurs des DataFrames diffèrent. Utilisation de la taille minimale pour la corrélation.")
        min_length = min(len(programs_df), len(referentiel_df))
        truncated_programs = programs_df["Competence_Count"].iloc[:min_length]
        truncated_referentiel = referentiel_df["Competence_Count"].iloc[:min_length]
    else:
        truncated_programs = programs_df["Competence_Count"]
        truncated_referentiel = referentiel_df["Competence_Count"]

    correlation, p_value = pearsonr(truncated_programs, truncated_referentiel)
    print(f"Corrélation : {correlation:.2f}, p-valeur : {p_value:.2e}")

def compute_tfidf_similarity(list1, list2):
    """
    Calcule la similarité cosinus entre deux listes de compétences avec TF-IDF.
    """
    vectorizer = TfidfVectorizer(stop_words=FRENCH_STOPWORDS)
    tfidf_matrix = vectorizer.fit_transform([' '.join(list1), ' '.join(list2)])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return similarity[0][0]

def compute_semantic_similarity(list1, list2):
    """
    Calcule la similarité sémantique entre deux listes de compétences.
    """
    model = SentenceTransformer(EMBEDDING_MODEL)
    embeddings1 = model.encode(list1, convert_to_tensor=True)
    embeddings2 = model.encode(list2, convert_to_tensor=True)
    similarity_matrix = cosine_similarity(embeddings1, embeddings2)
    return similarity_matrix.mean()

def visualize_similarity(tfidf_similarity, semantic_similarity):
    """
    Génère une visualisation des similarités et l'enregistre sous forme d'image.
    """
    labels = ['TF-IDF Similarity', 'Semantic Similarity']
    values = [tfidf_similarity, semantic_similarity]

    plt.figure(figsize=(8, 6))
    plt.bar(labels, values, color=['blue', 'green'])
    plt.title("Comparaison des Similarités (après suppression des stopwords)")
    plt.ylabel("Score de Similarité")
    plt.ylim(0, 1)  # Les scores de similarité sont entre 0 et 1
    plt.savefig(f"{OUTPUT_DIR}similarity_scores_cleaned.png")
    plt.close()
    print(f"Graphique des similarités sauvegardé : {OUTPUT_DIR}similarity_scores_cleaned.png")

if __name__ == "__main__":
    # Exécuter l’analyse statistique
    analyze_statistics()

    # Charger les compétences
    esprit_competences_file = f"{CLEANED_DIR}programs_cleaned.csv"
    referentiel_competences_file = f"{CLEANED_DIR}referentiel_cleaned.csv"

    esprit_competences = pd.read_csv(esprit_competences_file)['Competences'].dropna().tolist()
    referentiel_competences = pd.read_csv(referentiel_competences_file)['Competences'].dropna().tolist()

    # Suppression des stopwords pour les similarités
    esprit_competences_cleaned = [remove_stopwords(' '.join(eval(c)), FRENCH_STOPWORDS) for c in esprit_competences]
    referentiel_competences_cleaned = [remove_stopwords(' '.join(c.split(";")), FRENCH_STOPWORDS) for c in referentiel_competences]

    # Calculer les similarités
    tfidf_similarity = compute_tfidf_similarity(esprit_competences_cleaned, referentiel_competences_cleaned)
    semantic_similarity = compute_semantic_similarity(esprit_competences_cleaned, referentiel_competences_cleaned)

    print(f"TF-IDF Similarité (après nettoyage) : {tfidf_similarity:.2f}")
    print(f"Semantic Similarité (après nettoyage) : {semantic_similarity:.2f}")

    # Visualiser les similarités
    visualize_similarity(tfidf_similarity, semantic_similarity)
