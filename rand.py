import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import random
import sys

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
random.shuffle(colors)

fig = plt.figure(figsize=(10,10))
plt.grid(which='both', axis='both', color='k', linestyle='--')
ax = plt.gca()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.set_axisbelow(True)
ax.set_xticklabels('')
ax.set_yticklabels('')
ax.tick_params(direction='inout', length=20, width=2)
ax.get_facecolor()


if np.random.uniform()>0.5:
    rn = np.random.randint(0,5,size=(3,2))
    t1 = plt.Polygon([[1+rn[0,0],10+rn[0,1]], [1+rn[1,0], 5+rn[1,1]], [2+rn[2,0],5+rn[2,1]]], color=colors[0], fill=False, lw=4)
    plt.scatter([1+rn[0,0],1+rn[1,0],2+rn[2,0]], [10+rn[0,1],5+rn[1,1],5+rn[2,1]], s=350, c=colors[0], edgecolors='w', lw=6, zorder=2)
    ax.add_patch(t1)
if np.random.uniform()>0.5:
    pos = np.random.randint(0,10, size=(np.random.randint(1,6),2))
    plt.scatter(pos[:,0], pos[:,1], s=350, c=colors[1], edgecolors='w', lw=6, zorder=2)
if np.random.uniform()>0.5:
    rn = np.random.randint(0,5,size=(2,2))
    plt.plot([0+rn[0,0],10+rn[1,0]], [0+rn[0,1],10+rn[1,1]], zorder=1, c=colors[2], lw=4)

plt.savefig(f'{sys.argv[1]}.jpg')
plt.savefig(f'{sys.argv[1]}.svg')
