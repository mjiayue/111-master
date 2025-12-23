# -*- coding: utf-8 -*-
"""
题目模型
定义题目相关的数据操作
"""
import json


class Question:
    """题目类"""

    def __init__(self, question_id=None, category=None, q_type=None, question=None,
                 options=None, answer=None, explanation=None, difficulty='medium', created_at=None):
        """
        初始化题目对象
        :param question_id: 题目ID
        :param category: 分类
        :param q_type: 题目类型（choice/judge/fill/code）
        :param question: 题目内容
        :param options: 选项（JSON格式字符串或列表）
        :param answer: 答案
        :param explanation: 解析
        :param difficulty: 难度
        :param created_at: 创建时间
        """
        self.id = question_id
        self.category = category
        self.type = q_type
        self.question = question
        # 如果options是字符串，解析为列表
        if isinstance(options, str) and options:
            try:
                self.options = json.loads(options)
            except json.JSONDecodeError:
                self.options = []
        else:
            self.options = options if options else []
        self.answer = answer
        self.explanation = explanation
        self.difficulty = difficulty
        self.created_at = created_at

    @classmethod
    def from_dict(cls, data):
        """
        从字典创建题目对象
        :param data: 题目数据字典
        :return: Question对象
        """
        if not data:
            return None

        return cls(
            question_id=data.get('id'),
            category=data.get('category'),
            q_type=data.get('type'),
            question=data.get('question'),
            options=data.get('options'),
            answer=data.get('answer'),
            explanation=data.get('explanation'),
            difficulty=data.get('difficulty', 'medium'),
            created_at=data.get('created_at')
        )

    def to_dict(self):
        """
        将题目对象转换为字典
        :return: 题目数据字典
        """
        return {
            'id': self.id,
            'category': self.category,
            'type': self.type,
            'question': self.question,
            'options': self.options,
            'answer': self.answer,
            'explanation': self.explanation,
            'difficulty': self.difficulty,
            'created_at': self.created_at
        }

    def get_options_json(self):
        """
        获取JSON格式的选项字符串
        :return: JSON字符串
        """
        return json.dumps(self.options, ensure_ascii=False)

    def check_answer(self, user_answer):
        """
        检查用户答案是否正确
        :param user_answer: 用户答案
        :return: 是否正确
        """
        if self.type == 'choice' or self.type == 'judge':
            return str(user_answer).strip().upper() == str(self.answer).strip().upper()
        elif self.type == 'fill':
            # 填空题，去除首尾空格比较
            return str(user_answer).strip() == str(self.answer).strip()
        elif self.type == 'code':
            # 编程题需要运行代码比较结果，这里简单比较字符串
            return str(user_answer).strip() == str(self.answer).strip()
        return False

    def __repr__(self):
        return f"<Question {self.type} - {self.category} - {self.question[:20]}...>"
