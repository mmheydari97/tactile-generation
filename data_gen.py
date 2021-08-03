import random
import numpy as np
from math import comb

P_1D = 0.25
CROSS = []

def bezier(x, P):
    n = P.shape[0]
    b = 0

    for i in range(n):
        a = comb(n,i)*((1-x)**(n-i))*(x**i)
        b = b + a*P[i].reshape(1,-1)

    if b.shape[1] == 1:
        b = np.concatenate((x,b), axis=1)
    return b


if random.random() <= P_1D:
    P = P.reshape(-1,1).flatten()[::2]

for i in range(10):
    x = np.linspace(0, 1, 10000).reshape(-1,1)
    P = np.array([[random.randint(-20,20), random.randint(-20,20)] for i in range(random.randint(2,20))])
    b = bezier(x, P)
    np.save(f"./points/{i+1}.npy", b)
