import pandas as pd
import numpy as np
import glob
import os


# 使用glob模块获取所有Excel文件的路径
file_paths = glob.glob('D:/dddd/Travel-recommendation-algorithm/WQW毕设/景点/*.xlsx')

# 读取所有文件并合并到一个DataFrame中
all_data = pd.DataFrame()

for file_path in file_paths:
    # 读取文件
    df = pd.read_excel(file_path)
    # 获取文件名作为景点名称，这里假设文件名就是景点名称，没有扩展名
    # os.path.basename获取文件名和扩展名，os.path.splitext分离文件名和扩展名
    attraction_name = os.path.splitext(os.path.basename(file_path))[0]
    # 将景点名称作为一个新列添加到DataFrame中
    df['attraction_name'] = attraction_name
    # 合并数据
    all_data = pd.concat([all_data, df], ignore_index=True)

# 删除可能存在的重复行
all_data.drop_duplicates(inplace=True)

# 创建评分矩阵，使用pivot_table
rating_matrix = all_data.pivot_table(index='用户名', columns='attraction_name', values='评分', fill_value=0)

# 'rating_matrix' 现在是一个包含用户对景点评分的矩阵，缺失值已被填充为0

# 导出评分矩阵到Excel文件
rating_matrix.to_excel("rating_matrix.xlsx")
