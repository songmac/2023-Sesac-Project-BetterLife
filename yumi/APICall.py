# %%
import requests
import pandas as pd
from dotenv import load_dotenv
import os
import json

#load .env
load_dotenv()

api_key = os.environ.get('SEOUL_API_KEY')
#서울 운동 프로그램 url
url = 'http://openapi.seoul.go.kr:8088/'+api_key+'/json/ListProgramByPublicSportsFacilitiesService/1/1000/'
#response = requests.get(url)
json = requests.get(url).json()

json['ListProgramByPublicSportsFacilitiesService'].keys()

json['ListProgramByPublicSportsFacilitiesService']['list_total_count']




# %%
