# Code source: https://dash-bootstrap-components.opensource.faculty.ai/examples/simple-sidebar/
import dash
from dash import html, dcc, callback, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
from pages.sas_key import get_df, get_df_description
from pages.visualize import *
import pandas as pd
from pages import relevance_page, facts_page, topicmodeling_page, sentimentanalysis_page, conflictingviewpoints_page

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://codepen.io/chriddyp/pen/bWLwgP.css'], suppress_callback_exceptions=True)
app.title = "BEReddiT"

server = app.server

# Read the list of available subreddits
file1 = open("pages/subreddit_list.txt", "r")
subreddits = file1.readlines()
subreddits = list(set(map(lambda item: item.replace('\n', ''), subreddits)))
subreddits.sort(key=str.lower)
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
    'width': '70%',
    'margin': '0 auto',
}

TEXT_STYLE = {
    'textAlign':'center',
    'width': '70%',
    'margin': '0 auto',
}

sidebar = html.Div(
    [
        html.H2("BEReddiT", className="display-5"),
        html.Hr(),
        html.P(
            "Visualization Dashboard", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Subreddit", href="/facts", active="exact"),
                dbc.NavLink("Relevance", href="/relevance", active="exact"),
                dbc.NavLink("Topic Modeling", href="/topicmodeling", active="exact"),
                dbc.NavLink("Sentiment Analysis", href="/sentimentanalysis", active="exact"),
                dbc.NavLink("Conflicting Viewpoints", href="/conflictingviewpoints", active="exact"),
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
    dcc.Loading(children=[dcc.Store(id='session', storage_type='memory')], fullscreen=True),
    # dcc.Loading(children=[html.Div(id='session', style={'display':'none'})], fullscreen=True),
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
                            html.Div([
                                dcc.Dropdown(
                                    subreddits,
                                    "computerscience",
                                    id='data',
                                )
                            ], style=CENTER_STYLE),
                            html.H3(id="homesubredditprinter", style=TEXT_STYLE),
                            html.P("Click on a tab to view analysis on the selected subreddit!", style={'textAlign':'center'})
                        ])
                    ])
        
        ### Quick Facts Page
        elif pathname == "/facts":
            return facts_page.layout

        ### Relevance Page
        elif pathname == "/relevance":
            return relevance_page.layout

        ### Topic Modeling Page
        elif pathname == "/topicmodeling":
            return topicmodeling_page.layout

        ### Sentiment Page
        elif pathname == "/sentimentanalysis":
            return sentimentanalysis_page.layout

        ### Conflicting Viewpoints Page
        elif pathname == "/conflictingviewpoints":
            return conflictingviewpoints_page.layout

    except ValueError as e:
        print(e)
        return html.H1('No data loaded. Head to Home Page First!', style={'textAlign':'center'})
    except NameError as e:
        print(e)
        return html.H1('No data loaded. Head to Home Page First!', style={'textAlign':'center'})


    ### 404 Page
    # If the user tries to reach a different page, return a 404 message
    return html.H1('404: Page Not Found', style={'textAlign':'center'})

### USED TO UPDATE THE DF FROM HOME PAGE
@app.callback(
    Output('session', 'data'),
    Output('homesubredditprinter', 'children'),
    Input('data', 'value')
)
def update_df(value):
    # Load the data
    df = get_df(value)
    return df.to_dict("records"), f"Selected: {value}"


if __name__=='__main__':
    app.run_server(debug=True)
    # app.run_server(debug=False)
