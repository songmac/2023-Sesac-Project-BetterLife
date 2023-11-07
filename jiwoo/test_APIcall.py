#%% 
from dotenv import load_dotenv
import requests
import os
import json
import pandas as pd

load_dotenv()
api_key = os.environ.get('SEOUL_API_KEY')

url = 'http://openapi.seoul.go.kr:8088/'+api_key+'/json/ListProgramByPublicSportsFacilitiesService/1/1000/'
#response = requests.get(url)
json = requests.get(url).json()
json['ListProgramByPublicSportsFacilitiesService'].keys()
print(json)
# %%
