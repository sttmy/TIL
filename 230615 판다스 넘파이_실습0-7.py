import pandas as pd

dates = pd.date_range('2021-07-01','2021-07-06')
temps1 = pd.Series([80,82,85,90,83,87], index=dates)
temps2 = pd.Series([70,75,69,83,79,77], index=dates)
temps3 = pd.Series([75,77,67,82,77,85], index=dates)
print(temps3)
temps_df2 = pd.concat([temps1, temps2, temps3], axis = 1)
temps_df2.columns = ['Missoula','Philadelphia','temps3']
print(temps_df2)