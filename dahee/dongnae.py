# 서울시 생활체육포털 우리동네 프로그램 csv 파일을 인코딩 후 불러오기
import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

df = pd.read_csv('dahee\data\서울시 생활체육포털 우리동네 프로그램.csv', encoding='cp949')

# 데이터 정보 확인
# print(df.info())

# 'dongnae' 데이터로 전처리
dongnae = df

# 컬럼명 변경
dongnae.rename(columns={'참가규모(명)':'정원수', '수혜기관명':'시설명','종목':'종목명'}, inplace=True)

# 컬럼명 확인
# print(dongnae.columns)

# 상위 5개 데이터 확인
# print(dongnae.head())

# '일시' 데이터를 분리해서 '요일'과 '시간 컬럼에 추가(둘 중 하나가 없는 경우 양쪽에 추가한 상태 -> 후처리 필요)
dongnae[['요일', '시간']] = None
for i in range(len(df['일시'])):
  if len(dongnae['일시'][i].split()) == 1:
    dongnae['요일'][i] = dongnae['일시'][i].split()[0]
    dongnae['시간'][i] = dongnae['일시'][i].split()[0]
  else:
    dongnae['요일'][i] = dongnae['일시'][i].split()[0]
    dongnae['시간'][i] = dongnae['일시'][i].split()[1]

# '내용' 데이터와 '종목명'데이터를 합쳐 '프로그램명' 컬럼에 추가(같은 데이터일 경우 둘 중 하나만 추가)
dongnae['프로그램명'] = None
for i in range(len(df)):
  if dongnae['내용'][i] != dongnae['종목명'][i]:
    dongnae['프로그램명'][i] = dongnae['내용'][i] + '[' + df['종목명'][i] + ']'
  else:
    dongnae['프로그램명'][i] = dongnae['내용'][i]

# '프로그램기간', '수강료', '접수방법', '접수기간' 컬럼 추가(추후 데이터 추가 작업 진행)
dongnae[['프로그램기간', '수강료', '접수방법', '접수기간']] = None

# 컬럼 삭제
dongnae = dongnae.drop(['일련번호', '지역구', '제목', '장소', '전화번호', '기관 홈페이지', '내용'], axis='columns')

# 컬럼 순서 변경
dongnae = dongnae[['시설명', '주소', '종목명', '프로그램명', '대상', '요일', '시간', '프로그램기간', '수강료',  '정원수', '접수방법', '접수기간']]

# 인코딩 후 csv 파일로 저장
dongnae.to_csv('dahee/data/dongnae.csv', mode='w', encoding='cp949', index=False)
