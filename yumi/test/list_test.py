user_answers = ['학생', '종로구', '무', '수명연장', '구기및라켓', '새벽', '주1회']
result_program_names = ['수영', '필라테스', '헬스']
user_dic = {}

for idx, program_name in enumerate(result_program_names):
    # 새로운 리스트 생성하여 삽입
    updated_answer = user_answers[:2] + [program_name] + user_answers[2:]
    
    # user_dic에 저장
    user_dic[idx] = updated_answer

print(user_dic)
