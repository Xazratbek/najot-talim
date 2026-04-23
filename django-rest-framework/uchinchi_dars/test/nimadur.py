import requests

url = 'http://127.0.0.1:8000/'
res =  requests.get(url)
for i in range(len(res.json()['data'])):
    print(res.json()['data'][i]['title'])
    print(res.json()['data'][i]['summary'])