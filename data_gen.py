import random
import numpy as np
from math import comb

P_1D = 0.25
CROSS = []
NUM_SAMPLES = 50000

def bezier(x, P):
    n = P.shape[0]
    b = 0

    for i in range(n):
        a = comb(n,i)*((1-x)**(n-i))*(x**i)
        b = b + a*P[i].reshape(1,-1)

    if b.shape[1] == 1:
        b = np.concatenate((x,b), axis=1)
    return b


for i in range(NUM_SAMPLES):
    x = np.linspace(0, 1, 10000).reshape(-1,1)
    P = np.array([[random.randint(-20,20), random.randint(-20,20)] for i in range(random.randint(2,20))])
    
    if random.random() <= P_1D:
        P = P.reshape(-1,1).flatten()[::2]
    b = bezier(x, P)
    print(f"{i+1}.npy generated")
    np.save(f"./points/{i+1}.npy", b)
