import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import itertools
from wordcloud import WordCloud, STOPWORDS

from src.features.preprocess import PreProcess
from src.features.preprocess_old import PreProcess

from pprint import pprint
from bertopic import BERTopic

import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer, PorterStemmer
import re

from gensim import corpora, models
import gensim