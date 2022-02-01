import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer, PorterStemmer
import re

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
# nltk.download('omw-1.4')


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
    def remove_urls(df, column):
        """
        Function used to remove urls from strings
        :param df: Dataframe to manipulate
        :param column: The column to preprocess
        """
        def filter_urls(s):
            """
            Helpfer function used to replace URLs with empty string
            """
            if isinstance(s, str):
                return re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', s, flags=re.MULTILINE)
            else:
                return s

        df[column] = df[column].apply(filter_urls)

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
    def lemm(df, column):
        """
        Lemm the tokenized words. This will also POS TAG the tokenized words.
        :param df: Dataframe to manipulate
        :param column: The column to preprocess
        """
        def get_pos_tags(words):
            '''
            Helper function
            Get the part of speech (POS) tags for the words
            '''
            tags=[]
            for word in words:
                tags.append(nltk.pos_tag([word]))
            return tags

        def get_lemma(word_tags):
            '''
            Helper function
            Reduce the words to their base word (lemma) by using a lexicon
            '''
            wordnet_lemmatizer = WordNetLemmatizer()
            lemma = []
            for element in word_tags:
                word = element[0][0]
                pos = element[0][1]
                tag = nltk.pos_tag([word])[0][1][0].upper()
                tag_dict = {"J": wordnet.ADJ, # Mapping NLTK POS tags to WordNet POS tags
                        "N": wordnet.NOUN,
                        "V": wordnet.VERB,
                        "R": wordnet.ADV}

                wordnet_pos = tag_dict.get(tag, wordnet.NOUN)
                lemma.append(wordnet_lemmatizer.lemmatize(word, wordnet_pos))
            return(lemma)

        df[column + '_tag'] = df[column + '_filtered'].apply(get_pos_tags)
        df[column + '_lemm'] = df[column + '_tag'].apply(get_lemma)


    @staticmethod
    def preprocess(df, column, lemm=False):
        """
        Preprocess the column by fill_na, tokenize, filtering, and stemming
        :param df: Dataframe to manipulate
        :param column: The column to preprocess
        :param lemm: boolean to compute lemmatization. False by default.
        """
        PreProcess.fill_na(df, column)
        PreProcess.remove_urls(df, column)
        PreProcess.tokenize(df, column)
        PreProcess.filter_stopwords(df, column)
        PreProcess.stem(df, column)
        if lemm:
            PreProcess.lemm(df, column)
        return df