import os, re
from dotenv import load_dotenv
import panel as pn
import time
import asyncio

import openai
import concurrent.futures

#load .env
load_dotenv()
api_key = os.environ.get('OPENAI_API_KEY')

#api key 설정
openai.api_key = api_key

#open ai 설정 : gpt-3.5-turbo
def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0, max_tokens=500):
    response = openai.chat.completions.create(
        model= model,
        messages = messages,
        temperature = temperature,
        max_tokens = max_tokens,
        stop= ["종료", "나가기"]
    )
    return response.choices[0].message.content

#챗봇 답변 속도를 높이기 위해 병렬 작업처리
def interact_with_model(context):
    #concurrent.futures 모듈은 비동기적으로 실행하는 인터페이스
    #ThreadPoolExecutor 는 스레드 풀을 사용하여 호출을 비동기적으로 실행하는 Executor 서브 클래스
    with concurrent.futures.ThreadPoolExecutor() as executor:
        #submit()객체는 future 객체를 반환(비동기 연산의 결과)
        future = executor.submit(get_completion_from_messages, context)
        #수행 완료된 작업물
        response = future.result()
    return response

#openai에 학습할 내용
context = [
    {'role':'assistant',
     'content':"""
      너는 사용자에게 적합한 운동프로그램을 추천하기 위한 챗봇이야
      사용자에게 먼저 인사를 하고, 해당하는 질문 3개야
      아래 해당하는 질문에 모든 답변만 받아줘
      모든 질문에 답변을 다 받으면 인사와 함께 챗봇을 종료해줘

      질문을 순서대로 사용자에게 한개씩 해줘

      - 나이가 어떻게 되나요?
      - 거주지가 어떻게 되나요? (중구 회현동)
      - 운동 목표를 골라주세요. (1: 체력단련, 2: 심폐기능단련)
    """
    }
  ]

#사용자가 형식에 맞지 않게 답변을 한 경우 처리 
address_pattern = "r'^[가-힣]+구 [가-힣]+동$"
num_pattern = "r'^[0-9]"

# 유효한 경우 True, 그렇지 않은 경우 False
def is_valid_input(reponse, prompt):
    # 여기에서 input_text가 유효한지 여부를 판단하는 로직을 추가
    address_keywords = ["거주지", "동", "구", "사는곳"]
    if reponse in address_keywords :
        if re.match(prompt, address_pattern) :
            return True
        else : False
    else :
        if re.match(prompt, num_pattern) :
            return True
        else : False

#챗봇 질문과 사용자 답변 panel 라이브러리를 통해 화면 출력
def collect_messages(_):
    start_time = time.time()
    prompt = inp.value_input
    inp.value = '' #사용자 입력 초기화
    #사용자 content 입력
    if is_valid_input(response ,prompt):
        context.append({'role':'user', 'content':f"{prompt}"})
        #openai 응답값
        response = interact_with_model(context)
        end_time = time.time()
        context.append({'role':'system', 'content':f"{response}"})
        print("prompt 값 : ", prompt)
        #화면에 보여주기
        panels.append(pn.Row('나:', pn.pane.Markdown(prompt, width=600)))
        panels.append(pn.Row('나의운동코치:', pn.pane.Markdown(response, width=600, styles={'background-color': '#f0fcd4'})))
        print("taken time : ", end_time - start_time)
    else:
        # 유효하지 않은 입력에 대한 안내 메시지
        panels.append(pn.Row('나의운동코치:', pn.pane.Markdown("죄송합니다. 입력이 잘못되었습니다. 다시 시도해주세요.", width=600, styles={'background-color': '#f0fcd4'})))
    return pn.Column(*panels)

#챗봇 화면 만들기 
pn.extension()

panels = []

#챗봇 input버튼
inp = pn.widgets.TextInput(value="안녕하세요!!", placeholder='입력해주세요')
#입력 버튼
button_conversation = pn.widgets.Button(name="입력")
#대화내용 화면에 표기
interactive_conversation = pn.bind(lambda _: asyncio.create_task(collect_messages(_)), button_conversation)
dashboard = pn.Column(
    inp,
    pn.Row(button_conversation),
    pn.panel(interactive_conversation, loading_indicator=True, height=300),
)
#대쉬보드 출력
dashboard.show()


