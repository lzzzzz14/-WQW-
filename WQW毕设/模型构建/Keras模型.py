import tensorflow as tf
print(tf.__version__)

from tensorflow.python.keras.models import Model
from tensorflow.python.keras.layers import Embedding, Dense, Input, concatenate, Flatten, Dropout
from tensorflow.python.keras.optimizers import Adam
import pandas as pd
# from tensorflow.python.keras.preprocessing.text import Tokenizer
# import torch

# 类别特征的嵌入维度
EMBEDDING_DIM = 50

# 用户URL和景点名称的输入
user_input = Input(shape=(1,), name='user_input')
item_input = Input(shape=(1,), name='item_input')

# 嵌入层
user_embedding = Embedding(output_dim=EMBEDDING_DIM, input_dim=num_users, input_length=1, name='user_embedding')(user_input)
item_embedding = Embedding(output_dim=EMBEDDING_DIM, input_dim=num_items, input_length=1, name='item_embedding')(item_input)

# 展平嵌入向量
user_vec = Flatten(name='FlattenUsers')(user_embedding)
item_vec = Flatten(name='FlattenItems')(item_embedding)

# 合并特征
concat = concatenate([user_vec, item_vec])

# 全连接层
fc1 = Dense(128, activation='relu')(concat)
fc2 = Dense(64, activation='relu')(fc1)
fc3 = Dropout(0.5)(fc2)
output = Dense(1, activation='linear')(fc3)

# 编译模型
model = Model(inputs=[user_input, item_input], outputs=output)
model.compile(optimizer=Adam(lr=0.001), loss='mse', metrics=['mae'])

model.summary()
