import panel as pn
import re
import pandas as pd
import get_facility_info
    
location_pattern = r'^[가-힣]+구$'

#대답에 따라 사용자 응답 유효성 검사
def is_valid_input(index, response):
    if index == 1 : #연령대
        if response in ['1', '2', '3'] :
            return True
        else : False
    elif index == 2 : #위치
            if re.match(location_pattern, response) :
                return True
            else : False
    elif index == 3 : #장애여부
            if response in ['1', '2'] :
                return True
            else : False
    elif index == 4 : #운동목표
            if response in ['1', '2', '3', '4', '5', '6', '7'] :
                return True
            else : False
    elif index == 5 : #선호 운동
            if response in ['1', '2', '3', '4','5', '6', '7', '8'] :
                return True
            else : False
    elif index == 6 : #운동 시간대
            if response in ['1', '2', '3', '4', '5'] :
                return True
            else : False
    elif index == 7 : #주당 운동 빈도
            if response in ['1', '2', '3', '4', '5'] :
                return True
            else : False
    elif index == 8 : #중요항목
            if response in ['1', '2', '3', '4', '5', '6', '7'] :
                return True
            else : False
    else : 
        return True

#chatbot
class ExerciseChatbot:
    def __init__(self):
        #self.user_data = {}
        self.questions = [
            "안녕하세요! 저는 공공 운동 프로그램을 추천을 도와주는 챗봇입니다.\n지금부터 여러 가지 질문을 통해 사용자에게 맞춤형 운동 프로그램을 추천해 드리겠습니다.\n먼저 몇 가지 개인 정보를 알아보겠습니다\n먼저, 당신의 연령대가 어떻게 되나요?\n1: 학생, 2: 성인, 3: 노인",
            "당신이 운동을 할때 선호하는 '지역구'을 알려주세요 (예시: 중구, 종로구, 마포구 등)",
            "장애로 인해 운동시 활동에 불편한 점이 있나요? (1: 없음, 2: 있음)",
            "이제는 운동에 대한 선호에 대해 알아보겠습니다.\n어떤 목표로 운동을 하시려나요?\n1: 수명 연장 \n2: 심폐 기능 향상 \n3: 근력 향상 \n4: 유연성 향상 \n5: 체중 및 신체구성(체지방) \n6: 기분개선 \n7: 무관",
            "어떤 종류의 운동을 선호하시나요?\n1: 구기 및 라켓\n2: 레저\n3: 무도\n4: 무용\n5: 민속\n6: 재활\n7: 체력단련 및 생활운동\n8: 무관",            
            "어떤 시간대에 운동하는 것을 선호하시나요?\n 1: 새벽\n 2: 오전\n 3: 오후\n 4: 저녁\n 5: 무관",
            "주당 몇 회를 하는 운동을 원하시나요?\n 1: 주1회\n 2: 주2회\n 3: 주3회\n 4: 주4회 이상\n 5: 무관",
            "현재 항목 중 가장 중요하게 여기는 것이 무엇인가요?\n1: 운동 목표\n2: 연령대\n3: 선호 지역\n4: 선호 시간대\n5: 선호 운동 \n6: 무관",
            "질문이 끝났습니다. 잠시만 기다려주세요~~ 곧 운동 프로그램을 추천해드리겠습니다"
        ]
        # 질문과 응답 기록을 저장
        self.chat_history = []  
        #현재 어떤 질문을 물어봐야하는지 나타내는 것
        self.current_question_index = 0

    #질문을 구분하기 위해 1씩 증가
    def ask_next_question(self):
        if self.current_question_index < len(self.questions):
            next_question = self.questions[self.current_question_index]
            self.current_question_index += 1
            return next_question
        else:
            "질문을 마치겠습니다"
        
    #챗봇의 현재 사용자의 채팅 기록
    def process_user_response(self, response):
        current_question = self.questions[self.current_question_index - 1]
        self.chat_history.append({'role': 'system', 'message': current_question})
        if is_valid_input(self.current_question_index, response) :
            self.chat_history.append({'role': '나', 'message': response})
            #print(response)
            # 선택한 번호에 대응하는 키 값을 출력
            key = get_key_from_response(self.current_question_index, response)
            print(f"선택한 번호에 대응하는 키 값: {key}")
            #프로그램을 추천할때 분류가 필요한 항목만 입력(연령대, 위치, 장애여부,운동빈도)
            if self.current_question_index in [1,2,3,6,7] :
                user_answers.append(key)
        else :
            self.chat_history.append({'role': 'system', 'message': "죄송합니다. 입력 형식이 잘못되었습니다. 다시 입력해주세요"})
            self.current_question_index -= 1 #잘못된 답변을 했을때 다시 이전 질문으로 돌아가기 위함
    
    #사용자가 모든 질문에 답했는지 여부를 확인
    def is_all_questions_answered(self):
        return self.current_question_index == len(self.questions)

