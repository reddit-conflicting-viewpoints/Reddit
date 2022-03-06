from dash import dcc, html, Input, Output, callback
from pages.sas_key import get_csv_url
import plotly.express as px
from pages.visualize import *
import pandas as pd

layout = html.Div([
    html.Div([

        html.Div([
            html.P("X-Axis", style={'textAlign':'center'}),
            dcc.Dropdown(id='xaxis-column'),
            dcc.RadioItems(
                ['Linear', 'Log'],
                'Linear',
                id='xaxis-type',
                inline=True
            )
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            html.P("Y-Axis", style={'textAlign':'center'}),
            dcc.Dropdown(id='yaxis-column'),
            dcc.RadioItems(
                ['Linear', 'Log'],
                'Linear',
                id='yaxis-type',
                inline=True
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'),
    
    # dcc.Slider(
    #     df['Year'].min(),
    #     df['Year'].max(),
    #     step=None,
    #     id='year--slider',
    #     value=df['Year'].max(),
    #     marks={str(year): str(year) for year in df['Year'].unique()},
    # )
])


@callback(
    Output('indicator-graphic', 'figure'),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'),
    Input('xaxis-type', 'value'),
    Input('yaxis-type', 'value'),
    Input('session', 'data')
)
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type, data):
    
    subreddit = data
    df = pd.read_csv(get_csv_url(subreddit))

    fig = px.scatter(x=df[xaxis_column_name],
                     y=df[yaxis_column_name],
                     hover_name=df['post_id'].apply(lambda s: "Post ID: " + s))

    # fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    fig.update_xaxes(title=xaxis_column_name,
                     type='linear' if xaxis_type == 'Linear' else 'log')

    fig.update_yaxes(title=yaxis_column_name,
                     type='linear' if yaxis_type == 'Linear' else 'log')

    return fig

@callback(
    Output('xaxis-column', 'options'),
    Output('yaxis-column', 'options'),
    Input('session', 'data')
)
def update_dropdown(data):
    subreddit = data
    df = pd.read_csv(f'data/results/{subreddit}_hot_results.csv')
    return list(df.columns), list(df.columns)
