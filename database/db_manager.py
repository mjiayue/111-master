# -*- coding: utf-8 -*-
"""
数据库管理模块
负责SQLite数据库的创建、连接和基本操作
"""
import sqlite3
import os
import hashlib
from datetime import datetime
from config import DATABASE_PATH, DEFAULT_USER


class DatabaseManager:
    """数据库管理器类"""

    def __init__(self, db_path=DATABASE_PATH):
        """
        初始化数据库管理器
        :param db_path: 数据库文件路径
        """
        self.db_path = db_path
        self.connection = None
        self.cursor = None

        # 如果数据库不存在，创建数据库和表
        if not os.path.exists(db_path):
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            self.create_database()

    def connect(self):
        """连接数据库"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            # 设置返回字典格式的行
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
            return True
        except sqlite3.Error as e:
            print(f"数据库连接失败: {e}")
            return False

    def disconnect(self):
        """断开数据库连接"""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None

    def commit(self):
        """提交事务"""
        if self.connection:
            self.connection.commit()

    def rollback(self):
        """回滚事务"""
        if self.connection:
            self.connection.rollback()

    def create_database(self):
        """创建数据库和所有表"""
        self.connect()

        # 创建用户表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                nickname TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')
        # 为用户表增加头像和背景字段（向后兼容）
        try:
            self.cursor.execute("ALTER TABLE users ADD COLUMN avatar_path TEXT")
        except Exception:
            pass
        try:
            self.cursor.execute("ALTER TABLE users ADD COLUMN bg_path TEXT")
        except Exception:
            pass

        # 创建知识点表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS knowledge_points (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                code_example TEXT,
                difficulty TEXT DEFAULT 'medium',
                order_num INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 创建题目表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                type TEXT NOT NULL,
                question TEXT NOT NULL,
                options TEXT,
                answer TEXT NOT NULL,
                explanation TEXT,
                difficulty TEXT DEFAULT 'medium',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 创建学习记录表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                knowledge_id INTEGER NOT NULL,
                study_time INTEGER DEFAULT 0,
                completed BOOLEAN DEFAULT 0,
                last_study_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (knowledge_id) REFERENCES knowledge_points(id)
            )
        ''')

        # 创建练习记录表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS practice_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                question_id INTEGER NOT NULL,
                user_answer TEXT,
                is_correct BOOLEAN,
                submit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                time_spent INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (question_id) REFERENCES questions(id)
            )
        ''')

        # 创建错题本表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS wrong_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                question_id INTEGER NOT NULL,
                wrong_count INTEGER DEFAULT 1,
                mastered BOOLEAN DEFAULT 0,
                first_wrong_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_wrong_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (question_id) REFERENCES questions(id),
                UNIQUE(user_id, question_id)
            )
        ''')

        # 创建学习统计表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS study_statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                study_date DATE NOT NULL,
                total_time INTEGER DEFAULT 0,
                questions_completed INTEGER DEFAULT 0,
                questions_correct INTEGER DEFAULT 0,
                knowledge_learned INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(id),
                UNIQUE(user_id, study_date)
            )
        ''')

        self.commit()

        # 初始化默认数据
        self.initialize_default_data()

        self.disconnect()

    def initialize_default_data(self):
        """初始化默认数据（默认用户）"""
        # 添加默认用户
        password_hash = hashlib.md5(DEFAULT_USER['password'].encode()).hexdigest()
        try:
            self.cursor.execute(
                "INSERT INTO users (username, password, nickname) VALUES (?, ?, ?)",
                (DEFAULT_USER['username'], password_hash, DEFAULT_USER['nickname'])
            )
            self.commit()
        except sqlite3.IntegrityError:
            # 用户已存在，忽略
            pass

    def execute_query(self, query, params=None):
        """
        执行查询语句
        :param query: SQL查询语句
        :param params: 查询参数
        :return: 查询结果
        """
        if not self.connection:
            self.connect()

        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"查询执行失败: {e}")
            return []

    def execute_update(self, query, params=None):
        """
        执行更新语句
        :param query: SQL更新语句
        :param params: 更新参数
        :return: 影响的行数
        """
        if not self.connection:
            self.connect()

        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            print(f"更新执行失败: {e}")
            self.rollback()
            return 0

    def insert(self, query, params=None):
        """
        插入数据
        :param query: SQL插入语句
        :param params: 插入参数
        :return: 插入的记录ID
        """
        if not self.connection:
            self.connect()

        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"插入执行失败: {e}")
            self.rollback()
            return None

    def get_user_by_username(self, username):
        """
        根据用户名获取用户信息
        :param username: 用户名
        :return: 用户信息字典
        """
        query = "SELECT * FROM users WHERE username = ?"
        result = self.execute_query(query, (username,))
        return dict(result[0]) if result else None

    def verify_user(self, username, password):
        """
        验证用户登录
        :param username: 用户名
        :param password: 密码
        :return: 用户信息字典或None
        """
        user = self.get_user_by_username(username)
        if user:
            password_hash = hashlib.md5(password.encode()).hexdigest()
            if user['password'] == password_hash:
                # 更新最后登录时间
                self.execute_update(
                    "UPDATE users SET last_login = ? WHERE id = ?",
                    (datetime.now(), user['id'])
                )
                return user
        return None

    def update_user_last_login(self, user_id):
        """
        更新用户最后登录时间
        :param user_id: 用户ID
        """
        self.execute_update(
            "UPDATE users SET last_login = ? WHERE id = ?",
            (datetime.now(), user_id)
        )


# 全局数据库管理器实例
db_manager = DatabaseManager()
