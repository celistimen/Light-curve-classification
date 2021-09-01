

# This is the default file for a component, save this as XXXWindow.py and modify
# this can be deleted




import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output
from dash_extensions.callback import DashCallbackBlueprint
import Jupyter.Lib.Visualisation as dv

import globals

dcb = DashCallbackBlueprint() 


def getGraph2DWindow(app):
    # Getting and setting variables happens here, these should be gotten from 
    feature_df = globals.DAO.getFeatureDF()
    
    cols = feature_df.columns
    cols = cols.drop(["Number","Label"])
    option_list = []
    
    # Make key value pairs for buttons
    for value in cols:
        option_list.append({'label': value.replace('_',' '), 'value': value})
        
    
    #TODO add labels for the dropdownboxes
    ### Layout
    this = html.Div(children=[
         dcc.Graph(
            id='pls_graph',
            figure=dv.getScatterplotFigure(feature_df, option_list[0]["value"], option_list[1]["value"]),
            style={"height": globals.height_options["graph_height"]["pls_graph"]}# 
        ),
        dbc.Row([
            dbc.Col(
                dcc.Dropdown(
                    
                    options=option_list,
                    value = option_list[0]["value"],
                    clearable = False,
                    id= "dropdown_x_axis"                        
                ),style= {'padding-left': '0px'})
            ,
            dbc.Col(
                dcc.Dropdown(
                    
                    options=option_list,
                    value = option_list[1]["value"],
                    clearable = False,
                    id= "dropdown_y_axis"                        
                ),style= {'padding-right': '0px'}),
            
            ],
            style= {'margin':'5px'}
        ),        
             dcc.Store('graph_clicked', data = []), 
        ],
        id= "graph_2D_window"
    )
    
     
 
    
    
    @globals.dcb.callback(
          Output("graph_clicked", 'data'),
          [Input('pls_graph', 'clickData')])
    def updatePulse(clickdata):
        if ('customdata' in clickdata["points"][0]): 
            number = clickdata["points"][0]["customdata"][0]
            return [number]
        else:
            return [0], False
        
     
    
    @app.callback(
         Output('pls_graph', 'figure'),
         [Input('dropdown_x_axis', 'value'),
          Input('dropdown_y_axis', 'value')])
    def update2DGraph(x_axis, y_axis):
        feature_df = globals.DAO.getFeatureDF()
        return dv.getScatterplotFigure(feature_df, x_axis, y_axis)
    return this

