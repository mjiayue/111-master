# -*- coding: utf-8 -*-
"""
登录窗口
提供用户登录界面
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QPropertyAnimation, QParallelAnimationGroup, QEasingCurve
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from database.db_manager import db_manager
from models.user import User
from config import WINDOW_CONFIG, THEME_COLORS, DEFAULT_USER


class LoginWindow(QWidget):
    """登录窗口类"""

    # 登录成功信号
    login_success = pyqtSignal(object)  # 传递User对象

    def __init__(self):
        """初始化登录窗口"""
        super().__init__()
        self._first_show = True
        self.current_user = None
        self.init_ui()

    def showEvent(self, event):
        """首次显示时播放淡入+上移过渡动画"""
        super().showEvent(event)
        if getattr(self, '_first_show', False):
            self._first_show = False
            orig = self.pos()
            start = QPoint(orig.x(), orig.y() + 8)
            # 初始位置与透明度
            self.move(start)
            self.setWindowOpacity(0.0)

            anim_op = QPropertyAnimation(self, b'windowOpacity')
            anim_op.setDuration(280)
            anim_op.setStartValue(0.0)
            anim_op.setEndValue(1.0)
            anim_op.setEasingCurve(QEasingCurve.OutCubic)

            anim_pos = QPropertyAnimation(self, b'pos')
            anim_pos.setDuration(280)
            anim_pos.setStartValue(start)
            anim_pos.setEndValue(orig)
            anim_pos.setEasingCurve(QEasingCurve.OutCubic)

            group = QParallelAnimationGroup(self)
            group.addAnimation(anim_op)
            group.addAnimation(anim_pos)
            group.start()
            self._show_anim = group
            # 保证窗口激活
            try:
                self.raise_()
                self.activateWindow()
            except Exception:
                pass

    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle('PyPalPrep - 登录')
        self.setFixedSize(760, 820)  # 增加窗口宽度和高度以完整显示文字
        self.center_window()

        # 设置背景色
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor('#F6F7F9'))  # 浅灰色背景
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 40, 40, 40)  # 减小边距

        # 标题
        title_label = QLabel('Welcome to PyPalPrep 🎉')
        title_font = QFont('Microsoft YaHei', 28, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet('color: #222222; padding: 10px;')
        main_layout.addWidget(title_label)

        # 副标题
        subtitle_label = QLabel('AI-powered Python Learning Assistant')
        subtitle_font = QFont('Microsoft YaHei', 14)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet('color: #999999; margin-bottom: 25px; padding: 5px;')
        main_layout.addWidget(subtitle_label)

        # 登录表单容器 - 简化版
        form_frame = QFrame()
        form_frame.setStyleSheet(f'''
            QFrame {{
                background-color: white;
                border-radius: 10px;
                padding: 30px 40px;
            }}
        ''')
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(20)

        # 用户名输入框（无标签，直接用placeholder）
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('用户名')
        self.username_input.setFont(QFont('Microsoft YaHei', 15))
        self.username_input.setFixedHeight(56)
        self.username_input.setStyleSheet(f'''
            QLineEdit {{
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 12px 18px;
                background-color: white;
                color: {THEME_COLORS["dark"]};
            }}
            QLineEdit:focus {{
                border: 2px solid {THEME_COLORS["primary"]};
            }}
        ''')
        self.username_input.setText('1')
        form_layout.addWidget(self.username_input)

        # 密码输入框（无标签，直接用placeholder）
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('密码')
        self.password_input.setFont(QFont('Microsoft YaHei', 15))
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(56)
        self.password_input.setStyleSheet(f'''
            QLineEdit {{
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 12px 18px;
                background-color: white;
                color: {THEME_COLORS["dark"]};
            }}
            QLineEdit:focus {{
                border: 2px solid {THEME_COLORS["primary"]};
            }}
        ''')
        self.password_input.setText('1')
        self.password_input.returnPressed.connect(self.handle_login)
        form_layout.addWidget(self.password_input)

        # 登录按钮
        self.login_button = QPushButton('登录')
        self.login_button.setFont(QFont('Microsoft YaHei', 26, QFont.Bold))
        self.login_button.setMinimumHeight(56)
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.setStyleSheet(f'''
            QPushButton {{
                background-color: {THEME_COLORS["primary"]};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 12px;
            }}
            QPushButton:hover {{
                background-color: #1976D2;
            }}
            QPushButton:pressed {{
                background-color: #0D47A1;
            }}
        ''')
        self.login_button.clicked.connect(self.handle_login)
        form_layout.addWidget(self.login_button)

        main_layout.addWidget(form_frame)

        # 提示信息
        hint_label = QLabel('默认账号：1    密码：1')
        hint_label.setFont(QFont('Microsoft YaHei', 12))
        hint_label.setAlignment(Qt.AlignCenter)
        hint_label.setStyleSheet(f'color: {THEME_COLORS["info"]}; margin-top: 20px; padding: 10px;')
        main_layout.addWidget(hint_label)

        # 版权信息
        copyright_label = QLabel('© 2025 PyPalPrep. All rights reserved.')
        copyright_label.setFont(QFont('Microsoft YaHei', 11))
        copyright_label.setAlignment(Qt.AlignCenter)
        copyright_label.setStyleSheet('color: #999999; margin-top: 10px;')
        main_layout.addWidget(copyright_label)

        main_layout.addStretch()

        self.setLayout(main_layout)

    def center_window(self):
        """窗口居中显示"""
        from PyQt5.QtWidgets import QDesktopWidget
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(
            int((screen.width() - size.width()) / 2),
            int((screen.height() - size.height()) / 2)
        )

    def handle_login(self):
        """处理登录"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        # 验证输入
        if not username:
            QMessageBox.warning(self, '警告', '请输入用户名！')
            self.username_input.setFocus()
            return

        if not password:
            QMessageBox.warning(self, '警告', '请输入密码！')
            self.password_input.setFocus()
            return

        # 验证用户
        db_manager.connect()
        user_data = db_manager.verify_user(username, password)
        db_manager.disconnect()

        # 开发便捷登录兜底：若数据库异常或默认用户未初始化，允许使用配置中的默认账号直接登录
        if not user_data and username == DEFAULT_USER['username'] and password == DEFAULT_USER['password']:
            user_data = {
                'id': 1,
                'username': DEFAULT_USER['username'],
                'password': 'md5',
                'nickname': DEFAULT_USER['nickname']
            }

        if user_data:
            self.current_user = User.from_dict(user_data)
            QMessageBox.information(self, '成功', f'欢迎您，{self.current_user.nickname}！')
            self.login_success.emit(self.current_user)
            self.close()
        else:
            QMessageBox.critical(self, '错误', '用户名或密码错误！')
            self.password_input.clear()
            self.password_input.setFocus()
