# -*- coding: utf-8 -*-
"""
学习记录模型
定义学习记录相关的数据操作
"""


class LearningRecord:
    """学习记录类"""

    def __init__(self, record_id=None, user_id=None, knowledge_id=None,
                 study_time=0, completed=False, last_study_at=None):
        """
        初始化学习记录对象
        :param record_id: 记录ID
        :param user_id: 用户ID
        :param knowledge_id: 知识点ID
        :param study_time: 学习时长（秒）
        :param completed: 是否完成
        :param last_study_at: 最后学习时间
        """
        self.id = record_id
        self.user_id = user_id
        self.knowledge_id = knowledge_id
        self.study_time = study_time
        self.completed = completed
        self.last_study_at = last_study_at

    @classmethod
    def from_dict(cls, data):
        """
        从字典创建学习记录对象
        :param data: 学习记录数据字典
        :return: LearningRecord对象
        """
        if not data:
            return None

        return cls(
            record_id=data.get('id'),
            user_id=data.get('user_id'),
            knowledge_id=data.get('knowledge_id'),
            study_time=data.get('study_time', 0),
            completed=bool(data.get('completed', 0)),
            last_study_at=data.get('last_study_at')
        )

    def to_dict(self):
        """
        将学习记录对象转换为字典
        :return: 学习记录数据字典
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'knowledge_id': self.knowledge_id,
            'study_time': self.study_time,
            'completed': self.completed,
            'last_study_at': self.last_study_at
        }


class PracticeRecord:
    """练习记录类"""

    def __init__(self, record_id=None, user_id=None, question_id=None,
                 user_answer=None, is_correct=None, submit_time=None, time_spent=0):
        """
        初始化练习记录对象
        :param record_id: 记录ID
        :param user_id: 用户ID
        :param question_id: 题目ID
        :param user_answer: 用户答案
        :param is_correct: 是否正确
        :param submit_time: 提交时间
        :param time_spent: 用时（秒）
        """
        self.id = record_id
        self.user_id = user_id
        self.question_id = question_id
        self.user_answer = user_answer
        self.is_correct = is_correct
        self.submit_time = submit_time
        self.time_spent = time_spent

    @classmethod
    def from_dict(cls, data):
        """
        从字典创建练习记录对象
        :param data: 练习记录数据字典
        :return: PracticeRecord对象
        """
        if not data:
            return None

        return cls(
            record_id=data.get('id'),
            user_id=data.get('user_id'),
            question_id=data.get('question_id'),
            user_answer=data.get('user_answer'),
            is_correct=bool(data.get('is_correct')) if data.get('is_correct') is not None else None,
            submit_time=data.get('submit_time'),
            time_spent=data.get('time_spent', 0)
        )

    def to_dict(self):
        """
        将练习记录对象转换为字典
        :return: 练习记录数据字典
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'question_id': self.question_id,
            'user_answer': self.user_answer,
            'is_correct': self.is_correct,
            'submit_time': self.submit_time,
            'time_spent': self.time_spent
        }


class WrongQuestion:
    """错题记录类"""

    def __init__(self, record_id=None, user_id=None, question_id=None,
                 wrong_count=1, mastered=False, first_wrong_at=None, last_wrong_at=None):
        """
        初始化错题记录对象
        :param record_id: 记录ID
        :param user_id: 用户ID
        :param question_id: 题目ID
        :param wrong_count: 错误次数
        :param mastered: 是否已掌握
        :param first_wrong_at: 首次错误时间
        :param last_wrong_at: 最后错误时间
        """
        self.id = record_id
        self.user_id = user_id
        self.question_id = question_id
        self.wrong_count = wrong_count
        self.mastered = mastered
        self.first_wrong_at = first_wrong_at
        self.last_wrong_at = last_wrong_at

    @classmethod
    def from_dict(cls, data):
        """
        从字典创建错题记录对象
        :param data: 错题记录数据字典
        :return: WrongQuestion对象
        """
        if not data:
            return None

        return cls(
            record_id=data.get('id'),
            user_id=data.get('user_id'),
            question_id=data.get('question_id'),
            wrong_count=data.get('wrong_count', 1),
            mastered=bool(data.get('mastered', 0)),
            first_wrong_at=data.get('first_wrong_at'),
            last_wrong_at=data.get('last_wrong_at')
        )

    def to_dict(self):
        """
        将错题记录对象转换为字典
        :return: 错题记录数据字典
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'question_id': self.question_id,
            'wrong_count': self.wrong_count,
            'mastered': self.mastered,
            'first_wrong_at': self.first_wrong_at,
            'last_wrong_at': self.last_wrong_at
        }
