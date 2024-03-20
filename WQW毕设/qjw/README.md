2024/3/18-进度
一、数据收集
1. 【去哪儿url】爬取去哪儿前200个景点的url，存储在【scraped_data.xlsx】
2. 【openTime】通过景点的url爬取200个景点的景点名称、景点介绍、景点门票价格、景点开放时间，存储在【scenic_details.xlsx】
3. 【userComm】通过景点的url爬取用户名称、用户文字评论、用户url、用户评分，景点url、景点名称，存储在【comments_data.xlsx】
4. 【userAttr】通过用户url爬取用户曾经访问过的景点，到访时间，用户url，用户名称？，存储在【user_visits_data.xlsx】

2024/3/19-进度
二、数据清洗和预处理:
【scraped_data.xlsx】200个景点的url、景点名称。
【scenic_details.xlsx】有200个景点的景点名称、景点介绍、景点门票价格、景点开放时间。
【comments_data.xlsx】有用户名称、用户文字评论、用户url、用户评分，景点url、景点名称。
【user_visits_data.xlsx】用户曾经访问过的景点，到访时间，用户url，用户名。

1. 确保所有数据都是最新的且格式一致。
    -统一url格式，都包含https://前缀，删除不必要参数
   - url去重，保证url有效性
   - 合并数据，将【scenic_details.xlsx】和【comments_data.xlsx】通过景点名称合并，得到【combined_data】景点名称、景点评分、用户评论、用户url、用户名称、景点url、景点介绍、门票价格、景点开放时间。
2. 检查并处理缺失值、异常值和重复项。
3. 确保各个文件中的景点名称一致，以便能够准确关联数据。
4. 标准化用户URL和景点URL以确保它们的一致性和可链接性。

2024/3/20-进度（去哪儿网页中，对景点按热度排名，筛选出200个景点）
1. 修改【scraped_data.xlsx】景点url、景点名称、景点排名
2. 修改【scenic_details.xlsx】景点名称、景点介绍、景点门票价格、景点开放时间
3. 修改【comments_data.xlsx】用户名称、用户文字评论、用户url、用户评分、景点url、景点名称（每个景点提取了前50个用户评论）
4. 待修改【user_visits_data.xlsx】历史访问过的景点存在空值，同时有些是评论，需要f12自己校准。
5. 待修改【combined_data】合并【scenic_details.xlsx】和【comments_data.xlsx】
