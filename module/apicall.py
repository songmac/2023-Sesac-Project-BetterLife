import os
from dotenv import load_dotenv
import requests
import pandas as pd
import math
from PyKakao import Local

#API 데이터 불려오는 모듈

#load .env
load_dotenv()
api_key = os.environ.get('SEOUL_API_KEY')

#API로 서울 운동 프로그램 데이터를 호출하는 함수
def call_seoul_execise_program() :
    #서울 운동 프로그램 url : 전체 데이터 개수를 들고 오기 위함
    init_url = 'http://openapi.seoul.go.kr:8088/{}/json/ListProgramByPublicSportsFacilitiesService/1/10/'.format(api_key)
    response = requests.get(init_url)
    data = response.json()
    #서비스 이름 추출
    serviceName = init_url.split('/')[5]

    #해당하는 서비스 전체 데이터 개수
    total_cnt = data['ListProgramByPublicSportsFacilitiesService']['list_total_count']
    print(total_cnt)

    #excel 항목에 넣을 list
    center_names = []
    programs = []
    subjects = []
    terms = []
    weeks = []
    class_times = []
    class_fees = []
    programs_desc = []
    class_capacities = []

    for i in range(1, math.ceil(total_cnt/1000) + 1) :
        #서울 공공 데이터는 최대 1000건까지 가능
        end = i * 1000
        start = end - 1000 + 1

        if end > total_cnt :
            end = total_cnt

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

        #해당하는 항목만 출력
        for item in items :
            center_names.append(item['CENTER_NAME'])
            programs.append(item['PROGRAM_NAME'])
            subjects.append(item['SUBJECT_NAME'])
            terms.append(item['TERM'])
            weeks.append(item['WEEK'])
            class_times.append(item['CLASS_TIME'])
            class_fees.append(item['FEE'])
            programs_desc.append(item['INTRO'])
            class_capacities.append(item['CAPACITY'])

    #json 데이터 dataframe으로 만들기 
    df_item = pd.DataFrame({'시설명' : center_names, '프로그램명' : programs, '종목명' : subjects, '기간' : terms, '요일': weeks, 
                            '진행시간(1회)' : class_times, '수업료' : class_fees, '프로그램 소개' : programs_desc, '전체정원수' : class_capacities})
    return df_item

#카카오 지도 API 들고 오기 
