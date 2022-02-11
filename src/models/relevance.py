import pandas as pd
import numpy as np
from src.utils import get_project_root
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class Relevance:

    def __init__(self, compared_with: str = 'title'):
        """
        Relevance object constructor

        :param compared_with: the item to compare comments with. Can take values: 'title', 'body', 'title-body'
        """
        self.compared_with = compared_with
        self.model = SentenceTransformer('bert-base-nli-mean-tokens')
        self.df = None

    def generate_relevance(self, df):
        """

        :param df:
        :return:
        """
        similarities = np.array([])
        for post_id in df['post_id'].unique():
            temp = df[df['post_id'] == post_id]
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

            sentence_embeddings = model.encode(comments)
            similarity = cosine_similarity([sentence_embeddings[-1]], sentence_embeddings[:-1])
            similarities = np.append(similarities, similarity.flatten())
            df['relevance'] = similarities
            self.df = df
            return df

    def save_to_file(self, path: str = 'data/results', file_name: str = 'relevance.csv'):
        if not self.df:
            raise Exception("Call generate_relevance first before save_to_file")
        p = get_project_root().joinpath(path)
        p.mkdir(parents=True, exist_ok=True)
        self.df.to_csv(p.joinpath(file_name), index=False)
