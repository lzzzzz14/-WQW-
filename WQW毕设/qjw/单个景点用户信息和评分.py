from encodings import utf_8
import requests
from bs4 import BeautifulSoup
import pandas as pd

url_base = 'https://travel.qunar.com/p-oi709981-shenzhenyeshengdongwu-1-{}?rank=0#lydp'

# 创建一个字典来存储你的 headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

user_profiles = []
user_count = 0  #初始化用户计数器

for page_number in range(1, 40):
    url = url_base.format(page_number)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    user_boxes = soup.find_all('li', class_='e_comment_item clrfix')

    for user_box in user_boxes:
        user_profile = {}
        
        # 查找用户昵称的a标签
        user_a = user_box.find('div', class_='e_comment_usr_name').find('a', rel='nofollow')
        
        # 检查是否找到了a标签
        if user_a:
            user_count += 1 # 每找到一个用户，计数器加1
            user_profile['nickname'] = user_a.text.strip()
            user_profile['profile_url'] = user_a['href']

            #查找星级评分
            star_span = user_box.find('span', class_='cur_star')
            user_profile['star_rating'] = star_span['class'][-1] if star_span else 'N/A'

            user_profiles.append(user_profile)
            # 打印或存储用户个人资料
            # print(f"用户{user_count} - 昵称: {user_profile.get('nickname', 'N/A')}, 个人主页链接: {user_profile.get('profile_url', 'N/A')}, 星级评分: {user_profile['star_rating']}")

# 打印总用户数量
print(f"总用户数量: {user_count}")

# 创建一个 DataFrame 对象
df = pd.DataFrame(user_profiles)

# 将 DataFrame 写入 Excel 文件
df.to_excel('user_profiles.xlsx', index=False)