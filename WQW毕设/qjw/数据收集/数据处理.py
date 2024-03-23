# import pandas as pd
# import os

# # 读取文件
# # 获取当前脚本的绝对路径
# current_directory = os.path.dirname(os.path.abspath(__file__))
# # 步骤1：读取Excel文件
# # 替换下面的'your_excel_file.xlsx'为你的Excel文件路径

# excel_path = os.path.join(current_directory,'comments_data.xlsx')
# comments_df = pd.read_excel(excel_path)
# #数据清洗
# #comments_df = comments_df.dropna(subset=['User URL', 'Scenic Name', 'User Comment'])
# # 步骤3：构建评论矩阵
# # 如果一个用户对同一景点有多条评论，这里我们选择合并这些评论
# comments_matrix = comments_df.groupby(['User URL', 'Scenic Name'])['User Comment'].apply(' '.join).unstack(fill_value='')

# # 提取'User Rating'中的数字
# # comments_path['User Rating Numeric'] = comments_path['User Rating'].str.extract('(\d+)$').astype(float)

# # 步骤2：构建评分矩阵
# #comments_matrix = comments_path.pivot_table(columns='Scenic Name', index='User URL', values='User Comment', fill_value=0)

# # 显示合并后的前几行数据
# print(comments_matrix.head())


# # 步骤3：将评分矩阵存储为新的Excel文件
# # 替换下面的'rating_matrix.xlsx'为你想要保存的新Excel文件名
# comments_matrix.to_excel('comments_matrix.xlsx')

# print('数据已成功保存到Excel文件。')


####################################################
import pandas as pd
import os

# 读取文件
# 获取当前脚本的绝对路径
current_directory = os.path.dirname(os.path.abspath(__file__))
# 步骤1：读取Excel文件
# 替换下面的'your_excel_file.xlsx'为你的Excel文件路径

excel_path = os.path.join(current_directory,'comments_data.xlsx')
comments_path = pd.read_excel(excel_path)

# 提取'User Rating'中的数字
comments_path['User Rating Numeric'] = comments_path['User Rating'].str.extract('(\d+)$').astype(float)

# 步骤2：构建评分矩阵
rating_matrix = comments_path.pivot_table(columns='Scenic Name', index='User URL', values='User Rating Numeric', fill_value=0)

# 显示合并后的前几行数据
print(rating_matrix.head())


rating_matrix.to_excel('rating_matrix.xlsx')

print('数据已成功保存到Excel文件。')


