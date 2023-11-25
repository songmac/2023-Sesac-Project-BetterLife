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
    )
    return response.choices[0].message.content

# #챗봇 답변 속도를 높이기 위해 병렬 작업처리
# def interact_with_model(context):
#     #concurrent.futures 모듈은 비동기적으로 실행하는 인터페이스
#     #ThreadPoolExecutor 는 스레드 풀을 사용하여 호출을 비동기적으로 실행하는 Executor 서브 클래스
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         #submit()객체는 future 객체를 반환(비동기 연산의 결과)
#         future = executor.submit(get_completion_from_messages, context)
#         #수행 완료된 작업물
#         response = future.result()
#     return response

#openai가 사용자에게 질문할 내용 학습
question_context = [
 {'role':'system',
     'content':"""
      너는 사용자에게 적합한 운동프로그램을 추천하기 위한 챗봇이야
      사용자에게 먼저 인사를 하고, 해당하는 질문 3개야
      아래 해당하는 질문에 모든 답변만 받아줘

      질문을 순서대로 사용자에게 한개씩 해줘

      - 나이가 어떻게 되나요?
      - 거주지가 어떻게 되나요? (예시 : 중구, 종로구, 마포구 등)
      - 운동 목표를 골라주세요. (1: 체력단련, 2: 심폐기능단련)
    """
    }  
]

#openai가 사용자에게 모델링한 프로그램을 출력해줄 내용 학습
answer_context = [
 {'role':'system',
     'content':"""
      너는 사용자에게 적합한 운동프로그램을 추천하기 위한 챗봇이야 
      프로그램명 {program}
      시설명 {facility}
      위치 {location}을
      여기에 해당하는 정보 기준으로만 사용자에게 말하듯이 말해줘
    """
    }  
]

#사용자가 형식에 맞지 않게 답변을 한 경우 처리 
address_pattern = "r'^[가-힣]+구"
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
    

#모델링 input값으로 넣기 위해 사용자 입력값 저장
user_input = []
#챗봇이 먼저 질문을 하기 위해 사용자 첫 질문 default값 설정을 위함
inital_start = 0
#질문 content/답변 content 구분을 위함
is_question = True

#모델링한 결과값 넣기
program = "수영"
facility = "광진문화예술회관"
location = "서울시 광진구 자양동"

#챗봇 질문 및 답변 저장
def collect_messages(_):
    global inital_start
    global is_question

    if inital_start == 0 :
        prompt = "안녕하세요"
        inp.value = "" #사용자 입력 초기화
    else : 
        prompt = inp.value_input
        inp.value = ""

    start_time = time.time()
    #사용자 content 입력
    if is_valid_input(response, prompt): # 사용자 입력값 유효성 검사
        if is_question : #질문용 챗봇
            question_context.append({'role':'user', 'content':f"{prompt}"})
            #openai 응답값
            response = get_completion_from_messages(question_context)
            end_time = time.time()
            question_context.append({'role':'system', 'content':f"{response}"})

            if response in ["목표", "마지막"]: #마지막 질문
                is_question = False
        else : #답변용 챗봇
            answer_context[-1]['content'] = answer_context[-1]['content'].format(
            program=program, facility=facility, location=location)
            response = get_completion_from_messages(answer_context)
            
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


