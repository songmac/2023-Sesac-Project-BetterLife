import os
from surprise import SVD
from surprise.dataset import DatasetAutoFolds
from surprise import Reader
import pandas as pd
import chardet
import itertools

# 파일 경로 정의
script_directory = os.getcwd()
user_preferences_path = os.path.join(script_directory, 'data', 'user_preferences.csv')
facility_programs_path = os.path.join(script_directory, 'data', 'facility_programs.csv')

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

def load_csv(file_path):
    try:
        encoding = detect_encoding(file_path)
        header = None
        if "code" in pd.read_csv(file_path, encoding=encoding, header=None, nrows=1).values:
            header = 0

        # 파일의 처음 몇 줄을 출력하여 파일 구조 확인
        with open(file_path, 'r', encoding=encoding) as file:
            for _ in range(5):
                print(file.readline().strip())

        # 파일 구조에 기반하여 열 업데이트
        columns = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # 실제 구조에 맞게 업데이트
        return pd.read_csv(file_path, encoding=encoding, header=header, usecols=columns, on_bad_lines='skip', skiprows=[0])
    except UnicodeDecodeError:
        columns = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        return pd.read_csv(file_path, encoding='utf-8', header=header, engine='python', usecols=columns, on_bad_lines='skip', skiprows=[0])


# 두 파일에 대해 load_csv 함수 호출
user_preferences_content = load_csv(user_preferences_path)
facility_programs_content = load_csv(facility_programs_path)

# load_dataset_auto_folds 함수 수정
def load_dataset_auto_folds(ratings_file):
    try:
        reader = Reader(line_format='user item rating timestamp', sep=',', rating_scale=(0.5, 5))
        return DatasetAutoFolds(ratings_file=ratings_file, reader=reader)
    except UnicodeDecodeError as e:
        print("UnicodeDecodeError:", e)
        return None
    except FileNotFoundError as e:
        print("FileNotFoundError:", e)
        return None
    except Exception as e:
        print("An error occurred:", e)
        return None

# exercise_recommendation_system 함수 수정
def exercise_recommendation_system(user_preferences_file, facility_programs_file, user_id=9, top_n=10):
    data_folds = load_dataset_auto_folds(ratings_file=user_preferences_file)

    if data_folds is not None:
        trainset = data_folds.build_full_trainset()
        algo = SVD(n_factors=50, n_epochs=20, random_state=42)
        algo.fit(trainset)

        facility_programs = load_csv(facility_programs_file)
        user_preferences = load_csv(user_preferences_file)

        unseen_list = get_unseen_surprise(user_preferences, facility_programs, user_id)
        top_programs_preds = recomm_program_by_surprise(algo, user_id, unseen_list, top_n)

        print('#' * 8, f'Top-{top_n} 추천 시설 프로그램 리스트', '#' * 8)
        for top_program in top_programs_preds:
            print('* 추천 시설 프로그램 이름:', top_program[2])
            print('* 해당 프로그램의 예측 평점:', top_program[1])
            print()
    else:
        print("데이터셋을 로드하는 중 오류가 발생했습니다.")

# get_unseen_surprise 함수 수정
def get_unseen_surprise(user_preferences, facility_programs, user_id):
    seen_programs = user_preferences[user_preferences['userId'] == user_id]['code'].tolist()
    total_programs = facility_programs['code'].tolist()
    unseen_programs = [program for program in total_programs if program not in seen_programs]
    return unseen_programs

# recomm_program_by_surprise 함수 수정
def recomm_program_by_surprise(algo, user_id, unseen_programs, top_n=10):
    predictions = [algo.predict(str(user_id), str(code)) for code in unseen_programs]

    def sortkey_est(pred):
        return pred.est

    predictions.sort(key=sortkey_est, reverse=True)

    top_predictions = predictions[:top_n]

    top_program_codes = [int(pred.iid) for pred in top_predictions]
    top_program_ratings = [pred.est for pred in top_predictions]
    top_program_names = programs[programs['code'].isin(top_program_codes)]['프로그램명']

    top_program_preds = [(code, rating, name) for code, rating, name in zip(top_program_codes, top_program_ratings, top_program_names)]
    return top_program_preds

# main 함수 수정
def main():
    print("Script Directory:", script_directory)
    print("User Preferences File:", user_preferences_path)
    print("Facility Programs File:", facility_programs_path)

    print("User Preferences File Exists:", os.path.exists(user_preferences_path))
    print("Facility Programs File Exists:", os.path.exists(facility_programs_path))

    user_preferences_content = load_csv(user_preferences_path)
    facility_programs_content = load_csv(facility_programs_path)

    print("User Preferences Content:")
    print(user_preferences_content)

    print("\nFacility Programs Content:")
    print(facility_programs_content)

    exercise_recommendation_system(
        user_preferences_file=user_preferences_path,
        facility_programs_file=facility_programs_path,
        user_id=9,
        top_n=10
    )

# main 함수 호출
if __name__ == "__main__":
    main()
