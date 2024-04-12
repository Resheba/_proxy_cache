import requests

url = "https://gsr-rabota.ru/api/v2/Vacancies/All/List"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
