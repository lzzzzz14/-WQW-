import os
import torch
from transformers import BertTokenizer, BertModel
from sklearn.cluster import KMeans
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

# 检查是否有CUDA支持的GPU
if torch.cuda.is_available():
    device = torch.device("cuda")
    print("There is a GPU available, using the GPU...")
else:
    device = torch.device("cpu")
    print("No GPU available, using the CPU instead...")

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased').to(device)

folder_path = "../景点评价"

file_names = os.listdir(folder_path)

texts = []

save_name = []

for file_name in file_names:
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        sight_name = file_name[:-4]
        save_name.append(sight_name)
        text = sight_name + ": " + text
        texts.append(text)

# 提取特征
features = []
for text in texts:
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512).to(device)
    outputs = model(**inputs)
    if torch.cuda.is_available():
        features.append(outputs.last_hidden_state[:, 0, :].cpu().numpy())
    else:
        features.append(outputs.last_hidden_state[:, 0, :].detach().numpy())  # 取CLS标记的输出作为特征

features = np.vstack(features)  # 将特征列表转换为numpy数组

# 聚类
kmeans = KMeans(n_clusters=3)  # 假设我们想要分成4个类别
kmeans.fit(features)
labels = kmeans.labels_  # 获取每个文本的类别标签

print(labels)  # 打印每个文本的类别

label_0 = []
label_1 = []
label_2 = []
label_3 = []

for i in range(0, len(labels)):
    # labels=0
    if labels[i] == 0:
        label_0.append(save_name[i])
    elif labels[i] == 1:
        label_1.append(save_name[i])
    elif labels[i] == 2:
        label_2.append(save_name[i])
    elif labels[i] == 3:
        label_3.append(save_name[i])

print('label_0: ', label_0)
print('label_1: ', label_1)
print('label_2: ', label_2)
print('label_3: ', label_3)

tsne = TSNE(n_components=2, random_state=0)
reduced_features = tsne.fit_transform(features)

# 根据聚类标签对降维后的特征进行颜色编码
# colors = ['r', 'b', 'g', 'c']  # 假设我们有4个聚类，分别用红色、蓝色、绿色和青色表示
colors = ['r', 'b', 'g']
for i in range(len(colors)):  # 这里更改循环的次数来匹配聚类的数目
    x = reduced_features[labels == i, 0]
    y = reduced_features[labels == i, 1]
    plt.scatter(x, y, c=colors[i], label=f'Cluster {i}')

plt.title('t-SNE visualization of text clustering')
plt.xlabel('t-SNE 1')
plt.ylabel('t-SNE 2')
plt.legend(loc='best')
plt.show()
