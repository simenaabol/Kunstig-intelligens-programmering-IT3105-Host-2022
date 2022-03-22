import numpy as np
import random

# testliste = [i for i in range(10)]

# prob_dist = [0.01, 0.0, 0.99]

# i = np.random.choice(a=np.arange(len(prob_dist)), size=None, p=prob_dist)

# print(i)
# i = np.random.choice(a=np.arange(len(prob_dist)), size=None, p=prob_dist)

# print(i)
# i = np.random.choice(a=np.arange(len(prob_dist)), size=None, p=prob_dist)

# print(i)
# i = np.random.choice(a=np.arange(len(prob_dist)), size=None, p=prob_dist)

# print(i)
# i = np.random.choice(a=np.arange(len(prob_dist)), size=None, p=prob_dist)

# print(i)

# print(testliste)

# testliste = testliste / np.sum(testliste)

# print(testliste)

# distr_for_rbuf = []

# for i in range(10):
#     distr_for_rbuf.append(i) # LITT USIKKER PÅ DENNE

# print(distr_for_rbuf)
distribution = [0.7 , 0.0, 0.1]


# ind = distribution.index(0.7)
start = True
ind = -1
while ind == -1 or distribution[ind] == 0:
    ind = random.randint(0, len(distribution))
    
print('ind:', ind)
ind = 0

