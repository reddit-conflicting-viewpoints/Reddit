from dash import dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import numpy as np
import scipy.stats as stats
from pages.style import PADDING_STYLE

THRESHOLD = 0.5

PASS_TEST = """
The p-value obtained is {pvalue:.2f}. The p-value is less than our significance level of 0.10.  
**Therefore, we conclude that there is enough evidence to support that the comments are not relevant to their posts.**
"""

FAIL_TEST = """
The p-value obtained is {pvalue:.2f}. The p-value is greater than our significance level of 0.10.  
**Therefore, we conclude that there is not enough evidence to support that the comments are not relevant to their posts.**
"""

layout =html.Div([
            html.H1('Relevance - Are the comments in discussions relevant to the submission?',style={'textAlign':'center'}),
            html.H3(id="relevancesubredditprinter", style={'textAlign':'center'}),

            ### Comment Relevance Histogram Distribution and T-Test
            dbc.Card([
                html.H5("Comment Relevance Histogram"),
                dcc.Loading(children=[
                    dcc.Graph(id='relevance1'),
                ]),
            ], style=PADDING_STYLE),
            ### End Comment Relevence Histogram

            ### Comment Relevance Table
            dbc.Card([
                html.H5("Comment Relevance Table"),
                dcc.Loading(children=[
                    dash_table.DataTable(id="reltable", page_size=10,
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
                                     style_data_conditional=[
                                         {
                                             'if': {
                                                 'filter_query': '{Comment Relevance} >= 0.5',
                                             },
                                             'backgroundColor': 'lightgreen',
                                         },
                                         {
                                             'if': {
                                                 'filter_query': '{Comment Relevance} < 0.5',
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
            ], style=PADDING_STYLE),
            ### End Comment Relevance Table
    
            ### T-Test
            dbc.Card([
                html.H5("Are the comments in the subreddit relevant to their posts?"),
                dcc.Loading(children=[
                    html.P(f"Wilcoxon test for difference of medians (Alternate Hypothesis: subreddit median relevance < {THRESHOLD}):"),
                    html.P(f"Conducting test with 0.10 significance level"),
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
                                           labels={'comment_relevance':'Comment Relevance Score', 'count':'Number of Comments'},
                                           opacity=0.6, 
                                           color="color",
                                           color_discrete_map={
                                           "green": "green",
                                           "red": "red",
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
        comment_df = df[['comment', 'comment_relevance']].copy()

        comment_df.rename(columns={'comment': 'Comment', 'comment_relevance': 'Comment Relevance'}, inplace=True)
        return f'Subreddit: {subreddit}', comm_relevance_dist, test_output, comment_df.to_dict('records')
    except KeyError as e:
        print(e)
        return 'No data loaded! Go to Home Page first!', {}, "", []
