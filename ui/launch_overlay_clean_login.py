# -*- coding: utf-8 -*-
"""
PyPalPrep登录页：清透灵动+iOS极简高级风格
核心视觉：清透双层丝带文字+细闪颗粒微浮动
"""
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QLineEdit, QLabel
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, pyqtSignal, QTimer, pyqtProperty, QEasingCurve, QPoint
from PyQt5.QtGui import QFont, QPalette, QColor, QPainter, QBrush, QPainterPath, QPen, QFontMetrics
import math
import random


class TransparentTextWidget(QWidget):
    """清透双层丝带文字部件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.text = "PyPalPrep"
        
        # 字体配置：圆角饱满款，字高占屏幕垂直中间40%
        screen_height = QApplication.primaryScreen().size().height()
        font_size = int(screen_height * 0.4 / 1.5)  # 根据行高调整
        self.font = QFont("SF Pro Rounded", font_size)
        self.font.setBold(True)
        self.font.setWeight(QFont.ExtraBold)  # 笔画加粗10%
        self.font.setLetterSpacing(QFont.AbsoluteSpacing, 3)  # 字间距+3px
        
        # 颜色：清透银蓝系
        self.stroke_color = QColor('#D4E0EB')  # 内层勾边：清透银灰
        self.fill_color = QColor('#E8F1F8')    # 外层填充：清透浅蓝
        
        # 细闪颗粒微浮动参数
        self.sparkle_offset = 0.0
        self.sparkle_timer = QTimer()
        self.sparkle_timer.timeout.connect(self._update_sparkles)
        self.sparkle_timer.start(50)  # 50ms刷新
    
    def _update_sparkles(self):
        """更新细闪颗粒位置（±0.5px微浮动）"""
        self.sparkle_offset += 0.1
        if self.sparkle_offset > math.pi * 2:
            self.sparkle_offset = 0
        self.update()
    
    def paintEvent(self, event):
        """绘制清透双层丝带文字"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        
        # 文字居中，向右倾斜5°
        painter.save()
        
        # 计算文字尺寸
        metrics = QFontMetrics(self.font)
        text_width = metrics.width(self.text)
        text_height = metrics.height()
        
        # 居中位置
        center_x = self.width() / 2.0
        center_y = self.height() / 2.0
        
        # 移动到中心，倾斜5°
        painter.translate(center_x, center_y)
        painter.rotate(5)  # 向右倾斜5°
        
        # 创建文字路径
        path = QPainterPath()
        path.addText(-text_width / 2.0, text_height / 3.0, self.font, self.text)
        
        # 第1层：外层填充（清透浅蓝，60%透明度）
        fill_color_with_alpha = QColor(self.fill_color)
        fill_color_with_alpha.setAlpha(int(255 * 0.6))
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(fill_color_with_alpha))
        painter.drawPath(path)
        
        # 第2层：内层勾边（清透银灰，70%透明度，1px柔化）
        stroke_color_with_alpha = QColor(self.stroke_color)
        stroke_color_with_alpha.setAlpha(int(255 * 0.7))
        pen = QPen(stroke_color_with_alpha)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)
        
        # 第3层：细闪颗粒（0.5px，±0.5px微浮动）
        self._draw_sparkles(painter, path)
        
        painter.restore()
    
    def _draw_sparkles(self, painter, text_path):
        """绘制细闪颗粒（±0.5px微浮动）"""
        # 固定随机种子以保证一致性
        random.seed(42)
        
        # 沿着文字路径分布颗粒
        path_length = text_path.length()
        num_sparkles = int(path_length / 50)  # 每50px一个颗粒
        
        for i in range(num_sparkles):
            t = i / num_sparkles
            point = text_path.pointAtPercent(t)
            
            # 微浮动：±0.5px
            offset_x = math.sin(self.sparkle_offset + i * 0.5) * 0.5
            offset_y = math.cos(self.sparkle_offset + i * 0.7) * 0.5
            
            sparkle_x = point.x() + offset_x
            sparkle_y = point.y() + offset_y
            
            # 绘制0.5px的半透明白色闪点
            from PyQt5.QtCore import QRectF
            painter.setBrush(QColor(255, 255, 255, 150))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QRectF(sparkle_x - 0.25, sparkle_y - 0.25, 0.5, 0.5))
    
    def stop_animation(self):
        """停止细闪动画"""
        self.sparkle_timer.stop()


