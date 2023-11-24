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

#chat gpt 호출하기 : gpt-3.5-turbo
def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0, max_tokens=500):
    response = openai.chat.completions.create(
        model= model,
        messages = messages,
        temperature = temperature,
        max_tokens = max_tokens, #최대 토큰값
        stop= ["종료", "나가기"] #종료값
    )
    return response.choices[0].message.content


#openai에 학습할 내용
context = [
 {'role':'system',
     'content':"""
      너는 사용자에게 적합한 운동프로그램을 추천하기 위한 챗봇이야 
      해당하는 값을 넣어서     
      프로그램명 {program}
      위치 {location}
      시간 {business_hour}을 정보 기준으로 사용자에게 말하듯이 말해줘
    """
    }  
]

program = "수영"
location = "광진문화예술회관"
business_hour = "오전6시 ~ 오후 10시"

#user_input = [] #모델링 input값으로 넣기 위해 사용자 입력값 저장
def collect_messages(_):
    prompt = inp.value_input
    inp.value = '' #사용자 입력 초기화
    start_time = time.time()
    context[-1]['content'] = context[-1]['content'].format(
    program=program, location=location, business_hour=business_hour
    )
    #user_input.append(prompt)
    #openai 응답값
    response = get_completion_from_messages(context)
    context.append({'role':'system', 'content':f"{response}"})
    end_time = time.time()
    print("respose time : ", end_time - start_time)
    #화면에 보여주기
    panels.append(pn.Row('나:', pn.pane.Markdown(prompt, width=600)))
    panels.append(pn.Row('나의운동코치:', pn.pane.Markdown(response, width=600, styles={'background-color': '#f0fcd4'})))
    return pn.Column(*panels)

pn.extension()

#디스플레이를 위한 패널
panels = [] 

#챗봇 input버튼
inp = pn.widgets.TextInput(value="안녕하세요", placeholder='답변을 입력해주세요')
button_conversation = pn.widgets.Button(name="입력")
interactive_conversation = pn.bind(collect_messages, button_conversation)
dashboard = pn.Column(
    inp,
    pn.Row(button_conversation),
    pn.panel(interactive_conversation, loading_indicator=True),
)
#대쉬보드 출력
dashboard.show()


