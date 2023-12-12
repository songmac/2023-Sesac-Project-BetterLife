# 라이브러리 임포트
import pandas as pd
import numpy as np
from surprise import Dataset, Reader, SVD, accuracy
from surprise.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
import joblib
import chardet
import time



#--------------------------------------------------------------------------------------------------------------------------------------------#




def load_data_and_train_svd_model(file_path):
    # 데이터 로드
    exercise_review_data_df = pd.read_csv(file_path, encoding='utf-8')
    model_df = exercise_review_data_df[['사용자ID', '운동프로그램', '가중평균만족도']]
    reader = Reader(rating_scale=(0.0, 5.0))
    data = Dataset.load_from_df(model_df, reader)

    # 학습 시작 시간 측정
    start_time = time.time()

    # Grid Search로 최적의 매개변수 찾기
    param_grid = {
        'n_epochs': [20, 40],
        'n_factors': [50, 100, 150, 200, 250],
        'lr_all': [0.002, 0.005, 0.007],
        'reg_all': [0.02, 0.05, 0.1]
    }
    grid_search = GridSearchCV(SVD, param_grid=param_grid, measures=['rmse', 'mae'], cv=5)
    grid_search.fit(data)

    # 최적의 매개변수로 모델 생성 및 훈련
    best_params = grid_search.best_params['rmse']
    algo = SVD(n_factors=best_params['n_factors'], n_epochs=best_params['n_epochs'], lr_all=best_params['lr_all'], reg_all=best_params['reg_all'])
    trainset = data.build_full_trainset()
    algo.fit(trainset)

    # 모델 저장
    joblib.dump(algo, 'svd_model.pkl')

    # 학습 종료 시간 측정 및 소요 시간 계산
    end_time = time.time()
    elapsed_time = end_time - start_time

    print("Grid Search 최적의 매개변수:", grid_search.best_params['rmse'])
    print("학습에 걸린 시간: {:.2f}초".format(elapsed_time))

    return algo, best_params['n_factors'], best_params['n_epochs'], best_params['lr_all'], best_params['reg_all']


# 파일 경로 설정
file_path = 'C:/Users/User/project/SESAC/2023-Sesac-Project-BeLife/data/exercise_reviews_dataset.csv'

# SVD 모델 생성 및 훈련
algo, best_n_factors, best_n_epochs, best_lr_all, best_reg_all = load_data_and_train_svd_model(file_path)



#--------------------------------------------------------------------------------------------------------------------------------------------#




# 새로운 입력 데이터 샘플
new_data_values = [
    ['1001', '학생', '무', '양천구 신월제2동', '무관', '구기및라켓', '오전', '주1회', '선호지역', '1001_5', '요가_하타', '3.2'],
    # 추가 데이터 행을 여기에 입력할 수 있음
]


def process_new_data_and_update_model(algo, new_data_values, update_model_with_new_data, predict_program_rating, get_top_programs):
    """
    새로운 데이터로 모델 업데이트, 예측 및 추천 수행
    - algo: 학습된 모델
    - new_data_values: 새로운 사용자 데이터 값
    - update_model_with_new_data: 모델 업데이트 함수
    - predict_program_rating: 평점 예측 함수
    - get_top_programs: 상위 추천 프로그램 추출 함수
    """
    new_data_columns = ['사용자ID', '연령대', '장애유무', '선호지역', '운동목표', '선호운동', '선호시간대', '선호빈도', '중요항목', '리뷰ID', '운동프로그램', '가중평균만족도']
    new_data = pd.DataFrame(data=new_data_values, columns=new_data_columns)
    update_model_with_new_data(algo, new_data)
    prediction = predict_program_rating(algo, (new_data_values[0][0], new_data_values[0][10]))
    print(f"사용자 {new_data_values[0][0]}가 프로그램 '{new_data_values[0][10]}'에 대한 예상 평점은 {prediction['예상평점']:.1f}입니다.")
    top_programs = get_top_programs(algo, new_data_values[0][0])
    print(f"\n사용자 {new_data_values[0][0]}에게 추천하는 프로그램 상위 3개:")
    for program in top_programs:
        print(f"{program['프로그램명']}: 예상 평점 {program['예상평점']:.1f}")
    return top_programs


def update_model_with_new_data(algo, new_data_values):
    # 기존 데이터 로드
    exercise_review_data_df = pd.read_csv(file_path, encoding='utf-8')

    # 새로운 데이터 추가
    new_data_columns = ['사용자ID', '연령대', '장애유무', '선호지역', '운동목표', '선호운동', '선호시간대', '선호빈도', '중요항목', '리뷰ID', '운동프로그램', '가중평균만족도']
    new_data_df = pd.DataFrame(new_data_values, columns=new_data_columns)
    updated_data_df = pd.concat([exercise_review_data_df, new_data_df])

    # 데이터셋을 surprise 라이브러리 형식으로 로드
    reader = Reader(rating_scale=(0.0, 5.0))
    data = Dataset.load_from_df(updated_data_df[['사용자ID', '운동프로그램', '가중평균만족도']], reader)
    trainset = data.build_full_trainset()

    # 기존의 하이퍼파라미터를 유지한 채로 모델 훈련
    algo.fit(trainset)

    # 모델 저장
    joblib.dump(algo, 'svd_model.pkl')




def predict_rating(algo, user_program_pair):
    """
    개별 프로그램에 대한 사용자 평점 예측
    - algo: 학습된 모델
    - user_program_pair: 사용자와 프로그램명 쌍
    """
    user_id, program_name = user_program_pair
    prediction = algo.predict(user_id, program_name)
    return {'프로그램명': program_name, '예상평점': prediction.est}

def get_top_programs(algo, user_id, num_programs=3):
    """
    사용자별 상위 프로그램 예측
    - algo: 학습된 모델
    - user_id: 사용자 ID
    - num_programs: 추천할 프로그램 수
    """
    # 기존 데이터 로드 및 유니크한 프로그램 명 추출
    exercise_review_data_df = pd.read_csv(file_path, encoding='utf-8')
    unique_programs = exercise_review_data_df['운동프로그램'].unique()

    # 최대 num_programs 개수만큼의 프로그램명 사용
    test_data = [(user_id, program) for program in unique_programs[:num_programs]]
    predictions = [predict_rating(algo, pair) for pair in test_data]

    # 예상 평점에 따라 정렬
    predicted_programs = sorted(predictions, key=lambda x: x['예상평점'], reverse=True)
    return predicted_programs



#--------------------------------------------------------------------------------------------------------------------------------------------#



# 함수 호출
update_model_with_new_data(algo, new_data_values)


# 새로운 예측 및 추천 수행
top_programs = process_new_data_and_update_model(algo, new_data_values, update_model_with_new_data, predict_rating, get_top_programs)

# 결과 출력
for program in top_programs:
    print(f"{program['프로그램명']}: 예상 평점 {program['예상평점']:.1f}")
