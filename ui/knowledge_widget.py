# -*- coding: utf-8 -*-
"""
知识点学习模块
显示Python知识点内容，支持分类浏览和学习记录
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QListWidget, QTextEdit, QSplitter, QGroupBox, QMessageBox,
                             QListWidgetItem, QProgressBar)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QTextCursor
from database.db_manager import db_manager
from utils.data_loader import DataLoader
from config import KNOWLEDGE_CATEGORIES, THEME_COLORS
from datetime import datetime
import time


class KnowledgeWidget(QWidget):
    """知识点学习界面"""

    def __init__(self, user):
        """初始化知识点学习界面"""
        super().__init__()
        self.current_user = user
        self.current_knowledge = None
        self.start_time = None
        self.init_ui()
        self.load_categories()

    def init_ui(self):
        """初始化界面"""
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)

        # 创建分隔器
        splitter = QSplitter(Qt.Horizontal)

        # 左侧：分类和知识点列表
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        # 分类列表
        category_label = QLabel('知识点分类')
        category_label.setFont(QFont('Microsoft YaHei', 13, QFont.Bold))
        left_layout.addWidget(category_label)

        self.category_list = QListWidget()
        self.category_list.setFont(QFont('Microsoft YaHei', 12))
        self.category_list.setSpacing(8)  # 增加分类间距
        self.category_list.itemClicked.connect(self.on_category_selected)
        left_layout.addWidget(self.category_list)

        # 知识点列表
        knowledge_label = QLabel('知识点列表')
        knowledge_label.setFont(QFont('Microsoft YaHei', 13, QFont.Bold))
        left_layout.addWidget(knowledge_label)

        self.knowledge_list = QListWidget()
        self.knowledge_list.setFont(QFont('Microsoft YaHei', 12))
        self.knowledge_list.setSpacing(8)  # 增加知识点间距
        self.knowledge_list.itemClicked.connect(self.on_knowledge_selected)
        left_layout.addWidget(self.knowledge_list)

        splitter.addWidget(left_widget)

        # 右侧:知识点详情
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(10, 15, 10, 10)  # 增加顶部边距防止遮挡
        
        # 标题和操作按钮
        title_layout = QHBoxLayout()
        self.title_label = QLabel('请选择知识点')
        self.title_label.setFont(QFont('Microsoft YaHei', 16, QFont.Bold))
        self.title_label.setStyleSheet(f'color: {THEME_COLORS["primary"]};')
        title_layout.addWidget(self.title_label)

        title_layout.addStretch()

        self.mark_complete_btn = QPushButton('标记为已完成')
        self.mark_complete_btn.setFont(QFont('Microsoft YaHei', 12))
        try:
            from PyQt5.QtWidgets import QSizePolicy
            self.mark_complete_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        except Exception:
            pass
        self.mark_complete_btn.setMinimumHeight(44)
        self.mark_complete_btn.clicked.connect(self.mark_as_completed)
        self.mark_complete_btn.setEnabled(False)
        title_layout.addWidget(self.mark_complete_btn)

        right_layout.addLayout(title_layout)

        # 学习进度条
        progress_layout = QHBoxLayout()
        progress_label = QLabel('学习进度:')
        progress_label.setFont(QFont('Microsoft YaHei', 11))
        progress_layout.addWidget(progress_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        progress_layout.addWidget(self.progress_bar)

        right_layout.addLayout(progress_layout)

        # 知识点内容
        content_group = QGroupBox('知识点内容')
        content_group.setFont(QFont('Microsoft YaHei', 12, QFont.Bold))
        content_group.setStyleSheet('QGroupBox { padding-top: 20px; margin-top: 10px; }')
        content_layout = QVBoxLayout()

        self.content_text = QTextEdit()
        self.content_text.setFont(QFont('Microsoft YaHei', 13))
        self.content_text.setReadOnly(True)
        content_layout.addWidget(self.content_text)

        content_group.setLayout(content_layout)
        right_layout.addWidget(content_group, 3)

        # 代码示例
        code_group = QGroupBox('代码示例')
        code_group.setFont(QFont('Microsoft YaHei', 12, QFont.Bold))
        code_group.setStyleSheet('QGroupBox { padding-top: 22px; margin-top: 2px; }')  # 减小上边距让代码框上移
        code_layout = QVBoxLayout()

        self.code_text = QTextEdit()
        self.code_text.setFont(QFont('Consolas', 11))
        self.code_text.setReadOnly(True)
        self.code_text.setStyleSheet('''
            QTextEdit {
                background-color: #263238;
                color: #AAAAAA;
                border: 1px solid #455A64;
                padding: 10px;
            }
        ''')
        code_layout.addWidget(self.code_text)

        code_group.setLayout(code_layout)
        right_layout.addWidget(code_group, 2)  # 增加代码示例区域比例

        # 学习时长显示
        self.time_label = QLabel('学习时长: 0 秒')
        self.time_label.setFont(QFont('Microsoft YaHei', 11))
        right_layout.addWidget(self.time_label)

        splitter.addWidget(right_widget)

        # 设置分隔器比例
        splitter.setSizes([300, 700])

        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

        # 创建定时器用于记录学习时长
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_study_time)

    def load_categories(self):
        """加载分类列表"""
        self.category_list.clear()
        for category in KNOWLEDGE_CATEGORIES:
            item = QListWidgetItem(category)
            self.category_list.addItem(item)

    def on_category_selected(self, item):
        """分类被选中"""
        category = item.text()
        self.load_knowledge_by_category(category)

    def load_knowledge_by_category(self, category):
        """加载指定分类的知识点"""
        self.knowledge_list.clear()
        knowledge_points = DataLoader.load_knowledge_by_category(category)

        for kp in knowledge_points:
            item = QListWidgetItem(f"{kp.title}")
            item.setData(Qt.UserRole, kp)
            self.knowledge_list.addItem(item)

        if not knowledge_points:
            item = QListWidgetItem("暂无知识点")
            item.setFlags(Qt.NoItemFlags)
            self.knowledge_list.addItem(item)

    def on_knowledge_selected(self, item):
        """知识点被选中"""
        knowledge = item.data(Qt.UserRole)
        if knowledge:
            self.display_knowledge(knowledge)
            self.start_learning_timer()

    def display_knowledge(self, knowledge):
        """显示知识点详情"""
        self.current_knowledge = knowledge

        # 更新标题
        self.title_label.setText(f"{knowledge.category} - {knowledge.title}")

        # 更新内容
        self.content_text.setPlainText(knowledge.content)

        # 更新代码示例
        if knowledge.code_example:
            self.code_text.setPlainText(knowledge.code_example)
        else:
            self.code_text.setPlainText("# 暂无代码示例")

        # 启用完成按钮
        self.mark_complete_btn.setEnabled(True)

        # 更新学习进度
        self.update_progress()

    def start_learning_timer(self):
        """开始学习计时"""
        self.start_time = time.time()
        self.timer.start(1000)  # 每秒更新一次

    def update_study_time(self):
        """更新学习时长显示"""
        if self.start_time:
            elapsed = int(time.time() - self.start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60
            self.time_label.setText(f'📊 学习时长: {minutes} 分 {seconds} 秒')

    def mark_as_completed(self):
        """标记为已完成"""
        if not self.current_knowledge:
            return

        # 计算学习时长
        study_time = int(time.time() - self.start_time) if self.start_time else 0

        # 保存学习记录
        db_manager.connect()

        # 检查是否已有记录
        query = """
            SELECT id, study_time FROM learning_records
            WHERE user_id = ? AND knowledge_id = ?
        """
        result = db_manager.execute_query(
            query,
            (self.current_user.id, self.current_knowledge.id)
        )

        if result:
            # 更新现有记录
            record = dict(result[0])
            total_time = record['study_time'] + study_time
            update_query = """
                UPDATE learning_records
                SET study_time = ?, completed = 1, last_study_at = ?
                WHERE id = ?
            """
            db_manager.execute_update(
                update_query,
                (total_time, datetime.now(), record['id'])
            )
        else:
            # 创建新记录
            insert_query = """
                INSERT INTO learning_records
                (user_id, knowledge_id, study_time, completed, last_study_at)
                VALUES (?, ?, ?, 1, ?)
            """
            db_manager.insert(
                insert_query,
                (self.current_user.id, self.current_knowledge.id, study_time, datetime.now())
            )

        db_manager.disconnect()

        QMessageBox.information(self, '成功', '已标记为完成！')
        self.update_progress()

        # 重置计时器
        self.timer.stop()
        self.start_time = None
        self.time_label.setText('📊 学习时长: 0 秒')

    def update_progress(self):
        """更新学习进度"""
        db_manager.connect()

        # 总知识点数
        total_query = "SELECT COUNT(*) as count FROM knowledge_points"
        total_result = db_manager.execute_query(total_query)
        total_count = dict(total_result[0])['count'] if total_result else 0

        # 已完成数
        completed_query = """
            SELECT COUNT(*) as count FROM learning_records
            WHERE user_id = ? AND completed = 1
        """
        completed_result = db_manager.execute_query(completed_query, (self.current_user.id,))
        completed_count = dict(completed_result[0])['count'] if completed_result else 0

        db_manager.disconnect()

        if total_count > 0:
            progress = int((completed_count / total_count) * 100)
            self.progress_bar.setValue(progress)
            self.progress_bar.setFormat(f'{completed_count}/{total_count} ({progress}%)')
        else:
            self.progress_bar.setValue(0)
            self.progress_bar.setFormat('0/0 (0%)')

    def refresh(self):
        """刷新数据"""
        self.load_categories()
        self.update_progress()
