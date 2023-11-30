import pandas as pd
import streamlit as st
from ExerciseChatbot_stremlit import ExerciseChatbot

st.title("Benebit ChatBot")
st.markdown("**맞춤 공공시설 운동 프로그램 추천 시스템 ChatBot 🐱**")

#initial message
INITIAL_MESSAGE = [
    {
        "role": "system",
        "content": "안녕하세요! 저는 공공체육시설 운동 프로그램을 추천을 도와주기 위한 챗봇 Benebit이예요. 당신의 정보를 알기 위해 몇가지 질문을 할꺼예요. 해당하는 부분을 선택해 주시면 되요 지금부터 시작할께요🔍",
    },
]

#initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = INITIAL_MESSAGE.copy()
    #st.session_state["messages"].append({"role" : "assistant", "content" : "먼저, 당신의 연령대가 어떻게 되나요?\n1: 학생(초,중,고), 2: 성인(대학생 포함), 3: 노인"})

if "assistant" not in st.session_state:
    st.session_state["assistant"] = ExerciseChatbot()
else:
    exercise_chatbot = st.session_state["assistant"]

# get data
excel_file_path = './data/langchain_facility_info.xlsx'
data = pd.read_excel(excel_file_path)
unique_program = data.drop_duplicates()

exercise_chatbot = ExerciseChatbot()

#display chat messages for history on app rerun
for message in st.session_state["messages"]:
    print("***",message)
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


next_question = exercise_chatbot.ask_next_question()
with st.chat_message("assistant") :
    st.markdown(next_question)
    
# react to user input
if prompt := st.chat_input("답변을 입력해주세요"):
    #display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
        
    #add user message to chat history
    st.session_state["messages"].append({"role" : "user", "content" : prompt})

    #response = f"Echo : {prompt}"
    print('prompt :', prompt)
    if exercise_chatbot.process_user_response(prompt) :
        pass
    else : 
        #st.chat_message("assistant")
        st.markdown("입력형식이 잘못 됐습니다")
    
    # exercise_chatbot.process_user_response(prompt)
    # next_question = exercise_chatbot.ask_next_question()

    #display assistant reponse in chat message contain 
    with st.chat_message("assistant") :
        st.markdown(next_question)
        
    #add assistant reponse to chat history
    st.session_state["messages"].append({"role" : "assistant", "content" : next_question})
    

