import requests

endpoint = "http://localhost:8000/api/v1/"

response = requests.get(endpoint)

print(response.text)
print("STATUS CODE:", response.status_code)


