# -*- coding: utf-8 -*-
"""
成绩统计模块
显示用户的成绩统计和数据分析图表
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox,
                             QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from utils.data_loader import DataLoader
from config import THEME_COLORS, KNOWLEDGE_CATEGORIES, QUESTION_TYPES
from database.db_manager import db_manager
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class StatisticsWidget(QWidget):
    """成绩统计界面"""

    def __init__(self, user):
        """初始化成绩统计界面"""
        super().__init__()
        self.current_user = user
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 设置中文字体
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        self.init_ui()
        self.load_data()

    def init_ui(self):
        """初始化界面"""
        main_layout = QVBoxLayout()
        # 顶部边距设为 0，使标题紧贴顶端
        main_layout.setContentsMargins(10, 0, 10, 10)

        # 标题
        title_label = QLabel('成绩统计分析')
        # 不使用全局 pageTitle，避免过大内边距
        title_label.setFont(QFont('SF Pro Display', 18, QFont.Bold))
        title_label.setStyleSheet(f'color: {THEME_COLORS["primary"]}; padding: 0px 6px; margin: 0px;')
        main_layout.addWidget(title_label)

        # 图表区域（占满剩余空间）
        charts_layout = QHBoxLayout()
        charts_layout.setContentsMargins(0, 0, 0, 0)
        charts_layout.setSpacing(10)

        # 分类准确率饼图
        accuracy_group = QGroupBox('各分类准确率')
        accuracy_group.setFont(QFont('SF Pro Display', 13, QFont.Bold))
        accuracy_group.setStyleSheet('QGroupBox { padding-top: 28px; margin-top: 0px; } QGroupBox::title { left: 10px; top: 6px; }')
        accuracy_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        accuracy_layout = QVBoxLayout()
        accuracy_layout.setContentsMargins(8, 18, 8, 8)

        self.accuracy_figure = Figure(figsize=(7, 5))
        self.accuracy_canvas = FigureCanvas(self.accuracy_figure)
        self.accuracy_canvas.setMinimumHeight(0)
        self.accuracy_canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        accuracy_layout.addWidget(self.accuracy_canvas)

        accuracy_group.setLayout(accuracy_layout)
        charts_layout.addWidget(accuracy_group)

        # 题型分布柱状图
        type_group = QGroupBox('题型练习分布')
        type_group.setFont(QFont('SF Pro Display', 13, QFont.Bold))
        type_group.setStyleSheet('QGroupBox { padding-top: 28px; margin-top: 0px; } QGroupBox::title { left: 10px; top: 6px; }')
        type_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        type_layout = QVBoxLayout()
        type_layout.setContentsMargins(8, 18, 8, 8)

        self.type_figure = Figure(figsize=(7, 5))
        self.type_canvas = FigureCanvas(self.type_figure)
        self.type_canvas.setMinimumHeight(0)
        self.type_canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        type_layout.addWidget(self.type_canvas)

        type_group.setLayout(type_layout)
        charts_layout.addWidget(type_group)

        main_layout.addLayout(charts_layout)
        # 让图表区域占满剩余空间
        main_layout.setStretch(0, 0)  # 标题不伸展
        main_layout.setStretch(1, 1)  # 图表伸展
        charts_layout.setStretch(0, 1)
        charts_layout.setStretch(1, 1)


        self.setLayout(main_layout)

    def load_data(self):
        """加载数据"""
        self.load_accuracy_chart()
        self.load_type_chart()

    def load_accuracy_chart(self):
        """加载准确率饼图"""
        db_manager.connect()

        # 获取各分类的准确率
        categories = []
        accuracies = []

        for category in KNOWLEDGE_CATEGORIES:
            # 该分类的总题数
            total_query = """
                SELECT COUNT(*) as count FROM practice_records pr
                JOIN questions q ON pr.question_id = q.id
                WHERE pr.user_id = ? AND q.category = ?
            """
            total_result = db_manager.execute_query(total_query, (self.current_user.id, category))
            total_count = dict(total_result[0])['count'] if total_result else 0

            if total_count > 0:
                # 该分类的正确题数
                correct_query = """
                    SELECT COUNT(*) as count FROM practice_records pr
                    JOIN questions q ON pr.question_id = q.id
                    WHERE pr.user_id = ? AND q.category = ? AND pr.is_correct = 1
                """
                correct_result = db_manager.execute_query(
                    correct_query,
                    (self.current_user.id, category)
                )
                correct_count = dict(correct_result[0])['count'] if correct_result else 0

                accuracy = (correct_count / total_count) * 100
                categories.append(category)
                accuracies.append(round(accuracy, 1))

        db_manager.disconnect()

        # 绘制饼图
        self.accuracy_figure.clear()
        ax = self.accuracy_figure.add_subplot(111)

        if categories:
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8',
                     '#F7DC6F', '#BB8FCE', '#85C1E9', '#F8B739', '#52B788']
            wedges, texts, autotexts = ax.pie(
                accuracies,
                labels=categories,
                autopct='%1.1f%%',
                startangle=90,
                colors=colors[:len(categories)]
            )
            for text in texts:
                text.set_fontsize(11)
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontsize(10)
                autotext.set_weight('bold')
        else:
            ax.text(0.5, 0.5, '暂无数据', ha='center', va='center',
                   fontsize=14, transform=ax.transAxes)

        ax.set_title('各分类准确率', fontsize=14, fontweight='bold')
        self.accuracy_canvas.draw()

    def load_type_chart(self):
        """加载题型分布柱状图"""
        db_manager.connect()

        # 获取各题型的练习数量
        types = []
        counts = []

        for q_type, type_name in QUESTION_TYPES.items():
            query = """
                SELECT COUNT(*) as count FROM practice_records pr
                JOIN questions q ON pr.question_id = q.id
                WHERE pr.user_id = ? AND q.type = ?
            """
            result = db_manager.execute_query(query, (self.current_user.id, q_type))
            count = dict(result[0])['count'] if result else 0

            if count > 0:
                types.append(type_name)
                counts.append(count)

        db_manager.disconnect()

        # 绘制柱状图
        self.type_figure.clear()
        ax = self.type_figure.add_subplot(111)

        if types:
            colors = [THEME_COLORS['primary'], THEME_COLORS['success'],
                     THEME_COLORS['warning'], THEME_COLORS['danger']]
            bars = ax.bar(types, counts, color=colors[:len(types)], alpha=0.7)

            # 在柱子上显示数值
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom', fontsize=10, fontweight='bold')

            ax.set_ylabel('练习数量', fontsize=12)
            ax.set_title('题型练习分布', fontsize=14, fontweight='bold')
            ax.grid(axis='y', alpha=0.3)
        else:
            ax.text(0.5, 0.5, '暂无数据', ha='center', va='center',
                   fontsize=14, transform=ax.transAxes)

        self.type_canvas.draw()

    def refresh(self):
        """刷新数据"""
        self.load_data()
