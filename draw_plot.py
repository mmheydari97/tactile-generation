import argparse
import os
import random
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from weakref import ref

from utils import draw_grids, postprocessing, maskgen, get_figsize, get_rgb_color, get_random_string
from polygon_gen import generate_polygon
from bezier_generator import generate_bezier 

np_load_old = np.load
np.load = lambda *a,**k: np_load_old(*a, allow_pickle=True, **k)


def draw_pair(axes=None, grid_param=0.4, legend_param=0.2, gscale_param=0.2, figsize=(5,5), filename=None, **kwargs):
    grid_p = np.random.rand() 
    gscale_p = np.random.rand()
    
    # plot source image
    with plt.style.context('default'):
    
        fig = plt.figure(figsize=figsize)
        ax = plt.gca()
        bg_color = get_rgb_color(0.1)
        ax.set_facecolor(bg_color)

        lw = random.randint(1,5)
        tl = max(lw, random.randint(1,5))+1
        axes(ax, lw=lw, tl=tl)

        fontsize = random.randint(8, 20)
        plt.xticks(fontsize=fontsize)
        plt.yticks(fontsize=fontsize)


        if "bezier" in kwargs:
            b = kwargs["bezier"]
            plt.plot(b[:,0], b[:,1], c=get_rgb_color(1), zorder=3, label=get_random_string(10))

        if "scatter" in kwargs and kwargs["scatter"] is not None:
            points = kwargs["scatter"]
            for i in range(1,random.randint(2,5)):
                plt.scatter(points[::i,0], points[::i,1], s=50, c=get_rgb_color(1), zorder=4, label=get_random_string(10))
            

        if "polygon" in kwargs:
            polygon = kwargs["polygon"]
            plt.fill(polygon[:,0], polygon[:,1], fc=get_rgb_color(0.4), ec=get_rgb_color(1), zorder=3, label=get_random_string(10))

        if grid_p < grid_param:
            ls = random.choice(['-', '--', ':', '-.'])
            lw = random.randint(1,2)
            draw_grids(ax, color=get_rgb_color(1), linestyle=ls, linewidth=lw, alpha=0.5)
       
        if np.random.rand() < legend_param:
            ax.legend()
        
        if np.random.rand() < legend_param:
            plt.xlabel(get_random_string(20, min_length=5))

        if np.random.rand() < legend_param:
            plt.ylabel(get_random_string(20, min_length=5))

        if np.random.rand() < legend_param:
            plt.title(get_random_string(40, min_length=10))

        fig.savefig(f'./source/s_{filename}.png', dpi=75)
        postprocessing(f'./source/s_{filename}.png', gray=(gscale_p < gscale_param))
        plt.close('all')


    # plot target image
    if opt.target == "channelwise":
        with plt.style.context('default'):
            fig = plt.figure(figsize=figsize)
            ax = plt.gca()

            if "bezier" in kwargs:
                b = kwargs["bezier"]
                plt.plot(b[:,0], b[:,1], c="w", lw=1, zorder=0)

            if "scatter" in kwargs and kwargs["scatter"] is not None:
                points = kwargs["scatter"]
                plt.scatter(points[:,0], points[:,1], s=1, c="w", zorder=0)

            if "polygon" in kwargs:
                polygon = kwargs["polygon"]
                plt.fill(polygon[:,0], polygon[:,1], fc="#ffffff00", ec="w", zorder=0)

            a = axes(ax, lw=2, tl=0)
            ax.set_axisbelow(True)
            ax.tick_params(direction='inout', length=20, width=1)
            ax.set_xticklabels('')
            ax.set_yticklabels('')
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            
            fig.savefig(f'./tactile/t_{filename}_axes.tiff', dpi=75)
            
            ax.tick_params(direction='inout', length=0, width=0, zorder=3)
            
            if a is not None:
                for arrow in a:
                    ax.lines.remove(arrow())

            for _, item in ax.spines.items():
                item.set_visible(False)

            if grid_p < grid_param:
                draw_grids(ax, color='k', linestyle='--', linewidth=1)
            
            fig.savefig(f'./tactile/t_{filename}_grids.tiff', dpi=75)
            plt.grid(False)


            if "bezier" in kwargs:
                plt.plot(b[:,0], b[:,1], clip_on=False, c='k', lw=4, zorder=3)
            if "scatter" in kwargs and kwargs["scatter"] is not None:
                plt.scatter(points[:,0], points[:,1], s=300, c='k', ec='w', lw=5, zorder=4)

            if "polygon" in kwargs:
                polygon = kwargs["polygon"]
                plt.fill(polygon[:,0], polygon[:,1], fc="#ffffff00", ec='k', lw=4, zorder=3)


            fig.savefig(f'./tactile/t_{filename}_content.tiff', dpi=75)
            maskgen(f'./tactile/t_{filename}.tiff')
            plt.close('all')
    else:
        with plt.style.context('default'):
            fig = plt.figure(figsize=figsize)
            ax = plt.gca()
            a = axes(ax, lw=2, tl=0)
            ax.set_axisbelow(True)
            ax.tick_params(direction='inout', length=20, width=1)
            ax.set_xticklabels('')
            ax.set_yticklabels('')
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)

            if "bezier" in kwargs:
                plt.plot(b[:,0], b[:,1], clip_on=False, c='r', lw=4, zorder=3)
            if "scatter" in kwargs and kwargs["scatter"] is not None:
                plt.scatter(points[:,0], points[:,1], s=300, c='r', ec='w', lw=5, zorder=4)

            if "polygon" in kwargs:
                polygon = kwargs["polygon"]
                plt.fill(polygon[:,0], polygon[:,1], fc="#ffffff00", ec='r', lw=4, zorder=3)

            if grid_p < grid_param:
                draw_grids(ax, color='b', linestyle='--', linewidth=1)


            fig.savefig(f'./tactile/t_{filename}.tiff', dpi=300)
            postprocessing(f'./tactile/t_{filename}.tiff')
            plt.close('all')


