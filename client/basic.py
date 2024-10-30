import requests

endpoint = "https://httpbin.org/anything"

response = requests.get(endpoint, json={"query": "Hello, world!"})

print(response.json())


