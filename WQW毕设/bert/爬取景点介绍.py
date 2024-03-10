import requests
from bs4 import BeautifulSoup

url = 'https://you.ctrip.com/sight/shenzhen26/2778.html'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    paragraphs = soup.find_all('p', class_='inset-p')
    extracted_text = [p.get_text() for p in paragraphs]
    print(extracted_text)

file_path = '1'

with open(file_path, 'w', encoding='utf-8') as file:
    for line in extracted_text:
        file.write(line + "\n")

