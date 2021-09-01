# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd


#sklearn
from sklearn.base import BaseEstimator, TransformerMixin 
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import make_pipeline # Create pipeline without explicit naming of each step, convenient for nesting without cluttering code
from sklearn.pipeline import FeatureUnion # pipeline for feature extraction steps specifically

#tsfresh
from tsfresh import extract_features
from tsfresh.utilities.dataframe_functions import impute
from tsfresh import feature_extraction 

#TSFEL 
import tsfel

#Cesium
from cesium import featurize

#Kymatio
from kymatio.torch import Scattering1D as Scattering1D_Torch
import torch


# The 24 features are hardcoded for portability
feature_names = ['tsfresh_Value__cid_ce__normalize_True',
       'tsfresh_Value__change_quantiles__f_agg_"var"__isabs_True__qh_0.2__ql_0.0',
       'tsfresh_Value__change_quantiles__f_agg_"var"__isabs_False__qh_0.4__ql_0.0',
       'tsfresh_Value__change_quantiles__f_agg_"var"__isabs_True__qh_0.8__ql_0.0',
       'tsfresh_Value__fft_coefficient__attr_"abs"__coeff_1',
       'tsfresh_Value__fft_aggregated__aggtype_"centroid"',
       'tsfresh_Value__number_crossing_m__m_0',
       'tsfresh_Value__ratio_beyond_r_sigma__r_1.5',
       'tsfresh_Value__ratio_beyond_r_sigma__r_3',
       'tsfresh_Value__lempel_ziv_complexity__bins_5',
       'tsfresh_Value__lempel_ziv_complexity__bins_100',
       'tsfresh_Value__fourier_entropy__bins_10',
       'tsfresh_Value__permutation_entropy__dimension_6__tau_1',
       'TSFEL_0_Fundamental frequency', 'TSFEL_0_Median diff',
       'TSFEL_0_Spectral entropy', 'TSFEL_0_Spectral spread',
       'TSFEL_0_Wavelet energy_2', 'Cesium_period_fast',
       'Cesium_freq1_lambda', 'Cesium_freq1_signif', 'Cesium_freq2_freq',
       'Cesium_freq_frequency_ratio_21', 'Cesium_p2p_scatter_2praw']



# The sklearn estimator
# The feature extraction functions take the data in the form of a dataframe with only data columns, or a 2D numpy array
# The cached function is an exception and also needs the ID ("Number" column) of stars
class AutomatedFeatureExtraction(BaseEstimator, TransformerMixin):        
    def __init__(self, tsfresh_ = True, tsfel_ = True, cesium_ = True):
        self.tsfresh_ = tsfresh_
        self.tsfel_ = tsfel_
        self.cesium_ = cesium_
        
        feature_list = []
        
        # You can choose which libraries to include
        if self.tsfresh_:
            feature_list.append(("tsfresh",FunctionTransformer(tsfreshFeatures, validate = False)))
        if self.tsfel_:
            feature_list.append(("tsfel",FunctionTransformer(TSFELFeatures, validate = False)))
        if self.cesium_:
            feature_list.append(("cesium",make_pipeline(
                FunctionTransformer(CesiumFeatures, validate = False),
                SimpleImputer())) # cesium returns nan sometimes
            )            
        self.feature_union = FeatureUnion(feature_list)
        
    def fit(self, X, *_):
        self.feature_union.fit(X)
        return self

    def transform(self, X, *_):
        return self.feature_union.transform(X)

# The cached function passes the dataframe in its entirety because the cachemanager uses the Number 
# To avoid extracting the features each time, there is the option to use a cache manager.
# However, this requires a different format: a dataframe with a row for each light curve, and a "Number" column 
# as ID for each star
class AutomatedFECached(BaseEstimator, TransformerMixin):
    def __init__(self, cache_manager):
        self.cache_manager = cache_manager
        
    def getCachedFeatures(self, df):
        return self.cache_manager.getCached(df)
    
    def fit(self, X, *_):
        return self

    def transform(self, df, *_):
        features = FunctionTransformer(self.getCachedFeatures, validate = False).transform(df)
        return features


###############################  tsfresh   ###############################################################
# function that extracts the best tsfreshFeatures
def tsfreshFeatures(X):
    # Create configuration file
    tsfresh_names =[name.split('tsfresh_')[1] for name in feature_names if 'tsfresh' in name]
    temp_df = pd.DataFrame(columns = tsfresh_names)
    kind_to_fc_parameters = feature_extraction.settings.from_columns(temp_df) 

    # Convert to tsfresh format (vertical stacking/melting)
    df  = pd.DataFrame(X)
    df = df.reset_index() # Add index column for pulse No.
    verticalDf = pd.melt(df, id_vars='index', var_name="Time", value_name="Value").sort_values(["index","Time"]).reset_index(drop=True)

    # feature extraction
    # To multithread the tsfresh feature extraction, pass the parameter: n_jobs (multithreading takes some startup time and is slower for only a couple of samples)
    threads = 1
    if X.shape[0] > 500:
        threads = 0 # threads = 0 lets tsfresh determine the amount of threads
    X_tsfresh = extract_features(verticalDf, column_id='index', column_sort='Time',  kind_to_fc_parameters = kind_to_fc_parameters, n_jobs = threads)  
    
    # make sure there are no nan's 
    impute(X_tsfresh)
    
    # return the features as a numpy array
    return X_tsfresh.to_numpy()


