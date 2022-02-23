import sys
import time
import logging
import asyncio
import asyncpraw
import pandas as pd
from dataclasses import dataclass, field
from typing import List
from src.utils import get_project_root
from contextlib import asynccontextmanager
from config import ScraperConfig, default_config

# reddit API credentials
CLIENT_ID = 'xG2uYfBViT_APANuInp5Yw'
CLIENT_SECRET = 'ewGDf8V8LFdgCuH0VxmYUehgKq18ug'
USER_AGENT = 'uw_msds_2021fall'

# logger setup
handler = logging.StreamHandler(sys.stdout)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


class TerminalError(Exception):
    pass


def async_retry(times=3, delay=0):
    """
    async retry decorator
    """
    def func_wrapper(fn):
        async def wrapper(*args, **kwargs):
            for _ in range(times):
                try:
                    return await fn(*args, **kwargs)
                except Exception:
                    time.sleep(delay)
            raise TerminalError()
        return wrapper
    return func_wrapper


@dataclass(frozen=True)
class SubRedditData:
    name: str
    posts_df: pd.DataFrame = field(repr=False)
    comments_df: pd.DataFrame = field(repr=False)


class AsyncRedditScraper:
    def __init__(self, config: ScraperConfig):
        self.config = config
        self._data: List[SubRedditData] = []

    @asynccontextmanager
    async def _generate_session(self):
        session =  asyncpraw.Reddit(client_id=CLIENT_ID,
                                    client_secret=CLIENT_SECRET,
                                    user_agent=CLIENT_SECRET)
        try:
            yield session
        except Exception:
            pass
        finally:
            await session.close()

    async def _fetch_from_single_subreddit(self, subreddit_name: str):
        logger.info(f'start scraping subreddit: {subreddit_name}')
        async with self._generate_session() as session:
            posts_retrieved = []
            comments_retrieved = []
            subreddit = await session.subreddit(subreddit_name)

            scrape_order = {
                'hot': subreddit.hot,
                'new': subreddit.new,
                'top': subreddit.top,
                'rising': subreddit.rising
            }

            posts = [post async for post in
                     scrape_order[self.config.scrape_order](limit=self.config.max_post_count)
                     if not post.stickied]

            for post in posts:
                posts_retrieved.append([post.id,
                                        post.title,
                                        post.link_flair_text,
                                        post.score,
                                        post.upvote_ratio,
                                        post.subreddit,
                                        post.url,
                                        post.num_comments,
                                        post.selftext,
                                        post.created])

            
            comment_forests = await asyncio.gather(*[post.comments() for post in posts])
            await asyncio.gather(*[comment_forest.replace_more(0) for comment_forest in comment_forests])
            # in place
            for comment_forest in comment_forests:
                top_comments = comment_forest.list()[:self.config.max_comment_count][::-1]
                while top_comments:
                    comment = top_comments.pop()
                    if comment.stickied:
                        continue
                    comments_retrieved.append([comment.submission.id,
                                               comment.id,
                                               comment.parent_id,
                                               comment.body,
                                               comment.ups,
                                               comment.downs,
                                               comment.controversiality,
                                               comment.total_awards_received,
                                               comment.score,
                                               comment.locked,
                                               comment.collapsed,
                                               comment.is_submitter,
                                               comment.created_utc])
                    
        posts_df = pd.DataFrame(posts_retrieved,
                                columns=['post_id', 'title', 'flair', 'score', 'upvote_ratio', 'subreddit', ' url',
                                         'num_comments', 'body', 'created'])
        comments_df = pd.DataFrame(comments_retrieved,
                                   columns=['post_id', 'comment_id', 'parent_id', 'comment',
                                            'up_vote_count', 'down_vote_count', 'controversiality',
                                            'total_awards_received', 'score', 'is_locked', 'is_collapsed',
                                            'is_submitter', 'created_utc'])
        return SubRedditData(subreddit_name, posts_df, comments_df)

    @async_retry(times=3, delay=10)
    async def scrape(self):

        scrape_order_str = {
            'hot': 'hottest',
            'new': 'newest',
            'top': 'top',
            'rising': 'rising'
        }

        logger.info(f'start scraping top {self.config.max_post_count} {scrape_order_str[self.config.scrape_order]} posts with '
                    f'{self.config.max_comment_count} comments per post from the following subreddits: '
                    f'{", ".join(self.config.subreddit_list)}')
        try:
            self._data = await asyncio.gather(*(self._fetch_from_single_subreddit(subreddit_name) for
                                              subreddit_name in self.config.subreddit_list))
        except Exception:
            logger.error("failed to scrape, retrying...")
            raise
        return self

    def save_to_file(self):
        if not self._data:
            pass
        p = get_project_root().joinpath('data/raw')
        p.mkdir(parents=True, exist_ok=True)
        for data_obj in self._data:
            data_obj.posts_df.to_csv(p.joinpath(f'{data_obj.name}_{self.config.scrape_order}_posts.csv'), index=False)
            data_obj.comments_df.to_csv(p.joinpath(f'{data_obj.name}_{self.config.scrape_order}_comments.csv'), index=False)
        return self


async def main():
    scraper = AsyncRedditScraper(default_config)
    scraped = await scraper.scrape()
    logger.info("All Success!")
    for data_obj in scraped._data:
        logger.info(f"Subreddit {data_obj.name} retrieved "
                    f"{data_obj.posts_df.shape[0]} posts and "
                    f"{data_obj.comments_df.shape[0]} comments.")
    scraped.save_to_file()


if __name__ == '__main__':
    tik = time.perf_counter()
    asyncio.run(main())
    tok = time.perf_counter()
    logger.info(f"total run time {tok-tik}")
