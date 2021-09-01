

# The NavBar used to contain a lot of components, some of the code is still here


import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash import no_update

from dash.dependencies import Input, Output, State, ClientsideFunction

import globals


def getNavbar(app):
    # Getting and setting variables happens here, these should be gotten from 
    #  the global settings file in the furute #todo
    min_height = 200
    max_height = 1500
    n_marks = 5 # divide in 5 parts
    graph_id = {"Light curve graph height": "light_curve_graph",
                     "Frequency graph height": "frequency_graph",
                     "2D representation height": "pls_graph"}
    marks = {}
    for i in range(n_marks+1):
        mark = (max_height - min_height)/(n_marks) *i + min_height
        marks[mark] = str(mark)
        
    graph_height_sliders = html.Div(className= "options_graph_sliders",
        children = [html.Div([
            html.Label(
                id=f"{ID}_height_slider_label",
                htmlFor = f"{ID}_height_slider",
                children=[
                    name
                    ]),
            dcc.Slider(
                        id = f"{ID}_height_slider",
                        min=min_height,
                        max=max_height,
                        step=10,
                        marks=marks,
                        value=globals.height_options["graph_height"][ID],
                        updatemode='drag'
                    )
            ],className = "center") for name, ID in graph_id.items()])
    
    
    options = [
        graph_height_sliders,
        html.Div(id='hidden-div2', style={'display':'none'}),
    ]    
    
    ### Layout
    this = dbc.NavbarSimple(
    children=[                
            dbc.Button(
                children=[  html.I(className="fa fa-cog fa-sm")],
                id="options_button",
                className="mx-2",
            ),dbc.Popover( # The tooltips have to be here instead of the script file since the popover is not always present 
                [
                    dbc.PopoverHeader(children = ["Options"]),
                    dbc.PopoverBody(options),
                ],
                id="options_popover",
                target="options_button",
                placement="bottom",
                is_open = False                
            )            
        ],
        brand="Stellar explorer 2021",
        brand_href="#",
        color="primary",
        dark=True,
    )
    
    
    ### Callbacks
    # Define callbacks here
    
    # Height sliders
    for name, ID in graph_id.items():
        @globals.dcb.callback(Output(ID, "style"),
                      [Input(f"{ID}_height_slider", "value")],
                      [State(ID, "style")])
        def changeHeight(height, style):
            ctx = dash.callback_context
            if not ctx.triggered:
                button_id = 'No clicks yet'
                return no_update
            else:
                [button_id, propertyName] = ctx.triggered[0]['prop_id'].split('.');
                graph_id = button_id.split("_height_slider")[0]
                globals.height_options["graph_height"][graph_id] = height
                globals.GCM.updateCache("graph_height",globals.height_options["graph_height"])
                globals.GCM.up_to_date = False # updated when polled
                style["height"] = height
            return style
            
    
    app.clientside_callback(
        ClientsideFunction(
            namespace='clientside3',
            function_name='openElementWithId'
        ),
        Output("options_popover", "is_open"),
        [Input("options_button", "n_clicks")],
        [State("options_popover", "is_open"),
         State("options_button","id")],
    )        
    
    
    def toggle_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open

    
    
    
    
    return this

