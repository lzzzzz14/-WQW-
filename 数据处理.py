import os
import pandas as pd

# 设置文件夹路径
folder_path = r'D:\dddd\Travel-recommendation-algorithm\WQW毕设\attr'

# 存储所有文件的DataFrame的列表
dfs = []

# 遍历文件夹中的每个xlsx文件
for filename in os.listdir(folder_path):
    if filename.endswith(".xlsx"):
        file_path = os.path.join(folder_path, filename)
        
        # 读取xlsx文件到DataFrame
        df = pd.read_excel(file_path)

        # 从用户评分、评论数等字段中提取用户相关特征
        #df['用户活跃度'] = df['用户评分'] * df['评论数']
        #df['评论频率'] = df['评论数'] / df['用户评论数']


        df['评分'] = pd.to_numeric(df['评分'], errors='coerce')  # 将 '评分' 列转换为数值型
        df['点评数量'] = pd.to_numeric(df['点评数量'], errors='coerce')  # 将 '点评数量' 列转换为数值型

        df = df.dropna(subset=['评分', '点评数量'])  # 删除包含缺失值的行

        # 从景点热度、评分、评论数等字段中提取景点相关特征
        df['热度分数'] = df['评分'] * df['点评数量']
        #df['受欢迎程度'] = df['景点评分'] / df['用户评论数']

        # 将处理后的DataFrame添加到列表
        dfs.append(df)

# 合并所有文件的DataFrame
merged_df = pd.concat(dfs, ignore_index=True)

# 打印合并后的DataFrame的头部，以确保数据正确处理
print(merged_df.head())