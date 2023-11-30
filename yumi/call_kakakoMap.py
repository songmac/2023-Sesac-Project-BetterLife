from PyKakao import Local
from dotenv import load_dotenv
import sys
#상위 디렉토리에서 모듈을 불려오기 위한 경로 지정
sys.path.append("D:/2023-Sesac-Project-BeLife/module/")
import csvfile
import os
import numpy as np
import pandas as pd

#excel 파일 불려오기
excelFile = 'langchain_facility_info'
saveFile = 'langchain_facility_info'
excelPath = './yumi/'

#load .env
load_dotenv()
kakao_api_key = os.environ.get('KAKAO_API_KEY')

#주소 들고 오기
def getOldAddress(keyword) :
    api = Local(service_key = kakao_api_key)
    try:
        df = api.search_keyword(keyword, dataframe=True)
        return df['address_name'][0]
    except:
        return '주소없음'

#좌표(x,y) 들고 오기
# 좌표(x, y) 가져오기
def getCoordinate(keyword):
    api = Local(service_key=kakao_api_key)
    df = api.search_keyword(keyword, dataframe=True)
    x = df['x'].iloc[0]
    y = df['y'].iloc[0]
    print(f"API 호출 결과 - 주소: {keyword}, x: {x}, y: {y}")
    return x, y

#csv file 불려오기
rawData = csvfile.getCSVFile(excelPath, excelFile)

rawData[['x', 'y']] = rawData['지번주소'].apply(lambda x: getCoordinate(x) if x is not None else (None, None)).apply(pd.Series)
print(rawData[['x', 'y']])

#위도, 경도값 저장
csvfile.saveFile(rawData, excelPath, saveFile)

#dataNum = rawData['시설명'].count()
#print(dataNum)



#시설명 키워드로 지번 주소 들고오기
#rawData['지번주소'] = rawData['시설명'].apply(getOldAddress)
#시설명 키워드로 지번 주소 들고오기
#rawData['좌표'] = rawData['지번주소'].apply(getOldAddress)

# for index in range(0, dataNum + 1) :
#     rawData[['x', 'y']]  = rawData['지번주소'].apply(lambda x: getCoordinate(x) if x is not None else '위도,경도없음')
#     rawData[['x', 'y']] [index]
   #rawData['지번주소'][index] = np.where(name is not None, getNewAddress(name), '주소없음')
   # print(rawData['시설명'][index])
   # print(getNewAddress(rawData['시설명'][index]))
   # print(rawData['지번주소'][index])
#    coordainate_name.append(getCoordinate(rawData[['x', 'y']][index]))
