# -*- coding: utf-8 -*-
"""
代码编辑器模块
提供Python代码编写和执行功能
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QTextEdit, QGroupBox, QMessageBox, QFileDialog, QSplitter)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from utils.code_executor import CodeExecutor
from config import EDITOR_CONFIG, THEME_COLORS
import os


class EditorWidget(QWidget):
    """代码编辑器界面"""

    def __init__(self, user):
        """初始化代码编辑器界面"""
        super().__init__()
        self.current_user = user
        self.code_executor = CodeExecutor(timeout=EDITOR_CONFIG['timeout'])
        self.current_file = None
        self.init_ui()

    def init_ui(self):
        """初始化界面"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)

        # 顶部工具栏（加框显示）
        toolbar_group = QGroupBox('🛠️ 工具栏')
        toolbar_group.setFont(QFont('Microsoft YaHei', 11, QFont.Bold))
        toolbar_group.setStyleSheet('QGroupBox { padding-top: 20px; margin-top: 10px; }')
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setContentsMargins(10, 6, 10, 10)  # 四周留白
        toolbar_layout.setSpacing(8)  # 按钮间距

        new_btn = QPushButton('📄 新建')
        new_btn.setFont(QFont('Microsoft YaHei', 10))
        new_btn.setMinimumHeight(35)  # 统一按钮高度
        new_btn.clicked.connect(self.new_file)
        toolbar_layout.addWidget(new_btn)

        open_btn = QPushButton('📂 打开')
        open_btn.setFont(QFont('Microsoft YaHei', 10))
        open_btn.setMinimumHeight(35)  # 统一按钮高度
        open_btn.clicked.connect(self.open_file)
        toolbar_layout.addWidget(open_btn)

        save_btn = QPushButton('💾 保存')
        save_btn.setFont(QFont('Microsoft YaHei', 10))
        save_btn.setMinimumHeight(35)  # 统一按钮高度
        save_btn.clicked.connect(self.save_file)
        toolbar_layout.addWidget(save_btn)

        toolbar_layout.addSpacing(20)

        run_btn = QPushButton('▶️ 运行代码')
        run_btn.setFont(QFont('Microsoft YaHei', 11, QFont.Bold))  # 放大按钮字体
        run_btn.setMinimumHeight(35)  # 扩大按钮高度
        run_btn.setStyleSheet(f'''
            QPushButton {{
                background-color: {THEME_COLORS["success"]};
                color: white;
                padding: 10px 24px;
                border-radius: 5px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #388E3C;
            }}
        ''')
        run_btn.clicked.connect(self.run_code)
        toolbar_layout.addWidget(run_btn)

        clear_btn = QPushButton('🗑️ 清空')
        clear_btn.setFont(QFont('Microsoft YaHei', 10))
        clear_btn.setMinimumHeight(35)  # 统一按钮高度
        clear_btn.clicked.connect(self.clear_editor)
        toolbar_layout.addWidget(clear_btn)

        toolbar_layout.addStretch()

        self.file_label = QLabel('未命名文件')
        self.file_label.setFont(QFont('Microsoft YaHei', 10))
        toolbar_layout.addWidget(self.file_label)

        toolbar_group.setLayout(toolbar_layout)
        main_layout.addWidget(toolbar_group)

        # 创建分隔器
        splitter = QSplitter(Qt.Vertical)

        # 代码编辑区域
        editor_group = QGroupBox('💻 代码编辑器')
        editor_group.setFont(QFont('Microsoft YaHei', 11, QFont.Bold))
        editor_group.setStyleSheet('QGroupBox { padding-top: 20px; margin-top: 10px; }')  # 防止标题和内容重叠
        editor_layout = QVBoxLayout()

        self.code_editor = QTextEdit()
        self.code_editor.setFont(QFont(EDITOR_CONFIG['font_family'], EDITOR_CONFIG['font_size']))
        self.code_editor.setStyleSheet('''
            QTextEdit {
                background-color: #263238;
                color: #AAAAAA;
                border: 1px solid #455A64;
                padding: 10px;
                line-height: 1.5;
            }
        ''')
        self.code_editor.setTabStopWidth(EDITOR_CONFIG['tab_size'] * 8)
        self.code_editor.setPlaceholderText('# 在此编写Python代码\n# 按"运行代码"按钮执行代码\n\nprint("Hello, Python!")')
        editor_layout.addWidget(self.code_editor)

        editor_group.setLayout(editor_layout)
        splitter.addWidget(editor_group)

        # 输出区域
        output_group = QGroupBox('📋 运行结果')
        output_group.setFont(QFont('Microsoft YaHei', 11, QFont.Bold))
        output_group.setStyleSheet('QGroupBox { padding-top: 20px; margin-top: 10px; }')  # 防止标题和内容重叠
        output_layout = QVBoxLayout()

        self.output_text = QTextEdit()
        self.output_text.setFont(QFont(EDITOR_CONFIG['font_family'], 10))
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet('''
            QTextEdit {
                background-color: #1E1E1E;
                color: #D4D4D4;
                border: 1px solid #3C3C3C;
                padding: 10px;
            }
        ''')
        output_layout.addWidget(self.output_text)

        # 清空输出按钮
        clear_output_btn = QPushButton('清空输出')
        clear_output_btn.setFont(QFont('Microsoft YaHei', 9))
        clear_output_btn.clicked.connect(lambda: self.output_text.clear())
        output_layout.addWidget(clear_output_btn)

        output_group.setLayout(output_layout)
        splitter.addWidget(output_group)

        # 设置分隔器比例
        splitter.setSizes([600, 300])

        main_layout.addWidget(splitter)

        # 底部提示信息
        hint_layout = QHBoxLayout()
        hint_label = QLabel('💡 提示: 支持标准Python语法 | 代码执行超时时间: 5秒')
        hint_label.setFont(QFont('Microsoft YaHei', 9))
        hint_label.setStyleSheet('color: #666666;')
        hint_layout.addWidget(hint_label)
        main_layout.addLayout(hint_layout)

        self.setLayout(main_layout)

    def new_file(self):
        """新建文件"""
        if self.code_editor.toPlainText().strip():
            reply = QMessageBox.question(
                self, '确认',
                '当前文件未保存，是否继续？',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.No:
                return

        self.code_editor.clear()
        self.output_text.clear()
        self.current_file = None
        self.file_label.setText('未命名文件')

    def open_file(self):
        """打开文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, '打开Python文件',
            '',
            'Python Files (*.py);;All Files (*.*)'
        )

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                    self.code_editor.setPlainText(code)
                    self.current_file = file_path
                    self.file_label.setText(os.path.basename(file_path))
                    self.output_text.append(f'✓ 已打开文件: {file_path}')
            except Exception as e:
                QMessageBox.critical(self, '错误', f'打开文件失败: {str(e)}')

    def save_file(self):
        """保存文件"""
        if self.current_file:
            file_path = self.current_file
        else:
            file_path, _ = QFileDialog.getSaveFileName(
                self, '保存Python文件',
                '',
                'Python Files (*.py);;All Files (*.*)'
            )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    code = self.code_editor.toPlainText()
                    f.write(code)
                    self.current_file = file_path
                    self.file_label.setText(os.path.basename(file_path))
                    self.output_text.append(f'✓ 已保存文件: {file_path}')
                    QMessageBox.information(self, '成功', '文件保存成功！')
            except Exception as e:
                QMessageBox.critical(self, '错误', f'保存文件失败: {str(e)}')

    def run_code(self):
        """运行代码"""
        code = self.code_editor.toPlainText().strip()

        if not code:
            QMessageBox.warning(self, '提示', '请先输入代码！')
            return

        self.output_text.append('\n' + '='*50)
        self.output_text.append('开始执行代码...')
        self.output_text.append('='*50 + '\n')

        # 验证语法
        is_valid, error = self.code_executor.validate_code(code)
        if not is_valid:
            self.output_text.append(f'❌ 语法错误:\n{error}')
            return

        # 执行代码
        success, output, error = self.code_executor.execute(code)

        if success:
            self.output_text.append('✓ 执行成功:')
            if output:
                self.output_text.append(output)
            else:
                self.output_text.append('(无输出)')
        else:
            self.output_text.append(f'❌ 执行错误:\n{error}')

        self.output_text.append('\n' + '='*50)
        self.output_text.append('执行完成')
        self.output_text.append('='*50 + '\n')

    def clear_editor(self):
        """清空编辑器"""
        reply = QMessageBox.question(
            self, '确认',
            '确定要清空编辑器吗？',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.code_editor.clear()

    def refresh(self):
        """刷新数据"""
        pass  # 编辑器不需要刷新
