import pandas as pd  
indi_book = pd.read_csv("C:/Users/user/Desktop/hackton_2024/indi_book.csv")

# 빈 feature 값이 존재하는 데이터 삭제 
indi_book = indi_book.dropna()
indi_book = indi_book.reset_index()


indi_book_document = indi_book["줄거리"]

#Kkma로 형태소 분석 
!pip install konlpy
from konlpy.tag import Okt
okt = Okt()
indi_book_document_token = [] 

for iterate in range(len(indi_book_document)):
    n_adj = []
    document_lst = okt.pos(indi_book_document[iterate])

    for word, tag in document_lst:
        if tag in ["Noun","Adjective"]:
            n_adj.append(word)
    # 블용어 처리 
    stop_words = " 대한 윤석열 대해 한동훈 대통령 여사 대통령실  명태 올해 관련 대해 위해 최근 여사 김건희 우리 라며 대한 의원 입니다 윤석열 한동훈 대통령 민주당 러시아 대통령실 문재인 명씨 신수지 보이 필요하다 있는 있어 배민 커넥트 배민프모 쿠팡 퀄리 카카오 가 가장 같은 같이 것 것과 것이 것도 게 결론적으로 결과적으로 경우 거의 경향이 고 곳 그 그가 그들 그는 그녀 그들 그때 그래서 그러나 그런 그렇다 그리고 그만큼 그밖에 그에 그에게 그에게서 그에겐 그였고 그중 그중에 그중에서도 극히 근거로 근거한 기에 기타 까지 나 나머지 나아가 나와 나는 날 내 내내 내에서 너희 너희가 너무 내가 너의 더구나 더욱 더군다나 더불어 덕분에 도대체 때문에 또한 때 따라서 띄어쓰기 로 마다 만큼 말하자면 무렵 무슨 뭐 모든 무엇 미만 바 바로 바와 반면에 반해 받아 버린 별 별로 본 부터 뿐만 뿐만이 사이 새롭게 생각에 생각에서 생각하면 서로 설명했듯이 소위 손 수 순간 시 실제로 실제 아 아까 아니 아니다 아닙니다 아래 아무래도 아주 안 앞서 약간 언제 어디 어때 어떤 어떻게 여기 여기에 여전히 역시 여러 여러가지 여러개 여러차례 예를 예를들면 오 오늘 오히려 와 왜 외 요 요즘 우리는 우리의 우리도 우리를 우리를위해 우리는 우리에게 우리에게서 우리도 우리를 우리는 우선 이 이가 이게 이런 이러한 이라고 이란 이로 이를 이른 이와 이외 이후 있다 있으면 있지만 잘 잘못 전 전반적으로 전부 전체 절대 절대로 정말 정말로 정리해 정작 제 제가 제기 제때 제발 조차 좀 좋은 좋지 좋았다 중요하게 중심으로 중요한 중에서 지금 지금까지 지켜야 차례로 참 참으로 첫 처음 처음에는 처음으로 추가적으로 치고 크기 큰 클 통해 통하여 특히 파악하고 하게 하겠다고 하곤 하기에 하고 하기에 하게 하고나서 하나 하나같이 한 한데 한때 한편으로 할 한다 한마디로 할수있다 함께 한편으로 할때 하여 해야 할수 해보았다 해보면 해봤다 해야한다 해야할 하고있고 하고있는 해왔다 했었다 했으며 해왔고 해왔지만 하여 했을때 할지 할때마다 했으며 할때만 하는중에 할때만 했으나 했었고 하여야 할수없었다 하여야할때 하여야할 할수있을 했으며 했을 해오면서 해오기위해 해왔으나 해오려고 하여금 했고 했으나 할수없게 했으나 했지만 하여금 했고 했지만 할수없었다 했지만 할때까지 했을때까지 했지만 할때만 했을때까지 하여야 했다"

    stop_words = set(stop_words.split(' '))
    n_adj = [word for word in n_adj if not word in stop_words and len(word) > 1]
    indi_book_document_token.append(n_adj)


first_week_topic = pd.read_csv("C:/Users/user/Desktop/hackton_2024/first_week_topic.csv")
second_week_topic = pd.read_csv("C:/Users/user/Desktop/hackton_2024/second_week_topic.csv")


# 토큰화 
!pip install gensim
from gensim.corpora import Dictionary
from gensim.utils import simple_preprocess
from itertools import chain

# 이중 리스트를 단일 리스트로 변환

