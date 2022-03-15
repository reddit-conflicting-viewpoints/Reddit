from dash import dcc, html, Input, Output, callback
from .visualize import *
import dash_bootstrap_components as dbc
from pages.style import PADDING_STYLE
import plotly.express as px
import pandas as pd
import numpy as np


layout =html.Div([
            html.H1('Conflicting Viewpoints',style={'textAlign':'center'}),
            html.Div([
                html.H3("Identifying Conflict, Influence and Polarizing Views", className="display-6 text-center"),
                html.P(id='conflictprinter',className='fs-4 text-center'),
                html.Hr(),
            ]), 
            dbc.Card([
                html.H5("Controversy and Relevance of comments by Topics", className="card-title"),
                html.P("Here we summarize topics, sentiments and relevance in one graph. Each point represents aggregates by Topics", className = 'card-subtitle'),
                html.Li("Controversy (y-axis) Scale(-4, 4): We calculated the controversy score by finding how much the sentiment of a post's comment deviates from the sentiment of the post itself. In this axis we aggregated these deviations by topic."),
                html.Li("Relevance (x-axis) Scale(0, 1): Relevance is determined as shown previously. This axis shows the average relevance of comments aggregated by Topics."),
                html.Li("Comment Count (size): The size indicates how many comments belong to that Topic."),
                html.P("NOTE: Positive or negative controversy shows in which polarity the comments conflicted with their posts. This means that comments were either more positive or negative with respect the post they respond to.", className = 'card-subtitle'),

                
                
                dcc.Loading(children=[
                    dcc.Graph(id='viewpoints1'),
                ])
            ], style=PADDING_STYLE),
            dbc.Card([
                dcc.Loading(children=[
                    html.Div(children=[
                        dcc.Dropdown(
                            id='post_selection'
                        ),
                    ], style={'width': '70%', 'margin': '0 auto'}),
                    dcc.Graph(id='viewpoints2'),
                ])
            ], style=PADDING_STYLE),
        ])


@callback(
    Output('conflictprinter', 'children'),
    Output('viewpoints1', 'figure'),
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
        controversy_relevance_plot = cv_plot('scatter', fig1_df[1:], x_col='comment_relevance_mean', y_col='sentiment_diff_mean', size='sentiment_diff_size', title='r/'+df.iloc[0]['subreddit'], hover_name='comment_topics', labels={
                     "sentiment_diff_mean": "Average Controversy",
                     "comment_relevance_mean": "Average Comment Relevance"
                 })

        # relevance_avgs = []
        # for time in list(df[df['post_id'] == post_id_here].sort_values('comment_created', ascending=True)['comment_created']):
        #     relevance_avgs.append(df[(df['post_id'] == post_id_here) & (df['comment_created'] <= time)]['comment_relevance'].mean())

        return f'We used posts and comments sentiment scores as well as their relevance scores to identify conflicting viewpoints in r/{subreddit}.', controversy_relevance_plot
    except KeyError as e:
        print(e)
        return 'No data loaded! Go to Home Page first!', {}

@callback(
    Output('post_selection', 'options'),
    Output('post_selection', 'value'),
    Output('viewpoints2', 'figure'),
    Input('session', 'data'),
    Input('post_selection', 'value')
)
def update_graph_2(data, post_id):
    try:
        df = pd.DataFrame(data)
        subreddit = df.at[0, 'subreddit']
        
        post_id_list = df[['post_id', 'post_index', 'post_title']].groupby('post_id',as_index=False, sort=False).agg({'post_index': 'count', 'post_title': 'first'})
        post_id_list = post_id_list[post_id_list['post_index'] > 9].sort_values(by=['post_index'], ascending=False).reset_index(drop=True)

        # figure 2
        if post_id is None:
            post_id_here = post_id_list.at[0, 'post_id']
            post_title = post_id_list.at[0, 'post_title']
        else:
            # post_id_here = post_id
            post_title = post_id
            post_id_here = post_id_list[post_id_list['post_title'] == post_id].iloc[0]['post_id']

        sentiment_avgs = []
        for time in list(df[df['post_id'] == post_id_here].sort_values('comment_created', ascending=True)['comment_created']):
            sentiment_avgs.append(df[(df['post_id'] == post_id_here) & (df['comment_created'] <= time)]['comment_sentiment'].mean())

        comment_series_1_plot = px.line(sentiment_avgs, labels={
                     "index": "Number of Comments",
                     "value": "Average Comment Sentiment",
                     "variable": "Average Comment Sentiment"
                 }, title=df[df['post_id'] == post_id_here].iloc[0]['post_title'] + ' - ' + df.iloc[0]['subreddit'])
        comment_series_1_plot.update_layout(showlegend=False)

        return post_id_list['post_title'], post_title, comment_series_1_plot
    except KeyError as e:
        print(e)
        return [], '', {}
