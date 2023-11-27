import panel as pn
from ExerciseChatbot import exercise_chatbot

class ExerciseChatbotPanel :
    #클래스 초기화 
    def __init__(self, exercise_chatbot):
        self.exercise_chatbot = exercise_chatbot
        #챗봇의 질문 리스트
        self.questions = [
            exercise_chatbot.greet_user,
            exercise_chatbot.ask_age,
            exercise_chatbot.ask_location,
            exercise_chatbot.ask_disability,
            exercise_chatbot.ask_preference,
            exercise_chatbot.ask_goal,
            exercise_chatbot.ask_health_condition,
            exercise_chatbot.ask_hour,
            exercise_chatbot.ask_preferred_sport,
            exercise_chatbot.ask_preferred_frequency,
            exercise_chatbot.ask_priority,
            exercise_chatbot.recommend_program
        ]
        #현재 어떤 질문을 물어봐야하는지 나타내는 것
        self.current_question_index = 0
        self.panel = None

    #다음 질문을 하기 위해 1씩 증가
    def next_question(self, event=None):
        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]()
            self.current_question_index += 1
            return question
        
    #panel 라이브러리를 사용하여 대화형 위젯 생성
    def create_panel(self):
        self.panel = pn.Column(
            pn.bind(self.next_question, self),
            sizing_mode="scale_both"  #가로, 세로크기를 모두 비율에 따라 조절
        )
        return self.panel


# 패널 생성
exercise_chatbot_panel = ExerciseChatbotPanel(exercise_chatbot)

# servable : panel을 서버에 연결
exercise_chatbot_panel.create_panel().servable().show()

