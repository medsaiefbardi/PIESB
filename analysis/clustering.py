import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import ast
import os
import spacy
import re

# Charger le modèle NLP français
nlp = spacy.load("fr_core_news_sm")

# Répertoires
TRANSFORMED_DIR = "data/cleaned"
CLUSTERED_DIR = "data/cleaned"
OUTPUT_DIR = "output"

# Liste de stopwords en français
FRENCH_STOPWORDS = set([
    "de", "des", "et", "à", "la", "le", "les", "un", "une", "dans", "par", "avec",
    "pour", "sur", "en", "au", "aux", "du", "ou", "qui", "que", "dont", "est", "à",
    ":", "-", "(", ")", ".", "...", ";", ",","d","l","domaine","activité","structure","Utilisation","information","Techniques","utilisation","techniques","informations","produits","service","Gestion","clients","gestion","Réglementation","commerciale","outils","traitement","suivi","réglementation","équipe","actions","entreprise","électronique"
])

def clean_text(text):
    """
    Supprime les caractères spéciaux et double espaces d'une chaîne de texte.
    """
    text = re.sub(r"[^\w\s]", " ", text)  # Remplace les caractères non-alphanumériques par des espaces
    text = re.sub(r"\s+", " ", text)  # Remplace les multiples espaces par un seul
    return text.strip()

def remove_stopwords_and_verbs(text, stopwords):
    """
    Supprime les stopwords et les verbes d'une chaîne de texte.
    """
    text = clean_text(text)  # Nettoyage initial
    doc = nlp(text)
    filtered_words = [
        token.text for token in doc
        if token.text.lower() not in stopwords and token.pos_ not in {"VERB", "AUX"}
    ]
    return ' '.join(filtered_words)

def perform_clustering(input_file, column_name, output_file):
    """
    Effectue le clustering des compétences et sauvegarde les résultats.
    """
    # Charger le fichier nettoyé
    df = pd.read_csv(input_file)

    # Transformer les listes en chaînes de caractères après suppression des stopwords et des verbes
    df[column_name] = df[column_name].apply(
        lambda x: remove_stopwords_and_verbs(' '.join(eval(x)), FRENCH_STOPWORDS) if isinstance(x, str) else ''
    )

    # Vectorisation des compétences
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df[column_name])

    # Appliquer le clustering KMeans
    kmeans = KMeans(n_clusters=5, random_state=42)
    df['Cluster'] = kmeans.fit_predict(X)

    # Réduction dimensionnelle pour la visualisation
    pca = PCA(n_components=2)
    reduced_data = pca.fit_transform(X.toarray())
    df['PCA1'], df['PCA2'] = reduced_data[:, 0], reduced_data[:, 1]

    return df

def assign_cluster_short_names(df, column_name, cluster_column):
    """
    Donne des noms courts et significatifs aux clusters en évitant les répétitions de mots.
    """
    cluster_short_names = {}
    used_words = set()  # Ensemble pour suivre les mots déjà utilisés

    for cluster_id in df[cluster_column].unique():
        # Filtrer les compétences du cluster
        cluster_data = df[df[cluster_column] == cluster_id][column_name]

        # Compter les mots les plus fréquents en excluant les stopwords et verbes
        words = ' '.join(cluster_data).split()
        filtered_words = [word for word in words if word.lower() not in FRENCH_STOPWORDS]
        most_common = Counter(filtered_words).most_common(10)  # Considérer les 10 mots les plus fréquents

        # Générer un nom court basé sur les mots-clés dominants, en évitant les répétitions
        cluster_name = []
        for word, _ in most_common:
            if word not in used_words:
                cluster_name.append(word)
                used_words.add(word)  # Marquer le mot comme utilisé
            if len(cluster_name) == 2:  # Limiter à 2 mots
                break
        
        cluster_short_names[cluster_id] = ' '.join(cluster_name)
    
    return cluster_short_names

def plot_clusters_with_names(df, cluster_column, output_file, cluster_names):
    """
    Visualise les clusters avec les noms de clusters affichés sur la légende.
    """
    # Ajouter les noms des clusters dans le DataFrame
    df['Cluster_Name'] = df[cluster_column].map(cluster_names)
    custom_palette = {
        cluster_name: color for cluster_name, color in zip(
            cluster_names.values(),
            ['red', 'green', 'yellow', 'blue', 'black']
        )
    }
    # Visualisation des clusters
    plt.figure(figsize=(10, 6))
    scatter_plot = sns.scatterplot(
        data=df,
        x='PCA1',
        y='PCA2',
        hue='Cluster_Name',  # Utiliser les noms des clusters comme légende
        palette=custom_palette,
        legend='full'
    )
    scatter_plot.set_title('Clustering des compétences avec noms des clusters')
    scatter_plot.set_xlabel('Composante Principale 1 (PCA1)')
    scatter_plot.set_ylabel('Composante Principale 2 (PCA2)')
    scatter_plot.legend(title='Clusters', loc='upper right', fontsize='small')

    # Sauvegarder le graphique
    plt.savefig(output_file)
    plt.close()
    print(f"Graphique des clusters sauvegardé : {output_file}")

if __name__ == "__main__":
    # Chemin des fichiers
    referentiel_file = os.path.join(TRANSFORMED_DIR, "referentiel_transformed.csv")
    clustered_file = os.path.join(CLUSTERED_DIR, "referentiel_clustered.csv")
    output_image_path = os.path.join(OUTPUT_DIR, "clustering_competences_named.png")

    # Exécuter le clustering
    clustered_df = perform_clustering(referentiel_file, "Competences", clustered_file)

    # Assigner des noms courts aux clusters
    cluster_short_names = assign_cluster_short_names(clustered_df, "Competences", "Cluster")

    # Afficher les noms courts des clusters
    print("\nNoms des clusters :")
    for cluster_id, short_name in cluster_short_names.items():
        print(f"Cluster {cluster_id} : {short_name}")

    # Visualiser les clusters avec noms
    plot_clusters_with_names(clustered_df, "Cluster", output_image_path, cluster_short_names)
