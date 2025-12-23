# -*- coding: utf-8 -*-
"""
启动遮罩与登录页动效 v2（iOS 极简高级风格）
核心：主体水珠 + 水流扩散，全程平缓流畅，无乱飞
时序：0-1秒初始 → 1-4秒放大 → 4-6秒汇聚 → 6-8秒彩虹渐变 → 8-11秒扩散 → 11秒欢迎页
"""
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QApplication, QFrame
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, pyqtSignal, QParallelAnimationGroup, QTimer, pyqtProperty, QEasingCurve, QPointF, QPoint, QSequentialAnimationGroup
from PyQt5.QtGui import QFont, QPalette, QColor, QPainter, QBrush, QPen, QRadialGradient, QPainterPath, QLinearGradient
from PyQt5.QtWidgets import QGraphicsOpacityEffect, QGraphicsDropShadowEffect
import random
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

        # 极简浅灰背景
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor('#F8F9FA'))
        self.setPalette(palette)

        # 主体水珠（大水珠主体）
        self.main_ball = WaterDropletWidget(self)
        self.main_ball.setFixedSize(100, 100)
        self.main_ball.move(self.width()//2 - 50, self.height()//2 - 50)

        # 水流容器（6-8股细小水珠流，缠绕在主体周围）
        self.water_streams = []
        for i in range(7):
            stream = WaterStreamWidget(self)
            self.water_streams.append(stream)

        # 文字标签（显示 "PyPalPrep"）
        self.text_label = QLabel("PyPalPrep", self)
        self.text_label.setFont(QFont('SF Pro Rounded', 48, QFont.Medium))
        self.text_label.setStyleSheet('color: rgba(179, 229, 252, 0);')  # 初始隐藏
        self.text_label.setAlignment(Qt.AlignCenter)

        # 彩虹渐变进度（0.0-1.0）
        self._rainbow_progress = 0.0
        self._stream_scatter_progress = 0.0

        self.start()

    def start(self):
        """启动完整动画序列"""
        self.showFullScreen()
        self._start_sequence()

    def _start_sequence(self):
        """按时序执行完整动画流程"""
        # 0-1秒：初始化（水珠+水流缠绕）
        QTimer.singleShot(0, self._init_water_streams)
        
        # 1秒后：开始放大（1-4秒，持续3秒）
        QTimer.singleShot(1000, self._expand_phase)
        
        # 4秒后：汇聚成字（4-6秒，持续2秒）
        QTimer.singleShot(4000, self._gather_phase)
        
        # 6秒后：彩虹渐变（6-8秒，持续2秒）
        QTimer.singleShot(6500, self._rainbow_phase)
        
        # 8秒后：水流扩散（8-11秒，持续3秒）
        QTimer.singleShot(8000, self._scatter_phase)
        
        # 11秒后：显示欢迎页
        QTimer.singleShot(11000, self._show_welcome)

    def _init_water_streams(self):
        """初始化水流，缠绕在主体周围"""
        self.main_ball.setVisible(True)
        cx = self.width() // 2
        cy = self.height() // 2
        
        for i, stream in enumerate(self.water_streams):
            stream.setVisible(True)
            # 环绕主体，角度均匀分布
            angle = (i / len(self.water_streams)) * 2 * math.pi
            stream._base_angle = angle
            stream._orbit_radius = 60  # 初始围绕半径
            stream._update_position(cx, cy, angle, 60)
            
            # 慢速旋转：0.2秒/圈（比原来慢4倍）
            orbit_anim = QPropertyAnimation(stream, b"orbitAngle")
            orbit_anim.setDuration(2000)  # 2秒一圈
            orbit_anim.setStartValue(angle)
            orbit_anim.setEndValue(angle + 2 * math.pi)
            orbit_anim.setLoopCount(-1)
            orbit_anim.start()
            stream._orbit_anim = orbit_anim

    def _expand_phase(self):
        """1-4秒：主体+水流同步放大（匀速无卡顿）"""
        cx = self.width() // 2
        cy = self.height() // 2
        
        # 主体水珠放大：100px → 600px
        expand_anim = QPropertyAnimation(self.main_ball, b"geometry")
        expand_anim.setDuration(3000)  # 3秒
        expand_anim.setStartValue(QRect(cx - 50, cy - 50, 100, 100))
        expand_anim.setEndValue(QRect(cx - 300, cy - 300, 600, 600))
        expand_anim.setEasingCurve(QEasingCurve.Linear)  # 匀速
        
        # 水流同步放大（通过缩放半径）
        radius_anim = QPropertyAnimation(self, b"streamRadius")
        radius_anim.setDuration(3000)
        radius_anim.setStartValue(60)
        radius_anim.setEndValue(300)
        radius_anim.setEasingCurve(QEasingCurve.Linear)
        
        group = QParallelAnimationGroup(self)
        group.addAnimation(expand_anim)
        group.addAnimation(radius_anim)
        group.finished.connect(self._on_expand_done)
        group.start()
        self._expand_anim = group

    def _on_expand_done(self):
        """放大完成后，更新所有水流的轨道半径"""
        for stream in self.water_streams:
            stream._orbit_radius = 300

    def _gather_phase(self):
        """4-6秒：水流聚拢，拼接成 'PyPalPrep' 文字"""
        # 停止水流的公转动画
        for stream in self.water_streams:
            if hasattr(stream, '_orbit_anim'):
                stream._orbit_anim.stop()
        
        # 计算文字布局点（基于主球中心）
        cx = self.width() // 2
        cy = self.height() // 2
        text = "PyPalPrep"
        
        # 简化：文字从左到右均匀分布在主球表面
        char_count = len(text)
        text_width = 450  # 文字总宽度
        text_height = 200
        start_x = cx - text_width // 2
        start_y = cy - text_height // 2
        
        targets = []
        for i in range(len(self.water_streams)):
            # 水流按顺序映射到文字的不同位置
            char_idx = i % char_count
            x = start_x + (char_idx / char_count) * text_width
            y = start_y + (random.random() - 0.5) * text_height
            targets.append((x, y))
        
        # 动画：水流聚拢到文字位置
        group = QParallelAnimationGroup(self)
        for i, stream in enumerate(self.water_streams):
            tx, ty = targets[i]
            anim = QPropertyAnimation(stream, b"pos")
            anim.setDuration(2000)  # 2秒聚拢
            anim.setStartValue(stream.pos())
            anim.setEndValue(QPoint(int(tx), int(ty)))
            anim.setEasingCurve(QEasingCurve.InOutCubic)
            group.addAnimation(anim)
        
        group.finished.connect(self._on_gather_done)
        group.start()
        self._gather_anim = group

    def _on_gather_done(self):
        """聚拢完成，显示文字并准备彩虹渐变"""
        self.text_label.setText("PyPalPrep")
        self.text_label.setStyleSheet('color: rgba(179, 229, 252, 255);')  # 显示
        self.text_label.setVisible(True)
        # 重新计算位置（中心对齐）
        metrics = self.text_label.fontMetrics()
        width = metrics.width("PyPalPrep")
        self.text_label.setGeometry(
            self.width() // 2 - width // 2,
            self.height() // 2 - 30,
            width + 20,
            60
        )

    def _rainbow_phase(self):
        """6-8秒：从左到右的线性彩虹渐变"""
        rainbow_anim = QPropertyAnimation(self, b"rainbowProgress")
        rainbow_anim.setDuration(2000)  # 2秒
        rainbow_anim.setStartValue(0.0)
        rainbow_anim.setEndValue(1.0)
        rainbow_anim.setEasingCurve(QEasingCurve.Linear)
        rainbow_anim.start()
        self._rainbow_anim = rainbow_anim

    def _scatter_phase(self):
        """8-11秒：水流扩散平铺，形成背景纹理"""
        scatter_anim = QPropertyAnimation(self, b"streamScatterProgress")
        scatter_anim.setDuration(3000)  # 3秒
        scatter_anim.setStartValue(0.0)
        scatter_anim.setEndValue(1.0)
        scatter_anim.setEasingCurve(QEasingCurve.Linear)
        scatter_anim.start()
        self._scatter_anim = scatter_anim

    def _show_welcome(self):
        """11秒后：显示欢迎页"""
        self.text_label.hide()
        for stream in self.water_streams:
            stream.hide()
        self.main_ball.hide()
        
        # 创建欢迎页UI
        self._create_welcome_ui()

    def _create_welcome_ui(self):
        """构建欢迎页UI"""
        # 主标题
        title = QLabel("PyPalPrep", self)
        title.setFont(QFont('SF Pro Rounded', 80, QFont.Medium))
        title.setStyleSheet('color: white;')
        title.setAlignment(Qt.AlignCenter)
        title.setGeometry(self.width()//2 - 200, self.height()//2 - 150, 400, 100)
        
        # 副标题
        subtitle = QLabel("Welcome to Your Learning Journey", self)
        subtitle.setFont(QFont('SF Pro Rounded', 18))
        subtitle.setStyleSheet('color: rgba(255, 255, 255, 0.7);')
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setGeometry(self.width()//2 - 300, self.height()//2 - 30, 600, 50)
        
        # 按钮：Sign In
        btn_signin = QPushButton("Sign In", self)
        btn_signin.setFont(QFont('SF Pro Rounded', 16))
        btn_signin.setGeometry(self.width()//2 - 160, self.height()//2 + 60, 150, 50)
        btn_signin.setStyleSheet('''
            QPushButton {
                background-color: white;
                color: #B3E5FC;
                border: 2px solid #B3E5FC;
                border-radius: 25px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #B3E5FC;
                color: white;
            }
        ''')
        
        # 按钮：Sign Up
        btn_signup = QPushButton("Sign Up", self)
        btn_signup.setFont(QFont('SF Pro Rounded', 16))
        btn_signup.setGeometry(self.width()//2 + 10, self.height()//2 + 60, 150, 50)
        btn_signup.setStyleSheet('''
            QPushButton {
                background-color: transparent;
                color: white;
                border: 2px solid white;
                border-radius: 25px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: white;
                color: #B3E5FC;
            }
        ''')
        
        # 标题浮动动画
        title_bob = QPropertyAnimation(title, b"pos")
        title_bob.setDuration(2000)
        title_bob.setStartValue(title.pos() + QPoint(0, -8))
        title_bob.setEndValue(title.pos() + QPoint(0, 8))
        title_bob.setLoopCount(-1)
        title_bob.setEasingCurve(QEasingCurve.InOutSine)
        title_bob.start()
        
        # 副标题淡入淡出
        sub_op = QGraphicsOpacityEffect(subtitle)
        subtitle.setGraphicsEffect(sub_op)
        sub_fade = QPropertyAnimation(sub_op, b"opacity")
        sub_fade.setDuration(2000)
        sub_fade.setStartValue(0.5)
        sub_fade.setEndValue(1.0)
        sub_fade.setLoopCount(-1)
        sub_fade.start()
        
        # 按钮滑入动画（从下向上）
        for btn in (btn_signin, btn_signup):
            btn_slide = QPropertyAnimation(btn, b"pos")
            btn_slide.setDuration(1000)
            btn_slide.setStartValue(btn.pos() + QPoint(0, 50))
            btn_slide.setEndValue(btn.pos())
            btn_slide.setEasingCurve(QEasingCurve.OutCubic)
            btn_slide.start()

    def getRainbowProgress(self):
        return self._rainbow_progress

    def setRainbowProgress(self, v):
        self._rainbow_progress = v
        self.main_ball._rainbow_progress = v
        self.update()

    rainbowProgress = pyqtProperty(float, fget=getRainbowProgress, fset=setRainbowProgress)

    def getStreamRadius(self):
        return getattr(self, '_stream_radius', 60)

    def setStreamRadius(self, v):
        self._stream_radius = v
        # 更新所有水流的位置
        cx = self.width() // 2
        cy = self.height() // 2
        for i, stream in enumerate(self.water_streams):
            angle = (i / len(self.water_streams)) * 2 * math.pi
            stream._update_position(cx, cy, angle, v)

    streamRadius = pyqtProperty(float, fget=getStreamRadius, fset=setStreamRadius)

    def getStreamScatterProgress(self):
        return self._stream_scatter_progress

    def setStreamScatterProgress(self, v):
        self._stream_scatter_progress = v
        self.update()

    streamScatterProgress = pyqtProperty(float, fget=getStreamScatterProgress, fset=setStreamScatterProgress)

    def paintEvent(self, event):
        """绘制背景与扩散纹理"""
        super().paintEvent(event)
        
        # 扩散阶段：绘制水流纹理背景
        if self._stream_scatter_progress > 0:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            
            for stream in self.water_streams:
                # 计算扩散目标位置（随机分布）
                target_x = random.uniform(0, self.width())
                target_y = random.uniform(0, self.height())
                
                # 从当前位置向目标扩散
                current_x = stream.x() + (target_x - stream.x()) * self._stream_scatter_progress
                current_y = stream.y() + (target_y - stream.y()) * self._stream_scatter_progress
                
                # 绘制低透明度水珠背景
                color = stream._get_color()
                color.setAlpha(int(50))  # 低透明度（20%）
                painter.setBrush(QBrush(color))
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(int(current_x), int(current_y), stream.width(), stream.height())


class WaterDropletWidget(QWidget):
    """主体水珠：透明浅蓝色，带高光质感"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._rainbow_progress = 0.0
        self.setAttribute(Qt.WA_TranslucentBackground)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 基础色：#B3E5FC，透明度75%
        base_color = QColor('#B3E5FC')
        base_color.setAlpha(int(0.75 * 255))
        
        # 渐变：彩虹色混合（根据进度）
        if self._rainbow_progress > 0:
            rainbow_colors = [
                QColor('#FFB3BA'),  # 红
                QColor('#FFDFBA'),  # 橙
                QColor('#FFFFBA'),  # 黄
                QColor('#BAFFC9'),  # 绿
                QColor('#BAE1FF'),  # 蓝
                QColor('#E2BAFF'),  # 紫
            ]
            idx = int(self._rainbow_progress * (len(rainbow_colors) - 1))
            if idx < len(rainbow_colors) - 1:
                c1 = rainbow_colors[idx]
                c2 = rainbow_colors[idx + 1]
                t = self._rainbow_progress * (len(rainbow_colors) - 1) - idx
                blended = QColor(
                    int(c1.red() * (1 - t) + c2.red() * t),
                    int(c1.green() * (1 - t) + c2.green() * t),
                    int(c1.blue() * (1 - t) + c2.blue() * t)
                )
                blended.setAlpha(int(0.75 * 255))
                draw_color = blended
            else:
                draw_color = rainbow_colors[-1]
                draw_color.setAlpha(int(0.75 * 255))
        else:
            draw_color = base_color
        
        # 绘制圆形水珠
        gradient = QRadialGradient(self.width() * 0.3, self.height() * 0.3, self.width() / 2)
        gradient.setColorAt(0.0, QColor(255, 255, 255, int(0.4 * 255)))  # 高光
        gradient.setColorAt(0.5, draw_color)
        gradient.setColorAt(1.0, draw_color)
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, self.width(), self.height())


class WaterStreamWidget(QWidget):
    """水流：细小水珠，缠绕在主体周围或扩散平铺"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._orbit_angle = 0.0
        self._base_angle = 0.0
        self._orbit_radius = 60
        self._rainbow_progress = 0.0
        # 初始颜色：#E0F7FF，透明度60%
        self._base_color = QColor('#E0F7FF')
        self._base_color.setAlpha(int(0.6 * 255))
        self.setFixedSize(15, 15)  # 细小水珠
        self.setAttribute(Qt.WA_TranslucentBackground)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 色彩混合（彩虹渐变）
        if self._rainbow_progress > 0:
            rainbow_colors = [
                QColor('#FFB3BA'),
                QColor('#FFDFBA'),
                QColor('#FFFFBA'),
                QColor('#BAFFC9'),
                QColor('#BAE1FF'),
                QColor('#E2BAFF'),
            ]
            idx = int(self._rainbow_progress * (len(rainbow_colors) - 1))
            if idx < len(rainbow_colors) - 1:
                c1 = rainbow_colors[idx]
                c2 = rainbow_colors[idx + 1]
                t = self._rainbow_progress * (len(rainbow_colors) - 1) - idx
                color = QColor(
                    int(c1.red() * (1 - t) + c2.red() * t),
                    int(c1.green() * (1 - t) + c2.green() * t),
                    int(c1.blue() * (1 - t) + c2.blue() * t)
                )
                color.setAlpha(int(0.6 * 255))
            else:
                color = rainbow_colors[-1]
                color.setAlpha(int(0.6 * 255))
        else:
            color = self._base_color
        
        # 绘制高光球体
        gradient = QRadialGradient(self.width() * 0.3, self.height() * 0.3, self.width() / 2)
        gradient.setColorAt(0.0, QColor(255, 255, 255, int(0.3 * 255)))
        gradient.setColorAt(0.4, color)
        gradient.setColorAt(1.0, color)
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, self.width(), self.height())

    def getOrbitAngle(self):
        return self._orbit_angle

    def setOrbitAngle(self, v):
        self._orbit_angle = v
        # 根据轨道角度更新位置
        if hasattr(self.parent(), 'width'):
            parent = self.parent()
            cx = parent.width() // 2
            cy = parent.height() // 2
            self._update_position(cx, cy, v, self._orbit_radius)

    orbitAngle = pyqtProperty(float, fget=getOrbitAngle, fset=setOrbitAngle)

    def _update_position(self, cx, cy, angle, radius):
        """根据轨道参数更新位置"""
        x = cx + radius * math.cos(angle) - self.width() // 2
        y = cy + radius * math.sin(angle) - self.height() // 2
        self.move(int(x), int(y))

    def _get_color(self):
        """获取当前色彩"""
        if self._rainbow_progress > 0:
            rainbow_colors = [
                QColor('#FFB3BA'),
                QColor('#FFDFBA'),
                QColor('#FFFFBA'),
                QColor('#BAFFC9'),
                QColor('#BAE1FF'),
                QColor('#E2BAFF'),
            ]
            idx = int(self._rainbow_progress * (len(rainbow_colors) - 1))
            if idx < len(rainbow_colors) - 1:
                c1 = rainbow_colors[idx]
                c2 = rainbow_colors[idx + 1]
                t = self._rainbow_progress * (len(rainbow_colors) - 1) - idx
                return QColor(
                    int(c1.red() * (1 - t) + c2.red() * t),
                    int(c1.green() * (1 - t) + c2.green() * t),
                    int(c1.blue() * (1 - t) + c2.blue() * t)
                )
            else:
                return rainbow_colors[-1]
        else:
            return self._base_color
