
# The filter window is currently not added, This enables the user to filter a subset of the dataframe, for example, on name or label of the star
# This contains a lot of remnants from previous project

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash import no_update
from dash.dependencies import Input, Output, State
import globals

only_training_set = "only_training_set"


def getFilterWindow(app):
    # Getting and setting variables happens here, these should be gotten from 
    #  the global settings file in the furute #todo
    
    
    additional_filters = html.Details([
        html.Summary(children = [html.H6(children=["Additional filters"], id = "additional_filter_options_title",style={"display": "inline-block"})  ]),
        html.Div(
            id="additional_filter_div",
            children=[
                dbc.Card(
                    dbc.CardBody([
                        html.Label(
                            id="filter_personal_labels_label",
                            htmlFor = "personal_filter_dropdown",
                            children=["Personal filters:"]),
                        dcc.Dropdown(
                            id = "personal_filter_dropdown",
                            options=makeOptionsForPersonalFilter(),
                            value=[],
                            multi=True,
                            ),
                        html.Label(
                            id="filter_detailed_labels_label",
                            htmlFor = "filter_detailed_labels",
                            children=["Detailed labels:"]),
                        dcc.Input(
                            id= "filter_detailed_labels",
                            placeholder = "", 
                            debounce = True
                            ),
                        html.Label(
                            id="filter_observation_label",
                            htmlFor = "filter_observation",
                            children=["Observation:"]),
                        dcc.Input(
                            id= "filter_observation",
                            placeholder = "", 
                            debounce = True
                            ),
                        html.Label(
                            id="filter_certainty_label",
                            htmlFor = "filter_certainty",
                            
                            children=["Certainty < "]),
                        dcc.Input(
                            id= "filter_certainty",
                            placeholder = "", 
                            debounce = True,
                            type= 'number',
                            min= 0,
                            max= 100,
                            style={'width': '50px'}
                            ),
                        html.Span("%"),
                        
                        html.Details(children = [
                            html.Summary(children = [html.H6(children=["Hidden pulses"], id = "hidden_pulses_title",style={"display": "inline-block"})  ]),
                                html.Div(children = [
                                    dcc.Checklist(
                                        id= "additional_filter_checklist",
                                        options=[
                                            {'label': 'Show no data pulses', 'value': 'nodata'},
                                            {'label': 'Show flat pulses', 'value': 'flat'},
                                            {'label': 'Show bump pulses', 'value': 'bump'},
                                            {'label': 'Show bulge pulses', 'value': 'bulge'},
                                            {'label': 'Show low premag current pulses', 'value': 'low_premag'},
                                            {'label': 'Hide other pulses', 'value': 'hide'},                               
                                        ],
                                        value=[]
                                        )
                                    ])
                            ])
                        ],
                        )
                    )
                ]
            )
        ])
    
    additional_options = html.Details([
        html.Summary(children = [html.H6(children=["Sorting options"], id = "additional_sorting_options_title",style={"display": "inline-block"})  ]),
        html.Div(
            id="additional_options_div",
            children = [
                dbc.Card(
                    dbc.CardBody([
                        dcc.RadioItems(
                                id= "additional_sorting_options_radio",
                                options=[
                                    {'label': 'Sort by Certainty', 'value': 'sort_certainty'},
                                    {'label': 'Sort by ShotNo (asc)', 'value': 'sort_shotno_asc'},
                                    {'label': 'Sort by ShotNo (desc)', 'value': 'sort_shotno_desc'},
                                    {'label': 'Sort by Similarity', 'value': 'sort_similarity'},
                                ],
                                value='sort_shotno_desc'
                            ),
                        dbc.Button(children = ["Set similarity pulse",
                                        # getHelpBadge(getText("classification_button_help"), "tooltiptextleft")
                                        ], 
                            id="find_similar_button", color = "primary"
                            ),
                        dcc.Store(id = "similar_pulse_shotno", data = "data"),
                    ]))
                
                ]
            )
        ])
            
    
    inside = html.Details([
            html.Summary(children = [ html.H5(children=["Filter options"], id = "filter_options_title",style={"display": "inline-block"})]),
            html.Div(                
                className="column",
                children=[
                    dcc.Checklist(
                        id= "filter_checklist",
                        options=[
                            {'label': 'Only training set', 'value': 'only_training_set'}
                        ],
                        value=[]
                        ),
                    html.Div([
                        html.Label(
                            id="filter_expert_labels_label",
                            htmlFor = "filter_expert_labels",
                            children=["Expert Labels:"]),
                        dcc.Dropdown(
                            id="filter_expert_labels",
                            options=[
                                {'label': '1', 'value': '1'},
                                {'label': '2', 'value': '2'},
                                {'label': '3', 'value': '3'},
                                {'label': '4', 'value': '4'}
                            ],
                            value=[], # empty, all pulses are selected
                            multi=True
                        ),
                        # The same, but for the classifier labels
                        html.Label(
                            id="filter_classifier_labels_label",
                            htmlFor = "filter_classifier_labels",
                            children=["Classifier Labels:"]),
                        dcc.Dropdown(
                            id="filter_classifier_labels",
                            options=[
                                {'label': '1', 'value': '1'},
                                {'label': '2', 'value': '2'},
                                {'label': '3', 'value': '3'},
                                {'label': '4', 'value': '4'}
                            ],
                            value=[], # empty, all pulses are selected
                            multi=True
                            )
                        ], className = "together"),
                      
                    html.Div(
                        children= [
                            dcc.Input(
                                id="ShotNoBegin_filter",
                                type="number",
                                placeholder="ShotNo begin",
                                debounce=True   # this causes the filter to wait until the user is finished typing
                                ),
                            dcc.Input(
                                id="ShotNoEnd_filter",
                                type="number",
                                placeholder="ShotNo end",
                                debounce=True
                                )
                            ], className = "together"),                    
                    
                    
                    additional_filters,
                    additional_options,
                    
                    html.P(
                        id="pulse_counter",
                        children=[" # pulses: ", len(globals.selector_df)],
                        style = {"display":"inline"}),
                        dbc.Button(
                            children = [html.I(className="fa fa-refresh")], # fas fa-sync-alt fa-sm
                            id="filter_button",
                            n_clicks= 0,
                            size="sm", color= "primary", #style = {"display":"inline-block"}
                            )
                  
                ]) #div
            
            ]) # details
            
          
    
    this = dbc.Card(
        [
            dbc.CardBody(
                [
                    inside
                ],
                
            ),
        ],
        id="filter_window" # used for the help function
    )
    ### Layout
   
    
    
    
    ### Callbacks
    
    
    
    # Find similar pulses
    @app.callback(
        Output("similar_pulse_shotno", "data"),  # , Output("additional_sorting_options_radio","value")
        [Input("find_similar_button", "n_clicks")],
        [State("store_local_show_shotno",'data')])
    def updateSimilarPulse(n_clicks, current_shotno):
        if (current_shotno):
            globals.similarity_df = globals.classification_manager.getSimilarityDF(current_shotno)
            return current_shotno
        return no_update
    
    #
    # Define callbacks here
    # dcb because ActiveLearningWindow also can set the data_selector
    @app.callback(
        [Output("data_selector","data"),
         Output("pulse_counter","children"),
         Output('data_selector','page_current')],
        [Input("filter_checklist","value"),      # the checkboxes 
         Input("filter_expert_labels"   ,"value"),# only show a subset of expert labels
         Input("filter_button","n_clicks"),     # manually filter
         Input("ShotNoBegin_filter","value"),   # filter between these shotnumbers
         Input("ShotNoEnd_filter","value"),
         Input("additional_filter_checklist","value"),
         Input("filter_classifier_labels","value"),
         Input("additional_sorting_options_radio","value"),
         Input("dummy_button", "n_clicks"),
         Input("filter_detailed_labels","value"),
         Input("filter_observation","value"),
         Input("filter_certainty","value"),
         Input("confusion_shotnos", "data"),
         Input("similar_pulse_shotno","data")], # to update when a new pulse is added
        [State("dynamic_filtering_checkbox","value"),
         State('data_selector','page_current'),
         State('data_selector','page_size'),
         State("store_local_show_shotno",'data')])
    def updateDataSelector(checklist_value, filter_labels_value, n_clicks , 
                           shotno_begin, shotno_end, additional_filters, filter_classifier_labels_value,
                           sorting_value,dummy_button_n_clicks, filter_detailed_labels, filter_observation, 
                           filter_certainty, confusion_shotnos, similarity_shotno,
                           dynamic_filtering, page_current, page_size, current_shotno): # n_clicks is not needed
        # Check which button has caused the callback, the filter button should always update
        ctx = dash.callback_context
        if not ctx.triggered:
            button_id = 'No clicks yet'
        else:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if (button_id == "confusion_shotnos"):
            # show the confusion shotnos
            shotnos = confusion_shotnos
            filtered = globals.DAO.getPulseInformation() # all pulses
            filtered = filtered[filtered["ShotNo"].isin(shotnos)]
            return makeSelectorDF(filtered) # returns 3 values
        
        
            
        #don't filter if dynamic filtering is off and the filter_button is not clicked
        if ((len(dynamic_filtering) == 0) & (button_id != "filter_button")) :# 'on' is not in the list
            pulsecounter_text = "# pulses: ", len(globals.selector_df)
            return globals.selector_df_data, pulsecounter_text, page_current
        # Otherwise filter
        else:
            # Filter the bulk of the pulses with the additional filters
            # The additional filters are default not shown so unless the value is in additional_filters it is not shown
            filtered = globals.DAO.getPulseInformation() # all pulses
            if ('low_premag' not in additional_filters):
                filtered = filtered[filtered["PremagnetizationCurrent"] > 2000]
            filters = ["nodata","flat","bump","bulge"] # these are taken out if they are not present in additional_filters
            for f in filters:
                if (f not in additional_filters):
                    filtered = filtered[filtered[f + "_filter"] == False] # the pulse is only shown only if the filter = False 
                    #for (value in additional_filters):
            
            # Keep only the filtered pulses
            if ("hide" in additional_filters):
                filtered = filtered[(((filtered["bump_filter"]) | (filtered["bulge_filter"])) | ((filtered["nodata_filter"]) | (filtered["flat_filter"]) |  (filtered["PremagnetizationCurrent"]< 2000 )))]            
            
            # Regular filters
            
            if (only_training_set in checklist_value):
                filtered = filtered[filtered["ExpertLabel"].notnull()]
            # if none or all 4 are selected, nothing is filtered
            if (len(filter_labels_value)>0):
                filter_labels= [float(i) for i in filter_labels_value]
                filtered = filtered[filtered["ExpertLabel"].isin(filter_labels) ]
            # Analogues but for the classifier labels
            if (len(filter_classifier_labels_value)>0):
                filter_labels= [float(i) for i in filter_classifier_labels_value]
                filtered = filtered[filtered["ClassifierLabel"].isin(filter_labels) ]
            if (shotno_begin != None):
                filtered = filtered[filtered["ShotNo"] >= shotno_begin]
            if (shotno_end != None):
                filtered = filtered[filtered["ShotNo"] <= shotno_end]
            
                

            # Detailed label & Observationfilter
            if ((filter_detailed_labels != None) & (filter_detailed_labels != "")):
                filtered = filtered[filtered["DetailedLabel"].str.contains(filter_detailed_labels) == True]
            if ((filter_observation != None) & (filter_observation != "")):
                filtered = filtered[filtered["Observation"].str.contains(filter_observation) == True]
            if ((filter_certainty != None) & (filter_certainty != "")):
                filtered = filtered[filtered["Certainty"] < filter_certainty/100]
            # more filters come here
            
            
            # Sorting
            if ((button_id == "similar_pulse_shotno") & (sorting_value == 'sort_similarity')):
                similarity_df = globals.similarity_df
                filtered = filtered.merge(similarity_df, how = 'inner', on= 'ShotNo')
                filtered = filtered.sort_values('similarity', ascending = False)   
            elif (sorting_value == "sort_certainty"):
                filtered = filtered.sort_values("Certainty")        
            elif (sorting_value == "sort_shotno_asc"):
                filtered = filtered.sort_values("ShotNo")
            elif (sorting_value == "sort_shotno_desc"):
                filtered = filtered.sort_values("ShotNo", ascending= False)
            elif (sorting_value == "sort_similarity"):
                similarity_df = globals.similarity_df
                # if it is not already calculated, calculate it now from the current pulse
                if (len(similarity_df) == 0):
                    #calculate similarity df from current_pulse_shotno
                    globals.similarity_df = globals.classification_manager.getSimilarityDF(current_shotno)
                similarity_df = globals.similarity_df
                filtered = filtered.merge(similarity_df, how = 'inner', on= 'ShotNo')
                filtered = filtered.sort_values('similarity', ascending = False)     


            globals.selector_df = filtered[globals.selector_columns]
            globals.selector_df_data = globals.selector_df.round(5).to_dict('records')
            
            # columns =[{"name": i, "id":i} for i in globals.selector_df.columns]
            # om ook het aantal colomns aan te passen
            amount = len(globals.selector_df)
            pulsecounter_text = "# pulses: ",  amount
            if (page_current == None):
                page_current=0
            if (amount < page_size):
                page_current = 0
            return globals.selector_df_data, pulsecounter_text, page_current
        
        

    
    return this

def makeOptionsForPersonalFilter():
    uniques = globals.DAO.getPulseInformation()["PersonalFilter"].unique().tolist()
    uniques = [x for x in uniques if str(x) != 'nan'] # remove nan from the list
    uniques.sort()
    options = []
    for unique in uniques:
        options.append({'label':unique, 'value': unique})
    return options



def makeSelectorDF(filtered):
    globals.selector_df = filtered[globals.selector_columns]
    globals.selector_df_data = globals.selector_df.round(5).to_dict('records')
    # om ook het aantal colomns aan te passen
    amount = len(globals.selector_df)
    pulsecounter_text = "# pulses: ",  amount
    page_current = 0
    return globals.selector_df_data, pulsecounter_text, page_current
    

    
    
    
    