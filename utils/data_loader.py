# -*- coding: utf-8 -*-
"""
数据加载器
用于加载和管理知识点、题目等数据
"""
from database.db_manager import db_manager
from models.knowledge import KnowledgePoint
from models.question import Question
from models.record import LearningRecord, PracticeRecord, WrongQuestion
import json


class DataLoader:
    """数据加载器类"""

    @staticmethod
    def load_all_knowledge_points():
        """
        加载所有知识点
        :return: 知识点列表
        """
        db_manager.connect()
        query = "SELECT * FROM knowledge_points ORDER BY category, order_num"
        results = db_manager.execute_query(query)
        db_manager.disconnect()

        knowledge_points = []
        for row in results:
            kp = KnowledgePoint.from_dict(dict(row))
            knowledge_points.append(kp)

        return knowledge_points

    @staticmethod
    def load_knowledge_by_category(category):
        """
        根据分类加载知识点
        :param category: 分类名称
        :return: 知识点列表
        """
        db_manager.connect()
        query = "SELECT * FROM knowledge_points WHERE category = ? ORDER BY order_num"
        results = db_manager.execute_query(query, (category,))
        db_manager.disconnect()

        knowledge_points = []
        for row in results:
            kp = KnowledgePoint.from_dict(dict(row))
            knowledge_points.append(kp)

        return knowledge_points

    @staticmethod
    def load_knowledge_by_id(knowledge_id):
        """
        根据ID加载知识点
        :param knowledge_id: 知识点ID
        :return: 知识点对象
        """
        db_manager.connect()
        query = "SELECT * FROM knowledge_points WHERE id = ?"
        results = db_manager.execute_query(query, (knowledge_id,))
        db_manager.disconnect()

        if results:
            return KnowledgePoint.from_dict(dict(results[0]))
        return None

    @staticmethod
    def load_all_questions():
        """
        加载所有题目
        :return: 题目列表
        """
        db_manager.connect()
        query = "SELECT * FROM questions ORDER BY category, type"
        results = db_manager.execute_query(query)
        db_manager.disconnect()

        questions = []
        for row in results:
            q = Question.from_dict(dict(row))
            questions.append(q)

        return questions

    @staticmethod
    def load_questions_by_category(category):
        """
        根据分类加载题目
        :param category: 分类名称
        :return: 题目列表
        """
        db_manager.connect()
        query = "SELECT * FROM questions WHERE category = ? ORDER BY type"
        results = db_manager.execute_query(query, (category,))
        db_manager.disconnect()

        questions = []
        for row in results:
            q = Question.from_dict(dict(row))
            questions.append(q)

        return questions

    @staticmethod
    def load_questions_by_type(q_type):
        """
        根据类型加载题目
        :param q_type: 题目类型
        :return: 题目列表
        """
        db_manager.connect()
        query = "SELECT * FROM questions WHERE type = ?"
        results = db_manager.execute_query(query, (q_type,))
        db_manager.disconnect()

        questions = []
        for row in results:
            q = Question.from_dict(dict(row))
            questions.append(q)

        return questions

    @staticmethod
    def load_question_by_id(question_id):
        """
        根据ID加载题目
        :param question_id: 题目ID
        :return: 题目对象
        """
        db_manager.connect()
        query = "SELECT * FROM questions WHERE id = ?"
        results = db_manager.execute_query(query, (question_id,))
        db_manager.disconnect()

        if results:
            return Question.from_dict(dict(results[0]))
        return None

    @staticmethod
    def load_user_learning_records(user_id):
        """
        加载用户的学习记录
        :param user_id: 用户ID
        :return: 学习记录列表
        """
        db_manager.connect()
        query = """
            SELECT lr.*, kp.title, kp.category
            FROM learning_records lr
            LEFT JOIN knowledge_points kp ON lr.knowledge_id = kp.id
            WHERE lr.user_id = ?
            ORDER BY lr.last_study_at DESC
        """
        results = db_manager.execute_query(query, (user_id,))
        db_manager.disconnect()

        records = []
        for row in results:
            record_dict = dict(row)
            records.append(record_dict)

        return records

    @staticmethod
    def load_user_practice_records(user_id, limit=None):
        """
        加载用户的练习记录
        :param user_id: 用户ID
        :param limit: 限制数量
        :return: 练习记录列表
        """
        db_manager.connect()
        if limit:
            query = """
                SELECT pr.*, q.question, q.type, q.category
                FROM practice_records pr
                LEFT JOIN questions q ON pr.question_id = q.id
                WHERE pr.user_id = ?
                ORDER BY pr.submit_time DESC
                LIMIT ?
            """
            results = db_manager.execute_query(query, (user_id, limit))
        else:
            query = """
                SELECT pr.*, q.question, q.type, q.category
                FROM practice_records pr
                LEFT JOIN questions q ON pr.question_id = q.id
                WHERE pr.user_id = ?
                ORDER BY pr.submit_time DESC
            """
            results = db_manager.execute_query(query, (user_id,))
        db_manager.disconnect()

        records = []
        for row in results:
            records.append(dict(row))

        return records

    @staticmethod
    def load_user_wrong_questions(user_id):
        """
        加载用户的错题
        :param user_id: 用户ID
        :return: 错题列表
        """
        db_manager.connect()
        query = """
            SELECT wq.*, q.question, q.type, q.answer, q.explanation, q.options, q.category
            FROM wrong_questions wq
            LEFT JOIN questions q ON wq.question_id = q.id
            WHERE wq.user_id = ? AND wq.mastered = 0
            ORDER BY wq.last_wrong_at DESC
        """
        results = db_manager.execute_query(query, (user_id,))
        db_manager.disconnect()

        wrong_questions = []
        for row in results:
            wrong_questions.append(dict(row))

        return wrong_questions

    @staticmethod
    def get_user_statistics(user_id):
        """
        获取用户统计信息
        :param user_id: 用户ID
        :return: 统计信息字典
        """
        db_manager.connect()

        # 总学习时长
        query = "SELECT SUM(study_time) as total_time FROM learning_records WHERE user_id = ?"
        result = db_manager.execute_query(query, (user_id,))
        total_study_time = dict(result[0])['total_time'] if result and result[0][0] else 0

        # 完成的知识点数
        query = "SELECT COUNT(*) as count FROM learning_records WHERE user_id = ? AND completed = 1"
        result = db_manager.execute_query(query, (user_id,))
        completed_knowledge = dict(result[0])['count'] if result else 0

        # 总练习题数
        query = "SELECT COUNT(*) as count FROM practice_records WHERE user_id = ?"
        result = db_manager.execute_query(query, (user_id,))
        total_questions = dict(result[0])['count'] if result else 0

        # 正确题数
        query = "SELECT COUNT(*) as count FROM practice_records WHERE user_id = ? AND is_correct = 1"
        result = db_manager.execute_query(query, (user_id,))
        correct_questions = dict(result[0])['count'] if result else 0

        # 错题数
        query = "SELECT COUNT(*) as count FROM wrong_questions WHERE user_id = ? AND mastered = 0"
        result = db_manager.execute_query(query, (user_id,))
        wrong_questions_count = dict(result[0])['count'] if result else 0

        db_manager.disconnect()

        accuracy = (correct_questions / total_questions * 100) if total_questions > 0 else 0

        return {
            'total_study_time': total_study_time or 0,
            'completed_knowledge': completed_knowledge,
            'total_questions': total_questions,
            'correct_questions': correct_questions,
            'wrong_questions_count': wrong_questions_count,
            'accuracy': round(accuracy, 2)
        }
