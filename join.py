import os
import pandas as pd

db1 = pd.DataFrame()
directory = os.path.join("combo")
for root, dirs, files in os.walk(directory):
    for file in files:
       if file.endswith(".csv"):
           db = pd.read_csv('combo/' + str(file))
           db1 = pd.concat([db,db1])

db1 = db1.drop_duplicates()
db1 = db1.sample(frac=1)
db1.to_csv(r'output.csv', index=False, header=True)
