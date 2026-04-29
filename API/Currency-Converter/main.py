import requests

response = requests.get('https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5')

if response.status_code == 200:
    data = response.json()
    print("Success:", data)

    for item in data:
        print(f"One {item['ccy']} costs {item['buy']} {item['base_ccy']}")

elif response.status_code == 404:
    print("Error: Resource not found")
else:
    print(f"Request failed with status code: {response.status_code}")