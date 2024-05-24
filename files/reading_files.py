import pandas as pd

towns = ['duken', 'addis', 'mojo', 'bishoftu', 'adama']
population = ['22o3io23', '232384029', '232938239', '3429382983', '23892382']

dict_town = {'towns': towns, 'population': population}

df_towns = pd.DataFrame(dict_town)
df_towns.to_csv('towns.csv', index=False)
