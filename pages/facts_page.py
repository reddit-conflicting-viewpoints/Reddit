from dash import dcc, html, Input, Output, callback, dash_table
import plotly.express as px
import pandas as pd
from pages.sas_key import get_df_description

TEXT_STYLE = {
    'textAlign':'center',
    'width': '70%',
    'margin': '0 auto',
}

layout =html.Div([
            dcc.Loading(children=[
                html.H1('Quick Facts',style={'textAlign':'center'}),
                html.H3(id="factssubredditprinter", style={'textAlign':'center'}),
                html.H5("Subreddit Description:", style=TEXT_STYLE),
                html.P(id='subredditdescription', style=TEXT_STYLE),
                html.H5("Subreddit Quick Facts:", style=TEXT_STYLE),
                dash_table.DataTable(id="subredditfacts",
                                     style_header={'font-weight': 'bold'},
                                     style_cell={'font-family':'sans-serif'},
                                     style_data={'whiteSpace': 'normal', 'height': 'auto'}),

                html.H5("Post Data Preview:", style=TEXT_STYLE),
                ### Posts Table
                dash_table.DataTable(id="subreddittable", page_size=5,
                                     # fixed_rows={'headers': True},
                                     style_header={'font-weight': 'bold'},
                                     style_data={'whiteSpace': 'normal'},
                                     style_cell={'font-family':'sans-serif', 'textAlign': 'left'},
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
                ### End of table
                html.H5("Comments Data Preview:", style=TEXT_STYLE),
                ### Comments Table
                dash_table.DataTable(id="subredditcommenttable", page_size=5,
                                     # fixed_rows={'headers': True},
                                     style_header={'font-weight': 'bold'},
                                     style_data={'whiteSpace': 'normal'},
                                     style_cell={'font-family':'sans-serif', 'textAlign': 'left'},
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
                ### End of table
            ], fullscreen=True),
        ])

@callback(
    Output('factssubredditprinter', 'children'),
    Output('subredditdescription', 'children'),
    Output('subredditfacts', 'data'),
    Output('subreddittable', 'data'),
    Output('subredditcommenttable', 'data'),
    Input('session', 'data')
)
def update_df(data):
    # Load the data
    df = pd.DataFrame(data)
    subreddit = df.at[0, 'subreddit']
    subreddit_df = get_df_description(subreddit)

    # Obtain description of the subreddit
    description = subreddit_df.at[0, 'description']

    # Posts Table
    post_df = df[['post_id', 'post_title', 'post_body']].groupby('post_id', as_index=False, sort=False).first()
    post_df.rename(columns={'post_id': 'Post Id', 'post_title': 'Post Title', 'post_body': 'Post Body'}, inplace=True)

    # Comments Table
    comment_df = df[['post_id', 'comment_id', 'comment']].copy()
    comment_df.rename(columns={'post_id': 'Post Id', 'comment_id': 'Comment Id', 'comment': 'Comment'}, inplace=True)

    # Quick Facts Table
    number_of_posts = len(post_df)
    number_of_comments = len(df)
    facts = [{
        "Number of hot posts scraped": number_of_posts,
        "Number of hot comments scraped": number_of_comments,
        "Number of subscribers": subreddit_df.at[0, 'subscribers']
    }]
    return f"Selected: {subreddit}", description, facts, post_df.to_dict('records'), comment_df.to_dict('records')
