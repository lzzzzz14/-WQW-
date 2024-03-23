import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os


# 获取当前脚本的绝对路径
current_directory = os.path.dirname(os.path.abspath(__file__))
excel_path = os.path.join(current_directory, 'comments_data.xlsx')

# 从Excel文件中读取URL列表
excel_data = pd.read_excel(excel_path)
# 这里我们直接使用 excel_data DataFrame，因为我们会在这个DataFrame上添加新的列
user_urls = excel_data['User URL'].tolist()  # 假设用户URL的列名是 'User URL'

# 创建一个字典来存储你的 headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}


# 用于保存所有用户数据的列表
all_user_data = []

# 遍历每个用户的 URL
for index, user_url in enumerate(user_urls, start=1):

    # 检查URL是否有效
    if pd.isnull(user_url) or user_url.strip() == 'N/A':
        continue

    full_url = 'https:' + user_url if 'http' not in user_url else user_url
    user_data = {'User URL': full_url, 'Visited Spots': []}

    try:
        # 发送http请求
        response = requests.get(full_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # 查找所有包含景点名称的<a>标签


            # 提取用户名称，假设用户名称在<span>标签的class 'name' 中
            user_name_tag = soup.find('span', class_='name')
            user_data['User Name'] = user_name_tag.get_text(strip=True) if user_name_tag else 'N/A'


            # 提取所有访问过的景点
            spots = soup.find_all('a', class_='tit')  # 请根据实际HTML结构调整此选择器
            for spot in spots:
                user_data['Visited Spots'].append(spot.get_text(strip=True))
        
            # 提取访问该景点的时间
            visit_time = soup.find('div', class_='from-detail').get_text(strip=True) if soup.find('div', class_='from-detail') else 'N/A'
        
            # 添加数据到列表中
            all_user_data.append(user_data)
        
             # 打印提取的数据
            print(f"Processed User {index}: {user_data['User Name']} - {len(user_data['Visited Spots'])} Spots")
        
        # 适当延迟以避免过快发送请求
        time.sleep(1)
    except Exception as e:
        print(f"Error processing user URL {full_url}: {e}")
        

# 转换提取的数据为pandas DataFrame
df_users = pd.DataFrame(all_user_data)

# 保存到Excel文件
df_users.to_excel('user_visited_spots_details.xlsx', index=False)

print("数据已成功保存到 Excel 文件。")
