"""
@author: pavan_yadav and @author: Sanjana_shroff

Place this script as part of the folder containing crushmerged_1.csv and create dummy resuults folder
in compute canada and run the script as a job

Output generated as crushed_results.csv under results folder

Purpose of script is to process data and run ML models
"""
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
from numpy import mean, absolute
import numpy as np
import seaborn as sns
from imputation_feature_selection_2 import fill_SI,fill_KNNI,svr,read_previous_csv,feature_selection_crush,get_correlated_column,drop_MOCA_from_df
from imputation_feature_selection_1 import fill_Zero, fill_mean, fill_median, fill_IM,knn,linear,label_encoding,feature_selection

cv = KFold(n_splits=5, random_state=1, shuffle=True)
df = pd.read_csv(r"./crushmerged_1.csv")

#testing with smaller data
#df = pd.read_csv(r"D:\STFX\Course Project\correlation_connectomatics\crushmerged150.csv")
#correlation = df.corr() #commented because of size obligations

#function to call all ML models
def call_all_models(kdf):
    Y = kdf['MOCA']
    X = kdf.drop("MOCA", axis=1)
    resl = linear(X,Y)
    ress = svr(X,Y)
    resk = knn(X,Y)
    return [resl,ress,resk]

#calling different models and storing the results
def corr_models():
    results= []
    for i in [0.5,0.4,0.3]:
        print("For corr value:",i)
        results.append("corr> "+str(i))
        list_columns, correlation_subset = get_correlated_column(i)
        main_kdf = feature_selection_crush(correlation_subset,df,i,False,False)
        results.append(main_kdf.shape[1])
        main_kdf = label_encoding(main_kdf)
        main_kdf = drop_MOCA_from_df(main_kdf)
        
        print("Fill zero")
        kdf = main_kdf
        kdf = fill_Zero(main_kdf) 
        results.append("Fill zero")
        results = results + call_all_models(kdf)
        
        print("Fill mean")
        kdf = fill_mean(main_kdf)
        call_all_models(kdf)
        results = results + ["","","Fill mean"]
        results = results + call_all_models(kdf)
        
        print("Fill median")
        kdf = fill_median(main_kdf)
        call_all_models(kdf)
        results = results + ["","","Fill median"]
        results = results + call_all_models(kdf)
        
        print("Fill IM")
        kdf = fill_IM(main_kdf)
        call_all_models(kdf)
        results = results + ["","","Fill IM"]
        results = results + call_all_models(kdf)
    
        print("Fill KNN")
        kdf = fill_KNNI(main_kdf)
        call_all_models(kdf)
        results = results + ["","","Fill KNN"]
        results = results + call_all_models(kdf)
        
        print("Fill SI")
        kdf = fill_SI(main_kdf)
        call_all_models(kdf)
        results = results + ["","","Fill S1"]
        results = results + call_all_models(kdf)
        
        
    return results

results = corr_models()
dfcrush = pd.DataFrame(columns=["Method of feature selection","Column used","Imputation methods","Linear reg","SVR","KNN"])
r = list(zip(*([iter(results)]*6)))
dfcrush = pd.concat([pd.DataFrame(r, columns=dfcrush.columns), dfcrush], ignore_index=True)
dfcrush.to_csv(r"./results/crushed_results.csv")