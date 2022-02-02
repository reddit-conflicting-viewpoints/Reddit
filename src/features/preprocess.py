import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer, PorterStemmer
import re


nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')


class PreProcess:
    """
    Preprocessing pipeline class

    Notes:
        Some functions perform processing on the column itself.
        Some functions perform processing on column_word_token.

        Please read documentation above to know where the task is performed.

        If writing your own manual function, please call functions that process
        on the column itself first, then functions that perform on tokenized
        columns. If needed, you can convert tokens back into a string by
        calling the function: token_to_str.

    Functions:
        fill_na: performs on the column itself
        tokenize: generates a column_word_token column
        clean_special_characters: performs on column_word_token
        filter_stopwords: performs on column_word_token
        remove_urls: performs on the column itself
        expand_contractions: performs on the column itself
        remove_hashtags: performs on the column itself
        remove_escape_chars: performs on the column itself
        stem: performs on column_word_token
        lemm: performs on column_word_token
        token_to_str: converts the column_word_token back into a string in a
            new column
        preprocess: an all in one function
    """

    def __init__(self):
        pass

    def fill_na(self, df, column):
        """
        Fill na (empty values) with ''
        Column: Raw strings
        Performs the task in-place (in the same column)

        :param df: Dataframe to manipulate
        :param column: The column to preprocess
        """
        df[column] = df[column].fillna('')
        return df

    def tokenize(self, df, column):
        """
        Tokenize the content
        Column: Raw strings
        Performs the task in the column: "column + '_word_token'"

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
        return df

    def clean_special_characters(self, df, column, remove_digits=False):
        """
        Filter out stopwords and punctuation
        NOTE: MUST BE CALLED AFTER tokenize
        Column: List of word tokens
        Performs the task in the column: "column + '_word_token'"

        :param df: Dataframe to manipulate
        :param column: The column to preprocess
        :param remove_digits: Option to remove digits as special characters
        """

        def get_clean_sentences(sentences, remove_digits):
            """
            Helper function

            Cleaning sentences by removing special characters and optionally
            digits
            """
            clean_sentences = []
            for sent in sentences:
                if not remove_digits:
                    pattern = r'[^a-zA-Z0-9\s]'
                else:
                    pattern = r'[^a-zA-Z\s]'
                clean_text = re.sub(pattern, '', sent)
                clean_text = clean_text.lower()  # Converting to lower case
                if clean_text != '':
                	clean_sentences.append(clean_text)
            return clean_sentences

        df[column + '_word_token'] = df[column + '_word_token'].apply(
            lambda s: get_clean_sentences(s, remove_digits))
        return df

    def filter_stopwords(self, df, column):
        """
        Filter out stopwords and punctuation
        NOTE: MUST BE CALLED AFTER tokenize
        Column: List of word tokens
        Performs the task in the column: "column + '_word_token'"

        :param df: Dataframe to manipulate
        :param column: The column to preprocess
        """
        stop_words = set(stopwords.words('english'))

        def filter_stopwords(words):
            """
            Removing stopwords from given words
            """
            filtered_words = [w for w in words if w not in stop_words]
            # print('\nFiltered words:', filtered_words)
            return filtered_words

        df[column + '_word_token'] = df[column + '_word_token'].apply(
            filter_stopwords)
        df[column + '_word_token'] = df[column + '_word_token'].apply(
            lambda s: list(filter(None, s)))
        return df

    def remove_urls(self, df, column):
        """
        Function used to remove urls from strings
        Column: Raw strings
        Performs the task in-place (in the same column)

        :param df: Dataframe to manipulate
        :param column: The column to preprocess
        """

        def filter_urls(s):
            """
            Helper function used to replace URLs with empty string
            """
            if isinstance(s, str):
                return re.sub(
                    r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', s,
                    flags=re.MULTILINE)
            else:
                return s

        df[column] = df[column].apply(filter_urls)
        return df

        # TODO: slang-lookup

    def expand_contractions(self, df, column):
        """
        Function used to expand contractions of text
        Column: Raw strings
        Performs the task in-place (in the same column)

        :param df: Dataframe to manipulate
        :param column: The column to preprocess
        """

        def expand_contractions_helper(s):
            """
            Helper function used to replace contractions with full forms
            """

            # dictionary consisting of the contraction and the actual value
            Apos_dict = {"'s": " is", "n't": " not", "'m": " am",
                         "'ll": " will", "'d": " would", "'ve": " have",
                         "'re": " are"}
            if isinstance(s, str):
                # replace the contractions
                for key, value in Apos_dict.items():
                    if key in s:
                        s = s.replace(key, value)
            return s

        df[column] = df[column].apply(expand_contractions_helper)
        return df

    def remove_hashtags(self, df, column):
        """
        Function used to remove hashtags from text
        Column: Raw strings
        Performs the task in-place (in the same column)

        :param df: Dataframe to manipulate
        :param column: The column to preprocess
        """

        def remove_hashtags_helper(s):
            """
            Helper function used to replace hashtags with empty string
            """
            if isinstance(s, str):
                return re.sub(r'#', '', s)
            else:
                return s

        df[column] = df[column].apply(remove_hashtags_helper)
        return df

    def remove_escape_chars(self, df, column):
        """
        Function used to remove escape characters from text
        Column: Raw strings
        Performs the task in-place (in the same column)

        :param df: Dataframe to manipulate
        :param column: The column to preprocess
        """

        def remove_escape_chars_helper(s):
            """
            Helper function used to replace escape character: \n, with empty
            string
            """
            if isinstance(s, str):
                return re.sub(r'\n', '', s)
            else:
                return s

        df[column] = df[column].apply(remove_escape_chars_helper)
        return df

    def stem(self, df, column):
        """
        Stem the tokenized words
        NOTE: MUST BE CALLED AFTER tokenize
        Column: List of word tokens
        Performs the task in the column: "column + '_word_token'"

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

        df[column + '_word_token'] = df[column + '_word_token'].apply(
            get_stems)
        return df

    def lemm(self, df, column):
        """
        Lemm the tokenized words. This will also POS TAG the tokenized words.
        NOTE: MUST BE CALLED AFTER tokenize
        Column: List of word tokens
        Performs the task in the column: "column + '_word_token'"

        :param df: Dataframe to manipulate
        :param column: The column to preprocess
        """

        def get_pos_tags(words):
            """
            Helper function
            Get the part of speech (POS) tags for the words
            """
            tags = []
            for word in words:
                tags.append(nltk.pos_tag([word]))
            return tags

        def get_lemma(word_tags):
            """
            Helper function
            Reduce the words to their base word (lemma) by using a lexicon
            """
            wordnet_lemmatizer = WordNetLemmatizer()
            lemma = []
            for element in word_tags:
                word = element[0][0]
                pos = element[0][1]
                tag = nltk.pos_tag([word])[0][1][0].upper()
                tag_dict = {"J": wordnet.ADJ,
                            # Mapping NLTK POS tags to WordNet POS tags
                            "N": wordnet.NOUN,
                            "V": wordnet.VERB,
                            "R": wordnet.ADV}

                wordnet_pos = tag_dict.get(tag, wordnet.NOUN)
                lemma.append(wordnet_lemmatizer.lemmatize(word, wordnet_pos))
            return lemma

        df[column + '_tag'] = df[column + '_word_token'].apply(get_pos_tags)
        df[column + '_word_token'] = df[column + '_tag'].apply(get_lemma)
        return df

    def token_to_str(self, df, column):
        """
        Function used to convert token back to string format

        :param df: Dataframe to manipulate
        :param column: The column to preprocess
        """

        df[column + '_untokenized'] = df[column + '_word_token'].apply(
            lambda s: ' '.join(s))
        return df

    def preprocess(self, df, column, lemm=False):
        """
        All in one function that calls the other preprocessing functions to
        quickly generate preprocessed text.

        Preprocesses the column by:
        1. fill_na for empty strings
        2. remove URLs
        3. expand contractions
        4. remove hashtags
        5. remove escape chars '\n'
        ### All of the above are performed in-place (the same column)
        ### Below generates a new column
        6. tokenize the text into list of words
        7. filter out special characters that are not alphabetical or numerical
        8. filter stopwords
        9. stemming/lemmatization

        :param df: Dataframe to manipulate
        :param column: The column to preprocess
        :param lemm: boolean to compute lemmatization. False by default.
        """
        self.fill_na(df, column)
        self.remove_urls(df, column)
        self.expand_contractions(df, column)
        self.remove_hashtags(df, column)
        self.remove_escape_chars(df, column)
        self.tokenize(df, column)
        self.clean_special_characters(df, column)
        self.filter_stopwords(df, column)
        if lemm:
            self.lemm(df, column)
        else:
            self.stem(df, column)
        return df
