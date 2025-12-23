# -*- coding: utf-8 -*-
"""
错题本模块
显示和管理用户的错题
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QTableWidget, QTableWidgetItem, QGroupBox, QMessageBox,
                             QHeaderView, QTextEdit, QDialog, QDialogButtonBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from utils.data_loader import DataLoader
from models.question import Question
from config import THEME_COLORS, QUESTION_TYPES
from database.db_manager import db_manager
from datetime import datetime


class MistakesWidget(QWidget):
    """错题本界面"""

    def __init__(self, user):
        """初始化错题本界面"""
        super().__init__()
        self.current_user = user
        self.init_ui()
        self.load_data()

    def init_ui(self):
        """初始化界面"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)

        # 标题和操作按钮
        header_layout = QHBoxLayout()

        title_label = QLabel('我的错题本')
        title_label.setObjectName('pageTitle')
        title_label.setFont(QFont('Microsoft YaHei', 16, QFont.Bold))
        title_label.setStyleSheet(f'color: {THEME_COLORS["danger"]};')
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        refresh_btn = QPushButton('刷新')
        refresh_btn.setFont(QFont('Microsoft YaHei', 10))
        refresh_btn.clicked.connect(self.refresh)
        header_layout.addWidget(refresh_btn)

        main_layout.addLayout(header_layout)

        # 统计信息
        stats_layout = QHBoxLayout()

        self.total_label = QLabel('总错题数: 0')
        self.total_label.setFont(QFont('Microsoft YaHei', 11))
        stats_layout.addWidget(self.total_label)

        stats_layout.addSpacing(30)

        self.unmastered_label = QLabel('未掌握: 0')
        self.unmastered_label.setFont(QFont('Microsoft YaHei', 11))
        self.unmastered_label.setStyleSheet(f'color: {THEME_COLORS["danger"]};')
        stats_layout.addWidget(self.unmastered_label)

        stats_layout.addStretch()

        main_layout.addLayout(stats_layout)

        # 错题表格
        table_group = QGroupBox('📋 错题列表')
        table_group.setFont(QFont('Microsoft YaHei', 11, QFont.Bold))
        table_group.setStyleSheet('QGroupBox { padding-top: 20px; margin-top: 10px; }')
        table_layout = QVBoxLayout()

        self.mistakes_table = QTableWidget()
        self.mistakes_table.setColumnCount(7)
        self.mistakes_table.setHorizontalHeaderLabels([
            '题目', '类型', '分类', '错误次数', '首次错误', '最近错误', '操作'
        ])
        self.mistakes_table.setFont(QFont('Microsoft YaHei', 10))
        self.mistakes_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.mistakes_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.mistakes_table.setSelectionBehavior(QTableWidget.SelectRows)
        table_layout.addWidget(self.mistakes_table)

        table_group.setLayout(table_layout)
        main_layout.addWidget(table_group)

        self.setLayout(main_layout)

    def load_data(self):
        """加载错题数据"""
        self.mistakes_table.setRowCount(0)

        wrong_questions = DataLoader.load_user_wrong_questions(self.current_user.id)

        # 更新统计信息
        self.total_label.setText(f'总错题数: {len(wrong_questions)}')
        unmastered_count = sum(1 for wq in wrong_questions if not wq.get('mastered', False))
        self.unmastered_label.setText(f'未掌握: {unmastered_count}')

        # 填充表格
        for i, wq in enumerate(wrong_questions):
            self.mistakes_table.insertRow(i)

            # 题目
            question_text = wq.get('question', '')
            if len(question_text) > 50:
                question_text = question_text[:50] + '...'
            question_item = QTableWidgetItem(question_text)
            self.mistakes_table.setItem(i, 0, question_item)

            # 类型
            q_type = wq.get('type', '')
            type_text = QUESTION_TYPES.get(q_type, q_type)
            type_item = QTableWidgetItem(type_text)
            type_item.setTextAlignment(Qt.AlignCenter)
            self.mistakes_table.setItem(i, 1, type_item)

            # 分类
            category_item = QTableWidgetItem(wq.get('category', ''))
            category_item.setTextAlignment(Qt.AlignCenter)
            self.mistakes_table.setItem(i, 2, category_item)

            # 错误次数
            wrong_count = wq.get('wrong_count', 0)
            count_item = QTableWidgetItem(str(wrong_count))
            count_item.setTextAlignment(Qt.AlignCenter)
            self.mistakes_table.setItem(i, 3, count_item)

            # 首次错误时间
            first_wrong = wq.get('first_wrong_at', '')
            if first_wrong:
                first_time_str = str(first_wrong)[:19]
            else:
                first_time_str = ''
            first_item = QTableWidgetItem(first_time_str)
            first_item.setTextAlignment(Qt.AlignCenter)
            self.mistakes_table.setItem(i, 4, first_item)

            # 最近错误时间
            last_wrong = wq.get('last_wrong_at', '')
            if last_wrong:
                last_time_str = str(last_wrong)[:19]
            else:
                last_time_str = ''
            last_item = QTableWidgetItem(last_time_str)
            last_item.setTextAlignment(Qt.AlignCenter)
            self.mistakes_table.setItem(i, 5, last_item)

            # 操作按钮
            btn_widget = QWidget()
            btn_layout = QHBoxLayout(btn_widget)
            btn_layout.setContentsMargins(5, 2, 5, 2)

            view_btn = QPushButton('查看')
            view_btn.setFont(QFont('Microsoft YaHei', 9))
            view_btn.clicked.connect(lambda checked, row=i: self.view_question(row))
            btn_layout.addWidget(view_btn)

            master_btn = QPushButton('已掌握')
            master_btn.setFont(QFont('Microsoft YaHei', 9))
            master_btn.clicked.connect(lambda checked, row=i: self.mark_mastered(row))
            btn_layout.addWidget(master_btn)

            btn_layout.setContentsMargins(0, 0, 0, 0)
            self.mistakes_table.setCellWidget(i, 6, btn_widget)

        # 保存数据引用
        self.wrong_questions_data = wrong_questions

    def view_question(self, row):
        """查看题目详情"""
        if row >= len(self.wrong_questions_data):
            return

        wq = self.wrong_questions_data[row]

        # 创建对话框
        dialog = QDialog(self)
        dialog.setWindowTitle('错题详情')
        dialog.setMinimumSize(600, 500)

        layout = QVBoxLayout()

        # 题目信息
        info_text = f'''
题型: {QUESTION_TYPES.get(wq.get('type', ''), wq.get('type', ''))}
分类: {wq.get('category', '')}
错误次数: {wq.get('wrong_count', 0)}
        '''
        info_label = QLabel(info_text)
        info_label.setFont(QFont('Microsoft YaHei', 10))
        layout.addWidget(info_label)

        # 题目内容
        question_group = QGroupBox('题目')
        question_layout = QVBoxLayout()
        question_text = QTextEdit()
        question_text.setFont(QFont('Microsoft YaHei', 11))
        question_text.setReadOnly(True)
        question_text.setPlainText(wq.get('question', ''))
        question_text.setMaximumHeight(100)
        question_layout.addWidget(question_text)
        question_group.setLayout(question_layout)
        layout.addWidget(question_group)

        # 选项（如果有）
        options = wq.get('options')
        if options:
            try:
                import json
                if isinstance(options, str):
                    options_list = json.loads(options)
                else:
                    options_list = options

                options_group = QGroupBox('选项')
                options_layout = QVBoxLayout()
                options_text = QTextEdit()
                options_text.setFont(QFont('Microsoft YaHei', 11))
                options_text.setReadOnly(True)
                options_text.setPlainText('\n'.join(options_list))
                options_text.setMaximumHeight(100)
                options_layout.addWidget(options_text)
                options_group.setLayout(options_layout)
                layout.addWidget(options_group)
            except:
                pass

        # 正确答案
        answer_group = QGroupBox('正确答案')
        answer_layout = QVBoxLayout()
        answer_label = QLabel(wq.get('answer', ''))
        answer_label.setFont(QFont('Microsoft YaHei', 12, QFont.Bold))
        answer_label.setStyleSheet(f'color: {THEME_COLORS["success"]};')
        answer_layout.addWidget(answer_label)
        answer_group.setLayout(answer_layout)
        layout.addWidget(answer_group)

        # 解析
        explanation = wq.get('explanation', '')
        if explanation:
            explanation_group = QGroupBox('解析')
            explanation_layout = QVBoxLayout()
            explanation_text = QTextEdit()
            explanation_text.setFont(QFont('Microsoft YaHei', 11))
            explanation_text.setReadOnly(True)
            explanation_text.setPlainText(explanation)
            explanation_layout.addWidget(explanation_text)
            explanation_group.setLayout(explanation_layout)
            layout.addWidget(explanation_group)

        # 按钮
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(dialog.accept)
        layout.addWidget(button_box)

        dialog.setLayout(layout)
        dialog.exec_()

    def mark_mastered(self, row):
        """标记为已掌握"""
        if row >= len(self.wrong_questions_data):
            return

        wq = self.wrong_questions_data[row]

        reply = QMessageBox.question(
            self, '确认',
            '确定已经掌握这道题了吗？',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            db_manager.connect()
            update_query = """
                UPDATE wrong_questions
                SET mastered = 1
                WHERE user_id = ? AND question_id = ?
            """
            db_manager.execute_update(
                update_query,
                (self.current_user.id, wq.get('question_id'))
            )
            db_manager.disconnect()

            QMessageBox.information(self, '成功', '已标记为掌握！')
            self.refresh()

    def refresh(self):
        """刷新数据"""
        self.load_data()
