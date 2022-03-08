from dash import dcc, html, Input, Output, callback
from pages.sas_key import get_df
import plotly.express as px
from pages.visualize import *
import pandas as pd

layout =html.Div([
            html.H1('Sentiment Analysis - Can we identify conflict with Sentiment?',style={'textAlign':'center'}),
            dcc.Loading(children=[
                html.H3(id='sentimentsubredditprinter',style={'textAlign':'center'}),
            ], fullscreen=True),
        ])

@callback(
    Output('sentimentsubredditprinter', 'children'),
    Input('session', 'data')
)
def update_graph(data):
    df = pd.DataFrame(data)
    subreddit = df.at[0, 'subreddit']
    return f'Subreddit: {subreddit}'
