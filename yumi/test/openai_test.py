import openai
import os
from dotenv import load_dotenv

#load .env
load_dotenv()
api_key = os.environ.get('OPENAI_API_KEY')

openai.api_key = api_key

prompt = "hello ai!!! "

completions = openai.Completion.create(
    engine="text-davinci-002",
    prompt= prompt,
    max_tokens=100,
    n=1,
    stop=["because", "however"],
)

message = completions.choices[0].text

messages = [
    {"role" : "system", "content" : "안녕!!!"},
    {"role" : "user", "content" : "만나서 반가워!!!"}

]
# while True:
#     #user_content = input("사용자")
#     message.append({"role" : "system", "content" : "안녕!!!"})
#     completion = openai.ChatCompletion.create(model = "gpt-3.5-turbo", message = messages)
#     assistant_content = completion.choices[0].message["content"].strip()
#     message.append({"role" : "assitant", "content" : f"{assistant_content}"})

#     print(f"GPT : {assistant_content}")

