# 라이브러리 임포트
import pandas as pd
import numpy as np
from surprise import Dataset, Reader, SVD, accuracy
from surprise.model_selection import train_test_split, GridSearchCV
import joblib
from multiprocessing import Pool


def create_svd_model(data):
    """
    SVD 모델 생성 및 훈련
    - data: 훈련 데이터셋
    """
    algo = SVD(n_factors=50, random_state=42)
    trainset = data.build_full_trainset()
    algo.fit(trainset)
    return algo

def predict_rating(algo, user_program_pair):
    """
    개별 프로그램에 대한 사용자 평점 예측
    - algo: 학습된 모델
    - user_program_pair: 사용자와 프로그램명 쌍
    """
    user_id, program_name = user_program_pair
    prediction = algo.predict(user_id, program_name)
    return {'프로그램명': program_name, '예상평점': prediction.est}

def get_top_programs_parallel(algo, user_id, num_programs=3):
    """
    병렬 처리를 이용한 사용자별 상위 프로그램 예측
    - algo: 학습된 모델
    - user_id: 사용자 ID
    - num_programs: 추천할 프로그램 수
    """
    test_data = [(user_id, f"프로그램_{i}") for i in range(1, num_programs + 1)]
    
    with Pool() as pool:
        predictions = pool.map(lambda x: predict_rating(algo, x), test_data)

    predicted_programs = sorted(predictions, key=lambda x: x['예상평점'], reverse=True)
    return predicted_programs

def update_model_with_new_data(algo, new_data):
    """
    새로운 데이터로 모델 업데이트
    - algo: 학습된 모델
    - new_data: 새로운 사용자 데이터
    """
    algo_data = algo.trainset.build_testset() + [(user, item, rating) for user, item, rating in new_data.itertuples(index=False)]
    algo.fit(algo_data)
    model_filename = 'svd_model.pkl'
    joblib.dump(algo, model_filename)

def process_and_train_svd_model(file_path):
    """
    파일에서 데이터를 불러와 SVD 모델 생성 및 훈련
    - file_path: 데이터 파일 경로
    """
    exercise_review_data_df = pd.read_csv(file_path, encoding='utf-8')
    model_df = pd.DataFrame({
        '사용자': np.repeat(exercise_review_data_df['사용자ID'], len(exercise_review_data_df)),
        '프로그램명': np.tile(exercise_review_data_df['운동프로그램'].tolist(), len(exercise_review_data_df)),
        '평점': np.tile(exercise_review_data_df['만족도'].tolist(), len(exercise_review_data_df))
    })
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(model_df[["사용자", "프로그램명", "평점"]], reader)
    trainset, testset = train_test_split(data, test_size=0.25)
    param_grid = {'n_epochs': [20, 40], 'n_factors': [50, 100, 200]}
    grid = GridSearchCV(SVD, param_grid=param_grid, measures=['rmse', 'mae'], cv=3)
    grid.fit(data)
    return grid.best_params['rmse']

def process_new_data_and_update_model(algo, new_data_values, update_model_with_new_data, predict_program_rating, get_top_programs):
    """
    새로운 데이터로 모델 업데이트, 예측 및 추천 수행
    - algo: 학습된 모델
    - new_data_values: 새로운 사용자 데이터 값
    - update_model_with_new_data: 모델 업데이트 함수
    - predict_program_rating: 평점 예측 함수
    - get_top_programs: 상위 추천 프로그램 추출 함수
    """
    new_data_columns = ['사용자ID', '연령대', '장애유무', '선호지역', '운동목표', '선호운동', '선호시간대', '선호빈도', '중요항목', '리뷰ID', '운동프로그램', '만족도']
    new_data = pd.DataFrame(data=new_data_values, columns=new_data_columns)
    update_model_with_new_data(algo, new_data)
    prediction = predict_program_rating(algo, new_data_values[0][0], new_data_values[0][10])
    print(f"사용자 {new_data_values[0][0]}가 프로그램 '{new_data_values[0][10]}'에 대한 예상 평점은 {prediction:.2f}입니다.")
    top_programs = get_top_programs(algo, new_data_values[0][0])
    print(f"\n사용자 {new_data_values[0][0]}에게 추천하는 프로그램 상위 3개:")
    for program in top_programs:
        print(f"{program['프로그램명']}: 예상 평점 {program['예상평점']:.2f}")
    return top_programs




# 데이터 파일 경로
file_path = 'C:/Users/User/project/SESAC/2023-Sesac-Project-BeLife/data/exercise_review_data_1000.csv'
# SVD 모델 생성 및 훈련
best_params = process_and_train_svd_model(file_path)
algo = create_svd_model(best_params)  # 여기서 best_params는 GridSearch를 통해 얻은 최적의 파라미터를 사용



# 새로운 데이터 예시
new_data_values = [
    ['1001', '학생', '무', '양천구 신월제2동', '무관', '구기및라켓', '오전', '주1회', '선호지역', '1_5', '요가_하타', '1'],
    ['1002', '성인', '유', '동대문구 회기동', '체중 및 신체구성 조절', '레저', '무관', '주3회', '선호시간대', '3_1', '치어리더', '4'],
    ['1003', '노인', '유', '양천구 신정제4동', '무관', '재활', '무관', '주4회이상', '운동목표', '4_1', '요가_산후', '3'],
    # 추가 데이터 행을 여기에 입력할 수 있음
]

# 함수 호출
top_programs = process_new_data_and_update_model(algo, new_data_values, update_model_with_new_data, predict_rating, get_top_programs_parallel)

# 결과 출력
for program in top_programs:
    print(f"{program['프로그램명']}: 예상 평점 {program['예상평점']:.2f}")
