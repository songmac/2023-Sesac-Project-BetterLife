import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import GridSearchCV 
import joblib
import time
from mfsvd_dataset import generate_user_info_and_reviews


def load_data_and_train_svd_model(file_path):
    # 데이터 로드 및 SVD 모델 훈련 함수
    exercise_review_data_df = pd.read_csv(file_path, encoding='utf-8')
    model_df = exercise_review_data_df[['사용자ID', '운동프로그램', '가중평균만족도']]
    reader = Reader(rating_scale=(0.0, 5.0))
    data = Dataset.load_from_df(model_df, reader)

    start_time = time.time()

    param_grid = {
        'n_epochs': [20, 40],
        'n_factors': [50, 100, 150, 200, 250],
        'lr_all': [0.002, 0.005, 0.007],
        'reg_all': [0.02, 0.05, 0.1]
    }
    grid_search = GridSearchCV(SVD, param_grid=param_grid, measures=['rmse', 'mae'], cv=5)
    grid_search.fit(data)

    best_params = grid_search.best_params['rmse']
    algo = SVD(**best_params)
    trainset = data.build_full_trainset()
    algo.fit(trainset)

    joblib.dump(algo, 'svd_model.pkl')

    end_time = time.time()
    elapsed_time = end_time - start_time

    # RMSE와 MSE 값을 출력
    print("Grid Search 최적의 매개변수:", best_params)
    print("RMSE: {:.4f}".format(grid_search.best_score['rmse']))
    print("MSE: {:.4f}".format(grid_search.best_score['mae']))
    print("학습에 걸린 시간: {:.2f}초".format(elapsed_time))

    # 학습 데이터셋 개수를 출력
    trainset_len = sum(1 for _ in trainset.all_ratings())
    print("학습 데이터셋 개수:", trainset_len)

    return algo


# 기존 데이터셋에서 최대 사용자 ID 찾기
def find_max_user_id(file_path):
    exercise_review_data_df = pd.read_csv(file_path, encoding='utf-8')
    max_user_id = exercise_review_data_df['사용자ID'].max()
    return max_user_id





def predict_program_rating(algo, user_program_pair):
    """
    개별 프로그램에 대한 사용자 평점 예측
    - algo: 학습된 모델
    - user_program_pair: 사용자와 프로그램명 쌍
    """
    user_id, program_name = user_program_pair
    prediction = algo.predict(user_id, program_name)
    return {'프로그램명': program_name, '예상평점': prediction.est}


def get_top_programs(algo, user_id, num_programs):
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
    predictions = [predict_program_rating(algo, pair) for pair in test_data]

    # 예상 평점에 따라 정렬
    predicted_programs = sorted(predictions, key=lambda x: x['예상평점'], reverse=True)
    return predicted_programs


def integrated_model_update_and_recommendation(num_users_to_generate, file_path, algo):
    max_user_id = find_max_user_id(file_path)
    start_user_id = max_user_id + 1  # 새로운 사용자 ID 시작점 설정
    generated_data = generate_user_info_and_reviews(start_user_id, num_users_to_generate, 1, 5)
    # print(generated_data)

    exercise_review_data_df = pd.read_csv(file_path, encoding='utf-8')
    updated_data_df = pd.concat([exercise_review_data_df, generated_data[['사용자ID', '운동프로그램', '가중평균만족도']]])

    reader = Reader(rating_scale=(0.0, 5.0))
    data = Dataset.load_from_df(updated_data_df[['사용자ID', '운동프로그램', '가중평균만족도']], reader)
    trainset = data.build_full_trainset()
    algo.fit(trainset)
    joblib.dump(algo, 'svd_model_updated.pkl')

    for user_id in generated_data['사용자ID'].unique():
        output_str = ""
        output_str += f"사용자ID: {user_id}, " 

        top_programs = get_top_programs(algo, user_id, 3)
        output_str += f"추천 프로그램: " 
        for program in top_programs:
            output_str += f"{program['프로그램명']}; "
            # output_str += f"추천 프로그램: {program['프로그램명']}(예상 평점: {program['예상평점']:.1f}); "
        print(output_str)


# 주요 실행 부분
file_path = 'C:/Users/User/project/SESAC/2023-Sesac-Project-BeLife/data/exercise_reviews_dataset.csv'
num_users_to_generate = 1

algo = load_data_and_train_svd_model(file_path)
integrated_model_update_and_recommendation(num_users_to_generate, file_path, algo)