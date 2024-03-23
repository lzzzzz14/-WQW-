from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Placeholder for the combined text of all labels
# 词云的文本内容
labels_text = " ".join([
   '2024湾区超级灯会', '七娘山', '世界之窗', '东澳岛', '东部华侨城茶溪谷', '中英街', '仙湖植物园', '何香凝美术馆', '华侨城大鹏旅游区', '南沙天后宫', '双月湾', '园博园', '圆明新园', '地王观光·深港之窗', '外伶仃岛', '大梅沙海滨公园', '大湾区一号（港珠澳大桥航线）', '大鹏半岛', '巽寮湾', '广州塔', '情侣路', '惠州西湖', '杨梅坑', '沙面', '深圳博物馆', '深圳欢乐谷', '深圳红立方', '港珠澳大桥游', '珠江夜游', '珠海横琴《长隆秀》', '珠海渔女', '珠海长隆度假区', '珠海长隆海洋王国', '红树林', '西涌滨海旅游度假区', '观澜湖生态运动公社', '观澜生态水上乐园', '较场尾', '长隆宇宙飞船', '长隆欢乐世界', '长隆飞鸟乐园', '长鹿旅游休博园', '隐贤山庄', '青青世界' # Placeholder text representing all the labels combined
])

# Creating the word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white',font_path='msyh.ttc').generate(labels_text)
#wordcloud.generate(labels_text)


# Displaying the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
