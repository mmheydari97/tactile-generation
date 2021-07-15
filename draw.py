import random
import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from scipy.interpolate import interp1d
from math import comb

PLOT_COLOR = "#"+''.join([random.choice('0123456789abcdef') for j in range(6)])
GRID_PARAM = random.random()
P_1D = 0.25
FIG_SIZE = random.choices([[10,10], [10,20], [20,10]], weights=[.5, .25, .25])[0]

def bezier(x, P):
    n = P.shape[0]
    b = 0

    for i in range(n):
        a = comb(n,i)*((1-x)**(n-i))*(x**i)
        b = b + a*P[i].reshape(1,-1)

    if b.shape[1] == 1:
        b = np.concatenate((x,b), axis=1)
    return b

x = np.linspace(0, 1, 10000).reshape(-1,1)
P = np.array([[random.randint(-20,20), random.randint(-20,20)] for i in range(random.randint(2,20))])

if random.random() <= P_1D:
    P = P.reshape(-1,1).flatten()[::2]


b = bezier(x, P)

def draw_grids(axis):
    ax1.set_zorder(0)
    plt.grid(which='both', axis='both', color='k', linestyle='--')


with plt.style.context(random.choice(plt.style.available)):
    fig1 = plt.figure(figsize=FIG_SIZE)
    ax1 = plt.gca()
    ax1.set_xticklabels('')
    ax1.set_yticklabels('')
    plt.plot(b[:,0], b[:,1], c=PLOT_COLOR)
    if GRID_PARAM < 0.25:
        draw_grids(ax1)
    plt.savefig('test.jpg')
    

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
    plt.savefig('test.svg')

