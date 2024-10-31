import requests
import os

endpoint = "http://localhost:8000/api/v1/"

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Use context manager to ensure file is properly closed
with open(os.path.join(script_dir, "tesseract-example-noisy.png"), "rb") as image_file:
    response = requests.post(endpoint, files={
        "image": image_file
    })

print("OCR Results:", response.json())
print("STATUS CODE:", response.status_code)


