# Code source: https://dash-bootstrap-components.opensource.faculty.ai/examples/simple-sidebar/
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
from pages import page1, page2

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "BEReddiT"

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
                dbc.NavLink("Page 1", href="/page1", active="exact"),
                dbc.NavLink("Page 2", href="/page2", active="exact"),
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
        return [html.H1('Welcome to BEReddiT',style={'textAlign':'center'})]
    elif pathname == "/page1":
        return page1.layout
    elif pathname == "/page2":
        return page2.layout
    # If the user tries to reach a different page, return a 404 message
    return html.H1('404: Page Not Found', style={'textAlign':'center'})


if __name__=='__main__':
    app.run_server(debug=True)
    # app.run_server(debug=False)
