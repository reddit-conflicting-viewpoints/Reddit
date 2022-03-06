from dash import dcc, html, Input, Output, callback
from pages.visualize import *
import pandas as pd

layout = html.Div([
    dcc.Graph(id='first'),
])

@callback(
    Output('first', 'figure'),
    Input('session', 'data')
)
def update_graph(data):
    subreddit = data
    df = pd.read_csv(f'data/results/{subreddit}_hot_results.csv')
    return plot('scatter', df, x_col='comment_relevance', y_col='comment_score', title=subreddit, threshold_col='comment_relevance', threshold_min=0.5, threshold_max=1)
