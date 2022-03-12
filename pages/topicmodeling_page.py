from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from pages.style import PADDING_STYLE


layout =html.Div([
            html.H1('Topic Modeling - What are posts talking about?',style={'textAlign':'center'}),
            html.H3(id='topicsubredditprinter', style={'textAlign':'center'}),
    
            ### Comment Topic Modeling
            dbc.Card([
                html.H5("Comment Topic Modeling"),
                dcc.Loading(children=[
                    dcc.Graph(id='topic1'),
                ]),
            ], style=PADDING_STYLE),
            ### End Comment Topic Modeling
            ### Post Topic Modeling
            dbc.Card([
                html.H5("Post Topic Modeling"),
                dcc.Loading(children=[
                    dcc.Graph(id='topic2'),
                ]),
            ], style=PADDING_STYLE),
            ### End Post Topic Modeling
        ])

@callback(
    # Output('first', 'figure'),
    Output('topicsubredditprinter', 'children'),
    Output('topic1', 'figure'),
    Output('topic2', 'figure'),
    Input('session', 'data')
)
def update_graph(data):
    try:
        df = pd.DataFrame(data)
        subreddit = df.at[0, 'subreddit']
        
        # Topic modeling for comments
        comm_topics_fig = px.bar(df.comment_topics.value_counts()[1:16],
                                 title='<b>Top 15</b> Important Topics For Comments',
                                 labels={'index':'Topics', 'value':'Count (Number of Comments)'})
        comm_topics_fig.update_layout(showlegend=False)

        # Topic modeling for posts
        post_df = df[['post_topics', 'post_id']].groupby('post_topics', as_index=False).count()
        post_topics_fig = px.bar(post_df[1:16],
                                 x='post_topics',
                                 y='post_id',
                                 title='Important Topics For Posts',
                                 labels={'post_topics':'Topics', 'post_id':'Count (Number of Posts)'})
        post_topics_fig.update_layout(showlegend=False)

        return f'Subreddit: {subreddit}', comm_topics_fig, post_topics_fig
    except KeyError as e:
        print(e)
        return 'No data loaded! Go to Home Page first!', {}, {}
