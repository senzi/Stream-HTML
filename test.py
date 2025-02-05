import requests

response = requests.post(
    'http://localhost:5000/v1/chat/completions',
    stream=True
)

for line in response.iter_lines():
    if line:
        print(line.decode('utf-8'))