from PyKakao import Local
from dotenv import load_dotenv
import sys
#상위 디렉토리에서 모듈을 불려오기룰 위한 경로 지정
sys.path.append("D:/2023-Sesac-Project-BetterLife/module/")
import os, csvfile
import numpy as np

#excel 파일 불려오기 
excelName = 'mandatory_seoul_program'
saveName = 'mandatory_seoul_program_oldAddr'
excelPath = './data/'

#load .env
load_dotenv()
rest_api_key = os.environ.get('REST_API_KEY')

#주소 들고 오기
def getNewAddress(keyword) :
    api = Local(service_key = rest_api_key)
    try:
        df = api.search_keyword(keyword, dataframe=True)
        return df['address_name'][0]
    except:
        return '주소없음'

#좌표(x,y) 들고 오기
def getCoordinate(keyword) :
    api = Local(service_key = rest_api_key)
    df = api.search_keyword(keyword, dataframe=True)
    return df[['x','y']].iloc[0]

#csv file 불려오기
rawData = csvfile.getCSVFile(excelPath, excelName)

dataNum = rawData['시설명'].count()

#시설명 키워드로 지번 주소 들고오기
rawData['지번주소'] = rawData['시설명'].apply(getNewAddress)

#지번주소값 저장
csvfile.saveFile(rawData, excelPath, saveName)

# for index in range(0, dataNum + 1) :
#rawData['지번주소'] = rawData['시설명'].apply(lambda x: getNewAddress(x) if x is not None else '주소없음')
   #rawData['지번주소'][index]
   #rawData['지번주소'][index] = np.where(name is not None, getNewAddress(name), '주소없음')
   #print(rawData['시설명'][index])
  # print(getNewAddress(rawData['시설명'][index]))
#print(rawData['지번주소'][index])
   #buildingName.append(getNewAddress(rawData['시설명'][index]))

#rint(buildingName)
#print(rawData)
   #rawData['구주소'][index] = rawData.apply(lambda x : getNewAddress(rawData['시설명'][index] is not None else '주소없음'))
    #rawData.at[index, '구주소'] = getNewAddress(rawData['시설명']) if rawData['시설명'] is not None else '주소없음'

