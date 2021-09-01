

# The help window is currently not used
# uses utility and assets/help.json


import dash_html_components as html
import dash_bootstrap_components as dbc

from utility import getText


def getHelpWindow(app):
    # Getting and setting variables happens here
    table_header = [
    html.Thead(html.Tr([html.Th("Switch behaviour"), html.Th("Label"),html.Th("Color")]))
    ]
    
    row1 = html.Tr([html.Td("Good"), html.Td("1"),html.Td(style= {'backgroundColor': 'green'})])
    row2 = html.Tr([html.Td("Intermediate"), html.Td("2"),html.Td(style= {'backgroundColor': 'yellow'})])
    row3 = html.Tr([html.Td("Slow"), html.Td("3"),html.Td(style= {'backgroundColor': 'orange'})])
    row4 = html.Tr([html.Td("Failure"), html.Td("4"),html.Td(style= {'backgroundColor': 'red'})])

    table_body = [html.Tbody([row1, row2, row3, row4])]
    color_table = dbc.Table(table_header + table_body, bordered=True)

    
    ### Layout
    this =html.Div([
                    dbc.ModalHeader("Help"),
                    dbc.ModalBody([
                            dbc.Row([
                                    dbc.Col("", width= 5),
                                    dbc.Col(
                                        html.Div(children =[html.H4("General")]),
                                        width =7)
                                ]
                            ),
                            dbc.Row([
                                dbc.Col(children = [getImage("assets/images/datatable.png", "The datatable shows the shotnumbers of the pulses along with their Expert/Classifier Label and the assigned certainty. The datatable can be clicked to select a pulse." )],
                                                    width = 5),
                                dbc.Col(html.Div([getText("general_help_1"),html.Br(),
                                                  getText("general_help_2"),html.Br(),
                                                  color_table]), width = 7),html.Br()
                                ]),
                            dbc.Row([
                                    dbc.Col("",                            
                                        width=5),
                                    dbc.Col(
                                        html.Div(children =[html.H4("Functionality")]),
                                        width =7)
                                ]
                            ),
                            getInformation("Active learning", "general_help_1", "assets/images/pulse_information.png", "The pulse can be assigned a label by filling in the ExpertLabel field. Doing so will include the pulse in the training set."),
                            getInformation("Expanding the pulse classes", "general_help_expanding"),
                            getInformation("The 2D graph", "general_help_2D_graph"),
                            getInformation("", "general_help_2D_graph_2")
                        ],
                        style = {"text-align": "justify",      # make the text look pretty
                             "text-justify": "inter-word"}
                    ),
                    dbc.ModalFooter(
                        #dbc.Button("Close", id="help_overlay_close", className="ml-auto")
                    ),
                ])
    
    
    ### Callbacks
    # Define callbacks here
    
    
    return this



def getImage(src, caption):
    img = html.Img(src=src)
    fig = html.Figure(children = [img,html.Figcaption(caption)], style = {'text-align': 'center', 'font-style':'italic'})
    return fig

def getInformation(header, explanation_id, img_src = 0, fig_caption = ""):    
    explanation = getText(explanation_id)
    fig = ""
    if (img_src != 0):
        fig = getImage(img_src, fig_caption)
    
    children =[]
    if (header != ""):
        children.append(html.H5(header))
    children.append(html.P( explanation))

    row = dbc.Row([
                dbc.Col(fig,                            
                    width=5),
                dbc.Col(
                    html.Div(children =children),
                    width =7)
            ]
        )
    
    return row
    