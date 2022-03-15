from dash import dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import numpy as np
import scipy.stats as stats
from pages.style import PADDING_STYLE

THRESHOLD = 0.5
TEXT_STYLE = {
    'textAlign':'center',
    'width': '70%',
    'margin': '0 auto',
    'background-color': 'AliceBlue',
    'color': 'Blue'
}
PASS_TEST = """
The p-value obtained is {pvalue:.2f}. The p-value is less than our significance level of 0.10.  
**Hence, we conclude that there `is` enough evidence to support that the comments are not relevant to their posts.**
"""

FAIL_TEST = """
The p-value obtained is {pvalue:.2f}. The p-value is greater than our significance level of 0.10.  
**Hence, we conclude that there `is not` enough evidence to support that the comments are not relevant to their posts.**
"""

layout =html.Div([
            html.H1('Relevance',style={'textAlign':'center'}),
            html.Div([
                html.H3("Are the comments in discussions relevant to the submission?", className="display-6 text-center"),
                html.P(id='relevancesubredditprinter',className='fs-4 text-center'),
                html.Hr(),
            ]), 
            ### Comment Relevance Histogram Distribution and T-Test
            dbc.Card([
                html.H5("Does this Subreddit have relevant discussion?", className = 'card-title'),
                html.P('This histogram shows us the frequency distribution of relevance scores across all comments in this subreddit. We included a dotted line at the 0.5 relevance mark as we found that to be a good indicator of having good relevance to the parent post in multiple subreddits. Any score >0.5 can be deemed as satisfactorily relevant. *NOTE: Negative relevance score may occur if the comment is too small to compare with its original post!', className = 'card-subtitle'),
                dcc.Loading(children=[
                    dcc.Graph(id='relevance1'),
                ]),
            ], style=PADDING_STYLE),
            ### End Comment Relevence Histogram

            ### Comment Relevance Table
            dbc.Card([
                html.H5("Comment Relevance Preview", className = 'card-title'),
                html.P('Check out how relevance scores reflect on a more granular level by looking at relevance scores for each comment with respect to their posts.', className = 'card-subtitle'),
                html.P("Click on a comment to see which post it refers to below.", style=TEXT_STYLE),
                dcc.Loading(children=[
                    dash_table.DataTable(id="reltable", page_size=10,
                                     style_header={'font-weight': 'bold'},
                                     style_data={'whiteSpace': 'normal'},
                                     columns=[{'name': 'Comment', 'id': 'Comment'}, {'name': 'Comment Relevance', 'id': 'Comment Relevance'}],
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
                                                 'filter_query': '{Comment Relevance} >= 0.5',
                                             },
                                             'backgroundColor': '#80ff59',
                                         },
                                         {
                                             'if': {
                                                 'filter_query': '{Comment Relevance} < 0.5',
                                             },
                                             'backgroundColor': '#ff6e6e',
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
                    html.Div(id='relposttable')
                ]),
            ], style=PADDING_STYLE),
            ### End Comment Relevance Table
    
            ### T-Test
            dbc.Card([
                html.H5("So, are the comments in this subreddit relevant to their posts?"),
                dcc.Loading(children=[
                    html.P(f"We use the Wilcoxon test for difference of medians to determine this. (Alternate Hypothesis: subreddit median relevance < {THRESHOLD}):"),
                    html.P(f"*Conducting test with 0.10 significance level"),
                    dcc.Markdown(id='relttest'),
                ])
            ], style=PADDING_STYLE)
            ### End T-Test
        ]),

@callback(
    Output('relevancesubredditprinter', 'children'),
    Output('relevance1', 'figure'),
    Output('relttest', 'children'),
    Output('reltable', 'data'),
    Input('session', 'data')
)
def update_graph(data):
    try:
        df = pd.DataFrame(data)
        subreddit = df.at[0, 'subreddit']

        # Generate Comment Relevance Histogram Distribution plot
        df["color"] = np.select(
                                [df["comment_relevance"].gt(THRESHOLD), df["comment_relevance"].lt(THRESHOLD)],
                                ["green", "red"],
                                "orange")
        comm_relevance_dist = px.histogram(df,
                                           x="comment_relevance",
                                           title='Distribution of Comment Relevance',
                                           labels={'comment_relevance':'Comment Relevance Score', 'count':'Number of Comments', 'color':'Comment Relevance Score'},
                                           color="color",
                                           color_discrete_map={
                                           "green": "#80ff59",
                                           "red": "#ff6e6e",
                                           "orange": "orange"})
        comm_relevance_dist.update_layout(yaxis_title="Number of Comments", showlegend=False)
        comm_relevance_dist.add_vline(x=THRESHOLD, line_width=3, line_dash="dash", line_color="black")

        # Hypothesis Test
        # test = stats.ttest_1samp(a=df.comment_relevance, popmean=THRESHOLD, alternative='less')
        comment_relevance_scores = df.comment_relevance.to_numpy()
        comment_relevance_scores = comment_relevance_scores - THRESHOLD
        test = stats.wilcoxon(x=comment_relevance_scores, alternative='less')
        if test.pvalue > 0.1:
            test_output = FAIL_TEST.format(pvalue=test.pvalue)
        else:
            test_output = PASS_TEST.format(pvalue=test.pvalue)

        # Comment Relevance Table
        comment_df = df[['comment', 'comment_relevance', 'post_id']].copy()
        comment_df['id'] = comment_df.post_id

        comment_df.rename(columns={'comment': 'Comment', 'comment_relevance': 'Comment Relevance'}, inplace=True)
        return f'For r/{subreddit}, we calculated relevance scores on a real number scale from 0 to 1 to see how relevant comments were to their original posts, 0 showing no relevance at all and 1 meaning extremely relevant. We believe relevance to be an important factor in deciding if a discussion is propagating in the right direction.', comm_relevance_dist, test_output, comment_df.to_dict('records')
    except KeyError as e:
        print(e)
        return 'No data loaded! Go to Home Page first!', {}, "", []

@callback(
    Output('relposttable', 'children'),
    Input('session', 'data'),
    Input('reltable', 'active_cell')
)
def display_post(data, active_cell):
    if active_cell is None:
        return ""

    df = pd.DataFrame(data)
    selected = df[df['post_id'] == active_cell['row_id']]
    selected = selected[['post_id', 'post_title', 'post_body']].groupby('post_id').first()
    selected.rename(columns={'post_title': 'Post Title', 'post_body': 'Post Body'}, inplace=True)

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
