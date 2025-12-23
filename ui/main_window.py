# -*- coding: utf-8 -*-
"""
主窗口
系统主界面，包含菜单栏、工具栏、状态栏和各功能模块
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QStackedWidget, QListWidget, QListWidgetItem,
                             QMenuBar, QMenu, QAction, QToolBar,
                             QStatusBar, QMessageBox, QLabel, QToolTip, QGraphicsDropShadowEffect, QApplication)
from PyQt5.QtCore import Qt, QTimer, QDateTime, QSize
from PyQt5.QtGui import QColor, QFont, QIcon
from config import WINDOW_CONFIG, THEME_COLORS
from models.user import User
from ui.ai_assistant_widget import FloatingAssistant
from database.db_manager import db_manager


class MainWindow(QMainWindow):
    """主窗口类"""

    def __init__(self, user):
        """
        初始化主窗口
        :param user: 当前登录用户
        """
        super().__init__()
        self.current_user = user
        self.init_ui()

    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle(WINDOW_CONFIG['title'])
        self.setGeometry(100, 100, WINDOW_CONFIG['width'], WINDOW_CONFIG['height'])
        self.setMinimumSize(WINDOW_CONFIG['min_width'], WINDOW_CONFIG['min_height'])
        self.showMaximized()  # 最大化显示，保留系统标题栏和按钮

        # 加载用户背景偏好并应用全局半透明样式
        # 壁纸功能已禁用，使用默认背景
        self.bg_pref = None
        self.apply_background_theme(None)

        # 全局字体整体再放大（+35%），让其他界面文字更清晰
        try:
            app = QApplication.instance()
            if app is not None:
                base_font = app.font()
                ps = base_font.pointSizeF()
                if ps > 0:
                    base_font.setPointSizeF(ps * 1.35)
                else:
                    base_font.setPointSize(14)
                app.setFont(base_font)
        except Exception:
            pass

        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 创建左侧收起导航 + 右侧内容堆栈
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(12, 12, 12, 12)
        content_layout.setSpacing(12)

        # 左侧导航（收起式）
        self.nav_list = QListWidget()
        self.nav_list.setObjectName('navList')
        self.nav_list.setFixedWidth(88)  # 收起宽度更宽一点
        self.nav_list.setSpacing(8)     # 垂直间距更紧凑
        self.nav_list.setContentsMargins(8, 16, 8, 16)  # 适当收紧留白
        self.nav_list.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # 允许垂直滚动
        self.nav_list.setStyleSheet('QListWidget { background: transparent; }')
        self.nav_list.installEventFilter(self)
        content_layout.addWidget(self.nav_list)

        # 右侧内容区使用堆栈切换不同模块
        self.stack = QStackedWidget()
        content_layout.addWidget(self.stack)

        main_layout.addLayout(content_layout)

        # 延迟加载各个功能模块（防止循环导入）
        self.init_modules()

        # 绑定导航切换
        self.nav_list.currentRowChanged.connect(self.on_page_changed)

        # 悬浮式 AI 助手（右下角，可拖动、展开/收起）
        try:
            self.ai_assistant = FloatingAssistant(self)
            self.ai_assistant.raise_()
        except Exception:
            self.ai_assistant = None

    def showEvent(self, event):
        """确保主窗口显示时居中并置顶"""
        super().showEvent(event)
        try:
            self.raise_()
            self.activateWindow()
            if hasattr(self, 'ai_assistant') and self.ai_assistant:
                # 延迟重新定位浮标，确保窗口大小已更新
                QTimer.singleShot(200, lambda: self.ai_assistant.reposition_on_parent_resize())
        except Exception as e:
            print(f"ShowEvent error: {e}")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        try:
            if hasattr(self, 'ai_assistant') and self.ai_assistant:
                self.ai_assistant.reposition_on_parent_resize()
        except Exception:
            pass

    def init_modules(self):
        """初始化各功能模块"""
        # 这里会在后续添加各个功能模块的标签页
        # 暂时添加占位符
        from ui.knowledge_widget import KnowledgeWidget
        from ui.practice_widget import PracticeWidget
        from ui.editor_widget import EditorWidget
        from ui.progress_widget import ProgressWidget
        from ui.mistakes_widget import MistakesWidget
        from ui.statistics_widget import StatisticsWidget
        from ui.profile_widget import ProfileWidget
        from ui.exam_widget import ExamWidget

        # 添加知识点学习模块（不使用图标，只保留文字）
        self.knowledge_widget = KnowledgeWidget(self.current_user)
        self.stack.addWidget(self.knowledge_widget)
        self.nav_list.addItem(QListWidgetItem('知识学习'))

        # 添加题库练习模块
        self.practice_widget = PracticeWidget(self.current_user)
        self.stack.addWidget(self.practice_widget)
        self.nav_list.addItem(QListWidgetItem('题库练习'))

        # 添加模拟考试模块
        self.exam_widget = ExamWidget(self.current_user)
        self.stack.addWidget(self.exam_widget)
        self.nav_list.addItem(QListWidgetItem('模拟考试'))

        # 添加代码编辑器模块
        self.editor_widget = EditorWidget(self.current_user)
        self.stack.addWidget(self.editor_widget)
        self.nav_list.addItem(QListWidgetItem('编辑器'))

        # 添加学习进度模块（将“学习记录”会迁移到个人主页）
        self.progress_widget = ProgressWidget(self.current_user)
        self.stack.addWidget(self.progress_widget)
        self.nav_list.addItem(QListWidgetItem('学习进度'))

        # 添加错题本模块
        self.mistakes_widget = MistakesWidget(self.current_user)
        self.stack.addWidget(self.mistakes_widget)
        self.nav_list.addItem(QListWidgetItem('错题本'))

        # 添加成绩统计模块
        self.statistics_widget = StatisticsWidget(self.current_user)
        self.stack.addWidget(self.statistics_widget)
        self.nav_list.addItem(QListWidgetItem('成绩统计'))

        # 添加个人主页模块（包含学习记录、头像更换、背景自定义）
        self.profile_widget = ProfileWidget(self.current_user)
        self.stack.addWidget(self.profile_widget)
        self.nav_list.addItem(QListWidgetItem('个人主页'))

        # 统一条目高度、对齐与提示，提升“均匀分布”的观感
        # 调整字体（进一步缩小：约 +5%），并将每项高度略增（88 -> 102）
        cur_font = self.nav_list.font()
        ps = cur_font.pointSizeF()
        if ps > 0:
            cur_font.setPointSizeF(ps * 1.05)
        else:
            # 若无法获取点大小，则设置一个合适的字号
            cur_font.setPointSize(12)
        self.nav_list.setFont(cur_font)

        for i in range(self.nav_list.count()):
            item = self.nav_list.item(i)
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setSizeHint(QSize(340, 240))  # 更宽更高,纵向更舒展
            item.setToolTip(item.text())      # 收起时悬停显示完整名称

    def on_page_changed(self, index):
        """页面切换时刷新数据"""
        # 切换到对应页面
        self.stack.setCurrentIndex(index)
        
        # 根据索引刷新对应页面的数据
        # 索引对应：0=知识学习, 1=题库练习, 2=模拟考试, 3=编辑器, 
        #          4=学习进度, 5=错题本, 6=成绩统计, 7=个人主页
        try:
            if index == 0 and hasattr(self, 'knowledge_widget'):
                self.knowledge_widget.refresh()
            elif index == 1 and hasattr(self, 'practice_widget'):
                self.practice_widget.refresh()
            elif index == 2 and hasattr(self, 'exam_widget'):
                self.exam_widget.refresh()
            elif index == 4 and hasattr(self, 'progress_widget'):
                self.progress_widget.refresh()
            elif index == 5 and hasattr(self, 'mistakes_widget'):
                self.mistakes_widget.refresh()
            elif index == 6 and hasattr(self, 'statistics_widget'):
                self.statistics_widget.refresh()
            elif index == 7 and hasattr(self, 'profile_widget'):
                self.profile_widget.refresh()
        except Exception as e:
            print(f'页面刷新出错: {e}')

    def load_background_pref(self):
        """从数据库读取用户的背景偏好（图片路径或纯色color:#xxxxxx）"""
        try:
            db_manager.connect()
            result = db_manager.execute_query('SELECT bg_path FROM users WHERE id = ?', (self.current_user.id,))
            if result:
                return dict(result[0]).get('bg_path')
        except Exception:
            return None
        finally:
            db_manager.disconnect()
        return None

    def apply_background_theme(self, bg_pref=None):
        """根据用户选择应用背景（图片或纯色）并统一半透明卡片"""
        if bg_pref is not None:
            self.bg_pref = bg_pref

        base_bg = THEME_COLORS.get('background', '#F6F7F9')
        background_rule = f"background-color: {base_bg};"

        pref = getattr(self, 'bg_pref', None)
        if pref:
            if isinstance(pref, str) and pref.startswith('color:'):
                color_value = pref.split(':', 1)[1] or base_bg
                background_rule = f"background-color: {color_value};"
            else:
                # 图片背景，保持等比覆盖
                path_norm = pref.replace('\\', '/')
                background_rule = (
                    f"background-color: {base_bg};"
                    f"background-image: url('{path_norm}');"
                    "background-position: center center;"
                    "background-repeat: no-repeat;"
                    "background-attachment: fixed;"
                    "background-size: cover;"
                )

        nav_item_bg = "rgba(255,255,255,0.82)"
        card_bg = "rgba(255,255,255,0.82)"

        style = f"""
            QMainWindow {{
                {background_rule}
                font-family: 'SF Pro Display', 'PingFang SC', 'Microsoft YaHei', 'Segoe UI';
            }}
            /* 中心部件应用相同背景 */
            QMainWindow > QWidget {{
                {background_rule}
            }}
            /* 左侧导航 */
            .leftNav {{
                background-color: transparent;
            }}
            QListWidget#navList {{
                background-color: transparent;
                border: none;
            }}
            QListWidget#navList::item {{
                padding: 16px 30px;
                border-radius: 16px;
                color: {THEME_COLORS['dark']};
                margin: 8px 10px;
                background-color: {nav_item_bg};
                border: 1px solid rgba(0,0,0,0.06);
            }}
            QListWidget#navList::item:selected {{
                background-color: rgba(255,255,255,0.95);
                color: {THEME_COLORS['primary']};
                font-weight: 600;
                border: none;
            }}
            QListWidget#navList::item:hover {{
                background-color: rgba(0,0,0,0.06);
                transform: none;
            }}
            /* 卡片与控件半透明，透出底色 */
            QGroupBox {{
                background-color: {card_bg};
                border-radius: 12px;
                border: none;
            }}
            QLabel#pageTitle {{
                background-color: {card_bg};
                border: none;
                border-radius: 12px;
                padding: 14px 16px;
            }}
            QTableWidget, QListWidget, QTextEdit, QLineEdit, QComboBox, QSpinBox {{
                background-color: rgba(255,255,255,0.85);
                border-radius: 10px;
                border: none;
            }}
            QScrollBar:vertical {{
                width: 12px;
                background-color: transparent;
            }}
            QScrollBar::handle:vertical {{
                background-color: rgba(0,0,0,0.2);
                border-radius: 6px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: rgba(0,0,0,0.3);
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                border: none;
                background: none;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
            QScrollBar:horizontal {{
                height: 12px;
                background-color: transparent;
            }}
            QScrollBar::handle:horizontal {{
                background-color: rgba(0,0,0,0.2);
                border-radius: 6px;
                min-width: 20px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background-color: rgba(0,0,0,0.3);
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                border: none;
                background: none;
            }}
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
                background: none;
            }}
            QPushButton {{
                border-radius: 10px;
                padding: 8px 12px;
            }}
            QPushButton:hover {{
                background-color: rgba(0,0,0,0.03);
            }}
            QPushButton:pressed {{
                transform: scale(0.995);
            }}
        """
        self.setStyleSheet(style)

    def refresh_data(self):
        """初始化菜单栏"""
        menubar = self.menuBar()
        menubar.setFont(QFont('SF Pro Display', 10))

        # 文件菜单
        file_menu = menubar.addMenu('文件')

        refresh_action = QAction('刷新数据', self)
        refresh_action.setShortcut('F5')
        refresh_action.triggered.connect(self.refresh_data)
        file_menu.addAction(refresh_action)

        file_menu.addSeparator()

        exit_action = QAction('退出', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 学习菜单
        study_menu = menubar.addMenu('学习')

        knowledge_action = QAction('知识学习', self)
        knowledge_action.triggered.connect(lambda: self.stack.setCurrentIndex(0))
        study_menu.addAction(knowledge_action)

        practice_action = QAction('题库练习', self)
        practice_action.triggered.connect(lambda: self.stack.setCurrentIndex(1))
        study_menu.addAction(practice_action)

        editor_action = QAction('编辑器', self)
        editor_action.triggered.connect(lambda: self.stack.setCurrentIndex(2))
        study_menu.addAction(editor_action)

        # 统计菜单
        stats_menu = menubar.addMenu('统计')

        progress_action = QAction('学习进度', self)
        progress_action.triggered.connect(lambda: self.stack.setCurrentIndex(3))
        stats_menu.addAction(progress_action)

        mistakes_action = QAction('错题本', self)
        mistakes_action.triggered.connect(lambda: self.stack.setCurrentIndex(4))
        stats_menu.addAction(mistakes_action)

        statistics_action = QAction('成绩统计', self)
        statistics_action.triggered.connect(lambda: self.stack.setCurrentIndex(5))
        stats_menu.addAction(statistics_action)

        # 帮助菜单
        help_menu = menubar.addMenu('帮助')

    def center_window(self):
        """窗口居中显示"""
        from PyQt5.QtWidgets import QDesktopWidget
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(
            int((screen.width() - size.width()) / 2),
            int((screen.height() - size.height()) / 2)
        )

    def refresh_data(self):
        """刷新所有数据"""
        try:
            # 刷新各个模块的数据
            if hasattr(self, 'knowledge_widget'):
                self.knowledge_widget.refresh()
            if hasattr(self, 'practice_widget'):
                self.practice_widget.refresh()
            if hasattr(self, 'progress_widget'):
                self.progress_widget.refresh()
            if hasattr(self, 'mistakes_widget'):
                self.mistakes_widget.refresh()
            if hasattr(self, 'statistics_widget'):
                self.statistics_widget.refresh()

            QMessageBox.information(self, '提示', '数据刷新成功！')
        except Exception as e:
            QMessageBox.warning(self, '警告', f'数据刷新失败: {str(e)}')

    def eventFilter(self, source, event):
        """处理左侧导航的悬停展开/收起行为"""
        from PyQt5.QtCore import QEvent, QPropertyAnimation, QEasingCurve
        if source == self.nav_list:
            if event.type() == QEvent.Enter:
                # 使用动画展开导航
                anim = QPropertyAnimation(self.nav_list, b"minimumWidth")
                anim.setDuration(180)
                anim.setStartValue(self.nav_list.width())
                anim.setEndValue(600)  # 再加宽，格子更舒展
                anim.setEasingCurve(QEasingCurve.OutCubic)
                anim.start()
                # keep reference to avoid GC
                self._nav_anim = anim

                # 展开时添加柔和灰色外阴影（0, 4px, 12px, rgba(0,0,0,0.12)）
                try:
                    shadow = QGraphicsDropShadowEffect(self.nav_list)
                    shadow.setOffset(0, 4)
                    shadow.setBlurRadius(24)  # 近似 12px 的柔化
                    shadow.setColor(QColor(0, 0, 0, int(255 * 0.12)))
                    self.nav_list.setGraphicsEffect(shadow)
                    self._nav_shadow = shadow
                except Exception:
                    pass
            elif event.type() == QEvent.Leave:
                anim = QPropertyAnimation(self.nav_list, b"minimumWidth")
                anim.setDuration(160)
                anim.setStartValue(self.nav_list.width())
                anim.setEndValue(88)  # 收回宽度与收起保持一致
                anim.setEasingCurve(QEasingCurve.InCubic)
                anim.start()
                self._nav_anim = anim

                # 收回时显示提示气泡：提示“悬停展开”
                try:
                    global_pos = self.nav_list.mapToGlobal(self.nav_list.rect().center())
                    QToolTip.showText(global_pos, '悬停展开', self.nav_list)
                except Exception:
                    pass

                # 收起时移除阴影
                try:
                    self.nav_list.setGraphicsEffect(None)
                    self._nav_shadow = None
                except Exception:
                    pass
        return super().eventFilter(source, event)

    def show_about(self):
        """显示关于对话框"""
        about_text = '''
        <h2>Python学习教辅系统</h2>
        <p><b>版本:</b> 1.0.0</p>
        <p><b>基于:</b> Python计算机二级考试大纲</p>
        <p><b>功能特点:</b></p>
        <ul>
            <li>📚 系统的Python知识点学习</li>
            <li>✍️ 丰富的题库练习（选择、判断、填空、编程）</li>
            <li>💻 内置代码编辑器和执行环境</li>
            <li>📊 学习进度可视化跟踪</li>
            <li>📝 智能错题本管理</li>
            <li>📈 详细的成绩统计分析</li>
        </ul>
        <p><b>技术栈:</b> Python 3.x + PyQt5 + SQLite</p>
        <p><b>© 2025 版权所有</b></p>
        '''
        QMessageBox.about(self, '关于', about_text)

    def closeEvent(self, event):
        """窗口关闭事件"""
        reply = QMessageBox.question(
            self, '确认退出',
            '确定要退出Python学习教辅系统吗？',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
