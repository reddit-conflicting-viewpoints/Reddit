from dash import dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from pages.sas_key import get_df_description
from pages.style import PADDING_STYLE

TEXT_STYLE = {
    'textAlign':'center',
    'width': '70%',
    'margin': '0 auto',
}

layout =html.Div([
            html.H1('Subreddit Information',style={'textAlign':'center'}),
            html.H3(id="factssubredditprinter", style={'textAlign':'center'}),
            dbc.Card(style=PADDING_STYLE, children=[
                html.H5("Subreddit Description"),
                dcc.Loading(children=[
                    html.P(id='subredditdescription', style=TEXT_STYLE),
                ]),
            ]),
            dbc.Card([
                html.H5("Subreddit Quick Facts", className="card-title"),
                dcc.Loading(children=[
                    # html.H5("Subreddit Quick Facts", style=TEXT_STYLE),
                    dash_table.DataTable(id="subredditfacts",
                                         style_header={'font-weight': 'bold'},
                                         style_cell={'font-family':'sans-serif', 'font-size': '14px'},
                                         style_data={'whiteSpace': 'normal', 'height': 'auto'}),
                ])
            ], style=PADDING_STYLE),

            ### Posts Table
            dbc.Card([
                html.H5("Post Data Preview", className="card-title"),
                dcc.Loading(children=[
                # html.H5("Post Data Preview", style=TEXT_STYLE),
                    dash_table.DataTable(id="subreddittable", page_size=5,
                                         # fixed_rows={'headers': True},
                                         style_header={'font-weight': 'bold'},
                                         style_data={'whiteSpace': 'normal'},
                                         style_cell={'font-family':'sans-serif', 'textAlign': 'left', 'font-size': '14px'},
                                         columns=[{'name': 'post_id', 'id': 'post_id'}, {'name': 'post_title', 'id': 'post_title'}, {'name': 'post_body', 'id': 'post_body'}],
                                         css=[{
                                             'selector': '.dash-spreadsheet td div',
                                             'rule': '''
                                                 line-height: 15px;
                                                 max-height: 70px; min-height: 33px;
                                                 display: block;
                                                 overflow-y: auto;
                                             '''
                                        }]
                    ),
                ]),
            # ], style=PADDING_STYLE),
            ### End of table
            ### Comments Table
            # dbc.Card([
                html.H5("Comments Data Preview", className="card-title"),
                dcc.Loading(children=[
                    # html.H5("Comments Data Preview", style=TEXT_STYLE),
                    # html.P("Click a post in the above Post Table to view comments for that post", style=TEXT_STYLE),
                    html.P("Click a post in the above Post Table to view comments for that post"),
                    dash_table.DataTable(id="subredditcommenttable", page_size=5,
                                         # fixed_rows={'headers': True},
                                         style_header={'font-weight': 'bold'},
                                         style_data={'whiteSpace': 'normal'},
                                         style_cell={'font-family':'sans-serif', 'textAlign': 'left', 'font-size': '14px'},
                                         css=[{
                                             'selector': '.dash-spreadsheet td div',
                                             'rule': '''
                                                 line-height: 15px;
                                                 max-height: 70px; min-height: 33px;
                                                 display: block;
                                                 overflow-y: auto;
                                             '''
                                        }]
                    )
                ])
            ], style=PADDING_STYLE),
            ### End of table

            ### Score Frequency Plots
            dbc.Card([
                html.H5("Score Frequency Distribution Plots", className="card-title"),
                html.Div(className='row', children=[
                    dcc.Loading(children=[
                        html.Div([
                            ### Post Score Plot
                            html.Div(className="six columns", children=[
                                dcc.Graph(id='facts1'),
                                # dcc.RangeSlider(0, 20, 1, value=[5, 15], id='my-range-slider'),
                            ]),
                            ### Comment Score Plot
                            html.Div(className="six columns", children=[
                                dcc.Graph(id="facts2"),
                            ])
                        ]),
                    ]),
                ]),
            ], style=PADDING_STYLE),
            ### End of plot

            ### Word Count Frequency Plots
            dbc.Card([
                html.H5("Word Count Frequency Distribution Plots", className="card-title"),
                html.Div(className='row', children=[
                    dcc.Loading(children=[
                        html.Div([
                            ### Post Word Count Plot
                            html.Div(className="six columns", children=[
                                dcc.Graph(id='facts3'),
                            ]),
                            ### Comment Word Count Plot
                            html.Div(className="six columns", children=[
                                dcc.Graph(id="facts4"),
                            ])
                        ]),
                    ]),
                ]),
            ], style=PADDING_STYLE),
            ### End of plot
        ])

