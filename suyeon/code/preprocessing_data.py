import pandas as pd
import numpy as np
import sys
#상위 디렉토리에서 모듈을 들고 오기 위해 경로 지정
sys.path.append("C:/Users/User/project/SESAC/2023-Sesac-Project-BetterLife/module/")
import csvfile


datafilePath = './data/' #파일 들고 오기
datafileName = 'merge_all_seoul_program' #모든 프로그램 엑셀 파일 
savefilePath = './data/' #저장 경로
savefileName = 'mandatory_seoul_program' #저장파일명
 

#allProgramsDf = csvfile.call_csv(datafilePath, datafileName)

allProgramsDf = pd.read_csv(datafilePath + datafileName + '.csv' ) #파일 불러오기
print("테이블 정보 : ", allProgramsDf.shape) #원본 파일 테이블 정보


allProgramsDf = allProgramsDf.drop('주소', axis=1) #주소가 모두 값이 blank로 삭제
print("결측값 개수 : ", allProgramsDf.isnull().sum()) #원본 파일 결측값 개수 


allPrograms = allProgramsDf.dropna(axis=0) #원본 파일에 결측값이 있으면 행전체 삭제 
print("원본 결측지 제거 후 :",  allPrograms.shape) #원본 파일의 결측값 제거 후 개수


mandatoryPrograms = allProgramsDf[['시설명','종목명','프로그램명','대상','요일','시간','시설주소']] #필수적인 항목만 추출
print("필수항목 결측값 개수", mandatoryPrograms.isnull().sum()) #필수적인 항목만 결측값 개수 
print("필수항목 결측값 제거후 개수", mandatoryPrograms.dropna(axis=0).shape) #필수항목 결측값 제거 후 개수


mandatoryPrograms.to_csv(savefilePath + savefileName + '.csv' , encoding='utf-8-sig', index=False)