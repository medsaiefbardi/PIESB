from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast
import os
TRANSFORMED_DIR = "data/cleaned"
CLUSTERED_DIR = "data/cleaned"

def safe_eval(text):
    """Essayez de convertir une chaîne en liste Python, sinon retournez une liste vide."""
    try:
        return ast.literal_eval(text) if isinstance(text, str) else []
    except (ValueError, SyntaxError):
        return []

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def perform_clustering(input_file, column_name, output_file):
    # Charger le fichier nettoyé
    df = pd.read_csv(input_file)

    # Transformer les listes en chaînes de caractères
    df[column_name] = df[column_name].apply(lambda x: ' '.join(eval(x)) if isinstance(x, str) else '')

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

    # Visualisation des clusters
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='PCA1', y='PCA2', hue='Cluster', palette='viridis')
    plt.title('Clustering des compétences')
    plt.show()

    # Sauvegarder le fichier clusterisé
    df.to_csv(output_file, index=False)
    print(f"Fichier clusterisé sauvegardé : {output_file}")

if __name__ == "__main__":
    referentiel_file = os.path.join(TRANSFORMED_DIR, "referentiel_transformed.csv")
    clustered_file = os.path.join(CLUSTERED_DIR, "referentiel_clustered.csv")
    perform_clustering(referentiel_file, "Competences", clustered_file)
