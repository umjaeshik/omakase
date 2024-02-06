from PIL import Image
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pandas as pd
from PyQt5.QtGui import QPixmap
from scipy.io import mmwrite, mmread
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from PyQt5.QtCore import QStringListModel
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import linear_kernel

import pickle


form_window = uic.loadUiType('./recommendation.ui')[0]
class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Tfidf_matrix = mmread('./models/Tfidf_movie_review.mtx').tocsr()
        with open('./models/tfidf.picle','rb') as f:
            self.Tfidf = pickle.load(f)
        self.embedding_model = Word2Vec.load('./models/word2vec_movie_review.model')
        self.df_reviews = pd.read_csv('./reviews_one_kinonights.csv')
        self.titles = list(self.df_reviews['titles'])
        self.titles.sort()
        for title in self.df_reviews['titles']:
            self.comboBox.addItem(title)
        self.comboBox.currentIndexChanged.connect(self.combobox_slot)
        self.pushButton.clicked.connect(self.btn_slot)

        model=QStringListModel()
        model.setStringList(self.titles)
        completer = QCompleter()
        completer.setModel(model)
        self.input_keyword.setCompleter(completer)

    def btn_slot(self):
        keyword = self.input_keyword.text()
        print(keyword)
        if keyword in self.titles:
            recommendation = self.recommendation_by_movie_title(keyword)
        else:
            recommendation = self.recommendation_by_keyboard(keyword)



        recommendation = '\n'.join(list(recommendation))
        self.label_result.setText(recommendation)



    def recommendation_by_keyboard(self, keyword):
        sim_word = self.embedding_model.wv.most_similar(keyword, topn=10)
        words = [keyword]
        for word, _ in sim_word:
            words.append(word)
        sentence = []
        count = 10
        for word in words:
            sentence = sentence + [word] * count
            count -= 1
        sentence = ' '.join(sentence)
        print(sentence)
        sentence_vec = self.Tfidf.transform([sentence])
        cosine_sim = linear_kernel(sentence_vec, self.Tfidf_matrix)
        recommendation = self.getRecommendation(cosine_sim)
        return recommendation



    def getRecommendation(self, consine_sim):
        print('들어옴')
        simScore = list(enumerate(consine_sim[-1]))  # 인덱스 유지위해
        simScore = sorted(simScore, key=lambda x: x[1], reverse=True)
        simScore = simScore[:11]
        movieIdx = [i[0] for i in simScore]
        recmovieList = self.df_reviews.iloc[movieIdx, 0]
        return recmovieList[1:11]

    def recommendation_by_movie_title(self, title):
        print('debug4')
        movie_idx = self.df_reviews[self.df_reviews['titles'] == title].index[0]
        print('debug6')
        print(title)
        print(movie_idx)
        cosine_sim = linear_kernel(self.Tfidf_matrix[movie_idx], self.Tfidf_matrix)
        print('debug5')
        recommendation = self.getRecommendation(cosine_sim)

        return recommendation


    def combobox_slot(self):
        print('들어옴2')
        title = self.comboBox.currentText()
        recommendation =  self.recommendation_by_movie_title(title)
        self.label_result.setText(recommendation)

if __name__ =='__main__':

    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())
