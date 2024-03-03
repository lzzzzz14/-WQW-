from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import re
import time

# 指定ChromeDriver的路径
chrome_driver_path = r'C:\Users\12570\Downloads\chromedriver-win64\chromedriver.exe'
s = Service(chrome_driver_path)
driver = webdriver.Chrome(service=s)

# 打开网页
driver.get('https://you.ctrip.com/sight/shenzhen26/2778.html')

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
            # 用户名
            username = comment.find_element(By.CSS_SELECTOR, "div.userName").text
            # 评分
            score_src = comment.find_element(By.CSS_SELECTOR, "span.averageScore > img.scoreIcon").get_attribute('src')
            score = re.search(r'score-(\d+).png', score_src).group(1)
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

            # 打印信息
            print(f"用户名: {username}, 评分: {score}, 评论时间: {comment_time}, IP所属地: {ip_location}, 点赞数: {upvote}")

    except Exception as e:
        print(f"跳转到第 {page_num} 页时发生错误：", e)
        continue  # 出错时继续下一页

# 关闭浏览器
driver.quit()
