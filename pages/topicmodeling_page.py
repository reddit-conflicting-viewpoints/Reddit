from dash import dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd


layout =html.Div([
            html.Div(id='topicnone', style={'display': 'none'}),
            html.H1('Topic Modeling - What are posts talking about?',style={'textAlign':'center'}),
            dcc.Loading(children=[
                html.H3(id='topicsubredditprinter', style={'textAlign':'center'}),
                # dcc.Graph(id='topic1'),
            ]),
        ])

@callback(
    # Output('first', 'figure'),
    Output('topicsubredditprinter', 'children'),
    Input('topicnone', 'children')
)
def update_graph(data):
    try:
        df = pd.read_csv('temp.csv')
        subreddit = df.at[0, 'subreddit']
        return f'Subreddit: {subreddit}'
    except KeyError:
            return 'No data loaded! Go to Home Page first!'
