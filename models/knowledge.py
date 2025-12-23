# -*- coding: utf-8 -*-
"""
知识点模型
定义知识点相关的数据操作
"""


class KnowledgePoint:
    """知识点类"""

    def __init__(self, knowledge_id=None, category=None, title=None, content=None,
                 code_example=None, difficulty='medium', order_num=0, created_at=None):
        """
        初始化知识点对象
        :param knowledge_id: 知识点ID
        :param category: 分类
        :param title: 标题
        :param content: 内容
        :param code_example: 代码示例
        :param difficulty: 难度
        :param order_num: 排序号
        :param created_at: 创建时间
        """
        self.id = knowledge_id
        self.category = category
        self.title = title
        self.content = content
        self.code_example = code_example
        self.difficulty = difficulty
        self.order_num = order_num
        self.created_at = created_at

    @classmethod
    def from_dict(cls, data):
        """
        从字典创建知识点对象
        :param data: 知识点数据字典
        :return: KnowledgePoint对象
        """
        if not data:
            return None

        return cls(
            knowledge_id=data.get('id'),
            category=data.get('category'),
            title=data.get('title'),
            content=data.get('content'),
            code_example=data.get('code_example'),
            difficulty=data.get('difficulty', 'medium'),
            order_num=data.get('order_num', 0),
            created_at=data.get('created_at')
        )

    def to_dict(self):
        """
        将知识点对象转换为字典
        :return: 知识点数据字典
        """
        return {
            'id': self.id,
            'category': self.category,
            'title': self.title,
            'content': self.content,
            'code_example': self.code_example,
            'difficulty': self.difficulty,
            'order_num': self.order_num,
            'created_at': self.created_at
        }

    def __repr__(self):
        return f"<KnowledgePoint {self.category} - {self.title}>"
