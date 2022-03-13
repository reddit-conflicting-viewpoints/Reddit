from dash import dcc, html, Input, Output, callback
from .visualize import *
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

        # figure 1: 
        df['sentiment_diff'] = df['comment_sentiment'] - df['post_sentiment']

        fig1_df = df[['comment_topics', 'comment_relevance', 'sentiment_diff']].groupby('comment_topics', as_index=False).agg(['mean', 'size']).reset_index()
        fig1_df = fig1_df.droplevel(1, axis=1)
        cols = ['comment_topics', 'comment_relevance_mean', 'comment_relevance_size', 'sentiment_diff_mean', 'sentiment_diff_size']
        fig1_df.columns = cols
        controversy_relevance_plot = cv_plot('scatter', fig1_df[1:], x_col='comment_relevance_mean', y_col='sentiment_diff_mean', size='sentiment_diff_size', title=df.iloc[0]['subreddit'], hover_name='comment_topics', labels={
                     "sentiment_diff_mean": "Controversy",
                     "comment_relevance_mean": "Comment Relevance"
                 })
        
        # figure 2 TODO:choose a post id
        post_id_here = df['post_id'].iloc[0]
        sentiment_avgs = []
        for time in list(df[df['post_id'] == post_id_here].sort_values('comment_created', ascending=True)['comment_created']):
            sentiment_avgs.append(df[(df['post_id'] == post_id_here) & (df['comment_created'] <= time)]['comment_sentiment'].mean())
        
        comment_series_1_plot = px.line(sentiment_avgs, labels={
                     "index": "Number of Comments",
                     "value": "Average Comment Sentiment",
                     "variable": "Average Comment Sentiment"
                 }, title=df[df['post_id'] == post_id_here].iloc[0]['post_title'] + '-' + df.iloc[0]['subreddit'])

        # relevance_avgs = []
        # for time in list(df[df['post_id'] == post_id_here].sort_values('comment_created', ascending=True)['comment_created']):
        #     relevance_avgs.append(df[(df['post_id'] == post_id_here) & (df['comment_created'] <= time)]['comment_relevance'].mean())

        # figure 3
        controversy_comment_topic_plot = cv_plot('bar',df[['comment_topics', 'sentiment_diff']].groupby('comment_topics').mean().reset_index().sort_values(by='sentiment_diff'), x_col='comment_topics', y_col='sentiment_diff', title=df.iloc[0]['subreddit'], labels={
                     "sentiment_diff": "Controversy",
                     "comment_topics": "Comment Topic"
                 }, width=1000, height=800)
        
        return f'Subreddit: {subreddit}', controversy_relevance_plot, comment_series_1_plot, controversy_comment_topic_plot
    except KeyError as e:
        print(e)
        return 'No data loaded! Go to Home Page first!', {}, {}, {}