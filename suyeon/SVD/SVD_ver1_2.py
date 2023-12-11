import pandas as pd
import numpy as np
from surprise import SVD, Dataset, Reader, accuracy
from surprise.model_selection import train_test_split, GridSearchCV
import joblib

def create_svd_model(data):
    algo = SVD(n_factors=50, random_state=42)
    trainset = data.build_full_trainset()
    algo.fit(trainset)
    return algo

def predict_program_rating(algo, user_id, program_name):
    prediction = algo.predict(user_id, program_name)
    return prediction.est

def get_top_programs(algo, user_id, num_programs=3):
    # 예측할 부분 (rating이 없는) 데이터만 추출
    test_data = pd.DataFrame({'사용자': [user_id] * num_programs,
                              '프로그램명': [f"프로그램_{i}" for i in range(1, num_programs + 1)]})

    predictions = [algo.predict(row['사용자'], row['프로그램명']) for _, row in test_data.iterrows()]

    # 예측 결과에서 프로그램명(pred.iid)을 배열에 저장
    predicted_programs = [{'프로그램명': pred.iid, '예상평점': pred.est} for pred in predictions]

    # 평점에 따라 정렬
    predicted_programs = sorted(predicted_programs, key=lambda x: x['예상평점'], reverse=True)

    return predicted_programs

def update_model_with_new_data(algo, new_data):
    # 기존 데이터에 새로운 데이터 추가
    algo_data = algo.trainset.build_testset() + [(user, item, rating) for user, item, rating in new_data.itertuples(index=False)]
    
    # 모델 재학습
    algo.fit(algo_data)

    # 모델 저장
    model_filename = 'svd_model.pkl'
    joblib.dump(algo, model_filename)

import pandas as pd
import numpy as np
from surprise import Dataset, Reader, SVD, train_test_split, GridSearchCV

def process_and_train_svd_model(file_path):
    # 데이터 불러오기 (UTF-8 인코딩 사용)
    exercise_review_data_df = pd.read_csv(file_path, encoding='utf-8')

    # 테이블 생성
    model_df = pd.DataFrame({
        '사용자': np.repeat(exercise_review_data_df['사용자ID'], len(exercise_review_data_df)),
        '프로그램명': np.tile(exercise_review_data_df['운동프로그램'].tolist(), len(exercise_review_data_df)),
        '평점': np.tile(exercise_review_data_df['만족도'].tolist(), len(exercise_review_data_df))
    })

    # Reader, Dataset 오브젝트로 학습용 데이터셋 생성 및 분리
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(model_df[["사용자", "프로그램명", "평점"]], reader)
    trainset, testset = train_test_split(data, test_size=0.25)

    # Grid Search
    param_grid = {'n_epochs': [20, 40], 'n_factors': [50, 100, 200]}
    grid = GridSearchCV(SVD, param_grid=param_grid, measures=['rmse', 'mae'], cv=3)
    grid.fit(data)

    print(f"Best RMSE: {grid.best_score['rmse']}")
    print(f"Best parameters: {grid.best_params['rmse']}")

    # 최적의 n_factors 값 출력
    best_n_factors = grid.best_params['rmse']['n_factors']
    print(f"Best n_factors: {best_n_factors}")

    return grid.best_params['rmse']


file_path = r'C:\Users\User\project\SESAC\2023-Sesac-Project-BeLife\data\exercise_review_data_1000.csv'
best_params = process_and_train_svd_model(file_path)



def process_new_data_and_update_model(algo, new_data_values, update_model_with_new_data, predict_program_rating, get_top_programs):
    # 새로운 데이터 생성
    new_data_columns = ['사용자ID','연령대','장애유무','선호지역','운동목표','선호운동','선호시간대','선호빈도','중요항목','리뷰ID','운동프로그램','만족도']
    new_data = pd.DataFrame(data=new_data_values, columns=new_data_columns)

    # 모델 업데이트
    update_model_with_new_data(algo, new_data)

    # 사용자 입력값 예외 처리 없이 사용자에게 새로운 예측 수행
    prediction = predict_program_rating(algo, new_data_values[0], new_data_values[10])
    print(f"사용자 {new_data_values[0]}가 프로그램 '{new_data_values[10]}'에 대한 예상 평점은 {prediction:.2f}입니다.")

    # 사용자에게 새로운 추천 프로그램 출력
    top_programs = get_top_programs(algo, new_data_values[0])
    print(f"\n사용자 {new_data_values[0]}에게 추천하는 프로그램 상위 3개:")
    for program in top_programs:
        print(f"{program['프로그램명']}: 예상 평점 {program['예상평점']:.2f}")

    return top_programs


new_data_values = [
    ['1001','학생','무','양천구 신월제2동','무관','구기및라켓','오전','주1회','선호지역','1_5','요가_하타','1']
    # 다른 데이터도 추가 가능
]

top_programs = process_new_data_and_update_model(algo, new_data_values, update_model_with_new_data, predict_program_rating, get_top_programs)
