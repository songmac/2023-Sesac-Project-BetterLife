import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 전처리된 프로그램 정보 data
excel_file_path = './yumi/langchain_facility_info.csv'
program_info_data = pd.read_csv(excel_file_path)

# Remove duplicate rows based on '프로그램명'
program_info_data = program_info_data.drop_duplicates(subset='프로그램명', keep='first')

# 첫번째 tfidf_matrix에서 모든 프로그램간의 코사인 유사도 계산
tfidf_vector = TfidfVectorizer()
tfidf_matrix = tfidf_vector.fit_transform(program_info_data['프로그램명'] + " " + program_info_data['연령'] + " " + program_info_data['장애'] + " " + str(
    program_info_data['주간횟수']) + " " + program_info_data['시간대'] + " " + program_info_data['지번주소']).toarray()

tfidf_df = pd.DataFrame(tfidf_matrix, columns=tfidf_vector.get_feature_names_out(), index=program_info_data['프로그램명'])

# 프로그램간 유사도
cosine_sim = cosine_similarity(tfidf_df)

# 새로운 입력값에 대하여 이전 tfidf_matrix와 비교하여 코사인 유사도 계산
def find_recommended_program(user_program, user_age, user_disability, user_frequency, user_hour, user_location, data):
    user_input = user_program + " " + user_age + " " + user_disability + " " + user_frequency + " " + user_hour + " " + user_location
    input_vector = tfidf_vector.transform([user_input]).toarray().flatten()

    # Change tfidf_matrix to tfidf_df in the following line
    sim_scores = cosine_similarity([input_vector], tfidf_df).flatten()
    similar_program_indices = sim_scores.argsort()[::-1]

    recommendations = []
    for idx in similar_program_indices[:3]:
        program_info = program_info_data.iloc[idx]
        program_info['Cosine Similarity'] = sim_scores[idx]
        recommendations.append(program_info)

    return pd.DataFrame(recommendations)

user_program = '수영'
user_age = '성인'
user_disability = '무'
user_frequency = '3'
user_hour = '오후'
user_location = '중랑구'

result = find_recommended_program(user_program, user_age, user_disability, user_frequency, user_hour, user_location, program_info_data)
print(result)
