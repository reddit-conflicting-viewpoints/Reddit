# Code source: https://dash-bootstrap-components.opensource.faculty.ai/examples/simple-sidebar/
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
from pages import relevance_page, sentimentanalysis_page, topicmodeling_page

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "BEReddiT"

server = app.server

# Read the list of available subreddits
file1 = open("pages/subreddit_list.txt", "r")
subreddits = file1.readlines()
subreddits = list(map(lambda item: item.replace('\n', ''), subreddits))
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
    dcc.Store(id='session', storage_type='session', data='computerscience'),
    sidebar,
    content
])


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        # Can add more items to the list, for more content in homepage.
        return html.Div([

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
    elif pathname == "/relevance":
        return relevance_page.layout
    elif pathname == "/topicmodeling":
        return topicmodeling_page.layout
    elif pathname == "/sentimentanalysis":
        return sentimentanalysis_page.layout
    # If the user tries to reach a different page, return a 404 message
    return html.H1('404: Page Not Found', style={'textAlign':'center'})

@app.callback(
    Output('session', 'data'),
    Input('data', 'value')
)
def update_df(value):
    return value


if __name__=='__main__':
    app.run_server(debug=True)
    # app.run_server(debug=False)
