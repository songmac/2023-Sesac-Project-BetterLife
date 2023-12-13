# content and collaborative filtering based hybrid modeling
# 콘텐츠 기반 필터링 구현: 사용자의 선호도 및 기타 특성을 이용하여 콘텐츠 기반 추천을 생성
# 하이브리드 추천 생성: 협업 필터링과 콘텐츠 기반 필터링의 결과를 통합하여 최종 추천을 생성



import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import GridSearchCV 
import joblib
import time
import random

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from mfsvd_modeling import load_data_and_train_svd_model, get_top_programs, integrated_model_update_and_recommendation
from mfsvd_modeling import find_max_user_id, predict_program_rating
from mfsvd_dataset import generate_user_info_and_reviews



# 주요 실행 부분
file_path = 'C:/Users/User/project/SESAC/2023-Sesac-Project-BeLife/data/exercise_reviews_dataset.csv'
num_users_to_generate = 5

algo = load_data_and_train_svd_model(file_path)
integrated_model_update_and_recommendation(num_users_to_generate, file_path, algo)



# 사용자 프로필과 운동 프로그램 프로필을 생성하는 함수
def create_user_and_program_profiles(data):
    # 사용자 프로필 생성
    user_profiles = data[['사용자ID', '운동목표', '선호운동']].drop_duplicates().set_index('사용자ID')
    user_profiles['profile'] = user_profiles.apply(lambda x: ' '.join(x), axis=1)

    # 운동 프로그램 프로필 생성
    program_profiles = data[['운동프로그램', '가중평균만족도']].groupby('운동프로그램').mean()

    return user_profiles, program_profiles



korean_stop_words = ['을','를']

# 콘텐츠 기반 추천을 수행하는 함수
def content_based_recommendation(user_id, user_profiles, program_profiles, top_n=5):
    tfidf = TfidfVectorizer(stop_words=korean_stop_words)
    tfidf_matrix = tfidf.fit_transform(user_profiles['profile'])

    # 해당 사용자 프로필과 모든 프로그램 프로필 간의 유사도 계산
    user_profile = tfidf.transform([user_profiles.loc[user_id, 'profile']])
    cosine_sim = cosine_similarity(user_profile, tfidf_matrix)

    # 가장 유사한 프로그램 추천
    top_indices = cosine_sim.argsort()[0][-top_n:][::-1]
    recommended_programs = program_profiles.iloc[top_indices].index.tolist()

    return recommended_programs



# 사용자 및 프로그램 프로필 생성
combined_reviews_df = generate_user_info_and_reviews(num_users=num_users_to_generate)
user_profiles, program_profiles = create_user_and_program_profiles(combined_reviews_df)



# 예시 사용자에 대한 콘텐츠 기반 추천
user_id = 1 # 예시 사용자 ID
recommended_programs = content_based_recommendation(user_id, user_profiles, program_profiles)
print(f'콘텐츠 기반 추천 결과: {recommended_programs}')


def hybrid_recommendation(user_id, user_profiles, program_profiles, algo, top_n=3):
    content_based_recs = content_based_recommendation(user_id, user_profiles, program_profiles, top_n)
    collaborative_recs = [program['프로그램명'] for program in get_top_programs(algo, user_id, top_n)]

    hybrid_recs = list(set(content_based_recs + collaborative_recs))

    return hybrid_recs[:top_n]

# 예시 사용자에 대한 하이브리드 추천
user_id = 1 # 예시 사용자 ID
hybrid_recommendations = hybrid_recommendation(user_id, user_profiles, program_profiles, algo)
print(f'하이브리드 기반 추천 결과: {hybrid_recommendations}')