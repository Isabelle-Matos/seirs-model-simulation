# Contains auxiliars functions

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from modules.engine import Simulator
import csv
import os

def plot_grid_generation(sim, gen_number, folder_path):
    plt.figure(figsize=(4, 4))
    
    # Soma +1 nos estados para que o menor valor (-1) vire 0 e case com a paleta
    bg_numeric = sim.states + 1 
    
    # Índices: 0(S_init), 1(E), 2(I1), 3(I2), 4(R), 5(S_ciclo)
    cmap = ListedColormap(['#FFFACD', '#D3D3D3', '#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFACD'])
    
    plt.imshow(bg_numeric, cmap=cmap, vmin=0, vmax=5)
    
    dynamic_fontsize = max(1, int(100 / sim.size))
    rows, cols = sim.states.shape
    
    for i in range(rows):
        for j in range(cols):
            state = sim.states[i, j]
            label = sim.labels[i, j]
            
            # O texto só aparece se a label for <= geração atual E se o estado não for -1.
            # Isso garante que no Exposto(Geração Inicial), o fundo seja Cinza e o texto fique invisível!
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
    
    plt.title(f'Generation {gen_number}')
    plt.tight_layout()
    plt.savefig(f"{folder_path}/grid_gen_{gen_number}.png", dpi=300)
    plt.close()


def plot_history(history, n, g):
    
    total_nodes = g * g
    #total_nodes = history['Susceptible'][0] + history['Exposed'][0] + history['Infected'][0] + history['Recovered'][0]

    plt.figure(figsize=(6, 5))

    styles = {'Susceptible': ':', 'Exposed': ':', 'Infected': ':', 'Recovered': ':'}
    colors = {'Susceptible': 'blue', 'Exposed': 'orange', 'Infected': 'red', 'Recovered': 'green'}

    generations = len(history['Susceptible'])

    for state, data in history.items():
        percentage_data = [(v / total_nodes) * 100 for v in data]
        plt.plot(percentage_data, label=state, color=colors[state], 
                 linestyle=styles[state], linewidth=2, marker='o', markersize=1)
    
    plt.title(f"SEIRS Model\n{n} neighborhood, N = {g}")
    plt.xlabel("Generation")
    plt.ylabel("Percentage of nodes")

    plt.ylim(0, 105)
    plt.xlim(0, 12)
    plt.xticks(range(0, 13))

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=4, frameon=False)
    plt.tight_layout()

    output_path = f"images/{n}_grid_{g}/epidemic_curves.png"
    plt.savefig(output_path)
    plt.close()

def save_history_to_csv(history, folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        
    csv_path = os.path.join(folder_path, "stats.csv")
    
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Generation', 'S', 'E', 'I', 'R'])
        
        # Escreve os dados linha por linha
        generations = len(history['Susceptible'])
        for i in range(generations):
            writer.writerow([
                f"Gen.{i}", 
                history['Susceptible'][i], 
                history['Exposed'][i], 
                history['Infected'][i], 
                history['Recovered'][i]
            ])


def plot_comparative_history(all_histories, grid_size, output_folder):
    states = ['Susceptible', 'Exposed', 'Infected', 'Recovered']
    
    generations = len(all_histories['VN']['Susceptible'])

    for state in states:
        plt.figure(figsize=(8, 5))
        for neigh, history in all_histories.items():
            plt.plot(range(len(history[state])), history[state], label=neigh)
        
        plt.title(f'Evolution of the {state.upper()} nodes (Grid: {grid_size})')
        plt.xlabel('Generation')
        plt.ylabel('Number of nodes')

        plt.xlim(0, generations - 1) # O eixo X acompanha o total de gerações dinamicamente
        
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"{output_folder}/comparative_{state}_N{grid_size}.png")
        plt.close()