import pandas as pd


df = pd.read_csv("data/transactions.csv")

print(df)
print("\nTotal records:", len(df))
print("\nAverage amount:", df["amount"].mean())