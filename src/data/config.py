# config file for scraper
from dataclasses import dataclass
from typing import List
import numpy as np


@dataclass(frozen=True)
class ScraperConfig:
    subreddit_list: List[str]  # list of subreddits to scrape
    scrape_order: str  # order to scrape the data from. Can take values: 'hot', 'new', 'top', 'rising'. Notes: 'top' scrapes top of all time.
    tree: bool # scrape comments of comments if true. scrape top level comments only if false
    max_post_count: int  # number of hot posts to retrieve
    max_comment_count: int  # number of top comments associated with each retrieved post


default_config = scraper_config = ScraperConfig(
    subreddit_list=['lotr'],
    scrape_order='new',
    tree=True,
    max_post_count=10,
    max_comment_count=10)
