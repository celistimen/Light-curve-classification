
import dash_core_components as dcc
import dash_html_components as html


# Custom imports:
import Jupyter.Lib.Visualisation as dv

from layout.Graph2DWindow import getGraph2DWindow


import globals

# This layout file is for the center pane with different graphs

def getGraphWindow(app):
    
    heights = globals.height_options["graph_height"]
    
    ### Layout
    this =  html.Div(
                #className="seven columns",
                children=[
                    html.Div(        
                        children=[
                            dcc.Graph(
                                id='light_curve_graph',
                                figure=dv.getBlankFigure(),
                                style={'display':'block', 'height': heights["light_curve_graph"]}
                            ),
                            dcc.Graph(
                                id='frequency_graph',
                                figure=dv.getBlankFigure(),
                                style={'display':'block','height': heights["frequency_graph"]}
                            ),                            
                            getGraph2DWindow(globals.app)
                        ],
                        id= "graph_div",
                        style={'display':'block'}
                    ), 
                ], style={'width': '100%'})
            
    
    ### Callbacks
    # Define callbacks here
    
    
    return this