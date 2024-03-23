import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse

# 假设df是你的DataFrame，包含user_id, item_id, 和 rating
# 例如: df = pd.DataFrame({'user_id': [...], 'item_id': [...], 'rating': [...]})

# 步骤 1: 创建用户-景点评分矩阵
pivot_table = df.pivot_table(index='user_id', columns='item_id', values='rating').fillna(0)

# 步骤 2: 计算用户之间的相似度
sparse_matrix = sparse.csr_matrix(pivot_table.values)
user_similarity = cosine_similarity(sparse_matrix)

# 将相似度矩阵转换成DataFrame，方便后续操作
user_similarity_df = pd.DataFrame(user_similarity, index=pivot_table.index, columns=pivot_table.index)

# 步骤 3: 为每个用户找到最相似的N个用户（邻居）
def find_n_neighbors(df, n):
    order = np.argsort(df.values, axis=1)[:, :n]
    df = df.apply(lambda x: pd.Series(x.sort_values(ascending=False)
           .iloc[:n].index, 
          index=['top{}'.format(i) for i in range(1, n+1)]), axis=1)
    return df

# 假设我们选择最相似的3个用户
n_neighbors = 3
top_n_neighbors = find_n_neighbors(user_similarity_df, n_neighbors)

# 步骤 4: 生成推荐
def recommend_items(user_id, user_similarity_df, pivot_table, top_n_neighbors):
    # 从邻居中获取未评分的景点并预测评分
    similar_users = top_n_neighbors.loc[user_id]
    similar_users = similar_users.dropna()
    recommendations = pd.Series()
    for i, user in enumerate(similar_users):
        # 加权平均评分
        weights = user_similarity_df.loc[user_id, similar_users.index]
        ratings = pivot_table.loc[user, :] * weights[i]
        recommendations = recommendations.append(ratings)
    
    recommendations = recommendations.groupby(recommendations.index).sum()
    recommended_items = recommendations.sort_values(ascending=False).index.tolist()
    
    # 移除已经评分过的景点
    rated_items = pivot_table.loc[user_id]
    rated_items = rated_items[rated_items > 0].index.tolist()
    recommendations = [item for item in recommended_items if item not in rated_items]
    
    return recommendations[:10]  # 返回排名前10的推荐

# 为指定的用户生成推荐
user_id = '某个特定的用户ID'
recommendations = recommend_items(user_id, user_similarity_df, pivot_table, top_n_neighbors)
print(recommendations)
