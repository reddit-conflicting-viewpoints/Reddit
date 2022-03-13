from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

import plotly.express as px
import pandas as pd

PADDING_STYLE = {
    'padding-top': '5px',
    'padding-right': '5px',
    'padding-bottom': '5px',
    'padding-left': '5px',
    'margin-bottom': '10px'
}

layout =html.Div([
            html.H1('Conflicting Viewpoints - Identifying Bias, Influence and Polarizing Views',style={'textAlign':'center'}),
            html.H3(id='sentimentsubredditprinter',style={'textAlign':'center'}),
                dbc.Card([
                    dcc.Loading(children=[
                        dcc.Graph(id='viewpoints1'),
                    ])
                ], style=PADDING_STYLE),
                dbc.Card([
                    dcc.Loading(children=[
                        dcc.Graph(id='viewpoints2'),
                    ])
                ], style=PADDING_STYLE),
                dbc.Card([
                    dcc.Loading(children=[
                        dcc.Graph(id='viewpoints3'),
                    ])
                ], style=PADDING_STYLE),
        ])


@callback(
    Output('viewpoints1', 'figure'),
    Output('viewpoints2', 'figure'),
    Output('viewpoints3', 'figure'),
    Output('conflictprinter', 'children'),
    Input('session', 'data')
)
def update_graph(data):
    try:
        df = pd.DataFrame(data)
        subreddit = df.at[0, 'subreddit']
        return f'Subreddit: {subreddit}'
    except KeyError:
            return 'No data loaded! Go to Home Page first!'
