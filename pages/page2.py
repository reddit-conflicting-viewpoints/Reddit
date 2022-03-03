from dash import dcc, html, Input, Output, callback
import plotly.express as px
from pages.visualize import *
import pandas as pd

df = pd.read_csv('data/results/computerscience_hot_results.csv')

layout = html.Div([
    html.Div([

        html.Div([
            html.P("X-Axis", style={'textAlign':'center'}),
            dcc.Dropdown(
                df.columns,
                'post_score',
                id='xaxis-column'
            ),
            dcc.RadioItems(
                ['Linear', 'Log'],
                'Linear',
                id='xaxis-type',
                inline=True
            )
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            html.P("Y-Axis", style={'textAlign':'center'}),
            dcc.Dropdown(
                df.columns,
                'post_upvote_ratio',
                id='yaxis-column'
            ),
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
    
    
    html.H3('Page 2'),
    dcc.Dropdown(
        {f'Page 2 - {i}': f'{i}' for i in ['New York City', 'Montreal', 'Los Angeles']},
        id='page-2-dropdown'
    ),
    html.Div(id='page-2-display-value'),
    dcc.Link('Go to Page 1', href='/page1'),
    dcc.Graph(id='indicator-graphic2', figure=plot('scatter', df, x_col='comment_relevance', y_col='comment_score', title='Computer Science', threshold_col='comment_relevance', threshold_min=0.5, threshold_max=1, color='comment_controversiality'))

])


@callback(
    Output('indicator-graphic', 'figure'),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'),
    Input('xaxis-type', 'value'),
    Input('yaxis-type', 'value'))
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type):

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
    Output('page-2-display-value', 'children'),
    Input('page-2-dropdown', 'value'))
def display_value(value):
    return f'You have selected {value}'