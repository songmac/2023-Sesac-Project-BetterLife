# 서울시 공공 체육시설별 운영프로그램 정보 csv 파일을 인코딩 후 불러오기
import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

df = pd.read_csv('dahee\data\서울시 공공 체육시설별 운영프로그램 정보.csv', encoding='cp949')

# 데이터 정보 확인
# print(df.info())

# 'program' 데이터로 전처리
program = df

# 컬럼 확인
# print(program.columns)

# 컬럼 삭제
program = program.drop(['종목시설명', '장소', '홈페이지', '주차면(면)', '문의전화', 'FAX', '이메일', '반명', '레벨', '프로그램소개', '선별방법', '온라인예약링크', '사용여부(센터에서 강좌오픈여부)', '강좌시작일', '강좌종료일', '가격무료확인'], axis='columns')

# 컬럼명 변경
program.rename(columns={'진행시간(1회)':'시간', '수강료(원)':'수강료','전체정원수':'정원수', '기간':'프로그램기간'}, inplace=True)

# 컬럼 순서 변경
program = program[['시설명', '주소', '종목명', '프로그램명', '대상', '요일', '시간', '프로그램기간', '수강료',  '정원수', '접수방법', '접수기간']]

# 상위 5개 데이터 확인
# print(program.head())

# 인코딩 후 csv 파일로 저장
program.to_csv('dahee/data/program.csv', mode='w', encoding='cp949', index=False)