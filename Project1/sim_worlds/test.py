tup = (0,1)
res = type(tup) is tuple

print(res)
# print(tup[0][1])

def Reverse(tuples):
    new_tup = ()
    for i in reversed(tuples):
        new_tup = new_tup + (i,)
    return new_tup


print(Reverse(tup))


