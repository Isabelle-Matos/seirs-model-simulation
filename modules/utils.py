# Contains auxiliars functions

import glob
import pandas as pd 

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from modules.engine import Simulator
import csv
import os

def plot_grid_generation(sim, gen_number, folder_path, p_str):
    plt.figure(figsize=(4, 4))

    bg_numeric = sim.states + 1 
    
    # i: 0(S_init), 1(E), 2(I1), 3(I2), 4(R), 5(S_cicle)
    cmap = ListedColormap(['#FFFACD', '#D3D3D3', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFACD'])
    
    plt.imshow(bg_numeric, cmap=cmap, vmin=0, vmax=5)
    
    dynamic_fontsize = max(1, int(100 / sim.size))
    rows, cols = sim.states.shape
    
    for i in range(rows):
        for j in range(cols):
            state = sim.states[i, j]
            label = sim.labels[i, j]
            
            if label != -1 and label <= gen_number:
                if state in [1, 2]:
                    text_color = 'red'          
                elif state == 3:
                    text_color = '#00AA00'        
                else:
                    text_color = 'black'        
                    
                plt.text(j, i, str(label), ha='center', va='center', color=text_color, fontsize=dynamic_fontsize)
    
    grid_linewidth = 0.5 if cols <= 20 else 0.1
    plt.grid(which='major', color='gray', linestyle='-', linewidth=grid_linewidth)
    plt.xticks(np.arange(-.5, cols, 1), [])
    plt.yticks(np.arange(-.5, rows, 1), [])
    plt.tick_params(axis='both', which='both', length=0)
    
    plt.title(f'Generation Generation {gen_number} | p = {p_str}')
    plt.tight_layout()
    plt.savefig(f"{folder_path}/grid_gen_{gen_number}_{p_str}.png", dpi=300)
    plt.close()


def plot_history(history, n, g, p_str, folder_path):
    
    total_nodes = g * g

    plt.figure(figsize=(6, 5))
    styles = {'Susceptible': ':', 'Exposed': ':', 'Infected': ':', 'Recovered': ':'}
    colors = {'Susceptible': 'blue', 'Exposed': 'orange', 'Infected': 'red', 'Recovered': 'green'}

    generations = len(history['Susceptible'])

    for state, data in history.items():
        percentage_data = [(v / total_nodes) * 100 for v in data]
        plt.plot(percentage_data, label=state, color=colors[state], 
                 linestyle=styles[state], linewidth=2, marker='o', markersize=1)
    
    plt.title(f"SEIRS Model\n{n} neighborhood, N = {g}, p = {p_str}")
    plt.xlabel("Generation")
    plt.ylabel("Percentage of nodes")

    plt.ylim(0, 105)
    plt.xlim(0, generations - 1)

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=4, frameon=False)
    plt.tight_layout()

    output_path = os.path.join(folder_path, "epidemic_curves.png")
    plt.savefig(output_path)
    plt.close()

def save_history_to_csv(history, folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        
    csv_path = os.path.join(folder_path, "stats.csv")
    
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Generation', 'S', 'E', 'I', 'R'])
        
        generations = len(history['Susceptible'])
        for i in range(generations):
            writer.writerow([
                f"Gen.{i}", 
                history['Susceptible'][i], 
                history['Exposed'][i], 
                history['Infected'][i], 
                history['Recovered'][i]
            ])


def plot_comparative_history(all_histories, grid_size, p_str, output_folder):
    states = ['Susceptible', 'Exposed', 'Infected', 'Recovered']
    total_nodes = grid_size * grid_size
    generations = len(all_histories['moore']['Susceptible'])


    first_neigh = list(all_histories.keys())[0]
    generations = len(all_histories[first_neigh]['Susceptible'])

    for state in states:
        plt.figure(figsize=(8, 5))
        for neigh, history in all_histories.items():
            plt.plot(history[state], label=neigh, linewidth=2)
        
        plt.title(f'Evolution of the {state.upper()} nodes (Grid: {grid_size}), p = {p_str}')
        plt.xlabel('Generation')
        plt.ylabel('Number of nodes')

        plt.xlim(0, generations - 1)

        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"{output_folder}/comparative_{state}_N{grid_size}_p{p_str}.png")
        plt.close()

def analyze_results(root_path, exit_path):
    if not os.path.exists(exit_path):
        os.makedirs(exit_path)

    files = glob.glob(os.path.join(root_path, "**", "stats.csv"), recursive=True)
    result = []

    for f in files:
        slice = f.split(os.sep)
        p_valor = float(slice[-3].split('_')[1])
        config_grid = slice[-2] # Ex: L_grid_10
        
        df = pd.read_csv(f)
        
        estability = df['I'].std() 
        max_infected = df['I'].max()
        
        result.append({
            'p': p_valor, 
            'config': config_grid, 
            'I_max': max_infected, 
            'estabilidade_std': estability
        })

    df_resume = pd.DataFrame(result)
    
    df_resume.to_csv(os.path.join(exit_path, "complete_analysis.csv"), index=False)
    df_stable = df_resume.nsmallest(3, 'estabilidade_std')
    df_stable.to_csv(os.path.join(exit_path, "cenarios_mais_estaveis.csv"), index=False)
    
    df_resume['grid_size'] = df_resume['config'].apply(lambda x: x.split('_')[-1])

    for size in df_resume['grid_size'].unique():
        plt.figure(figsize=(8, 5))
        subset_grid = df_resume[df_resume['grid_size'] == size]
        
        for config in subset_grid['config'].unique():
            subset_config = subset_grid[subset_grid['config'] == config]
            plt.plot(subset_config['p'], subset_config['estabilidade_std'], 
                     marker='o', label=config)
        
        plt.title(f'Estabilidade do Sistema: Grid {size}x{size}')
        plt.xlabel('Fator Humano (p)')
        plt.ylabel('Desvio Padrão da Instabilidade')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        plt.savefig(os.path.join(exit_path, f"grafico_estabilidade_grid_{size}.png"))
        plt.close() 

    print(f"Análise concluída com sucesso! Gráficos salvos em: {exit_path}")