from dash import dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
import scipy.stats as stats
from pages.style import PADDING_STYLE


layout =html.Div([
            html.H1('Sentiment Analysis',style={'textAlign':'center'}),

            html.Div([
                html.H3("Let's identify conflict with Sentiment", className="display-6 text-center"),
                html.H3(id='sentimentsubredditprinter',className='fs-4 text-center'),
                html.Hr(),
            ]), 
            ### Sentiment post and comment Distribution Plots
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

            dbc.Card([
                html.H5("Comment Sentiment Table"),
                dcc.Loading(children=[
                    dash_table.DataTable(id="senttable", page_size=10,
                                     style_header={'font-weight': 'bold'},
                                     style_data={'whiteSpace': 'normal'},
                                     columns=[{'name': 'Comment', 'id': 'Comment'}, {'name': 'Comment Sentiment', 'id': 'Comment Sentiment'}],
                                     style_cell={
                                             'font-family':'sans-serif',
                                             'textAlign': 'left',
                                             'font-size': '14px',
                                             'padding-top': '3px',
                                             'padding-bottom': '8px',
                                             'padding-left': '8px',
                                             'padding-right': '8px',
                                         },
                                     style_data_conditional=[
                                         {
                                             'if': {
                                                 'filter_query': '{Comment Sentiment} = 5',
                                             },
                                             'backgroundColor': '#91ff78',
                                         },
                                                                                  {
                                             'if': {
                                                 'filter_query': '{Comment Sentiment} = 4',
                                             },
                                             'backgroundColor': '#ddffb6',
                                         },
                                        {
                                             'if': {
                                                 'filter_query': '{Comment Sentiment} = 3',
                                             },
                                             'backgroundColor': '#b6d7ff',
                                         },
                                        {
                                             'if': {
                                                 'filter_query': '{Comment Sentiment} = 2',
                                             },
                                             'backgroundColor': '#f9b6ff',
                                         },
                                         {
                                             'if': {
                                                 'filter_query': '{Comment Sentiment} = 1',
                                             },
                                             'backgroundColor': '#FFB6C1',
                                         }
                                     ],
                                     css=[{
                                         'selector': '.dash-spreadsheet td div',
                                         'rule': '''
                                             line-height: 15px;
                                             max-height: 75px; min-height: 33px;
                                             display: block;
                                             overflow-y: auto;
                                         '''
                                    }]
                    )
                ]),
                dcc.Loading(children=[
                    html.Div(id='posttable')
                ]),
            ], style=PADDING_STYLE),
        ])

@callback(
    Output('sentimentsubredditprinter', 'children'),
    Output('sent1', 'figure'),
    Output('sent2', 'figure'),
    Output('senttable', 'data'),
    Input('session', 'data')
)
def update_graph(data):
    try:
        df = pd.DataFrame(data)
        subreddit = df.at[0, 'subreddit']

        # figure 1: Post Sentiment
        post_df = df[['post_id', 'post_sentiment']].groupby('post_id', as_index=False, sort=False).first()
        post_df["color"] = np.select(
            [post_df["post_sentiment"].eq(5), post_df["post_sentiment"].eq(4), post_df["post_sentiment"].eq(2), post_df["post_sentiment"].eq(1)],
            ["green", "lightgreen", "orange", "red"],
            "blue"
        )
        post_sent_fig = px.histogram(post_df, 
                                     x="post_sentiment",
                                     title='Sentiment Distribution for Posts',
                                     text_auto=True, 
                                     color="color",
                                     color_discrete_map={
                                         "green": "#91ff78",
                                         "lightgreen": "#ddffb6",
                                         "orange": "#f9b6ff",
                                         "red": "#FFB6C1",
                                         "blue": "#b6d7ff"
                                     }).update_layout(
                                     xaxis_title="Sentiment", yaxis_title="Number of Posts", showlegend=False)

        # figure 2
        df.dropna(inplace=True, subset=['comment_sentiment'])
        df["color"] = np.select(
            [df["comment_sentiment"].eq(5), df["comment_sentiment"].eq(4), df["comment_sentiment"].eq(2), df["comment_sentiment"].eq(1)],
            ["green", "lightgreen", "orange", "red"],
            "blue"
        )
        comment_sent_fig = px.histogram(df, 
                                        x="comment_sentiment",
                                        title='Sentiment Distribution for Comments',
                                        text_auto=True,
                                        color="color",
                                        color_discrete_map={
                                        "green": "#91ff78",
                                         "lightgreen": "#ddffb6",
                                         "orange": "#f9b6ff",
                                         "red": "#FFB6C1",
                                         "blue": "#b6d7ff"
                                        }).update_layout(
                                        xaxis_title="Sentiment", yaxis_title="Number of Comments", showlegend=False)


        # print("mean: ", np.mean(post_df['post_sentiment']))
        # print("mean: ", np.mean(df['comment_sentiment']))
        # print("median: ", np.median(post_df['post_sentiment']))
        # print("median: ", np.median(df['comment_sentiment']))
#         ### Post sentiment test
#         post_sentiment_scores = post_df.post_sentiment.to_numpy()
#         post_sentiment_scores = post_sentiment_scores - 3
#         test = stats.wilcoxon(x=post_sentiment_scores, alternative='less')
#         print(test)

#         ### Comment sentiment test
#         comment_sentiment_scores = df.comment_sentiment.to_numpy()
#         comment_sentiment_scores = comment_sentiment_scores - 3
#         test = stats.wilcoxon(x=comment_sentiment_scores, alternative='less')
#         print(test)

        # Comment Relevance Table
        comment_df = df[['comment', 'comment_sentiment', 'post_id']].copy()
        comment_df['id'] = comment_df.post_id

        comment_df.rename(columns={'comment': 'Comment', 'comment_sentiment': 'Comment Sentiment'}, inplace=True)
        return f"Let's look at the sentiments of posts and comments in r/{subreddit} to see if we can identify conflict of interests with respect to comments and their posts. Here, sentiments are labeled on a scale of 1-5: 1 being negative sentiments, 3 being neutral and 5 being positive sentiments. Usually negative sentiments are the ones that project conflict.", post_sent_fig, comment_sent_fig, comment_df.to_dict('records')
    except KeyError as e:
        print(e)
        return 'No data loaded! Go to Home Page first!', {}, {}, []

@callback(
    Output('posttable', 'children'),
    Input('session', 'data'),
    Input('senttable', 'active_cell')
)
def display_post(data, active_cell):
    if active_cell is None:
        return ""

    df = pd.DataFrame(data)
    selected = df[df['post_id'] == active_cell['row_id']]
    selected = selected[['post_id', 'post_title', 'post_body']].groupby('post_id').first()

    table = dash_table.DataTable(selected.to_dict('records'), page_size=5,
                                 style_header={'font-weight': 'bold'},
                                 style_data={'whiteSpace': 'normal'},
                                 style_cell={
                                     'font-family':'sans-serif',
                                     'textAlign': 'left',
                                     'font-size': '14px',
                                     'padding-top': '3px',
                                     'padding-bottom': '8px',
                                     'padding-left': '8px',
                                     'padding-right': '8px',
                                 },
                                 css=[{
                                     'selector': '.dash-spreadsheet td div',
                                     'rule': '''
                                         line-height: 15px;
                                         max-height: 75px; min-height: 33px;
                                         display: block;
                                         overflow-y: auto;
                                     '''
                                }]
            ),
    return table
