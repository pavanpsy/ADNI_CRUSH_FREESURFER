"""
@author: sanjana_shroff

Purpose of script is to process data 
"""

import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.impute import SimpleImputer 
from sklearn.svm import SVR
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from numpy import mean, absolute

cv = KFold(n_splits=5, random_state=1, shuffle=True)

#function to fill null values with simple imputation
def fill_SI(kdf_dropped):
    imputer = SimpleImputer(strategy="most_frequent")
    kdf_dropped = pd.DataFrame(imputer.fit_transform(kdf_dropped), columns=kdf_dropped.columns)
    return kdf_dropped
#function to fill null values with KNN imputater
def fill_KNNI(kdf_dropped):
    imputer = KNNImputer(n_neighbors=5)
    kdf_dropped = pd.DataFrame(imputer.fit_transform(kdf_dropped), columns=kdf_dropped.columns)
    return kdf_dropped

#reading previoud CSV files for fetching the highly correlated columns
def read_previous_csv():
    df1 = pd.read_csv(r"./fullPS.csv")
    df_css = df1[df1["rows_considered"]>60/100*146]
    return list(df_css.iloc[:,0])

#below function returns list of column names with atleast 68 rows and the subset of dataframe
def get_correlated_column(i):
    #df = pd.read_csv(r"./fullPS.csv",index_col=False)
    df = pd.read_csv(r"D:\STFX\Course Project\correlation_connectomatics\fullPS.csv",index_col=False)
    df = df.rename(columns={'Unnamed: 0': 'column_names'})
    df = df.sort_values(['rows_considered', 'MOCA_rho'], ascending=(False,False), key=abs)
    #df.to_csv(r"./sorted_by_rows.csv")
    df_subset_correlation = df[df.rows_considered > 68.0]
    cor_target = abs(df_subset_correlation["MOCA_rho"])
    df_subset_correlation = df_subset_correlation[cor_target>i]
    df_subset_correlation = df_subset_correlation[["column_names","MOCA_rho"]]
    columns_list = list(df_subset_correlation["column_names"])
    columns_list.append("MOCA")
    return columns_list,df_subset_correlation

#drops rows that have missing MOCA value
def drop_MOCA_from_df(kdf):
    #test_df = kdf[kdf['MOCA'].isnull()]
    kdf_dropped = kdf.dropna(subset=['MOCA'])
    return kdf_dropped

#fetch highly correlated features of CRUSH
def feature_selection_crush(correlation,df,i,feature_select = True,calculate_fresh=True):
    if calculate_fresh:
        cor_target = abs(correlation["MOCA"])
        relevant_features = cor_target[cor_target>i]
        #print(relevant_features.shape)
        if feature_select:
            full_ps = read_previous_csv()
            feat_select = ['MOCA']
            for feat in relevant_features.index:
                if feat in list(df.columns[119:]):
                    if feat in full_ps:
                        feat_select.append(feat)
            return df[feat_select]
        else:
            lv,x=get_correlated_column(i)
            return df[lv]
            #return df[relevant_features.index]
    else:
        lv,x=get_correlated_column(i)
        return df[lv]

#SVM for Regression
def svr(X,Y):
    model = SVR()
    scores = cross_val_score(model, X, Y, scoring='neg_mean_absolute_error',
                             cv=cv, n_jobs=-1)
    print("SVM: {:.4f}".format(mean(absolute(scores))))
    return mean(absolute(scores))
