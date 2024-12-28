import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

# URLS des programmes à scraper
PROGRAM_URLS = [
    "https://www.esb.tn/programmes/licences/sciences-de-gestion/",
    "https://www.esb.tn/programmes/licences/licence-en-business-computing/",
    "https://www.esb.tn/programmes/licences/licence-en-mathematiques-appliquees/",
    "https://www.esb.tn/programmes/masters-professionnels/master-en-management-digital-systemes-dinformation/",
    "https://www.esb.tn/programmes/masters-professionnels/master-en-marketing-digital/",
    "https://www.esb.tn/programmes/masters-professionnels/master-en-business-analytics/",
    "https://www.esb.tn/programmes/masters-professionnels/master-professionnel-de-comptabilite-controle-audit/",
    "https://www.esb.tn/programmes/masters-professionnels/master-professionnel-gamma/",
    "https://www.esb.tn/programmes/masters-professionnels/master-professionnel-en-finance-digitale/",
    "https://www.esb.tn/programmes/alternance/BA-alternance/",
    "https://www.esb.tn/programmes/doubles-diplomes/partenaires-academiques/",
]

# Chemins des fichiers
RAW_PATH = "data/raw/programs.csv"


# Fonction pour scraper les détails d'un programme
def scrape_program_details(url):
    """Scrape les détails d'un programme à partir de son URL."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    program_details = {"URL": url}

    # Objectifs
    objectives_section = soup.find('h3', text='Objectifs')
    if objectives_section:
        objectives = objectives_section.find_next('p').get_text(strip=True)
        program_details['Objectifs'] = objectives

    # Compétences
    competences_section = soup.find('h3', text='Compétences')
    if competences_section:
        competences = [li.get_text(strip=True) for li in competences_section.find_next('ul').find_all('li')]
        program_details['Compétences'] = competences

    # Contenu
    contenu_section = soup.find('h3', text='Contenu')
    if contenu_section:
        contenu = contenu_section.find_next('ul').get_text(separator=' ', strip=True)
        program_details['Contenu'] = contenu

    # Métiers
    metiers_section = soup.find('h3', text='Métiers')
    if metiers_section:
        metiers = [li.get_text(strip=True) for li in metiers_section.find_next('ul').find_all('li')]
        program_details['Métiers'] = metiers

    # Secteurs d'activité
    secteurs_section = soup.find('h3', text='Secteurs d’activité')
    if secteurs_section:
        secteurs = [li.get_text(strip=True) for li in secteurs_section.find_next('ul').find_all('li')]
        program_details['Secteurs d’activité'] = secteurs

    return program_details


# Fonction pour scraper tous les programmes
def scrape_all_programs(url_list):
    """Scrape les détails de tous les programmes dans une liste d'URLs."""
    all_programs = []
    for url in url_list:
        print(f"Scraping {url}...")
        try:
            details = scrape_program_details(url)
            all_programs.append(details)
        except Exception as e:
            print(f"Erreur lors du scraping de {url} : {e}")
            continue
    return all_programs


# Fonction pour sauvegarder les données scrappées en CSV
def save_to_csv(data, filename):
    """Sauvegarde les données scrappées dans un fichier CSV."""
    df = pd.DataFrame(data)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"Données sauvegardées dans {filename}")


# Fonction principale
def main():
    print("Lancement du scraping des programmes d'ESB...")
    data = scrape_all_programs(PROGRAM_URLS)
    save_to_csv(data, RAW_PATH)
    print("Scraping terminé avec succès !")


if __name__ == "__main__":
    main()
