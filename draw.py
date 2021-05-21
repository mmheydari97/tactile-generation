import random
import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from scipy.interpolate import interp1d
from math import comb

color = "#"+''.join([random.choice('0123456789abcdef') for j in range(6)])

def bezier(x, P):
    n = len(P)
    b = 0
    for i in range(n):
        b = b + comb(n,i)*((1-x)**(n-i))*(x**i)*P[i]
    return b

x = np.linspace(0, 1, 10000)
P = [random.randint(-20,20) for i in range(random.randint(2,20))]
b = bezier(x, P)

with plt.style.context(random.choice(plt.style.available)):

    fig1 = plt.figure(figsize=(10,10))
    ax1 = plt.gca()
    ax1.set_xticklabels('')
    ax1.set_yticklabels('')
    plt.plot(x*40-20, b, c=color)
    plt.savefig('test.jpg')

with plt.style.context('default'):
    fig2 = plt.figure(figsize=(10,10))
    ax2 = plt.gca()
    ax2.set_xticklabels('')
    ax2.set_yticklabels('')
    plt.grid(which='both', axis='both', color='k', linestyle='--')
    ax2.spines['right'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax2.set_axisbelow(True)
    ax2.tick_params(direction='inout', length=20, width=2)

    plt.plot(x*40-20, b, zorder=1, c=color, lw=5)
    plt.savefig('test.svg')













# random.shuffle(colors)

# t1 = plt.Polygon([[1,10], [1, 5], [2,5]], color='r', fill=False, lw=4)
# ax.add_patch(t1)
# plt.scatter([1,10,1,10], [1,10,10,1], s=350, c='g', edgecolors='w', lw=6, zorder=2)
# plt.plot([0,10], [0,10], zorder=1, c='b', lw=4)

# Polynomial curve fitting
# --------------------------
# def PolyCoefficients(x, coeffs):
#     o = len(coeffs)
#     y = 0
#     for i in range(o):
#         y += coeffs[i]*x**i
#     return y

# x = np.linspace(-100, 100, 10000)
# coeffs = np.random.uniform(-5,5,size=50)
# print(coeffs)
# plt.plot(x, PolyCoefficients(x, coeffs))
# plt.show()
# --------------------------

# Spline curve fitting
# x = np.linspace(-10, 10, num=10)
# y = np.cos(-x**2/9.0)

# f2 = interp1d(x, y, kind='cubic')
# xnew = np.linspace(0, 10, num=1000)
# plt.plot(x, y, 'o', xnew, f2(xnew), '--')

# plt.show()
