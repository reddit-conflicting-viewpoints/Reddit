from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

import plotly.express as px
import pandas as pd
import numpy as np

PADDING_STYLE = {
    'padding-top': '5px',
    'padding-right': '5px',
    'padding-bottom': '5px',
    'padding-left': '5px',
    'margin-bottom': '10px'
}

layout =html.Div([
            html.H1('Conflicting Viewpoints - Identifying Bias, Influence and Polarizing Views',style={'textAlign':'center'}),
            html.H3(id='conflictprinter',style={'textAlign':'center'}),
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
    Output('conflictprinter', 'children'),
    Output('viewpoints1', 'figure'),
    Output('viewpoints2', 'figure'),
    Output('viewpoints3', 'figure'),
    Input('session', 'data')
)
def update_graph(data):
    try:
        df = pd.DataFrame(data)
        subreddit = df.at[0, 'subreddit']

        # figure 1: Post Sentiment
        post_df = df[['post_id', 'post_sentiment']].groupby('post_id', as_index=False, sort=False).first()
        post_df["color"] = np.select(
            [post_df["post_sentiment"].eq(5), post_df["post_sentiment"].eq(1)],
            ["green", "red"],
            "blue"
        )
        post_sent_fig = px.histogram(post_df, 
                                     x="post_sentiment",
                                     title='Sentiment Distribution for Posts',
                                     text_auto=True, 
                                     color="color",
                                     color_discrete_map={
                                         "green": "green",
                                         "red": "red",
                                         "blue": "blue"
                                     }).update_layout(
                                     xaxis_title="Sentiment", yaxis_title="Number of Posts", showlegend=False)

        # figure 2
        df = pd.DataFrame(data)
        subreddit = df.at[0, 'subreddit']
       
        df["color"] = np.select(
            [df["comment_sentiment"].eq(5), df["comment_sentiment"].eq(1)],
            ["green", "red"],
            "blue"
        )
        comment_sent_fig = px.histogram(df, 
                                        x="comment_sentiment",
                                        title='Sentiment Distribution for Comments',
                                        text_auto=True,
                                        color="color",
                                        color_discrete_map={
                                            "green": "green",
                                            "red": "red",
                                            "blue": "blue"
                                        }).update_layout(
                                        xaxis_title="Sentiment", yaxis_title="Number of Comments", showlegend=False)

        # figure 3
        post_df2 = df[['post_id', 'post_sentiment', 'comment_relevance']].groupby('post_id', as_index=False, sort=False).agg({'post_sentiment': 'first', 'comment_relevance': 'mean'})
        box_plot = px.box(post_df2, x="post_sentiment", y='comment_relevance').update_layout(xaxis_title="Sentiment", yaxis_title="Post Relevance", showlegend=False)

        return f'Subreddit: {subreddit}', post_sent_fig, comment_sent_fig, box_plot
    except KeyError as e:
        print(e)
        return 'No data loaded! Go to Home Page first!', {}, {}, {}