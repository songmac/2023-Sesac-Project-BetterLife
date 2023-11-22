import os
import panel as pn
import openai
from openai import OpenAI
from dotenv import load_dotenv
import json, requests

#load .env
load_dotenv()
api_key = os.environ.get('OPENAI_API_KEY')

#api key 설정
openai.api_key = api_key

#openai 응답 받기
def get_openai_response(message):
    #openai url 
    openai_url = "https://api.openai.com/v1/engines/davinci/completions"

    #header값
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }
    
    data = {
        "prompt": message
    }
    response = requests.post(openai_url, json=data, headers=headers)

    if response.status_code == 200:
        return response.json()["choices"][0]["text"]
    else:
        return f"Error: {response.status_code}, {response.text}"

#open ai 설정 : gpt-3.5-turbo
def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0, max_tokens=1000):
    response = openai.chat.completions.create(
        model= model,
        messages = messages,
        temperature = temperature,
        max_tokens = max_tokens,
        stop= "종료"
    )
    return response.choices[0].message.content

#openai에 학습할 내용
context = [
    {'role':'assistant',
     'content':"""
      너는 사용자에게 적합한 운동프로그램을 추천하기 위한 챗봇이야
      사용자에게 먼저 인사를 하고, 해당하는 질문 4개야
      아래 해당하는 질문에 모든 답변만 받아줘
      모든 답변을 다 받으면 인사와 함께 챗봇을 종료해줘

      질문을 순서대로 사용자에게 한개씩 해줘

      1. 나이가 어떻게 되나요?
      2. 운동 목표를 골라주세요. (1: 체력단련, 2: 심폐기능단련)
    """
    }
  ]

#챗봇 질문과 사용자 답변 panel 라이브러리를 통해 화면 출력
def collect_messages(_):
    prompt = inp.value_input
    inp.value = ''
    #사용자 content 입력
    context.append({'role':'user', 'content':f"{prompt}"})
    #openai 응답값
    response = get_completion_from_messages(context)
    context.append({'role':'system', 'content':f"{response}"})
    print("context 값 : ", context)
    #화면에 보여주기
    panels.append(
        pn.Row('나:', pn.pane.Markdown(prompt, width=600)))
    panels.append(
        pn.Row('나의운동코치:', pn.pane.Markdown(response, width=600, styles={'background-color': '#f0fcd4'})))
    return pn.Column(*panels)

#챗봇 화면 만들기 
pn.extension()

panels = []

#input 화면
inp = pn.widgets.TextInput(value="안녕하세요!!", placeholder='입력해주세요')
#버튼
button_conversation = pn.widgets.Button(name="입력")
interactive_conversation = pn.bind(collect_messages, button_conversation)
dashboard = pn.Column(
    inp,
    pn.Row(button_conversation),
    pn.panel(interactive_conversation, loading_indicator=True, height=300),
)
#대쉬보드 출력
dashboard.show()
