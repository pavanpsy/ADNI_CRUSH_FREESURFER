"""
@author: pavan_yadav

Purpose of script is to process data 
"""
import numpy as np
import pandas as pd
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from numpy import mean, absolute
from sklearn .preprocessing import LabelEncoder

cv = KFold(n_splits=5, random_state=1, shuffle=True)

#different imputation methods to fill missing values
def fill_Zero(kdf_dropped):
    kdf_dropped = kdf_dropped.fillna(0)
    return kdf_dropped
def fill_mean(kdf_dropped):
    kdf_dropped = kdf_dropped.fillna(kdf_dropped.mean())
    return kdf_dropped
def fill_median(kdf_dropped):
    kdf_dropped = kdf_dropped.fillna(kdf_dropped.median())
    return kdf_dropped
def fill_IM(kdf_dropped):
    imputer = IterativeImputer(estimator=ExtraTreesRegressor(n_estimators=10, random_state=0), missing_values=np.nan, sample_posterior=False, 
                                 max_iter=10, tol=0.001, 
                                 n_nearest_features=4, initial_strategy='median')
    kdf_dropped = pd.DataFrame(imputer.fit_transform(kdf_dropped), columns=kdf_dropped.columns)
    return kdf_dropped

#encoding categorical values
def label_encoding(kdf):
    number = LabelEncoder()
    for col in kdf.columns:
        if kdf[col].dtype != np.int64 and kdf[col].dtype != np.float64:
            kdf[col] = number.fit_transform(kdf[col].astype(str))
    return kdf

#feature selection for Freesurfer data
def feature_selection(correlation,df,i,feature_select = True):
    cor_target = abs(correlation["MOCA"])
    relevant_features = cor_target[cor_target>i]
    print(relevant_features.shape)
    if feature_select:
        feat_select = ['MOCA']
        for feat in relevant_features.index:
            if feat in list(df.columns[116:]):
                if feat in list():
                    print(feat)
                    feat_select.append(feat)
        return df[feat_select]
    else:
        return df[relevant_features.index]

#Ml models
def linear(X,Y):
    model = LinearRegression()
    #use k-fold CV to evaluate model
    scores = cross_val_score(model, X, Y, scoring='neg_mean_absolute_error',
                             cv=cv, n_jobs=-1)
    #view mean absolute error
    print("Linear Regression: {:.4f}".format(mean(absolute(scores))))
    return mean(absolute(scores))

def knn(X,Y):
    model = KNeighborsRegressor()
    #use k-fold CV to evaluate model
    scores = cross_val_score(model, X, Y, scoring='neg_mean_absolute_error',
                             cv=cv, n_jobs=-1)

    #view mean absolute error
    print("K Nearest Neighbor: {:.4f}".format(mean(absolute(scores))))
    return mean(absolute(scores))

#hist plot to fetch the range of predicted values
def hisplots_linear_MOCA(correlation,df):
    main_kdf = feature_selection(correlation,df,0.5)
    main_kdf = label_encoding(main_kdf)
    #kdf, test_df = drop_MOCA_from_df(main_kdf)
    main_kdf = fill_IM(main_kdf)
    Y = main_kdf['MOCA']
    X = main_kdf.drop("MOCA", axis=1)
    resl = linear(X,Y)

    linReg = LinearRegression()
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=0)
    linReg.fit(x_train, y_train)
    y_pred = linReg.predict(x_test)
    ax = sns.histplot(y_test)
    ax.set(xlabel='MOCA Score', ylabel='Number of exams')
    ax.set_xlim(5,30)
    ax.figure.suptitle('Histplot with actual MOCA scores')
    ax.figure.savefig(r".\\tested_MOCA_histplot.png")

    ax2=sns.histplot(y_pred)
    ax2.set(xlabel='MOCA Score', ylabel='Number of exams')
    ax2.set_xlim(5,30)
    ax2.figure.suptitle('Histplot with predicted MOCA scores')
    ax.figure.savefig(r".\\predicted_MOCA_histplot.png")