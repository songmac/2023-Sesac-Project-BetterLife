import pandas as pd
import warnings
import streamlit as st
from ExerciseChatbot import ExerciseChatbot

warnings.filterwarnings("ignore")

exercise_chatbot = ExerciseChatbot()

st.title("CommunityFit Recommend ChatBot")
st.caption("Personalized Exercise Program Recommendation ChatBot")

# Initial Chatbot Message
INITIAL_MESSAGE = [
    {"role": "chatbot", "content": "안녕하세요! 저는 공공체육시설 운동 프로그램을 추천하는 ComFit이에요. 당신의 정보를 알기 위해 몇 가지 질문을 할 거에요. 해당하는 부분을 선택해 주세요. 지금부터 시작할게요! 🔍"}
]

if "messages" not in st.session_state:
    st.session_state["messages"] = INITIAL_MESSAGE.copy()

# Display initial messages
for entry in st.session_state["messages"]:
    st.write(f"{entry['role']}: {entry['content']}")

# Excel 파일 읽기
excel_file_path = './data/langchain_facility_info.xlsx'
data = pd.read_excel(excel_file_path)
unique_program = data.drop_duplicates()

# Questions and Answers
questions = exercise_chatbot.get_all_questions()
answers = []

# Display Questions and Get Answers
for question in questions:
    user_answer = st.text_input(f"Chatbot: {question}", key=f"answer_{question['id']}")
    answers.append({"role": "User", "content": user_answer})

    # Process user response
    exercise_chatbot.process_user_response(user_answer)

# Disable the button after all questions are answered
if len(questions) == len(answers):
    st.session_state.button_disabled = True

# Display Chat History
st.text_area("Chat History", value="\n".join([f"{entry['role']}: {entry['content']}" for entry in st.session_state["messages"] + answers]))

# If all questions are answered, recommend programs
if st.session_state.button_disabled:
    st.text("챗봇이 마지막 인사를 합니다. 챗봇을 종료합니다.")
    result_df = exercise_chatbot.get_program_recommendations(unique_program)
    if not result_df.empty:
        st.text_area("추천된 프로그램 정보:", value=result_df.to_string(index=False))
