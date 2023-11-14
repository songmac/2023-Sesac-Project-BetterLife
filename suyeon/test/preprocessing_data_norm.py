import pandas as pd
import numpy as np
import sys
#상위 디렉토리에서 모듈을 들고 오기 위해 경로 지정
sys.path.append("C:/Users/User/project/SESAC/2023-Sesac-Project-BeLife/module/")
import csvfile


datafilePath = './data/' #파일 들고 오기
datafileName = 'mandatory_seoul_program' #모든 프로그램 엑셀 파일 
 

manProgramsDf = pd.read_csv(datafilePath + datafileName + '.csv' ) #파일 불러오기
# print("테이블 : ", manProgramsDf) #원본 파일 테이블 정보
# print("테이블 정보 : ", manProgramsDf.shape) #원본 파일 테이블 정보 (17231, 7)

df = pd.DataFrame(manProgramsDf)

df_dd = df.drop_duplicates(['시설명']) #['시설명','종목명','프로그램명','대상','요일','시간','시설주소']