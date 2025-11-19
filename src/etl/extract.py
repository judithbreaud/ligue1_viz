
from src.api import api_get


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

#def save_raw_matches(matches_json,file_path="data/raw/matches_2015_2025.json"):


