# -*- coding: utf-8 -*-
import sqlite3
DATABASE_PATH = 'database/python_learning.db'
knowledge_data = [
    ('字典与集合', '字典完全指南', '字典的创建、访问、修改和遍历', 'person = {"name": "张三", "age": 25}', 'medium'),
    ('字典与集合', '集合详解', '集合的创建和集合运算', 's1 = {1,2,3}; s2 = {2,3,4}', 'medium'),
    ('字典与集合', '字典高级应用', '嵌套字典和defaultdict、Counter', 'from collections import defaultdict', 'hard'),
    ('字符串操作', '字符串高级方法', '字符串查找、替换、分割', 'text.find("Python"); text.split()', 'medium'),
    ('字符串操作', '字符串格式化', '三种格式化方式', 'f"{name}, {age}"', 'hard'),
    ('字符串操作', '正则表达式', 're模块的使用', 'import re; re.search()', 'hard'),
    ('文件操作', '文件读写高级', 'with语句和多种读取方式', 'with open("file") as f:', 'medium'),
    ('文件操作', 'CSV和JSON', 'csv和json模块的使用', 'import csv, json', 'hard'),
    ('文件操作', '目录管理', 'os和pathlib模块', 'from pathlib import Path', 'hard'),
    ('面向对象', '继承与多态', '类的继承和方法重写', 'class Dog(Animal):', 'hard'),
    ('面向对象', '特殊方法', '魔术方法__init__、__str__等', 'def __add__(self, other):', 'hard'),
    ('面向对象', '装饰器属性', '@property和@classmethod', '@property\ndef area(self):', 'hard'),
]
conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()
for cat, title, content, code, diff in knowledge_data:
    cursor.execute('SELECT COUNT(*) FROM knowledge_points WHERE category=? AND title=?', (cat, title))
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO knowledge_points (category,title,content,code_example,difficulty) VALUES (?,?,?,?,?)', (cat, title, content, code, diff))
        print(f"Added: {cat} - {title}")
conn.commit()
cursor.execute('SELECT category, COUNT(*) FROM knowledge_points GROUP BY category')
for row in cursor.fetchall():
    print(f"{row[0]}: {row[1]}个")
conn.close()
print("Done!")
