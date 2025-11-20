import matplotlib.pyplot as plt
def compare_rank(standings_long, team_1, team_2,col1="red",col2="blue"):
    """plots the rankings of team_1 and team_2
    """
    df1=standings_long[standings_long["team"]==team_1]
    df2=standings_long[standings_long["team"]==team_2]

    plt.figure(figsize=(10, 6))
    
    # Tracer les courbes
    plt.step(df1["matchday"], df1["rank"], where="post", label=team_1, color=f"tab:{col1}")
    plt.step(df2["matchday"], df2["rank"], where="post", label=team_2, color=f"tab:{col2}")

    #plt.plot(df1["matchday"], df1["rank"], marker="o", label=team_1, color="tab:blue")
    #plt.plot(df2["matchday"], df2["rank"], marker="o", label=team_2, color="tab:red")
    
    # Inverser l'axe y (car rang 1 = meilleur classement, on veut le mettre en haut)
    plt.gca().invert_yaxis()
    
    # Ajouter des labels et un titre
    plt.xlabel("Journée (matchday)")
    plt.ylabel("Classement (rank)")
    plt.title(f"Évolution du classement : {team_1} vs {team_2}")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    
    plt.show()

def compare_points_total(standings_long, team_1, team_2,col1="red",col2="blue"):
    """plots the total points day after day of team_1 and team_2
    """
    df1=standings_long[standings_long["team"]==team_1]
    df2=standings_long[standings_long["team"]==team_2]

    plt.figure(figsize=(10, 6))
    
    # Tracer les courbes
    plt.step(df1["matchday"], df1["points_cum"], where="post", label=team_1, color=f"tab:{col1}")
    plt.step(df2["matchday"], df2["points_cum"], where="post", label=team_2, color=f"tab:{col2}")

    #plt.plot(df1["matchday"], df1["rank"], marker="o", label=team_1, color="tab:blue")
    #plt.plot(df2["matchday"], df2["rank"], marker="o", label=team_2, color="tab:red")
    
    # Ajouter des labels et un titre
    plt.xlabel("Journée (matchday)")
    plt.ylabel("Points")
    plt.title(f"Points total : {team_1} vs {team_2}")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    
    plt.show()

def compare_resultats(standings_long, team_1, team_2,col1="red",col2="blue"):

    """plots the results of each matchday of team_1 and team_2
    """
    df1=standings_long[standings_long["team"]==team_1]
    df2=standings_long[standings_long["team"]==team_2]

    plt.figure(figsize=(10, 6))
    
    # Tracer les courbes
    plt.scatter(df1["matchday"], df1["points"], label=team_1, color=f"tab:{col1}",marker='s')
    plt.scatter(df2["matchday"], df2["points"], label=team_2, color=f"tab:{col2}",marker="*")

    #plt.plot(df1["matchday"], df1["rank"], marker="o", label=team_1, color="tab:blue")
    #plt.plot(df2["matchday"], df2["rank"], marker="o", label=team_2, color="tab:red")
    
    # Ajouter des labels et un titre
    plt.xlabel("Journée (matchday)")
    plt.ylabel("Résultats (points)")
    plt.title(f"Résultats (points) : {team_1} vs {team_2}")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    
    plt.show()


def compare_gf(standings_long, team_1, team_2,col1="red",col2="blue"):
    """plots the accumulated number of goals scored by team_1 and team_2
    """
    df1=standings_long[standings_long["team"]==team_1]
    df2=standings_long[standings_long["team"]==team_2]

    plt.figure(figsize=(10, 6))
    
    # Tracer les courbes
    plt.step(df1["matchday"], df1["gf_cum"], where="post", label=team_1, color=f"tab:{col1}")
    plt.step(df2["matchday"], df2["gf_cum"], where="post", label=team_2, color=f"tab:{col2}")

    #plt.plot(df1["matchday"], df1["rank"], marker="o", label=team_1, color="tab:blue")
    #plt.plot(df2["matchday"], df2["rank"], marker="o", label=team_2, color="tab:red")
    
    # Ajouter des labels et un titre
    plt.xlabel("Journée (matchday)")
    plt.ylabel("Buts marqués")
    plt.title(f"Buts marqués (cumulés) : {team_1} vs {team_2}")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    
    plt.show()

def compare_ga(standings_long, team_1, team_2,col1="red",col2="blue"):
    """plots the accumulated number of goals scored against team_1 and team_2
    """
    df1=standings_long[standings_long["team"]==team_1]
    df2=standings_long[standings_long["team"]==team_2]

    plt.figure(figsize=(10, 6))
    
    # Tracer les courbes
    plt.step(df1["matchday"], df1["ga_cum"], where="post", label=team_1, color=f"tab:{col1}")
    plt.step(df2["matchday"], df2["ga_cum"], where="post", label=team_2, color=f"tab:{col2}")

    #plt.plot(df1["matchday"], df1["rank"], marker="o", label=team_1, color="tab:blue")
    #plt.plot(df2["matchday"], df2["rank"], marker="o", label=team_2, color="tab:red")
    plt.gca().invert_yaxis()

    # Ajouter des labels et un titre
    plt.xlabel("Journée (matchday)")
    plt.ylabel("Buts encaissés")
    plt.title(f"Buts encaissés (cumulés) : {team_1} vs {team_2}")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    
    plt.show()

def compare_gdif(standings_long, team_1, team_2,col1="red",col2="blue"):
    """plots the goal average of team_1 and team_2
    """
    df1=standings_long[standings_long["team"]==team_1]
    df2=standings_long[standings_long["team"]==team_2]

    plt.figure(figsize=(10, 6))
    
    # Tracer les courbes
    plt.step(df1["matchday"], df1["gdif_cum"], where="post", label=team_1, color=f"tab:{col1}")
    plt.step(df2["matchday"], df2["gdif_cum"], where="post", label=team_2, color=f"tab:{col2}")

    #plt.plot(df1["matchday"], df1["rank"], marker="o", label=team_1, color="tab:blue")
    #plt.plot(df2["matchday"], df2["rank"], marker="o", label=team_2, color="tab:red")
    
    # Ajouter des labels et un titre
    plt.xlabel("Journée (matchday)")
    plt.ylabel("Goal average")
    plt.title(f"Goal average : {team_1} vs {team_2}")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    
    plt.show()
