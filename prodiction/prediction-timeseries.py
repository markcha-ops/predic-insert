
from tag.tag_client import TagClient
from TimesereisData.data_fetcher import Client
from dataProcess.process_data import processing
import time
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
with TagClient() as client:
    data = client.get_data()
# 필요한 파라미터 정의

# 데이터 가져오기
start_time = time.time()  # 루프 시작 시간 기록
processed_items = 0      # 처리된 항목 수
for index, item in enumerate(data):
    processed_items += 1

    # 현재까지 소요된 시간 계산
    current_time = time.time()
    elapsed_time = current_time - start_time

    # 진척도와 예상 소요 시간 계산
    progress = (index + 1) / len(data)
    estimated_total_time = elapsed_time / progress
    estimated_remaining_time = estimated_total_time - elapsed_time

    print(f"진척도: {progress:.2%}, 예상 남은 시간: {estimated_remaining_time:.2f}초")



    tagname = item['tagname']
    client = Client(end="2024-01-15T09:51:00Z", start="2024-01-10T09:39:00Z", tagname=tagname, calcType="TREND")
    tranning_data = client.requset()

    import pandas as pd
    import numpy as np
    # 주어진 데이터


    # 데이터를 DataFrame으로 변환
    df = pd.DataFrame(tranning_data)
    df.set_index('time', inplace=True)
    df.index = pd.DatetimeIndex(df.index, freq='T')
    import matplotlib.pyplot as plt

    df.plot(figsize=(10, 5))
    plt.show()

    import warnings
    import itertools
    warnings.filterwarnings("ignore")

    # 하이퍼파라미터 조합 생성
    p = d = q = range(0, 3)
    pdq = list(itertools.product(p, d, q))

    best_aic = np.inf
    best_pdq = None
    best_model = None
    from statsmodels.tsa.arima.model import ARIMA
    # 하이퍼파라미터 탐색
    for param in pdq:
            try:
                    model = ARIMA(df['value'], order=param)
                    results = model.fit()

                    if results.aic < best_aic:
                            best_aic = results.aic
                            best_pdq = param
                            best_model = results
            except:
                    continue

    # print(f"Best ARIMA{best_pdq} model - AIC:{best_aic}")
    # print(11111111111111111111)
    # 미래 값 예측
    forecast = best_model.forecast(steps=1428)
    forecast = pd.DataFrame(forecast)
    # print(forecast)


    processing.increaseData(forecast)
    # print(11111111111111111111)
    # processing.decision(forecast, 100)


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