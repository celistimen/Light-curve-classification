# -*- coding: utf-8 -*-

# This file can add some helpful badges, nothing important here

import dash_html_components as html
import dash_bootstrap_components as dbc
import json



def getHelpBadge(text, tooltip_class):
    return dbc.Badge(children = [
          html.I(className="fa fa-question-circle fa-sm"),
          html.Span(text, className = tooltip_class)
          ],
        color="light", className="ml-1 tooltipped"
        )

def getText(explanation_id):
    with open('assets/help.json') as f:
        helpdata = json.load(f)
    explanation = helpdata[explanation_id]
    return html.P(explanation,style={'margin-bottom': '5px'})

