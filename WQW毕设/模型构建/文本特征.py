from transformers import BertTokenizer
import os
import pandas as pd

# 文本特征预处理模块

# 获取当前脚本的绝对路径
current_directory = os.path.dirname(os.path.abspath(__file__))
excel_path = os.path.join(current_directory,'comments_matrix.xlsx')
comments_df = pd.read_excel(excel_path) # 加载excel文件

# 将所有评论转换为一个列表，用特殊标记"[PAD]"代替空评论
# 将数字0替换为"[PAD]"标记
comments_list = comments_df.replace(0, "[PAD]").values.flatten()



# 加载预训练的BERT分词器
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# 设置最大序列长度
MAX_LEN = 256  # 这个值可能需要根据您数据的具体情况进行调整

# 对每个评论进行编码
encoded_comments = [tokenizer.encode_plus(
    comment,
    add_special_tokens=True,
    max_length=MAX_LEN,
    padding='max_length',
    truncation=True,
    return_attention_mask=True
) for comment in comments_list]

# 提取Token IDs和注意力掩码
input_ids = [item['input_ids'] for item in encoded_comments]
attention_masks = [item['attention_mask'] for item in encoded_comments]

# 打印处理后的前几条评论的Token IDs和注意力掩码
for i in range(min(5, len(input_ids))):  # 只打印前5条评论，或者更少如果总评论数小于5
    print(f"Comment {i+1} Token IDs: {input_ids[i]}")
    print(f"Comment {i+1} Attention Mask: {attention_masks[i]}\n")



###############################

# 将数据集导入Keras模型中

# # train_model.py
# from data_preprocessing import preprocess_data

# # 获取预处理后的数据集
# dataset = preprocess_data('path/to/your/dataset.xlsx')


#####################