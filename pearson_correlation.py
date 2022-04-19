"""
@author: sanjana_shroff

Place this script as part of the folder containing crushmerged_1.csv
create a dummy results folder under working directory in compute canada and run the script as a job

Output generated as fullPS.csv under results folder

Purpose of script is to find Correlation analysis between featured and MOCA column
"""
import pandas as pd
import scipy.stats

#uncomment below lines for freesufer data
#df = pd.read_csv(r"D:/STFX/Course Project/correlation_connectomatics/newmergedDf.csv")
#df = pd.read_csv(r"D:\STFX\Course Project\project595results\freesurfer\measurement_labels_header_modified.csv")

df = pd.read_csv(r"./crushmerged_1.csv")#reading crushed data
df_columns = df.columns[116:]#Ignore metadata and only fetch connectomatics columns

newdf = pd.DataFrame(columns=['MOCA_rho','MOCA_p', 'rows_considered'])#adding three new columns

outfile = open("./output.txt", 'w')
for col in df_columns:
    subdf = df[[col,'MOCA']]
    subdf = subdf.dropna()
    try:
        rho_value, p_value= scipy.stats.pearsonr(subdf[col], subdf['MOCA'])
        #store resuts when the correlation is more than 0.1 ignore tyhe remaining files
        if(abs(rho_value)>0.1):
            newdf.loc[col]=[rho_value, p_value, subdf.shape[0]]
    except Exception as e:
            outfile.write(col+'\n')
newdf = newdf.sort_values(['rows_considered', 'MOCA_rho'],ascending=(False, False),key=abs)

#uncomment following line for freesurfer results
#newdf.to_csv(r"D:\STFX\Course Project\project595results\freesurfer\fullPS.csv")

newdf.to_csv(r"./results/fullPS.csv")#save the results