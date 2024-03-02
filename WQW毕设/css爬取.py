from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
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
for page_num in range(2, 11):
    try:
        # 等待跳转输入框出现
        input_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.ant-pagination-options-quick-jumper input"))
        )

        # 清除输入框，并输入新的页码
        input_box.clear()
        input_box.send_keys(str(page_num))
        input_box.send_keys(Keys.ENTER)  # 通过发送回车键来触发跳转

        print('这是第：', page_num, '页')

        # 显式等待某个元素出现，确保页面已经跳转
        # 这个选择器需要根据页面上确实会改变的内容来定制
        # WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, "更新的元素选择器"))
        # )

        # 等待一段时间让页面加载
        time.sleep(2)

    except Exception as e:
        print(f"跳转到第 {page_num} 页时发生错误：", e)
        break  # 如果出现错误，跳出循环

# 关闭浏览器
driver.quit()
