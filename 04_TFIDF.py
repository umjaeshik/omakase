import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.io import mmwrite, mmread
import pickle

df_reviews = pd.read_csv('./res_naver_sum.csv')
df_reviews.info()

Tfidf = TfidfVectorizer(sublinear_tf=True)
Tfidf_matrix = Tfidf.fit_transform(df_reviews['reviews'])
print(Tfidf_matrix.shape)

with open('./models/tfidf.picle','wb')as f:
    pickle.dump(Tfidf,f)
mmwrite('./models/Tfidf_res_review.mtx',Tfidf_matrix)

