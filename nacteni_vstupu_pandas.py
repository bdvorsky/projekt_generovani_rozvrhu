import pandas as pd

vstup_lektori = pd.read_csv("vstup_lektori.csv", sep=";")
vstup_studenti = pd.read_csv("vstup_var2_studenti.csv", sep=";")

print(vstup_lektori.head())
print(vstup_studenti.loc[0:2])