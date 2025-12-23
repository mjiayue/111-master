# -*- coding: utf-8 -*-
"""
用户模型
定义用户相关的数据操作
"""
from datetime import datetime


class User:
    """用户类"""

    def __init__(self, user_id=None, username=None, nickname=None, created_at=None, last_login=None):
        """
        初始化用户对象
        :param user_id: 用户ID
        :param username: 用户名
        :param nickname: 昵称
        :param created_at: 创建时间
        :param last_login: 最后登录时间
        """
        self.id = user_id
        self.username = username
        self.nickname = nickname
        self.created_at = created_at
        self.last_login = last_login

    @classmethod
    def from_dict(cls, data):
        """
        从字典创建用户对象
        :param data: 用户数据字典
        :return: User对象
        """
        if not data:
            return None

        return cls(
            user_id=data.get('id'),
            username=data.get('username'),
            nickname=data.get('nickname'),
            created_at=data.get('created_at'),
            last_login=data.get('last_login')
        )

    def to_dict(self):
        """
        将用户对象转换为字典
        :return: 用户数据字典
        """
        return {
            'id': self.id,
            'username': self.username,
            'nickname': self.nickname,
            'created_at': self.created_at,
            'last_login': self.last_login
        }

    def __repr__(self):
        return f"<User {self.username} ({self.nickname})>"
