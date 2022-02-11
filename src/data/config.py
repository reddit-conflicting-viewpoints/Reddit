# config file for scraper
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ScraperConfig:
    subreddit_list: List[str]  # list of subreddits to scrape
    scrape_order: str  # order to scrape the data from. Can take values: 'hot', 'new', 'top', 'rising'. Notes: 'top' scrapes top of all time.
    max_post_count: int  # number of hot posts to retrieve
    max_comment_count: int  # number of top comments associated with each retrieved post


default_config = scraper_config = ScraperConfig(
    subreddit_list=['computerscience', 'music', 'loseit', 'AmItheAsshole', 'NoStupidQuestions', 'antiwork'],
    scrape_order='hot',
    max_post_count=100000000000,
    max_comment_count=90000000000000000)
