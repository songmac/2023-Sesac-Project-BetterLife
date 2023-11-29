import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_seq_items', None)

# csv 파일에서 DataFrame을 읽어오기
df = pd.read_csv('dahee/data/unique_data_code.csv', encoding='cp949')

# 종목명 띄어쓰기 삭제
for i in range(len(df['종목명'])):
    df['종목명'][i] = df['종목명'][i].replace(' ', '')

# 연령 변경
df.loc[df['연령']=='청소년', '연령'] = '학생'
print(df.head())

# 시설주소 열 추가
df['시설주소'] = None
for i in range(len(df['지번주소'])):
    df['시설주소'][i] = df['지번주소'][i].split()[1]

# 지번주소 열 삭제
df = df.drop(columns='지번주소')
print(df.head())

# 인코딩 후 csv 파일로 저장
df.to_csv('dahee/data/program.csv', mode='w', encoding='cp949', index=False)


