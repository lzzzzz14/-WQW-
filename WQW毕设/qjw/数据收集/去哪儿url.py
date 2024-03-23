import requests
from bs4 import BeautifulSoup
import pandas as pd

# 创建一个字典来存储你的 headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

# 爬取的基础URL
base_url = 'https://travel.qunar.com/p-cs300118-shenzhen-jingdian-3-{}'

# 用于存储提取的数据
data = {'Href': [], 'Description': [],'sight':[],'Ranking':[]}

# 遍历所有页面
for page in range(1, 21):  # 因为是1到20页，所以是range(1, 21)
    url = base_url.format(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 查找所有的<li>标签，它们的class为"item"
    items = soup.find_all('li', class_='item')
    
    # 遍历每个<li>标签
    for item in items:
        # 获取<a>标签的href属性
        a_tag = item.find('a', {'data-beacon': 'poi'})
        if a_tag:
            data['Href'].append(a_tag['href'])
        
        # 获取描述信息
        desbox = item.find('div', class_='desbox')
        if desbox:
            data['Description'].append(desbox.text.strip())

         # 在每个 'li' 元素中查找类名为 'cn_tit' 的 'span' 元素
        cn_tit_tag = item.find('span', class_='cn_tit')
        if cn_tit_tag:
        # 提取文本内容
            data['sight'].append(cn_tit_tag.text.strip())
            # text_content = cn_tit_tag.get_text(strip=True)
            # print(text_content)

        #  深圳景点排名
        ranking_tag_span = item.find('span',class_='ranking_sum')
        if ranking_tag_span:
            # 获取标签的文本内容，即景点排名
            data['Ranking'].append(ranking_tag_span.text.strip())
        
        #print(f"景点排名：{data}")


# 转换数据为DataFrame
df = pd.DataFrame(data)

# 保存DataFrame到Excel文件
df.to_excel('scraped_data.xlsx', index=False)

# 打印景点数量和页数
print(f"爬取的景点数量: {len(df)}")
print(f"爬取的页数: {page}")


