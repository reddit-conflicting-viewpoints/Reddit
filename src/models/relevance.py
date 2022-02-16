import pandas as pd
import numpy as np
from src.utils import get_project_root
from src.features.preprocess import PreProcess
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class Relevance:

    def __init__(self, compared_with: str = 'title'):
        """
        Relevance object constructor

        :param compared_with: the item to compare comments with. Can take values: 'title', 'body', 'title-body',
            'parent', 'title-parent', 'body-parent', 'title-body-parent'
        """
        self.compared_with = compared_with
        self.model = SentenceTransformer('bert-base-nli-mean-tokens')
        self.df = None

    def generate_relevance(self, df):
        """
        Generates a relevance score for each comment compared to either title, body, or both.
        Will automatically call generate_relevance with parents if compared with a parent comment.

        :param df: The dataframe to run relevance on. Make sure the dataframe has posts and comments merged
        :return: The dataframe with relevance score column
        """
        
        if 'title' not in df.columns:
            raise Exception('Missing title column. Merge posts and columns')
        
        if 'comment' not in df.columns:
            raise Exception('Missing comment column. Merge posts and columns')
        
        if self.compared_with not in ['title', 'body', 'title-body']:
            return self.generate_relevance_with_parents(df)

        # First fill na for empty titles, bodies, and comments
        title_body_comment = pd.DataFrame(df[['post_id', 'title', 'body', 'comment']])
        pp = PreProcess()
        pp.fill_na(title_body_comment, 'title')
        pp.fill_na(title_body_comment, 'body')
        # pp.fill_na(title_body_comment, 'comment')

        similarities = np.array([])
        for post_id in title_body_comment['post_id'].unique():
            temp = title_body_comment[title_body_comment['post_id'] == post_id]
            if pd.isnull(temp.iloc[0]['comment']):
                similarities = np.append(similarities, 0)
                continue
            title = temp.iloc[0]['title']
            body = temp.iloc[0]['body']            

            compared_dict = {
                'title': title,
                'body': body,
                'title-body': title + ' ' + body
            }

            topic = compared_dict[self.compared_with]

            comments = temp['comment'].to_list()
            comments.append(topic)

            sentence_embeddings = self.model.encode(comments)
            similarity = cosine_similarity([sentence_embeddings[-1]], sentence_embeddings[:-1])
            similarities = np.append(similarities, similarity.flatten())
        df['relevance'] = similarities
        self.df = df
        return df
    
    def generate_relevance_with_parents(self, df):
        """
        Generates a relevance score for each comment compared with a parent comment.
        This will also generate a parent_comment column.

        :param df: The dataframe to run relevance on. Make sure the dataframe has posts and comments merged
        :return: The dataframe with relevance score column
        """
        
        # Generate parent column if it isn't in the dataframe
        if 'parent_comment' not in df.columns:
            PreProcess.get_parent_comment(df)
        
        # First fill na for empty titles, bodies, and comments
        title_body_comment = pd.DataFrame(df[['post_id', 'title', 'body', 'comment', 'parent_comment']])
        pp = PreProcess()
        pp.fill_na(title_body_comment, 'title')
        pp.fill_na(title_body_comment, 'body')
        pp.fill_na(title_body_comment, 'parent_comment')
        
        similarities = np.array([])
        for post_id in title_body_comment['post_id'].unique():
            temp = title_body_comment[title_body_comment['post_id'] == post_id]
            
            if pd.isnull(temp.iloc[0]['comment']):
                similarities = np.append(similarities, 0)
                continue
            
            title = temp.iloc[0]['title']
            body = temp.iloc[0]['body']
            
            for i in range(len(temp)):
                parent = temp.iloc[i]['parent_comment']

                compared_dict = {
                    'parent': parent,
                    'title-parent': title + ' ' + parent,
                    'body-parent': body + ' ' + parent,
                    'title-body-parent': title + ' ' + body + ' ' + parent
                }

                topic = compared_dict[self.compared_with]

                comment = temp.iloc[i]['comment']
                comments = [comment, topic]

                sentence_embeddings = self.model.encode(comments)
                similarity = cosine_similarity([sentence_embeddings[-1]], sentence_embeddings[:-1])
                similarities = np.append(similarities, similarity.flatten())
        df['relevance'] = similarities
        self.df = df
        return df

    def save_to_file(self, path: str = 'data/results', file_name: str = 'relevance.csv'):
        """
        Saves the output relevance file to a csv. Must run the generate_relevance function beforehand.

        :param path: The folder path to save the file in.
        :param file_name: The filename to save the file with. Please include '.csv' at the end.
        """
        if self.df is not None:
            p = get_project_root().joinpath(path)
            p.mkdir(parents=True, exist_ok=True)
            self.df.to_csv(p.joinpath(file_name), index=False)
        else:
            raise Exception("Missing relevance. Call generate_relevance first before save_to_file")
