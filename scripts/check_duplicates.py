# -*- coding: utf-8 -*-
"""检查知识点是否重复"""
from database.db_manager import db_manager

db_manager.connect()

# 检查重复的知识点
query = """
SELECT category, title, COUNT(*) as cnt 
FROM knowledge_points 
GROUP BY category, title 
HAVING COUNT(*) > 1
"""
result = db_manager.execute_query(query)

if result:
    print("发现重复的知识点:")
    for row in result:
        print(f"  {row['category']} - {row['title']}: {row['cnt']}条")
else:
    print("没有发现重复的知识点")

# 查看所有知识点数量
count_query = "SELECT COUNT(*) as total FROM knowledge_points"
count_result = db_manager.execute_query(count_query)
print(f"\n总共有 {count_result[0]['total']} 条知识点")

# 按分类统计
category_query = """
SELECT category, COUNT(*) as cnt 
FROM knowledge_points 
GROUP BY category
"""
category_result = db_manager.execute_query(category_query)
print("\n各分类知识点数量:")
for row in category_result:
    print(f"  {row['category']}: {row['cnt']}条")

db_manager.disconnect()
