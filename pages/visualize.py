import numpy as np
import plotly.express as px

def plot(plot_type, df, x_col, y_col, title='', threshold_col=None, threshold_min=None, threshold_max=None, color=None, size=None):
    accepted_types = ['line', 'scatter', 'bar']
    if plot_type == None or plot_type not in accepted_types:
        raise Exception('plot_type cannot be None or plot_type is not an accepted type "line, scatter, or bar"')
    if threshold_col is not None:
        if threshold_col not in df.columns:
            raise Exception('Threshold column is not in dataframe columns')
        level_max = np.mean(df[threshold_col]) + threshold_max*np.std(df[threshold_col])
        level_min = np.mean(df[threshold_col]) - threshold_min*np.std(df[threshold_col])
        # print('Max ' + threshold_col + ' shown:', level_max)
        # print('Min ' + threshold_col + ' shown:', level_min)
        df = df[(df[threshold_col] > level_min) & (df[threshold_col] < level_max)]
    if plot_type == 'line':
        # print('WARNING: Size variable cannot be used with this plot type.')
        return px.line(df, x=x_col, y=y_col, title=title, color=color)
    if plot_type == 'scatter':
        return px.scatter(df, x=x_col, y=y_col, title=title, color=color, size=size)
    if plot_type == 'bar':
        # print('WARNING: Size variable cannot be used with this plot type.')
        return px.bar(df, x=x_col, y=y_col, title=title, color=color)

def cv_plot(plot_type, df, x_col, y_col, title='', threshold_col=None, threshold_min=None, threshold_max=None, text_col=None, color=None, size=None, hover_name=None, labels=None, width=None, height=None):
    accepted_types = ['line', 'scatter', 'bar']
    if plot_type == None or plot_type not in accepted_types:
        raise Exception('plot_type cannot be None or plot_type is not an accepted type "line, scatter, or bar"')
    if threshold_col is not None:
        if threshold_col not in df.columns:
            raise Exception('Threshold column is not in dataframe columns')
        print('Max ' + threshold_col + ' shown:', threshold_max)
        print('Min ' + threshold_col + ' shown:', threshold_min)
        df = df[(df[threshold_col] > threshold_min) & (df[threshold_col] < threshold_max)]
    if plot_type == 'line':
        print('WARNING: Size variable cannot be used with this plot type.')
        return px.line(df, x=x_col, y=y_col, title=title, color=color, labels=labels, width=width, height=height)
    if plot_type == 'scatter':
        return px.scatter(df, x=x_col, y=y_col, title=title, color=color, text=text_col, size=size, hover_name=hover_name, labels=labels, width=width, height=height)
    if plot_type == 'bar':
        print('WARNING: Size variable cannot be used with this plot type.')
        return px.bar(df, x=x_col, y=y_col, title=title, color=color, labels=labels, width=width, height=height)
# plot('scatter', df_dic[i], x_col='relevance', y_col='score_y', title=i, threshold_col='relevance', threshold_min=0.5, threshold_max=1, color='controversiality')