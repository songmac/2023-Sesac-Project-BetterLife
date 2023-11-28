import os
import panel as pn
from dotenv import load_dotenv
import gradio as gr 

from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from typing import Optional
from pydantic import BaseModel

# Load .env
load_dotenv()
api_key = os.environ.get('OPENAI_API_KEY')

answer_context = [
 {'role':'system',
     'content':"""
      너는 사용자에게 적합한 운동프로그램을 추천하기 위한 챗봇이야 
      해당하는 값을 넣어서     
      프로그램명 {program}
      위치 {location}
      시간 {business_hour}을 정보 기준으로 사용자에게 말하듯이 말해줘
    """
    }  
 ]

class CustomAIMessage(AIMessage):
    questions: Optional[list[str]] = None

class ExerciseChatBot:
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=1.0,
            model='gpt-3.5-turbo-0613',
            openai_api_key=api_key
        )

    def interact_with_model(self, user_input):
        # Langchain에서 사용할 형식으로 메시지 포맷 변경
        history_langchain_format = [SystemMessage(content="안녕하세요! 운동 프로그램 추천을 시작합니다.")]

        # AIMessage 대신에 CustomAIMessage를 사용
        custom_ai_message = CustomAIMessage(content=user_input, questions=[
            """너는 사용자에게 적합한 운동프로그램을 추천하기 위한 챗봇이야 
            해당하는 값을 넣어서     
            프로그램명 {program}
            위치 {location}
            시간 {business_hour}을 정보 기준으로 사용자에게 말하듯이 말해줘)"""
        ])
        
        history_langchain_format.append(custom_ai_message)

        try:
            gpt_response = self.llm(history_langchain_format)
            return gpt_response.content
        except Exception as e:
            return f"죄송합니다 입력이 잘못되었습니다 다시 입력해주세요"
        
exercise_chat_bot_instance = ExerciseChatBot()

program = "수영"
location = "광진문화예술회관"
business_hour = "오전6시 ~ 오후 10시"
user_input = "종로구에 위치한 센터 이름이 추천해줘"
response = exercise_chat_bot_instance.interact_with_model(user_input)
print(response)
# gr.ChatInterface(
#     fn=exercise_chat_bot_instance.interact_with_model,
#     textbox=gr.Textbox(placeholder="입력", container=False, scale=5),
#     # 채팅창의 크기를 조절한다.
#     chatbot=gr.Chatbot(height=400),
#     title="운동 프로그램 추천 시스템",
#     description="운동프로그램을 추천해 주는 챗봇 입니다",
#     theme="soft",
#     # retry_btn="다시보내기 ↩",
#     # undo_btn="이전챗 삭제 ❌",
#     # clear_btn="전챗 삭제 💫",
# ).launch()