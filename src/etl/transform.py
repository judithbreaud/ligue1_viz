import pandas as pd

def pts(row):
    #return the points in a football game utilitary function for classement_interactif

    if row["score.winner"] == "HOME_TEAM" and row["is_home"]:
        return 3
    if row["score.winner"] == "AWAY_TEAM" and not row["is_home"]:
        return 3
    if row["score.winner"] == "DRAW":
        return 1
    return 0


def classement_interactif(matches_json):
   #from the json request from the API, creates an interactive ranking for each matchday and each team

   #select the matches and puts them in the pd format   
   matches_list = matches_json["matches"]
   df_matches = pd.json_normalize(matches_list)
   #restriction to finished games and the important columns
   df_short=df_matches[df_matches.status=="FINISHED"][["id","status","matchday","season.id","homeTeam.name","awayTeam.name","score.winner","score.fullTime.home","score.fullTime.away"]]

   #preparation for long format with a row for each matchday x team.
   #home games
   df_home = df_short.copy()
   df_home["team"] = df_home["homeTeam.name"]
   df_home["gf"] = df_home["score.fullTime.home"]
   df_home["ga"] = df_home["score.fullTime.away"]
   df_home["is_home"] = True
   #away games
   df_away = df_short.copy()
   df_away["team"] = df_away["awayTeam.name"]
   df_away["gf"] = df_away["score.fullTime.away"]
   df_away["ga"] = df_away["score.fullTime.home"]
   df_away["is_home"] = False
   #creation of the long format
   df_long = pd.concat([df_home, df_away], ignore_index=True)

   #calculating number of points gained at each day 
   df_long["points"] = df_long.apply(pts, axis=1)
   df_long["win"]   = df_long["points"] == 3
   df_long["draw"]  = df_long["points"] == 1
   df_long["loss"]  = df_long["points"] == 0

   #cumulating stats along the gamedays
   df_long.sort_values(["team","matchday"], inplace=True)
   df_long["points_cum"]=df_long.groupby("team")["points"].cumsum()
   df_long["gf_cum"] = df_long.groupby("team")["gf"].cumsum()
   df_long["ga_cum"] = df_long.groupby("team")["ga"].cumsum()
   df_long["gdif_cum"] = df_long["gf_cum"] - df_long["ga_cum"]
   df_long["wins_cum"]  = df_long.groupby("team")["win"].cumsum()
   df_long["draws_cum"] = df_long.groupby("team")["draw"].cumsum()
   df_long["losses_cum"] = df_long.groupby("team")["loss"].cumsum()

   #creating the ranking day by day

   df_long["rank"] = (
    df_long
    .sort_values(["matchday", "points_cum", "gdif_cum", "gf_cum"], ascending=[True, False, False, False])
    .groupby("matchday")
    .cumcount() + 1
   )

   return df_long[[
    "matchday", "team", "points",
    "points_cum", "gf_cum", "ga_cum", "gdif_cum",
    "wins_cum", "draws_cum", "losses_cum",
    "rank"
   ]].sort_values(["matchday","rank"])
