import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_seq_items', None)

df = pd.read_csv('dahee/data/unique_data_code.csv', encoding='cp949')
# print('df: ', df.shape)
# print(df)

# 연령별 dataframe 생성
df_student = df[df['연령']=='청소년']
df_adult = df[df['연령']=='성인']
df_elderly= df[df['연령']=='노인']

# 인코딩 후 csv 파일로 저장
df_student.to_csv('dahee/data/df_student.csv', mode='w', encoding='cp949', index=False)
df_adult.to_csv('dahee/data/df_adult.csv', mode='w', encoding='cp949', index=False)
df_elderly.to_csv('dahee/data/df_elderly.csv', mode='w', encoding='cp949', index=False)


# 중복되지 않는 데이터 종류 개수 확인
# print(df.nunique())

# # 중복값 제거
# df_unique = df.drop_duplicates()
# df_unique = df_unique.reset_index(drop=True)
# print('unique: ', df_unique.shape)

# print(df)
# print(df.head())

# 열 삭제
# df = df.iloc[:, :10]
# print(df.head())


# # 시설명이 '강낭구민체육관'인 지번주소 변경
# df.loc[df['시설명'] == '강남구민체육관', '지번주소'] = '서울 강남구 개포동 271'

# print(df.head())


