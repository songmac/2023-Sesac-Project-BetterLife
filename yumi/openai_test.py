#메세지를 동적으로 받았을때 openai
import os, re
from dotenv import load_dotenv
import panel as pn
import time

import openai

#openai 설정 키값 들고 오기
load_dotenv()
api_key = os.environ.get('OPENAI_API_KEY')

#openai api key 설정
openai.api_key = api_key
program = "수영"
location = "광진문화예술회관"
business_hour = "오전6시 ~ 오후 10시"

prompt= input("입력하세요 :" )

response = openai.chat.completions.create(
        model= "gpt-3.5-turbo-0613",
        messages=[
            {'role':'system',
            'content':"""
            너는 사용자에게 적합한 운동프로그램을 추천하기 위한 챗봇이야
            모든 질문에 답변을 다 받으면 
            프로그램명 {program}
            위치 {location}
            시간 {business_hour} 에 해당하는 정보만으로 사용자에게 말하듯이 말해줘
            """
            }  
        ],
        temperature = 0,
        max_tokens = 500, #최대 토큰값
)
print(response.choices[0].message.content)