@callback(
    Output('factssubredditprinter', 'children'),
    Output('subredditdescription', 'children'),
    Output('subredditfacts', 'data'),
    Output('subreddittable', 'data'),
    Output('facts1', 'figure'),
    Output('facts2', 'figure'),
    Output('facts3', 'figure'),
    Output('facts4', 'figure'),
    Input('session', 'data'),
)
def update_df(data):
    try:
        # Load the data
        df = pd.DataFrame(data)
        subreddit = df.at[0, 'subreddit']
        subreddit_df = get_df_description(subreddit)

        # Obtain description of the subreddit
        description = subreddit_df.at[0, 'description']

        # Posts Table
        post_df = df[['post_id', 'post_title', 'post_body', 'post_score']].groupby('post_id', as_index=False, sort=False).first()
        post_df['id'] = post_df.post_id
        # post_df.rename(columns={'post_id': 'Post Id', 'post_title': 'Post Title', 'post_body': 'Post Body'}, inplace=True)

        # Quick Facts Table
        number_of_posts = len(post_df)
        number_of_comments = len(df)
        facts = [{
            "Number of hot posts scraped": number_of_posts,
            "Number of hot comments scraped": number_of_comments,
            "Number of subscribers": subreddit_df.at[0, 'subscribers']
        }]

        # Post Score Plot
        posts_score_hist = px.histogram(post_df, 
                                        x="post_score",
                                        title='Frequency Distribution of Post Score',
                                        labels={'score':'Score', 'count':'Number of Posts'},
                                        opacity=0.8,
                                        color_discrete_sequence=['indianred'],
                                        text_auto=True).update_layout(
                                        yaxis_title="Number of Posts")

        # Comment Score Plot
        comms_score_hist = px.histogram(df,                                
                                x="comment_score",
                                log_y=True,
                                title='Frequency Distribution of Comment Score',
                                opacity=0.8).update_layout(
                                xaxis_title="Score", yaxis_title="Number of Comments (log scale)")

        post_df['word_counts'] = post_df.post_title.str.cat(post_df.post_body, sep=" ").str.split().apply(len)
        df['word_counts'] = df.comment.astype(str).str.split().apply(len)

        # Post Word Count Distribution
        post_word_count = px.histogram(post_df, 
                                       x="word_counts",
                                       title='Word-Count Distribution for Posts',
                                       labels={'word_counts':'Word Count', 'count':'Number of Posts'},
                                       opacity=0.8,
                                       color_discrete_sequence=['indianred'],
                                       text_auto=True).update_layout(
                                       yaxis_title="Number of Posts")

        # Comment Word Count Distribution
        comms_word_count = px.histogram(df, 
                           x="word_counts",
                           log_y=True,
                           title='Word-Count Distribution for Comments',
                           opacity=0.8).update_layout(
                           xaxis_title="Word Count", yaxis_title="Number of Comments (log scale)")

        return f"Selected: {subreddit}", description, facts, post_df.to_dict('records'), posts_score_hist, comms_score_hist, post_word_count, comms_word_count
    except KeyError as e:
        print(e)
        return 'No data loaded! Go to Home Page first!', "", [], [], {}, {}, {}, {}

@callback(
    Output('subredditcommenttable', 'data'),
    Input('session', 'data'),
    Input('subreddittable', 'active_cell')
)
def update_comment_table(data, active_cell):
    try:
        # Load DataFrame
        df = pd.DataFrame(data)
        
        # Comments Table
        comment_df = df[['post_id', 'comment']].copy()
        comment_df.rename(columns={'post_id': 'Post Id', 'comment': 'Comment'}, inplace=True)
        
        if active_cell is not None:
            comment_df = comment_df[comment_df['Post Id'] == active_cell['row_id']]
        return comment_df.to_dict('records')
    except KeyError as e:
        print(e)
        return []
