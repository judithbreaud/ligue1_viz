from src.features import match_features_pred_model_2
from src.simulation import run_monte_carlo, compute_rank_probabilities
import pandas as pd

def run_season_monte_carlo(
    df_matches,
    elo_history,
    model,
    standings_path,
    n_simulations=10000
):
    

    X,Y,label=match_features_pred_model_2(df_matches,elo_history,None)
    label_unplayed=label[Y.isna()]
    X_unplayed=X[Y.isna()]
    y_label_played=label[~Y.isna()].copy()
    y_label_played["score.winner"] = Y[~Y.isna()]
    old_goal_dif = pd.read_parquet(standings_path)
    old_goal_dif = (
        old_goal_dif
        .sort_values("matchday")
        .groupby("team", as_index=False)
        .last()
    )[["team", "gdif_cum"]]
    probas = model.predict_proba(X_unplayed)
    classes = model.classes_
    res=run_monte_carlo(n_simulations,probas,classes,label_unplayed,y_label_played,old_goal_dif)
    rank_probs = compute_rank_probabilities(res, n_simulations)
    return rank_probs