###############################  TSFEL  ###############################################################
# help function to transform the dataframe to a correct format
def dfToListOfDf(df):
    dataframe_list = []
    # df_f = getDataColumns(df)
    for i in range(len(df)):
        row = df.iloc[i]
        new_df = pd.DataFrame(row).reset_index().drop('index', axis = 1)
        dataframe_list.append(new_df)
    return dataframe_list

# TSFEL does not have a method to make config files from feature names so we have to do it manually
# Create configuration file
def makeTSFELConfig(config_names):
    my_cfg_file = tsfel.get_features_by_domain()                                                                              # If no argument is passed retrieves all available features
    for category in my_cfg_file.keys():
        for key in my_cfg_file[category].keys():
            if (key not in config_names):
                my_cfg_file[category][key]["use"] = "no"
            else:
                my_cfg_file[category][key]["use"] = "yes" # confusingly TSFEL uses "yes" and "no" instead of True or False     
    return my_cfg_file

# The main feature extraction method
def TSFELFeatures(X):
    # This is how the columns are named after the extraction process
    TSFEL_names =[name.split('TSFEL_')[1] for name in feature_names if 'TSFEL' in name]
    
    # The names in the config file are slightly different, for example MFCC has multiple features called 0_MFCC_6 ...
    config_names = [name.split("_")[1] for name in TSFEL_names]
    
    # make a config file based on these feature names
    my_cfg_file = makeTSFELConfig(config_names)
    
    # Transform to the format for tsfel, a list of dataframes
    df = pd.DataFrame(X)
    df_list = dfToListOfDf(df) # helper function above
    X_transformed = tsfel.time_series_features_extractor(my_cfg_file, df_list)        
    return X_transformed[TSFEL_names].to_numpy()


###############################  Cesium   ###############################################################
# Cesium is a bit weird in comparison to the other libraries:
#     -Cesium takes a list of arrays for the measurements ("values_list") and a list of arrays for the timestamps ("times_list")
#     -Unlike TSFEL and tsfresh, some of the features depend on the times passed, to stay consistent with the feature analysis
#      and to be easily compatible with sklearn estimators, a list of times is created by splitting the 27.3822 (days) in equal timeframes
#      Consequently, there is a small error on the times, but the values of the features seem to be relatively unaffected by it
#     -Furthermore, the speed of the algorithm strongly depends on the times passed

def CesiumFeatures(X):
    # Create configuration
    cesium_names =[name.split('Cesium_')[1] for name in feature_names if 'Cesium' in name]
    observation_duration = 27.3822 # MODIFY for other datasetset

    # Cesium takes a list, every array in the list is the light curve of one star
    if (type(X) == pd.core.frame.DataFrame):
        X = X.to_numpy()
    values_list = [array for array in X]
    
    # The length of the signal, X.shape[1] for 2D arrays, X.shape[0] for a single light curve
    signal_length = X.shape[1]
    
    # The observation times, equal times are used for all light curves
    times = np.array([float(x)/signal_length*observation_duration for x in range(signal_length)])
    # if the data is not evenly spaced, the times_list can be configured as needed
    times_list = [times for  i in range(len(values_list))]
    
    # Extract features
    fset_cesium = featurize.featurize_time_series(    times=times_list,
                                          values=values_list,
                                          errors=None,
                                         features_to_use = cesium_names)
    return fset_cesium.to_numpy()



##########################################################################################################
###############################  Kymatio   ###############################################################
##########################################################################################################
# wavelet scattering transform
class WST(BaseEstimator, TransformerMixin):       
    def __init__(self, J = 6, Q = 1, device = 'cuda'):
        # define scattering transformer
        # B = batch size, T is length of signal
        # J = scale parameter, max scale is 2^J 
        self.J = J
        self.Q = Q
        self.device = device
    
    def fit(self, X, *_):
        if isinstance(X, pd.DataFrame):
             X = X.drop(["Number","Label"], axis = 1).to_numpy()
        T = X.shape[1]
        self.scattering_transformer = Scattering1D_Torch(self.J,T,self.Q)
        self.scattering_transformer.to(self.device)
        return self

    def transform(self, X, *_):
        if isinstance(X, pd.DataFrame):
             X = X.drop(["Number","Label"], axis = 1).to_numpy()
        X_gpu = torch.Tensor(X).to(self.device).contiguous() # Tensore takes 3D array, so [None,:] places it in its own array
        transformed = self.scattering_transformer(X_gpu)
        transformed = transformed.cpu()
        (n, a, b) = transformed.shape
        transformed = transformed.reshape(n, a*b)
        return transformed

