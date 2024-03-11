import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

file_path = '../attractions.xlsx'

df = pd.read_excel(file_path)

site_names = df['景点名称'].tolist()
urls = df['网址'].tolist()

i = 0

for i in range(0, len(urls)):
# for i in range(1):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/122.0.0.0 Safari/537.36'
    }

    txt_path = f'../景点评价/{site_names[i]}.txt'

    response = requests.get(urls[i], headers=headers)

    if response.status_code == 200:
        html_doc = response.text
        soup = BeautifulSoup(html_doc, 'html.parser')
        module_content = soup.find('div', class_='moduleContent')
        extracted_text = ' '.join(module_content.stripped_strings)

    # print(extracted_text)

    with open(txt_path, 'w', encoding='utf-8') as file:
        file.write(extracted_text)

    i += 1
    print(f'{i}：{site_names[i]}')

    time.sleep(3)

