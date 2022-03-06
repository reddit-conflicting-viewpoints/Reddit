from dash import dcc, html, Input, Output, callback
import plotly.express as px
from pages.visualize import *
import pandas as pd

layout = html.Div([
    html.H1('Welcome to BEReddiT',style={'textAlign':'center'})
])
