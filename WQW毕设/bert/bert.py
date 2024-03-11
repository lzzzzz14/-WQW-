import os
import torch
from transformers import BertTokenizer, BertModel
from sklearn.cluster import KMeans
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

folder_path = "../景点评价"

file_names = os.listdir(folder_path)

texts = []

for file_name in file_names:
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        texts.append(text)

# 提取特征
features = []
for text in texts:
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    outputs = model(**inputs)
    features.append(outputs.last_hidden_state[:, 0, :].detach().numpy())  # 取CLS标记的输出作为特征

features = np.vstack(features)  # 将特征列表转换为numpy数组

# 聚类
kmeans = KMeans(n_clusters=4)  # 假设我们想要分成4个类别
kmeans.fit(features)
labels = kmeans.labels_  # 获取每个文本的类别标签

print(labels)  # 打印每个文本的类别

tsne = TSNE(n_components=2, random_state=0)
reduced_features = tsne.fit_transform(features)

# 根据聚类标签对降维后的特征进行颜色编码
colors = ['r', 'b', 'g', 'c']  # 假设我们有4个聚类，分别用红色、蓝色、绿色和青色表示
for i in range(len(colors)):  # 这里更改循环的次数来匹配聚类的数目
    x = reduced_features[labels == i, 0]
    y = reduced_features[labels == i, 1]
    plt.scatter(x, y, c=colors[i], label=f'Cluster {i}')

plt.title('t-SNE visualization of text clustering')
plt.xlabel('t-SNE 1')
plt.ylabel('t-SNE 2')
plt.legend(loc='best')
plt.show()
