import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
import pandas as pd
def compare_rank(standings_long, team_1, team_2,col1="red",col2="blue"):
    """plots the rankings of team_1 and team_2
    """
    df1=standings_long[standings_long["team"]==team_1]
    df2=standings_long[standings_long["team"]==team_2]
    
    fig, ax = plt.subplots(figsize=(10, 6))

    
    # Tracer les courbes
    ax.step(df1["matchday"], df1["rank"], where="post", label=team_1, color=f"tab:{col1}")
    ax.step(df2["matchday"], df2["rank"], where="post", label=team_2, color=f"tab:{col2}")

    ax.invert_yaxis()

    # Ajouter des labels et un titre
    ax.set_xlabel("Journée")
    ax.set_ylabel("Classement")
    ax.set_title(f"Évolution du classement : {team_1} vs {team_2}")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)

    return fig

def compare_points_total(standings_long, team_1, team_2,col1="red",col2="blue"):
    """plots the total points day after day of team_1 and team_2
    """
    df1=standings_long[standings_long["team"]==team_1]
    df2=standings_long[standings_long["team"]==team_2]

    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Tracer les courbes
    ax.step(df1["matchday"], df1["points_cum"], where="post", label=team_1, color=f"tab:{col1}")
    ax.step(df2["matchday"], df2["points_cum"], where="post", label=team_2, color=f"tab:{col2}")

    #plt.plot(df1["matchday"], df1["rank"], marker="o", label=team_1, color="tab:blue")
    #plt.plot(df2["matchday"], df2["rank"], marker="o", label=team_2, color="tab:red")
    
    # Ajouter des labels et un titre
    ax.set_xlabel("Journée")
    ax.set_ylabel("Points")
    ax.set_title(f"Points total : {team_1} vs {team_2}")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)
    
    return fig

def compare_resultats(standings_long, team_1, team_2,col1="red",col2="blue"):

    """plots the results of each matchday of team_1 and team_2
    """
    df1=standings_long[standings_long["team"]==team_1]
    df2=standings_long[standings_long["team"]==team_2]

    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Tracer les courbes
    ax.scatter(df1["matchday"], df1["points"], label=team_1, color=f"tab:{col1}",marker='s')
    ax.scatter(df2["matchday"], df2["points"], label=team_2, color=f"tab:{col2}",marker="*")

    #plt.plot(df1["matchday"], df1["rank"], marker="o", label=team_1, color="tab:blue")
    #plt.plot(df2["matchday"], df2["rank"], marker="o", label=team_2, color="tab:red")
    
    # Ajouter des labels et un titre
    ax.set_xlabel("Journée")
    ax.set_ylabel("Résultats (points)")
    ax.set_title(f"Résultats (points) : {team_1} vs {team_2}")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)
    
    return fig


def compare_gf(standings_long, team_1, team_2,col1="red",col2="blue"):
    """plots the accumulated number of goals scored by team_1 and team_2
    """
    df1=standings_long[standings_long["team"]==team_1]
    df2=standings_long[standings_long["team"]==team_2]

    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Tracer les courbes
    ax.step(df1["matchday"], df1["gf_cum"], where="post", label=team_1, color=f"tab:{col1}")
    ax.step(df2["matchday"], df2["gf_cum"], where="post", label=team_2, color=f"tab:{col2}")

    #plt.plot(df1["matchday"], df1["rank"], marker="o", label=team_1, color="tab:blue")
    #plt.plot(df2["matchday"], df2["rank"], marker="o", label=team_2, color="tab:red")
    
    # Ajouter des labels et un titre
    ax.set_xlabel("Journée")
    ax.set_ylabel("Buts marqués")
    ax.set_title(f"Buts marqués (cumulés) : {team_1} vs {team_2}")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)
    
    return fig

def compare_ga(standings_long, team_1, team_2,col1="red",col2="blue"):
    """plots the accumulated number of goals scored against team_1 and team_2
    """
    df1=standings_long[standings_long["team"]==team_1]
    df2=standings_long[standings_long["team"]==team_2]

    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Tracer les courbes
    ax.step(df1["matchday"], df1["ga_cum"], where="post", label=team_1, color=f"tab:{col1}")
    ax.step(df2["matchday"], df2["ga_cum"], where="post", label=team_2, color=f"tab:{col2}")

    #plt.plot(df1["matchday"], df1["rank"], marker="o", label=team_1, color="tab:blue")
    #plt.plot(df2["matchday"], df2["rank"], marker="o", label=team_2, color="tab:red")
    ax.invert_yaxis()

    # Ajouter des labels et un titre
    ax.set_xlabel("Journée")
    ax.set_ylabel("Buts encaissés")
    ax.set_title(f"Buts encaissés (cumulés) : {team_1} vs {team_2}")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)
    
    return fig

def compare_gdif(standings_long, team_1, team_2,col1="red",col2="blue"):
    """plots the goal average of team_1 and team_2
    """
    df1=standings_long[standings_long["team"]==team_1]
    df2=standings_long[standings_long["team"]==team_2]

    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Tracer les courbes
    ax.step(df1["matchday"], df1["gdif_cum"], where="post", label=team_1, color=f"tab:{col1}")
    ax.step(df2["matchday"], df2["gdif_cum"], where="post", label=team_2, color=f"tab:{col2}")

    #plt.plot(df1["matchday"], df1["rank"], marker="o", label=team_1, color="tab:blue")
    #plt.plot(df2["matchday"], df2["rank"], marker="o", label=team_2, color="tab:red")
    
    # Ajouter des labels et un titre
    ax.set_xlabel("Journée")
    ax.set_ylabel("Goal average")
    ax.set_title(f"Goal average : {team_1} vs {team_2}")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)
    
    return fig

def vizualisation_prediction(df):
    '''une visualisation plotly des prédictions'''
    df_home=df.copy()
    df_home["Issue"]="Domicile"
    df_home["proba"]=round(df_home["HOME_TEAM"]*100,1)
    df_draw=df.copy()
    df_draw["Issue"]="Nul"
    df_draw["proba"]=round(100*df_home["DRAW"],1)
    df_away=df.copy()
    df_away["Issue"]="Exterieur"
    df_away["proba"]=round(100*df_home["AWAY_TEAM"],1)

    df_long=pd.concat([df_home,df_draw,df_away])
    df_long.drop(columns=["AWAY_TEAM","DRAW","HOME_TEAM"],inplace=True)
    df_long.sort_values(by="game_name",inplace=True)
    fig = px.bar(
        df_long,
        x="proba",
        y="game_name",
        color="Issue",
        orientation="h",
        category_orders={
        "Issue": ["Domicile", "Nul", "Exterieur"]
    },
        color_discrete_map={
        "Domicile":  "#1042A7", 
        "Nul":       "#A7A7A7",  # gris
        "Exterieur": "#810191"  
    },
    labels={"game_name":"Match","proba":"Probabilité (%)"}
    )
    return fig
