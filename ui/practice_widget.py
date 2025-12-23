# -*- coding: utf-8 -*-
"""
题库练习模块
支持选择题、判断题、填空题、编程题的练习
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QListWidget, QTextEdit, QRadioButton, QLineEdit, QGroupBox,
                             QMessageBox, QButtonGroup, QComboBox, QCheckBox, QSplitter,
                             QListWidgetItem, QProgressBar, QScrollArea)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from database.db_manager import db_manager
from utils.data_loader import DataLoader
from utils.code_executor import CodeExecutor
from models.question import Question
from config import KNOWLEDGE_CATEGORIES, QUESTION_TYPES, THEME_COLORS
from datetime import datetime
import time
import json


class PracticeWidget(QWidget):
    """题库练习界面"""

    def __init__(self, user):
        """初始化题库练习界面"""
        super().__init__()
        self.current_user = user
        self.current_question = None
        self.current_questions = []
        self.current_index = 0
        self.start_time = None
        self.code_executor = CodeExecutor()
        self.init_ui()

    def init_ui(self):
        """初始化界面"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)

        # 顶部：筛选条件 + 进度合并成一张卡片
        filter_group = QGroupBox('筛选与进度')
        filter_group.setFont(QFont('Microsoft YaHei', 11, QFont.Bold))
        filter_group.setStyleSheet('QGroupBox { padding-top: 20px; margin-top: 10px; }')
        filter_group_layout = QVBoxLayout()

        filter_layout = QHBoxLayout()

        category_label = QLabel('分类:')
        category_label.setFont(QFont('Microsoft YaHei', 10))
        filter_layout.addWidget(category_label)

        self.category_combo = QComboBox()
        self.category_combo.setFont(QFont('Microsoft YaHei', 10))
        self.category_combo.addItem('全部')
        for category in KNOWLEDGE_CATEGORIES:
            self.category_combo.addItem(category)
        self.category_combo.currentTextChanged.connect(self.on_filter_changed)
        filter_layout.addWidget(self.category_combo)

        type_label = QLabel('题型:')
        type_label.setFont(QFont('Microsoft YaHei', 10))
        filter_layout.addWidget(type_label)

        self.type_combo = QComboBox()
        self.type_combo.setFont(QFont('Microsoft YaHei', 10))
        self.type_combo.addItem('全部')
        for key, value in QUESTION_TYPES.items():
            self.type_combo.addItem(value, key)
        self.type_combo.currentTextChanged.connect(self.on_filter_changed)
        filter_layout.addWidget(self.type_combo)

        filter_layout.addStretch()

        # 只显示未做题目开关，避免访问未定义控件导致加载崩溃
        self.only_new_checkbox = QCheckBox('只显示未做题目')
        self.only_new_checkbox.setFont(QFont('Microsoft YaHei', 10))
        filter_layout.addWidget(self.only_new_checkbox)

        load_btn = QPushButton('📥 加载题目')
        load_btn.setFont(QFont('Microsoft YaHei', 10))
        load_btn.clicked.connect(self.load_questions)
        filter_layout.addWidget(load_btn)

        filter_group_layout.addLayout(filter_layout)

        # 进度显示
        progress_layout = QHBoxLayout()
        self.question_label = QLabel('题目: 0/0')
        self.question_label.setFont(QFont('Microsoft YaHei', 10))
        progress_layout.addWidget(self.question_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)

        self.time_label = QLabel('用时: 0 秒')
        self.time_label.setFont(QFont('Microsoft YaHei', 10))
        progress_layout.addWidget(self.time_label)

        filter_group_layout.addLayout(progress_layout)
        filter_group.setLayout(filter_group_layout)
        main_layout.addWidget(filter_group)

        # 题目显示区域
        question_group = QGroupBox('题目')
        question_group.setFont(QFont('Microsoft YaHei', 11, QFont.Bold))
        question_group.setStyleSheet('QGroupBox { padding-top: 20px; margin-top: 10px; }')
        question_layout = QVBoxLayout()

        self.question_text = QTextEdit()
        self.question_text.setFont(QFont('Microsoft YaHei', 16))  # 放大题目字体
        self.question_text.setReadOnly(True)
        self.question_text.setMaximumHeight(420)  # 继续扩大
        question_layout.addWidget(self.question_text)

        question_group.setLayout(question_layout)
        main_layout.addWidget(question_group)

        # 答题区域（使用滚动区域）
        answer_group = QGroupBox('答题区')
        answer_group.setFont(QFont('Microsoft YaHei', 11, QFont.Bold))
        answer_group.setStyleSheet('QGroupBox { padding-top: 20px; margin-top: 10px; }')
        answer_group_layout = QVBoxLayout()

        answer_scroll = QScrollArea()
        answer_scroll.setWidgetResizable(True)
        answer_scroll.setMinimumHeight(150)  # 減少高度

        self.answer_widget = QWidget()
        self.answer_layout = QVBoxLayout(self.answer_widget)
        answer_scroll.setWidget(self.answer_widget)

        answer_group_layout.addWidget(answer_scroll)
        answer_group.setLayout(answer_group_layout)

        main_layout.addWidget(answer_group)

        # 解析显示区域
        explanation_group = QGroupBox('💡 解析')
        explanation_group.setFont(QFont('Microsoft YaHei', 11, QFont.Bold))
        explanation_group.setStyleSheet('QGroupBox { padding-top: 20px; margin-top: 10px; }')  # 防止标题和内容重叠
        explanation_layout = QVBoxLayout()

        self.explanation_text = QTextEdit()
        self.explanation_text.setFont(QFont('Microsoft YaHei', 13))  # 放大解析字体
        self.explanation_text.setReadOnly(True)
        # 移除最大高度限制，让解析内容完整显示并支持页面滑动
        explanation_layout.addWidget(self.explanation_text)

        explanation_group.setLayout(explanation_layout)
        main_layout.addWidget(explanation_group)

        # 底部按钮
        button_layout = QHBoxLayout()

        self.prev_btn = QPushButton('⬅️ 上一题')
        self.prev_btn.setFont(QFont('Microsoft YaHei', 10))
        self.prev_btn.clicked.connect(self.prev_question)
        self.prev_btn.setEnabled(False)
        button_layout.addWidget(self.prev_btn)

        self.submit_btn = QPushButton('✓ 提交答案')
        self.submit_btn.setFont(QFont('Microsoft YaHei', 10, QFont.Bold))
        self.submit_btn.setStyleSheet(f'''
            QPushButton {{
                background-color: {THEME_COLORS["primary"]};
                color: white;
                padding: 8px 20px;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: #1976D2;
            }}
            QPushButton:disabled {{
                background-color: #CCCCCC;
            }}
        ''')
        self.submit_btn.clicked.connect(self.submit_answer)
        self.submit_btn.setEnabled(False)
        button_layout.addWidget(self.submit_btn)

        self.next_btn = QPushButton('➡️ 下一题')
        self.next_btn.setFont(QFont('Microsoft YaHei', 10))
        self.next_btn.clicked.connect(self.next_question)
        self.next_btn.setEnabled(False)
        button_layout.addWidget(self.next_btn)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # 创建定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)

    def on_filter_changed(self):
        """筛选条件改变"""
        pass  # 可以在这里添加自动加载功能

    def load_questions(self):
        """加载题目"""
        try:
            category = self.category_combo.currentText()
            q_type = self.type_combo.currentData()
            only_new = self.only_new_checkbox.isChecked()

            db_manager.connect()

            # 构建基础查询和排除已做题目的子查询
            exclude_done = ""
            params = []

            if only_new:
                # 排除已做题目
                exclude_done = " AND id NOT IN (SELECT question_id FROM practice_records WHERE user_id = ?)"
                params.append(self.current_user.id)

            if category == '全部' and not q_type:
                query = f"SELECT * FROM questions WHERE 1=1{exclude_done} ORDER BY RANDOM()"
                results = db_manager.execute_query(query, tuple(params))
            elif category == '全部':
                query = f"SELECT * FROM questions WHERE type = ?{exclude_done} ORDER BY RANDOM()"
                params.insert(0, q_type)
                results = db_manager.execute_query(query, tuple(params))
            elif not q_type:
                query = f"SELECT * FROM questions WHERE category = ?{exclude_done} ORDER BY RANDOM()"
                params.insert(0, category)
                results = db_manager.execute_query(query, tuple(params))
            else:
                query = f"SELECT * FROM questions WHERE category = ? AND type = ?{exclude_done} ORDER BY RANDOM()"
                params = [category, q_type] + params
                results = db_manager.execute_query(query, tuple(params))

            db_manager.disconnect()

            self.current_questions = []
            for row in results:
                q = Question.from_dict(dict(row))
                self.current_questions.append(q)

            if self.current_questions:
                self.current_index = 0
                self.display_question(self.current_questions[0])
                self.update_navigation()
                status = "（仅未做）" if only_new else "（包含已做）"
                QMessageBox.information(self, '成功', f'已加载 {len(self.current_questions)} 道题目{status}！')
            else:
                if only_new:
                    QMessageBox.warning(self, '提示', '没有找到未做的题目！\n提示：可以取消勾选"只显示未做题目"来查看所有题目。')
                else:
                    QMessageBox.warning(self, '提示', '没有找到符合条件的题目！')
                self.clear_display()
        except Exception as e:
            # 添加错误处理，防止崩溃
            import traceback
            error_msg = f'加载题目失败: {str(e)}\n\n{traceback.format_exc()}'
            print(f'[ERROR] {error_msg}')
            QMessageBox.critical(self, '错误', f'加载题目失败: {str(e)}')
            try:
                db_manager.disconnect()
            except:
                pass

    def display_question(self, question):
        """显示题目"""
        self.current_question = question
        self.start_time = time.time()
        self.timer.start(1000)

        # 更新题目编号
        self.question_label.setText(f'题目: {self.current_index + 1}/{len(self.current_questions)}')

        # 更新进度条
        if len(self.current_questions) > 0:
            progress = int(((self.current_index + 1) / len(self.current_questions)) * 100)
            self.progress_bar.setValue(progress)

        # 显示题目内容
        question_html = f'''
        <p style="font-size: 36px;">
            <b>[{QUESTION_TYPES.get(question.type, question.type)}] {question.category}</b>
        </p>
        <p style="font-size: 34px; line-height: 2.4;">{question.question}</p>
        '''
        self.question_text.setHtml(question_html)

        # 清空解析
        self.explanation_text.clear()

        # 根据题型显示答题区域
        self.clear_answer_widget()

        if question.type == 'choice':
            self.display_choice_answer(question)
        elif question.type == 'judge':
            self.display_judge_answer(question)
        elif question.type == 'fill':
            self.display_fill_answer(question)
        elif question.type == 'code':
            self.display_code_answer(question)

        self.submit_btn.setEnabled(True)

    def clear_answer_widget(self):
        """清空答题区域"""
        # 删除所有子部件
        while self.answer_layout.count():
            child = self.answer_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def display_choice_answer(self, question):
        """显示选择题答题区域"""
        self.button_group = QButtonGroup()

        for i, option in enumerate(question.options):
            radio = QRadioButton(option)
            radio.setFont(QFont('Microsoft YaHei', 14))  # 放大选项字体
            self.button_group.addButton(radio, i)
            self.answer_layout.addWidget(radio)

        self.answer_layout.addStretch()

    def display_judge_answer(self, question):
        """显示判断题答题区域"""
        self.button_group = QButtonGroup()

        true_radio = QRadioButton('正确 (T)')
        true_radio.setFont(QFont('Microsoft YaHei', 14))  # 放大判断选项字体
        self.button_group.addButton(true_radio, 0)
        self.answer_layout.addWidget(true_radio)

        false_radio = QRadioButton('错误 (F)')
        false_radio.setFont(QFont('Microsoft YaHei', 14))  # 放大判断选项字体
        self.button_group.addButton(false_radio, 1)
        self.answer_layout.addWidget(false_radio)

        self.answer_layout.addStretch()

    def display_fill_answer(self, question):
        """显示填空题答题区域"""
        label = QLabel('请输入答案:')
        label.setFont(QFont('Microsoft YaHei', 14))  # 放大提示文本
        self.answer_layout.addWidget(label)

        self.fill_input = QLineEdit()
        self.fill_input.setFont(QFont('Microsoft YaHei', 13))  # 放大输入框字体
        self.fill_input.setPlaceholderText('在此输入答案...')
        self.answer_layout.addWidget(self.fill_input)

        self.answer_layout.addStretch()

    def display_code_answer(self, question):
        """显示编程题答题区域"""
        label = QLabel('请输入Python代码:')
        label.setFont(QFont('Microsoft YaHei', 14))  # 放大提示文本
        self.answer_layout.addWidget(label)

        self.code_input = QTextEdit()
        self.code_input.setFont(QFont('Consolas', 12))  # 放大代码字体
        self.code_input.setPlaceholderText('在此输入Python代码...')
        self.code_input.setMinimumHeight(200)  # 增加最小高度
        self.code_input.setStyleSheet('''
            QTextEdit {
                background-color: #263238;
                color: #AAAAAA;
                border: 1px solid #455A64;
                padding: 10px;
            }
        ''')
        self.answer_layout.addWidget(self.code_input)

        run_btn = QPushButton('▶️ 运行代码')
        run_btn.setFont(QFont('Microsoft YaHei', 12))  # 放大按马字体
        run_btn.clicked.connect(self.run_code)
        self.answer_layout.addWidget(run_btn)

        output_label = QLabel('运行结果:')
        output_label.setFont(QFont('Microsoft YaHei', 12))  # 放大输出提示
        self.answer_layout.addWidget(output_label)

        self.code_output = QTextEdit()
        self.code_output.setFont(QFont('Consolas', 11))  # 放大输出字体
        self.code_output.setReadOnly(True)
        self.code_output.setMaximumHeight(150)  # 增加输出高度
        self.answer_layout.addWidget(self.code_output)

    def run_code(self):
        """运行代码"""
        if not hasattr(self, 'code_input'):
            return

        code = self.code_input.toPlainText().strip()
        if not code:
            self.code_output.setPlainText('请输入代码！')
            return

        # 验证代码语法
        is_valid, error = self.code_executor.validate_code(code)
        if not is_valid:
            self.code_output.setPlainText(f'❌ 语法错误:\n{error}')
            return

        # 执行代码
        success, output, error = self.code_executor.execute(code)
        if success:
            result = f'✓ 执行成功:\n{output if output else "(无输出)"}'
            self.code_output.setPlainText(result)
        else:
            self.code_output.setPlainText(f'❌ 执行错误:\n{error}')

    def submit_answer(self):
        """提交答案"""
        if not self.current_question:
            return

        user_answer = self.get_user_answer()
        if user_answer is None:
            QMessageBox.warning(self, '提示', '请先作答！')
            return

        # 停止计时
        self.timer.stop()
        time_spent = int(time.time() - self.start_time) if self.start_time else 0

        # 检查答案
        is_correct = self.current_question.check_answer(user_answer)

        # 保存练习记录
        db_manager.connect()
        insert_query = """
            INSERT INTO practice_records
            (user_id, question_id, user_answer, is_correct, submit_time, time_spent)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        db_manager.insert(
            insert_query,
            (self.current_user.id, self.current_question.id, str(user_answer),
             is_correct, datetime.now(), time_spent)
        )

        # 如果答错，添加到错题本
        if not is_correct:
            # 检查错题本中是否已存在
            check_query = """
                SELECT id, wrong_count FROM wrong_questions
                WHERE user_id = ? AND question_id = ?
            """
            result = db_manager.execute_query(
                check_query,
                (self.current_user.id, self.current_question.id)
            )

            if result:
                # 更新错误次数
                wrong_record = dict(result[0])
                update_query = """
                    UPDATE wrong_questions
                    SET wrong_count = ?, last_wrong_at = ?
                    WHERE id = ?
                """
                db_manager.execute_update(
                    update_query,
                    (wrong_record['wrong_count'] + 1, datetime.now(), wrong_record['id'])
                )
            else:
                # 添加新的错题记录
                insert_wrong_query = """
                    INSERT INTO wrong_questions
                    (user_id, question_id, wrong_count, mastered, first_wrong_at, last_wrong_at)
                    VALUES (?, ?, 1, 0, ?, ?)
                """
                db_manager.insert(
                    insert_wrong_query,
                    (self.current_user.id, self.current_question.id,
                     datetime.now(), datetime.now())
                )

        db_manager.disconnect()

        # 显示结果和解析
        self.show_result(is_correct, user_answer)

        # 禁用提交按钮
        self.submit_btn.setEnabled(False)

    def get_user_answer(self):
        """获取用户答案"""
        if not self.current_question:
            return None

        if self.current_question.type == 'choice':
            if hasattr(self, 'button_group'):
                checked = self.button_group.checkedId()
                if checked >= 0:
                    options = ['A', 'B', 'C', 'D', 'E', 'F']
                    return options[checked] if checked < len(options) else None
        elif self.current_question.type == 'judge':
            if hasattr(self, 'button_group'):
                checked = self.button_group.checkedId()
                if checked == 0:
                    return 'T'
                elif checked == 1:
                    return 'F'
        elif self.current_question.type == 'fill':
            if hasattr(self, 'fill_input'):
                answer = self.fill_input.text().strip()
                return answer if answer else None
        elif self.current_question.type == 'code':
            if hasattr(self, 'code_input'):
                code = self.code_input.toPlainText().strip()
                return code if code else None

        return None

    def show_result(self, is_correct, user_answer):
        """显示答题结果"""
        if is_correct:
            result_msg = f'✓ 回答正确！\n'
        else:
            result_msg = f'✗ 回答错误！\n'
            result_msg += f'您的答案: {user_answer}\n'
            result_msg += f'正确答案: {self.current_question.answer}\n'

        if self.current_question.explanation:
            result_msg += f'\n{self.current_question.explanation}'

        self.explanation_text.setPlainText(result_msg)

        # 显示消息框
        if is_correct:
            QMessageBox.information(self, '正确', '✓ 回答正确！')
        else:
            QMessageBox.warning(self, '错误', f'✗ 回答错误！\n正确答案: {self.current_question.answer}')

    def prev_question(self):
        """上一题"""
        if self.current_index > 0:
            self.current_index -= 1
            self.display_question(self.current_questions[self.current_index])
            self.update_navigation()

    def next_question(self):
        """下一题"""
        if self.current_index < len(self.current_questions) - 1:
            self.current_index += 1
            self.display_question(self.current_questions[self.current_index])
            self.update_navigation()

    def update_navigation(self):
        """更新导航按钮状态"""
        self.prev_btn.setEnabled(self.current_index > 0)
        self.next_btn.setEnabled(self.current_index < len(self.current_questions) - 1)

    def update_time(self):
        """更新用时显示"""
        if self.start_time:
            elapsed = int(time.time() - self.start_time)
            self.time_label.setText(f'用时: {elapsed} 秒')

    def clear_display(self):
        """清空显示"""
        self.question_text.clear()
        self.explanation_text.clear()
        self.clear_answer_widget()
        self.question_label.setText('题目: 0/0')
        self.progress_bar.setValue(0)
        self.time_label.setText('用时: 0 秒')
        self.submit_btn.setEnabled(False)
        self.prev_btn.setEnabled(False)
        self.next_btn.setEnabled(False)

    def refresh(self):
        """刷新数据"""
        pass  # 题库数据一般不需要刷新
