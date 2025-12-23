# -*- coding: utf-8 -*-
"""
配置文件
存储系统的全局配置信息
"""
import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 数据库配置
DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'python_learning.db')

# 默认用户配置
DEFAULT_USER = {
    'username': '1',
    'password': '1',
    'nickname': 'Python学习者'
}

# 窗口配置
WINDOW_CONFIG = {
    'title': 'PyPalPrep',
    'width': 1200,
    'height': 800,
    'min_width': 1000,
    'min_height': 600
}

# 代码编辑器配置
EDITOR_CONFIG = {
    'font_family': 'Consolas',
    'font_size': 12,
    'tab_size': 4,
    'timeout': 5  # 代码执行超时时间（秒）
}

# 资源路径配置
RESOURCES_DIR = os.path.join(BASE_DIR, 'resources')
ICONS_DIR = os.path.join(RESOURCES_DIR, 'icons')
IMAGES_DIR = os.path.join(RESOURCES_DIR, 'images')
DATA_DIR = os.path.join(RESOURCES_DIR, 'data')

# 主题颜色配置
THEME_COLORS = {
    # iOS 风格：低饱和浅色系
    'primary': '#5B9BD5',      # 柔和蓝
    'success': '#6FBF73',
    'warning': '#E6A23C',
    'danger': '#E05252',
    'info': '#7FD7E6',
    'dark': '#3C4858',         # 深色用于文字
    'light': '#FFFFFF',        # 纯白背景卡片
    'background': '#F6F7F9'    # 页面背景浅灰
}

# 知识点分类
KNOWLEDGE_CATEGORIES = [
    'Python基础',
    '数据类型',
    '运算符与表达式',
    '流程控制',
    '函数',
    '字符串处理',
    '列表与元组',
    '字典与集合',
    '文件操作',
    '异常处理',
    '面向对象编程',
    '模块与包',
    '常用标准库'
]

# 题目类型
QUESTION_TYPES = {
    'choice': '选择题',
    'judge': '判断题',
    'fill': '填空题',
    'code': '编程题'
}

# 难度等级
DIFFICULTY_LEVELS = {
    'easy': '简单',
    'medium': '中等',
    'hard': '困难'
}
