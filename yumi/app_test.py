import warnings
import streamlit as st
from ExerciseChatbot import ExerciseChatbot
#python -m streamlit run ./yumi/app_test.py

warnings.filterwarnings("ignore")
chat_history = []

exercise_chatbot = ExerciseChatbot()

#Chatbot title
st.title("CommunityFit Recommand ChatBot")
st.caption("사용자별 맞춤 공공시설 운동 프로그램 추천 ChatBot")
#st.set_page_config(page_title="Exercise Chatbot", layout="wide")
#st.title("취저   공공 운동프로그램 추천 챗봇")
#사이드바
with open("D:/2023-Sesac-Project-BetterLife/ui/sidebar.md", "r", encoding='utf-8') as sidebar_file:
    sidebar_content = sidebar_file.read()
    st.sidebar.markdown(sidebar_content)

with open("D:/2023-Sesac-Project-BetterLife/ui/styles.md", "r", encoding='utf-8') as styles_file:
    styles_content = styles_file.read()
    print(styles_content)

#처음 챗봇 인사말
INITIAL_MESSAGE = [
    {
        "role": "system",
        "content": "안녕하세요! 저는 공공체육시설 운동 프로그램을 추천하는 ComFit이예요. 당신의 정보를 알기 위해 몇가지 질문을 할꺼예요. 해당하는 부분을 선택해 주시면 되요 지금부터 시작할께요🔍",
    },
]

if "messages" not in st.session_state:
    st.session_state["messages"] = INITIAL_MESSAGE.copy()

# 사이드 바 표기
st.sidebar.markdown(sidebar_content)

# 리셋 버튼
if st.sidebar.button("Reset Chat"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.session_state["messages"] = INITIAL_MESSAGE
    st.session_state["history"] = []
    
st.sidebar.markdown(
    "**Note:** <span style='color:red'>현재 모델링은 SVD기준으로 만들어졌습니다</span>",
    unsafe_allow_html=True,
)

#html을 렌더링할떄 안전성 검사를 뛰고 해당 HTML 코드를 그대로 표시
st.write(styles_content, unsafe_allow_html=True)

# 세션상태에서 message라는 키로 초기 메시지를 저장하는 것
if "content" not in st.session_state.keys():
    st.session_state["messages"] = INITIAL_MESSAGE.copy()

if "history" not in st.session_state:
    st.session_state["history"] = []
    
# 초기 메시지 출력
for entry in st.session_state["messages"]:
    st.write(f"{entry['role']}: {entry['content']}")
    
# 사용자 입력 받기
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    
# 사용자 입력에 대한 챗봇 응답 표시
if st.button("입력"):
    response = exercise_chatbot.process_user_response(prompt)
    st.session_state.messages.append({"role": "system", "content": response})

    # 대화 내용 기록
    append_chat_history(prompt, response)

    # 챗봇의 질문 표시
    next_question = exercise_chatbot.ask_next_question()
    st.session_state.messages.append({"role": "system", "content": next_question})
    append_chat_history(response, next_question)
    
 # 사용자에게 보여줄 추천 프로그램 표시
    if exercise_chatbot.is_all_questions_answered():
        st.button("Reset Chat", key="reset_button")  # 버튼 재활성화
        st.text("챗봇이 마지막 인사를 합니다. 챗봇을 종료합니다.")
        st.session_state["messages"] = INITIAL_MESSAGE  # 메시지 초기화