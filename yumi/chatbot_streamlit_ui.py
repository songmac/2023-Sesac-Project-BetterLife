import pandas as pd
import get_facility_info
from exercise_chatbot import ExerciseChatbot  # 새로 추가한 import

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

#프로그램 추천을 위한 answer값
modeling_answers = []
#해당하는 프로그램 정보를 추출하기 위한 answer값
cosine_answers = []
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
        #모델링하여 프로그램이 3개라 dict형태로 사용자 입력값 + 추천프로그램명 저장
        result_program_names = ['수영', '필라테스', '헬스']
        answer_dic = {}
        for idx, program_name in enumerate(result_program_names):
            # 새로운 리스트 생성하여 삽입
            updated_answer = cosine_answers[:2] + [program_name] + cosine_answers[2:]
            # user_dic에 저장
            answer_dic[idx] = updated_answer

        # 결과를 저장할 데이터프레임 초기화
        result_df = pd.DataFrame()

        print("프로그램 추천 모델링을 위한 입력값 :", modeling_answers)
        print("해당하는 프로그램 위치값을 위한 입력값 :", cosine_answers)

        # 각 프로그램별로 코사인 유사도 계산
        for key, value in answer_dic.items():
            #answer = answer_dic[answer_key]  # answer_dic에서 실제 answer 가져오기
            modeling_input = ' '.join(value)
            print("modeling_input:", modeling_input)
            recommendations_df = get_facility_info.recommend_programs(modeling_input, unique_program)

            # 전체 결과 데이터프레임에 추가
            result_df = pd.concat([result_df, recommendations_df])

        # 프로그램 추천 정보를 채팅창에 추가
        if not result_df.empty:
            chat_history += "\n추천된 프로그램 정보:\n"
            chat_history += result_df.to_string(index=False)

    chat_history_panel.object = chat_history

#버튼이 클릭되었을 때 호출
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
