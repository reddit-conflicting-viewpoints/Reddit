# Code source: https://dash-bootstrap-components.opensource.faculty.ai/examples/simple-sidebar/
import dash
from dash import html, dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
from pages.sas_key import get_df
from pages.visualize import *
#from pages import relevance_page, sentimentanalysis_page, topicmodeling_page

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "BEReddiT"

server = app.server

global df
global subreddit

# Read the list of available subreddits
file1 = open("pages/subreddit_list.txt", "r")
subreddits = file1.readlines()
subreddits = list(set(map(lambda item: item.replace('\n', ''), subreddits)))
subreddits.sort()
file1.close()

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

# Center of Div
CENTER_STYLE = {
    'width': '50%',
    'margin': '0 auto',
}

sidebar = html.Div(
    [
        html.H2("BEReddiT", className="display-4"),
        html.Hr(),
        html.P(
            "Visualization Dashboard", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Relevance", href="/relevance", active="exact"),
                dbc.NavLink("Topic Modeling", href="/topicmodeling", active="exact"),
                dbc.NavLink("Sentiment Analysis", href="/sentimentanalysis", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    dcc.Loading(children=[dcc.Store(id='session', storage_type='local')], fullscreen=True),
    sidebar,
    content
])


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    try:
        ### Home Page
        if pathname == "/":
            # Can add more items to the list, for more content in homepage.
            return  html.Div([

                        # Welcome Header
                        html.H1('Welcome to BEReddiT', style={'textAlign':'center'}),

                        # Introduction Paragraph
                        html.Div([
                            html.P('Add an Introduction here!', style={'textAlign':'center'})
                        ], style=CENTER_STYLE),

                        # Drop down menu for selecting SubReddit
                        html.Div([
                            html.P('Pick a SubReddit to Analyze', style={'textAlign':'center'}),
                            dcc.Dropdown(
                                subreddits,
                                "computerscience",
                                id='data'
                            )
                        ], style=CENTER_STYLE)
                    ])

        ### Relevance Page
        elif pathname == "/relevance":
            return  html.Div([
                        html.H1('Relevance - Are the comments in discussions relevant to the submission?',style={'textAlign':'center'}),
                        html.H3(f'Subreddit: {subreddit}',style={'textAlign':'center'}),
                        dcc.Loading(children=[dcc.Graph(id='first')], fullscreen=True),
                    ])

        ### Topic Modeling Page
        elif pathname == "/topicmodeling":
            return  html.Div([
                        html.H1('Topic Modeling - What are posts talking about?',style={'textAlign':'center'}),
                        html.H3(f'Subreddit: {subreddit}',style={'textAlign':'center'}),
                    ])

        ### Sentiment Page
        elif pathname == "/sentimentanalysis":
            return  html.Div([
                        html.H1('Sentiment Analysis - Can we identify conflict with Sentiment?',style={'textAlign':'center'}),
                        html.H3(f'Subreddit: {subreddit}',style={'textAlign':'center'}),
                        html.Div([
                            html.Div([
                                html.P("X-Axis", style={'textAlign':'center'}),
                                dcc.Dropdown(id='xaxis-column', options=df.columns, value='post_score'),
                                dcc.RadioItems(
                                    ['Linear', 'Log'],
                                    'Linear',
                                    id='xaxis-type',
                                    inline=True
                                )
                            ], style={'width': '48%', 'display': 'inline-block'}),

                            html.Div([
                                html.P("Y-Axis", style={'textAlign':'center'}),
                                dcc.Dropdown(id='yaxis-column', options=df.columns, value='post_upvote_ratio'),
                                dcc.RadioItems(
                                    ['Linear', 'Log'],
                                    'Linear',
                                    id='yaxis-type',
                                    inline=True
                                )
                            ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
                        ]),

                        dcc.Loading(children=[dcc.Graph(id='indicator-graphic')], fullscreen=True),

                        # dcc.Slider(
                        #     df['Year'].min(),
                        #     df['Year'].max(),
                        #     step=None,
                        #     id='year--slider',
                        #     value=df['Year'].max(),
                        #     marks={str(year): str(year) for year in df['Year'].unique()},
                        # )
                    ])
    except NameError:
        return html.H1('No data loaded. Head to Home Page First!', style={'textAlign':'center'})

    ### 404 Page
    # If the user tries to reach a different page, return a 404 message
    return html.H1('404: Page Not Found', style={'textAlign':'center'})

@app.callback(
    Output('session', 'data'),
    Input('data', 'value')
)
def update_df(value):
    global df
    df = get_df(value)
    global subreddit
    subreddit = value
    return ""

@callback(
    Output('first', 'figure'),
    Input('session', 'data')
)
def update_graph(data):
    global df
    global subreddit
    return px.histogram(df, x="comment_relevance", title=f'Comment Relevance Histogram (Subreddit: {subreddit})')
    # return plot('scatter', df, x_col='comment_relevance', y_col='comment_score', title=subreddit, threshold_col='comment_relevance', threshold_min=0.5, threshold_max=1)

@callback(
    Output('indicator-graphic', 'figure'),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'),
    Input('xaxis-type', 'value'),
    Input('yaxis-type', 'value'),
    Input('session', 'data')
)
def update_graph2(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type, data):
    global subreddit
    global df

    fig = px.scatter(x=df[xaxis_column_name],
                     y=df[yaxis_column_name],
                     hover_name=df['post_id'].apply(lambda s: "Post ID: " + s))

    # fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    fig.update_xaxes(title=xaxis_column_name,
                     type='linear' if xaxis_type == 'Linear' else 'log')

    fig.update_yaxes(title=yaxis_column_name,
                     type='linear' if yaxis_type == 'Linear' else 'log')
    return fig


if __name__=='__main__':
    app.run_server(debug=True)
    # app.run_server(debug=False)
