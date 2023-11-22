import os
import panel as pn
from openai import OpenAI
from dotenv import load_dotenv

#load .env
load_dotenv()
api_key = os.environ.get('OPENAI_API_KEY')

#open ai 설정 : gpt-3.5-turbo
def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = OpenAI.chat.completions.create(
        api_key = api_key,
        model= model,
        messages = messages,
        temperature = temperature
    )
    return response.choices[0].message.content

#챗봇 화면 만들기 
pn.extension()

panels = []

context = [
    {'role':'assistant',
     'content':"""
      너는 사용자에게 적합한 운동프로그램을 추천하기 위한 챗봇이야
      사용자에게 먼저 인사를 하고, 해당하는 질문 4개야
      아래 해당하는 질문에 모든 답변을 받으면,각 질문을 항목별로 구분해

      질문을 순서대로 사용자에게 한개씩 해줘

      1. 당신의 이름이 뭔가요?
      2. 나이가 어떻게 되나요?
      3. 사는 곳의 정보를 알려주세요. (ex. 서울시 관악구)
      4. 운동 목표를 골라주세요. (A: 체력단련, B: 심폐기능단련)
    """
    }
  ]

inp = pn.widgets.TextInput(value="안녕하세요", placeholder='답변을 입력해주세요')
button_conversation = pn.widgets.Button(name="입력")

interactive_conversation = pn.bind(collect_messages, button_conversation)

dashboard = pn.Column(
    inp,
    pn.Row(button_conversation),
    pn.panel(interactive_conversation, loading_indicator=True, height=300),
)

dashboard.show()
