# -*- coding: utf-8 -*-
# The main layout file, each subcomponent is defined in a separate file

import dash_html_components as html
import dash_bootstrap_components as dbc

# Layout imports
from layout.DataWindow    import getDataWindow
from layout.GraphWindow   import getGraphWindow
from layout.Navbar import getNavbar

# The different components are defined in their own file in the layout folder along with their callbacks

# Left column:
    # The filterwindow is currently disabled

def getLayout(app):
    div = html.Div(
        id="main_window",
        children=[
            getNavbar(app),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(                            
                            children=[
                                # getFilterWindow(app),
                                getDataWindow(app),
                                ],style={"position": "sticky", "top": "0"}),
                        width= 3,
                        className = "left_column"),
                    dbc.Col(
                        getGraphWindow(app),
                        className = 'center_column'),                         
                    ],className = "main_row"),     
        ])
    
    return div