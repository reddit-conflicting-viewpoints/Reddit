from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
from pages.style import PADDING_STYLE


layout =html.Div([
            html.H1('Sentiment Analysis - Can we identify conflict with Sentiment?',style={'textAlign':'center'}),
            html.H3(id='sentimentsubredditprinter',style={'textAlign':'center'}),

            ### Sentiment Distribution Plots
            dbc.Card([
                html.H5("Sentiment Distribution", className="card-title"),
                html.Div(className='row', children=[
                    dcc.Loading(children=[
                        html.Div([
                            ### Post Score Plot
                            html.Div(className="six columns", children=[
                                dcc.Graph(id='sent1'),
                                # dcc.RangeSlider(0, 20, 1, value=[5, 15], id='my-range-slider'),
                            ]),
                            ### Comment Score Plot
                            html.Div(className="six columns", children=[
                                dcc.Graph(id="sent2"),
                            ])
                        ]),
                    ]),
                ]),
            ], style=PADDING_STYLE),
            ### End of plot

            ### Box Plot sentiment vs post_relevance
            dbc.Card([
                html.H5("Sentiment vs Post Relevance"),
                dcc.Loading(children=[
                    dcc.Graph(id='sent3'),
                ]),
            ], style=PADDING_STYLE),
            ### End Box Plot
        ])

@callback(
    Output('sentimentsubredditprinter', 'children'),
    Output('sent1', 'figure'),
    Output('sent2', 'figure'),
    Output('sent3', 'figure'),
    Input('session', 'data')
)
def update_graph(data):
    try:
        df = pd.DataFrame(data)
        subreddit = df.at[0, 'subreddit']

        # Post Sentiment
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

        post_df2 = df[['post_id', 'post_sentiment', 'comment_relevance']].groupby('post_id', as_index=False, sort=False).agg({'post_sentiment': 'first', 'comment_relevance': 'mean'})
        box_plot = px.box(post_df2, x="post_sentiment", y='comment_relevance').update_layout(xaxis_title="Sentiment", yaxis_title="Post Relevance", showlegend=False)

        return f'Subreddit: {subreddit}', post_sent_fig, comment_sent_fig, box_plot
    except KeyError as e:
        print(e)
        return 'No data loaded! Go to Home Page first!', {}, {}, {}
