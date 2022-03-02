from src.models.relevance_old import Relevance
from src.models.bertmodels import BertModels
import pandas as pd
from src.utils import get_project_root


class SubredditAnalysis:

    def __init__(self, subreddit='computerscience', sort_order='hot', set_num_posts=2000, set_num_comments=20000):
        """
        Subreddit Analysis constructor

        3 DataFrames:
            - Subreddit Data
            - Post Data
            - Comment Data

        Running static functions(?):
            Preprocess Posts data
            Preprocess Comments data
            Retrieve Topics for posts and comments
                Add Topics list to respective dataframes
            Get Sentiment Score for posts and comments
            Get Relevance Score for posts->subreddit and comments->posts
                Add scores to respective dataframes

        :param subreddit: name of subreddit for analysis
        :param sort_order: order of submissions retrieved from reddit
        :param set_num_posts: set max number of posts for analysis
        :param set_num_comments: set max number of comments for analysis
        """

        self.subreddit = subreddit
        self.sort_order = sort_order

        bertmodels_obj = BertModels(subreddit=subreddit, sort_type=sort_order)

        def topic_extractor(topics_tag_list, topics):
            topic_mapping = topics_tag_list.set_index('Topic').to_dict()['Name']
            topics_list = list((pd.Series(topics)).map(topic_mapping))
            return topics_list

        # 1. posts preprocessing
        print('********1. Preprocessing Posts for Topic Modeling*********')
        self.posts_df = bertmodels_obj.posts_df[:set_num_posts].copy()
        if self.posts_df.body.nunique() == 0:
            col_for_analysis = 'title'
        else:
            col_for_analysis = 'body'
        
        topic_prep_posts = bertmodels_obj.topic_preprocess(self.posts_df, col_for_analysis)
        print('********DONE: Preprocessing Posts for Topic Modeling*********')

        # 2. topic modeling for posts
        print('********2. Topic Modeling for Posts*********')
        bertmodels_obj.topic_modeling(topic_prep_posts, col_for_analysis+'_word_token', visualize=False)
        topic_prep_posts['topics'] = topic_extractor(bertmodels_obj.model.get_topic_info(), bertmodels_obj.topics)
        self.bert_posts = topic_prep_posts.copy()
        bertmodels_obj.save_topic_model()
        print('********DONE: Topic Modeling for Posts*********')
        
        # 2a. reduce topics to less than 10 for posts 
        print('********2a. Reduce Topics for Posts (<10)*********')
        bertmodels_obj.reduce_topics(nr_topics=10)
        bertmodels_obj.save_topic_model()
        print('********DONE: Reduce Topics for Posts (<10)*********')

        # 3. sentiment analysis for posts
        print('********3. Preprocessing Posts for Sentiment Analysis*********')
        bertmodels_obj.sentiment_preprocess(self.bert_posts, col_for_analysis)
        print('********DONE: Preprocessing Posts for Sentiment Analysis*********')

        print('********3a. Sentiment Analysis of Posts*********')
        bertmodels_obj.sentiment_analysis(self.bert_posts, col_for_analysis)
        print('********DONE: Sentiment Analysis of Posts*********')

        # 4. comments preprocessing
        print('********4. Preprocessing Comments for Topic Modeling*********')
        self.comments_df = bertmodels_obj.comments_df[:set_num_comments].copy()
        topic_prep_comments = bertmodels_obj.topic_preprocess(self.comments_df, 'comment')
        print('********DONE: Preprocessing Comments for Topic Modeling*********')

        # 5. topic modeling for comments
        print('********5. Topic Modeling for Comments*********')
        bertmodels_obj.topic_modeling(topic_prep_comments, 'comment_word_token', visualize=False)
        topic_prep_comments['topics'] = topic_extractor(bertmodels_obj.model.get_topic_info(), bertmodels_obj.topics)
        self.bert_comments = topic_prep_comments.copy()
        bertmodels_obj.save_topic_model(post=False)
        print('********DONE: Topic Modeling for Comments*********')
        
        # 5a. reduce topics to less than 15 for comments
        print('********5a. Reduce Topics for Comments (<15)*********')
        bertmodels_obj.reduce_topics(nr_topics=15)
        bertmodels_obj.save_topic_model()
        print('********DONE: Reduce Topics for Comments (<15)*********')

        # 6. sentiment analysis for comments
        print('********6. Preprocessing Comments for Sentiment Analysis*********')
        bertmodels_obj.sentiment_preprocess(self.bert_comments, 'comment')
        print('********DONE: Preprocessing Comments for Sentiment Analysis*********')

        print('********6a. Sentiment Analysis of Comments*********')
        bertmodels_obj.sentiment_analysis(self.bert_comments, 'comment')
        print('********DONE: Sentiment Analysis of Comments*********')

        # 7. getting relevance score
        print('********7. Relevance Scores*********')
        relevance = Relevance('title-body')
        self.data = self.bert_posts.merge(self.bert_comments, left_on='post_id', right_on='post_id', how='left')
        relevance.generate_relevance(self.data)
        self.res_df = relevance.df
        print('********DONE: Relevance Scores*********')
        
        # 8. Cleaning column names and saving results dataframe to file.
        print('********8. Cleaning and Saving Results to File*********')
        self.clean_res_df()
        self.save_to_file()
        print('********DONE: Cleaning and Saving Results to File*********')

    def get_posts_data(self):
        return self.posts_df

    def get_comments_data(self):
        return self.comments_df

    def get_processed_posts(self):
        return self.bert_posts

    def get_processed_comments(self):
        return self.bert_comments

    def get_result_df(self):
        return self.res_df

    def save_to_file(self, path: str = 'data/results'):
        """
        Saves the output relevance file to a csv. Must run the generate_relevance function beforehand.

        :param path: The folder path to save the file in.
        """
        post_file_name = f'{self.subreddit}_{self.sort_order}_posts.csv'
        comments_file_name = f'{self.subreddit}_{self.sort_order}_comments.csv'
        result_file_name = f'{self.subreddit}_{self.sort_order}_results.csv'
        if self.res_df is not None:
            p = get_project_root().joinpath(path)
            p.mkdir(parents=True, exist_ok=True)
            self.bert_posts.to_csv(p.joinpath(post_file_name), index=False)
            self.bert_comments.to_csv(p.joinpath(comments_file_name), index=False)
            self.res_df.to_csv(p.joinpath(result_file_name), index=False)
        else:
            raise Exception("Missing res_df. Error occured running pipeline.")

    def clean_res_df(self):
        """
        Function used to clean up the columns of the res_df
        """
        # TODO: Finish this function
        # self.res_df['index_x'] = ...
        self.res_df.rename(columns={
                    "index_x": "post_index", 
                    "title": "post_title",
                    "score_x": "post_score",
                    "upvote_ratio": "post_upvote_ratio",
                    " url": "post_url",
                    "body": "post_body",
                    "created": "post_created",
                    'body_word_token': 'post_body_word_token',
                    'body_tag': 'post_body_tag',
                    'body_string_x': 'post_body_string',
                    'topics_x': 'post_topics',
                    'sentiment_x': 'post_sentiment',
                    'index_y': 'comment_index',
                    'up_vote_count': 'comment_up_vote_count',
                    'down_vote_count': 'comment_down_vote_count',
                    'controversiality': 'comment_controversiality',
                    'total_awards_received': 'comment_total_awards_received',
                    'score_y': 'comment_score',
                    'is_locked': 'comment_is_locked',
                    'is_collapsed': 'comment_is_collapsed',
                    'is_submitter': 'comment_is_submitter',
                    'created_utc': 'comment_created',
                    'body_string_y': 'comment_body_string',
                    'topics_y': 'comment_topics',
                    'sentiment_y': 'comment_sentiment',
                    'relevance': 'comment_relevance'
                }, inplace=True)
