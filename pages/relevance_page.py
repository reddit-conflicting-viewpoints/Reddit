from dash import dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px


layout =html.Div([
            html.H1('Relevance - Are the comments in discussions relevant to the submission?',style={'textAlign':'center'}),
            dcc.Loading(children=[
                html.H3(id="relevancesubredditprinter", style={'textAlign':'center'}),
                dcc.Graph(id='relevance1')
            ], fullscreen=True),
        ])

@callback(
    Output('relevance1', 'figure'),
    Output('relevancesubredditprinter', 'children'),
    Input('session', 'data')
)
def update_graph(data):
    try:
        df = pd.DataFrame(data)
        subreddit = df.at[0, 'subreddit']
        return px.histogram(df, x="comment_relevance", title=f'Comment Relevance Histogram (Subreddit: {subreddit})'), f'Subreddit: {subreddit}'
    except KeyError:
        return {}, 'No data loaded! Go to Home Page first!'