stem_lst = list(chain(*indi_book_document_token)) + first_week_topic.iloc[:,0].tolist() + first_week_topic.iloc[:,1].tolist() + first_week_topic.iloc[:,2].tolist() + first_week_topic.iloc[:,3].tolist() + first_week_topic.iloc[:,4].tolist() + first_week_topic.iloc[:,5].tolist() + second_week_topic.iloc[:,0].tolist() + second_week_topic.iloc[:,1].tolist() + second_week_topic.iloc[:,2].tolist() + second_week_topic.iloc[:,3].tolist() + second_week_topic.iloc[:,4].tolist() + second_week_topic.iloc[:,5].tolist()  + second_week_topic.iloc[:,6].tolist()     


# Dictionary 객체 생성 (단어-숫자 매핑)
dictionary = Dictionary([stem_lst])



# 각 문장을 숫자 ID로만 변환
indi_book_document_vector = [dictionary.doc2idx(text) for text in indi_book_document_token]



first_week_topic_1 = dictionary.doc2idx(first_week_topic.iloc[:,0].tolist())
first_week_topic_2 = dictionary.doc2idx(first_week_topic.iloc[:,1].tolist())
first_week_topic_3 = dictionary.doc2idx(first_week_topic.iloc[:,2].tolist())
first_week_topic_4 = dictionary.doc2idx(first_week_topic.iloc[:,3].tolist())
first_week_topic_5 = dictionary.doc2idx(first_week_topic.iloc[:,4].tolist())
first_week_topic_6 = dictionary.doc2idx(first_week_topic.iloc[:,5].tolist())



second_week_topic_1 = dictionary.doc2idx(second_week_topic.iloc[:,0].tolist())
second_week_topic_2 = dictionary.doc2idx(second_week_topic.iloc[:,1].tolist())
second_week_topic_3 = dictionary.doc2idx(second_week_topic.iloc[:,2].tolist())
second_week_topic_4 = dictionary.doc2idx(second_week_topic.iloc[:,3].tolist())
second_week_topic_5 = dictionary.doc2idx(second_week_topic.iloc[:,4].tolist())
second_week_topic_6 = dictionary.doc2idx(second_week_topic.iloc[:,5].tolist())
second_week_topic_7 = dictionary.doc2idx(second_week_topic.iloc[:,6].tolist())

import numpy as np

def pad_vectors(vec1, vec2):
    # 두 벡터의 길이를 비교
    len_diff = len(vec1) - len(vec2)
    
    # vec1이 길면 vec2를 패딩, vec2가 길면 vec1을 패딩
    if len_diff > 0:
        vec2 = np.pad(vec2, (0, len_diff), mode='constant')
    elif len_diff < 0:
        vec1 = np.pad(vec1, (0, -len_diff), mode='constant')
    
    return vec1, vec2

def cosine_similarity(vec1, vec2):
    # 벡터 패딩
    vec1, vec2 = pad_vectors(vec1, vec2)
    
    # 벡터 내적
    dot_product = np.dot(vec1, vec2)
    
    # 벡터의 크기(유클리드 거리)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    
    # 코사인 유사도 계산
    cosine_sim = dot_product / (norm_vec1 * norm_vec2)
    
    return cosine_sim



first_recommender = [] 
for i in range(len(first_week_topic.columns)) :
    similarity_score = []
    for j in range(len(indi_book_document_vector)):
        similarity_score.append(cosine_similarity(np.array(dictionary.doc2idx(first_week_topic.iloc[:,i].tolist())), np.array(indi_book_document_vector[j])))
    if i % 2 == 0 : 
        index = np.argsort(similarity_score)[-15:][::1]
    else: 
        index = np.argsort(similarity_score)[-15:][::-1]
    first_recommender.append({f"{i+1}번째 이슈와 관련있는 독립서적(평균유사도값:{round(np.mean(sorted(similarity_score , reverse=True)[:15]),3)})" : [indi_book.loc[i,"서명"] for i in index]})


second_recommender = [] 
for i in range(len(second_week_topic.columns)) :
    similarity_score = []
    for j in range(len(indi_book_document_vector)):
        similarity_score.append(cosine_similarity(np.array(dictionary.doc2idx(second_week_topic.iloc[:,i].tolist())), np.array(indi_book_document_vector[j])))
    if i % 2 == 0 : 
        index = np.argsort(similarity_score)[-15:][::-1]
    else: 
        index = np.argsort(similarity_score)[-15:][::1]
    second_recommender.append({f"{i+1}번째 이슈와 관련있는 독립서적(평균유사도값:{round(np.mean(sorted(similarity_score , reverse=True)[:15]),3)})" : [indi_book.loc[i,"서명"] for i in index]})

