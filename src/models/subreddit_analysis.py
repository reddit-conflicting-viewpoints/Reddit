from imports import *

from src.features.preprocess import PreProcess
from src.models.relevance_old import Relevance
from src.models.bertmodels import BertModels

class SubredditAnalysis:
    
    def __init__(self, subreddit='computerscience', sort_order='hot', set_num_posts=500, set_num_comments=500):
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
        
        
        bertmodels_obj = BertModels(subreddit=subreddit, sort_type=sort_order)
        
        def topic_extractor(topics_tag_list, topics):
            topic_mapping = topics_tag_list.set_index('Topic').to_dict()['Name']
            topics_list = list((pd.Series(topics)).map(topic_mapping))
            return topics_list
        
        #1. posts preprocessing
        self.posts_df = bertmodels_obj.posts_df[:set_num_posts].copy() 
        topic_prep_posts = bertmodels_obj.topic_preprocess(self.posts_df, 'body')
        
        #2. topic modeling for posts
        print('********Topic Modeling for Posts*********')
        bertmodels_obj.topic_modeling(topic_prep_posts, 'body_word_token', visualize=False)
        topic_prep_posts['topics'] = topic_extractor(bertmodels_obj.model.get_topic_info(), bertmodels_obj.topics)
        self.bert_posts = topic_prep_posts.copy()
        print('********DONE: Topic Modeling for Posts*********')
        
        #3. sentiment analysis for posts
        print('********Preprocessing for Sentiment Analysis for Posts*********')
        bertmodels_obj.sentiment_preprocess(self.bert_posts, 'body')
        
        print('********DONE: Preprocessing for Sentiment Analysis for Posts*********')
        
        bertmodels_obj.sentiment_analysis(self.bert_posts, 'body')
        
        #4. comments preprocessing
        self.comments_df = bertmodels_obj.comments_df[:set_num_comments].copy()
        topic_prep_comments = bertmodels_obj.topic_preprocess(self.comments_df, 'comment')
        
        #5. topic modeling for comments
        print('********Topic Modeling for Comments*********')
        bertmodels_obj.topic_modeling(topic_prep_comments, 'comment_word_token', visualize=False)
        topic_prep_comments['topics'] = topic_extractor(bertmodels_obj.model.get_topic_info(), bertmodels_obj.topics)
        self.bert_comments = topic_prep_comments.copy()
        print('********DONE: Topic Modeling for Comments*********')
        
        #6. sentiment analysis for comments
        print('********Preprocessing for Sentiment Analysis for Comments*********')
        bertmodels_obj.sentiment_preprocess(self.bert_comments, 'comment')
        print('********DONE: Preprocessing for Sentiment Analysis for Comments*********')
        
        bertmodels_obj.sentiment_analysis(self.bert_comments, 'comment')
        
        #7. getting relevance score
        print('********Relevance Scores*********')
        relevance = Relevance('title-body')
        self.data = self.bert_posts.merge(self.bert_comments, left_on='post_id', right_on='post_id', how='left')
        relevance.generate_relevance(self.data)
        self.res_df = relevance.df
        print('********DONE: Relevance Scores*********')
#         relevance.save_to_file(file_name='relevance_1.csv')

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
