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

    resIdx = [i[0] for i in simScore]
    resList = df_reviews.iloc[resIdx,0]
    return resList


df_reviews = pd.read_csv('./res_naver_sum.csv')
Tfidf_matrix = mmread('./models/Tfidf_movie_review.mtx').tocsr()
with open('./models/tfidf.picle','rb') as f:
    Tfidf = pickle.load(f)

embedding_model = Word2Vec.load('./models/word2vec_res_review.model')
keyword = ['콩나물','국밥']
list_mul = [10,7,1]
recommendations = []
simLists=[]


for idx,key_list in enumerate(keyword):
    sim_word = embedding_model.wv.most_similar(key_list, topn=10)
    words = [key_list]
    for word, _ in sim_word:
        words.append(word)

    sentence=[]
    count = list_mul[idx]
    for word in words:
        sentence = sentence + [word] * count
        count -=1

    sentence = ' '.join(sentence)
    sentence_vec = Tfidf.transform([sentence])
    cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix)
    simLists.append(cosine_sim)
    print(sentence)
sim_sum = np.array([[0.0] * 1445])
for idx, simscore in enumerate(simLists):
    sim_sum += sim_sum + simscore * list_mul[idx]


recommendation = getRecommendation(sim_sum)
#print(recommendation)
#순위별로
print(recommendation.info())
results=df_reviews.iloc[recommendation.index]
print(results)
count=0
for i in range(0,len(results['names'])):
    if len(results.iloc[i,1])>15000:
        if results.iloc[i,2] == '고양시':
            if count<1:
                count+=1
                print(results.iloc[i,0])
            else:
                break


























