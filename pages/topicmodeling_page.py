from dash import dcc, html, Input, Output, callback
import plotly.express as px
from pages.visualize import *
import pandas as pd

df = pd.read_csv('data/results/computerscience_hot_results.csv')

layout = html.Div([
    html.H1('Welcome to BEReddiT',style={'textAlign':'center'})
])
