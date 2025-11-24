from dotenv import load_dotenv
load_dotenv()
from src.etl import fetch_matches, save_raw_matches, classement_interactif
import pandas as pd
import os

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

    print("Done.")

if __name__ == "__main__":
    main()