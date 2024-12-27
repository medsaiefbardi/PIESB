from scraping.scraping_esb import main as scrape_esb
from scraping.scraping_ref import main as scrape_ref

def run_all_scrapers():
    print("Exécution des scripts de scraping...")

    # Scraping ESB
    scrape_esb()

    # Scraping Référentiel
    scrape_ref()

    print("Tous les processus de scraping sont terminés.")

if __name__ == "__main__":
    run_all_scrapers()
