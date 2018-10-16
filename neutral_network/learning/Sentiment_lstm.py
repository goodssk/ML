# -*- coding: utf-8 -*-
import yaml
import sys

from neutral_network.activators import IdentityActivator
import multiprocessing
import numpy as np
from gensim.models import Word2Vec
from gensim.corpora.dictionary import Dictionary
from sklearn.cross_validation import train_test_split

from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
from keras.layers.core import Dense, Dropout, Activation
from keras.models import model_from_yaml
np.random.seed(1337)
import jieba
import pandas as pd

from neutral_network.lstm import LstmLayer

sys.setrecursionlimit(1000000)
# set parameters:
vocab_dim = 100
maxlen = 100
n_iterations = 1  # ideally more..
n_exposures = 10
window_size = 7
batch_size = 32
n_epoch = 4
input_length = 100
cpu_count = multiprocessing.cpu_count()


def loadfile():
    neg = pd.read_excel('data/neg.xls', header=None, index=None)
    pos = pd.read_excel('data/pos.xls', header=None, index=None)

    combined = np.concatenate((pos[0], neg[0]))
    y = np.concatenate((np.ones(len(pos), dtype=int), np.zeros(len(neg), dtype=int)))

    print(y)

    return combined, y


def tokenizer(text):

    text = [jieba.lcut(document.replace('\n', '')) for document in text]

    return text


def create_dictionaries(model=None, combined=None):

    if(combined is not None) and (model is not None):
        gensim_dict = Dictionary()
        gensim_dict.doc2bow(model.wv.vocab.keys(), allow_update=True)

    word2id = {v: k + 1 for k, v in gensim_dict.items()}
    word2vec = {word: model[word] for word in word2id.keys()}

    def parse_dataset(combined):
        ''' Words become integers
        '''
        data=[]
        for sentence in combined:
            new_txt = []
            for word in sentence:
                try:
                    new_txt.append(word2id[word])
                except:
                    new_txt.append(0)
            data.append(new_txt)
        return data

    combined = parse_dataset(combined)
    combined = sequence.pad_sequences(combined, maxlen=maxlen)

    return word2id, word2vec, combined


def get_data(index_dict, word_vectors, combined, y):

    n_symbols = len(index_dict) + 1
    embedding_weights = np.zeros((n_symbols, vocab_dim))
    for word, index in index_dict.items():
        embedding_weights[index, :] = word_vectors[word]
    x_train, x_test, y_train, y_test = train_test_split(combined, y, test_size=0.2)
    return n_symbols, embedding_weights, x_train, y_train, x_test, y_test


def train_lstm(n_symbols, embedding_weights, x_train, y_train, x_test, y_test):

    model = Sequential()
    model.add(Embedding(output_dim=vocab_dim,
                        input_dim=n_symbols,
                        mask_zero=True,
                        weights=[embedding_weights],
                        input_length=input_length))
    model.add(LSTM(output_dim=50, activation='sigmoid', inner_activation='hard_sigmoid'))
    model.add(Dropout(0.5))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    print('Compiling the model')
    model.compile(loss='binary_crossentropy',
                  optimizer='adam', metrics=['accuracy'])
    print('Train')
    model.fit(x_train, y_train, batch_size=batch_size, nb_epoch=n_epoch, verbose=1,
              validation_data=(x_test, y_test))
    print("Evaluate")
    score = model.evaluate(x_test, y_test, batch_size=batch_size)
    yaml_string = model.to_yaml()
    with open('data/lstm.yml', 'w') as outfile:
        outfile.write(yaml.dump(yaml_string))
    model.save_weights('data/lstm.h5')
    print('Test score', score)


def inout_transform(string):
    words = jieba.lcut(string)
    words = np.array(words).reshape(1, -1)
    model = Word2Vec.load('Word2vec_model.pkl')
    _,_,combined = create_dictionaries(model, words)
    return combined

def lstm_predict(string):

    print('loading model......')
    with open('data/lstm.yml', 'r') as f:
        yaml_string = yaml.load(f)

    model = model_from_yaml(yaml_string)
    print('loading weights......')
    model.load_weights('data/lstm.h5')
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    data = inout_transform(string)
    data.reshape(1, -1)
    result = model.predict_classes(data)

    if result[0][0] == 1:
        print(string, 'positive')
    else:
        print(string, 'negative')

def train():
    combined, y =loadfile()
    combined = tokenizer(combined)
    #print(combined)

    model = Word2Vec(size=vocab_dim,
                     min_count=n_exposures,
                     window=window_size,
                     workers=cpu_count,
                     iter=n_iterations)
    model.build_vocab(combined)
    model.train(combined, total_examples=model.corpus_count, epochs=model.iter)
    model.save('Word2vec_model.pkl')

    index_dict, word_vectors, combined = create_dictionaries(model, combined)
    n_symbols, embedding_weights, x_train, y_train, x_test, y_test = get_data(index_dict, word_vectors, combined, y)
    train_lstm(n_symbols, embedding_weights, x_train, y_train, x_test, y_test)


if __name__ == '__main__':

    string1 = '超难喝，还不干净，泡了之后上面漂浮一层污物'
    string2 = '包装漏气差评，又不好喝，有一股怪味差评'
    string3 = '两斤漏气一斤，送的杯杯还碎了。官方不是说好的全程不落地的嘛。'
    string4 = '屏幕较差，拍照也很粗糙。'
    string5 = '质量不错，是正品 ，安装师傅也很好，才要了83元材料费'
    string6 = '第三次买了，依然很好，我老公每天晚上必须要喝茶，这十年来每天喝茶已经成了他的习惯了，在你家买了几次了，以后还会继续在你家买的。'

    lstm_predict(string3)
