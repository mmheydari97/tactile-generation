import os
import random
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from utils import draw_grids, figure2image, figure2mask
from polygon_gen import generate_polygon

np_load_old = np.load
np.load = lambda *a,**k: np_load_old(*a, allow_pickle=True, **k)


def draw_pair(color, grid_param=0.4, figsize=(5,5), filename=None, **kwargs):
    grid_p = np.random.rand() 
    # plot source image
    with plt.style.context('default'):
    
        fig = plt.figure(figsize=figsize)
        ax = plt.gca()
        ax.set_xticklabels('')
        ax.set_yticklabels('')
        if "bezier" in kwargs:
            b = kwargs["bezier"]
            plt.plot(b[:,0], b[:,1], c=color)

        if "scatter" in kwargs and kwargs["scatter"] is not None:
            points = kwargs["scatter"]
            plt.scatter(points[:,0], points[:,1], s=50, c=color, zorder=3)

        if "polygon" in kwargs:
            polygon = kwargs["polygon"]
            plt.fill(polygon[:,0], polygon[:,1], fc=f"{color}33", ec=color)

        if grid_p < grid_param:
            draw_grids(ax)
       
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_axisbelow(True)
        ax.spines['left'].set_position('zero')
        ax.spines['left'].set_zorder(0)
        ax.spines['left'].set_linewidth(2)

        ax.spines['bottom'].set_position('zero')
        ax.spines['bottom'].set_zorder(0)
        ax.spines['bottom'].set_linewidth(2)

        ax.plot((1), (0), ls="", marker=">", ms=10, color="k",
        transform=ax.get_yaxis_transform(), clip_on=False)
        ax.plot((0), (1), ls="", marker="^", ms=10, color="k",
        transform=ax.get_xaxis_transform(), clip_on=False)
        ax.tick_params(length=5)


        figure2image(fig).save(f'./source/s_{filename}.png')


    # plot target image
    with plt.style.context('default'):
        fig = plt.figure(figsize=figsize)
        ax = plt.gca()
        ax.set_xticklabels('')
        ax.set_yticklabels('')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_axisbelow(True)
        ax.tick_params(direction='inout', length=25, width=1)

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
        ax.spines['left'].set_zorder(0)
        ax.spines['left'].set_linewidth(2)
        ax.spines['bottom'].set_position('zero')
        ax.spines['bottom'].set_zorder(0)
        ax.spines['bottom'].set_linewidth(2)

        ax.plot((1), (0), ls="", marker=">", ms=10, color="k",
        transform=ax.get_yaxis_transform(), clip_on=False)
        ax.plot((0), (1), ls="", marker="^", ms=10, color="k",
        transform=ax.get_xaxis_transform(), clip_on=False)

        mask_axes = figure2mask(fig)

        ax.tick_params(direction='inout', length=0, width=0)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.plot((1), (0), ls="", marker=">", ms=15, color="w",
        transform=ax.get_yaxis_transform(), clip_on=False)
        ax.plot((0), (1), ls="", marker="^", ms=15, color="w",
        transform=ax.get_xaxis_transform(), clip_on=False)
        

        if grid_p < grid_param:
            draw_grids(ax, color='k', linestyle='--', linewidth=1)
        
        mask_grid = figure2mask(fig)        
        plt.grid(False)


        if "bezier" in kwargs:
            plt.plot(b[:,0], b[:,1], zorder=2, clip_on=False, c='k', lw=4)
        if "scatter" in kwargs and kwargs["scatter"] is not None:
            plt.scatter(points[:,0], points[:,1], s=300, c='k', ec='w', lw=5, zorder=3)

        if "polygon" in kwargs:
            polygon = kwargs["polygon"]
            plt.fill(polygon[:,0], polygon[:,1], fc="#ffffff00", ec='k', lw=4)


        mask_plot = figure2mask(fig)
        res = np.zeros(mask_plot.shape, dtype=np.uint8)
        res = mask_plot*3 
        res[(mask_grid>0) & (mask_plot==0)] = 2
        res[(mask_axes>0) & (mask_plot==0)] = 1
        im_res = Image.fromarray(res, mode="L")
        im_res.save(f'./tactile/t_{filename}.tiff')

    
for i in range(2000):
    PLOT_COLOR = "#"+''.join([random.choice('0123456789abcdef') for _ in range(6)])
    GRID_PARAM = random.random()
    FIG_SIZE = random.choices([[5,5], [2.5,5], [5,2.5]], weights=[.5, .25, .25])[0]
    b = np.load(f"./points/{i+1}.npy")
    pointidx = np.random.randint(10)
    ps = b[0::b.shape[0]//pointidx,:] if pointidx > 0 else None
    draw_pair(PLOT_COLOR,GRID_PARAM,FIG_SIZE, f"{i+1}", bezier=b, scatter=ps)
    
for i in range(2000, 3500):
    PLOT_COLOR = "#"+''.join([random.choice('0123456789abcdef') for _ in range(6)])
    GRID_PARAM = random.random()
    FIG_SIZE = random.choices([[5,5], [2.5,5], [5,2.5]], weights=[.5, .25, .25])[0]

    ps = generate_polygon(center=(random.random()*2-1, random.random()*2-1),
                        avg_radius=1.5,
                        irregularity=0.2,
                        spikiness=0.1,
                        num_vertices=np.random.randint(3,10))
    draw_pair(PLOT_COLOR,GRID_PARAM,FIG_SIZE, f"{i+1}", scatter=ps, polygon=ps)

for i in range(3500, 5000):
    PLOT_COLOR = "#"+''.join([random.choice('0123456789abcdef') for _ in range(6)])
    GRID_PARAM = random.random()
    FIG_SIZE = random.choices([[5,5], [2.5,5], [5,2.5]], weights=[.5, .25, .25])[0]
    idx = np.random.randint(2,20)

    ps = np.array([[random.random()*100-50, random.random()*100-50] for _ in range(idx)])
    draw_pair(PLOT_COLOR,GRID_PARAM,FIG_SIZE, f"{i+1}", scatter=ps)
    plt.close('all')
