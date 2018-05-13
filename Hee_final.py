import pandas as pd
import numpy as np
from glob import glob
import pickle
import os
import sys
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.utils import resample
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split, GridSearchCV
from keras.wrappers.scikit_learn import KerasClassifier
from keras.layers.core import Activation
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, RNN
from keras.layers.embeddings import Embedding
from keras.models import load_model
import warnings
warnings.simplefilter('ignore', FutureWarning)
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'



def get_tokenizer(vocab_size, train_text=None):
    DATA_ROOT = 'Data'
    vocab_size = 200
    MAX_REVIEW_LEN = 250
    tokenizer_file_name = os.path.join(DATA_ROOT, 'tokenizers', 'tokenizer_' + str(vocab_size) + '.pkl')
    time_start = datetime.now()
    if os.path.isfile(tokenizer_file_name):
        print('Loading tokenizer...')
        with open(tokenizer_file_name, 'rb') as file:
            tokenizer = pickle.load(file)
    else:
        print('Training tokenizer...')
        tokenizer = Tokenizer(num_words=vocab_size)
        tokenizer.fit_on_texts(train_text)
        
        with open(tokenizer_file_name, 'wb') as file:
            pickle.dump(tokenizer, file)
        
    print('Got tokenizer for vocab size: ' + str(vocab_size) + ' in ' + str(datetime.now() - time_start))
    return tokenizer

def word_to_predict(sentence):
    DATA_ROOT = 'Data'
    vocab_size = 200
    MAX_REVIEW_LEN = 250
    model = load_model(os.path.join(DATA_ROOT, 'models', 'yelp_trained.hd5'))
    list_review = []
    tokenizer = get_tokenizer(vocab_size)
    tokenizer.fit_on_texts(list_review)
    list_review.append(sentence)
    list_review = tokenizer.texts_to_sequences(list_review)
    list_review = pad_sequences(list_review, maxlen=MAX_REVIEW_LEN)
    x = model.predict(list_review)
    a = pd.DataFrame(x)
    a.columns = [1,2,3,4,5]

    score = a.idxmax(axis=1)
    score = score[0]
    # z = dict = {}
    # for i in range(5):
    #     dict[str(i+1)] = round(((a.loc[0: ,i+1][0])*100),1)
    return score

