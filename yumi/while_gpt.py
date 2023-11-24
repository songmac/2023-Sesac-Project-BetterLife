import os, re
from dotenv import load_dotenv
import panel as pn
import time

import openai

#openai 설정 키값 들고 오기
load_dotenv()
api_key = os.environ.get('OPENAI_API_KEY')

user_input = "안녕!!"

i = 0
while True:
    if i == 0:
        question = "안녕"
    else : 
        question = input("Q:")

    if question == '종료' or question == 'exit':
        break

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", 
             "content": 
                """너는 사용자에게 적합한 운동프로그램을 추천하기 위한 챗봇이야
                   사용자에게 먼저 인사를 하고, 해당하는 질문 3개야
                   아래 해당하는 질문에 모든 답변만 받아줘

                   질문을 순서대로 사용자에게 한개씩 해줘

                   질문1 : 나이가 어떻게 되나요?
                   질문2 : 거주지가 어떻게 되나요? (예시 : 중구 회현동) """},
            {"role": "user", "content": question},
        ]
    )
    
    i += 1

    print(response.choices[0].message.content)