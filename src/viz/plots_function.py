import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
import pandas as pd
import plotly.graph_objects as go

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



def plot_rank_distribution(rank_probs, teams, title, xlim=(1, 18)):

    fig, ax = plt.subplots()

    for team in teams:
        ax.plot(
            rank_probs.columns,
            rank_probs.loc[team],
            marker='o',
            linestyle='-',
            label=team
        )

    ax.set_xlabel("Classement")
    ax.set_ylabel("Probabilité")
    ax.set_title(title)
    ax.legend()
    ax.grid()

    ax.set_xlim(*xlim)
    ax.set_ylim(0, 100)

    return fig

def plot_rank_distribution_plotly(rank_probs, teams, title):

    fig = go.Figure()

    x_vals = rank_probs.columns.astype(int)

    # keep only selected teams
    sub = rank_probs.loc[teams]

    # dynamic range based on where probabilities exist
    mask = sub.sum(axis=0) > 0
    x_vals = x_vals[mask.values]

    x_min, x_max = x_vals.min(), x_vals.max()

    for team in teams:
        fig.add_trace(
            go.Scatter(
                x=rank_probs.columns.astype(int),
                y=rank_probs.loc[team],
                mode='lines+markers',
                name=team
            )
        )

    fig.update_layout(
        title=title,
        xaxis_title="Classement",
        yaxis_title="Probabilité",
        xaxis=dict(range=[x_min, x_max]),
        yaxis=dict(range=[0, 100]),
        template="plotly_white"
    )

    return fig

def get_teams_by_zone(rank_probs, threshold=0.05):
    top7_prob = rank_probs.loc[:, 1:7].sum(axis=1)
    teams_top7 = top7_prob.sort_values(ascending=False)
    teams_top7 = teams_top7[teams_top7 > threshold].index.tolist()
    bottom3_prob = rank_probs.loc[:, 16:18].sum(axis=1)
    teams_bottom3 = bottom3_prob.sort_values(ascending=False)
    teams_bottom3 = teams_bottom3[teams_bottom3 > threshold].index.tolist()

    teams_other = rank_probs.index.difference(
        set(teams_top7).union(set(teams_bottom3))
    ).tolist()

    return teams_top7, teams_bottom3, teams_other

def plot_all_zones(rank_probs):
    teams_top7, teams_bottom3, teams_other = get_teams_by_zone(rank_probs)

    fig_top = plot_rank_distribution_plotly(
        rank_probs,
        teams_top7,
        "Probabilité Top 7"
    )

    fig_bottom = plot_rank_distribution_plotly(
        rank_probs,
        teams_bottom3,
        "Probabilité Relégation (Bottom 3)"
    )

    fig_other = plot_rank_distribution_plotly(
        rank_probs,
        teams_other,
        "Autres équipes"
    )

    return fig_top, fig_bottom, fig_other
