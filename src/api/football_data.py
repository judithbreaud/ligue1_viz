# Cellule: imports et chargement de la clé API depuis .env
import os
from dotenv import load_dotenv   # charge les variables d'environnement depuis un fichier .env
import requests                 # pour les appels HTTP
#import pandas as pd             # manipulation de données tabulaires
import json                     # pour afficher proprement le JSON si besoin

# Charge les variables d'environnement depuis le fichier .env (s'il existe).
load_dotenv()

# Récupère la clé API depuis la variable d'environnement FOOTBALL_DATA_TOKEN
API_TOKEN = os.getenv("FOOTBALL_DATA_TOKEN")

# Vérification simple : on lève une erreur explicite si la clé n'est pas trouvée
if not API_TOKEN:
    raise RuntimeError("Clé API non trouvée. Crée un fichier .env contenant FOOTBALL_DATA_TOKEN=ta_cle")

# Base URL pour football-data.org (version v4)
BASE_URL = "https://api.football-data.org/v4"

# Prépare les headers d'authentification pour toutes les requêtes
HEADERS = {"X-Auth-Token": API_TOKEN}

# Optionnel : petite info pour l'utilisateur
print("Clé API chargée. Base:", BASE_URL)

def api_get(path, params=None, base=BASE_URL, headers=HEADERS, timeout=10):
    """
    Effectue une requête GET sur base + path, retourne le JSON décodé.
    - path : chemin après la base (ex: "/competitions/2021/standings")
    - params : dict de query params (facultatif)
    - headers : en-têtes HTTP (par défaut HEADERS préparés ci-dessus)
    """
    url = base.rstrip("/") + "/" + path.lstrip("/")  # construit correctement l'URL
    # 1) On envoie la requête
    r = requests.get(url, headers=headers, params=params, timeout=timeout)
    # 2) Si le statut n'est pas 200, raise_for_status déclenche une exception HTTPError
    r.raise_for_status()
    # 3) Retourne la réponse décodée en JSON (sous forme de dict / list selon la réponse)
    return r.json()