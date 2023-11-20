import sys
#상위 디렉토리에서 모듈을 들고 오기 위해 경로 지정
sys.path.append("D:/2023-Sesac-Project-BetterLife/module/")
import apicall, csvfile
from tabulate import tabulate

saveFilePath = './data/'
saveFileName = 'seoul_execise_program'

#print(sys.path)
api_data = apicall.call_seoul_execise_program()
#print(tabulate(df, headers = 'keys',tablefmt='fancy_outline'))

#csv로 저장
csvfile.save_file(api_data, saveFilePath, saveFileName)
