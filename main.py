# Main script: controls the loop of p and calls the engine.py
import os

from modules.engine import Simulator
import matplotlib.pyplot as plt
import numpy as np
from modules.utils import plot_comparative_history, plot_grid_generation, plot_history, save_history_to_csv

def run_simulation(sim, generations=12):
    history = {'Susceptible': [], 'Exposed': [], 'Infected': [], 'Recovered': []}
    
    for g in range(generations):
        # -1 e 4 são Suscetíveis. 1 e 2 são Infectados.
        counts = {
            'Susceptible': int(np.sum((sim.states == -1) | (sim.states == 4))),
            'Exposed': int(np.sum(sim.states == 0)),
            'Infected': int(np.sum((sim.states == 1) | (sim.states == 2))),
            'Recovered': int(np.sum(sim.states == 3))
        }
        for key in history: 
            history[key].append(counts[key])
        sim.step()
        
    return history

def initiate_simulations():

    neighborhood = ['moore', 'L']
    grid_size = [10, 50, 100]
    probabilities = np.round(np.arange(0, 1.1, 0.1), 1) 

    data_by_grid = {g: {n: {} for n in neighborhood} for g in grid_size}
    base_folder = "images_human_factor"
    comp_folder = os.path.join(base_folder, "comparative_results")
    if not os.path.exists(comp_folder):
        os.makedirs(comp_folder)

    gen_config = {
        10: 15,   
        50: 65,   
        100: 110 
    }

    for n in neighborhood:
        for g in grid_size:

            for p in probabilities:
                p_str = f"{p:.1f}"

                prob_folder = os.path.join(base_folder, f"probability_{p_str}")
                sim_base_folder = os.path.join(prob_folder, f"{n}_grid_{g}")
                folder_grid = os.path.join(sim_base_folder, "grid")

                folder_csv = os.path.join("csv_human_factor", f"probability_{p_str}", f"{n}_grid_{g}")

                os.makedirs(folder_grid, exist_ok=True)
                os.makedirs(folder_csv, exist_ok=True)

                total_gens = gen_config[g]

                sim = Simulator(size=g, neighborhood=n, p=p)

                for gen in range(total_gens):
                    if g == 10:
                        plot_grid_generation(sim, gen, folder_grid, p_str)
                    sim.step()
                    
                sim_stats = Simulator(size=g, neighborhood=n, p=p)
                history = run_simulation(sim_stats, generations=total_gens)
                plot_history(history, n, g, p_str, folder_grid)
                save_history_to_csv(history, folder_csv)

                data_by_grid[g][n][p_str] = history
            
    for g in grid_size:
        for p in probabilities:
            p_str = f"{p:.1f}"
            data_by_neigh = {n: data_by_grid[g][n][p_str] for n in neighborhood}
            plot_comparative_history(data_by_neigh, g, p_str, comp_folder)

if __name__ == '__main__':

    initiate_simulations()