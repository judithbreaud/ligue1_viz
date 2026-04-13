import pandas as pd
import numpy as np
from src.etl import pts
def run_one_simulation(probas,classes,unplayed,played,old_goal_dif):
    unplayed = unplayed.copy()

    # Sample one class per row based on probabilities
    y_pred_random = np.array([
        np.random.choice(classes, p=proba)
        for proba in probas
    ])
    unplayed['score.winner']=y_pred_random
    df=pd.concat([unplayed,played])
    df_home=df[["matchday", "homeTeam.name","homeTeam.id", "score.winner"]].rename(
        columns={
            "homeTeam.name": "team","homeTeam.id": "id"
        }
    )
    df_home["is_home"] = True

    df_away = df[["matchday", "awayTeam.name","awayTeam.id", "score.winner"]].rename(
        columns={
            "awayTeam.name": "team",'awayTeam.id':"id"
        }
    )
    df_away["is_home"] = False
    df_long=pd.concat([df_home,df_away])
    df_long["points"] = df_long.apply(pts, axis=1)
    tot_points=df_long.groupby(['id','team'])['points'].sum().reset_index()

    merged_df = old_goal_dif.merge(tot_points, on='team', how='left')
    merged_df = merged_df.sort_values(
        by=["points", "gdif_cum"],
        ascending=False
    ).reset_index(drop=True)

    merged_df["rank"] = merged_df.index + 1

    return merged_df[["team","rank"]]


