
from tag.tag_client import TagClient
from TimesereisData.data_fetcher import Client
from dataProcess.process_data import processing
import time
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime, timedelta
from statsmodels.tsa.statespace.sarimax import SARIMAX
import numpy as np
import warnings
import itertools
import pandas as pd
warnings.filterwarnings("ignore")

with TagClient() as client:
    data = client.get_data()
# 필요한 파라미터 정의

# 데이터 가져오기
start_time = time.time()  # 루프 시작 시간 기록
processed_items = 0      # 처리된 항목 수
data = data[::-1]
for index, item in enumerate(data):

    processed_items += 1
    print(item['tagname'])
    # 현재까지 소요된 시간 계산
    current_time = time.time()

    # 진척도와 예상 소요 시간 계산
    progress = (index + 1) / len(data)

    print(f"진척도: {progress:.2%}")
    tagname = item['tagname']
    if (tagname[0] == 'V'):
        continue
    client = Client(start="2024-01-14T23:51:00Z", end="2024-01-16T18:39:00Z", tagname=tagname, calcType="TREND")
    find_data = client.requset()
    find_zero = False
    start_record_time = ""
    start_before_value = 0
    stop_record_time = ""
    stop_before_value = 0
    before_value = 0
    for row in find_data:
        value = row['value']
        if (value <= 0):
            if find_zero is False:
                start_record_time = row['time']
                start_before_value = before_value
                find_zero = True
        if find_zero is True:
            if (value > 0):
                stop_record_time = row['time']
                stop_before_value = value
                break
        before_value = value
    if stop_before_value == 0:
        stop_before_value = before_value
        stop_record_time = find_data[len(find_data) - 1]['time']
    start_time = datetime.fromisoformat(start_record_time + "+00:00")
    start_time = start_time - timedelta(minutes=1)
    end_time = datetime.fromisoformat(stop_record_time + "+00:00")

    isoformat = start_time.isoformat()
    z_ = isoformat[:19] + 'Z'
    client = Client(end=z_, start="2024-01-01T09:39:00Z", tagname=tagname, calcType="TREND")
    time_difference = end_time - start_time

    predit_cnt = int(time_difference.total_seconds() / 60)
    tranning_data = client.requset()

    # 주어진 데이터


    # 데이터를 DataFrame으로 변환
    df = pd.DataFrame(tranning_data)
    df.set_index('time', inplace=True)
    df.index = pd.DatetimeIndex(df.index, freq='T')

    print(df)
    # 하이퍼파라미터 조합 생성
    p = d = q = range(0, 3)
    pdq = list(itertools.product(p, d, q))

    best_aic = np.inf
    best_pdq = None
    best_model = None
    from statsmodels.tsa.arima.model import ARIMA

    p = 2  # 자기회귀 항의 차수
    d = 1  # 차분의 차수
    q = 2  # 이동 평균 항의 차수

    # 모델 훈련
    model = SARIMAX(df['value'], order=(1, 1, 1), seasonal_order=(0,0,0,0))
    model_fit = model.fit()

    # print(f"Best ARIMA{best_pdq} model - AIC:{best_aic}")
    # print(11111111111111111111)
    # 미래 값 예측
    forecast = model_fit.forecast(steps=predit_cnt)
    forecast = pd.DataFrame(forecast)
    # print(forecast)

    print(forecast)
    processing.increaseData(forecast)
    # print(11111111111111111111)
    print(stop_before_value)
    processing.decision(forecast, stop_before_value)
    print(start_before_value)
    processing.increasion(forecast, start_before_value)
    print(forecast)
    import pandas as pd




    url = "http://localhost:8886"  # InfluxDB 서버 URL
    token = "admintoken123"           # InfluxDB 접근 토큰
    org = "primary"      # 조직 이름
    bucket = "source"         # 버킷 이름

    # InfluxDB 클라이언트 생성
    client = InfluxDBClient(url=url, token=token, org=org)
    write_api = client.write_api(write_options=SYNCHRONOUS)

    # 데이터 프레임의 각 행에 대해 InfluxDB 포인트 생성 및 작성
    points = []

    for timestamp, row in forecast.iterrows():
        point = Point("source") \
            .tag("tagname", tagname) \
            .field("value", row['predicted_mean']) \
            .field("state", "good") \
            .time(timestamp)
        points.append(point)
    write_api.write(bucket=bucket, org=org, record=points)

    # 클라이언트 종료
    client.close()