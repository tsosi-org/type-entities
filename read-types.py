import pandas as pd

df = pd.read_csv("TSOSI-type-entities.csv", encoding= 'utf8')


print(df["tsosi_type"].value_counts())