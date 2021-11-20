import os
import random
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter, ImageOps
from PIL.ImageOps import invert
from utils import expand2square


file_count = len(next(os.walk("./intersections"))[2])
np_load_old = np.load
np.load = lambda *a,**k: np_load_old(*a, allow_pickle=True, **k)

def draw_grids(ax):
    ax.set_zorder(0)
    plt.grid(which='both', axis='both')
    
for i in range(file_count):
    PLOT_COLOR = "#"+''.join([random.choice('0123456789abcdef') for j in range(6)])
    GRID_PARAM = random.random()
    FIG_SIZE = random.choices([[10,10], [10,20], [20,10]], weights=[.5, .25, .25])[0]
    b = np.load(f"./points/{i+1}.npy")
    cross = np.load(f"./intersections/{i+1}.npy")
    with plt.style.context(random.choices(['classic', 'dark_background'], weights=[.9, .1])[0]):
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
        
        if cross.size != 0:
            scolor = "#{:06X}".format(16777215 - int(PLOT_COLOR.split("#")[1], 16))
            plt.scatter(cross[:,0], cross[:,1], s=350, c=scolor, edgecolors='w', lw=6, zorder=2)
        plt.savefig(f'./tactile/t_{i+1}.svg')


    with plt.style.context('default'):
        fig3 = plt.figure(figsize=FIG_SIZE)
        ax3 = plt.gca()
        ax3.set_xticklabels('')
        ax3.set_yticklabels('')
        ax3.axes.xaxis.set_visible(False)
        ax3.axes.yaxis.set_visible(False)

        for l in ax3.spines.values():
            l.set_visible(False)
        plt.plot(b[:,0], b[:,1], zorder=-1, c='w')
        if cross.size != 0:
            plt.scatter(cross[:,0], cross[:,1], zorder=1, s=3, c='k')

        plt.savefig(f'./mask/t_{i+1}.jpg')
    
    
    
    with Image.open(f'./mask/t_{i+1}.jpg') as img:
        img = invert(expand2square(img))
        img = ImageOps.equalize(img, mask=None)
        img = img.filter(ImageFilter.GaussianBlur(radius=2))
        img.save(f'./mask/t_{i+1}.jpg')

    plt.close('all')

# with open("./with_intersection.txt","w") as f:
#     for i in range(10000):
#         cross = np.load(f"./intersections/{i+1}.npy", allow_pickle=True)
#         if cross.size != 0:
#             f.writelines(f"{i+1}\n")