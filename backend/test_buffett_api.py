import requests

response = requests.get("http://localhost:8000/api/buffet-analysis/?ticker=AAPL")
print(response.status_code)
print(response.text)
