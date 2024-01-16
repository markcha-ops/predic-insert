import requests
import json

class Client:
    def __init__(self, start = "2024-01-15T09:51:00Z", end = "2024-01-16T09:39:00Z", tagname = "", calcType="TREND"):
        self.url = 'http://localhost:8089/api/data/raw';
        self.headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxIiwidXNlcm5hbWUiOiJhZG1pbiIsImF1dGgiOlsiUk9MRV9BRE1JTiJdLCJleHAiOjE2OTk2MDMxODV9.6ZYiXfs8ol3W6lMXsFb_9bS2V7zBWgkBWFpk5rm8YZVtbFtLjEf1oP2U7Op5NChvnj0BoyO1KvCJ0Ohlz57ObQ',
        'Content-Type': 'application/json'
    };
        self.data = {
        "name": "value",
        "total": True,
        "sum": False,
        "group": False,
        "rangeStart": start,
        "rangeEnd":end ,
        "searchStart": start,
        "searchEnd": end,
        "interval": "1m",
        "labels": {
            tagname:  {
                "scale": 1.0, "type": calcType, "groups": []
            }
        }
    };

    def requset(self):

        # 함수 호출하여 데이터 가져오기
        try:
            response = requests.post(self.url, headers=self.headers, data=json.dumps(self.data))
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error fetching data: {response.status_code} - {response.text}")
        except Exception as e:
            print(e)