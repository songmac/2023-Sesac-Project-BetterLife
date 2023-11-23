import pandas as pd
import os
from datetime import datetime

#cvs file처리하는 모듈

#수집한 날짜를 알기 위해 추가
today = datetime.now().strftime('%y%m%d')

#불려온 cvs 파일을 dataframe으로 리턴   
def getCSVFile(dirpath, fileName):
    fileName = dirpath + fileName + '.csv'
    df = pd.read_csv(fileName)
    return df

#csv 파일 저장
def saveFile(df, dirpath, fileName) :
    df.to_csv(dirpath + fileName + '_' + today + '.csv' , encoding='utf-8-sig', index=False)

#csv 파일 병합
def merge_csv(dirpath, savefile, fileName):
    merge_df = pd.DataFrame()
    file_list = os.listdir(dirpath)
    for file in file_list :
        df = pd.read_csv(dirpath + file, sep=",", dtype='object')
        print(df.shape)
        merge_df = merge_df._append(df)
    
    #동일한 폴더에 병합한 csv 파일 저장
    return merge_df.to_csv(savefile + fileName + '_' + today + ".csv", index=False, encoding='utf-8-sig')