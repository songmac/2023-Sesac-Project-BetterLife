import panel as pn
import pandas as pd
import get_facility_info
from ExerciseChatbot import ExerciseChatbot

#프로그램 추천을 위한 answer값
modeling_answers = []
#해당하는 프로그램 정보를 추출하기 위한 answer값
cosine_answers = []
# ExerciseChatbot 인스턴스 생성
exercise_chatbot = ExerciseChatbot()

# Panel 요소 생성
question_text = pn.pane.Str()
response_input = pn.widgets.TextInput(placeholder='입력해주세요')
submit_button = pn.widgets.Button(name='입력')
history_panel = pn.pane.Str(css_classes=['nanum-square'])
recommendation_table = pn.widgets.DataFrame(css_classes=['nanum-square'])

# 나눔 글꼴 경로
nanum_font_path = 'C:/Users/aline/AppData/Local/Microsoft/Windows/Fonts/NanumSquare.ttf'

# Panel 요소 생성
question_panel = pn.Column()
answer_panel = pn.Column()
history_panel = pn.Column()

# 질문 패널 스타일 설정
question_panel.styles = {
    'background-color': '#f9eb54',  # 질문 패널 배경색 노란색
    'padding': '10px',
    'margin': '5px',
    'border-radius': '10px',
}

# 응답 패널 스타일 설정
answer_panel.styles = {
    'background-color': '#93cbde',  # 응답 패널 배경색 파란색
    'padding': '10px',
    'margin': '5px',
    'border-radius': '10px',
}

# history 패널 스타일 설정
history_panel.styles = {
    'background-color': '#E1E8ED',  # history 패널 배경색 회색
    'padding': '10px',
    'margin': '5px',
    'border-radius': '10px',
}

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
        # 각 role에 따라 style 변수 정의
        style = 'background-color: #f9eb54;' if role == 'chatbot' else 'background-color: #93cbde;'
        # 질문인 경우
        if role == 'chatbot':
            question_panel.append(f"<div style='{style}'>{role}: {message}</div>")
        # 응답인 경우
        else:
            answer_panel.append(f"<div style='{style}'>{role}: {message}</div>")
            
        if role == 'user' and message:
            next_question = exercise_chatbot.ask_next_question()
            question_text.object = next_question
            
    history_panel.append(question_panel)
    history_panel.append(answer_panel)

    # 결과를 저장할 데이터프레임 초기화
    result_df = pd.DataFrame()
    
    # 사용자 응답을 이용하여 프로그램 정보 추천
    if exercise_chatbot.is_all_questions_answered():
        submit_button.disabled = True  # 모든 질문에 답했을 때 버튼 비활성화
        response_input.disabled = True
        
        #모델링하여 프로그램이 3개라 dict형태로 사용자 입력값 + 추천프로그램명 저장
        result_program_names = ['수영', '필라테스', '헬스']
        answer_dic = {}
        for idx, program_name in enumerate(result_program_names):
            # 새로운 리스트 생성하여 삽입
            updated_answer = cosine_answers[:2] + [program_name] + cosine_answers[2:]
            # user_dic에 저장
            answer_dic[idx] = updated_answer

        print("프로그램 추천 모델링을 위한 입력값 :", modeling_answers)
        print("해당하는 프로그램 위치값을 위한 입력값 :", cosine_answers)

        # 각 프로그램별로 코사인 유사도 계산
        for key, value in answer_dic.items():
            #answer = answer_dic[answer_key]  # answer_dic에서 실제 answer 가져오기
            modeling_input = ' '.join(value)
            print("modelint_input:", modeling_input)
            recommendations_df = get_facility_info.recommend_programs(modeling_input, unique_program)

            # 전체 결과 데이터프레임에 추가
            result_df = pd.concat([result_df, recommendations_df])

        # 프로그램 추천 정보를 채팅창에 추가
        if not result_df.empty:
            chat_history += "<div style='background-color: #f9eb54;'>\n추천된 프로그램 정보:</div>"
            recommendation_table.value = result_df[['시설명','종목명','프로그램명','연령','성별','장애','주간횟수','시간대','지번주소']].reset_index(drop=True)

    history_panel.object = chat_history
    response_input.styles = {'background-color': '#F9EB54', 'margin-top': '10px'}

#버튼이 클릭되었을 때 호출
submit_button.on_click(submit_response)
# 질문 표시
question_text.object = exercise_chatbot.ask_next_question()

# Panel 레이아웃 설정
layout = pn.Column(
    pn.Row(response_input, submit_button),# 텍스트 입력과 버튼을 같은 행에 배치
    question_text,
    history_panel,
    recommendation_table,
)

layout.styles = {'background': '#93cbde', 'padding': '10px', 'border': '2px solid #eee',
                 'box-shadow' :'3px 1px 4px rgba(0, 0, 0, 0.2)',}

# Panel 대시보드 표시
layout.servable().show()