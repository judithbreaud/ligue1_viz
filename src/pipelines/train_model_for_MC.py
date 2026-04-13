from src.etl import load_raw_matches
import pandas as pd
import os
from src.features import match_features_train_model_2
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
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
    X_23,y_23=match_features_train_model_2(df_matches_23,history_elo)
    X_24,y_24=match_features_train_model_2(df_matches_24,history_elo)
    X=pd.concat([X_23,X_24],ignore_index=True)
    y=pd.concat([y_23,y_24],ignore_index=True)

    print("== Preparing pipeline ==")

    num_features = ['dif_elo_before','dif_avg_goal_for','away_avg_goals_against',
                    'home_home_loss_rate','home_avg_points_before_match','home_avg_goals_against']

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_features)
        ]
    )
    pipeline=make_pipeline(preprocessor,RandomForestClassifier())
    print("== Grid search ==")

    rf_params = {
        'randomforestclassifier__n_estimators': [200, 500],
        'randomforestclassifier__max_depth': [None, 10],
        'randomforestclassifier__min_samples_leaf': [1, 4]
    }
    model=GridSearchCV(pipeline,
                       param_grid=rf_params,
                       cv=3,scoring='neg_log_loss')
    model.fit(X,y)

    print("== Calibration ==")

    calibrated = CalibratedClassifierCV(model.best_estimator_, cv=5, method='isotonic')
    calibrated.fit(X, y)

    print("== Save model ==")

    joblib.dump(calibrated,"models/match_prediction_MC")


    print("Done.")

if __name__ == "__main__":
    main()
