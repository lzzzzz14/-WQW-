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
urls = excel_data['Href'].tolist()  # URL列名为'Href'

# 用于存储提取的数据
data = {
    'User Rating': [],
    'User Comment': [],
    'User URL': [],
    'User Name': []
}

# 设置请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# ...之前的代码...

# 遍历每个景点的 URL
for index, url in enumerate(urls, start=1):
    try:
        print(f"正在处理第 {index} 个景点的 URL: {url}")
        
        # 发送请求
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 遍历每个评论项
        for comment_item in soup.find_all('li', class_='e_comment_item clrfix'):
            # 提取用户评分
            # 提取用户评分
            user_rating_tag = comment_item.find('span', class_='cur_star star_0')
            user_rating = ' '.join(user_rating_tag['class']) if user_rating_tag else 'N/A'

            
            # 提取用户文字评论
            # 提取用户文字评论，合并所有的 p 标签中的文本
            user_comments = comment_item.find_all('p')
            user_text_comment = ' '.join(p.get_text(strip=True) for p in user_comments) if user_comments else 'N/A'

            
           # 在comment_item中定位含有用户信息的div
            user_info_div = comment_item.find('div', class_='e_comment_usr_name')

            # 提取用户 URL
            user_link = user_info_div.find('a', rel='nofollow') if user_info_div else None
            user_url = user_link['href'] if user_link else 'N/A'

            # 提取用户名称
            user_name = user_link.get_text(strip=True) if user_link else 'N/A'

            
            # 添加数据到字典中
            data['User Rating'].append(user_rating)
            data['User Comment'].append(user_text_comment)
            data['User URL'].append(user_url)
            data['User Name'].append(user_name)
        
        # 适当延迟以避免过快发送请求
        time.sleep(1)
    except Exception as e:
        print(f"在处理 {url} 时发生错误: {e}")
        continue


# 将数据转换为 DataFrame
df = pd.DataFrame(data)

# 保存 DataFrame 到 Excel 文件
output_excel_path = 'comments_data.xlsx'
df.to_excel(output_excel_path, index=False)

print("数据已成功保存到 Excel 文件。")
