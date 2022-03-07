import pandas as pd
from pandas.errors import ParserError

AZURE_URL = "https://redditconflict.blob.core.windows.net/redditconflict/results/"
SAS_KEY = "?sp=r&st=2022-03-06T23:29:32Z&se=2023-01-01T07:29:32Z&sv=2020-08-04&sr=c&sig=%2FGHaPmXaEBpc36JBlYfMJLPE8dYr5cFcAsbPpjV16NA%3D"

def get_csv_url(subreddit, sort_order='hot'):
    return AZURE_URL + subreddit + "_" + sort_order + "_results.csv" + SAS_KEY

def get_df(subreddit, sort_order='hot'):
    try:
        df = pd.read_csv(get_csv_url(subreddit, sort_order))
    except ParserError:
        df = pd.read_csv(get_csv_url(subreddit, sort_order), lineterminator='\n')
    return df