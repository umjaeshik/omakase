import pandas as pd
from sklearn.metrics.pairwise import  linear_kernel
from scipy.io import mmread
import pickle
from konlpy.tag import Okt
from gensim.models import Word2Vec
import numpy as np


def getRecommendation(consine_sim):

    simScore = list(enumerate(consine_sim[-1])) #인덱스 유지위해
    simScore = sorted(simScore, key=lambda x:x[1], reverse=True)
    simScore = simScore
    resIdx = [i[0] for i in simScore]
    resList = df_reviews.iloc[resIdx,0]
    return resList


df_reviews = pd.read_csv('./res_naver_sum.csv')
Tfidf_matrix = mmread('./models/Tfidf_movie_review.mtx').tocsr()
with open('./models/tfidf.picle','rb') as f:
    Tfidf = pickle.load(f)

embedding_model = Word2Vec.load('./models/word2vec_res_review.model')
keyword = ['돈까스','정식','고급','친절하다']
list_mul = [10,5,10,10]
recommendations = []
simLists=[]

sentence = []
for idx,key_list in enumerate(keyword):
    sim_word = embedding_model.wv.most_similar(key_list, topn=10)
    words = [key_list]
    for word, _ in sim_word:
        words.append(word)

    count = list_mul[idx]
    for word in words:
        sentence = sentence + [word] * count
        count -=1

print(sentence)
sentence = ' '.join(sentence)

sentence_vec = Tfidf.transform([sentence])
cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix)
# simLists.append(cosine_sim)
#
# sim_sum = np.array([[0.0] * 1445])
# for idx, simscore in enumerate(simLists):
#     sim_sum += sim_sum + simscore * list_mul[idx]

recommendation = getRecommendation(cosine_sim)




results = df_reviews.iloc[recommendation.index]
count=0
#print(len(recommendation.index))
for i in range(0,len(recommendation.index)):
    if len(results.iloc[i,1])>10000 :
        #if results.iloc[i,2]=='고양시':
        if count < 10:
            print(results.iloc[i,0])
            count +=1
        else:
            break






























