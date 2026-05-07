import requests

url = 'http://127.0.0.1:8000/create/'
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Token f14d8d9c842c8bc8c79cc04d21c2413c44ee64ef'
}

post_data = {
    "title": "Yangi post sarlavhasi 2",
    "content": "Bu postning mazmuni va matni bu yerda bo'ladi."
}

response = requests.post(url, headers=headers,json=post_data)
print(response)
if response.status_code == 201:
    print("Ishladi")
data = response.json()
print(data)
