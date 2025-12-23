# -*- coding: utf-8 -*-
"""清理重复的知识点，只保留每个知识点的一条记录（order_num最小的）"""
from database.db_manager import db_manager

db_manager.connect()

# 找出所有重复的知识点，保留order_num最小的，删除其他的
query = """
DELETE FROM knowledge_points
WHERE id NOT IN (
    SELECT MIN(id)
    FROM knowledge_points
    GROUP BY category, title
)
"""

try:
    db_manager.execute_update(query)
    print("重复的知识点已清理完成")
    
    # 验证结果
    count_query = "SELECT COUNT(*) as total FROM knowledge_points"
    count_result = db_manager.execute_query(count_query)
    print(f"清理后剩余 {count_result[0]['total']} 条知识点")
    
    # 按分类统计
    category_query = """
    SELECT category, COUNT(*) as cnt 
    FROM knowledge_points 
    GROUP BY category
    ORDER BY category
    """
    category_result = db_manager.execute_query(category_query)
    print("\n各分类知识点数量:")
    for row in category_result:
        print(f"  {row['category']}: {row['cnt']}条")
        
except Exception as e:
    print(f"清理失败: {e}")
finally:
    db_manager.disconnect()
