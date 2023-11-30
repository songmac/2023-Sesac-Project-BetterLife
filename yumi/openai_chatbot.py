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

#openai가 사용자에게 질문할 내용 학습
question_context = [
 {'role':'system',
     'content':"""
      너는 사용자에게 적합한 운동프로그램을 추천하기 위한 챗봇이야
      사용자에게 먼저 인사를 하고, 해당하는 질문이 총 9개야
      아래 해당하는 질문에 모든 답변만 받아줘
      지역구를 답을 할때 구로만 끝나는 대답만 받아줘

      질문을 순서대로 사용자에게 한개씩 해줘

      "당신의 연령대가 어떻게 되나요?\n1: 학생(초,중,고), 2: 성인(대학생 포함), 3: 노인",
      "당신이 운동을 할때 선호하는 '지역구'을 알려주세요 (예시: 중구, 종로구, 마포구 등)",
      "장애로 인해 운동시 활동에 불편한 점이 있나요? (1: 없음, 2: 있음)",
      "이제는 운동에 대한 선호에 대해 알아보겠습니다.\n어떤 목표로 운동을 하시려나요?\n1: 수명 연장 \n2: 심폐 기능 향상 \n3: 근력 향상 \n4: 유연성 향상 \n5: 체중 및 신체구성(체지방) \n6: 기분개선 \n7: 무관",
      "어떤 종류의 운동을 선호하시나요?\n1: 구기 및 라켓\n2: 레저\n3: 무도\n4: 무용\n5: 민속\n6: 재활\n7: 체력단련 및 생활운동\n8: 무관",            
      "어떤 시간대에 운동하는 것을 선호하시나요?\n 1: 아침\n 2: 오전\n 3: 오전오후\n 4: 오후\n 5: 저녁 \n 6: 무관 ",
      "주당 몇 회를 하는 운동을 원하시나요?\n 1: 주1회\n 2: 주2회\n 3: 주3회\n 4: 주4회 이상\n 5: 무관",
      "현재 항목 중 가장 중요하게 여기는 것이 무엇인가요?\n1: 운동 목표\n2: 연령대\n3: 선호 지역\n4: 선호 시간대\n5: 선호 운동 \n6: 무관",
      "질문이 끝났습니다. 우리가 추천하는 운동 프로그램은 아래와 같습니다"
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
address_pattern = r'^[가-힣]+구$'
num_pattern = "r'^[0-9]"

# 유효한 경우 True, 그렇지 않은 경우 False
# def is_valid_input(reponse, prompt):
#     # 여기에서 input_text가 유효한지 여부를 판단하는 로직을 추가
#     address_keywords = ["거주지", "동", "구", "사는곳"]
#     if reponse in address_keywords :
#         if re.match(prompt, address_pattern) :
#             return True
#         else : False
#     else :
#         if re.match(prompt, num_pattern) :
#             return True
#         else : False
    

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
    return pn.Column(*panels)

def get_key_from_response(index, response):
    key_mappings = [
        {'1': '학생', '2':'성인', '3':'노인'},
        {},
        {'1': '무', '2':'유'}, 
        {'1':'수명 연장', '2': '심폐 기능 향상', '3':'근력 및 근육강화', '4':'유연성 향상', '5':'체중 및 신체구성(체지방)조절', '6':'기분 개선', '7' : '무관'},
        {'1':'구기 및 라켓', '2':'레저', '3':'무도', '4':'무용', '5':'민속', '6':'재활', '7':'체력단련및생활운동', '8' : '무관'},
        {'1':'아침', '2':'오전', '3':'오전오후', '4':'오후', '5':'저녁', '6':'무관'},
        {'1': '주1회', '2':'주2회', '3':'주3회', '4': '주4회 이상' , '5' : '무관'},
        {'1':'운동 목표', '2':'연령대', '3':'선호 지역', '4':'선호 시간대', '5':'선호 운동', '6':'무관'}
    ]
    return key_mappings[index-1].get(response, response)

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


