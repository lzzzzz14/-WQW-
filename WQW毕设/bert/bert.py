import torch
from transformers import BertTokenizer, BertModel

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

text = ("世界之窗正像它的名字那样，是一扇展现世界名胜的窗口的主题乐园，里面有世界各知名景点的缩影。除外，这里还有世界各地的风情表演，"
        "日本茶道、非洲风情歌舞秀等，等待你的观赏。"
        "景区按世界地域结构和游览活动内容分为世界广场、亚洲区、大洋洲区、欧洲区、非洲区、美洲区、雕塑园区、国际街。"
        "一般的游览顺序是世界广场（入口）-亚洲区-大洋区-非洲区-美洲区-欧洲区-雕塑园区、国际街区-世界广场（出口）。"
        "可以边参观各式建筑物拍照，边选择自己感兴趣的表演观看。")

inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)

with torch.no_grad():
    outputs = model(**inputs)

# 获取整个序列的汇总表示
embedding = outputs.pooler_output

print(embedding.shape)  # 查看embedding的形状
print(embedding)        # 打印embedding的实际内容
