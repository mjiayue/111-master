# -*- coding: utf-8 -*-
"""
启动动画：圆形水珠 → 字体 → 彩虹渐变 → 欢迎页
iOS 极简风格，高饱和彩虹色
"""
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QApplication
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, pyqtSignal, QTimer, pyqtProperty, QEasingCurve, QPoint
from PyQt5.QtGui import QFont, QPalette, QColor, QPainter, QBrush, QRadialGradient, QPainterPath
from PyQt5.QtWidgets import QGraphicsOpacityEffect
import math


class LaunchOverlay(QWidget):
    finished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.init_ui()

    def init_ui(self):
        self.resize(QApplication.primaryScreen().size())

        # 浅灰背景
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor('#F8F9FA'))
        self.setPalette(palette)

        # 水珠部件
        self.water_drop = WaterDropWidget(self)
        cx = self.width() // 2
        cy = self.height() // 2
        self.water_drop.move(cx - 50, cy - 50)

        # 启动动画
        QTimer.singleShot(100, self._start_animation)

    def _start_animation(self):
        """主动画序列"""
        # 0-4秒：放大并变成字
        expand_anim = QPropertyAnimation(self.water_drop, b"geometry")
        expand_anim.setDuration(4000)
        cx = self.width() // 2
        cy = self.height() // 2
        expand_anim.setStartValue(QRect(cx - 50, cy - 50, 100, 100))
        expand_anim.setEndValue(QRect(cx - 200, cy - 100, 400, 200))
        expand_anim.setEasingCurve(QEasingCurve.InOutCubic)
        
        morph_anim = QPropertyAnimation(self.water_drop, b"textProgress")
        morph_anim.setDuration(4000)
        morph_anim.setStartValue(0.0)
        morph_anim.setEndValue(1.0)
        morph_anim.setEasingCurve(QEasingCurve.InOutCubic)
        
        group = self._create_group([expand_anim, morph_anim])
        group.start()
        
        # 4秒后：彩虹渐变
        QTimer.singleShot(4000, self._start_rainbow)
        
        # 6秒后：显示欢迎页
        QTimer.singleShot(6000, self._show_welcome)

    def _create_group(self, animations):
        """创建并行动画组"""
        from PyQt5.QtCore import QParallelAnimationGroup
        group = QParallelAnimationGroup(self)
        for anim in animations:
            group.addAnimation(anim)
        return group

    def _start_rainbow(self):
        """彩虹渐变"""
        rainbow_anim = QPropertyAnimation(self.water_drop, b"rainbowProgress")
        rainbow_anim.setDuration(2000)
        rainbow_anim.setStartValue(0.0)
        rainbow_anim.setEndValue(1.0)
        rainbow_anim.setEasingCurve(QEasingCurve.Linear)
        rainbow_anim.start()

    def _show_welcome(self):
        """显示欢迎页"""
        self.water_drop.hide()
        
        # 标题
        title = QLabel("PyPalPrep", self)
        title.setFont(QFont('SF Pro Rounded', 72, QFont.Bold))
        title.setStyleSheet('color: white;')
        title.setAlignment(Qt.AlignCenter)
        title.move(self.width()//2 - 180, self.height()//2 - 100)
        title.adjustSize()
        title.show()
        
        # 副标题
        subtitle = QLabel("Welcome to Python Learning", self)
        subtitle.setFont(QFont('SF Pro Rounded', 16))
        subtitle.setStyleSheet('color: rgba(255, 255, 255, 0.8);')
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.move(self.width()//2 - 200, self.height()//2 + 20)
        subtitle.adjustSize()
        subtitle.show()
        
        # Sign In 按钮
        btn_signin = QPushButton("Sign In", self)
        btn_signin.setFont(QFont('SF Pro Rounded', 14, QFont.Medium))
        btn_signin.setGeometry(self.width()//2 - 160, self.height()//2 + 100, 130, 45)
        btn_signin.setStyleSheet('''
            QPushButton {
                background-color: white;
                color: #1976D2;
                border: none;
                border-radius: 22px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F0F0F0;
            }
        ''')
        btn_signin.show()
        
        # Sign Up 按钮
        btn_signup = QPushButton("Sign Up", self)
        btn_signup.setFont(QFont('SF Pro Rounded', 14, QFont.Medium))
        btn_signup.setGeometry(self.width()//2 + 30, self.height()//2 + 100, 130, 45)
        btn_signup.setStyleSheet('''
            QPushButton {
                background-color: transparent;
                color: white;
                border: 2px solid white;
                border-radius: 22px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        ''')
        btn_signup.show()
        
        # 标题浮动
        title_bob = QPropertyAnimation(title, b"pos")
        title_bob.setDuration(2000)
        title_bob.setStartValue(title.pos() + QPoint(0, -8))
        title_bob.setEndValue(title.pos() + QPoint(0, 8))
        title_bob.setLoopCount(-1)
        title_bob.setEasingCurve(QEasingCurve.InOutSine)
        title_bob.start()


class WaterDropWidget(QWidget):
    """水珠部件：圆球 → 字体 → 彩虹渐变"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._text_progress = 0.0  # 球 → 字
        self._rainbow_progress = 0.0  # 水珠蓝 → 彩虹
        self.setAttribute(Qt.WA_TranslucentBackground)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        
        w, h = self.width(), self.height()
        
        # 色彩：混合水珠蓝与彩虹色
        if self._rainbow_progress > 0:
            # 高饱和 iOS 彩虹色
            rainbow = [
                QColor(255, 59, 48),      # 红
                QColor(255, 149, 0),      # 橙
                QColor(255, 204, 0),      # 黄
                QColor(52, 211, 153),     # 绿
                QColor(59, 130, 246),     # 蓝
                QColor(168, 85, 247),     # 紫
            ]
            idx = int(self._rainbow_progress * (len(rainbow) - 1))
            if idx < len(rainbow) - 1:
                c1 = rainbow[idx]
                c2 = rainbow[idx + 1]
                t = self._rainbow_progress * (len(rainbow) - 1) - idx
                color = QColor(
                    int(c1.red() * (1-t) + c2.red() * t),
                    int(c1.green() * (1-t) + c2.green() * t),
                    int(c1.blue() * (1-t) + c2.blue() * t)
                )
            else:
                color = rainbow[-1]
        else:
            # 清透水珠蓝
            color = QColor('#B3E5FC')
        
        color.setAlpha(int(0.9 * 255))
        
        # 根据进度绘制圆球或字体
        if self._text_progress < 0.8:
            # 主要是圆球
            self._draw_circle(painter, w, h, color)
        else:
            # 主要是字体
            self._draw_text(painter, w, h, color)

    def _draw_circle(self, painter, w, h, color):
        """绘制圆形水珠"""
        # 径向渐变（高光效果）
        gradient = QRadialGradient(w * 0.3, h * 0.3, max(w, h) / 2)
        gradient.setColorAt(0.0, QColor(255, 255, 255, int(0.5 * 255)))
        gradient.setColorAt(0.5, color)
        gradient.setColorAt(1.0, color)
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, w, h)

    def _draw_text(self, painter, w, h, color):
        """绘制字体"""
        font = QFont('SF Pro Rounded', int(min(w, h) * 0.45), QFont.Bold)
        path = QPainterPath()
        path.addText(0, 0, font, "PyPalPrep")
        
        # 居中
        rect = path.boundingRect()
        path.translate((w - rect.width()) / 2, (h - rect.height()) / 2 + 10)
        
        # 渐变填充
        gradient = QRadialGradient(w * 0.4, h * 0.2, max(w, h) / 2)
        gradient.setColorAt(0.0, QColor(255, 255, 255, int(0.3 * 255)))
        gradient.setColorAt(0.5, color)
        gradient.setColorAt(1.0, color)
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawPath(path)

    def getTextProgress(self):
        return self._text_progress

    def setTextProgress(self, v):
        self._text_progress = v
        self.update()

    textProgress = pyqtProperty(float, fget=getTextProgress, fset=setTextProgress)

    def getRainbowProgress(self):
        return self._rainbow_progress

    def setRainbowProgress(self, v):
        self._rainbow_progress = v
        self.update()

    rainbowProgress = pyqtProperty(float, fget=getRainbowProgress, fset=setRainbowProgress)
