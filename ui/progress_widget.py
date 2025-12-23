# -*- coding: utf-8 -*-
"""
学习进度模块
显示用户的学习进度和统计信息
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox,
                             QTableWidget, QTableWidgetItem, QProgressBar, QHeaderView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from utils.data_loader import DataLoader
from config import THEME_COLORS, KNOWLEDGE_CATEGORIES
from database.db_manager import db_manager


class ProgressWidget(QWidget):
    """学习进度界面"""

    def __init__(self, user):
        """初始化学习进度界面"""
        super().__init__()
        self.current_user = user
        self.init_ui()
        self.load_data()

    def init_ui(self):
        """初始化界面"""
        # 初始化统计卡片标签引用字典（必须在创建卡片之前）
        self.stat_labels = {
            'time': None,
            'knowledge': None,
            'question': None,
        }

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)

        # 标题
        title_label = QLabel('学习进度概览')
        title_label.setObjectName('pageTitle')
        title_label.setFont(QFont('SF Pro Display', 18, QFont.Bold))
        title_label.setStyleSheet(f'color: {THEME_COLORS["primary"]};')
        main_layout.addWidget(title_label)

        # 总体统计卡片
        stats_layout = QHBoxLayout()

        # 学习时长卡片
        time_card = self.create_stat_card('总学习时长', '0 分钟', THEME_COLORS['primary'])
        stats_layout.addWidget(time_card)

        # 完成知识点卡片
        knowledge_card = self.create_stat_card('完成知识点', '0 个', THEME_COLORS['success'])
        stats_layout.addWidget(knowledge_card)

        # 完成题目卡片
        question_card = self.create_stat_card('完成题目', '0 道', THEME_COLORS['info'])
        stats_layout.addWidget(question_card)


        main_layout.addLayout(stats_layout)

        # 分类进度
        category_group = QGroupBox('')
        category_group.setFont(QFont('SF Pro Display', 11, QFont.Bold))
        category_group.setStyleSheet('QGroupBox { padding-top: 10px; margin-top: 10px; border: none; }')
        category_layout = QVBoxLayout()

        self.category_table = QTableWidget()
        self.category_table.setColumnCount(5)
        self.category_table.setHorizontalHeaderLabels(['分类', '总知识点', '已完成', '进度', '正确率'])
        self.category_table.setFont(QFont('Microsoft YaHei', 12))
        
        # 设置表头字体和样式
        header_font = QFont('Microsoft YaHei', 13, QFont.Bold)
        self.category_table.horizontalHeader().setFont(header_font)
        self.category_table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.category_table.horizontalHeader().setStyleSheet(
            'QHeaderView::section { background-color: #F0F0F0; padding: 8px; }'
        )
        self.category_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # 设置行高
        self.category_table.verticalHeader().setDefaultSectionSize(45)
        self.category_table.setMinimumHeight(300)
        self.category_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.category_table.setSelectionBehavior(QTableWidget.SelectRows)
        category_layout.addWidget(self.category_table)

        category_group.setLayout(category_layout)
        main_layout.addWidget(category_group)

        # 最近学习记录
        # 最近学习记录已迁移至个人主页（ProfileWidget）

        self.setLayout(main_layout)

    def create_stat_card(self, title, value, color):
        """创建统计卡片"""
        card = QGroupBox()
        card.setStyleSheet(f'''
            QGroupBox {{
                background-color: white;
                border: 2px solid {color};
                border-radius: 10px;
                padding: 20px;
            }}
        ''')

        layout = QVBoxLayout()

        title_label = QLabel(title)
        title_label.setFont(QFont('Microsoft YaHei', 13))
        title_label.setStyleSheet(f'color: {color}; font-weight: bold;')
        layout.addWidget(title_label)

        value_label = QLabel(value)
        value_label.setFont(QFont('Microsoft YaHei', 26, QFont.Bold))
        value_label.setStyleSheet(f'color: {color};')
        value_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(value_label)

        card.setLayout(layout)

        # 保存标签引用
        if '时长' in title:
            self.stat_labels['time'] = value_label
        elif '知识点' in title:
            self.stat_labels['knowledge'] = value_label
        elif '题目' in title:
            self.stat_labels['question'] = value_label
        elif '正确率' in title:
            self.stat_labels['accuracy'] = value_label

        return card

    def load_data(self):
        """加载数据"""
        # 获取统计信息
        stats = DataLoader.get_user_statistics(self.current_user.id)

        # 更新统计卡片
        if self.stat_labels['time']:
            minutes = stats['total_study_time'] // 60
            hours = minutes // 60
            remaining_minutes = minutes % 60
            if hours > 0:
                self.stat_labels['time'].setText(f"{hours} 小时 {remaining_minutes} 分钟")
            else:
                self.stat_labels['time'].setText(f"{minutes} 分钟")

        if self.stat_labels['knowledge']:
            self.stat_labels['knowledge'].setText(f"{stats['completed_knowledge']} 个")

        if self.stat_labels['question']:
            self.stat_labels['question'].setText(f"{stats['total_questions']} 道")


        # 加载分类进度
        self.load_category_progress()

        # 加载最近学习记录
        self.load_recent_records()

    def load_category_progress(self):
        """加载分类进度"""
        self.category_table.setRowCount(0)

        db_manager.connect()

        for i, category in enumerate(KNOWLEDGE_CATEGORIES):
            # 获取该分类的总知识点数
            total_query = "SELECT COUNT(*) as count FROM knowledge_points WHERE category = ?"
            total_result = db_manager.execute_query(total_query, (category,))
            total_count = dict(total_result[0])['count'] if total_result else 0

            # 获取已完成数（确保数据准确性：使用DISTINCT避免重复计数）
            completed_query = """
                SELECT COUNT(DISTINCT lr.knowledge_id) as count
                FROM learning_records lr
                JOIN knowledge_points kp ON lr.knowledge_id = kp.id
                WHERE lr.user_id = ? AND kp.category = ? AND lr.completed = 1
            """
            completed_result = db_manager.execute_query(
                completed_query,
                (self.current_user.id, category)
            )
            completed_count = dict(completed_result[0])['count'] if completed_result else 0

            # 获取该分类的练习题正确率
            accuracy_query = """
                SELECT
                    COUNT(CASE WHEN pr.is_correct = 1 THEN 1 END) as correct,
                    COUNT(*) as total
                FROM practice_records pr
                JOIN questions q ON pr.question_id = q.id
                WHERE pr.user_id = ? AND q.category = ?
            """
            accuracy_result = db_manager.execute_query(
                accuracy_query,
                (self.current_user.id, category)
            )

            if accuracy_result and dict(accuracy_result[0])['total'] > 0:
                correct = dict(accuracy_result[0])['correct']
                total = dict(accuracy_result[0])['total']
                accuracy = round((correct / total) * 100, 1)
                accuracy_text = f"{accuracy}%"
            else:
                accuracy_text = "未练习"

            # 计算进度
            progress = int((completed_count / total_count) * 100) if total_count > 0 else 0

            # 添加到表格
            self.category_table.insertRow(i)

            # 分类
            category_item = QTableWidgetItem(category)
            category_item.setTextAlignment(Qt.AlignCenter)
            category_item.setFont(QFont('Microsoft YaHei', 12, QFont.Bold))
            self.category_table.setItem(i, 0, category_item)

            # 总数
            total_item = QTableWidgetItem(str(total_count))
            total_item.setTextAlignment(Qt.AlignCenter)
            total_item.setFont(QFont('Microsoft YaHei', 12))
            self.category_table.setItem(i, 1, total_item)

            # 已完成
            completed_item = QTableWidgetItem(str(completed_count))
            completed_item.setTextAlignment(Qt.AlignCenter)
            completed_item.setFont(QFont('Microsoft YaHei', 12))
            self.category_table.setItem(i, 2, completed_item)

            # 进度
            progress_item = QTableWidgetItem(f'{progress}%')
            progress_item.setTextAlignment(Qt.AlignCenter)
            progress_item.setFont(QFont('Microsoft YaHei', 12, QFont.Bold))
            # 根据进度设置颜色
            if progress >= 80:
                progress_item.setForeground(Qt.darkGreen)
            elif progress >= 50:
                progress_item.setForeground(Qt.darkBlue)
            else:
                progress_item.setForeground(Qt.darkRed)
            self.category_table.setItem(i, 3, progress_item)

            # 正确率
            accuracy_item = QTableWidgetItem(accuracy_text)
            accuracy_item.setTextAlignment(Qt.AlignCenter)
            accuracy_item.setFont(QFont('Microsoft YaHei', 12, QFont.Bold))
            # 根据正确率设置颜色
            if accuracy_text != "未练习":
                acc_value = float(accuracy_text.rstrip('%'))
                if acc_value >= 80:
                    accuracy_item.setForeground(Qt.darkGreen)
                elif acc_value >= 60:
                    accuracy_item.setForeground(Qt.darkBlue)
                else:
                    accuracy_item.setForeground(Qt.darkRed)
            self.category_table.setItem(i, 4, accuracy_item)

        db_manager.disconnect()

    def load_recent_records(self):
        """加载最近学习记录"""
        # 最近学习记录已迁移到个人主页（ProfileWidget），此处不再显示
        return

    def refresh(self):
        """刷新数据"""
        self.load_data()
