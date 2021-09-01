# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer
import pickle
import os

# Custom imports
import Lib.Feature_Extraction as FE
import Lib.Combined_Feature_Extraction as CFE

import Lib.utils.Utils as Utils





class CombinedCacheManager():
    def __init__(self):
        self.cache_path = 'cachedir/' + 'combined_selected' + '_cache'
        self.cache = {}        
       
        self.extraction_pipe = make_pipeline(
                CFE.AutomatedFeatureExtraction()
            )
        
        self.read()
        
    def getCached(self, df):
    #         if (all(number in dic for number in lijst))
        if "Label" in df.columns.tolist(): df = df.drop(["Label"],axis = 1)
        cols = df.columns.tolist()
        
        if ( any(df[cols].isnull().any(axis=1))): # the label column can be NaN
            raise ValueError("CacheError: Some curves contain Nan and can not be not cached. It should be false.")
        
        # The numbers are the ID's of the light curves
        numbers = df["Number"].values

        
        # The cache is empty, extract the features and store them in cache
        if (len(self.cache) == 0):
            data_df = df.drop(["Number"], axis = 1)
            features = self.extraction_pipe.fit_transform(data_df)
            for number, row in zip(numbers,features):
                self.cache[number] = row
            self.write()# when all the numbers are stored in cache, write to file
            return self.get(numbers)
            # nieuw maken
            
        # Some or all of them are unavailable
        else:
            #checken of de numbers aanwezig zijn
            incache = self.get(numbers)# check of ze erin zitten
            if (len(incache) == len(numbers)):
                return incache
            else:
                # Find out which numbers are not in the list:                
                not_in_cache = list(set(numbers) - set(self.cache.keys()))
                self.add(df[df["Number"].isin(not_in_cache)])
                return self.get(numbers)
            
                    
    def add(self, df):
        data_df = df.drop(["Number"],axis = 1)
        extracted = self.extraction_pipe.fit_transform(data_df)
        for number, row  in zip(df["Number"].values, extracted):
            self.cache[number] =  row
        self.write()
    
    def get(self, numbers):
        #checken of ze erin zitten
        if (all(number in self.cache for number in numbers)):
            features = np.array([self.cache[number] for number in numbers])
            return features
        return []
    
    def write(self):
        with open(self.cache_path, 'wb') as config_dictionary_file:
            pickle.dump(self.cache, config_dictionary_file)
    
    def read(self):
        if (os.path.isfile(self.cache_path)):
            with open(self.cache_path, 'rb') as config_dictionary_file:
                self.cache = pickle.load(config_dictionary_file)
                
            
    def getCache(self):
        return self.cache