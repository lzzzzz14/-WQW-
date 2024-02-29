import time

import requests
from bs4 import BeautifulSoup

base_url = 'https://you.ctrip.com/sight/shenzhen26/s0-p{}.html#sightname'

# 创建一个字典来存储你的 headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

# 总的景点数量
total_sight_count = 0

# 循环页面编号从1-20
for page_num in range(1, 21):
    url = base_url.format(page_num)
    print(f"正在处理页面: {url}")

    # 发送GET请求
    response = requests.get(url, headers=headers)

    # 假设response.text是你从requests得到的HTML内容
    html_content = response.text

    if response.status_code == 200:
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # 找到所有包含景点信息的容器
        sight_items = soup.find_all('div', class_='rdetailbox')

        # 遍历每个景点容器
        for item in sight_items:
            # 提取景点的名称
            sight_name_tag = item.find('a')
            if sight_name_tag and 'title' in sight_name_tag.attrs:
                sight_name = sight_name_tag['title'].strip()

            # 提取景点的热度分数
            hot_score_tag = item.find('b', class_='hot_score_number')
            hot_score = hot_score_tag.text.strip() if hot_score_tag else "No Score"

            # 提取景点的评分
            # 根据新的截图，评分在<a class="score">标签内的<strong>标签里
            score_tag = item.find('a', class_='score')
            if score_tag:
                rating_tag = score_tag.find('strong')
                rating = rating_tag.text.strip() if rating_tag else "No Rating"

            # 提取点评数量
            comment_tag = item.find('a', class_='recomment')
            if comment_tag:
                # 从文本中提取括号内的数字
                comments_text = comment_tag.text.strip()
                comments_number = comments_text.strip('()').split('条')[0]  # 假设格式始终如"(123条点评)"
            else:
                comments_number = "No Comments"

            # 打印景点名称、热度分数和评分
            print(f"景点名称: {sight_name}, 热度分数: {hot_score}, 评分: {rating}, 点评数量: {comments_number}")

            # 景点计数器增加
            total_sight_count += 1
    else:
        print(f"访问页面 {url} 出错，状态码: {response.status_code}")

    # 稍作延时，避免过于频繁的请求
    time.sleep(1)

# 打印总的景点数量
print(f"总共打印了 {total_sight_count} 个景点的信息。")


