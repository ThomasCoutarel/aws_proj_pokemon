import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import boto3

# URL de départ
BASE_URL = "https://bulbapedia.bulbagarden.net"
URL = "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number"

BUCKET_NAME = "pokemons3proj"

GENERATIONS = [f"Generation_{roman}" for roman in ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]]

s3 = boto3.client("s3")


def upload_to_s3(img_url, bucket, key):
    try:
        response = requests.get(img_url, stream=True)
        if response.status_code == 200:
            s3.upload_fileobj(response.raw, bucket, key)
            print(f"[OK] {key} envoyé sur S3")
        else:
            print(f"[ERREUR] Impossible de télécharger {img_url}")
    except Exception as e:
        print(f"[ERREUR] {img_url} -> {e}")


def scrape_generation(gen_name, soup, limit=10):
    """Scrape les images d'une génération donnée et les envoie vers S3"""
    header = soup.find("span", {"id": gen_name})
    if not header:
        print(f"[WARN] {gen_name} introuvable.")
        return

    table = header.find_parent("h3").find_next_sibling("table")
    if not table:
        print(f"[WARN] Pas de table trouvée pour {gen_name}")
        return

    rows = table.find_all("tr")[1:]
    count = 0
    for row in rows:
        if count >= limit:
            break

        cols = row.find_all("td")
        if len(cols) < 3:
            continue

        name_tag = cols[2].find("a")
        if not name_tag:
            continue
        name = name_tag.text.strip().replace(" ", "_")

        img_tag = cols[1].find("img")
        if not img_tag:
            continue
        img_url = urljoin(BASE_URL, img_tag["src"])

        key = f"{gen_name}/{name}.png"

        upload_to_s3(img_url, BUCKET_NAME, key)

        count += 1


def main():
    response = requests.get(URL)
    if response.status_code != 200:
        print("Impossible d'accéder à la page.")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    for gen in GENERATIONS:
        print(f"\n=== Scraping {gen} (10 premiers Pokémon) ===")
        scrape_generation(gen, soup, limit=10)


if __name__ == "__main__":
    main()
