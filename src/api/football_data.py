import os
from dotenv import load_dotenv
import requests
import json

# Charge le .env si présent (utile en local)
#load_dotenv()

# Récupère la clé depuis l'environnement

def api_get(path, params=None, timeout=10):
    API_TOKEN = os.getenv("FOOTBALL_DATA_TOKEN", "").strip()
    if not API_TOKEN:
        raise ValueError("FOOTBALL_DATA_TOKEN n'est pas défini")

    # Base URL
    base = "https://api.football-data.org/v4"

    # Prépare le header
    headers = {"X-Auth-Token": API_TOKEN}
    url = base.rstrip("/") + "/" + path.lstrip("/")
    
    r = requests.get(url, headers=headers, params=params, timeout=timeout)
    
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"[ERROR] Status code: {r.status_code}, response: {r.text}")
        raise e
    
    return r.json()
