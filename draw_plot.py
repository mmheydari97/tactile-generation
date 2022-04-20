import os
import random
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from utils import draw_grids, postprocessing, maskgen
from polygon_gen import generate_polygon

np_load_old = np.load
np.load = lambda *a,**k: np_load_old(*a, allow_pickle=True, **k)


def draw_pair(color, grid_param=0.4, figsize=(5,5), filename=None, **kwargs):
    grid_p = 0 # np.random.rand() 
    # plot source image
    with plt.style.context('default'):
    
        fig = plt.figure(figsize=figsize)
        ax = plt.gca()
        ax.set_xticklabels('')
        ax.set_yticklabels('')

        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_axisbelow(True)
        ax.spines['left'].set_position('zero')
        ax.spines['left'].set_zorder(2)
        ax.spines['left'].set_linewidth(2)

        ax.spines['bottom'].set_position('zero')
        ax.spines['bottom'].set_zorder(2)
        ax.spines['bottom'].set_linewidth(2)

        ax.plot((1), (0), ls="", marker=">", ms=10, color="k",
        transform=ax.get_yaxis_transform(), clip_on=False, zorder=2)
        ax.plot((0), (1), ls="", marker="^", ms=10, color="k",
        transform=ax.get_xaxis_transform(), clip_on=False, zorder=2)
        ax.tick_params(length=5)


        if "bezier" in kwargs:
            b = kwargs["bezier"]
            plt.plot(b[:,0], b[:,1], c=color, zorder=3)

        if "scatter" in kwargs and kwargs["scatter"] is not None:
            points = kwargs["scatter"]
            plt.scatter(points[:,0], points[:,1], s=50, c=color, zorder=4)

        if "polygon" in kwargs:
            polygon = kwargs["polygon"]
            plt.fill(polygon[:,0], polygon[:,1], fc=f"{color}33", ec=color, zorder=3)

        if grid_p < grid_param:
            draw_grids(ax)
       
        
        fig.savefig(f'./source/s_{filename}.png', dpi=300)
        postprocessing(f'./source/s_{filename}.png')
        plt.close('all')


    # plot target image
    with plt.style.context('default'):
        fig = plt.figure(figsize=figsize)
        ax = plt.gca()
        ax.set_xticklabels('')
        ax.set_yticklabels('')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_axisbelow(True)
        ax.tick_params(direction='inout', length=20, width=1)

        if "bezier" in kwargs:
            b = kwargs["bezier"]
            plt.plot(b[:,0], b[:,1], c="w", lw=1)

        if "scatter" in kwargs and kwargs["scatter"] is not None:
            points = kwargs["scatter"]
            plt.scatter(points[:,0], points[:,1], s=1, c="w")

        if "polygon" in kwargs:
            polygon = kwargs["polygon"]
            plt.fill(polygon[:,0], polygon[:,1], fc="#ffffff00", ec="w")

        
        ax.spines['left'].set_position('zero')
        ax.spines['left'].set_zorder(2)
        ax.spines['left'].set_linewidth(2)
        ax.spines['bottom'].set_position('zero')
        ax.spines['bottom'].set_zorder(2)
        ax.spines['bottom'].set_linewidth(2)

        ax.plot((1), (0), ls="", marker=">", ms=10, color="k",
        transform=ax.get_yaxis_transform(), clip_on=False, zorder=2)
        ax.plot((0), (1), ls="", marker="^", ms=10, color="k",
        transform=ax.get_xaxis_transform(), clip_on=False, zorder=2)

        fig.savefig(f'./tactile/t_{filename}_axes.png', dpi=300)
        
        ax.tick_params(color="w")
        ax.spines['left'].set_color('w')
        ax.spines['bottom'].set_color('w')
        ax.plot((1), (0), ls="", marker=">", ms=11, color="w",
        transform=ax.get_yaxis_transform(), clip_on=False)
        ax.plot((0), (1), ls="", marker="^", ms=11, color="w",
        transform=ax.get_xaxis_transform(), clip_on=False)
        

        if grid_p < grid_param:
            draw_grids(ax, color='k', linestyle='--', linewidth=1)
        
        fig.savefig(f'./tactile/t_{filename}_grids.png', dpi=300)
        plt.grid(False)


        if "bezier" in kwargs:
            plt.plot(b[:,0], b[:,1], clip_on=False, c='k', lw=4, zorder=3)
        if "scatter" in kwargs and kwargs["scatter"] is not None:
            plt.scatter(points[:,0], points[:,1], s=300, c='k', ec='w', lw=5, zorder=4)

        if "polygon" in kwargs:
            polygon = kwargs["polygon"]
            plt.fill(polygon[:,0], polygon[:,1], fc="#ffffff00", ec='k', lw=4, zorder=3)


        fig.savefig(f'./tactile/t_{filename}_content.png', dpi=300)
        maskgen(f'./tactile/t_{filename}.png')

    
for i in range(20):
    PLOT_COLOR = "#"+''.join([random.choice('0123456789abcdef') for _ in range(6)])
    GRID_PARAM = random.random()
    FIG_SIZE = random.choices([[5,5], [2.5,5], [5,2.5]], weights=[.5, .25, .25])[0]
    b = np.load(f"./points/{i+1}.npy")
    pointidx = np.random.randint(10)
    ps = b[0::b.shape[0]//pointidx,:] if pointidx > 0 else None
    draw_pair(PLOT_COLOR,GRID_PARAM,FIG_SIZE, f"{i+1}", bezier=b, scatter=ps)
    
for i in range(20, 35):
    PLOT_COLOR = "#"+''.join([random.choice('0123456789abcdef') for _ in range(6)])
    GRID_PARAM = random.random()
    FIG_SIZE = random.choices([[5,5], [2.5,5], [5,2.5]], weights=[.5, .25, .25])[0]

    ps = generate_polygon(center=(random.random()*2-1, random.random()*2-1),
                        avg_radius=1.5,
                        irregularity=0.2,
                        spikiness=0.1,
                        num_vertices=np.random.randint(3,10))
    draw_pair(PLOT_COLOR,GRID_PARAM,FIG_SIZE, f"{i+1}", scatter=ps, polygon=ps)

for i in range(35, 50):
    PLOT_COLOR = "#"+''.join([random.choice('0123456789abcdef') for _ in range(6)])
    GRID_PARAM = random.random()
    FIG_SIZE = random.choices([[5,5], [2.5,5], [5,2.5]], weights=[.5, .25, .25])[0]
    idx = np.random.randint(2,20)

    ps = np.array([[random.random()*100-50, random.random()*100-50] for _ in range(idx)])
    draw_pair(PLOT_COLOR,GRID_PARAM,FIG_SIZE, f"{i+1}", scatter=ps)
    plt.close('all')
