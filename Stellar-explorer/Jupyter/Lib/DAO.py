# -*- coding: utf-8 -*-
import pandas as pd

# Data access object for light curves
class LightCurveDAO():
    def __init__(self, light_curve_filename, feature_filename = ""):
        # This is due to the lack of pointers in python and the easiest solution is to only access the dataframes through 
        self.light_curve_df = pd.read_csv(light_curve_filename)
        self.light_curve_df["Number"] = self.light_curve_df["Number"].astype(str) # make sure the number column is seen as a string. Without this line, can't find strings or integers 
        self.features_df = pd.read_csv(feature_filename)
        self.features_df["Number"] = self.features_df["Number"].astype(str)


        # To easily iterate all signals
        self.datacolumns = self.light_curve_df.columns.tolist()
        self.datacolumns.remove("Number")
        self.datacolumns.remove("Label")
      
    # Returns an object containing the number 
    def getCurveObject(self, number):
        curve = {}
        if number in self.light_curve_df["Number"].values:
            curve["data"]  = self.light_curve_df[self.light_curve_df["Number"]== number][self.datacolumns]
            curve["Label"] = self.light_curve_df[self.light_curve_df["Number"]== number]["Label"]
            curve["Number"] = number
        return curve
    
    # Returns dataseries of one curve
    def getCurve(self,number):
        data = 0
        if number in self.light_curve_df["Number"].values:
            data = self.light_curve_df[self.light_curve_df["Number"]== number][self.datacolumns].iloc[0]
        return data
    
    
    # These two functions do the same as their corresponding functions above, but for multiple curves
    def getCurveObjects(self,numberlist):
        curvelist = []
        for number in numberlist:
            curvelist.append(self.getCurveObject(number))
        return curvelist
    
    def getCurves(self, numberlist):
        curvelist = []
        for number in numberlist:
            curvelist.append(self.getCurve(number))
        return curvelist
    
    def getDF(self):
        return self.light_curve_df
    
    #Function for the features
    def getFeatureColumn(self,feature_index):
        return self.features_df.iloc[:,feature_index + 2] # 2 is the first feature, since Number and Label are also included
    
    def getFeatureDF(self):
        return self.features_df
        
        
        