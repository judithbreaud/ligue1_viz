from src.simulation import run_one_simulation
import pandas as pd
def run_monte_carlo(n_simulations,probas,classes,unplayed,played,old_goal_dif):
    results = []
    
    for sim in range(n_simulations):
        sim_result = run_one_simulation(probas,classes,unplayed,played,old_goal_dif)
        results.append(sim_result)
    
    return pd.concat(results)

def compute_rank_probabilities(res_monte_carlo, n_simulations):
    rank_probs = (
        res_monte_carlo
        .groupby(["team", "rank"])
        .size()
        .unstack(fill_value=0)
    )

    rank_probs = rank_probs * 100 / n_simulations
    return rank_probs