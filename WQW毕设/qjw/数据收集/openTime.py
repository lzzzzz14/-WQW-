import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

# 获取当前脚本的绝对路径
current_directory = os.path.dirname(os.path.abspath(__file__))

# 构建scraped_data.xlsx的完整路径
excel_path = os.path.join(current_directory, 'scraped_data.xlsx')


# 读取Excel文件中的URL
excel_data = pd.read_excel(excel_path)
urls = excel_data['Href'].tolist()  # 假设URL列名为'Href'

# 用于存储提取的数据
data = {'Scenic Name': [], 'Introduction': [], 'Ticket Price': [], 'Opening Hours': []}

# 遍历每个景点的URL
for index, url in enumerate(urls, start=1):
    print(f"正在处理第{index}个景点: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 提取景点名称
    scenic_name = soup.find('h1', class_='tit').text.strip() if soup.find('h1', class_='tit') else 'N/A'
    data['Scenic Name'].append(scenic_name)
    
    # 提取景点介绍
    introduction_section = soup.find('div', class_='e_db_content_box')
    introduction = ' '.join(p.text.strip() for p in introduction_section.find_all('p')) if introduction_section else 'N/A'
    data['Introduction'].append(introduction)
    
    # 提取门票价格
    ticket_price_section = soup.find('div', class_='e_db_content_box e_db_content_dont_indent')
    ticket_price = ticket_price_section.text.strip() if ticket_price_section else 'N/A'
    data['Ticket Price'].append(ticket_price)
    
    # 提取开放时间
    opening_hours_section = soup.find('div', class_='e_summary_list clrfix')
    opening_hours = ' '.join(p.text.strip() for td in opening_hours_section.find_all('td', class_='td_r') for p in td.find_all('p')) if opening_hours_section else 'N/A'
    data['Opening Hours'].append(opening_hours)

    # 在每个请求之间添加适当的延时
    time.sleep(1)

# 转换数据为DataFrame
df = pd.DataFrame(data)

# 保存DataFrame到Excel文件
df.to_excel('scenic_details.xlsx', index=False)

print("数据已成功保存到Excel文件。所有景点处理完毕。")
