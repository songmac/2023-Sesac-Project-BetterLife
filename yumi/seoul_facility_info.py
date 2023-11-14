import pandas as pd
import numpy as np

facility_info_df = pd.read_csv('./data/rawdata/서울시_공공체육시설_정보.csv', encoding='cp949')

program_df = pd.read_csv('./data/program.csv')

print(facility_info_df.shape)
print(program_df.shape)

#시설명, 시설주소, 연락처, 홈페이지
facility_info = facility_info_df[['시설명','시설주소','연락처','홈페이지']]

facility_name = facility_info_df['시설명']

#dataframe merge시키기 

df_merge = pd.merge(program_df, facility_info, how ='left')


#df_merge.to_csv('./data/merge_seoul_program.csv', mode='w', encoding='utf-8-sig', index=False)

print(df_merge.shape)

print(df_merge['시설주소'].isnull().sum())



