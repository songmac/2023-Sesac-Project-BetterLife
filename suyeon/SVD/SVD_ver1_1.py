import pandas as pd
import numpy as np
import chardet  # Don't forget to import chardet
from surprise import SVD, Dataset, Reader, accuracy
from surprise.model_selection import train_test_split, cross_validate, GridSearchCV
import time

exercise_review_data_path = r'C:\Users\User\project\SESAC\2023-Sesac-Project-BeLife\data\exercise_review_data_1000.csv'
model_df_path = r'C:\Users\User\project\SESAC\2023-Sesac-Project-BeLife\data\model_df.csv'

# 파일 인코딩 자동 감지
with open(exercise_review_data_path, 'rb') as f:
    result_f = chardet.detect(f.read())

encoding = result_f['encoding']

# 데이터 불러오기
exercise_review_data_df = pd.read_csv(exercise_review_data_path, encoding=encoding)

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
# n_factor depth에 따른 RMSE 확인
param_list = [10, 50, 100, 150, 200]
rmse_list_by_factors = []
ttime_list_by_factors = []

for n in param_list:
    train_start = time.time()
    algo = SVD(n_factors=n)
    algo.fit(trainset)
    train_end = time.time()
    print("모델 훈련 시간: %.2f 초" % (train_end - train_start))
    print(f"SVD 모델의 테스트 데이터셋 RMSE, n_factors={n}")

    # 모델 평가
    predictions = algo.test(testset)
    rmse_list_by_factors.append(accuracy.mse(predictions))
    ttime_list_by_factors.append(train_end - train_start)
    print("-" * 20)

print("n_factors 탐색 완료.")

# Cross-validation
merge_df = pd.read_csv(merge_df_path)
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(merge_df[["사용자", "프로그램명", "평점"]], reader=reader)

algo = SVD(n_factors=50, random_state=42)
cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

# Grid Search
param_grid = {'n_epochs':[20,40], 'n_factors':[50, 100, 200]}
grid = GridSearchCV(SVD, param_grid=param_grid, measures=['rmse', 'mae'], cv=3)
grid.fit(data)

print(grid.best_score['rmse'])
print(grid.best_params['rmse'])

# 예측할 부분 (rating이 없는) 데이터만 추출
test_data = testset
predictions = algo.test(test_data)

# test 평가를 위해 선택하지 않은 프로그램의 예상 점수를 dictionary 형태로 추출
estimated_unselected_dict = {}

for uid, iid, _, predicted_rating, _ in predictions:
    if uid in estimated_unselected_dict:
        estimated_unselected_dict[uid].append((iid, predicted_rating))
    else:
        estimated_unselected_dict[uid] = [(iid, predicted_rating)]

print('prediction type: ', type(predictions),
      'size ', len(predictions))
print()
print('pridictions 결과값 3개 미리보기')
result = [(pred.uid, pred.iid, pred.est) for pred in predictions[:3]]
print(result)

# 예측 결과에서 프로그램명(pred.iid)을 배열에 저장
predicted_programs = [pred.iid for pred in predictions]

# 저장된 배열의 일부만 출력
print("예측된 프로그램명 배열 일부:")
print(predicted_programs[:3])  # 3개만 출력
