from src.etl import load_raw_matches
import pandas as pd
import os
from src.features import match_features_train
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import GridSearchCV
import joblib

def main():
    print("== Loading data ==")
    matches_2024= load_raw_matches("data/raw/",season_id=2024)
    matches_2023= load_raw_matches("data/raw/",season_id=2023)
    df_matches_24 = pd.json_normalize(matches_2024["matches"])
    df_matches_23 = pd.json_normalize(matches_2023["matches"])
    print("== Loading elo history ==")
    history_elo = pd.read_parquet("data/processed/elos_history.parquet")
    print("== Preparing data ==")
    X_23,y_23=match_features_train(df_matches_23,history_elo)
    X_24,y_24=match_features_train(df_matches_24,history_elo)
    X=pd.concat([X_23,X_24],ignore_index=True)
    y=pd.concat([y_23,y_24],ignore_index=True)

    print("== Preparing pipeline ==")

    num_features = ['home_avg_goals_against', 'home_home_loss_rate',
        'home_form_last5', 'away_avg_goals_for',
        'away_form_last5', 'dif_loss_rate',
        "dif_elo_before","away_elo_before"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_features)
        ]
    )
    pipeline=make_pipeline(preprocessor,GradientBoostingClassifier())
    print("== Grid search ==")

    gb_params = {
        'gradientboostingclassifier__n_estimators': [100, 200],
        'gradientboostingclassifier__learning_rate': [0.05,0.1],
        'gradientboostingclassifier__max_depth': [3, 5],
    }
    model=GridSearchCV(pipeline,
                       param_grid=gb_params,
                       cv=3,scoring='neg_log_loss')
    model.fit(X,y)

    print("== Calibration ==")

    calibrated = CalibratedClassifierCV(model.best_estimator_, cv=5, method='isotonic')
    calibrated.fit(X, y)

    print("== Save model ==")

    joblib.dump(calibrated,"models/match_prediction")


    print("Done.")

if __name__ == "__main__":
    main()
