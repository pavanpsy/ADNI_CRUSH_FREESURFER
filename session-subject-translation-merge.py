"""
@author: pavan_yadav

Place this script as part of the folder containing ADNIMERGE.csv and subject-session-2-rid-viscode_mapping.csv 
in compute canada and run the script as a job

Output generated as dataframe_batch1.csv and dataframe_batch2.csv under same folder

Purpose of script is to merge metadata with crushed measurements
for unmatched examdate, nearest date is fetched using rid-viscode translation file 
"""
import pandas as pd
df = pd.read_csv(r"./ADNIMERGE.csv") #reading metadata
df2 = pd.read_csv(r"./subject-session-2-rid-viscode_mapping.csv") #reading viscode-translation
newDf = df.merge(df2, how='inner', on=("RID", "VISCODE"))

crushDf = pd.read_csv(r"./dataframe_batch1.csv") #reading crush-measuremnets
crushDf2 = pd.read_csv(r"./dataframe_batch2.csv") #reading crush-measuremnets

#merging both batches based on PatientID
try:
    listOfDataFrames = []
    ptid_list = []
    crushDf.rename(columns={'PatientID': 'PTID'}, inplace=True)
    for index, row in crushDf.iterrows():
        ptid_list.append(row["PTID"])
        ptid_sublist = row["PTID"].split('-')[1].split("S")
        ptid_formatted = ptid_sublist[0]+"_S_"+ptid_sublist[1]
        crushDf.loc[index, "PTID"] = ptid_formatted
        
        df2 = newDf.loc[(newDf["PTID"] == ptid_formatted) ]
        listOfDataFrames.append(df2)

    metadaDataFrame = pd.concat(listOfDataFrames)
    metadaDataFrame =pd.merge(metadaDataFrame, crushDf, on=["PTID"], how="inner")
    metadaDataFrame.to_csv(r"./crushmerged_csv_batch1.csv", index=False)
except Exception as e:
    print("Exception: ", e)

try:
    listOfDataFrames = []
    ptid_list = []
    crushDf2.rename(columns={'PatientID': 'PTID'}, inplace=True)
    for index, row in crushDf2.iterrows():
        ptid_list.append(row["PTID"])
        ptid_sublist = row["PTID"].split('-')[1].split("S")
        ptid_formatted = ptid_sublist[0]+"_S_"+ptid_sublist[1]
        crushDf2.loc[index, "PTID"] = ptid_formatted
        
        df2 = newDf.loc[(newDf["PTID"] == ptid_formatted) ]
        listOfDataFrames.append(df2)

    metadaDataFrame = pd.concat(listOfDataFrames)
    metadaDataFrame =pd.merge(metadaDataFrame, crushDf2, on=["PTID"], how="inner")
    metadaDataFrame.to_csv(r"./crushmerged_csv_batch2.csv", index=False)
except Exception as e:
    print("Exception: ", e)