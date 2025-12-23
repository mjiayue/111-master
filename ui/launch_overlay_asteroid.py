# -*- coding: utf-8 -*-
"""
启动动画：小行星 + 丝带环带 + 文字逐字符拼成
iOS 极简高级风：银蓝冷调，内敛质感，400px小行星+文字轻微超出
"""
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, pyqtSignal, QTimer, pyqtProperty, QEasingCurve, QPoint, QElapsedTimer
from PyQt5.QtGui import QFont, QPalette, QColor, QPainter, QBrush, QRadialGradient, QPainterPath, QFontMetrics, QPen
import math
import random


class AsteroidWidget(QWidget):
    """小行星：银蓝渐变，8秒自转，哑光金属质感"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # 小行星属性
        self.diameter = 400  # 400px固定直径
        self.rotation_angle = 0  # 旋转角度
        
        # 启动定时器：8秒/圈
        self.rotation_timer = QTimer()
        self.rotation_timer.timeout.connect(self._update_rotation)
        self.rotation_timer.start(16)  # 16ms刷新率
        
        self.creation_time = QElapsedTimer()
        self.creation_time.start()
        self.start_time = self.creation_time.elapsed()
        
        self.resize(self.diameter, self.diameter)
        
    def _update_rotation(self):
        """更新旋转角度：8秒一圈"""
        elapsed = self.creation_time.elapsed() - self.start_time
        self.rotation_angle = (elapsed / 8000.0) * 360.0  # 8秒360度
        self.update()
    
    def paintEvent(self, event):
        """绘制小行星：哑光金属质感"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        
        center_x = self.diameter / 2.0
        center_y = self.diameter / 2.0
        
        # 保存变换矩阵
        painter.save()
        painter.translate(center_x, center_y)
        painter.rotate(self.rotation_angle)
        painter.translate(-center_x, -center_y)
        
        # 第1层：核心银蓝渐变（中心深银灰，边缘浅蓝，对比明显）
        gradient = QRadialGradient(center_x, center_y, self.diameter / 2.0)
        gradient.setColorAt(0.0, QColor('#5B7A9E'))  # 核心：深银灰
        gradient.setColorAt(0.7, QColor('#8FBAE0'))  # 中间：中性银蓝
        gradient.setColorAt(1.0, QColor('#C5D9ED'))  # 边缘：浅蓝
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, self.diameter, self.diameter)
        
        # 第2层：哑光金属光泽（稀疏针尖细闪）
        self._draw_metallic_sheen(painter, center_x, center_y)
        
        # 第3层：稀疏银色细闪（≤1px）
        self._draw_fine_sparkles(painter, center_x, center_y)
        
        painter.restore()
    
    def _draw_metallic_sheen(self, painter, cx, cy):
        """绘制哑光金属光泽：上方弧形高光"""
        sheen_gradient = QRadialGradient(cx, cy * 0.3, self.diameter * 0.15)
        sheen_gradient.setColorAt(0.0, QColor(255, 255, 255, 10))  # 中心白色极淡
        sheen_gradient.setColorAt(1.0, QColor(255, 255, 255, 0))   # 边缘透明
        
        painter.setBrush(QBrush(sheen_gradient))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(int(cx - self.diameter * 0.2), int(cy * 0.05), 
                           int(self.diameter * 0.4), int(self.diameter * 0.3))
    
    def _draw_fine_sparkles(self, painter, cx, cy):
        """绘制稀疏银色细闪（≤1px）"""
        # 固定种子以保证一致性
        random.seed(42)
        
        num_sparkles = max(8, self.diameter // 50)  # 根据大小调整数量
        
        for _ in range(num_sparkles):
            # 随机位置：圆形范围内
            angle = random.uniform(0, 2 * math.pi)
            r = random.uniform(self.diameter * 0.1, self.diameter * 0.45)
            
            sparkle_x = cx + r * math.cos(angle)
            sparkle_y = cy + r * math.sin(angle)
            
            # 绘制1px的极淡银色点
            painter.setBrush(QColor(200, 210, 220, 80))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(int(sparkle_x - 0.5), int(sparkle_y - 0.5), 1, 1)
    
    def stop_rotation(self):
        """停止旋转"""
        self.rotation_timer.stop()


class RibbonTextWidget(QWidget):
    """丝带环带 + 逐字符拼成文字（内敛贴合行星）"""
    char_finished = pyqtSignal()
    
    def __init__(self, asteroid_diameter=400, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.text = "PyPalPrep"
        self.asteroid_diameter = asteroid_diameter
        self.char_progress = 0
        self.char_visibility = []
        self.is_finished = False
        
        # 字体配置：字高占行星直径70%
        font_size = int(asteroid_diameter * 0.7 / 1.5)  # 根据行星大小调整
        self.font = QFont("SF Pro Rounded", font_size)
        self.font.setBold(True)
        self.font.setLetterSpacing(QFont.PercentageSpacing, 120)  # 字间距+2px
        
        # 颜色：内层银灰勾边，外层浅蓝填底
        self.stroke_color = QColor('#D0D9E2')  # 内层：银灰勾边
        self.fill_color = QColor('#E8EDF2')    # 外层：浅蓝填底
        
        self.char_visibility = [0.0] * len(self.text)
        
        self.char_timer = QTimer()
        self.char_timer.timeout.connect(self._update_char_progress)
        self.start_time_ms = 0
    
    def start_animation(self):
        """启动逐字符动画"""
        self.start_time_ms = 0
        self.char_progress = 0
        self.char_visibility = [0.0] * len(self.text)
        self.is_finished = False
        self.char_timer.start(30)
    
    def _update_char_progress(self):
        """更新字符显示进度"""
        elapsed = self.start_time_ms
        self.start_time_ms += 30
        
        # 5秒内逐字符显示
        progress = min(elapsed / 5000.0, 1.0)
        num_chars_to_show = min(int(progress * len(self.text) + 1), len(self.text))
        
        for i in range(len(self.text)):
            if i < num_chars_to_show:
                char_start = i / len(self.text) * 5000
                char_end = (i + 1) / len(self.text) * 5000
                char_progress_val = max(0, min(1.0, (elapsed - char_start) / (char_end - char_start)))
                self.char_visibility[i] = char_progress_val
            else:
                self.char_visibility[i] = 0.0
        
        self.update()
        
        if progress >= 1.0 and not self.is_finished:
            self.is_finished = True
            self.char_timer.stop()
            self.char_finished.emit()
    
    def paintEvent(self, event):
        """绘制丝带+文字"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.setFont(self.font)
        
        metrics = QFontMetrics(self.font)
        text_width = metrics.width(self.text)
        text_height = metrics.height()
        
        # 文字居中
        x_start = (self.width() - text_width) // 2
        y = (self.height() - text_height) // 2 + 20
        
        # 绘制每个字符及其丝带
        x = x_start
        for i, char in enumerate(self.text):
            visibility = self.char_visibility[i]
            
            if visibility > 0:
                char_width = metrics.width(char)
                
                # 绘制丝带环带（内敛贴合）
                self._draw_ribbon_band(painter, x, y - 25, char_width, visibility)
                
                # 绘制丝带上的细闪颗粒
                self._draw_sparkles_on_ribbon(painter, x, y - 25, char_width, visibility)
                
                # 绘制字符
                self._draw_character(painter, char, x, y, visibility)
            
            x += metrics.width(char)
    
    def _draw_ribbon_band(self, painter, x, y, char_width, visibility):
        """绘制双层丝带环带（内敛贴合行星）"""
        ribbon_height = 14
        
        # 外层：蓝色填底（显著的蓝色）
        painter.fillRect(int(x - 4), int(y), int(char_width + 8), ribbon_height,
                        QColor(90, 170, 235, int(255 * visibility)))
        
        # 内层：深银灰勾边
        pen = QPen(QColor(45, 95, 155, int(255 * visibility)))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(int(x - 4), int(y), int(char_width + 8), ribbon_height)
    
    def _draw_sparkles_on_ribbon(self, painter, x, y, char_width, visibility):
        """绘制丝带上的细闪颗粒（±1px浮动）"""
        random.seed(hash(x) % 100)  # 基于位置的一致随机
        
        num_sparkles = max(2, int(visibility * 4))
        
        for _ in range(num_sparkles):
            sparkle_x = x + random.uniform(0, char_width)
            sparkle_y = y + 5 + random.uniform(-1, 1)  # ±1px浮动
            
            # 绘制1px的半透明银色点
            painter.setBrush(QColor(220, 225, 230, int(200 * visibility)))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(int(sparkle_x - 0.5), int(sparkle_y - 0.5), 1, 1)
    
    def _draw_character(self, painter, char, x, y, visibility):
        """绘制单个字符（深银灰勾边+蓝色填底）"""
        path = QPainterPath()
        path.addText(x, y + 35, self.font, char)
        
        # 绘制勾边（深银灰）
        pen = QPen(QColor(45, 95, 155, int(255 * visibility)))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.strokePath(path, pen)
        
        # 绘制填底（蓝色）
        painter.setBrush(QColor(90, 170, 235, int(235 * visibility)))
        painter.setPen(Qt.NoPen)
        painter.fillPath(path, QBrush(QColor(90, 170, 235, int(235 * visibility))))


class LaunchOverlay(QWidget):
    """启动动画主窗口：内敛高级感布局"""
    finished = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        screen = QApplication.primaryScreen()
        self.resize(screen.size())
        
        # 极浅冷灰背景
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor('#F2F4F6'))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        
        # 小行星部件（居中）
        asteroid_diameter = 400
        self.asteroid = AsteroidWidget(self)
        asteroid_x = (self.width() - asteroid_diameter) // 2
        asteroid_y = (self.height() - asteroid_diameter) // 2 - 50  # 稍上移
        self.asteroid.move(asteroid_x, asteroid_y)
        
        # 丝带+文字部件
        self.ribbon_text = RibbonTextWidget(asteroid_diameter, self)
        ribbon_y = asteroid_y - 80
        self.ribbon_text.setGeometry(0, ribbon_y, self.width(), 280)
        self.ribbon_text.char_finished.connect(self._on_text_finished)
        
        # 启动动画
        QTimer.singleShot(100, self._start_animation)
    
    def _start_animation(self):
        """启动主动画"""
        self.ribbon_text.start_animation()
    
    def _on_text_finished(self):
        """文字完成后显示按钮"""
        self._show_buttons()
        
        # 延迟2秒后进入主窗口
        QTimer.singleShot(2000, self._finish)
    
    def _show_buttons(self):
        """显示Sign In/Sign Up按钮"""
        button_width = 200
        button_height = 48
        button_y = self.height() // 2 + 180  # 行星下方30px
        
        # Sign In 按钮（白底+银灰边框）
        sign_in_btn = QPushButton("Sign In", self)
        sign_in_btn.setFont(QFont("SF Pro Rounded", 16, QFont.Bold))
        sign_in_btn.setFixedSize(button_width, button_height)
        sign_in_btn.setCursor(Qt.PointingHandCursor)
        sign_in_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                color: #5B7C99;
                border: 1px solid #D0D9E2;
                border-radius: 20px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #E8EDF2;
            }
        """)
        sign_in_btn.move(self.width() // 2 - button_width - 10, button_y)
        sign_in_btn.clicked.connect(self._finish)
        sign_in_btn.show()
        
        # Sign Up 按钮（透明+银灰边框）
        sign_up_btn = QPushButton("Sign Up", self)
        sign_up_btn.setFont(QFont("SF Pro Rounded", 16, QFont.Bold))
        sign_up_btn.setFixedSize(button_width, button_height)
        sign_up_btn.setCursor(Qt.PointingHandCursor)
        sign_up_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #5B7C99;
                border: 1px solid #D0D9E2;
                border-radius: 20px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #E8EDF2;
            }
        """)
        sign_up_btn.move(self.width() // 2 + 10, button_y)
        sign_up_btn.clicked.connect(self._finish)
        sign_up_btn.show()
        
        # 保存按钮引用
        self.sign_in_btn = sign_in_btn
        self.sign_up_btn = sign_up_btn
    
    def _finish(self):
        """完成动画"""
        self.asteroid.stop_rotation()
        self.finished.emit()
        self.close()
