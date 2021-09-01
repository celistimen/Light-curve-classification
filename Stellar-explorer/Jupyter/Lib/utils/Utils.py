# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_selection import SelectKBest
import os
import pickle
import math
from scipy import signal

from scipy.fft import fft, fftfreq


def DfToNumpy(df):
    return getDataColumns(df).to_numpy()


def canFloat(x):
    try:
        float(x)
        return True
    except:
        return False
    
def makeDataColumnList(lijst):
    somelist = [x for x in lijst if canFloat(x)] # Create list of time columns, remove Label and ShotNo if they haven't been removed yet   
    return somelist

def getDataColumns(df):
    datacolumns = makeDataColumnList(df.columns)
    return df[datacolumns]


def nameToFloat(label):
    names = ["APERIODIC", "CONSTANT", "CONTACT_ROT", "DSCT_BCEP", "ECLIPSE", "GDOR_SPB", "INSTRUMENT", "RRLYR_CEPHEID", "SOLARLIKE"]
    return names.index(label)
def nameArrayToFloatArray(label_list):
    return np.array([nameToFloat(x) for x in label_list])
def floatArrayToNameArray(label_list):
    names = ["APERIODIC", "CONSTANT", "CONTACT_ROT", "DSCT_BCEP", "ECLIPSE", "GDOR_SPB", "INSTRUMENT", "RRLYR_CEPHEID", "SOLARLIKE"]
    return np.array([names[x] for x in label_list])

# TSFEL
def dfToListOfDf(df):
    dataframe_list = []
    df_f = getDataColumns(df)
    for i in range(len(df_f)):
        row = df_f.iloc[i]
        new_df = pd.DataFrame(row).reset_index().drop('index', axis = 1)
        dataframe_list.append(new_df)
    return dataframe_list

def featureImportanceDataframe(features, labels, amount_of_features = 739,  feature_names = []):
    if (len(feature_names) == 0):
        feature_names = ["feature " + str(i) for i in range(len(features))]        
    bestfit = SelectKBest()
    features = bestfit.fit(features, labels)
    # Sort by feature importance (ascending)
    feature_names = np.array(feature_names)
    sorted_idx = features.scores_.argsort()
    
    feature_importance_df = pd.DataFrame(list(zip(feature_names[sorted_idx], features.scores_[sorted_idx])), columns = [ "Feature Name", "Feature importance"])
    return feature_importance_df

def makeCacheFile(obj, filename):
    with open(filename, 'wb') as config_dictionary_file:
        pickle.dump(obj, config_dictionary_file)
            
def readCacheFile(filename):
    if (os.path.isfile(filename)):
        with open(filename, 'rb') as config_dictionary_file:
            return pickle.load(config_dictionary_file)
    else:
        print("filename not found")
        
        
## FFT

def imputeArray(array):
    array = array.astype('float64') # fft does not work with array dtype object (from dataframe)
    for i in range(len(array)):
        if math.isnan(array[i]):
            j = i
            while(math.isnan(array[j]) and j < len(array)):
                j+=1
            array[i] = (array[j] + (j-i) * array[i-1]) / (j-i + 1)
    return array

def getFft(y, T): # cadence in sec
    y = imputeArray(y)
    N = len(y)
    yf = fft(y)
    xf = fftfreq(N, T)[:N//2]
    yf =2.0/N * np.abs(yf[0:N//2])
    return xf, yf

def getPSD(array):
    array = imputeArray(array)
    freqs, psd = signal.welch(array)
    return (freqs,psd)




# Check Feature importance
def plotFeatureImportances(forest):
    amount_of_features = len(forest.feature_importances_)
    importances = forest.feature_importances_
    std = np.std([tree.feature_importances_ for tree in forest.estimators_],
                 axis=0)
    indices = np.argsort(importances)[::-1]

    # Print the feature ranking
    print("Feature ranking:")
#     for f in range(amount_of_features):
#         print("%d. feature %d (%f)" % (f, indices[f], importances[indices[f]]))

    # Plot the impurity-based feature importances of the forest
    plt.figure()
    plt.title("Feature importances")
    plt.bar(range(amount_of_features), importances[indices],
            color="r", yerr=std[indices], align="center")
    plt.xticks(range(amount_of_features), indices )
    plt.xlim([-1, amount_of_features])
    plt.show()