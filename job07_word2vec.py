import pandas as pd
from gensim.models import Word2Vec

df_review = pd.read_csv('./res_naver_sum.csv')
df_review.info()

reviews=list(df_review['reviews'])
print(reviews[0])
tokens = []
for sentence in reviews:
    token = sentence.split()
    tokens.append(token)
print(token[0])
#vector_size 차원 축소 ->입력 토큰들에서 차원을 해당 숫자로 축소함.    window->  conv레이어 필터 사이즈라고 이해  min_count 의미 부여하기 위한 최소 필요횟수
embedding_model = Word2Vec(tokens, vector_size=100, window=4, min_count=20, workers=4, epochs=100,sg=1)
embedding_model.save('./models/word2vec_res_review.model')
print(len(embedding_model.wv.index_to_key))
print(list(embedding_model.wv.index_to_key))