def get_key_from_response(index, response):
    key_mappings = [
        {'1': '학생', '2':'성인', '3':'노인'}, 
        {},
        {'1': '무', '2':'유'}, 
        {'1':'수명연장', '2':'심폐기능향상', '3':'근력및근육강화', '4':'유연성향상', '5':'체중및신체구성(체지방)조절', '6':'기분개선', '7' : '무관'}, 
        {'1':'구기및라켓', '2':'레저', '3':'무도', '4':'무용', '5':'민속', '6':'재활', '7':'체력단련및생활운동', '8' : '무관'}, 
        {'1':'새벽', '2':'오전', '3':'오후', '4':'저녁', '5':'무관'},
        {'1': '주1회', '2':'주2회', '3':'주3회', '4': '주4회 이상' , '5' : '무관'},
        {'1':'운동 목표', '2':'연령대', '3':'선호지역', '4':'선호시간대', '5':'선호 운동', '6':'무관'}
    ]
    return key_mappings[index-1].get(response, response)

user_answers = []  

# ExerciseChatbot 인스턴스 생성
exercise_chatbot = ExerciseChatbot()

# Panel 요소 생성
question_text = pn.pane.Str()
response_input = pn.widgets.TextInput(placeholder='입력해주세요')
submit_button = pn.widgets.Button(name='입력')
chat_history_panel = pn.pane.Str('', width=600, height=300)

excel_file_path = './yumi/langchain_facility_info.xlsx'
data = pd.read_excel(excel_file_path)
#중복된 행은 삭제
unique_program = data.drop_duplicates()

# 사용자가 입력한 내용과 다음 질문을 화면에 표시하고 대화를 기록
def submit_response(event):
    response = response_input.value
    exercise_chatbot.process_user_response(response)
    
    # 다음 질문을 표시
    next_question = exercise_chatbot.ask_next_question()
    question_text.object = next_question
    response_input.value = ''
    
    # 대화 내용 기록
    chat_history = ''
    for entry in exercise_chatbot.chat_history:
        role = entry['role']
        message = entry['message']
        chat_history += f"{role}: {message}\n"
    
    # 사용자 응답을 이용하여 프로그램 정보 추천
    if exercise_chatbot.is_all_questions_answered():
        submit_button.disabled = True  # 모든 질문에 답했을 때 버튼 비활성화
        response_input.disabled = True
        
        #TODO : 모델링해서 나온 값 names에 넣기
        #TODO : user_answer에 프로그램명별로 넣어서 프로그램명이 포함된 user_answer을 만들어라
        result_program_names = ['수영', '필라테스', '헬스']
        for idx, program_name in enumerate(result_program_names):
            user_answers[idx].insert(2, program_name)
        print(user_answers)
        modeling_input = ' '.join(user_answers)
        #TODO : user_answer값이 3개인 경우 어떻게 유사도를 구할지 ...
        recommendations_df = get_facility_info.recommend_programs(modeling_input, unique_program)
        
        # 프로그램 추천 정보를 채팅창에 추가
        if not recommendations_df.empty:
            chat_history += "\n추천된 프로그램 정보:\n"
            chat_history += recommendations_df.to_string(index=False)

    chat_history_panel.object = chat_history

#TODO : 화면 라이브버리 변경

# 버튼이 클릭되었을 때 호출
submit_button.on_click(submit_response)
# 질문 표시
question_text.object = exercise_chatbot.ask_next_question()

# Panel 레이아웃 설정
layout = pn.Column(
    question_text,
    response_input,
    submit_button,
    chat_history_panel
)

# Panel 대시보드 표시
layout.servable().show()
