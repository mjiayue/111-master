# -*- coding: utf-8 -*-
"""
启动遮罩与小球动效
"""
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, pyqtSignal, QParallelAnimationGroup, QTimer, pyqtProperty, QEasingCurve
from PyQt5.QtGui import QFont, QPalette, QColor, QPainter, QBrush
from PyQt5.QtWidgets import QGraphicsOpacityEffect


class LaunchOverlay(QWidget):
    finished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.init_ui()

    def init_ui(self):
        self.resize(QApplication.primaryScreen().size())

        # 暗色背景
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor('#222222'))
        self.setPalette(palette)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)

        # 小球（自定义绘制，支持旋转标记以表现自转效果）
        class BallWidget(QWidget):
            def __init__(self, parent=None):
                super().__init__(parent)
                self._angle = 0
                self.setAttribute(Qt.WA_TranslucentBackground)

            def sizeHint(self):
                return self.size()

            def paintEvent(self, event):
                r = min(self.width(), self.height())
                painter = QPainter(self)
                painter.setRenderHint(QPainter.Antialiasing)
                # 画圆
                brush = QBrush(QColor(224, 247, 255, int(0.8 * 255)))
                painter.setBrush(brush)
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(0, 0, int(r), int(r))
                # 画一个小标记以表现旋转（像指针）
                painter.save()
                painter.translate(int(r/2), int(r/2))
                painter.rotate(self._angle)
                painter.setBrush(QBrush(QColor(180, 220, 255, 220)))
                painter.drawRect(int(r/2) - 3, -2, int(r/2), 4)
                painter.restore()

            def getAngle(self):
                return self._angle

            def setAngle(self, v):
                self._angle = v
                self.update()

            angle = pyqtProperty(float, fget=getAngle, fset=setAngle)

        self.ball = BallWidget(self)
        self.ball.setFixedSize(20, 20)
        self.ball_effect = QGraphicsOpacityEffect(self.ball)
        self.ball.setGraphicsEffect(self.ball_effect)
        self.ball_effect.setOpacity(1.0)

        # 文本
        self.text = QLabel('Welcome to Learn Python', self)
        self.text.setStyleSheet('color: rgba(255,255,255,0.0);')
        self.text.setFont(QFont('SF Pro Display', 20))
        self.text.setAlignment(Qt.AlignCenter)
        self.text_effect = QGraphicsOpacityEffect(self.text)
        self.text.setGraphicsEffect(self.text_effect)
        self.text_effect.setOpacity(0.0)

        layout.addWidget(self.ball, alignment=Qt.AlignCenter)
        layout.addSpacing(12)
        layout.addWidget(self.text, alignment=Qt.AlignCenter)

    def start(self):
        # 放大动画（1.5s）
        screen = QApplication.primaryScreen().size()
        center_x = screen.width() // 2
        center_y = screen.height() // 2

        start_rect = QRect(center_x - 10, center_y - 10, 20, 20)
        end_rect = QRect(center_x - 100, center_y - 100, 200, 200)

        self.ball_anim = QPropertyAnimation(self.ball, b"geometry")
        self.ball_anim.setDuration(1500)
        self.ball_anim.setStartValue(start_rect)
        self.ball_anim.setEndValue(end_rect)
        self.ball_anim.setEasingCurve(QEasingCurve.InOutCubic)

        # 自转动画（持续）
        self.rotate_anim = QPropertyAnimation(self.ball, b"angle")
        self.rotate_anim.setDuration(500)  # 0.5s per full rotation
        self.rotate_anim.setStartValue(0)
        self.rotate_anim.setEndValue(360)
        self.rotate_anim.setLoopCount(-1)

        # 文本淡入
        self.text_anim = QPropertyAnimation(self.text_effect, b"opacity")
        self.text_anim.setDuration(1500)
        self.text_anim.setStartValue(0.0)
        self.text_anim.setEndValue(1.0)

        group = QParallelAnimationGroup(self)
        group.addAnimation(self.ball_anim)
        group.addAnimation(self.text_anim)

        group.finished.connect(self._on_expand_finished)
        self.showFullScreen()
        # 启动自转
        self.rotate_anim.start()
        group.start()
        # keep reference
        self._group = group
        self._rotate = self.rotate_anim

    def _on_expand_finished(self):
        # 消散淡出（0.8s）
        fade_anim = QPropertyAnimation(self.ball_effect, b"opacity")
        fade_anim.setDuration(800)
        fade_anim.setStartValue(1.0)
        fade_anim.setEndValue(0.0)

        text_fade = QPropertyAnimation(self.text_effect, b"opacity")
        text_fade.setDuration(800)
        text_fade.setStartValue(1.0)
        text_fade.setEndValue(0.0)

        group2 = QParallelAnimationGroup(self)
        group2.addAnimation(fade_anim)
        group2.addAnimation(text_fade)
        group2.finished.connect(self._on_fade_finished)
        group2.start()
        self._group2 = group2

    def _on_fade_finished(self):
        # 等一小会然后关闭遮罩
        QTimer.singleShot(120, self._finish)

    def _finish(self):
        self.hide()
        self.finished.emit()
