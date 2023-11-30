import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#코사인 유사도를 통해 프로그램에 해당하는 시설 정보 추출
def recommend_programs(user_answers, data):
    #TF_IDF 변환 모델 초기화
    #TF-IDF는 TF와 IDF를 곱한 값을 의미하는 데, 문서를 d, 단어를 t, 문서의 총 개수를 n이라고 표현

    # 사용자 답변 중 "무관"을 제외
    user_answers = ' '.join(answer for answer in user_answers.split() if answer != "무관")
    print(user_answers)
    # 사용자 응답 벡터화
    vectorizer = TfidfVectorizer()
    user_vector = vectorizer.fit_transform([user_answers])
    user_vocab = vectorizer.vocabulary_

    # 프로그램 벡터화
    program_descriptions = data['시설명'] + ' ' + data['종목명']+ ' ' + data['프로그램명'] + ' ' + data['연령']+ ' ' + data['성별'] + ' ' + data['장애']+ ' ' + data['주간횟수'].astype(str) + ' ' + data['시간대'] + ' ' + data['지번주소']
    program_vectorizer = TfidfVectorizer(vocabulary=user_vocab)
    program_vectors = program_vectorizer.fit_transform(program_descriptions)

    # 코사인유사도 계산
    cosine_similarities = cosine_similarity(user_vector, program_vectors).flatten()

    # 유사도가 높은 순서대로 정렬된 인덱스 가져오기
    similar_program_indices = cosine_similarities.argsort()[::-1]

    # 추천 결과를 담을 리스트
    recommendations = []
    for idx in similar_program_indices[:1]:
        program_info = data.iloc[idx].copy()
        program_info['Cosine Similarity'] = cosine_similarities[idx]
        
        # 추천된 프로그램 중에 중복 프로그램 확인
        duplicate_program = any((program_info == existing).all() for existing in recommendations)

        #중복된 프로그램이 없는 경우에만 추가
        if not duplicate_program:
            recommendations.append(program_info)
    return pd.DataFrame(recommendations)

# 예시 사용
# user_answers = '학생 수영 종로구 무 새벽 주1회'
# excel_file_path = './yumi/langchain_facility_info.xlsx'
# df = pd.read_excel(excel_file_path)
# #중복된 행은 삭제
# unique_program = df.drop_duplicates()
# recommendations = recommend_programs(user_answers, unique_program)
# print(recommendations)