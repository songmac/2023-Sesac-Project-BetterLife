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
    )
    return response.choices[0].message.content

#openai에 학습할 내용
context = [
 {'role':'system',
     'content':"""
      너는 사용자에게 적합한 운동프로그램을 추천하기 위한 챗봇이야
      사용자에게 먼저 인사를 하고, 해당하는 질문 3개야
      아래 해당하는 질문에 모든 답변만 받아줘

      질문을 순서대로 사용자에게 한개씩 해줘

      - 나이가 어떻게 되나요?
      - 거주지가 어떻게 되나요? (예시 : 중구 회현동)
      - 운동 목표를 골라주세요. (1: 체력단련, 2: 심폐기능단련)
    """
    }  
]

#챗봇 질문 및 답변 저장하기 
user_input = [] #모델링 input값으로 넣기 위해 사용자 입력값 저장
#챗봇이 사용자가 먼저 입력을 하지 않으면 챗봇이 반응을 하지 않으므로, 
#사용자가 default 값으로 안녕하세요로 시작하게 만들기 위함
inital_start = 0
def collect_messages(_):
    global inital_start
    if inital_start == 0 :
        prompt = "안녕하세요"
        inp.value = ""
    else : 
        prompt = inp.value_input
        inp.value = ""
    start_time = time.time()
    #사용자 content 입력
    context.append({'role':'user', 'content':f"{prompt}"})
    user_input.append(prompt)
    #openai 응답값
    response = get_completion_from_messages(context)
    context.append({'role':'system', 'content':f"{response}"})
    end_time = time.time()
    print("respose time : ", end_time - start_time)
    #화면에 보여주기
    panels.append(pn.Row('나:', pn.pane.Markdown(prompt, width=600)))
    panels.append(pn.Row('나의운동코치:', pn.pane.Markdown(response, width=600, styles={'background-color': '#f0fcd4'})))
    inital_start += 1

    if "종료" in prompt:
        return pn.Column("채팅이 이미 종료되었습니다.")
    
    return pn.Column(*panels)

#-----------------------------------------------------------------------#
#챗봇화면 만들기 
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