class LoginForm(QWidget):
    """清透iOS极简登录表单"""
    login_clicked = pyqtSignal(str, str)  # 用户名，密码
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        # 获取屏幕尺寸而不是父窗口尺寸
        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        parent_width = screen_size.width()
        parent_height = screen_size.height()
        
        # 用户名标签
        username_label = QLabel("用户名", self)
        username_label.setFont(QFont("SF Pro Display", 18))
        username_label.setStyleSheet("color: #666666;")
        username_label.setGeometry(parent_width // 2 - 250, parent_height // 2 + 60, 500, 50)
        
        # 用户名输入框
        self.username_input = QLineEdit(self)
        self.username_input.setFont(QFont("SF Pro Display", 16))
        self.username_input.setGeometry(parent_width // 2 - 250, parent_height // 2 + 120, 500, 80)
        self.username_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 10px 16px;
                background-color: #F8F8F8;
                color: #333333;
            }
            QLineEdit:focus {
                border: 2px solid #999999;
                background-color: #FFFFFF;
            }
        """)
        self.username_input.setPlaceholderText("请输入用户名")
        
        # 密码标签
        password_label = QLabel("密码", self)
        password_label.setFont(QFont("SF Pro Display", 18))
        password_label.setStyleSheet("color: #666666;")
        password_label.setGeometry(parent_width // 2 - 250, parent_height // 2 + 210, 500, 50)
        
        # 密码输入框
        self.password_input = QLineEdit(self)
        self.password_input.setFont(QFont("SF Pro Display", 16))
        self.password_input.setGeometry(parent_width // 2 - 250, parent_height // 2 + 280, 500, 80)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 10px 16px;
                background-color: #F8F8F8;
                color: #333333;
            }
            QLineEdit:focus {
                border: 2px solid #999999;
                background-color: #FFFFFF;
            }
        """)
        self.password_input.setPlaceholderText("请输入密码")
        
        # 登录按钮
        login_btn = QPushButton("登录", self)
        login_btn.setFont(QFont("SF Pro Display", 16, QFont.Bold))
        login_btn.setGeometry(parent_width // 2 - 250, parent_height // 2 + 390, 500, 80)
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #999999;
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 16px;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #777777;
            }
            QPushButton:pressed {
                background-color: #555555;
            }
        """)
        login_btn.clicked.connect(self._on_login)
        
        # 保存引用
        self.username_label = username_label
        self.password_label = password_label
        self.login_btn = login_btn
    
    def _on_login(self):
        """处理登录"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            return
        
        self.login_clicked.emit(username, password)
    
    def show_form(self):
        """显示登录表单"""
        self.username_input.show()
        self.password_input.show()
        self.username_label.show()
        self.password_label.show()
        self.login_btn.show()
        self.username_input.setFocus()


class LaunchOverlay(QWidget):
    """PyPalPrep登录页：清透灵动+iOS极简高级风格"""
    finished = pyqtSignal(str, str)  # 登录完成，传递用户名和密码
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        screen = QApplication.primaryScreen()
        self.resize(screen.size())
        
        # 全白背景
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor('#FFFFFF'))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        
        # 大的灰色 PyPalPrep 标题
        title_label = QLabel('PyPalPrep', self)
        title_font = QFont('SF Pro Display', 100)
        title_font.setBold(True)
        title_font.setWeight(QFont.ExtraBold)
        title_label.setFont(title_font)
        title_label.setStyleSheet('color: #CCCCCC;')  # 浅灰色
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setGeometry(0, self.height() // 2 - 280, self.width(), 250)
        
        # 登录表单
        self.login_form = LoginForm(self)
        self.login_form.login_clicked.connect(self._on_login)
    
    def _on_login(self, username, password):
        """处理登录"""
        self.finished.emit(username, password)
        self.close()
