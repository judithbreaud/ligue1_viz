
from src.api import api_get
import json
import os

def fetch_matches(competition_id: int, season_id: int):
    """
    Récupère la liste des matches d'une compétition et d'une saison donnée.
    Ex : 2015 = Ligue 1, 2021 = Premier League.

    Retourne le JSON déjà décodé (dict ou list) fourni par api_get().
    """
    return api_get(
        f"/competitions/{competition_id}/matches",
        params={"season": season_id}
    )

def save_raw_matches(matches_json,folder_path="data/raw/"):
    """
    Sauvegarde la réponse JSON brute dans un fichier structuré :
    data/raw/FL1_2025.json
    """
    season_id=matches_json["filters"]['season']
    competition_code=matches_json["competition"]["code"] #FL1 pour ligue 1
    os.makedirs(folder_path, exist_ok=True)
    filename = f"{competition_code}_{season_id}.json"
    full_path = os.path.join(folder_path, filename)

    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(matches_json, f, indent=2, ensure_ascii=False)
    return full_path


def load_raw_matches(folder_path="data/raw/",competition_code="FL1",season_id=2025):
    """
    Charge un fichier JSON brut préalablement sauvegardé.
    """
    filename = f"{competition_code}_{season_id}.json"
    full_path = os.path.join(folder_path, filename)
    with open(full_path, "r", encoding="utf-8") as f:
        json.load(f)
