import streamlit as st
from ExerciseChatbot import ExerciseChatbot

class SessionState:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

session_state = SessionState(chatbot_initialized=False)

exercise_chatbot = ExerciseChatbot()

def main():
    
    if not session_state.chatbot_initialized:
        session_state.exercise_chatbot = ExerciseChatbot()
        session_state.chatbot_initialized = True
        
    st.title("For Your Better Life")

    # 채팅 기록
    for entry in session_state.exercise_chatbot.chat_history:
        role = entry['role']
        message = entry['message']
        st.write(f"{role}: {message}")

    # 현재 질문 표기
    current_question = session_state.exercise_chatbot.ask_next_question()
    
    # 다음 질문
    st.write(f"챗봇: 안녕하세요! 저는 공공 운동 프로그램을 추천을 도와주는 챗봇입니다.")
    st.write(f"지금부터 여러 가지 질문을 통해 사용자에게 맞춤형 운동 프로그램을 추천해 드리겠습니다.")
    st.write(f"먼저 몇 가지 개인 정보를 알아보겠습니다")
    #st.write(f"챗봇: {current_question}")
    

    if not any(entry['message'] == current_question for entry in session_state.exercise_chatbot.chat_history):
        st.write(f"챗봇: {current_question}")

    user_response = st.text_input("나: ", key=current_question)

    # 입력 버튼
    if st.button("입력"):
        session_state.exercise_chatbot.process_user_response(user_response)
        user_response = ""

if __name__ == "__main__":
    main()
    
    #streamlit run chatbot_ui.py
