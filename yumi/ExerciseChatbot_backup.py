import panel as pn
import re
    
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
            if response in ['1', '2', '3', '4', '5', '6'] :
                return True
            else : False
    elif index == 5 : #건강상태
            if response in ['1', '2', '3', '4','5','6','7','8'] :
                return True
            else : False
    elif index == 6 : #운동 시간대
            if response in ['1', '2', '3', '4','5'] :
                return True
            else : False
    elif index == 7 : #선호 운동
            if response in ['1', '2', '3', '4','5','7'] :
                return True
            else : False
    elif index == 8 : #운동빈도
            if response in ['1', '2', '3', '4'] :
                return True
            else : False
    elif index == 9 : #중요항목
            if response in ['1', '2', '3', '4','5','6','7'] :
                return True
            else : False
    else : 
        return True
    
user_input = []       
class ExerciseChatbot:
    def __init__(self):
        self.user_data = {}
        self.questions = [
            "안녕하세요! 저는 공공 운동 프로그램을 추천을 도와주는 챗봇입니다.\n지금부터 여러 가지 질문을 통해 사용자에게 맞춤형 운동 프로그램을 추천해 드리겠습니다.\n먼저 몇 가지 개인 정보를 알아보겠습니다\n\n먼저, 당신의 연령대가 어떻게 되나요? (1: 학생, 2: 성인, 3: 노인)",
            "당신이 선호하는 지역을 알려주세요 (예시: 중구, 종로구, 마포구 등)",
            "장애 여부를 알려주세요 (1: 없음, 2: 있음)",
            "이제는 운동에 대한 선호에 대해 알아보겠습니다.\n어떤 목표로 운동을 하시려나요?\n1: 체중관리 및 다이어트 \n2: 스트레스 해소 및 심리적 향상 \n3: 근력 및 근지구력 향상 \n4: 체형관리 및 개선 \n5: 사회적 활동 및 취미 \n6: 성능 향상 및 목표 도달)",
            "아래 건강 상태 중 어떤 문제를 갖고 있나요? \n1: 관절 및 근육 상태 (관절염, 근육 경련, 근육 약화 등\n2: 심폐 기능 (심혈관 질환, 호흡기 문제)\n3: 당뇨 관리 (혈당 관리)\n4: 스트레스 관리\n5: 우울증 및 불안\n6: 수면 문제\n7: 대사 증후군 및 대사 질환 (당뇨, 고혈압 등 대사 관련 질환)\n8: 호르몬 수준",
            "어떤 시간대에 운동하는 것을 선호하시나요? (1: 새벽, 2: 오전, 3: 오후, 4: 저녁, 5: 무관)",
            "어떤 종류의 운동을 선호하시나요?\n1: 구기및라켓\n2: 레저\n3: 무도\n4: 무용\n5: 민속\n6: 재활\n7: 체력단련및생활운동)",
            "주당 몇 회 정도의 운동을 선호하시나요? (1: 주1회 2: 주2회 3: 주3회 4: 주4회 이상)",
            "현재 항목 중 가장 중요하게 여기는 것이 무엇인가요?\n1: 건강상태\n2: 운동목표\n3: 연령대\n4: 거주지\n5: 선호빈도\n6: 선호시간대\n7: 선호인원수"
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
            return "질문이 끝났습니다. 잠시만 기다려주세요 곧 운동 프로그램을 추천해드리겠습니다"
        
    #챗봇의 현재 사용자의 채팅 기록
    def process_user_response(self, response):
        current_question = self.questions[self.current_question_index - 1]
        self.chat_history.append({'role': 'system', 'message': current_question})
        if is_valid_input(self.current_question_index, response) :
            self.chat_history.append({'role': '나', 'message': response})
            user_input.append(response)
        else :
            self.chat_history.append({'role': 'system', 'message': "죄송합니다. 입력이 잘못되었습니다. 다시 입력해주세요"})
            self.current_question_index -= 1 #잘못된 답변을 했을때 다시 이전 질문으로 돌아가기 위함
            
# ExerciseChatbot 인스턴스 생성
exercise_chatbot = ExerciseChatbot()

# Panel 요소 생성
question_text = pn.pane.Str()
response_input = pn.widgets.TextInput(placeholder='입력해주세요')
submit_button = pn.widgets.Button(name='입력')
chat_history_panel = pn.pane.Str('', width=600, height=300)

# 사용자가 입력한 내용을 갖고와 다음 질문을 화면에 표시하고 대화를 기록
def submit_response(event):
    response = response_input.value
    exercise_chatbot.process_user_response(response)
    next_question = exercise_chatbot.ask_next_question()
    question_text.object = next_question
    response_input.value = ''

    # 대화 내용 기록
    chat_history = ''
    for entry in exercise_chatbot.chat_history:
        role = entry['role']
        message = entry['message']
        chat_history += f"{role}: {message}\n"

    chat_history_panel.object = chat_history

# Panel 레이아웃 설정
layout = pn.Column(
    question_text,
    response_input,
    submit_button,
    chat_history_panel
)

print("사용자 전체 답변 : ", user_input)

# 버튼이 클릭되었을 때 호출
submit_button.on_click(submit_response)

# 질문 표시
question_text.object = exercise_chatbot.ask_next_question()

# Panel 대시보드 표시
layout.servable().show()
