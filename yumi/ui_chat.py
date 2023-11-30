import pandas as pd
import streamlit as st
from exercise_chatbot import ExerciseChatbot
import get_facility_info
import uuid

# Create an instance of ExerciseChatbot
exercise_chatbot = ExerciseChatbot()

unique_key = str(uuid.uuid4())

# Load data
excel_file_path = 'D:/2023-Sesac-Project-BeLife/yumi/langchain_facility_info.xlsx'
data = pd.read_excel(excel_file_path)
unique_program = data.drop_duplicates()

# Panel elements
question_text = st.empty()
response_input = st.text_input(label='입력해주세요', key=unique_key)
submit_button = st.button('입력')
chat_history_panel = st.empty()

# Event handler for button click
def submit_response():
    response = response_input.value
    exercise_chatbot.process_user_response(response)

    next_question = exercise_chatbot.ask_next_question()
    question_text.text(next_question)
    response_input.text('')

    chat_history = ''
    for entry in exercise_chatbot.chat_history:
        role = entry['role']
        message = entry['message']
        chat_history += f"{role}: {message}\n"

    if exercise_chatbot.is_all_questions_answered():
        submit_button.disabled = True
        response_input.disabled = True

        result_program_names = ['수영', '필라테스', '헬스']
        answer_dic = {}
        for idx, program_name in enumerate(result_program_names):
            updated_answer = cosine_answers[:2] + [program_name] + cosine_answers[2:]
            answer_dic[idx] = updated_answer

        result_df = pd.DataFrame()

        for key, value in answer_dic.items():
            modeling_input = ' '.join(value)
            recommendations_df = get_facility_info.recommend_programs(modeling_input, unique_program)
            result_df = pd.concat([result_df, recommendations_df])

        if not result_df.empty:
            chat_history += "\n추천된 프로그램 정보:\n"
            chat_history += result_df.to_string(index=False)

    chat_history_panel.text(chat_history)

# Initial question
question_text.text(exercise_chatbot.ask_next_question())

# Streamlit app layout
st.sidebar.title('운동 프로그램 추천 챗봇')
st.sidebar.info('여러 가지 질문을 통해 맞춤형 운동 프로그램을 추천해 드립니다.')
layout = st.empty()

# Run the app
while not exercise_chatbot.is_finished():
    layout.title('운동 프로그램 추천 챗봇')
    layout.text('채팅 내역:')
    layout.text(chat_history_panel)
    layout.text_input(label='입력해주세요')
    layout.button('입력', on_click=submit_response)
    layout.text('채팅 내역:')
    layout.text(chat_history_panel)
    layout.empty()
