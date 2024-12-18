import requests
import os
from dotenv import load_dotenv

load_dotenv()

endpoint = "http://localhost:8000/api/v1/images/"
headers = {
    'Authorization': f"Token {os.getenv('API_TOKEN')}"
}

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Use context manager to ensure file is properly closed
with open(os.path.join(script_dir, "tesseract-example-noisy.png"), "rb") as image_file:
    response = requests.post(
        endpoint,
        files={"image": image_file},
        headers=headers
    )

print("OCR Image created: \n", response.json())
print("STATUS CODE:", response.status_code, "\n-------------------")

print(f"Getting details from {endpoint + str(response.json()['id'])}")

response = requests.get(
    endpoint + str(response.json()['id']),
    headers=headers
)

print("OCR Image details: \n", response.json())
print("STATUS CODE:", response.status_code, "\n-------------------")

print(f"Getting results from {response.json()['result_url']}")

response = requests.get(
    response.json()['result_url'],
    headers=headers
)

print("OCR Image results: \n", response.json())
print("STATUS CODE:", response.status_code, "\n-------------------")



