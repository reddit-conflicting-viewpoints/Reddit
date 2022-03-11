from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px


PADDING_STYLE = {
    'padding-top': '5px',
    'padding-right': '5px',
    'padding-bottom': '5px',
    'padding-left': '5px',
    'margin-bottom': '10px'
}

layout =html.Div([
            html.Div(id='relnone', style={'display': 'none'}),
            html.H1('Relevance - Are the comments in discussions relevant to the submission?',style={'textAlign':'center'}),
            html.H3(id="relevancesubredditprinter", style={'textAlign':'center'}),
            dbc.Card([
                dcc.Loading(children=[
                    dcc.Graph(id='relevance1')
                ]),
            ], style=PADDING_STYLE)
        ])

@callback(
    Output('relevance1', 'figure'),
    Output('relevancesubredditprinter', 'children'),
    Input('relnone', 'children')
)
def update_graph(data):
    try:
        df = pd.read_csv('temp.csv')
        subreddit = df.at[0, 'subreddit']
        return px.histogram(df, x="comment_relevance", title=f'Comment Relevance Histogram (Subreddit: {subreddit})'), f'Subreddit: {subreddit}'
    except KeyError:
        return {}, 'No data loaded! Go to Home Page first!'
