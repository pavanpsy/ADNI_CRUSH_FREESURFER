"""
@author: pavan_yadav

Place this script as part of the folder containing crushmerged_1.csv
in compute canada and run the script as a job

Output generated as df_anayse_crush_input.csv under same folder

Purpose of script is to make the dataset compliant with df-anayze
"""
import pandas as pd
from k_fold_models import label_encoding,drop_MOCA_from_df
df = pd.read_csv(r"./crushmerged_1.csv")
#df = pd.read_csv(r"D:\STFX\Course Project\correlation_connectomatics\crushmerged150.csv")

list_cols=list(df.columns[:118])#taking only measuremnets
list_cols.remove('MOCA')#deleting MOCA column

for ele in df.columns[119:]:
    #removing regions starting with 004
    if "0004" in ele:
        list_cols.append(ele)
df = df.drop(list_cols,axis=1)
lc =[]
ser_cols = df.isna().sum()

for key in ser_cols.keys():
    #removing measuremnets whose values are less that half of the total number of rows
    if ser_cols[key] > 80:
        lc.append(key)
#display the removed columns
print(lc)

df = df.drop(lc,axis=1)
main_kdf = label_encoding(df)#encoding categorical values
main_kdf = drop_MOCA_from_df(main_kdf)#dropping empty MOCA rows
main_kdf = main_kdf.fillna(main_kdf.mean())#filling null values iwth mean of that column
main_kdf.to_csv(r"./df_anayse_crush_input.csv")#storing output file