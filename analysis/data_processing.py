import pandas as pd

def load_data(file_path):
    return pd.read_csv(file_path)

def clean_data(df):
    """
    Effectue le nettoyage des données, comme le traitement des valeurs manquantes.
    """
    # Exemple de traitement des valeurs manquantes
    df = df.dropna()
    return df

def save_clean_data(df, output_path):
    """
    Sauvegarde les données nettoyées dans un nouveau fichier CSV.
    """
    df.to_csv(output_path, index=False)

# Exemple d'utilisation
if __name__ == "__main__":
    raw_data = load_data('raw_data.csv')
    clean_data = clean_data(raw_data)
    save_clean_data(clean_data, 'clean_data.csv')
