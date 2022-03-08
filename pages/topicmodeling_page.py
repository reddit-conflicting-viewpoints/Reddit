from dash import dcc, html, Input, Output, callback
import plotly.express as px
from pages.visualize import *
import pandas as pd

layout =html.Div([
            html.H1('Topic Modeling - What are posts talking about?',style={'textAlign':'center'}),
            dcc.Loading(children=[
                html.H3(id='topicsubredditprinter', style={'textAlign':'center'}),
            ], fullscreen=True),
        ])

@callback(
    # Output('first', 'figure'),
    Output('topicsubredditprinter', 'children'),
    Input('session', 'data')
)
def update_graph(data):
    df = pd.DataFrame(data)
    subreddit = df.at[0, 'subreddit']
    return f'Subreddit: {subreddit}'
