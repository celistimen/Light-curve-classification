# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

import plotly.express as px
import plotly.graph_objects as go



import Jupyter.Lib.utils.Utils as utils


###############################  Mainly for Dashboard
def getLightCurveFigure(curve, name):
    gridcolor = 'gainsboro'
    zerolinecolor = 'lightgrey'
    # colors taken from https://plotly.com/python/discrete-color/ set 1
    
    series = curve
    figure = go.Figure()
    figure.add_trace(go.Scatter(x=series.index, y= series.values, name= name, mode = "lines",  line=go.scatter.Line(color='rgb(55,126,184)'))) # soft blue
    figure.update_layout(title='Light curve',title_x=0.5, plot_bgcolor='rgba(0,0,0,0)',
               xaxis_title='Time (days)', yaxis_title='Flux')
    
    figure.update_xaxes(showgrid=True, gridwidth=1, gridcolor=gridcolor)
    figure.update_yaxes(showgrid=True, gridwidth=1, gridcolor=gridcolor,zerolinecolor=zerolinecolor)  
    return figure


# Use fft         
def getFrequencyFigure(curve_array, name):
    xf, yf = utils.getFft(curve_array.values, 30*60) # half hour, should not be hardcoded
    xf = xf * 1000000
    figure = getFigure(xf ,yf, "", x_axis = "Frequency (µHz)", y_axis = "Amplitude", bar = True)    
    return figure

        
# General method that is called by other, more specific methods
def getFigure(x, y, name, x_axis= "X axis", y_axis = "Y axis", color = 'rgb(55,126,184)', bar = False): # default to blue
    gridcolor = 'gainsboro'
    zerolinecolor = 'lightgrey'
    # colors taken from https://plotly.com/python/discrete-color/ set 1
    colormap = {'purple' : 'rgb(152,78,163)',
                'blue' : 'rgb(55,126,184)',
                'red' : 'rgb(228,26,28)'}
    if color in colormap.keys():
        color=colormap[color]
    
    figure = go.Figure()
    if (bar):
        figure.add_trace(go.Bar(x=x, y=y, name= name)) # soft blue
    else :
        figure.add_trace(go.Scatter(x=x, y=y, name= name, mode = "lines",  line=go.scatter.Line(color=color))) # soft blue
    figure.update_layout(title=name,title_x=0.5, plot_bgcolor='rgba(0,0,0,0)',
               xaxis_title = x_axis, yaxis_title = y_axis)
    
    figure.update_xaxes(showgrid=True, gridwidth=1, gridcolor=gridcolor)
    figure.update_yaxes(showgrid=True, gridwidth=1, gridcolor=gridcolor,zerolinecolor=zerolinecolor)  
    return figure


def getBlankFigure():
    figure = {
        'data':[
            {
                'x': [], 'y': [], 'type': 'line', 'name': ''        
            }
        ],
        'layout':{
            'title': ""
            }
        }
    return figure



# Feature plot
def getScatterplotFigure(df, x_axis, y_axis, show_legend = True, show_outliers= False, extra_data = ""):
    gridcolor = 'gainsboro'
    zerolinecolor = 'lightgrey'

    #color_discrete_map = {'APERIODIC':"lightblue", 'CONSTANT': "lightgreen", 'CONTACT_ROT':"yellow", 'DSCT_BCEP': "red", 'ECLIPSE':"purple", 'GDOR_SPB':"orange", 'INSTRUMENT': "darkblue", 'RRLYR_CEPHEID': "forestgreen", 'SOLARLIKE':'crimson'}
    columns = df.columns
    
    # standard figure
    figure = px.scatter(df, x=x_axis, y= y_axis, hover_name = "Number", color = "Label",
                        hover_data= columns)  #to specify your own colors, pass this parameter: color_discrete_map = color_discrete_map

    figure.update_layout(showlegend=show_legend)
        
    figure.update_layout(title='2D representation',title_x=0.5, plot_bgcolor='rgba(0,0,0,0)', 
                   xaxis_title=x_axis, yaxis_title=y_axis)
    figure.update_xaxes(showgrid=True, gridwidth=1, gridcolor=gridcolor,zerolinecolor=zerolinecolor)
    figure.update_yaxes(showgrid=True, gridwidth=1, gridcolor=gridcolor,zerolinecolor=zerolinecolor, secondary_y = False)

    
    figure.update_layout( clickmode = 'event+select') # only allow for certain traces
    for soort in figure.data:
        soort.selected.marker.color = "blue"

    return figure


# Todo: remove?
####################################   Visualize classificationresults in notebooks

# def plot_confusion_matrix(predictions, labels):
#     plt.figure(figsize=(5,5))
#     from sklearn.metrics import confusion_matrix
#     cm = confusion_matrix(y_pred=predictions, y_true=labels)
#     cm = cm.astype('int')
#     # cm = cm.astype('float')/cm.sum(axis=1)[:, np.newaxis]
#     plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    
#     plt.ylabel('True Label')
#     plt.xlabel('Predicted Label')
#     labels = ["APERIODIC",    "CONSTANT", "CONTACT_ROT", "DSCT_BCEP" , "ECLIPSE", "GDOR_SPB", "INSTRUMENT", "RRLYR_CEPHEID", "SOLARLIKE"]
#     plt.yticks(range(len(labels)),labels)
#     plt.xticks(range(len(labels)),labels, rotation = 'vertical') # verticale xticks toegevoegd
    
    
#     # fmt = '.3f'
#     fmt = 'd'
#     thresh = cm.max() / 2.
#     import itertools
#     for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
#         plt.text(j, i, format(cm[i, j], fmt),
#                  horizontalalignment="center",
#                  color="white" if cm[i, j] > thresh else "black")

#     plt.colorbar()
    

