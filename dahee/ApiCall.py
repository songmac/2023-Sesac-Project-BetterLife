from dotenv import load_dotenv
import requests
import os

load_dotenv()

# 서울시 체육시설 공공서비스예약 정보
service_api_key = os.environ.get('SEOUL_SERVICE_RESERVATION_API_KEY')

service_url = 'http://openAPI.seoul.go.kr:8088/'+service_api_key+'/json/ListPublicReservationSport/1/5/'

jsonService = requests.get(service_url).json()
# print(jsonService)

# 서울시 공공 체육시설별 운영프로그램 정보
program_api_key = os.environ.get('SEOUL_WORKOUT_PROGRAM_API_KEY')

program_url = 'http://openAPI.seoul.go.kr:8088/'+program_api_key+'/json/ListProgramByPublicSportsFacilitiesService/1/5/'

jsonProgram = requests.get(program_url).json()
print(jsonProgram)

# 성동구 도시관리공단 체육시설 강좌정보
seongdong_lecture = requests.get('https://sports.happysd.or.kr/rest/common/PublicData?serviceTypeCode=1')
# print(seongdong_lecture.text)

# # 성동구 도시관리공단 공공시설 개방정보
# seongdong_facility = requests.get('https://sports.happysd.or.kr/rest/common/PublicData?serviceTypeCode=2')
# # print(seongdong_facility.text)

# # 관악구 종합강좌정보
gwanak_program = requests.get('	https://data.gwanak.go.kr/openinf/sheetview.jsp?infId=OA-12723')
# print(gwanak_program.text)