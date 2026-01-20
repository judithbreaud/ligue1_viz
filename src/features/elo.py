import pandas as pd
import numpy as np



def build_linear_elo_from_ranking(
    rank_df,
    team_col="team_tla",
    rank_col="rank",
    top_elo=1700,
    bottom_elo=1330,
    promoted_teams=None,
    promoted_elo=None
):
    """
    rank_df: DataFrame with columns [rank_col, team_col], rank 1..N (1 is champion)
    promoted_teams: list of TLA that are promoted for the target season
    promoted_elo: if provided, use this value for promoted teams (else set slightly under bottom_elo)
    Returns: pd.DataFrame with columns [team, init_elo]
    """

    df = rank_df[[rank_col, team_col]].copy()
    df = df.sort_values(rank_col).reset_index(drop=True)
    df[rank_col] = df[rank_col].astype(int)

    N = df[rank_col].max()
    if N < 2:
        raise ValueError("Au moins 2 équipes attendues dans rank_df")

    # We fix rank 1 to top_elo.
    # For ranks 2..N we linearly interpolate between second_elo and bottom_elo.
    ranks_1_to_N = np.arange(1, N+1)
    linear_vals = np.linspace(top_elo, bottom_elo, len(ranks_1_to_N))

    elo_map = {}

    # Ranks 1..N
    for r, val in zip(ranks_1_to_N, linear_vals):
        team = df.loc[df[rank_col] == r, team_col].values
        if len(team) == 0:
            continue
        elo_map[team[0]] = float(val)

    # Promoted teams handling
    if promoted_teams is None:
        promoted_teams = []

    if promoted_elo is None:
        # put them slightly under bottom_elo
        promoted_elo = float(bottom_elo - 20)

    for t in promoted_teams:
        elo_map[t] = float(promoted_elo)

    return elo_map



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
    
    weakest = min(elos.values())

    for t in promoted_teams:
        elos[t] = weakest-20
    
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


def append_future_matchday_elos(
    elo_history: pd.DataFrame,
    elos_end: dict,
    season,
    next_matchday
):
    """
    Ajoute une ligne par équipe correspondant à l'Elo
    avant la prochaine journée (J+1)
    """
    rows = []

    for team, elo in elos_end.items():
        rows.append({
            "season": season,
            "matchday": next_matchday,
            "team": team,
            "elo_before": elo
        })

    future_df = pd.DataFrame(rows)
    return pd.concat([elo_history, future_df], ignore_index=True)


def update_elo_history_with_matchday(
    elo_history: pd.DataFrame,
    df_matchday_results: pd.DataFrame,
):
    """
    Met à jour l'historique Elo avec UNE journée supplémentaire
    """

    # dernière journée connue
    season = elo_history["season"].iloc[-1]
    last_md = elo_history[elo_history["season"]==season]["matchday"].max()

    # elos avant cette journée
    elos_before = (
        elo_history[(elo_history["matchday"] == last_md) & (elo_history["season"] == season)]
        .set_index("team")["elo_before"]
        .to_dict()
    )

   # Appliquer les matchs de la journée J
    elos = elos_before.copy()

    for _, row in df_matchday_results.iterrows():
        ht, at = row["homeTeam.tla"], row["awayTeam.tla"]
        gh, ga = row["score.fullTime.home"], row["score.fullTime.away"]

        new_ht, new_at = update_elo(elos[ht], elos[at], gh, ga)
        elos[ht], elos[at] = new_ht, new_at

    # Ajouter UNIQUEMENT l'Elo avant J+1
    rows = []
    for team, elo in elos.items():
        rows.append({
            "season": season,
            "matchday": last_md + 1,
            "team": team,
            "elo_before": elo
        })

    future_df = pd.DataFrame(rows)

    return pd.concat([elo_history, future_df], ignore_index=True),elos


def elo_dict_to_df(elo_dict, season, matchday):
    return (
        pd.DataFrame(
            elo_dict.items(),
            columns=["team_tla", "elo"]
        ).assign(season=season,matchday=matchday)
    )
