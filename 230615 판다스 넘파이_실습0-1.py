import pandas as pd

a = pd.Series((5,11,14,30,33,38,24))
a.index = (1,2,3,4,5,6,'bonus')
print(a)



b = pd.Series([5,11,14,30,33,38,24], index = [1,2,3,4,5,6,'bonus'])
print(b)


c = pd.Series([5,11,14,30,33,38,24])
c.index = [1,2,3,4,5,6,'bonus']
print(c)