import pandas as pd
import os
from datetime import datetime

#cvs file처리하는 모듈

#수집한 날짜를 알기 위해 추가
today = datetime.now().strftime('%y%m%d')

#불려온 cvs 파일을 dataframe으로 리턴   
def call_csv(dirpath, fileName):
    merged_file = dirpath + fileName + '.csv'
    df = pd.read_csv(merged_file)
    return df

#csv 파일 저장
def save_file(df, dirpath, fileName) :
    df.to_csv(dirpath + fileName + '_' + today + '.csv' , encoding='utf-8-sig', index=False)