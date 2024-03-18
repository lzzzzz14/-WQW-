import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# 获取当前脚本的绝对路径
current_directory = os.path.dirname(os.path.abspath(__file__))
excel_path = os.path.join(current_directory, 'scraped_data.xlsx')

# 从Excel文件中读取URL列表
excel_data = pd.read_excel(excel_path)
urls = excel_data['Href'].tolist()  # 假设URL列名为'Href'

# 用于存储提取的数据
data = {'Scenic Name': [], 'User Name': [], 'User URL': [], 'User Comment': []}

# 遍历每个景点的URL
for index, url in enumerate(urls, start=1):
    # 打印当前处理的景点编号和URL，显示进度
    print(f"Processing scenic spot {index}/{len(urls)}: {url}")
    
    # 请求页面内容
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 提取景点名称
    scenic_name = soup.find('h1', class_='tit').get_text(strip=True) if soup.find('h1', class_='tit') else 'N/A'
    
    # 遍历每个评论项
    for comment_item in soup.find_all('li', class_='e_comment_item clrfix'):
        user_name = comment_item.find('div', class_='e_comment_usr_name').get_text(strip=True) if comment_item.find('div', class_='e_comment_usr_name') else 'N/A'
        user_url = comment_item.find('a', rel='nofollow')['href'] if comment_item.find('a', rel='nofollow') else 'N/A'
        user_comment = ' '.join(p.get_text(strip=True) for p in comment_item.find_all('p', class_='e_comment_content')) if comment_item.find('p', class_='e_comment_content') else 'N/A'
        
        # 添加数据到字典中
        data['Scenic Name'].append(scenic_name)
        data['User Name'].append(user_name)
        data['User URL'].append(user_url)
        data['User Comment'].append(user_comment)
    
    # 适当延迟以避免过快发送请求
    time.sleep(1)

# 将数据转换为DataFrame
df = pd.DataFrame(data)

# 保存DataFrame到Excel文件
output_path = os.path.join(current_directory, 'comments_data.xlsx')
df.to_excel(output_path, index=False)

print("Data has been successfully saved to Excel.")
