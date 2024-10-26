import pandas as pd
import numpy as np
import random
from fastapi import FastAPI, HTTPException, Query
from konlpy.tag import Okt
from gensim.corpora import Dictionary
from itertools import chain
import os

# FastAPI 인스턴스 생성
app = FastAPI()

# CSV 파일 경로 설정 (같은 폴더에 있다고 가정)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
indi_book_path = os.path.join(BASE_DIR, "indi_book.csv")
indi_book2_path = os.path.join(BASE_DIR, "indi_book2.csv")  # 새로 사용할 파일
first_week_topic_path = os.path.join(BASE_DIR, "first_week_topic.csv")
second_week_topic_path = os.path.join(BASE_DIR, "second_week_topic.csv")

# CSV 파일 로드
indi_book = pd.read_csv(indi_book_path).dropna().reset_index()
first_week_topic = pd.read_csv(first_week_topic_path)
second_week_topic = pd.read_csv(second_week_topic_path)

# 형태소 분석 및 불용어 처리
okt = Okt()
stop_words = set("""
    대한 윤석열 대해 한동훈 대통령 여사 대통령실 명태 올해 관련 우리 ...
""".split())

indi_book_document_token = []
for doc in indi_book["줄거리"]:
    tokens = [word for word, tag in okt.pos(doc) if tag in ["Noun", "Adjective"] and word not in stop_words and len(word) > 1]
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
        topic_name = topic_df.columns[i]  # 주제명 가져오기
        similarity_scores = [
            cosine_similarity(np.array(dictionary.doc2idx(topic_df.iloc[:, i].tolist())), vec)
            for vec in indi_book_document_vector
        ]
        index = np.argsort(similarity_scores)[-15:][::(-1) ** i]
        recommendations.append({
            "topic": topic_name,  # 주제명 반환
            "score": round(np.mean(sorted(similarity_scores, reverse=True)[:15]), 3),
            "books": [indi_book.loc[idx, "서명"] for idx in index]
        })
    return recommendations

# 각 주차별 추천 생성
first_recommender = generate_recommendations(first_week_topic)
second_recommender = generate_recommendations(second_week_topic)

# 기존 추천 API 엔드포인트
@app.get("/recommendation")
async def get_random_recommendation():
    all_recommendations = first_recommender + second_recommender
    selected_recommendation = random.choice(all_recommendations)
    return {
        "topic": selected_recommendation["topic"],
        "score": selected_recommendation["score"],
        "books": selected_recommendation["books"]
    }

# 대체된 책 정보 조회 API (indi_book2.csv 사용)
@app.get("/book_info")
async def get_book_info(title: str = Query(..., description="찾고자 하는 책 제목")):
    # 새로운 indi_book2.csv 파일 로드
    books_df = pd.read_csv(indi_book2_path)

    # 책 제목과 일치하는 행 찾기
    book_row = books_df[books_df["서명"] == title]

    if book_row.empty:
        raise HTTPException(status_code=404, detail="해당 제목의 책을 찾을 수 없습니다.")

    # 해당 책의 index 값으로 상세 정보 추출
    index_value = book_row.iloc[0]["index"]
    book_info = books_df.iloc[index_value]

    return {
        "index": int(index_value),
        "title": book_info["서명"],
        "author": book_info["저자"],
        "genre": book_info["장르"],
        "summary": book_info["줄거리"],
        "author_intro": book_info["작가 소개"],
        "excerpt": book_info["책 속으로"]
    }

