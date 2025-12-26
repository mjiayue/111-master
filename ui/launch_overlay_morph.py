# -*- coding: utf-8 -*-
"""
启动遮罩与登录页动效（旋转成球 + 悬浮交互）
"""
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QApplication, QFrame
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, pyqtSignal, QParallelAnimationGroup, QTimer, pyqtProperty, QEasingCurve, QPointF, QSequentialAnimationGroup, QPoint
from PyQt5.QtGui import QFont, QPalette, QColor, QPainter, QBrush, QPen, QRadialGradient, QPainterPath, QPainterPath
from PyQt5.QtWidgets import QGraphicsOpacityEffect, QGraphicsDropShadowEffect
import random
import math


class LaunchOverlay(QWidget):
    finished = pyqtSignal()

    # 彩虹色阶（用于渐变与背景）
    RAINBOW_COLORS = [
        QColor(255, 0, 0),       # 红
        QColor(255, 127, 0),     # 橙
        QColor(255, 255, 0),     # 黄
        QColor(0, 255, 0),       # 绿
        QColor(0, 0, 255),       # 蓝
        QColor(128, 0, 128),     # 紫
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._rainbow_progress = 0.0
        self._draw_rainbow_bg = False
        self.init_ui()

    def init_ui(self):
        self.resize(QApplication.primaryScreen().size())

        # 极简浅灰背景
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor('#F8F9FA'))
        self.setPalette(palette)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignCenter)

        # 是否绘制水滴连接（迷你球与主球之间）
        self._draw_connections = False

        # 主球（初始为不规则模糊色块）
        self.main_ball = BallWidget(self)
        self.main_ball.setFixedSize(30, 30)
        self.main_ball.move(self.width()//2 - 15, self.height()//2 - 15)
        self.main_ball.setVisible(False)

        # 迷你小球列表
        # 15-20颗迷你球，尺寸20-30px
        self.mini_balls = []
        count = random.randint(15, 20)
        for i in range(count):
            mini = MiniBallWidget(self)
            size = random.randint(20, 30)
            mini.setFixedSize(size, size)
            mini.setVisible(False)
            self.mini_balls.append(mini)

        # 软件名字标签（初始隐藏）
        self.name_label = QLabel("PyPal Prep", self)
        self.name_label.setFont(QFont('Microsoft YaHei', 24, QFont.Light))
        self.name_label.setStyleSheet('color: rgba(255,255,255,0.0);')
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.move(self.width()//2 - 100, self.height()//2 - 20)
        self.name_label.setVisible(False)

        # 登录表单（初始隐藏）
        self.login_frame = QFrame(self)
        self.login_frame.setVisible(False)
        self.login_frame.setStyleSheet('''
            QFrame {
                background-color: transparent;
            }
        ''')
        form_layout = QVBoxLayout(self.login_frame)
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(0, 0, 0, 0)

        # 标题
        title = QLabel('登录 / PyPal Prep')
        title.setFont(QFont('SF Pro Display', 18, QFont.Light))
        title.setStyleSheet('color: #333333;')
        form_layout.addWidget(title)

        # 账号输入框
        self.account_input = QLineEdit()
        self.account_input.setPlaceholderText('账号')
        self.account_input.setFont(QFont('SF Pro Display', 14))
        self.account_input.setFixedHeight(40)
        self.account_input.setStyleSheet('''
            QLineEdit {
                border: none;
                border-bottom: 1px solid #E0E0E0;
                background-color: transparent;
                color: #333333;
            }
            QLineEdit:focus {
                border-bottom: 2px solid #E0F7FF;
            }
        ''')
        form_layout.addWidget(self.account_input)

        # 密码输入框
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('密码')
        self.password_input.setFont(QFont('SF Pro Display', 14))
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(40)
        self.password_input.setStyleSheet('''
            QLineEdit {
                border: none;
                border-bottom: 1px solid #E0E0E0;
                background-color: transparent;
                color: #333333;
            }
            QLineEdit:focus {
                border-bottom: 2px solid #E0F7FF;
            }
        ''')
        form_layout.addWidget(self.password_input)

        # 按钮布局
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.login_btn = QPushButton('登录')
        self.login_btn.setFont(QFont('SF Pro Display', 14))
        self.login_btn.setFixedSize(100, 40)
        self.login_btn.setStyleSheet('''
            QPushButton {
                background-color: #E0F7FF;
                color: #333333;
                border-radius: 3px;
                border: none;
            }
            QPushButton:hover {
                background-color: #B3E5FC;
            }
            QPushButton:pressed {
                background-color: #A8D8F0;
            }
        ''')
        # 添加阴影效果
        shadow = QGraphicsDropShadowEffect(self.login_btn)
        shadow.setBlurRadius(5)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 2)
        self.login_btn.setGraphicsEffect(shadow)
        btn_layout.addWidget(self.login_btn)

        self.register_btn = QPushButton('注册')
        self.register_btn.setFont(QFont('SF Pro Display', 14))
        self.register_btn.setStyleSheet('''
            QPushButton {
                background-color: transparent;
                color: #9E9E9E;
                border: none;
            }
            QPushButton:hover {
                color: #333333;
            }
        ''')
        btn_layout.addWidget(self.register_btn)

        form_layout.addLayout(btn_layout)

        # 连接信号（暂时）
        self.login_btn.clicked.connect(self._on_login_clicked)
        self.register_btn.clicked.connect(self._on_register_clicked)

    def start(self):
        self.showFullScreen()
        self._start_blob_to_ball()

    def _start_blob_to_ball(self):
        # 显示不规则色块
        self.main_ball.setVisible(True)
        self.main_ball.setIrregular(True)
        self.main_ball.update()

        # 自转动画（0.8s/圈）
        self.rotate_anim = QPropertyAnimation(self.main_ball, b"angle")
        self.rotate_anim.setDuration(800)
        self.rotate_anim.setStartValue(0)
        self.rotate_anim.setEndValue(360)
        self.rotate_anim.setLoopCount(-1)
        self.rotate_anim.start()

        # 1.2s过渡为正球形
        self.shape_anim = QPropertyAnimation(self.main_ball, b"irregularFactor")
        self.shape_anim.setDuration(1200)
        self.shape_anim.setStartValue(1.0)
        self.shape_anim.setEndValue(0.0)
        self.shape_anim.setEasingCurve(QEasingCurve.OutCubic)
        self.shape_anim.finished.connect(self._on_ball_formed)
        self.shape_anim.start()

    def _on_ball_formed(self):
        # 生成迷你小球
        center = QPointF(self.width()//2, self.height()//2)
        for mini in self.mini_balls:
            mini.setVisible(True)
            # 随机位置在半径50-100px范围内
            angle = random.uniform(0, 2*math.pi)
            dist = random.uniform(50, 100)
            x = center.x() + dist * math.cos(angle)
            y = center.y() + dist * math.sin(angle)
            mini.move(int(x - 4), int(y - 4))
            # 公转动画
            orbit_anim = QPropertyAnimation(mini, b"orbitAngle")
            orbit_anim.setDuration(random.randint(600, 1000))
            orbit_anim.setStartValue(angle)
            orbit_anim.setEndValue(angle + 2*math.pi)
            orbit_anim.setLoopCount(-1)
            orbit_anim.start()
            mini._orbit_anim = orbit_anim
            # 自转
            spin_anim = QPropertyAnimation(mini, b"angle")
            spin_anim.setDuration(500)
            spin_anim.setStartValue(0)
            spin_anim.setEndValue(360)
            spin_anim.setLoopCount(-1)
            spin_anim.start()
            mini._spin_anim = spin_anim

        # 开启水滴连接绘制
        self._draw_connections = True
        # 0.6s后放大主球
        QTimer.singleShot(600, self._expand_main_ball)

    def _expand_main_ball(self):
        # 显示名字标签
        self.name_label.setVisible(True)
        name_opacity = QPropertyAnimation(self.name_label, b"windowOpacity")
        name_opacity.setDuration(700)
        name_opacity.setStartValue(0.0)
        name_opacity.setEndValue(1.0)

        # 主球放大至300px，透明度50%，保持中心不变
        expand_anim = QPropertyAnimation(self.main_ball, b"geometry")
        expand_anim.setDuration(900)
        cx = self.width()//2
        cy = self.height()//2
        start_size = 30
        end_size = 300
        expand_anim.setStartValue(QRect(cx - start_size//2, cy - start_size//2, start_size, start_size))
        expand_anim.setEndValue(QRect(cx - end_size//2, cy - end_size//2, end_size, end_size))
        expand_anim.setEasingCurve(QEasingCurve.OutCubic)

        opacity_anim = QPropertyAnimation(self.main_ball, b"opacity")
        opacity_anim.setDuration(900)
        opacity_anim.setStartValue(1.0)
        opacity_anim.setEndValue(0.5)

        group = QParallelAnimationGroup(self)
        group.addAnimation(expand_anim)
        group.addAnimation(opacity_anim)
        group.addAnimation(name_opacity)
        # 动画完成后先让迷你小球汇聚成文字，再扩展为欢迎页
        group.finished.connect(self._gather_to_text)
        group.start()
        self._expand_group = group

    def _gather_to_text(self):
        # 停止迷你球的公转/自转动画
        for mini in getattr(self, 'mini_balls', []):
            if hasattr(mini, '_orbit_anim'):
                try:
                    mini._orbit_anim.stop()
                except Exception:
                    pass
            if hasattr(mini, '_spin_anim'):
                try:
                    mini._spin_anim.stop()
                except Exception:
                    pass
        # 使用字体轮廓采样生成更精准的点阵
        text = "PyPalPrep"
        # 构造路径：使用当前屏幕中心位置居中
        font = QFont('Microsoft YaHei', 64, QFont.Bold)
        path = QPainterPath()
        # 暂先在(0,0)绘制，再居中平移
        path.addText(0, 0, font, text)
        # 获取边界并居中到屏幕中心
        rect = path.boundingRect()
        center = QPointF(self.width()/2, self.height()/2)
        dx = center.x() - rect.center().x()
        dy = center.y() - rect.center().y()
        path.translate(dx, dy)

        # 采样路径元素，稀疏取点以匹配迷你球数量
        total = path.elementCount()
        step = max(1, total // max(1, len(self.mini_balls)))
        sampled = []
        for i in range(0, total, step):
            elem = path.elementAt(i)
            sampled.append((elem.x, elem.y))
        if not sampled:
            # 回退到简易居中点阵
            cx, cy = center.x(), center.y()
            sampled = [(cx-80, cy), (cx-40, cy), (cx, cy), (cx+40, cy), (cx+80, cy)]

        # 如果数量不足，循环填充；过多则截断
        targets = []
        for i in range(len(self.mini_balls)):
            pt = sampled[i % len(sampled)]
            targets.append((int(pt[0]), int(pt[1])))

        group = QParallelAnimationGroup(self)
        for idx, mini in enumerate(self.mini_balls):
            tx, ty = targets[idx]
            anim = QPropertyAnimation(mini, b"pos")
            anim.setDuration(800 + idx * 60)
            anim.setStartValue(mini.pos())
            anim.setEndValue(QPoint(int(tx - mini.width()/2), int(ty - mini.height()/2)))
            anim.setEasingCurve(QEasingCurve.OutCubic)
            group.addAnimation(anim)
        group.finished.connect(self._show_name_then_expand)
        group.start()
        self._gather_group = group

        # 文本发光效果：让 name_label 增加发光与轻微上下浮动
        self.name_label.setVisible(True)
        glow = QGraphicsDropShadowEffect(self.name_label)
        glow.setBlurRadius(20)
        glow.setColor(QColor(255, 255, 255, 120))
        glow.setOffset(0, 0)
        self.name_label.setGraphicsEffect(glow)

        # 上下浮动动画
        base_pos = self.name_label.pos()
        bob = QPropertyAnimation(self.name_label, b"pos")
        bob.setDuration(1800)
        bob.setStartValue(base_pos + QPoint(0, -4))
        bob.setEndValue(base_pos + QPoint(0, 4))
        bob.setLoopCount(-1)
        bob.setEasingCurve(QEasingCurve.InOutSine)
        bob.start()
        self._name_bob = bob

        # 在聚合过程中仍保持水滴连接，以增强汇聚感
        self._draw_connections = True

        # 触发彩虹渐变动画（1秒过渡）
        rainbow_anim = QPropertyAnimation(self, b"rainbowProgress")
        rainbow_anim.setDuration(1000)
        rainbow_anim.setStartValue(0.0)
        rainbow_anim.setEndValue(1.0)
        rainbow_anim.setEasingCurve(QEasingCurve.InOutQuad)
        rainbow_anim.start()
        self._rainbow_anim = rainbow_anim

    def _show_name_then_expand(self):
        # 隐藏迷你小球
        for mini in getattr(self, 'mini_balls', []):
            mini.hide()

        # 确保名字完全可见
        self.name_label.setVisible(True)
        name_fade = QPropertyAnimation(self.name_label, b"windowOpacity")
        name_fade.setDuration(400)
        name_fade.setStartValue(self.name_label.windowOpacity())
        name_fade.setEndValue(1.0)
        name_fade.start()
        self._name_fade = name_fade

        # 名字稳定1s后扩散平铺
        QTimer.singleShot(1000, self._expand_name_to_welcome)

    def _expand_name_to_welcome(self):
        # 扩散平铺：name_label 放大，透明度降低到30%，边缘模糊（样式模拟）
        end_rect = QRect(0, 0, self.width(), self.height())
        geom_anim = QPropertyAnimation(self.name_label, b"geometry")
        geom_anim.setDuration(900)
        geom_anim.setStartValue(self.name_label.geometry())
        geom_anim.setEndValue(end_rect)
        geom_anim.setEasingCurve(QEasingCurve.OutCubic)

        fade_anim = QPropertyAnimation(self.name_label, b"windowOpacity")
        fade_anim.setDuration(900)
        fade_anim.setStartValue(1.0)
        fade_anim.setEndValue(0.3)

        group = QParallelAnimationGroup(self)
        group.addAnimation(geom_anim)
        group.addAnimation(fade_anim)

        def on_done():
            # 切换到欢迎页布局
            self._show_welcome_page()

        group.finished.connect(on_done)
        group.start()
        self._expand_name_group = group

    def _show_welcome_page(self):
        # 清理前景
        self.name_label.hide()
        for mini in getattr(self, 'mini_balls', []):
            mini.hide()

        # 为迷你球赋予彩虹色，作为扩散背景
        text = "PyPalPrep"
        font = QFont('Microsoft YaHei', 64, QFont.Bold)
        path = QPainterPath()
        path.addText(0, 0, font, text)
        rect = path.boundingRect()
        center = QPointF(self.width()/2, self.height()/2)
        dx = center.x() - rect.center().x()
        dy = center.y() - rect.center().y()
        path.translate(dx, dy)

        total = path.elementCount()
        step = max(1, total // max(1, len(self.mini_balls)))
        sampled = []
        for i in range(0, total, step):
            elem = path.elementAt(i)
            sampled.append((elem.x, elem.y))
        if not sampled:
            cx, cy = center.x(), center.y()
            sampled = [(cx-80, cy), (cx-40, cy), (cx, cy), (cx+40, cy), (cx+80, cy)]

        # 为每个迷你球赋予彩虹色
        for i, mini in enumerate(self.mini_balls):
            idx = i % len(sampled)
            # 根据在文字中的位置计算彩虹色索引
            color_idx = int((idx / len(sampled)) * len(self.RAINBOW_COLORS)) % len(self.RAINBOW_COLORS)
            color = self.RAINBOW_COLORS[color_idx]
            mini._rainbow_color = color
            mini._use_rainbow = True

        # 固定主球居中且停止旋转，避免"飞出去"的视觉偏移
        try:
            cx = self.width()//2
            cy = self.height()//2
            size = self.main_ball.width()
            self.main_ball.setGeometry(cx - size//2, cy - size//2, size, size)
            if hasattr(self, 'rotate_anim'):
                self.rotate_anim.stop()
        except Exception:
            pass

        # 关闭水滴连接绘制，开启彩虹背景绘制
        self._draw_connections = False
        self._draw_rainbow_bg = True

        # 欢迎页背景轻微模糊扩散（模拟）
        try:
            from PyQt5.QtWidgets import QGraphicsBlurEffect
            blur = QGraphicsBlurEffect(self)
            blur.setBlurRadius(6)
            self.main_ball.setGraphicsEffect(blur)
        except Exception:
            pass

    def getRainbowProgress(self):
        return getattr(self, '_rainbow_progress', 0.0)

    def setRainbowProgress(self, v):
        self._rainbow_progress = v
        # 同步到所有球体
        self.main_ball._rainbow_progress = v
        for mini in getattr(self, 'mini_balls', []):
            mini._rainbow_progress = v
        self.update()

    rainbowProgress = pyqtProperty(float, fget=getRainbowProgress, fset=setRainbowProgress)

    def paintEvent(self, event):
        # 叠加绘制彩虹背景与水滴连接效果
        super().paintEvent(event)

        # 绘制彩虹背景（在欢迎页）
        if getattr(self, '_draw_rainbow_bg', False):
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            for mini in getattr(self, 'mini_balls', []):
                if hasattr(mini, '_use_rainbow') and mini._use_rainbow:
                    color = getattr(mini, '_rainbow_color', QColor(179, 229, 252))
                    # 低透明度（约30%×15%）
                    color.setAlpha(int(50))
                    painter.setBrush(QBrush(color))
                    painter.setPen(Qt.NoPen)
                    # 使用 drawEllipse(x, y, w, h)
                    painter.drawEllipse(int(mini.x()), int(mini.y()), mini.width(), mini.height())

        if not getattr(self, '_draw_connections', False):
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        main_center = QPointF(self.main_ball.x() + self.main_ball.width()/2,
                               self.main_ball.y() + self.main_ball.height()/2)
        for mini in getattr(self, 'mini_balls', []):
            if not mini.isVisible():
                continue
            mini_center = QPointF(mini.x() + mini.width()/2,
                                   mini.y() + mini.height()/2)
            dx = mini_center.x() - main_center.x()
            dy = mini_center.y() - main_center.y()
            dist = math.hypot(dx, dy)
            if dist > 160:
                continue
            t = max(0.0, 1.0 - dist/160.0)
            color = QColor(179, 229, 252, int(140 * t))
            pen = QPen(color)
            pen.setWidthF(7.0 * t + 1.0)
            painter.setPen(pen)
            mid = QPointF((main_center.x()+mini_center.x())/2,
                          (main_center.y()+mini_center.y())/2)
            nx, ny = -dy/dist if dist else 0, dx/dist if dist else 0
            ctrl = QPointF(mid.x() + nx * 22 * t, mid.y() + ny * 22 * t)
            path = QPainterPath(main_center)
            path.quadTo(ctrl, mini_center)
            painter.drawPath(path)

        # 欢迎页：主标题、副标题与按钮
        self.welcome_title = QLabel('PyPalPrep', self)
        self.welcome_title.setFont(QFont('SF Pro Display', 50))
        self.welcome_title.setStyleSheet('color: white;')
        self.welcome_title.setAlignment(Qt.AlignCenter)
        self.welcome_title.setGeometry(self.width()//2 - 200, self.height()//2 - 140, 400, 60)

        self.welcome_subtitle = QLabel('欢迎开启 Python 学习之旅', self)
        self.welcome_subtitle.setFont(QFont('SF Pro Display', 18))
        self.welcome_subtitle.setStyleSheet('color: #D0D0D0;')
        self.welcome_subtitle.setAlignment(Qt.AlignCenter)
        self.welcome_subtitle.setGeometry(self.width()//2 - 200, self.height()//2 - 70, 400, 30)

        self.btn_signin = QPushButton('Sign In', self)
        self.btn_signup = QPushButton('Sign Up', self)
        for btn in (self.btn_signin, self.btn_signup):
            btn.setStyleSheet('''
                QPushButton { background-color: white; color: #1E88E5; border: 2px solid #B3E5FC; border-radius: 18px; padding: 10px 18px; }
                QPushButton:hover { background-color: #B3E5FC; color: white; }
            ''')
            btn.setFixedSize(140, 40)

        self.btn_signin.setGeometry(self.width()//2 - 150, self.height()//2 + 20, 140, 40)
        self.btn_signup.setGeometry(self.width()//2 + 10, self.height()//2 + 20, 140, 40)

        # 标题左右微摆动
        title_anim = QPropertyAnimation(self.welcome_title, b"pos")
        title_anim.setDuration(2000)
        title_anim.setStartValue(self.welcome_title.pos() - QPoint(6, 0))
        title_anim.setEndValue(self.welcome_title.pos() + QPoint(6, 0))
        title_anim.setLoopCount(-1)
        title_anim.start()
        self._title_anim = title_anim

        # 副标题淡入淡出循环
        sub_op = QGraphicsOpacityEffect(self.welcome_subtitle)
        self.welcome_subtitle.setGraphicsEffect(sub_op)
        sub_fade = QPropertyAnimation(sub_op, b"opacity")
        sub_fade.setDuration(2000)
        sub_fade.setStartValue(0.4)
        sub_fade.setEndValue(1.0)
        sub_fade.setLoopCount(-1)
        sub_fade.start()
        self._sub_fade = sub_fade

        # 欢迎页背景轻微模糊扩散（模拟）：在主球上添加模糊效果
        try:
            from PyQt5.QtWidgets import QGraphicsBlurEffect
            blur = QGraphicsBlurEffect(self)
            blur.setBlurRadius(6)
            self.main_ball.setGraphicsEffect(blur)
        except Exception:
            pass

        # 按钮从下向上滑入
        for btn in (self.btn_signin, self.btn_signup):
            start = btn.pos() + QPoint(0, 40)
            anim = QPropertyAnimation(btn, b"pos")
            anim.setDuration(700)
            anim.setStartValue(start)
            anim.setEndValue(btn.pos())
            anim.setEasingCurve(QEasingCurve.OutCubic)
            anim.start()
        # 完成后保留在欢迎页，等待用户操作

    def _finish(self):
        # 结束遮罩并发出 finished 信号
        try:
            self.hide()
        except Exception:
            pass
        self.finished.emit()

    def _reveal_login_form(self):
        # 显现登录表单（右侧，从右向左渐入 + 轻微上浮）
        self.login_frame.setVisible(True)
        self.login_frame.move(self.width()//2 + 100, self.height()//2 - 100)

        # 渐入动画
        opacity_effect = QGraphicsOpacityEffect(self.login_frame)
        self.login_frame.setGraphicsEffect(opacity_effect)
        opacity_anim = QPropertyAnimation(opacity_effect, b"opacity")
        opacity_anim.setDuration(800)
        opacity_anim.setStartValue(0.0)
        opacity_anim.setEndValue(1.0)

        # 上浮动画
        pos_anim = QPropertyAnimation(self.login_frame, b"pos")
        pos_anim.setDuration(800)
        pos_anim.setStartValue(self.login_frame.pos())
        pos_anim.setEndValue(self.login_frame.pos() - QPoint(0, 10))
        pos_anim.setEasingCurve(QEasingCurve.OutCubic)

        group = QParallelAnimationGroup(self)
        group.addAnimation(opacity_anim)
        group.addAnimation(pos_anim)
        group.start()
        self._reveal_group = group

        # 鼠标悬停放缓旋转
        self.setMouseTracking(True)
        self.mouseMoveEvent = self._on_mouse_move

    def _on_mouse_move(self, event):
        # 检查鼠标是否在选项区
        form_rect = self.login_frame.geometry()
        if form_rect.contains(event.pos()):
            self.rotate_anim.setDuration(2000)  # 放缓到0.5s/圈
        else:
            self.rotate_anim.setDuration(800)

    def _on_login_clicked(self):
        # 模拟登录成功，结束动效
        self.finished.emit()

    def _on_register_clicked(self):
        # 暂时无操作
        pass


class BallWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._angle = 0
        self._irregular_factor = 1.0
        self._opacity = 1.0
        self._irregular = True
        self._rainbow_progress = 0.0
        # 水珠初始色：#B3E5FC
        self._base_color = QColor('#B3E5FC')
        self._base_color.setAlpha(int(0.7 * 255))
        self.setAttribute(Qt.WA_TranslucentBackground)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setOpacity(self._opacity)

        # 混合色：从水珠蓝渐变到彩虹色
        progress = getattr(self, '_rainbow_progress', 0.0)
        if progress > 0 and hasattr(LaunchOverlay, 'RAINBOW_COLORS'):
            color_idx = int(progress * (len(LaunchOverlay.RAINBOW_COLORS) - 1))
            if color_idx < len(LaunchOverlay.RAINBOW_COLORS) - 1:
                c1 = LaunchOverlay.RAINBOW_COLORS[color_idx]
                c2 = LaunchOverlay.RAINBOW_COLORS[color_idx + 1]
                t = progress * (len(LaunchOverlay.RAINBOW_COLORS) - 1) - color_idx
                brush_color = QColor(
                    int(c1.red() * (1-t) + c2.red() * t),
                    int(c1.green() * (1-t) + c2.green() * t),
                    int(c1.blue() * (1-t) + c2.blue() * t)
                )
                brush_color.setAlpha(int(0.7 * 255))
            else:
                brush_color = LaunchOverlay.RAINBOW_COLORS[-1]
                brush_color.setAlpha(int(0.7 * 255))
        else:
            brush_color = self._base_color

        if self._irregular_factor > 0:
            gradient = QRadialGradient(self.width()/2, self.height()/2, self.width()/2)
            # 高光渐变模拟水珠光泽
            gradient.setColorAt(0.0, brush_color)
            gradient.setColorAt(0.6, brush_color)
            lighter = QColor(brush_color)
            lighter.setAlpha(int(lighter.alpha() * 0.3))
            gradient.setColorAt(1.0, lighter)
            painter.setBrush(QBrush(gradient))
            painter.setPen(Qt.NoPen)
            path = QPainterPath()
            path.addEllipse(0, 0, self.width(), self.height())
            painter.drawPath(path)
        else:
            gradient = QRadialGradient(self.width()*0.3, self.height()*0.3, self.width()/2)
            gradient.setColorAt(0.0, QColor(255, 255, 255, int(0.3 * 255)))
            gradient.setColorAt(0.5, brush_color)
            gradient.setColorAt(1.0, brush_color)
            painter.setBrush(QBrush(gradient))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(0, 0, self.width(), self.height())

        painter.save()
        painter.translate(self.width()/2, self.height()/2)
        painter.rotate(self._angle)
        painter.setBrush(QBrush(QColor(180, 220, 255, 200)))
        painter.drawRect(QRect(-2, int(-self.height()/4), 4, int(self.height()/2)))
        painter.restore()

    def getAngle(self):
        return self._angle

    def setAngle(self, v):
        self._angle = v
        self.update()

    def getIrregularFactor(self):
        return self._irregular_factor

    def setIrregularFactor(self, v):
        self._irregular_factor = v
        self.update()

    def getOpacity(self):
        return self._opacity

    def setOpacity(self, v):
        self._opacity = v
        self.update()

    def setIrregular(self, irregular):
        self._irregular = irregular
        self.update()

    angle = pyqtProperty(float, fget=getAngle, fset=setAngle)
    irregularFactor = pyqtProperty(float, fget=getIrregularFactor, fset=setIrregularFactor)
    opacity = pyqtProperty(float, fget=getOpacity, fset=setOpacity)


class MiniBallWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._angle = 0
        self._orbit_angle = 0
        self._rainbow_progress = 0.0
        # 初始浅蓝水珠色：#E0F7FF
        self._base_color = QColor('#E0F7FF')
        self._base_color.setAlpha(int(0.6 * 255))
        self._rainbow_color = None
        self._use_rainbow = False
        self.setAttribute(Qt.WA_TranslucentBackground)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 选择色彩源
        if self._use_rainbow and self._rainbow_color:
            color = QColor(self._rainbow_color)
            color.setAlpha(int(0.6 * 255))
        else:
            # 混合渐变：从水珠蓝到彩虹色
            progress = getattr(self, '_rainbow_progress', 0.0)
            if progress > 0 and hasattr(LaunchOverlay, 'RAINBOW_COLORS'):
                color_idx = int(progress * (len(LaunchOverlay.RAINBOW_COLORS) - 1))
                if color_idx < len(LaunchOverlay.RAINBOW_COLORS) - 1:
                    c1 = LaunchOverlay.RAINBOW_COLORS[color_idx]
                    c2 = LaunchOverlay.RAINBOW_COLORS[color_idx + 1]
                    t = progress * (len(LaunchOverlay.RAINBOW_COLORS) - 1) - color_idx
                    color = QColor(
                        int(c1.red() * (1-t) + c2.red() * t),
                        int(c1.green() * (1-t) + c2.green() * t),
                        int(c1.blue() * (1-t) + c2.blue() * t)
                    )
                    color.setAlpha(int(0.6 * 255))
                else:
                    color = QColor(LaunchOverlay.RAINBOW_COLORS[-1])
                    color.setAlpha(int(0.6 * 255))
            else:
                color = self._base_color

        # 带高光渐变的球体
        gradient = QRadialGradient(self.width()*0.3, self.height()*0.3, self.width()/2)
        gradient.setColorAt(0.0, QColor(255, 255, 255, int(0.2 * 255)))
        gradient.setColorAt(0.4, color)
        gradient.setColorAt(1.0, color)
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, self.width(), self.height())

    def getAngle(self):
        return self._angle

    def setAngle(self, v):
        self._angle = v
        self.update()

    def getOrbitAngle(self):
        return self._orbit_angle

    def setOrbitAngle(self, v):
        self._orbit_angle = v
        # 更新位置
        center = QPointF(self.parent().width()//2, self.parent().height()//2)
        dist = 60  # 固定半径
        # 缩小随机抖动，避免视觉上主球“位移”的错觉
        jitter = 4
        x = center.x() + dist * math.cos(v) + random.uniform(-jitter, jitter)
        y = center.y() + dist * math.sin(v) + random.uniform(-jitter, jitter)
        self.move(int(x - self.width()/2), int(y - self.height()/2))
        self.update()

    angle = pyqtProperty(float, fget=getAngle, fset=setAngle)
    orbitAngle = pyqtProperty(float, fget=getOrbitAngle, fset=setOrbitAngle)