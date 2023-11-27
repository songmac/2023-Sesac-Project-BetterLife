import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#전처리된 프로그램 정보 data 엑셀 
excel_file_path = './yumi/langchain_facility_info.csv'
program_info_data = pd.read_csv(excel_file_path)

#TF_IDF 변환 모델 초기화
#TF-IDF는 TF와 IDF를 곱한 값을 의미하는 데, 문서를 d, 단어를 t, 문서의 총 개수를 n이라고 표현
tfidf_vector = TfidfVectorizer()
#tfidf_matrix = tfidf_vector.fit_transform안에 들어 있는 컬럼들을 하나로 합쳐 벡터화 시킴
tfidf_matrix = tfidf_vector.fit_transform(program_info_data['시설명'] + " " +program_info_data['프로그램명'] + " " + 
                                          program_info_data['지번주소'] + " " + program_info_data['연령'] + " " + program_info_data['장애'] + " " + 
                                          program_info_data['주간횟수'].astype(str) + " " + program_info_data['시간대']).toarray()
#print(tfidf_matrix.shape)
#모델에서 추출한 단어들의 리스트를 반환
tfidf_matrix_feature = tfidf_vector.get_feature_names_out()

#TF-IDF 행렬을 pandas의 DataFrame으로 변환
#index=program_info_data.프로그램명: 각 행의 인덱스를 프로그램명으로 지정
tfidf_matrix = pd.DataFrame(tfidf_matrix, columns=tfidf_matrix_feature, index = program_info_data.프로그램명)
# #print(tfidf_matrix.shape) => (11127, 550)

# #tf-idf vector를 코사인 유사도를 통해 유사도 값을 구해줌
# #프로그램 갯수만큼 n*n의 매트릭스 형태로 나옴
cosine_sim = cosine_similarity(tfidf_matrix)
#program_to_index = dict(zip(program_info_data['프로그램명'], program_info_data.index))

def get_recommendations(input_program, input_address, input_age, input_disability, input_frequency, input_hour, cosine_sim=cosine_sim, data=program_info_data):
    
    #input값에 해당하는 인덱스트 
    input_text = input_program + " " + input_address + " " + input_age + " " + input_disability + " " + input_frequency + " " + input_hour 
    
    # 입력값에 대한 TF-IDF 벡터 생성
    input_vector = tfidf_vector.fit_transform([input_text]).toarray().flatten()
    
    # 입력값과 각 프로그램의 코사인 유사도 계산
    sim_scores = cosine_similarity([input_vector], tfidf_matrix).flatten()
    
    # 유사도가 높은 순서대로 정렬된 인덱스 가져오기
    similar_program_indices = sim_scores.argsort()[::-1]
    
    # 추천 결과를 담을 리스트
    recommendations = []
    
    # 상위 3개의 유사한 프로그램 정보를 가져와 리스트에 추가
    for idx in similar_program_indices[:3]:
        program_info = data.iloc[idx]
        program_info['Cosine Similarity'] = sim_scores[idx]  
        recommendations.append(program_info)
    
    return pd.DataFrame(recommendations)
    
input_program = "댄스"
input_age  = '성인'
input_disability = '무'
input_address = '관악구'
input_frequency = '3'
input_hour = '아침'

recommendations = get_recommendations(input_program, input_age, input_disability, input_address, input_frequency, input_hour)
print(recommendations)
