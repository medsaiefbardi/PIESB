import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def scrape_ref():
    base_url = 'http://rtmc.emploi.nat.tn'
    driver = webdriver.Chrome()

    # URL principale
    start_url = f'{base_url}/dm/index.php/rtmcdp/listedp/M'
    driver.get(start_url)
    time.sleep(3)

    # Liste pour stocker les données finales
    data = []

    try:
        soup = BeautifulSoup(driver.page_source, 'lxml')

        # Extraire les catégories principales
        categories = soup.find_all('div', class_='accordion-header js-accordion-header')
        for idx, category in enumerate(categories):
            category_name = category.text.strip()
            print(f'Catégorie trouvée : {category_name}')

            # Extraire les domaines dans chaque catégorie
            domaines = category.find_next_sibling('div').find_all('td', style='padding-left:0', align='left')
            for d_idx, domaine in enumerate(domaines):
                domaine_name = domaine.text.strip()
                print(f'Domaine trouvé : {domaine_name}')

                # Trouver le lien pour chaque domaine
                more_info = domaine.find('a')
                if more_info:
                    link = urljoin(base_url, more_info['href'])  # Utiliser urljoin pour combiner correctement l'URL
                    print(f'Traitement du lien : {link}')

                    # Vérifier si le lien est valide
                    if not link.startswith('http'):
                        print(f"Lien invalide : {link}")
                        continue

                    # Naviguer vers le lien
                    driver.get(link)
                    time.sleep(2)

                    # Extraire les métiers
                    soup = BeautifulSoup(driver.page_source, 'lxml')
                    metiers = []
                    metier_content = soup.find('div', class_='table-responsive-sm')
                    if metier_content:
                        professions = metier_content.find_all('td', style='padding-left:0')
                        for metier in professions:
                            metiers.append(metier.text.strip())

                    # Extraire les competences
                    try:
                        competence_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#competences']"))
                        )
                        competence_button.click()
                        time.sleep(2)

                        soup = BeautifulSoup(driver.page_source, 'lxml')
                        competencies = soup.find_all('div', class_='accordion js-accordion')
                        competences_domaine = []
                        for competence_section in competencies:
                            competences = competence_section.find_all('td', style='padding-left:0')
                            for competence in competences:
                                competences_domaine.append(competence.text.strip())

                        # Ajouter les données collectées
                        data.append({
                            "Catégorie": category_name,
                            "Domaine": domaine_name,
                            "Metiers": ";".join(metiers),
                            "competences": "; ".join(competences_domaine)
                        })

                    except TimeoutException as e:
                        print(f"Erreur lors de l'accès à la rubrique competences : {e}")

    finally:
        driver.quit()

    # Sauvegarder les données dans un fichier CSV
    output_file = './data/raw/referentiel.csv'
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Données sauvegardées dans {output_file}")


def main():
    scrape_ref()  # Appelle la fonction principale de scraping


if __name__ == "__main__":
    main()
