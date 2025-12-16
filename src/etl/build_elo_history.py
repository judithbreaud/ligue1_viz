from dotenv import load_dotenv
load_dotenv()
from src.features import initialize_elos, reset_elos_between_seasons, expected_score,update_elo,compute_elo_for_season, build_linear_elo_from_ranking,append_future_matchday_elos
from src.etl import load_raw_matches
import pandas as pd
import os
import numpy as np

def main():
    print("== Building an history of the ELOs ==")
    print("== Fetching data ==")
    matches_23=load_raw_matches(season_id=2023)
    matches_24=load_raw_matches(season_id=2024)
    matches_25=load_raw_matches(season_id=2025)
    rank_22_23 = pd.read_parquet("data/processed/ranking_22_23.parquet")

    print("== Data into panda ==")
    df_matches_23 = pd.json_normalize(matches_23["matches"])
    
    df_matches_24 = pd.json_normalize(matches_24["matches"])
    df_matches_25_temp = pd.json_normalize(matches_25["matches"])
    df_matches_25 = df_matches_25_temp[df_matches_25_temp.status=="FINISHED"]

    print("== Saison 23-24 ==")
    elos_2324_start = build_linear_elo_from_ranking(
    rank_22_23,
    team_col="team_tla",
    rank_col="team_rank",
    top_elo=1700,
    bottom_elo=1330,
    promoted_teams=["HAC","FCM"]
    )
    print(elos_2324_start.keys)
    print(df_matches_23["homeTeam.tla"].unique())

    history_2324, elos_end_2324 = compute_elo_for_season(df_matches_23, elos_2324_start)
    print("== Saison 24-25 ==")
    elos_2425_start = reset_elos_between_seasons(elos_end_2324,promoted_teams=["AJA","ANG","ASS"])
    history_2425, elos_end_2425 = compute_elo_for_season(df_matches_24, elos_2425_start)
    print("== Saison 25-26 ==")
    elos_2526_start = reset_elos_between_seasons(elos_end_2425,promoted_teams=["FCL","PFC","FCM"])
    history_2526, elos_end_2526 = compute_elo_for_season(df_matches_25, elos_2526_start)
    last_md = df_matches_25["matchday"].max()
    next_md = last_md + 1
    season_2526 = df_matches_25["season.startDate"].iloc[0]

    history_2526 = append_future_matchday_elos(
        history_2526,
        elos_end_2526,
        season=season_2526,
        next_matchday=next_md
    )


    print("== Concaténer ==")
    elo_history = pd.concat([history_2324, history_2425, history_2526])
    
    print("== Enregistrer ==")

    os.makedirs("data/processed", exist_ok=True)
    processed_path = "data/processed/elos_history.parquet"

    print(f"== Saving processed data to {processed_path} ==")
    elo_history.to_parquet(processed_path, index=False)

    print("Done.")

if __name__ == "__main__":
    main()
