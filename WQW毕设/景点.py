import requests

url = 'https://you.ctrip.com/sight/shenzhen26/2778.html'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers)

print(response.status_code)

html_content = response.text

file_path = 'sight.html'

with open(file_path, 'w', encoding='utf-8') as file:
    file.write(html_content)

print(file_path)