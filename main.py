# Main script: controls the loop of p and calls the engine.py
import os

from modules.engine import Simulator
import matplotlib.pyplot as plt
import numpy as np
from modules.utils import plot_comparative_history, plot_grid_generation, plot_history, save_history_to_csv

if not os.path.exists('images'):
    os.makedirs('images')

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

    neighborhood = ['VN', 'moore', 'L']
    grid_size = [10, 50, 100]  

    comp_folder = "images/comparative_results"
    if not os.path.exists(comp_folder):
        os.makedirs(comp_folder)

    gen_config = {
        10: 15,   
        50: 65,   
        100: 110 
    }

    data_by_grid = {g: {} for g in grid_size}
    

    for n in neighborhood:
        for g in grid_size:

            folder_path = f"images/{n}_grid_{g}"
            folder_csv = f"csv_first_part/{n}_grid_{g}"

            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            if not os.path.exists(folder_csv):
                os.makedirs(folder_csv)

            total_gens = gen_config[g]

            sim = Simulator(size=g, neighborhood=n)

            for gen in range(12, total_gens):
                plot_grid_generation(sim, gen, folder_path)
                sim.step()
                
            sim_stats = Simulator(size=g, neighborhood=n)
            history = run_simulation(sim_stats, generations=total_gens)
            plot_history(history, n, g)
            save_history_to_csv(history, folder_csv)

            data_by_grid[g][n] = history
            
    for g in grid_size:
        plot_comparative_history(data_by_grid[g], g, comp_folder)

if __name__ == '__main__':

    initiate_simulations()