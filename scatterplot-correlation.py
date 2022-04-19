"""
@author: sanjana_shroff

Place this script as part of the folder containing crushmerged_1.csv and sorted_fullPS.csv 
in compute canada and run the script as a job

Output generated as different image file under the same folder

Purpose of script is to visualise the highly correlated measurements
"""
import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt

#This script runs for CRUSH data, file path can be modified for Freesurfer
list_top_features =  ["MOCA"]

#input the complete merged datfarme
df = pd.read_csv(r".\crushmerged_1.csv")

#unput the correlation matrix for all all column
cor = pd.read_csv(r'.\sorted_fullPS.csv')

#get the top 4 features from the fully calculated persons correlation file
top_4 = cor.iloc[1:5,0]
for i in range (1,5):
    list_top_features.append(top_4.get(i))
    print(top_4.get(i))
top_4_datasubset = df[list_top_features]

#creates plot for the top 4 highly correlated features
sns.set()
plot1 = sns.regplot(x=list_top_features[1],y=list_top_features[0],data=top_4_datasubset)
plot1.figure.savefig(r".\crush-correlation-1.png")
plot1 = sns.regplot(x=list_top_features[2],y=list_top_features[0],data=top_4_datasubset)
plot1.figure.savefig(r".\crush-correlation-2.png")
plot1 = sns.regplot(x=list_top_features[3],y=list_top_features[0],data=top_4_datasubset)
plot1.figure.savefig(r".\crush-correlation-3.png")
plot1 = sns.regplot(x=list_top_features[3],y=list_top_features[0],data=top_4_datasubset)
plot1.figure.savefig(r".\crush-correlation-4.png")


#plot for specific fields by manually ebtering the fields
neg_pos = df[['levman/1007-3011-roi-stddevFA',"levman/1009-3009-roi-meanADC",'MOCA']]
sns.set()
fig, axes = plt.subplots(1, 2,figsize=(20, 10))
fig.suptitle('Highly correlated features in both directions')
sns.regplot(ax=axes[0], x='levman/1007-3011-roi-stddevFA',y='MOCA',data=neg_pos)
axes[0].set(xlabel='Mean ADC between left fusiform grey matter - left lateral occipital white matter', ylabel='MOCA score')
sns.regplot(ax=axes[1], x="levman/1009-3009-roi-meanADC",y='MOCA',data=neg_pos)
axes[1].set(xlabel='Mean ADC between left inferior temporal grey matter - left inferior temporal white matter', ylabel='MOCA score')
axes[1].figure.savefig(r".\1007-3011-roi-stddevFA_correlation_and_1009-3009-roi-meanADC_correlation.png")