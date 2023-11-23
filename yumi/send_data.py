import openai
import os
import requests

# OpenAI API 키 설정
api_key = os.environ.get('OPENAI_API_KEY')
openai.api_key = api_key

# 사용자 입력값
user_input = "안녕하세요, 운동 코치님! 나는 25세이고 체력 단련을 원해요."

# API에 전송할 데이터
data = {
    "prompt": user_input,
    "max_tokens": 100,  # 최대 토큰 수 설정
    "temperature": 0.7  # 채팅의 창의성을 조절하는 매개변수
}

# API에 POST 요청
response = requests.post(
    "https://api.openai.com/v1/engines/davinci/completions",
    json=data,
    headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
)

# API 응답 확인
if response.status_code == 200:
    result = response.json()
    # 여기서 필요한 값 추출 또는 활용
    assistant_response = result["choices"][0]["text"]
    print("Assistant's response:", assistant_response)
else:
    print(f"Error: {response.status_code}, {response.text}")
