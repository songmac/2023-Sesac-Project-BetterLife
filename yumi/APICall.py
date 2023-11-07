import requests
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime

#load .env
load_dotenv()
api_key = os.environ.get('SEOUL_API_KEY')

#서울 운동 프로그램 url : 전체 데이터 개수를 들고 오기 위함
init_url = 'http://openapi.seoul.go.kr:8088/{}/json/ListProgramByPublicSportsFacilitiesService/1/10/'.format(api_key)
response = requests.get(init_url)
data = response.json()
#서비스 이름 추출
serviceName = init_url.split('/')[5]

#해당하는 서비스 전체 데이터 개수
items_cnt = data['ListProgramByPublicSportsFacilitiesService']['list_total_count']

#서울 공공 데이터는 최대 1000건까지 가능
start = 1

#전체 데이터 list
all_items = []
while True : 
    end = (start + 1000) -1
    servcie_url = 'http://openapi.seoul.go.kr:8088/{}/json/{}/{}/{}/'.format(api_key, serviceName, start, end)
    print(servcie_url)
    service_res = requests.get(servcie_url)
    service_data = service_res.json()
    #print(service_data)
    #서비스 이름 들고 오기 
    items = service_data[serviceName]['row']
    #json Key value
    #print(json['ListProgramByPublicSportsFacilitiesService'].keys())

    all_items.extend(items)
    start += 1000
        
    if end > items_cnt :
       break

#json 데이터 dataframe으로 만들기 
df_item = pd.DataFrame(items)
#오늘 날짜
today = datetime.now().strftime('%y%m%d')
print(today)
#파일로 저장
df_item.to_csv('./data/seoul_exercise_programs_'+ today +'_.csv', encoding='utf-8-sig', index=False)