import numpy as np

testliste = [i for i in range(10)]

print(testliste)

testliste = testliste / np.sum(testliste)

print(testliste)

distr_for_rbuf = []

for i in range(10):
    distr_for_rbuf.append(i) # LITT USIKKER PÅ DENNE

print(distr_for_rbuf)