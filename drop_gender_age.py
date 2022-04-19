"""
@author: sanjana_shroff

Place this script as part of the folder containing crushmerged_csv_batch1.csv and crushmerged_csv_batch2.csv 
in compute canada and run the script as a job

Output generated as crushmerged_1.csv and crushmerged_2.csv under same folder

Purpose of script is to reduce duplicate columns before merging metadata and measurements
"""
import pandas as pd
#program to delete gender and AGE as it is available as duplicate columns in CRUSH merged dataframe
df = pd.read_csv(r"./crushmerged_csv_batch1.csv")
df2 = pd.read_csv(r"./crushmerged_csv_batch2.csv")
#two batchs were avilable one @author:SanjanaShroff and another @author:PavanYadav

df.drop('Gender', inplace=True, axis=1)
df.drop('Age', inplace=True, axis=1)

df2.drop('Gender', inplace=True, axis=1)
df2.drop('Age', inplace=True, axis=1)

#generate two seperate csv files
df.to_csv(r"./crushmerged_1.csv", index=False)
df2.to_csv(r"./crushmerged_2.csv", index=False)

#printing to confirm certain columns in the merged dataframe
print("df1 columns:", df[116:120])
print("df2 columns:", df[115:120])