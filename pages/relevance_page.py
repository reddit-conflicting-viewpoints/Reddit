from dash import dcc, html, Input, Output, callback
from pages.visualize import *
from pages.sas_key import get_csv_url
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
    df = pd.read_csv(get_csv_url(subreddit))
    return plot('scatter', df, x_col='comment_relevance', y_col='comment_score', title=subreddit, threshold_col='comment_relevance', threshold_min=0.5, threshold_max=1)
