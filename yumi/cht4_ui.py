import pandas as pd
import warnings
import streamlit as st
import get_facility_info
from ExerciseChatbot import ExerciseChatbot  # 새로 추가한 import

warnings.filterwarnings("ignore")
chat_history = []

exercise_chatbot = ExerciseChatbot()

st.title("CommunityFit Recommand ChatBot")
st.caption("사용자별 맞춤 공공시설 운동 프로그램 추천 ChatBot")

with open("D:/2023-Sesac-Project-BetterLife/ui/sidebar.md", "r", encoding='utf-8') as sidebar_file:
    sidebar_content = sidebar_file.read()
    st.sidebar.markdown(sidebar_content)

with open("D:/2023-Sesac-Project-BetterLife/ui/styles.md", "r", encoding='utf-8') as styles_file:
    styles_content = styles_file.read()
    print(styles_content)

#처음 챗봇 인사말
INITIAL_MESSAGE = [
    {
        "role": "Chatbot",
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

# 세션상태에서 message라는 키로 초기 메시지를 저장하는 것
# if "content" not in st.session_state.keys():
#     st.session_state["messages"] = INITIAL_MESSAGE.copy()

# if "history" not in st.session_state:
#     st.session_state["history"] = []
    
# 초기 메시지 출력
for entry in st.session_state["messages"]:
    st.write(f"{entry['role']}: {entry['content']}")
    
# 사용자 입력 받기
# if prompt := st.text_input(label="", placeholder="답변을 입력해주세요"):
#     st.session_state.message.append({"role": "user", "content": prompt})

# Excel 파일 읽기
excel_file_path = './data/langchain_facility_info.xlsx'
data = pd.read_excel(excel_file_path)
unique_program = data.drop_duplicates()

question = exercise_chatbot.ask_next_question()
st.write(question)

#프로그램 추천을 위한 answer값
modeling_answers = []
#해당하는 프로그램 정보를 추출하기 위한 answer값
cosine_answers = []

# 사용자 입력
#response = st.text_input("입력해주세요", key="user_input")
response = st.chat_input(key="user_input")

# 응답 제출 버튼
if response :
    st.write(response)
    exercise_chatbot.process_user_response(response)
    next_question = exercise_chatbot.ask_next_question()
    st.write(next_question)
    st.text_input = ''

    # 대화 내역 표시
    chat_history = ''
    for entry in exercise_chatbot.chat_history:
        role = entry['role']
        message = entry['message'] #질문 내용
        chat_history += f"{role}: {message}\n"
    #st.text_area("챗봇과의 대화", chat_history, height=300)

    # 모든 질문에 답했다면 프로그램 추천 진행
    if exercise_chatbot.is_all_questions_answered():
        st.button.disabled = True  # 모든 질문에 답했을 때 버튼 비활성화
        st.text_input.disabled = True
        
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
        st.text_area(chat_history)

        st.text("챗봇이 마지막 인사를 합니다. 챗봇을 종료합니다.")
        st.text_area(chat_history)
        

# # Streamlit 페이지 실행
# if __name__ == '__main__':
#     import streamlit as st
#     st._main.run()