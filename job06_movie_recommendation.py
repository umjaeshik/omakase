import pandas as pd
from sklearn.metrics.pairwise import  linear_kernel
from scipy.io import mmread
import pickle
from konlpy.tag import Okt
from gensim.models import Word2Vec

def getRecommendation(consine_sim):
    simScore = list(enumerate(consine_sim[-1])) #인덱스 유지위해
    simScore = sorted(simScore, key=lambda x:x[1], reverse=True)
    simScore = simScore[:100]
    movieIdx = [i[0] for i in simScore]
    recmovieList = df_reviews.iloc[movieIdx,0]
    return recmovieList[0:100]
ref_idx = 6

df_reviews = pd.read_csv('./res_naver_sum.csv')
Tfidf_matrix = mmread('./models/Tfidf_movie_review.mtx').tocsr()
with open('./models/tfidf.picle','rb') as f:
    Tfidf = pickle.load(f)
#영화  index 이용
# print(df_reviews.iloc[ref_idx,0])
# consine_sim = linear_kernel(Tfidf_matrix[ref_idx],Tfidf_matrix)
# print(consine_sim[0])
# print(len(consine_sim))
# recommandation = getRecommendation(consine_sim)
# print(recommandation)
#
# print()

#keyword 이용
#키워드 입력-> 비슷한 의미 단어 10개 를  simword 넣어주고 문장을 만들어 준다.
#문장 생성 규칙 처음 입력단어부터 가장 가중치가 낮은 단어까지 고려해서 count -1 그리고 * 문장을 만들어줌.
#해당 문장을 벡터화해서 리니어 모델에 던져줌.
#코사인 값이 비슷한 상위 10개를 리턴해서 출력
embedding_model = Word2Vec.load('./models/word2vec_res_review.model')
keyword = ['생선','고급']
recommendations = []
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
    recommendation = getRecommendation(cosine_sim)
    #print(recommendation)

    recommendations.append(recommendation)

oriList = list(recommendations[0]) + list(recommendations[1])
removedupList = [] #중복값이 제거된 순수한 값이 들어갈 리스트
dupList = [] #중복된 값을 찾아서 넣어주는 리스트

for i in oriList:
    if i in removedupList:
        if i in dupList:
            pass
        else:
            dupList.append(i)
    else:
        removedupList.append(i)

print(dupList)



















