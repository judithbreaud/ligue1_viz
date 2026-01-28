from dotenv import load_dotenv
load_dotenv()
from src.etl import fetch_matches, save_raw_matches, classement_interactif, find_next_opponent,save_next_opponent
import pandas as pd
import os
from src.features import match_features_pred, update_elo_history_with_matchday,elo_dict_to_df
from src.etl import load_raw_matches
import joblib

COMPETITION_ID="FL1" #ligue 1
SEASON_ID="2025"

def main():
    print("== Fetching data from API ==")
    matches_json=fetch_matches(COMPETITION_ID,SEASON_ID)

    print("== Saving raw data ==")
    raw_path=save_raw_matches(matches_json)

    print(f"== Raw data saved at: {raw_path} ==")

    print("== Transforming data ==")
    df = classement_interactif(matches_json)

    os.makedirs("data/processed", exist_ok=True)
    processed_path = "data/processed/standings_long.parquet"

    print(f"== Saving processed data to {processed_path} ==")
    df.to_parquet(processed_path, index=False)
    
    print("== Finding next opponent ==")
    opponent=find_next_opponent(matches_json)
    save_next_opponent(opponent_name=opponent)

    print("== Import and repare data for prediction ==")
    df_matches_25 = pd.json_normalize(matches_json["matches"])
    history_elo = pd.read_parquet("data/processed/elos_history.parquet")

    last_elo_md = history_elo[history_elo["season"].str.contains("2025")]["matchday"].max()
    last_finished_md = (
        df_matches_25[df_matches_25["status"] == "FINISHED"]["matchday"].max()
    )
    print(f"Last finished matchday: {last_finished_md}")
    print(f"Last ELO matchday: {last_elo_md}")
    if last_elo_md==last_finished_md+1:
        print("No new matches, exiting pipeline")
        return
    elif last_elo_md==last_finished_md:
        #update elo then do prediction
        print("== Update ELO history ==")

        new_history_elo,elos_end=update_elo_history_with_matchday(history_elo,df_matches_25[df_matches_25["matchday"]==last_finished_md])
        print(1)

        os.makedirs("data/processed", exist_ok=True)
        processed_path = "data/processed/elos_history.parquet"

        print(f"== Saving processed data to {processed_path} ==")
        new_history_elo.to_parquet(processed_path, index=False)

        X_pred,y_none,label_pred=match_features_pred(df_matches_25,new_history_elo,last_finished_md+1) 

        print("== Import model ==")
        model=joblib.load("models/match_prediction")

        print(f"Predicting matchday: {last_finished_md + 1}")
        y_proba = model.predict_proba(X_pred)
        proba_df = pd.DataFrame(
            y_proba,
            columns=model.classes_
        )
        label_pred = label_pred.reset_index(drop=True)
        final_df_pred = pd.concat([label_pred, proba_df], axis=1)

        print("== Save prediction ==")

        os.makedirs("data/processed", exist_ok=True)
        processed_pred_path = "data/processed/next_matchday_prediction.parquet"

        final_df_pred.to_parquet(processed_pred_path, index=False)



    else: 
        #there is an error 
        print("There is an error")

    print("Done.")

if __name__ == "__main__":
    main()