import requests
# ip = "7.239.175.229"
# ip = "192.168.0.46"
ip = "127.0.0.1"
url = 'http://{}:8886/api/v2/delete?org=primary&bucket='.format(ip)
buckets = {
    'source': ['source'],
    # 'history': ['minute', 'hour', 'day', 'month', 'year']
    # 'history': ['year']
}

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Token admintoken123'
}
start = "2024-01-15T09:53:00Z"
end = "2024-01-16T09:39:00Z"
tagnames = [
    # "U003_PWR_kWh",
# "V014_LNG_Usage"
# "8bf3a62b-3cd5-467e-a6e6-93a2dca66415",
# "4b55af71-ebde-4e1e-a12e-81a042d4ecb4",
# "e8f95d1a-35cc-457a-8973-ee8d40de0f8f",
# "a45faabf-2693-4a99-b9e7-1eb2fccfd51c",
# "8a7927e3-c8a1-4105-a9a2-4003e0b2cfb6",
# "1385238a-617e-4b83-9867-7ea1c519d7de",
# "87d00cba-8fff-4324-9e10-48822694bb9c",
# "faac504a-4a26-4072-a48f-7e32c780ab1d",
# "4a81ee13-b517-45fd-97c8-5aac6edf8bb2",
# "8f426a80-d044-44fc-bd48-8aa670c56b9e",
# "ebfb452d-832d-45c3-b5d6-ea7c92bf88d3",
# "362f4573-a3fb-4061-96e0-2ddf0b32a7aa",
# "9b1cac62-ed7a-4f37-a877-fe4a2d686a15",
# "b6ae6445-7726-45a9-b792-4ca76693e79c",
# "012f113d-919a-4a6c-8051-1f552a06c12d",
# "b4e3b76d-2b3b-4d62-afc1-0e98cbd272ec",
# "036da6db-e6e1-4d84-ba70-5a1cb9f6f8be",
# "b2f5ba42-045d-45ab-be9e-44d619b34cfd",
# "bef2fd23-1feb-4e70-becc-096dcf034583",
# "5d0d56c7-fc8a-4cc7-9f1b-f37fc39b8117",
# "19939d07-c246-45a4-b375-a1c572ffc50a",
# "306bb5f2-65cf-41bc-98dc-9d13ec157f82",
# "38df8cb4-4926-4c49-b781-9e7ad84f03f9",
# "8602f4d6-8eff-4789-b286-7dcbf12a6254",
# "31317a20-9b77-4c67-8b6a-3972f441b548",
# "b8332227-32d4-4122-bc0e-e29dc7b33b74"
]
# for tagname in tagnames:
for bucket, measurements in buckets.items():
    urlName = url + bucket
    print(bucket)
    for measurement in measurements:
        data = {
            "start": start,
            "stop": end,
            # "predicate": '''_measurement=\"{}\" AND tagname=\"{}\"'''.format(measurement, tagname)
            "predicate": '''_measurement=\"{}\"'''.format(measurement)
        }
        print(urlName)
        print(data)
        response = requests.post(urlName, headers=headers, json=data)

        print(response.status_code)
        print(response.text)