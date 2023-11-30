import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.schema import AIMessage, SystemMessage
from typing import Optional

# .env 파일 로드
load_dotenv()
api_key = os.environ.get('OPENAI_API_KEY')

# AIMessage에 새로운 필드 추가
class CustomAIMessage(AIMessage):
    questions: Optional[list[str]] = None

# ExerciseChatBot 클래스 정의
class ExerciseChatBot:
    def __init__(self, csv_path):
        # ChatOpenAI 모델 초기화
        self.llm = ChatOpenAI(
            temperature=1.0,
            model='gpt-3.5-turbo-0613',
            openai_api_key=api_key
        )

        # TextLoader를 사용하여 파일 로드
        self.loader = TextLoader(csv_path, encoding='utf-8')
        self.document = self.loader.load()

    def find_recommand_program(self, user_input):
        # 여기에서 사용자 입력을 분석하고, 최적의 프로그램을 찾는 로직을 추가하세요.
        # 예를 들어, 사용자 입력에서 위치 정보를 추출하고, 가장 가까운 프로그램을 찾을 수 있는 방식으로 구현할 수 있습니다.
        # 이 부분은 프로젝트에 따라 다르게 구현될 수 있습니다.

        # 임시로 가장 가까운 프로그램을 찾았다고 가정합니다.
        program_name = "수영"
        facility = "광진문화예술회관"
        location = "서울시 광진구 자양동"

        return program_name, facility, location

    def interact_with_model(self, user_input):
        # 사용자 입력을 통해 가장 가까운 프로그램을 찾음
        program_name, facility, location = self.find_recommand_program(user_input)

        # Langchain에서 사용할 형식으로 메시지 포맷 변경
        history_langchain_format = [
            SystemMessage(content="당신은 운동 프로그램과 해당하는 센터의 위치, 운영 시간 등 관련 정보를 보여주는 챗봇 입니다.")]

        # AIMessage 대신에 CustomAIMessage를 사용
        ai_message = AIMessage(content=f"프로그램명 {program_name}을 추천합니다. 위치: {location}, 시설명: {facility}")

        history_langchain_format.append(ai_message)

        try:
            # ChatOpenAI 모델과 상호 작용
            gpt_response = self.llm(history_langchain_format)
            return gpt_response.content
        except Exception as e:
            return f"죄송합니다 입력이 잘못되었습니다 다시 입력해주세요"

# CSV 파일 경로 설정
csv_file_path = "./yumi/langchain_facility_info.xlsx"

# ExerciseChatBot 인스턴스 생성
exercise_chat_bot_instance = ExerciseChatBot(csv_file_path)

# 사용자 입력 받아서 모델과 상호 작용
user_input = "종로구에 위치한 센터 이름이 추천해줘"
response = exercise_chat_bot_instance.interact_with_model(user_input)

# 결과 출력
print(response)
