import pandas as pd

class processing:
    def increaseData(forecast):
        forecast['diff'] = forecast['predicted_mean'].diff()
        decreasing_values = forecast['diff'] < 0

        # 감소하는 값의 전후 평균으로 업데이트
        for idx in forecast[decreasing_values].index:
            if idx > forecast.index[0] and idx < forecast.index[-1]:
                before = forecast.loc[idx - pd.Timedelta(minutes=1), 'predicted_mean']
                after = forecast.loc[idx + pd.Timedelta(minutes=1), 'predicted_mean']
                forecast.loc[idx, 'predicted_mean'] = (before + after) / 2

    def decision(forecast, last_value):
        excess = forecast['predicted_mean'].iloc[-1] - last_value
        if excess <= 0.0:
            return
        # 마지막 값부터 시작하여 누적으로 초과분을 빼기
        len1 = len(forecast) - 1
        for i in range(len(forecast)):

            # 현재 위치에서 뺄 수 있는 최대값 계산 (현재 값 또는 남은 초과분 중 작은 값)
            rate = excess * (i / len1)

            # 값 조정
            forecast['predicted_mean'].iloc[i] -= rate

            # 초과분이 0이 되면 종료
            if excess <= 0:
                break

        forecast['adjusted'] = forecast['predicted_mean']

    def increasion(forecast, first_value):
        excess = first_value - forecast['predicted_mean'].iloc[0]
        if excess <= 0.0:
            return
        # 마지막 값부터 시작하여 누적으로 초과분을 빼기
        len1 = len(forecast) - 1
        for i in range(len(forecast)-1):

            # 현재 위치에서 뺄 수 있는 최대값 계산 (현재 값 또는 남은 초과분 중 작은 값)
            rate = excess * ((len1 - i) / len1)
            # if rate + forecast['predicted_mean'].iloc[i] > forecast['predicted_mean'].iloc[i+1]:

            # 값 조정
            forecast['predicted_mean'].iloc[i] += rate
            excess -= rate
            # 초과분이 0이 되면 종료
            if excess <= 0:
                break

        forecast['adjusted'] = forecast['predicted_mean']