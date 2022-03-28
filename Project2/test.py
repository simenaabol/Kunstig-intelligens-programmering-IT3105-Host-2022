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
# distribution = [0.7 , 0.0, 0.1]


# # ind = distribution.index(0.7)
# start = True
# ind = -1
# while ind == -1 or distribution[ind] == 0:
#     ind = random.randint(0, len(distribution))
    
# print('ind:', ind)
# ind = 0


# from collections import defaultdict

# kids = defaultdict(lambda: None) # main-kok
# kids[0] = 'kid en'
# kids[1] = 'kid to'

# print(kids)

# for kid in range(3):
#     print(kids[kid])
# # print(kids[3])
    
    
    
 
# print(kids)


# array= [ [0.0  , 0.0  ] , [0. ,  0.  ], [0.,  0.01], [0.01 ,0.  ], [0.  , 0.02], [0.02 ,0.  ], [0.  , 0.03], [0.03 ,0.  ], [0.   ,0.04], [0.04 ,0.01], [0.01 ,0.  ], [0.   ,0.01], [0.01 ,0.01], [0.01, 0.01], [0.01 ,0.02], [0.02 ,0.01], [0.01, 0.03], [0.03 ,0.01], [0.01 ,0.04], [0.04, 0.02], [0.02 ,0.  ], [0.  ,0.02], [0.02 ,0.01], [0.01 ,0.02], [0.02 ,0.02] ]
# ar = np.array(array)
# # indices, = np.nonzero(ar)
# indices, = np.transpose(np.nonzero(ar))

# print(indices)


x = np.array([ [0.0  , 0.0  ] , [0. ,  0.  ], [0.,  0.01], [0.01 ,0.  ], [0.  , 0.02], [0.02 ,0.  ], [0.  , 0.03], [0.03 ,0.  ], [0.   ,0.04], [0.04 ,0.01], [0.01 ,0.  ], [0.   ,0.01], [0.01 ,0.01], [0.01, 0.01], [0.01 ,0.02], [0.02 ,0.01], [0.01, 0.03], [0.03 ,0.01], [0.01 ,0.04], [0.04, 0.02], [0.02 ,0.  ], [0.  ,0.02], [0.02 ,0.01], [0.01 ,0.02], [0.02 ,0.02] ])

i = np.transpose(np.nonzero(x)[0])

print(i)