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
            html.Div(id='sentnone', style={'display': 'none'}),
            html.H1('Sentiment Analysis - Can we identify conflict with Sentiment?',style={'textAlign':'center'}),
            html.H3(id='sentimentsubredditprinter',style={'textAlign':'center'}),
            dbc.Card([
                dcc.Loading(children=[
                    dcc.Graph(id='sentiment1'),
                ])
            ], style=PADDING_STYLE),
            dbc.Card([
                dcc.Loading(children=[
                    dcc.Graph(id='sentiment2'),
                ])
            ], style=PADDING_STYLE),
            dbc.Card([
                dcc.Loading(children=[
                    dcc.Graph(id='sentiment3'),
                ])
            ], style=PADDING_STYLE),
            # dcc.Loading(children=[
            #     html.H3(id='sentimentsubredditprinter',style={'textAlign':'center'}),
            #     dcc.Graph(id='sentiment1'),
            #     dcc.Graph(id='sentiment2'),
            #     dcc.Graph(id='sentiment3'),
            # ], fullscreen=True),
        ])

@callback(
    Output('sentiment1', 'figure'),
    Output('sentiment2', 'figure'),
    Output('sentiment3', 'figure'),
    Output('sentimentsubredditprinter', 'children'),
    Input('sentnone', 'children')
)
def update_graph(data):
    try:
        df = pd.read_csv('temp.csv')
        subreddit = df.at[0, 'subreddit']
        return px.histogram(df, x="comment_sentiment"), px.box(df, x="comment_sentiment", y='comment_relevance'), px.box(df, x="post_id", y='comment_relevance'), f'Subreddit: {subreddit}'
    except KeyError:
            return {}, {}, {}, 'No data loaded! Go to Home Page first!'
