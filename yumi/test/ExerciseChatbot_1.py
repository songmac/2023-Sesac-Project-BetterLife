import panel as pn
 
#질문을 위한 챗봇 class
class ExerciseChatbot:
    
    def __init__(self):
        self.user_data = {}

    #챗봇 첫인사
    def greet_user(self):
        return pn.pane.Markdown("## 안녕하세요! 저는 공공 운동 프로그램을 추천을 도와주는 챗봇입니다. \n"
                                "지금부터 여러 가지 질문을 통해 사용자에게 맞춤형 운동 프로그램을 추천해 드리겠습니다. \n"
                                "먼저 몇 가지 개인 정보를 알아보겠습니다.")

    def ask_age(self):
        # print("당신의 연령대가 어떻게 되나요?")
        # print("1: 학생 2: 성인 3: 노인")
        # age = input("번호를 입력해 주세요: ")
        # self.user_data['age'] = age
        return pn.pane.Markdown("### 당신의 연령대가 어떻게 되나요?\n"
                                "1: 학생 2: 성인 3: 노인")

    def ask_location(self):
        # location = input("당신이 선호하는 지역을 알려주세요 (예시: 중구, 종로구, 마포구 등)")
        # self.user_data['location'] = location
        return pn.pane.Markdown("### 당신이 선호하는 지역을 알려주세요 (예시: 중구, 종로구, 마포구 등)")
        
    def ask_disability(self):
        # print("장애 여부를 알려주세요")
        # print("1: 없음")
        # print("2: 있음")
        # disability = input("번호를 선택해 주세요:")
        # self.user_data['disability'] = disability
        return pn.pane.Markdown("### 장애 여부를 알려주세요\n"
                                "1: 없음\n"
                                "2: 있음")

    def ask_preference(self):
        # print("이제는 운동에 대한 몇 가지 선호사항을 알아보겠습니다.")
        return pn.pane.Markdown("## 이제는 운동에 대한 몇 가지 선호사항을 알아보겠습니다.")
        
    def ask_goal(self):
        # print("어떤 목표로 운동을 하시려나요?")
        # print("1: 체중관리 및 다이어트")
        # print("2: 스트레스 해소 및 심리적 향상")
        # print("3: 근력 및 근지구력 향상")
        # print("4: 체형관리 및 개선")
        # print("5: 사회적 활동 및 취미")
        # print("6: 성능 향상 및 목표 도달")
        # goal = input("번호를 입력해주세요: ")
        # self.user_data['goal'] = goal
        return pn.pane.Markdown("### 어떤 목표로 운동을 하시려나요?\n"
                                "1: 체중관리 및 다이어트\n"
                                "2: 스트레스 해소 및 심리적 향상\n"
                                "3: 근력 및 근지구력 향상\n"
                                "4: 체형관리 및 개선\n"
                                "5: 사회적 활동 및 취미\n"
                                "6: 성능 향상 및 목표 도달")
    
    def ask_health_condition(self):      
        # print("아래 건강 상태 중 어떤 문제를 갖고 있나요? (하나만 선택해 주세요)")
        # print("1: 관절 및 근육 상태 (관절염, 근육 경련, 근육 약화 등)")
        # print("2: 심폐 기능 (심혈관 질환, 호흡기 문제)")
        # print("3: 당뇨 관리 (혈당 관리)")
        # print("4: 스트레스 관리")
        # print("5: 우울증 및 불안")
        # print("6: 수면 문제")
        # print("7: 대사 증후군 및 대사 질환 (당뇨, 고혈압 등 대사 관련 질환)")
        # print("8: 호르몬 수준")
        # health_conditions = input("번호를 입력해주세요: ")
        # self.user_data['condition'] = health_conditions
        return pn.pane.Markdown("### 아래 건강 상태 중 어떤 문제를 갖고 있나요? (하나만 선택해 주세요)\n"
                                "1: 관절 및 근육 상태 (관절염, 근육 경련, 근육 약화 등)\n"
                                "2: 심폐 기능 (심혈관 질환, 호흡기 문제)\n"
                                "3: 당뇨 관리 (혈당 관리)\n"
                                "4: 스트레스 관리\n"
                                "5: 우울증 및 불안\n"
                                "6: 수면 문제\n"
                                "7: 대사 증후군 및 대사 질환 (당뇨, 고혈압 등 대사 관련 질환)\n"
                                "8: 호르몬 수준")
        
    def ask_hour(self) :
        # print("어떤 시간대에 운동하는 것을 선호하시나요?")
        # print("1:새벽 2: 오전 3: 오후 4: 저녁 5: 무관")
        # hour = input("번호를 입력해 주세요:")
        # self.user_data['hour'] = hour
        return pn.pane.Markdown("### 어떤 시간대에 운동하는 것을 선호하시나요?\n"
                                "1: 새벽 2: 오전 3: 오후 4: 저녁 5: 무관")
        
    def ask_preferred_sport(self) :
        # print("어떤 종류의 운동을 선호하시나요?")
        # print("1.구기및라켓 2.레저 3.무도 4.무용 5.민속 6.재활 7.체력단련및생활운동")
        # sports = input(":")
        # self.user_data['sports'] = sports
        return pn.pane.Markdown("### 어떤 종류의 운동을 선호하시나요?\n"
                                "1. 구기및라켓 2. 레저 3. 무도 4. 무용 5. 민속 6. 재활 7. 체력단련및생활운동")
        
    def ask_preferred_frequency(self) :
    #     print("주당 몇 회 정도의 운동을 선호하시나요?")
    #     print("1: 주1회 2: 주2회 3: 주3회 4: 주4회이상")
    #     preferred_frequency = input("번호를 입력해주세요 :")
    #     self.user_data['preferred_frequency'] = preferred_frequency
        return pn.pane.Markdown("### 주당 몇 회 정도의 운동을 선호하시나요?\n"
                                "1: 주1회 2: 주2회 3: 주3회 4: 주4회 이상")
        
    def ask_priority(self) :
        # print("현재 항목 중 가장 중요하게 여기는 것이 무엇인가요?")
        # print("1.건강상태 2.운동목표 3.연령대 4.거주지 5.선호빈도 6.선호시간대 7.선호인원수")
        # priority = input("번호를 입력해주세요 :")
        # self.user_data['priority'] = priority
         return pn.pane.Markdown("### 현재 항목 중 가장 중요하게 여기는 것이 무엇인가요?\n"
                                "1. 건강상태 2. 운동목표 3. 연령대 4. 거주지 5. 선호빈도 6. 선호시간대 7. 선호인원수")

    def recommend_program(self):
        # print("\n사용자 정보:")
        # print(f"나이: {self.user_data['age']}세")
        # print(f"거주지: {self.user_data['location']}")
        # print(f"장여여부 : {self.user_data['disability']}")
        # #print(f"운동 목표: {'체력단련' if self.user_data['goal'] == '1' else '심폐기능단련'}")
        # print(f"운동 목표: {self.user_data['goal']}")
        # print(f"건강 상태 : {self.user_data['condition']}")
        # print(f"선호 시간대 : {self.user_data['hour']}")
        # print(f"선호 운동 : {self.user_data['sports']}")
        # print(f"선호 인원 : {self.user_data['preferred_frequency']}")
        # print(f"중요 항목 : {self.user_data['priority']}")
        return pn.pane.Markdown("\n## 사용자 정보:\n"
                                f"나이: {self.user_data['age']}세\n"
                                f"거주지: {self.user_data['location']}\n"
                                f"장여여부 : {self.user_data['disability']}\n"
                                f"운동 목표: {self.user_data['goal']}\n"
                                f"건강 상태 : {self.user_data['condition']}\n"
                                f"선호 시간대 : {self.user_data['hour']}\n"
                                f"선호 운동 : {self.user_data['sports']}\n"
                                f"선호 인원 : {self.user_data['preferred_frequency']}\n"
                                f"중요 항목 : {self.user_data['priority']}")
        

    #챗봇 질문 실행
    def run_chatbot(self):
        self.greet_user()
        self.ask_age()
        self.ask_location()
        self.ask_disability()
        self.ask_preference()
        self.ask_goal()
        self.ask_health_condition()
        self.ask_hour()
        self.ask_preferred_sport()
        self.ask_preferred_frequency()
        self.ask_priority()
        self.recommend_program()

# 챗봇 인스턴스 생성
exercise_chatbot = ExerciseChatbot()
# 챗봇 실행
#exercise_chatbot.run_chatbot()
app = pn.Column(
    exercise_chatbot.greet_user(),
    exercise_chatbot.ask_age(),
    exercise_chatbot.ask_location(),
    exercise_chatbot.ask_disability())
