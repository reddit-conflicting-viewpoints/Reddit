# config file for scraper
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ScraperConfig:
    subreddit_list: List[str]  # list of subreddits to scrape
    scrape_order: str  # order to scrape the data from. Can take values: 'hot', 'new', 'top', 'rising'. Notes: 'top' scrapes top of all time.
    max_post_count: int  # number of hot posts to retrieve
    max_comment_per_post: int  # number of top comments associated with each retrieved post
    max_comment_count: int  # total number of comments for the subreddit


default_config = scraper_config = ScraperConfig(
    subreddit_list=['AskReddit'],
    scrape_order='hot',
    max_post_count=1000,
    max_comment_per_post=100,
    max_comment_count=10000)
