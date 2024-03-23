import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


# 设置请求头
# 创建一个字典来存储你的 headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

# 获取当前脚本的绝对路径
# 使用os.getcwd()替换os.path.abspath(__file__)，特别是当你在Jupyter环境下运行时
current_directory = os.getcwd()
excel_path = os.path.join(current_directory, 'scraped_data.xlsx')

# 从Excel文件中读取URL列表
excel_data = pd.read_excel(excel_path)
scenic_urls = excel_data['Scenic URL'].tolist()  # URL列名为Scenic URL


# 存储最终数据的列表
data = []


# 遍历每个景点的URL
for base_url in scenic_urls:
    print(f"Processing: {base_url}")
    scenic_name = 'N/A'  # 初始化景点名称

    # 遍历每一页评论（1-5页）
    for page in range(1, 6):
        print(f"Fetching page {page}")
        url = f"{base_url}-1-{page}?rank=0#lydp"

        try:
            response = requests.get(url, headers=headers,timeout=10) #添加超时
            response.raise_for_status()  # 检查请求是否成功
            soup = BeautifulSoup(response.content, 'html.parser')

            # 仅在第一页时提取景点名称
            if page == 1:
                scenic_name_tag = soup.find('h1', class_='tit')
                if scenic_name_tag:
                    scenic_name = scenic_name_tag.get_text(strip=True)
                    print(f"Scenic Name: {scenic_name}")

            comment_items = soup.find_all('li', class_='e_comment_item clrfix')

            if not comment_items:  # 检查是否存在评论
                print("No comments found, moving to next scenic spot.")
                break


            # 遍历每个评论项
            for comment_item in comment_items:
                # 提取用户评分
                user_rating = 'N/A'
                user_rating_div_tag = comment_item.find('div', class_='e_comment_star_box')
                if user_rating_div_tag:
                    user_rating_span_tags = user_rating_div_tag.find_all('span')
                    if len(user_rating_span_tags) > 1:
                        user_rating = ' '.join(user_rating_span_tags[1]['class'])

                # 提取用户文字评论
                user_comments_tag = comment_item.find('div',class_='e_comment_content')
                user_comments = user_comments_tag.find_all('p')
                user_text_comment = ' '.join(p.get_text(strip=True) for p in user_comments) if user_comments else 'N/A'
                # print(f"text_comment: {user_text_comment}")

                # 定位含有用户信息的div
                user_info_div = comment_item.find('div', class_='e_comment_usr_name')
                user_link = user_info_div.find('a', rel='nofollow') if user_info_div else None
                user_url = user_link['href'] if user_link else 'N/A'
                user_name = user_link.get_text(strip=True) if user_link else 'N/A'

                # 将数据添加到列表中
                data.append({
                    'Scenic Name': scenic_name,
                    'User Name': user_name,
                    'User Rating': user_rating,
                    'User Comment': user_text_comment,
                    'User URL': user_url,
                    'Scenic URL': base_url
                })

            print(f"Completed page {page}")
            time.sleep(5)  # 适当延迟

           
        except requests.exceptions.RequestException as e:  # 更具体的异常捕获
            print(f"Error fetching page {page}: {e}")
            break
        

# 将结果转换为DataFrame
results_df = pd.DataFrame(data)

# 将数据保存为新的Excel文件
results_df.to_excel('scenic_comments.xlsx', index=False)
print("Data extraction complete. Saved to scenic_comments.xlsx.")