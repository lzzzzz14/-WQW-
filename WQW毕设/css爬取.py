from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import re
import time
import pandas as pd

file_path = 'attractions.xlsx'

df = pd.read_excel(file_path)

site_names = df['景点名称'].tolist()
urls = df['网址'].tolist()

for i in range(0, len(urls)):

    # 定义列标题
    columns = ["用户名", "评分", "评论时间", "IP所属地", "点赞数"]

    # 创建一个空的DataFrame
    df = pd.DataFrame(columns=columns)

    # 将这个空的DataFrame保存到一个新的Excel文件中
    excel_path = f'景点/{site_names[i]}.xlsx'  # 定义Excel文件的名称和路径
    df.to_excel(excel_path, index=False)  # 不包含索引

    print('已成功创建第', i+1, f'个Excel文件 {excel_path}，包含指定的列标题')

    # 评论计数器
    comment_count = 0

    # 指定ChromeDriver的路径
    chrome_driver_path = r'C:\Users\12570\Downloads\chromedriver-win64\chromedriver.exe'
    s = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=s)

    # 打开网页
    driver.get(urls[i])

    # 等待页面加载完成
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
    )

    # 循环从第二页跳转到第十页
    for page_num in range(1, 11):
        try:
            # 等待跳转输入框出现
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.ant-pagination-options-quick-jumper input"))
            ).clear()

            # 输入新的页码并跳转
            input_box = driver.find_element(By.CSS_SELECTOR, "div.ant-pagination-options-quick-jumper input")
            input_box.send_keys(str(page_num) + Keys.ENTER)

            # 等待页面加载完毕
            time.sleep(5)

            # 获取所有的评论元素
            comment_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.commentList > div.commentItem"))
            )

            # 遍历评论元素，提取相关信息
            for comment in comment_elements:

                # 创建一个列表用来存储数据
                data = []

                # 用户名
                username = comment.find_element(By.CSS_SELECTOR, "div.userName").text
                data.append(username)   # 加入用户名
                # 评分
                score_src = comment.find_element(By.CSS_SELECTOR, "span.averageScore > img.scoreIcon").get_attribute('src')
                score = re.search(r'score-(\d+).png', score_src).group(1)
                data.append(score)  # 加入评分

                # 评论时间和IP所属地
                comment_time_div = comment.find_element(By.CSS_SELECTOR, "div.commentTime")
                comment_time_content = comment_time_div.text
                # 使用正则表达式匹配“IP属地：”及其后的内容
                match = re.search(r'(.*)IP属地：(.*)', comment_time_content)
                if match:
                    comment_time = match.group(1).strip()
                    ip_location = match.group(2).strip()
                else:
                    comment_time = comment_time_content.strip()  # 如果没有匹配到，则整个内容都是时间
                    ip_location = "未知"
                data.append(comment_time)   # 加入评论时间
                data.append(ip_location)    # 加入IP所属地
                # 点赞数
                try:
                    # 获取包含点赞图标的元素
                    tools_item = comment.find_element(By.CSS_SELECTOR, "span.votedIcon").find_element(By.XPATH, "..")
                    # 获取该元素的所有文本内容，包括所有子元素
                    upvote = tools_item.get_attribute('textContent')
                    # 使用正则表达式提取数字
                    upvote_match = re.search(r'(\d+)', upvote)
                    # 如果匹配到数字，则为点赞数，否则为0
                    upvote = upvote_match.group(1) if upvote_match else '0'
                except NoSuchElementException:
                    # 如果没有找到点赞数，则可能是这个评论没有点赞
                    upvote = '0'
                data.append(upvote)     # 加入点赞数

                # 打印信息
                # print(f"用户名: {username}, 评分: {score}, 评论时间: {comment_time}, IP所属地: {ip_location}, 点赞数: {upvote}")

                # 读取已有的Excel文件
                df = pd.read_excel(excel_path)

                # 使用DataFrame的长度来确定新行的索引位置，并直接添加新数据
                df.loc[len(df)] = data

                # 将更新后的DataFrame保存回Excel文件
                df.to_excel(excel_path, index=False)

                # 评论计数器+1
                comment_count += 1

        except Exception as e:
            print(f"跳转到第 {page_num} 页时发生错误：", e)
            continue  # 出错时继续下一页

    # 关闭浏览器
    driver.quit()

    print('评论数量为：', comment_count)
