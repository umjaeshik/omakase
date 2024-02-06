import pandas as pd
from konlpy.tag import Okt
import re

df = pd.read_csv('./음식점_sum.csv')
df.info()

df_stopwords = pd.read_csv('./stopwords.csv')
stopwords = list(df_stopwords['stopword'])


okt = Okt()
cleaned_sentences=[]

for review in df.reviews:
    tokened_review = okt.pos(review, stem=True)

    df_token = pd.DataFrame(tokened_review,columns=['word','class'])
    df_token = df_token[(df_token['class']=='Noun') |
                        (df_token['class'] == 'Adjective') |
                        (df_token['class'] == 'Verb')]
    words=[]
    for word in df_token.word:
        if 1<len(word):
            if word not in stopwords:
                words.append(word)

    cleaned_sentence=' '.join(words)
    cleaned_sentences.append(cleaned_sentence)

df['reviews'] = cleaned_sentences
df.dropna(inplace = True)
df.to_csv('./res_naver_sum.csv',index=False)

df.info()
df = pd.read_csv('./res_naver_sum.csv')
df.dropna(inplace = True)

df.to_csv('./res_naver_sum.csv',index=False)
df.info()





