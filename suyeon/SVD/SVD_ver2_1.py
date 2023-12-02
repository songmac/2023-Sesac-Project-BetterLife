# 수정된 내용:
# ratings_file: 사용자의 선호도 평점이 있는 파일
# programs_file: 운동 프로그램 정보가 있는 파일

import pandas as pd
from surprise.dataset import DatasetAutoFolds
from surprise.dataset import Reader
from surprise import SVD

def get_unseen_programs(ratings, programs, user_id):
    # 특정 사용자가 본 exerciseId들을 리스트로 추출
    seen_programs = ratings[ratings['userId'] == user_id]['exerciseId'].tolist()
    # 모든 운동 프로그램들의 exerciseId들 리스트로 할당
    total_programs = programs['exerciseId'].tolist()
    # 특정 사용자가 본 exerciseId들을 제외한 나머지 추출
    unseen_programs = [program for program in total_programs if program not in seen_programs]
    return unseen_programs

def recommend_programs(algorithm, user_id, unseen_programs, top_n=10):
    # 알고리즘 객체의 predict()를 이용해 특정 user_id의 평점이 없는 운동 프로그램에 대해 평점 예측
    predictions = [algorithm.predict(str(user_id), str(exercise_id)) for exercise_id in unseen_programs]

    # predictions는 Prediction()으로 하나의 객체로 되어있기 때문에 예측 평점(est값)을 기준으로 정렬해야 함
    predictions.sort(key=lambda pred: pred.est, reverse=True)

    # 상위 top_n개의 예측값들만 추출
    top_predictions = predictions[:top_n]

    # top_predictions의 exerciseId, rating, program_name을 각각 추출
    top_program_ids = [int(pred.iid) for pred in top_predictions]
    top_program_ratings = [pred.est for pred in top_predictions]
    top_program_names = programs[programs['exerciseId'].isin(top_program_ids)]['program_name']

    # 위 3가지를 튜플로 담기
    top_program_preds = [(id, rating, name) for id, rating, name in zip(top_program_ids, top_program_ratings, top_program_names)]
    return top_program_preds

# 파일 경로 설정
ratings_file = '운동_선호도_평점.csv'
programs_file = '운동_프로그램.csv'

# Reader 객체 생성
reader = Reader(line_format='user item rating timestamp', sep=',', rating_scale=(0.5, 5))

# surprise dataset 파일 기반
data_folds = DatasetAutoFolds(ratings_file=ratings_file, reader=reader)

# 개별적으로 생성한 csv 파일 기반
trainset = data_folds.build_full_trainset()
algo = SVD(n_factors=50, n_epochs=20, random_state=42)
algo.fit(trainset)

# 운동 프로그램에 대한 정보 데이터 로딩
exercise_programs = pd.read_csv(programs_file)
exercise_ratings = pd.read_csv(ratings_file)

# 특정 사용자의 운동 프로그램 추천
unseen_list = get_unseen_programs(exercise_ratings, exercise_programs, user_id=9)
top_programs_preds = recommend_programs(algo, user_id=9, unseen_programs=unseen_list, top_n=10)

# 결과 출력
print('#' * 8, 'Top-10 추천 운동 프로그램 리스트', '#' * 8)
for top_program in top_programs_preds:
    print('* 추천 운동 프로그램 이름:', top_program[2])
    print('* 해당 프로그램의 예측 평점:', top_program[1])
    print()