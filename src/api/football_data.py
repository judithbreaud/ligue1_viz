# Cellule: imports et chargement de la clé API depuis .env
import os
from dotenv import load_dotenv   # charge les variables d'environnement depuis un fichier .env
import requests                 # pour les appels HTTP
#import pandas as pd             # manipulation de données tabulaires
import json                     # pour afficher proprement le JSON si besoin

# Charge les variables d'environnement depuis le fichier .env (s'il existe).
load_dotenv()


def get_api_token():
    token = os.getenv("FOOTBALL_DATA_TOKEN")
    if not token:
        raise RuntimeError("FOOTBALL_DATA_TOKEN absent. "
                           "En local : créer un .env. "
                           "Sur GitHub : ajouter dans Secrets.")
    return token


# Base URL pour football-data.org (version v4)
BASE_URL = "https://api.football-data.org/v4"

# Optionnel : petite info pour l'utilisateur
print("Clé API chargée. Base:", BASE_URL)

def api_get(path, params=None, base=BASE_URL, timeout=10):
    """
    Effectue une requête GET sur base + path, retourne le JSON décodé.
    - path : chemin après la base (ex: "/competitions/2021/standings")
    - params : dict de query params (facultatif)
    """
    token = get_api_token()

    # 🔍 DEBUG : afficher longueur et début du token
    print(f"[DEBUG] Token length: {len(token)}")
    print(f"[DEBUG] Token prefix: {token[:5]}***")

    headers = {"X-Auth-Token": token}
    print(f"[DEBUG] params: {params}")

    url = base.rstrip("/") + "/" + path.lstrip("/")
    print(f"[DEBUG] URL called: {url}")

    r = requests.get(url, headers=headers, params=params, timeout=timeout)
    r.raise_for_status()
    return r.json()
