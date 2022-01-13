import pandas as pd
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re


class PreProcess:
    """
    Preprocessing pipeline class
    """

    # def __init__(self, file_path=None, df=None):
    #     """
    #     Preprocessing constructor
    #
    #     :param file_path: String of the csv filepath
    #     :param is_post: Boolean of whether the data is the post or comments
    #     """
    #     if file_path:
    #         self.df = pd.read_csv(file_path)
    #     elif df:
    #         self.df = df
    #     else:
    #         raise Exception("Need a filepath or df")


    @staticmethod
    def fill_na(df, column):
        """
        Fill na (empty values) with ''

        :param df: Dataframe to manipulate
        :param column: The column to preprocess
        """
        df[column] = df[column].fillna('')

    @staticmethod
    def tokenize(df, column):
        """
        Tokenize the content

        :param df: Dataframe to manipulate
        :param column: The column to preprocess
        """
        def word_tokenize_helper(s):
            if len(s) == 0:
                return word_tokenize('')
            else:
                return word_tokenize(s[0])

        df[column + '_word_token'] = df[column].apply(sent_tokenize).apply(
            lambda s: word_tokenize_helper(s))

    @staticmethod
    def filter_stopwords(df, column):
        """
        Filter out stopwords and punctuation

        :param df: Dataframe to manipulate
        :param column: The column to preprocess
        """
        stop_words = set(stopwords.words('english'))

        def get_clean_sentences(sentences, remove_digits=False):
            """
            Cleaning sentences by removing special characters and optionally
            digits
            """
            clean_sentences = []
            for sent in sentences:
                pattern = r'[^a-zA-Z0-9\s]' if not remove_digits else r'[^a-zA-Z\s]'
                clean_text = re.sub(pattern, '', sent)
                clean_text = clean_text.lower()  # Converting to lower case
                clean_sentences.append(clean_text)
            # print('\nClean sentences:', clean_sentences)
            return clean_sentences

        def filter_stopwords(words):
            """
            Removing stopwords from given words
            """
            filtered_words = [w for w in words if w not in stop_words]
            # print('\nFiltered words:', filtered_words)
            return filtered_words

        df[column + '_filtered'] = df[column + '_word_token'].apply(
            get_clean_sentences)
        df[column + '_filtered'] = df[column + '_filtered'].apply(
            filter_stopwords)
        df[column + '_filtered'] = df[column + '_filtered'].apply(
            lambda s: list(filter(None, s)))

    @staticmethod
    def stem(df, column):
        """
        Stem the tokenized words

        :param df: Dataframe to manipulate
        :param column: The column to preprocess
        """
        def get_stems(words):
            """
            Reduce the words to their base word (stem) by cutting off the ends
            """
            ps = PorterStemmer()
            stems = []
            for word in words:
                stems.append(ps.stem(word))
            # print(stems)
            return stems

        df[column + '_stem'] = df[column + '_filtered'].apply(get_stems)

    @staticmethod
    def preprocess(df, column):
        """
        Preprocess the column by fill_na, tokenize, filtering, and stemming

        :param df: Dataframe to manipulate
        :param column: The column to preprocess
        """
        PreProcess.fill_na(df, column)
        PreProcess.tokenize(df, column)
        PreProcess.filter_stopwords(df, column)
        PreProcess.stem(df, column)
        return df
