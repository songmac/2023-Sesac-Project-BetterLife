import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


# 질문 리스트 생성
questions = [
    "1. 연령대를 선택해주세요. (1: 학생(초, 중, 고등), 2: 성인(대학생), 3: 노인)",
    "2. 건강 상태를 선택해주세요. (1: 디스크, 2: 관절 질환, 3: 혈압 질환, 4: 대사증후군, 5: 해당 없음)",
    "3. 운동 목표를 선택해주세요. (1: 심폐지구력 향상, 2: 근력 향상, 3: 체형 교정, 4: 무관)",
    "4. 선호 지역을 입력해주세요. (예: 관악구)",
    "5. 선호 빈도를 선택해주세요. (1: 주1회, 2: 주2회, 3: 주3회, 4: 주4회 이상)",
    "6. 선호 시간대를 선택해주세요. (1: 새벽, 2: 오전, 3: 오후, 4: 저녁, 5: 무관)",
    "7. 선호 운동을 선택해주세요. (1: 구기및라켓, 2: 레저, 3: 무도, 4: 무용, 5: 민속, 6: 재활, 7: 체력단련및생활운동)",
    "8. 선호 인원수를 선택해주세요. (1: 5명 이하, 2: 5명 이상, 3: 무관)",
    "9. 운동 프로그램을 선택할 때 가장 중요하게 생각하시는 항목을 골라주세요. (1: 연령대, 2: 건강상태, 3: 운동목표, 4: 선호 지역, 5: 선호빈도, 6: 선호시간대, 7: 선호운동, 8: 선호인원수, 9: 무관)"
]

# 질문 응답 딕셔너리
question_responses = [{'1': '학생(초, 중, 고등학생)', '2':'성인(대학생)', '3':'노인'}, {'1':'디스크', '2':'관절 질환', '3':'혈압 질환', '4':'대사증후군', '5':'해당 없음'}, {'1':'심폐지구력 향상', '2':'근력 향상', '3':'체형 교정', '4':'무관'}, {}, {'1': '주 1회', '2':'주 2회', '3':'주 3회', '4': '주 4회 이상'}, {'1':'새벽', '2':'오전', '3':'오후', '4':'저녁', '5':'무관'}, {'1':'구기 및 라켓', '2':'레저', '3':'무도', '4':'무용', '5':'민속', '6':'재활', '7':'체력 단련 및 생활 운동'}, {'1':'5명 이하', '2':'5명 이상', '3':'무관'}, {'1':'연령대', '2':'건강 상태', '3':'운동 목표', '4':'선호 지역', '5':'선호 빈도', '6':'선호 시간대', '7':'선호 운동', '8':'선호 인원수', '9':'무관'}]

# 질문 인덱스 초기화
question_index = 0

# 사용자 응답 딕셔너리에 저장
user_responses = {}

# 사용자 입력 유효성 검사
def validate_input(question, response):
    if not response:
        print('응답은 비어있을 수 없습니다.')
        return False
    
    if question_index == 3 and not re.match(r'\w+구', response):
        print('정확한 주소 형식으로 입력해주세요 (예: 관악구).')
        return False
    
    if question_index != 3 and response not in question_responses[question_index]:
        print('올바른 응답을 선택해주세요.')
        return False
    
    return True


def ask_question():
    global question_index
    if question_index < len(questions):
        current_question = questions[question_index]
        user_response = input(current_question + "\n")

        if not validate_input(current_question, user_response):
            ask_question()
            return

        response_key = str(user_response)

        if question_index == 3:
            user_responses[f'Question {question_index + 1}'] = user_response
        else:
            user_responses[f"Question {question_index + 1}"] = question_responses[question_index][response_key]
    
        question_index += 1
        ask_question()
    else:
        print("사용자 답변:")
        for key, value in user_responses.items():
            print(f"{key}: {value}")

# 함수 호출
ask_question()

#사용자 응답
user_answers = list(user_responses.values())


# 엑셀 파일 불러오기
df = pd.read_excel('dahee/data/data_code.xlsx')


# 벡터화를 위해 사용자 응답을 문자로 변환
user_answers_str = ' '.join(user_answers)

# 사용자 응답 벡터화
vectorizer = TfidfVectorizer()
user_vector = vectorizer.fit_transform([user_answers_str])
user_vocab = vectorizer.vocabulary_

# 프로그램 벡터화
program_descriptions = df['시설명'].astype(str) + ' ' + df['종목명'].astype(str) + ' ' + df['프로그램명'].astype(str) + ' ' + df['연령'].astype(str) + ' ' + df['성별'].astype(str) + ' ' + df['장애'].astype(str) + ' ' + df['주간횟수'].astype(str) + ' ' + df['시간대'].astype(str) + ' ' + df['지번주소'].astype(str)
program_vectorizer = TfidfVectorizer(vocabulary=user_vocab)
program_vectors = program_vectorizer.fit_transform(program_descriptions)
# program_vectors = vectorizer.transform(program_descriptions)

# 디버깅을 위한 벡터화 데이터 출력
# print("User Vector: ", user_vector)
# print("User Vocabr: ", user_vocab)
# print("\nProgram Vectors: ", program_vectors)

# 코사인유사도 계산
cosine_similarities = linear_kernel(user_vector, program_vectors).flatten()

# 데이터프레임에 코사인유사도 추가
df['cosine_similarity'] = cosine_similarities

# 코사인유사도 기준으로 내림차순 정렬
df = df.sort_values(by='cosine_similarity', ascending=False)

# 상위 추천 운동 프로그램 출력
top_recommendations = df[['시설명', '프로그램명', '연령', '성별', '장애', '주간횟수', '시간대', '지번주소', 'cosine_similarity']].head(5)
print(top_recommendations)