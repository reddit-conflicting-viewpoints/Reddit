from dash import dcc, html, Input, Output, callback
from pages.visualize import *
import pandas as pd

df = pd.read_csv('data/results/computerscience_hot_results.csv')

layout = html.Div([
    html.H3('Page 1'),
    dcc.Dropdown(
        {f'Page 1 - {i}': f'{i}' for i in ['New York City', 'Montreal', 'Los Angeles']},
        id='page-1-dropdown'
    ),
    html.Div(id='page-1-display-value'),
    dcc.Link('Go to Page 2', href='/page2'),
    dcc.Graph(id='indicator-graphic', figure=plot('scatter', df, x_col='comment_relevance', y_col='comment_score', title='Computer Science', threshold_col='comment_relevance', threshold_min=0.5, threshold_max=1, color='comment_controversiality'))
])

# @callback(
#     Output('indicator-graphic', 'figure'))
# def update_graph():
    
#     df = pd.read_csv('../data/results/computerscience_hot_results.csv')
    
#     return plot('scatter', df, x_col='relevance', y_col='score_y', title='Computer Science', threshold_col='relevance', threshold_min=0.5, threshold_max=1, color='controversiality')

@callback(
    Output('page-1-display-value', 'children'),
    Input('page-1-dropdown', 'value'))
def display_value(value):
    return f'You have selected {value}'