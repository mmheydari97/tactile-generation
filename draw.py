import os
import random
import sys
import numpy as np
import matplotlib.pyplot as plt
from math import comb


file_count = len(next(os.walk("./points"))[2])


def draw_grids(ax):
    ax.set_zorder(0)
    plt.grid(which='both', axis='both', color='k', linestyle='--')
    
for i in range(file_count):
    PLOT_COLOR = "#"+''.join([random.choice('0123456789abcdef') for j in range(6)])
    GRID_PARAM = random.random()
    FIG_SIZE = random.choices([[10,10], [10,20], [20,10]], weights=[.5, .25, .25])[0]
    b = np.load(f"./points/{i+1}.npy")

    with plt.style.context(random.choice(plt.style.available)):
        fig1 = plt.figure(figsize=FIG_SIZE)
        ax1 = plt.gca()
        ax1.set_xticklabels('')
        ax1.set_yticklabels('')
        plt.plot(b[:,0], b[:,1], c=PLOT_COLOR)
        if GRID_PARAM < 0.25:
            draw_grids(ax1)
        plt.savefig(f'./source/s_{i+1}.jpg')
        
    

    with plt.style.context('default'):
        fig2 = plt.figure(figsize=FIG_SIZE)
        ax2 = plt.gca()
        ax2.set_xticklabels('')
        ax2.set_yticklabels('')
        ax2.spines['right'].set_visible(False)
        ax2.spines['top'].set_visible(False)
        ax2.set_axisbelow(True)
        ax2.tick_params(direction='inout', length=20, width=2)
        plt.plot(b[:,0], b[:,1], zorder=1, c=PLOT_COLOR, lw=5)
        if GRID_PARAM < 0.25:
            draw_grids(ax2)
        cross = np.load(f"./intersections/{i+1}.npy")
        if cross.size != 0:
            plt.scatter(cross[:,0], cross[:,1], s=350, c=PLOT_COLOR, edgecolors='w', lw=6, zorder=2)
        plt.savefig(f'./tactile/t_{i+1}.svg')

