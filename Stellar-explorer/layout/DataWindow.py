# -*- coding: utf-8 -*-
# Most of the action happens in this file, if a light curve in the datatable is clicked, the light curve and its frequency spectrum are plotted.


import dash
import dash_html_components as html

import dash_table
from dash.dependencies import Input, Output, State # Wel degelijk gebruikt
from dash import no_update
import Jupyter.Lib.Visualisation as dv


import globals



def getDataWindow(app):
    # Getting and setting variables happens here, these should be gotten from 
    data_selector_width_large=42  #the width of one column
    column_1_width = 30
    column_2_width = 30

    data_selector_width_small=40
    # data_selector_width_large='70px'  #the width of one column
    # data_selector_width_small='40px'
    
    ### The layout 
    this =  html.Div(
        children=[
            dash_table.DataTable(
                id= "data_selector",
                columns =[{"name": i, "id":i} for i in globals.selector_df.columns],
                data = globals.selector_df.to_dict('records'),
                style_cell={
                        'height': 'auto',
                        # all three widths are needed
                        # 'minWidth': str(data_selector_width_small) +'px', 'width': str(data_selector_width_large) +'px', 'maxWidth': str(data_selector_width_large) +'px',
                        'whiteSpace': 'normal',
                        'overflow': 'hidden'
                    },
                style_cell_conditional=[
                        {
                            'if': {'column_id': 'Number'},
                            'textAlign': 'right',
                            # 'width': data_selector_width_large,
                            'minWidth': str(data_selector_width_large) +'px', 'width': str(data_selector_width_large) +'px', 'maxWidth': str(data_selector_width_large) +'px',
                        },
                        {
                            'if': {'column_id': 'Label'},
                            'textAlign': 'left',
                            # 'width': data_selector_width_small,
                            'minWidth': str(column_1_width) +'px', 'width': str(column_1_width) +'px', 'maxWidth': str(column_1_width) +'px',
                        }
                    ],
                style_data_conditional=[
                        # {
                        #     'if': {
                        #         'column_id': 'ExpertLabel',
                        #         'filter_query': '{ExpertLabel} eq "1"'
                        #     },
                        #     'backgroundColor': 'green',
                        #     'color': 'black',
                        # }
                    ],
                page_size=1000,
                css= [{'selector': 'tr :hover', 'rule': 'background-color: "lightgreen";'},
                      {'selector': '.dash-table-container', 'rule': 'border-color: "rgb(211, 211, 211)"'},
                      {'selector': '.dash-table-container', 'rule': 'border-style: "solid";'}
                      ]
                )],
        id="data_window" # used for the help function,
        
        )
    
    
    # The new callback to display light curves:
    @app.callback(
        [Output("light_curve_graph",'figure'),
         Output("frequency_graph","figure")],
        [Input('data_selector','active_cell'),
         Input('graph_clicked','data')], # this store is modified when clicking the 2D representation
        [State('data_selector','page_current'),
         State('data_selector','page_size'),
         State('light_curve_graph','figure')]
        )
    def update_graphs(active_cell, selected_number, 
                      page_current, page_size, old_light_curve):
        
        ctx = dash.callback_context

        if not ctx.triggered:
            button_id = 'No clicks yet'
        else:
            # can be used to check what triggered this
            [button_id, propertyName] = ctx.triggered[0]['prop_id'].split('.');    
            
            number = 0
            if (button_id == "data_selector"):                
                # determine the selected number
                if (page_current == None): #if page_current = 0 it is None, 
                    page_current = 0
                if active_cell is not None: # it is None when changing pages
                    i = active_cell["row"]
                    number = globals.selector_df.iloc[i+ (page_current)*page_size]["Number"]
                else:
                    return [dash.no_update, dash.no_update]
                     
            elif (button_id == "graph_clicked"):
                number = selected_number[0]
                
            light_curve_object = globals.DAO.getCurveObject(number)
                
            # make lightcurve figure in visualisation
            light_curve_data = light_curve_object["data"].iloc[0]            
            figure = dv.getLightCurveFigure(light_curve_data, "Light curve")       
            freq_figure = dv.getFrequencyFigure(light_curve_data, "Frequency")
            return [figure, freq_figure]
        
        # At the start, when nothing is selected, just show a blank figure
        return [dv.getBlankFigure(), dv.getBlankFigure()]            
    
    return this