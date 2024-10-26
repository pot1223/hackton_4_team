import pandas as pd
import numpy as np
import random
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from konlpy.tag import Okt
from gensim.corpora import Dictionary
from itertools import chain
import os

# FastAPI 인스턴스 생성
app = FastAPI()

# CORS 설정 추가
origins = [
    "http://123.37.11.58:3000/",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# CSV 파일 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
indi_book_path = os.path.join(BASE_DIR, "indi_book.csv")
indi_book2_path = os.path.join(BASE_DIR, "indi_book2.csv")
first_week_topic_path = os.path.join(BASE_DIR, "first_week_topic.csv")
second_week_topic_path = os.path.join(BASE_DIR, "second_week_topic.csv")

# CSV 파일 로드
indi_book = pd.read_csv(indi_book_path).dropna().reset_index()
first_week_topic = pd.read_csv(first_week_topic_path)
second_week_topic = pd.read_csv(second_week_topic_path)

# 형태소 분석 및 불용어 처리
okt = Okt()
stop_words = " 대한 윤석열 대해 한동훈 대통령 여사 대통령실  명태 올해 관련 대해 위해 최근 여사 김건희 우리 라며 대한 의원 입니다 윤석열 한동훈 대통령 민주당 러시아 대통령실 문재인 명씨 신수지 보이 필요하다 있는 있어 배민 커넥트 배민프모 쿠팡 퀄리 카카오 가 가장 같은 같이 것 것과 것이 것도 게 결론적으로 결과적으로 경우 거의 경향이 고 곳 그 그가 그들 그는 그녀 그들 그때 그래서 그러나 그런 그렇다 그리고 그만큼 그밖에 그에 그에게 그에게서 그에겐 그였고 그중 그중에 그중에서도 극히 근거로 근거한 기에 기타 까지 나 나머지 나아가 나와 나는 날 내 내내 내에서 너희 너희가 너무 내가 너의 더구나 더욱 더군다나 더불어 덕분에 도대체 때문에 또한 때 따라서 띄어쓰기 로 마다 만큼 말하자면 무렵 무슨 뭐 모든 무엇 미만 바 바로 바와 반면에 반해 받아 버린 별 별로 본 부터 뿐만 뿐만이 사이 새롭게 생각에 생각에서 생각하면 서로 설명했듯이 소위 손 수 순간 시 실제로 실제 아 아까 아니 아니다 아닙니다 아래 아무래도 아주 안 앞서 약간 언제 어디 어때 어떤 어떻게 여기 여기에 여전히 역시 여러 여러가지 여러개 여러차례 예를 예를들면 오 오늘 오히려 와 왜 외 요 요즘 우리는 우리의 우리도 우리를 우리를위해 우리는 우리에게 우리에게서 우리도 우리를 우리는 우선 이 이가 이게 이런 이러한 이라고 이란 이로 이를 이른 이와 이외 이후 있다 있으면 있지만 잘 잘못 전 전반적으로 전부 전체 절대 절대로 정말 정말로 정리해 정작 제 제가 제기 제때 제발 조차 좀 좋은 좋지 좋았다 중요하게 중심으로 중요한 중에서 지금 지금까지 지켜야 차례로 참 참으로 첫 처음 처음에는 처음으로 추가적으로 치고 크기 큰 클 통해 통하여 특히 파악하고 하게 하겠다고 하곤 하기에 하고 하기에 하게 하고나서 하나 하나같이 한 한데 한때 한편으로 할 한다 한마디로 할수있다 함께 한편으로 할때 하여 해야 할수 해보았다 해보면 해봤다 해야한다 해야할 하고있고 하고있는 해왔다 했었다 했으며 해왔고 해왔지만 하여 했을때 할지 할때마다 했으며 할때만 하는중에 할때만 했으나 했었고 하여야 할수없었다 하여야할때 하여야할 할수있을 했으며 했을 해오면서 해오기위해 해왔으나 해오려고 하여금 했고 했으나 할수없게 했으나 했지만 하여금 했고 했지만 할수없었다 했지만 할때까지 했을때까지 했지만 할때만 했을때까지 하여야 했다"
stop_words = set(stop_words.split(' '))

indi_book_document_token = []
for doc in indi_book["줄거리"]:
    tokens = [
        word for word, tag in okt.pos(doc)
        if tag in ["Noun", "Adjective"] and word not in stop_words and len(word) > 1
    ]
    indi_book_document_token.append(tokens)

# 전체 토큰화 및 Dictionary 생성
stem_lst = list(chain(*indi_book_document_token))
for topic_df in [first_week_topic, second_week_topic]:
    for col in topic_df.columns:
        stem_lst += topic_df[col].tolist()

dictionary = Dictionary([stem_lst])
indi_book_document_vector = [dictionary.doc2idx(text) for text in indi_book_document_token]

# 벡터 패딩 및 코사인 유사도 계산 함수
def pad_vectors(vec1, vec2):
    len_diff = len(vec1) - len(vec2)
    if len_diff > 0:
        vec2 = np.pad(vec2, (0, len_diff), mode='constant')
    elif len_diff < 0:
        vec1 = np.pad(vec1, (0, -len_diff), mode='constant')
    return vec1, vec2

def cosine_similarity(vec1, vec2):
    vec1, vec2 = pad_vectors(vec1, vec2)
    dot_product = np.dot(vec1, vec2)
    return dot_product / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# 추천 생성 함수
def generate_recommendations(topic_df):
    recommendations = []
    for i in range(len(topic_df.columns)):
        topic_name = topic_df.columns[i]
        similarity_scores = [
            cosine_similarity(np.array(dictionary.doc2idx(topic_df.iloc[:, i].tolist())), vec)
            for vec in indi_book_document_vector
        ]
        index = np.argsort(similarity_scores)[-15:][::(-1) ** i]
        recommendations.append({
            "topic": topic_name,
            "score": round(np.mean(sorted(similarity_scores, reverse=True)[:15]), 3),
            "books": [indi_book.loc[idx, "서명"] for idx in index]
        })
    return recommendations

# 각 주차별 추천 생성
first_recommender = generate_recommendations(first_week_topic)
second_recommender = generate_recommendations(second_week_topic)

# 추천 API 엔드포인트
@app.get("/recommendation")
async def get_random_recommendation():
    all_recommendations = first_recommender + second_recommender
    selected_recommendation = random.choice(all_recommendations)
    return {
        "topic": selected_recommendation["topic"],
        "score": selected_recommendation["score"],
        "books": selected_recommendation["books"]
    }

# 책 정보 조회 API (row 번호 기반 조회로 변경)
@app.get("/book_info")
async def get_book_info(title: str = Query(..., description="찾고자 하는 책 제목")):
    books_df = pd.read_csv(indi_book2_path)

    # 책 제목과 일치하는 행 찾기
    book_row = books_df[books_df["서명"] == title]

    if book_row.empty:
        raise HTTPException(status_code=404, detail="해당 제목의 책을 찾을 수 없습니다.")

    # row 번호로 책 정보 추출
    row_number = book_row.index[0]
    book_info = books_df.iloc[row_number]

    return {
        "index": int(row_number),
        "title": book_info["서명"],
        "author": book_info["저자"],
        "genre": book_info["장르"],
        "summary": book_info["줄거리"],
        "author_intro": book_info["작가 소개"],
        "excerpt": book_info["책 속으로"]
    }

