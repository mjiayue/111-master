# -*- coding: utf-8 -*-
"""
启动遮罩与登录页动效 v3（iOS 极简高级风格 - 流动水珠演进）
核心：不规则流动水珠 → 放大形成字体 → 彩虹渐变 → 直接欢迎页
"""
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QApplication
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, pyqtSignal, QParallelAnimationGroup, QTimer, pyqtProperty, QEasingCurve, QPointF, QPoint, QSequentialAnimationGroup
from PyQt5.QtGui import QFont, QPalette, QColor, QPainter, QBrush, QPen, QRadialGradient, QPainterPath
from PyQt5.QtWidgets import QGraphicsOpacityEffect
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

        # 核心：流动水珠小部件
        self.water_drop = FlowingWaterDropWidget(self)
        self.water_drop.move(self.width()//2 - 50, self.height()//2 - 50)

        # 彩虹覆盖层（最后阶段）
        self.rainbow_overlay = QWidget(self)
        self.rainbow_overlay.setGeometry(0, 0, self.width(), self.height())
        self.rainbow_overlay.setAttribute(Qt.WA_TranslucentBackground)
        self.rainbow_overlay.setVisible(False)
        self._rainbow_coverage = 0.0

        # 开启启动序列
        QTimer.singleShot(100, self._start_sequence)

    def _start_sequence(self):
        """0-11秒完整动画序列"""
        # 0-1秒：初始状态（水珠已显示，等待）
        QTimer.singleShot(1000, self._expand_phase)
        
        # 1-5秒：放大并形成字体
        # (在_expand_phase中处理)
        
        # 5-7秒：彩虹渐变
        QTimer.singleShot(5000, self._rainbow_phase)
        
        # 7-9秒：彩虹蔓延
        QTimer.singleShot(7000, self._spread_phase)
        
        # 9秒后：欢迎页
        QTimer.singleShot(9000, self._show_welcome)

    def _expand_phase(self):
        """1-5秒：水珠放大（1-4秒纯球形，4-5秒形成字体）"""
        # 放大动画
        expand_anim = QPropertyAnimation(self.water_drop, b"geometry")
        expand_anim.setDuration(4000)  # 4秒
        cx = self.width() // 2
        cy = self.height() // 2
        expand_anim.setStartValue(QRect(cx - 50, cy - 50, 100, 100))
        expand_anim.setEndValue(QRect(cx - 250, cy - 150, 500, 300))
        expand_anim.setEasingCurve(QEasingCurve.InOutCubic)
        expand_anim.start()
        self._expand_anim = expand_anim
        
        # 文字显现动画（延迟 4 秒后开始，持续 1 秒）
        QTimer.singleShot(4000, self._start_morph_to_text)

    def _start_morph_to_text(self):
        """4秒后启动文字显现动画"""
        morph_anim = QPropertyAnimation(self.water_drop, b"textMorphProgress")
        morph_anim.setDuration(1000)  # 1秒
        morph_anim.setStartValue(0.0)
        morph_anim.setEndValue(1.0)
        morph_anim.setEasingCurve(QEasingCurve.InOutCubic)
        morph_anim.start()
        self._morph_anim = morph_anim

    def _rainbow_phase(self):
        """5-7秒：字体从左到右彩虹渐变（清透蓝 → 彩虹色）"""
        rainbow_anim = QPropertyAnimation(self.water_drop, b"rainbowProgress")
        rainbow_anim.setDuration(2000)  # 2秒
        rainbow_anim.setStartValue(0.0)
        rainbow_anim.setEndValue(1.0)
        rainbow_anim.setEasingCurve(QEasingCurve.Linear)
        rainbow_anim.start()
        self._rainbow_anim = rainbow_anim

    def _spread_phase(self):
        """7-9秒：彩虹色蔓延覆盖屏幕"""
        spread_anim = QPropertyAnimation(self, b"rainbowCoverage")
        spread_anim.setDuration(2000)  # 2秒
        spread_anim.setStartValue(0.0)
        spread_anim.setEndValue(1.0)
        spread_anim.setEasingCurve(QEasingCurve.Linear)
        spread_anim.start()
        self._spread_anim = spread_anim

    def _show_welcome(self):
        """9秒后：隐藏水珠与彩虹，显示欢迎页"""
        self.water_drop.hide()
        self.rainbow_overlay.hide()
        self._create_welcome_ui()

    def _create_welcome_ui(self):
        """构建欢迎页UI"""
        # 标题
        title = QLabel("PyPalPrep", self)
        title.setFont(QFont('SF Pro Rounded', 80, QFont.Medium))
        title.setStyleSheet('color: white;')
        title.setAlignment(Qt.AlignCenter)
        title.setGeometry(self.width()//2 - 250, self.height()//2 - 120, 500, 100)
        title.show()
        
        # 副标题
        subtitle = QLabel("Welcome to Your Learning Journey", self)
        subtitle.setFont(QFont('SF Pro Rounded', 18))
        subtitle.setStyleSheet('color: rgba(255, 255, 255, 0.7);')
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setGeometry(self.width()//2 - 300, self.height()//2 - 10, 600, 50)
        subtitle.show()
        
        # Sign In 按钮
        btn_signin = QPushButton("Sign In", self)
        btn_signin.setFont(QFont('SF Pro Rounded', 16, QFont.Medium))
        btn_signin.setGeometry(self.width()//2 - 170, self.height()//2 + 80, 140, 50)
        btn_signin.setStyleSheet('''
            QPushButton {
                background-color: white;
                color: #B3E5FC;
                border: none;
                border-radius: 25px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #B3E5FC;
                color: white;
            }
        ''')
        btn_signin.show()
        
        # Sign Up 按钮
        btn_signup = QPushButton("Sign Up", self)
        btn_signup.setFont(QFont('SF Pro Rounded', 16, QFont.Medium))
        btn_signup.setGeometry(self.width()//2 + 30, self.height()//2 + 80, 140, 50)
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
                color: #1E88E5;
            }
        ''')
        btn_signup.show()
        
        # 标题浮动
        title_bob = QPropertyAnimation(title, b"pos")
        title_bob.setDuration(2000)
        title_bob.setStartValue(title.pos() + QPoint(0, -10))
        title_bob.setEndValue(title.pos() + QPoint(0, 10))
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

    def getRainbowCoverage(self):
        return self._rainbow_coverage

    def setRainbowCoverage(self, v):
        self._rainbow_coverage = v
        self.rainbow_overlay.setVisible(v > 0)
        self.update()

    rainbowCoverage = pyqtProperty(float, fget=getRainbowCoverage, fset=setRainbowCoverage)

    def paintEvent(self, event):
        """绘制彩虹蔓延覆盖"""
        super().paintEvent(event)
        
        if self._rainbow_coverage > 0:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # 彩虹色梯度从上到下蔓延
            rainbow_colors = [
                QColor('#FFB3BA'),  # 红
                QColor('#FFDFBA'),  # 橙
                QColor('#FFFFBA'),  # 黄
                QColor('#BAFFC9'),  # 绿
                QColor('#BAE1FF'),  # 蓝
                QColor('#E2BAFF'),  # 紫
            ]
            
            # 绘制蔓延矩形（从上向下）
            coverage_height = int(self.height() * self._rainbow_coverage)
            for i in range(6):
                color = rainbow_colors[i]
                alpha = int(60 * self._rainbow_coverage)  # 低透明度
                color.setAlpha(alpha)
                painter.fillRect(0, i * (self.height() // 6), self.width(), self.height() // 6, color)


class FlowingWaterDropWidget(QWidget):
    """流动的不规则水珠：初始→放大成字形→彩虹渐变"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._text_morph_progress = 0.0  # 0.0 → 1.0：从球形变成字体
        self._rainbow_progress = 0.0  # 0.0 → 1.0：彩虹渐变程度
        self._wave_phase = 0.0  # 波纹动画
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # 启动波纹效果（持续动画）
        wave_anim = QPropertyAnimation(self, b"wavePhase")
        wave_anim.setDuration(3000)
        wave_anim.setStartValue(0.0)
        wave_anim.setEndValue(2 * math.pi)
        wave_anim.setLoopCount(-1)
        wave_anim.start()
        self._wave_anim = wave_anim

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        
        w = self.width()
        h = self.height()
        
        # 混合色：从清透水珠蓝逐渐过渡到彩虹色
        if self._rainbow_progress > 0:
            rainbow_colors = [
                QColor('#FFB3BA'), QColor('#FFDFBA'), QColor('#FFFFBA'),
                QColor('#BAFFC9'), QColor('#BAE1FF'), QColor('#E2BAFF'),
            ]
            idx = int(self._rainbow_progress * (len(rainbow_colors) - 1))
            if idx < len(rainbow_colors) - 1:
                c1 = rainbow_colors[idx]
                c2 = rainbow_colors[idx + 1]
                t = self._rainbow_progress * (len(rainbow_colors) - 1) - idx
                color = QColor(
                    int(c1.red() * (1-t) + c2.red() * t),
                    int(c1.green() * (1-t) + c2.green() * t),
                    int(c1.blue() * (1-t) + c2.blue() * t)
                )
            else:
                color = rainbow_colors[-1]
        else:
            color = QColor('#B3E5FC')  # 清透水珠蓝
        
        color.setAlpha(int(0.8 * 255))  # 透明度75%
        
        # 绘制不规则的有机形状（模拟流动水珠）
        path = self._generate_water_drop_path(w, h)
        
        # 渐变填充（高光效果）
        gradient = self._create_water_gradient(w, h, color)
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawPath(path)
        
        # 阴影效果（增强水珠的立体感）
        shadow_color = QColor(0, 0, 0, 30)
        shadow_path = self._generate_shadow_path(w, h)
        painter.setBrush(QBrush(shadow_color))
        painter.drawPath(shadow_path)

    def _generate_water_drop_path(self, w, h):
        """生成不规则水珠形状（球形 → 字体混合）"""
        path = QPainterPath()
        
        # 初期（< 20% 进度）：纯球形
        if self._text_morph_progress < 0.2:
            cx, cy = w / 2, h / 2
            radius = min(w, h) / 2.8
            
            # 添加波纹变形（不规则边缘）
            num_points = 64
            for i in range(num_points + 1):
                angle = (i / num_points) * 2 * math.pi
                # 波纹扰动 + 随机突起
                wave_amp = 0.08 * math.sin(self._wave_phase + angle * 3)
                random_bump = random.uniform(-0.05, 0.05)
                r = radius * (1 + wave_amp + random_bump)
                x = cx + r * math.cos(angle)
                y = cy + r * math.sin(angle)
                if i == 0:
                    path.moveTo(x, y)
                else:
                    path.lineTo(x, y)
            path.closeSubpath()
        else:
            # 后期（>= 20% 进度）：逐渐过渡到字体
            t = min(1.0, self._text_morph_progress)
            
            # 生成文字路径
            font = QFont('SF Pro Rounded', int(min(w, h) * 0.55), QFont.Bold)
            text_path = QPainterPath()
            text_path.addText(0, 0, font, "PyPalPrep")
            
            # 获取文字边界并居中
            text_rect = text_path.boundingRect()
            tx = (w - text_rect.width()) / 2
            ty = (h - text_rect.height()) / 2
            text_path.translate(tx - text_rect.left(), ty - text_rect.top())
            
            # 如果进度还不足 100%，则混合球形与文字
            if t < 1.0:
                # 绘制球形 + 文字叠加（透明度混合）
                cx, cy = w / 2, h / 2
                radius = min(w, h) / 2.8 * (1 - t * 0.3)  # 球形逐渐缩小
                
                # 先绘制球形
                num_points = 64
                for i in range(num_points + 1):
                    angle = (i / num_points) * 2 * math.pi
                    wave_amp = 0.05 * math.sin(self._wave_phase + angle * 3)
                    r = radius * (1 + wave_amp)
                    x = cx + r * math.cos(angle)
                    y = cy + r * math.sin(angle)
                    if i == 0:
                        path.moveTo(x, y)
                    else:
                        path.lineTo(x, y)
                path.closeSubpath()
                # 再添加文字轮廓（部分透明）
                path.addPath(text_path)
            else:
                # 完全是文字
                path = text_path

        return path

    def _generate_shadow_path(self, w, h):
        """生成阴影路径（下方）"""
        shadow_path = QPainterPath()
        cx, cy = w / 2, h * 0.7
        shadow_path.addEllipse(cx - w * 0.35, cy, w * 0.7, h * 0.3)
        return shadow_path

    def _create_water_gradient(self, w, h, base_color):
        """创建水珠渐变（高光 + 阴影）"""
        gradient = QRadialGradient(w * 0.35, h * 0.3, max(w, h) / 2)
        
        # 高光（白色透明）
        highlight = QColor(255, 255, 255, int(0.4 * 255))
        gradient.setColorAt(0.0, highlight)
        
        # 中间色
        gradient.setColorAt(0.5, base_color)
        
        # 边缘色（暗一点）
        edge_color = QColor(base_color)
        edge_color.setAlpha(int(0.5 * 255))
        gradient.setColorAt(1.0, edge_color)
        
        return gradient

    def getTextMorphProgress(self):
        return self._text_morph_progress

    def setTextMorphProgress(self, v):
        self._text_morph_progress = v
        self.update()

    textMorphProgress = pyqtProperty(float, fget=getTextMorphProgress, fset=setTextMorphProgress)

    def getRainbowProgress(self):
        return self._rainbow_progress

    def setRainbowProgress(self, v):
        self._rainbow_progress = v
        self.update()

    rainbowProgress = pyqtProperty(float, fget=getRainbowProgress, fset=setRainbowProgress)

    def getWavePhase(self):
        return self._wave_phase

    def setWavePhase(self, v):
        self._wave_phase = v
        self.update()

    wavePhase = pyqtProperty(float, fget=getWavePhase, fset=setWavePhase)
