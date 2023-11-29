import streamlit as st
import warnings
#python -m streamlit run ./yumi/app_test.py

warnings.filterwarnings("ignore")
chat_history = []

#Chatbot title
st.title("CommunityFit Recommand ChatBot")
st.caption("사용자별 맞춤 공공시설 운동 프로그램 추천 ChatBot")
#st.set_page_config(page_title="Exercise Chatbot", layout="wide")
#st.title("취저   공공 운동프로그램 추천 챗봇")
#사이드바
with open("D:/2023-Sesac-Project-BetterLife/ui/sidebar.md", "r", encoding='utf-8') as sidebar_file:
    sidebar_content = sidebar_file.read()
    print(sidebar_content)

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

# Add a reset button
if st.sidebar.button("Reset Chat"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.session_state["messages"] = INITIAL_MESSAGE
    st.session_state["history"] = []
