import sys
#상위 디렉토리에서 모듈을 들고 오기 위해 경로 지정
sys.path.append("D:/2023-Sesac-Project-BetterLife/module/")
import csvfile
import pandas as pd

rawPath = './data/'
rawName = 'mandatory_seoul_program_oldAddr_231114'
savePath = './data/'
saveName = 'public_facility_seoul'
 
rawdata = csvfile.getCSVFile(rawPath, rawName)

#필요없는 시설명 제외(어린이집, 요양원, 초등학교, 돌봄, 경로당, 데이케어)한 행만 출력
rawdata = rawdata[~rawdata['시설명'].str.contains('어린이집|요양원|초등학교|돌봄|경로당|데이|케어|복지관|교회|유치원|복지센터|어르신|헬스장|배드민턴장|보건소|치매안심센터|아파트|양로원|보호센터|주민센터|키움센터|보육원|롯데캐슬|자치회관', na=False, case=False)]
print(rawdata.shape)
rawdata = rawdata[~rawdata['시설명'].isnull()]
#print(rawdata['시설명'].isnull().sum())
print(rawdata.shape)
csvfile.saveFile(rawdata, savePath, saveName)
