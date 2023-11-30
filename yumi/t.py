import streamlit as st
import pandas as pd
from exercise_chatbot import ExerciseChatbot  # 필요한 import
# 챗봇 객체 생성
exercise_chatbot = ExerciseChatbot()
# Excel 파일 읽기
excel_file_path = './yumi/langchain_facility_info.xlsx'
data = pd.read_excel(excel_file_path)
unique_program = data.drop_duplicates()
# Streamlit 인터페이스 구성
st.title("운동 프로그램 추천 챗봇")
# 질문 표시
question = exercise_chatbot.ask_next_question()
st.write(question)
# 사용자 입력
response = st.text_input("입력해주세요")
# 응답 제출 버튼
if st.button('입력'):
    exercise_chatbot.process_user_response(response)
    next_question = exercise_chatbot.ask_next_question()
    st.write(next_question)
    # 대화 내역 표시
    chat_history = ''
    for entry in exercise_chatbot.chat_history:
        role = entry['role']
        message = entry['message']
        chat_history += f"{role}: {message}\n"
    st.text_area("챗봇과의 대화", chat_history, height=300)
    # 모든 질문에 답했다면 프로그램 추천 진행
    if exercise_chatbot.is_all_questions_answered():
        # 추천 프로그램 계산 로직
        # 결과 프로그램 표시
        # 예시: st.write("추천 프로그램: 수영, 필라테스, 헬스")
# Streamlit 페이지 실행
if __name__ == '__main__':
    st.run()