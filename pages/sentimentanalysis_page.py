from dash import dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd


layout =html.Div([
            html.H1('Sentiment Analysis - Can we identify conflict with Sentiment?',style={'textAlign':'center'}),
            dcc.Loading(children=[
                html.H3(id='sentimentsubredditprinter',style={'textAlign':'center'}),
                dcc.Graph(id='sentiment1'),
                dcc.Graph(id='sentiment2'),
                dcc.Graph(id='sentiment3'),
            ], fullscreen=True),
        ])

@callback(
    Output('sentiment1', 'figure'),
    Output('sentiment2', 'figure'),
    Output('sentiment3', 'figure'),
    Output('sentimentsubredditprinter', 'children'),
    Input('session', 'data')
)
def update_graph(data):
    try:
        df = pd.DataFrame(data)
        subreddit = df.at[0, 'subreddit']
        return px.histogram(df, x="comment_sentiment"), px.box(df, x="comment_sentiment", y='comment_relevance'), px.box(df, x="post_id", y='comment_relevance'), f'Subreddit: {subreddit}'
    except KeyError:
            return {}, {}, {}, 'No data loaded! Go to Home Page first!'
