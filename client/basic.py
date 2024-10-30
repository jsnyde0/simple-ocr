import requests

endpoint = "http://localhost:8000/api/v1/"

response = requests.get(endpoint, params={"url_param": "test"}, json={"json_data": "test"})

print(response.json())
print("STATUS CODE:", response.status_code)


