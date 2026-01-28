import pandas as pd
from src.etl import pts

def prepare_match_features(df_matches, elo_df):
    """
    - df_matches is the pd.json_normalize version of the API data
    - merge elo
    - compute dif features
    - select final features
    """

    df=df_matches[["status","season.startDate","matchday","homeTeam.id","homeTeam.name","homeTeam.tla","awayTeam.id","awayTeam.name","awayTeam.tla",
                       "score.winner","score.fullTime.home","score.fullTime.away"]]
    
    df = df.sort_values(["matchday", "homeTeam.id"])

    df_home = df[["matchday", "homeTeam.id", "homeTeam.tla", "season.startDate",
                "score.fullTime.home", "score.fullTime.away", "score.winner"]].rename(
        columns={
            "homeTeam.id": "team_id",
            "homeTeam.tla": "team",
            "season.startDate": "season",
            "score.fullTime.home": "goals_for",
            "score.fullTime.away": "goals_against"
        }
    )
    df_home["is_home"] = True

    df_away = df[["matchday", "awayTeam.id", "awayTeam.tla", "season.startDate",
                "score.fullTime.home", "score.fullTime.away", "score.winner"]].rename(
        columns={
            "awayTeam.id": "team_id",
            "awayTeam.tla": "team",
            "season.startDate": "season",
            "score.fullTime.home": "goals_against",
            "score.fullTime.away": "goals_for"
        }
    )
    df_away["is_home"] = False

    df_home["win"]  = df_home["score.winner"] == "HOME_TEAM"
    df_home["loss"] = df_home["score.winner"] == "AWAY_TEAM"

    df_away["win"]  = df_away["score.winner"] == "AWAY_TEAM"
    df_away["loss"] = df_away["score.winner"] == "HOME_TEAM"

    df_long = pd.concat([df_home, df_away], ignore_index=True)
    df_long=pd.merge(df_long,elo_df,on=["season","matchday","team"])


    df_long = df_long.sort_values(["team_id", "matchday"])

    df_long["points"] = df_long.apply(pts, axis=1)
    df_long["points_before_match"] = (
        df_long.groupby("team_id")["points"]
            .cumsum()
            .shift(1)
    )
    df_long["avg_points_before_match"] = (
        df_long["points_before_match"]/(df_long["matchday"]-1)
    )

    df_long["goal_diff"] = df_long["goals_for"] - df_long["goals_against"]


    df_long["avg_goals_for"] = df_long.groupby("team_id")["goals_for"] \
                                    .transform(lambda s: s.shift(1).expanding().mean())

    df_long["avg_goals_against"] = df_long.groupby("team_id")["goals_against"] \
                                        .transform(lambda s: s.shift(1).expanding().mean())

    df_long["cum_goals_for"] = (
        df_long.groupby("team_id")["goals_for"].cumsum().shift(1)
    )
    df_long["cum_goals_against"] = (
        df_long.groupby("team_id")["goals_against"].cumsum().shift(1)
    )
    df_long["cum_goal_diff"] = df_long["cum_goals_for"] - df_long["cum_goals_against"]


    df_long["home_win_rate"] = (
        df_long[df_long.is_home]
        .groupby("team_id")["win"]
        .transform(lambda s: s.shift(1).expanding().mean())
    )

    df_long["away_win_rate"] = (
        df_long[~df_long.is_home]
        .groupby("team_id")["win"]
        .transform(lambda s: s.shift(1).expanding().mean())
    )

    df_long["away_loss_rate"] = (
        df_long[~df_long.is_home]
        .groupby("team_id")["loss"]
        .transform(lambda s: s.shift(1).expanding().mean())
    )

    df_long["home_loss_rate"] = (
        df_long[df_long.is_home]
        .groupby("team_id")["loss"]
        .transform(lambda s: s.shift(1).expanding().mean())
    )

    df_long = df_long.sort_values(
        ["matchday", "points_before_match", "cum_goal_diff", "cum_goals_for"],
        ascending=[True, False, False, False]
    )

    # On calcule le ranking par matchday en utilisant cumcount
    df_long["ranking_before_match"] = (
        df_long.groupby("matchday").cumcount() + 1
    )



    df_long["form_last5"] = (
        df_long.groupby("team_id")["points"]
            .transform(lambda s: s.shift(1).rolling(5, min_periods=1).sum())
    )

    df_stats=df_long[["team_id", "matchday","avg_points_before_match", "cum_goal_diff", "cum_goals_for", "cum_goals_against",
    "avg_goals_for", "avg_goals_against",
    "home_win_rate", "away_win_rate", "home_loss_rate", "away_loss_rate",
    "ranking_before_match", "form_last5","elo_before"]]


    df_merged = df\
    .merge(
        df_stats.add_prefix("home_"),
        left_on=["homeTeam.id", "matchday"],
        right_on=["home_team_id", "home_matchday"],
        how="left"
    )\
    .merge(
        df_stats.add_prefix("away_"),
        left_on=["awayTeam.id", "matchday"],
        right_on=["away_team_id", "away_matchday"],
        how="left"
    )
    df_merged.drop(columns=["season.startDate","status","homeTeam.id","awayTeam.id",
        "home_team_id", "home_matchday", 
        "away_team_id", "away_matchday","score.fullTime.home","score.fullTime.away",
        "home_away_win_rate","home_away_loss_rate","away_home_win_rate","away_home_loss_rate",
        "home_cum_goal_diff","away_cum_goal_diff","home_cum_goals_for","away_cum_goals_for",
        "home_cum_goals_against","away_cum_goals_against",'homeTeam.tla', 'awayTeam.tla',
    ],inplace=True)


    df_merged['dif_avg_points']=df_merged['home_avg_points_before_match']-df_merged['away_avg_points_before_match']
    df_merged['dif_avg_goal_for']=df_merged['home_avg_goals_for']-df_merged['away_avg_goals_for']
    df_merged['dif_avg_goal_against']=df_merged['home_avg_goals_against']-df_merged['away_avg_goals_against']
    df_merged['dif_win_rate']=df_merged['home_home_win_rate']-df_merged['away_away_win_rate']
    df_merged['dif_loss_rate']=df_merged['home_home_loss_rate']-df_merged['away_away_loss_rate']
    df_merged['dif_ranking']=df_merged['home_ranking_before_match']-df_merged['away_ranking_before_match']
    df_merged['dif_form_last5']=df_merged['home_form_last5']-df_merged['away_form_last5']
    df_merged['dif_elo_before']=df_merged['home_elo_before']-df_merged['away_elo_before']
    df_merged['rate_elo_before']=df_merged['home_elo_before']/df_merged['away_elo_before']


    df_for_model=df_merged[df_merged["matchday"]>5]

    return df_for_model


def match_features_train(df_matches,elo_df):
    df_for_model=prepare_match_features(df_matches,elo_df)
    X=df_for_model[['home_avg_goals_against', 'home_home_loss_rate',
       'home_form_last5', 'away_avg_goals_for',
       'away_form_last5', 'dif_loss_rate',
       "dif_elo_before","away_elo_before"]]
    y=df_for_model["score.winner"]
    return X,y

def match_features_pred(df_matches,elo_df,select_matchday):
    df_for_model=prepare_match_features(df_matches,elo_df)
    if select_matchday is not None:
        df_for_model=df_for_model[df_for_model["matchday"]==select_matchday]
    X=df_for_model[['home_avg_goals_against', 'home_home_loss_rate',
       'home_form_last5', 'away_avg_goals_for',
       'away_form_last5', 'dif_loss_rate',
       "dif_elo_before","away_elo_before"]]
    y=df_for_model["score.winner"]
    label = df_for_model[['matchday','homeTeam.name','awayTeam.name']].copy()
    label["game_name"]=label["homeTeam.name"]+" / "+label["awayTeam.name"]

    return X,y,label