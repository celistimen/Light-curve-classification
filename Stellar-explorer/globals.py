# -*- coding: utf-8 -*-

import dash
import dash_bootstrap_components as dbc

# Custom imports:
from Jupyter.Lib.DAO import LightCurveDAO

from dash_extensions.callback import DashCallbackBlueprint


# This file contains all the global variables such as the DAO (Data Access Object)
# To make this app available for multiple users, global variables can not be changed as this messes the multiprocessing up. Dash provides some alternatives such as cache elements 
# Keep user specific things on client side (for example through dash.Storage etc.)

def initialize():
    # global layout properties
    global loading_style
    loading_style = {'visibility':'visible'}
    
    global dcb
    dcb = DashCallbackBlueprint()   
    
    global app
    app = dash.Dash(__name__, external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"])
    
    
    # A single object that contains all the necessary data
    # For larger applications, you want to use a separate database, a job-queue might help as well: https://plotly.com/dash/job-queue/
    global DAO
    DAO = LightCurveDAO("data/Light_Curves_Labeled.csv", "data/features.csv")
    
    # This is the datatable on the left of the GUI
    global selector_columns
    selector_columns= ["Number","Label"]
    global selector_df  
    selector_df = DAO.getDF()[selector_columns]
    
    
    # the version for in the datatable, keep it in globals so an update is not needed everytime
    global selector_df_data
    selector_df_data = selector_df.to_dict('records')
    
    # settings file would be usefull
    global height_options
    height_options = {"graph_height":{"light_curve_graph": 450, "frequency_graph": 450, "pls_graph": 450 }}
