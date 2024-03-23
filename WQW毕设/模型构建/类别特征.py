import os
from sklearn.preprocessing import LabelEncoder
import pandas as pd

# 标签编码
# 获取当前脚本的绝对路径
current_directory = os.path.dirname(os.path.abspath(__file__))
excel_path = os.path.join(current_directory,'label_data.xlsx')
comments_df = pd.read_excel(excel_path) # 加载excel文件

# 用户URL的标签编码
user_le = LabelEncoder()
comments_df['user_id'] = user_le.fit_transform(comments_df['user_url'])

# 景点名称的标签编码
spot_le = LabelEncoder()
comments_df['spot_id'] = spot_le.fit_transform(comments_df['spot_name'])

# 现在，comments_df中包含了对应于用户URL和景点名称的数值ID：'user_id'和'spot_id'
# 打印comments_df的前10行，查看'user_id'和'spot_id'列
print(comments_df[['user_url', 'user_id', 'spot_name', 'spot_id']].head(10))


# 假设评分数据存储在'rating'列中
ratings = comments_df['rating'].values
# 打印 





# 封装成数据集
# dataset = tf.data.Dataset.from_tensor_slices(({
#     'user_id': comments_df['user_id'].values,
#     'spot_id': comments_df['spot_id'].values,
#     # 这里可以添加其他特征
# }, ratings))
