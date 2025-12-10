import pandas as pd
import numpy as np


def initialize_elos(teams, promoted_teams=None, base_elo=1500, promoted_elo=1450):
    """
    Initialise le rating Elo des équipes en début de saison.

    teams : liste des équipes
    promoted_teams : liste des équipes promues cette saison
    """
    elos = {}

    for t in teams:
        if promoted_teams and t in promoted_teams:
            elos[t] = promoted_elo
        else:
            elos[t] = base_elo

    return elos



def reset_elos_between_seasons(previous_elos, promoted_teams=None, alpha=0.75, base_elo=1500):
    """
    Applique le lissage intersaison :
    Elo_new = alpha * old_elo + (1-alpha) * base_elo
    """
    elos={team: alpha * rating + (1 - alpha) * base_elo
        for team, rating in previous_elos.items()}
    
    for t in promoted_teams:
        elos[t] = 1450
    
    return elos



def expected_score(elo_a, elo_b, home_advantage=55):
    """Renvoie la probabilité que A gagne contre B."""
    return 1 / (1 + 10 ** (-(elo_a + home_advantage - elo_b) / 400))



def update_elo(elo_home, elo_away, goals_home, goals_away, k=20):
    """Met à jour deux Elo en fonction du résultat."""
    # Résultat effectif
    if goals_home > goals_away:
        S_home, S_away = 1, 0
    elif goals_home < goals_away:
        S_home, S_away = 0, 1
    else:
        S_home, S_away = 0.5, 0.5

    # Probabilités attendues
    E_home = expected_score(elo_home, elo_away)
    E_away = 1 - E_home

    # Optionnel : bonus goal difference (type Club Elo)
    goal_diff = abs(goals_home - goals_away)
    margin_multiplier = 1 + (goal_diff - 1) * 0.1 if goal_diff > 1 else 1

    # Mise à jour Elo
    elo_home_new = elo_home + k * margin_multiplier * (S_home - E_home)
    elo_away_new = elo_away + k * margin_multiplier * (S_away - E_away)

    return elo_home_new, elo_away_new




def compute_elo_for_season(df_matches, elos_start):
    """
    df_matches doit contenir : saison, matchday, home_team, away_team, home_goals, away_goals
    Les matches doivent être triés chronologiquement !
    """
    df_matches = df_matches.sort_values(["matchday", "utcDate"])

    elos = elos_start.copy()
    history = []

    for _, row in df_matches.iterrows():

        ht, at = row["homeTeam.tla"], row["awayTeam.tla"]
        gh, ga = row["score.fullTime.home"], row["score.fullTime.away"]
        season, md = row['season.startDate'], row["matchday"]

        # Elo avant match
        elo_ht_before = elos[ht]
        elo_at_before = elos[at]

        history.append({
            "season": season,
            "matchday": md,
            "team": ht,
            "elo_before": elo_ht_before
        })
        history.append({
            "season": season,
            "matchday": md,
            "team": at,
            "elo_before": elo_at_before
        })

        # Mise à jour après match
        new_ht, new_at = update_elo(elo_ht_before, elo_at_before, gh, ga)
        elos[ht], elos[at] = new_ht, new_at

    return pd.DataFrame(history), elos