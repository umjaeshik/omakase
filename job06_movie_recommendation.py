import pandas as pd
from sklearn.metrics.pairwise import  linear_kernel
from scipy.io import mmread
import pickle
from konlpy.tag import Okt
from gensim.models import Word2Vec
import numpy as np


def getRecommendation(consine_sim,num):

    simScore = list(enumerate(consine_sim[-1])) #인덱스 유지위해
    simScore = sorted(simScore, key=lambda x:x[1], reverse=True)
    simScore = simScore[:num]
    resIdx = [i[0] for i in simScore]
    resList = df_reviews.iloc[resIdx,0]
    return resList[:10]
    return recmovieList[0:num]
ref_idx = 6

df_reviews = pd.read_csv('./res_naver_sum.csv')
Tfidf_matrix = mmread('./models/Tfidf_movie_review.mtx').tocsr()
with open('./models/tfidf.picle','rb') as f:
    Tfidf = pickle.load(f)

embedding_model = Word2Vec.load('./models/word2vec_res_review.model')
keyword = ['생선','고급']
list_mul = [2,1.5,1.3,1.1,1]
recommendations = []
simLists=[]
for key_list in keyword:
    sim_word = embedding_model.wv.most_similar(key_list, topn=10)
    words = [key_list]
    for word, _ in sim_word:
        words.append(word)
    sentence = []
    count = 10
    for word in words:
        sentence = sentence + [word] * count
        count -=1
    sentence = ' '.join(sentence)
    print(sentence)
    sentence_vec = Tfidf.transform([sentence])
    cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix)
    simLists.append(cosine_sim)

sim_sum = np.array([[0.0] * 1445])
for idx, simscore in enumerate(simLists):
    sim_sum += sim_sum + simscore * list_mul[idx]

recommendation = getRecommendation(sim_sum,50)
print(recommendation)






# food_result = pd.DataFrame({'names':'','simscore':0,'orderbyu':0})
# for recommendation in recommendations:
#     food_result = food_result + recommendation
#
# oriList = list(recommendations[0]) + list(recommendations[1])
#
#
#
#
# print(dupList)



















