import sys
import logging
import asyncio
import asyncpraw
import pandas as pd
from dataclasses import dataclass, field
from typing import Tuple
from pathlib import Path
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


@dataclass(frozen=True)
class SubRedditData:
    name: str
    posts_df: pd.DataFrame = field(repr=False)
    comments_df: pd.DataFrame = field(repr=False)


class AsyncRedditScraper:
    def __init__(self, config: ScraperConfig):
        self.config = config
        self._data: Tuple[SubRedditData] = None

    @asynccontextmanager
    async def _generate_session(self):
        session = asyncpraw.Reddit(client_id=CLIENT_ID,
                                   client_secret=CLIENT_SECRET,
                                   user_agent=CLIENT_SECRET)
        try:
            yield session
        except Exception:
            logger.error(f'Error occured for one subreddit.')
            raise
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

            async for post in scrape_order[self.config.scrape_order](limit=self.config.max_post_count):
                posts_retrieved.append([post.id,
                                        post.title,
                                        post.score,
                                        post.upvote_ratio,
                                        post.subreddit,
                                        post.url,
                                        post.num_comments,
                                        post.selftext,
                                        post.created])
                comments = await post.comments()
                await comments.replace_more(limit=None)
                all_comments = await comments.list()

                # DFS of the comments. (Appears in the same order as reddit)
                comment_queue = comments[:]
                comment_idx = 0
                while comment_queue and comment_idx < self.config.max_comment_count:
                    comment = comment_queue.pop(0)
                    comments_retrieved.append([
                        post.id,
                        comment.body,
                        comment.id,
                        comment.parent_id,
                        comment.created_utc,
                        comment.is_submitter])
                    comment_queue[0:0] = comment.replies
                    comment_idx += 1

                # BFS
                # counter = 0
                # for comment in all_comments:
                #     if counter == self.config.max_comment_count:
                #         break
                #     comments_retrieved.append([post.id, comment.body, comment.parent_id])
                #     counter += 1

        posts_df = pd.DataFrame(posts_retrieved,
                               columns=['post_id', 'title', 'score', 'upvote_ratio', 'subreddit', 'url',
                                        'num_comments', 'body', 'created'])
        comments_df = pd.DataFrame(comments_retrieved,
                                  columns=['post_id', 'comment', 'comment_id', 'parent_id', 'created', 'is_submitter'])
        logger.info(f'done scraping subreddit: {subreddit_name}')
        return SubRedditData(subreddit_name, posts_df, comments_df)

    async def scrape(self):
        logger.info(f'start scraping top {self.config.max_post_count} hottest posts with '
                   f'{self.config.max_comment_count} comments per post from the following subreddits: '
                    f'{", ".join(self.config.subreddit_list)}')
        self._data = await asyncio.gather(*(self._fetch_from_single_subreddit(subreddit_name) for
                                            subreddit_name in self.config.subreddit_list))
        return self

    def save_to_file(self):
        if not self._data:
            pass
        p = get_project_root().joinpath('data/raw')
        # p = Path('.').joinpath('data/raw')
        p.mkdir(parents=True, exist_ok=True)
        for data_obj in self._data:
            data_obj.posts_df.to_csv(p.joinpath(f'{data_obj.name}_posts.csv'), index=False)
            data_obj.comments_df.to_csv(p.joinpath(f'{data_obj.name}_comments.csv'), index=False)
        return self


async def main():
    scraper = AsyncRedditScraper(default_config)
    scraped = await scraper.scrape()
    scraped.save_to_file()


if __name__ == '__main__':
    asyncio.run(main())
