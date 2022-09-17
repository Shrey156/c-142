import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df=pd.read_csv('final.csv')

df=df[df['soup'].notna()]
count=CountVectorizer(stop_words='english')
m_count=count.fit_transform(df['soup'])
cs=cosine_similarity(m_count,m_count)
df=df.reset_index()

indicies=pd.Series(df.index,index=df['original_title'])

def get_recommendation(title):
    id=indicies[title]
    scores=list(enumerate(cs[id]))
    scores=sorted(scores,key=lambda x:x[1],reverse=True)
    scores=scores[1:11]
    movies_id=[i[0] for i in scores] 
    return df[['original_title' , 'poster_link' , 'runtime', 'release_date' , 'weighted_rating' ].iloc[movies_id]]