# -*- coding: utf-8 -*-
"""
登录成功后的全屏欢迎页（带文字浮动）
"""
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, pyqtSignal, QTimer, QPoint
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGraphicsOpacityEffect


class WelcomeOverlay(QWidget):
    finished = pyqtSignal()

    def __init__(self, username='', parent=None):
        super().__init__(parent)
        self.username = username
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.init_ui()

    def init_ui(self):
        self.resize(QApplication.primaryScreen().size())
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)

        # 背景使用样式表渐变
        self.setStyleSheet('background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 rgba(224,247,255,0.1), stop:1 rgba(243,229,245,0.1));')

        self.label = QLabel(f'欢迎，{self.username}')
        self.label.setFont(QFont('SF Pro Display', 28))
        self.label.setStyleSheet('color: #333333;')
        self.label.setAlignment(Qt.AlignCenter)

        self.opacity = QGraphicsOpacityEffect(self.label)
        self.label.setGraphicsEffect(self.opacity)
        self.opacity.setOpacity(1.0)

        layout.addWidget(self.label)

    def start(self):
        self.showFullScreen()
        # 垂直浮动动画 ±5px，周期2s（实现为上下循环）
        start_geo = self.label.geometry()
        x = start_geo.x()
        y = start_geo.y()
        # 使用两段动画：向上再向下
        self.anim_up = QPropertyAnimation(self.label, b"pos")
        self.anim_up.setDuration(1000)
        self.anim_up.setStartValue(self.label.pos())
        self.anim_up.setEndValue(self.label.pos() - QPoint(0, 5))

        self.anim_down = QPropertyAnimation(self.label, b"pos")
        self.anim_down.setDuration(1000)
        self.anim_down.setStartValue(self.label.pos() - QPoint(0, 5))
        self.anim_down.setEndValue(self.label.pos())

        # 简单循环：上下两段组成 2s 周期
        self.anim_up.finished.connect(self.anim_down.start)
        # 启动 first
        self.anim_up.start()

        # 2s 后淡出并结束
        print('[DEBUG] WelcomeOverlay: start animation')
        QTimer.singleShot(2000, self._do_fade)

    def _do_fade(self):
        fade = QPropertyAnimation(self.opacity, b"opacity")
        fade.setDuration(300)
        fade.setStartValue(1.0)
        fade.setEndValue(0.0)
        fade.finished.connect(self._finish)
        print('[DEBUG] WelcomeOverlay: doing fade')
        fade.start()
        self._fade = fade

    def _finish(self):
        print('[DEBUG] WelcomeOverlay: finished -> emitting signal')
        self.hide()
        self.finished.emit()