def draw_arrow_axes(ax, lw=2, tl=5):

    for spine in ax.spines.values():
        spine.set_zorder(2)
        spine.set_linewidth(lw)

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')

    ax.plot((1), (0), ls="", marker=">", ms=10, color="k",
    transform=ax.get_yaxis_transform(), clip_on=False, zorder=2)
    arrow1 = ref(ax.lines[-1])

    ax.plot((0), (1), ls="", marker="^", ms=10, color="k",
    transform=ax.get_xaxis_transform(), clip_on=False, zorder=2)
    arrow2 = ref(ax.lines[-1])

    ax.tick_params(length=tl)
    return arrow1, arrow2


def draw_box_axes(ax, lw=2, tl=5):
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_zorder(2)
        spine.set_linewidth(lw)

    ax.tick_params(length=tl)

def draw_lb_axes(ax, lw=2, tl=5):
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_zorder(2)
        spine.set_linewidth(lw)

    ax.tick_params(length=tl)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', type=str, choices=['rgb', 'channelwise'], default='rgb', help='type of target domain')
    parser.add_argument("--cnt_bezier", type=int, default=2000, help="number of bezier curves")
    parser.add_argument("--cnt_scatter", type=int, default=1500, help="number of scatter points")
    parser.add_argument("--cnt_polygon", type=int, default=1500, help="number of polygons")
    parser.add_argument("--p_figsize", nargs=3, type=float, default=[.5, .25, .25], help="figure size probabilities")
    parser.add_argument("--p_1D", type=float, default=0.4, help="probability of 1D bezeir generation")
    parser.add_argument("--p_grid", type=float, default=0.4, help="probability of drawing grid")
    parser.add_argument("--p_legend", type=float, default=0.2, help="probability of drawing legends")
    parser.add_argument("--p_grayscale", type=float, default=0.2, help="probability of grayscale source domain")

    opt = parser.parse_args()

    os.makedirs('./source', exist_ok=True)
    os.makedirs('./tactile', exist_ok=True)

    lim_bezier = opt.cnt_bezier
    lim_polygon = opt.cnt_bezier + opt.cnt_polygon
    lim_scatter = opt.cnt_bezier + opt.cnt_polygon + opt.cnt_scatter
    
    new_data = True

    for i in tqdm(range(lim_bezier), desc="bezier curves"):
        clr = get_rgb_color(1)
        fig_size = get_figsize(opt.p_figsize)
        
        if new_data:
            x = np.linspace(0, 1, 10000).reshape(-1,1)
            p = np.array([[random.randint(-20,20), random.randint(-20,20)] for i in range(random.randint(2,20))])
            if random.random() <= opt.p_1D:
                p = p.reshape(-1,1).flatten()[::2]
            b = generate_bezier(x, p)
        else:
            b = np.load(f"./points/{i+1}.npy")

        pointidx = np.random.randint(10)
        ps = b[0::b.shape[0]//pointidx,:] if pointidx > 0 else None
        axes_method = random.choices([draw_arrow_axes, draw_box_axes, draw_lb_axes], weights=[.5, .25, .25])[0]
        draw_pair(axes_method,opt.p_grid,opt.p_legend,opt.p_grayscale,fig_size, f"{i+1}", bezier=b, scatter=ps)

        
    for i in tqdm(range(lim_bezier, lim_polygon), desc="polygons"):
        clr = get_rgb_color(1)
        fig_size = get_figsize(opt.p_figsize)

        ps = generate_polygon(center=(random.random()*2-1, random.random()*2-1),
                            avg_radius=1.5,
                            irregularity=0.2,
                            spikiness=0.1,
                            num_vertices=np.random.randint(3,10))

        axes_method = random.choices([draw_arrow_axes, draw_box_axes, draw_lb_axes], weights=[.5, .25, .25])[0]
        draw_pair(axes_method,opt.p_grid,opt.p_legend,opt.p_grayscale,fig_size, f"{i+1}", scatter=ps, polygon=ps)


    for i in tqdm(range(lim_polygon, lim_scatter), desc="scatter plots"):
        clr = get_rgb_color(1)
        fig_size = get_figsize(opt.p_figsize)
        idx = np.random.randint(2,20)
        ps = np.array([[random.random()*100-50, random.random()*100-50] for _ in range(idx)])
        axes_method = random.choices([draw_arrow_axes, draw_box_axes, draw_lb_axes], weights=[.5, .25, .25])[0]
        draw_pair(axes_method,opt.p_grid,opt.p_legend,opt.p_grayscale,fig_size, f"{i+1}", scatter=ps)
