import numpy as np
from collections import deque

class Simulator:
    def __init__(self, size, neighborhood):
        self.size = size
        self.neighborhood = neighborhood
        
        # -1 = Susceptible Initial (needs contact) = -1
        # 0 = Exposed, 1 = Infected(g1), 2 = Infected(g2), 3 = Recovered, 4 = Susceptible(cycle)
        self.states = np.full((size, size), -1, dtype=int)
        self.labels = np.full((size, size), -1, dtype=int)
        self.configure_initial_state()

    def get_neighbors_coords(self, i, j):
        offsets = {
            'VN': [(0,1), (0,-1), (1,0), (-1,0)],
            'moore': [(di, dj) for di in [-1,0,1] for dj in [-1,0,1] if not (di==0 and dj==0)],
            'L': [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1, 2), (-1,-2)]
        }
        coords = []
        for di, dj in offsets[self.neighborhood]:
            ni, nj = (i + di) % self.size, (j + dj) % self.size
            coords.append((ni, nj))
        return coords
    
    def configure_initial_state(self):
        center = self.size // 2
        
        # Set up the labels using BFS to assign distances from the source
        queue = deque([(center, center)])
        self.labels[center, center] = 0
        while queue:
            ci, cj = queue.popleft()
            current_dist = self.labels[ci, cj]
            for ni, nj in self.get_neighbors_coords(ci, cj):
                if self.labels[ni, nj] == -1:
                    self.labels[ni, nj] = current_dist + 1
                    queue.append((ni, nj))


        #Initial state: center is infected, neighbors are exposed
        self.states[center, center] = 1 # Infected
        for ni, nj in self.get_neighbors_coords(center, center):
            self.states[ni, nj] = 0 # Exposed

    def step(self):
        new_states = self.states.copy()

        # PASS 1: Automatic progression of states
        # All nodes that have been touched by the disease advance 1 stage
        for i in range(self.size):
            for j in range(self.size):
                if self.states[i, j] != -1:
                    new_states[i, j] = (self.states[i, j] + 1) % 5

        # PASS 2: Initial susceptible nodes (-1) become exposed (0) if they have an infected neighbor (1 or 2)
        for i in range(self.size):
            for j in range(self.size):
                if self.states[i, j] == -1:
                    neighbors = self.get_neighbors_coords(i, j)
                    if any(new_states[ni, nj] in [1, 2] for ni, nj in neighbors):
                        new_states[i, j] = 0

        self.states = new_states