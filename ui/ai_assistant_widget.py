# -*- coding: utf-8 -*-
"""
悬浮式 AI 助手模块（计算机二级 Python 专用）
- 默认圆形悬浮按钮，点击 0.3s 展开/收起
- iOS 极简风格配色与动效
- 内置考点/真题/代码解释导览与问答守则
- 接入 DeepSeek API 提供智能问答服务
"""
import json
import requests
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, QPoint, QSize, QTimer, QEvent, QThread, pyqtSignal
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QFrame, QVBoxLayout, QHBoxLayout, QLabel,
    QTextBrowser, QTextEdit, QSizePolicy, QGraphicsDropShadowEffect, QMessageBox
)


class DeepSeekThread(QThread):
    """DeepSeek API 调用线程"""
    response_received = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    loading_state = pyqtSignal(bool)

    def __init__(self, messages, api_key):
        super().__init__()
        self.messages = messages
        self.api_key = api_key

    def run(self):
        """执行网络请求"""
        try:
            # DeepSeek API 配置
            url = "https://api.deepseek.com/v1/chat/completions"

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            # 构建系统提示词，限制在计算机二级Python范围内
            system_prompt = {
                "role": "system",
                "content": """你是一个专业的计算机二级Python教学助手，专门解答Python相关问题。
                请专注于以下范围：
                1. Python基础语法和数据类型
                2. 列表、字典、元组、集合操作
                3. 流程控制（if、for、while）
                4. 函数定义与调用
                5. 文件操作（读写、编码）
                6. 异常处理
                7. 常用内置模块（random、datetime、math等）
                8. 简单的算法和数据处理
                
                如果问题超出二级Python范围，请礼貌地引导回相关知识点。
                回答要简洁、准确、易懂，适合初学者理解。
                格式要求：使用Markdown语法，适当使用代码块示例。"""
            }

            # 将系统提示词添加到消息开头
            all_messages = [system_prompt] + self.messages

            data = {
                "model": "deepseek-chat",
                "messages": all_messages,
                "temperature": 0.7,
                "max_tokens": 2000,
                "stream": False
            }

            self.loading_state.emit(True)
            response = requests.post(url, headers=headers, json=data, timeout=30)

            if response.status_code == 200:
                result = response.json()
                if "choices" in result and len(result["choices"]) > 0:
                    content = result["choices"][0]["message"]["content"]
                    self.response_received.emit(content)
                else:
                    self.error_occurred.emit("API返回格式错误")
            else:
                error_msg = f"API请求失败: {response.status_code}\n"
                try:
                    error_detail = response.json().get("error", {}).get("message", "未知错误")
                    error_msg += error_detail
                except:
                    error_msg += response.text[:100]
                self.error_occurred.emit(error_msg)

        except requests.exceptions.Timeout:
            self.error_occurred.emit("请求超时，请检查网络连接")
        except requests.exceptions.ConnectionError:
            self.error_occurred.emit("网络连接失败，请检查网络")
        except requests.exceptions.RequestException as e:
            self.error_occurred.emit(f"请求异常: {str(e)}")
        except Exception as e:
            self.error_occurred.emit(f"未知错误: {str(e)}")
        finally:
            self.loading_state.emit(False)


class FloatingAssistant(QWidget):
    BUTTON_SIZE = 100
    PANEL_WIDTH = 900
    PANEL_HEIGHT = 1000
    EDGE_MARGIN = 18
    ANIM_MS = 300

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.SubWindow)
        self.setMouseTracking(True)

        # 获取用户信息
        self.user = getattr(parent, 'user', None) if parent else None
        self.user_avatar_path = None
        if self.user and hasattr(self.user, 'avatar_path'):
            self.user_avatar_path = self.user.avatar_path

        # DeepSeek API 配置
        self.api_key = "sk-ea90d96bf2b141b0b0dbaab768d9bcde"  # 你的API密钥
        self.conversation_history = []  # 对话历史
        self.max_history = 10  # 最大历史记录数

        self.expanded = False
        self.user_dragged = False
        self.drag_offset = None
        self.anchor_pos = None  # 记录右下角锚点，便于展开/收起定位

        self._loading_frames = ["⠁", "⠃", "⠇", "⠧", "⠷", "⠿", "⠿", "⠷", "⠧", "⠇", "⠃"]
        self._loading_index = 0
        self._loading_timer = QTimer(self)
        self._loading_timer.timeout.connect(self._tick_loading)

        self.deepseek_thread = None  # DeepSeek 线程实例

        self._build_ui()
        self._apply_palette()

        self.resize(self.BUTTON_SIZE, self.BUTTON_SIZE)
        self._place_bottom_right()
        self.raise_()

    def _build_ui(self):
        self.main_button = QPushButton("P", self)
        self.main_button.setObjectName("mainBtn")
        self.main_button.setFixedSize(self.BUTTON_SIZE, self.BUTTON_SIZE)
        self.main_button.setToolTip("PyPalPrep")
        self.main_button.setCursor(Qt.OpenHandCursor)
        self.main_button.installEventFilter(self)
        self.main_button.clicked.connect(self.toggle)

        self.panel = QFrame(self)
        self.panel.setFixedSize(self.PANEL_WIDTH, self.PANEL_HEIGHT)
        self.panel.setVisible(False)
        self.panel_layout = QVBoxLayout(self.panel)
        self.panel_layout.setContentsMargins(0, 0, 0, 0)
        self.panel_layout.setSpacing(0)

        # ===== 顶部栏 =====
        header = QHBoxLayout()
        header.setContentsMargins(16, 12, 16, 12)
        header.setSpacing(10)

        back_btn = QPushButton("←")
        back_btn.setFixedSize(40, 40)
        back_btn.setFont(QFont("SF Pro Display", 20, QFont.Bold))
        back_btn.clicked.connect(self.toggle)
        back_btn.setObjectName("backBtn")

        title = QLabel("PyPalPrep")
        title.setFont(QFont("SF Pro Display", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        # 添加清除历史按钮
        clear_btn = QPushButton("🗑")
        clear_btn.setFixedSize(40, 40)
        clear_btn.setFont(QFont("Arial", 18))
        clear_btn.setToolTip("清除对话历史")
        clear_btn.clicked.connect(self._clear_conversation)
        clear_btn.setObjectName("clearBtn")

        header.addWidget(back_btn)
        header.addStretch()
        header.addWidget(title)
        header.addStretch()
        header.addWidget(clear_btn)

        header_frame = QFrame()
        header_frame.setLayout(header)
        header_frame.setStyleSheet("background-color: #FAFAFA; border-bottom: 1px solid #E0E0E0;")
        header_frame.setMaximumHeight(75)
        self.panel_layout.addWidget(header_frame)

        # ===== 聊天区（可滚动）=====
        self.response_view = QTextBrowser()
        self.response_view.setObjectName("responseView")
        self.response_view.setOpenExternalLinks(True)  # 允许打开链接
        self.response_view.setStyleSheet("QTextBrowser { border: none; background-color: #FFFFFF; }")
        self.response_view.setPlaceholderText("开始聊天...")
        self.response_view.setReadOnly(True)
        self.panel_layout.addWidget(self.response_view, 1)

        # ===== 加载指示 =====
        self.loading_label = QLabel("")
        self.loading_label.setObjectName("loadingLabel")
        self.loading_label.setVisible(False)
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.panel_layout.addWidget(self.loading_label)

        # ===== 输入区（固定底部）=====
        input_frame = QFrame()
        input_frame.setStyleSheet("background-color: #FAFAFA; border-top: 1px solid #E0E0E0;")
        input_frame.setMaximumHeight(90)
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(12, 12, 12, 12)
        input_layout.setSpacing(10)

        # 回形针图标（上传）
        attach_btn = QPushButton("📎")
        attach_btn.setFixedSize(44, 44)
        attach_btn.setFont(QFont("Arial", 20))
        attach_btn.setObjectName("attachBtn")
        attach_btn.clicked.connect(self._show_quick_questions)
        input_layout.addWidget(attach_btn)

        # 输入框
        self.input_box = QTextEdit()
        self.input_box.setPlaceholderText("输入二级Python问题/代码...")
        self.input_box.setFixedHeight(55)
        self.input_box.setObjectName("inputBox")
        self.input_box.installEventFilter(self)  # 安装事件过滤器，支持Enter快捷键
        input_layout.addWidget(self.input_box)

        # 发送按钮（圆形黄色）
        self.send_btn = QPushButton("✈")
        self.send_btn.setFixedSize(54, 54)
        self.send_btn.setFont(QFont("Arial", 26))
        self.send_btn.clicked.connect(self._on_send)
        self.send_btn.setObjectName("sendBtn")
        input_layout.addWidget(self.send_btn)

        self.panel_layout.addWidget(input_frame)

    def _apply_palette(self):
        soft_blue = "#F2F2F2"     # 浅灰
        softer_blue = "#F7F7F7"   # 更浅的灰
        border_blue = "#E0E0E0"   # 浅灰色描边
        text_dark = "#333"

        self.setStyleSheet(f"""
            QWidget {{ font-family: 'SF Pro Display', 'PingFang SC', 'Microsoft YaHei', 'Segoe UI'; color: {text_dark}; }}
            QPushButton {{
                background: {soft_blue};
                border: 1px solid {border_blue};
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 18px;
            }}
            QPushButton#mainBtn {{ 
                font-size: 44px; 
                font-weight: bold; 
                color: #999; 
                border-radius: 50px; 
                background: #FFD700;
                border: none;
            }}
            QPushButton#mainBtn:hover {{ background: #FFC700; }}
            QPushButton#backBtn {{ border: none; background: transparent; font-size: 20px; }}
            QPushButton#clearBtn {{ border: none; background: transparent; font-size: 18px; }}
            QPushButton#clearBtn:hover {{ color: #FF4444; }}
            QPushButton#attachBtn {{ border: none; background: transparent; font-size: 18px; }}
            QPushButton#sendBtn {{ 
                background-color: #FFD700; 
                border: none; 
                border-radius: 25px; 
                color: #000;
                font-weight: bold;
            }}
            QPushButton#sendBtn:hover {{ background-color: #FFC700; }}
            QPushButton#sendBtn:pressed {{ background-color: #FFB700; }}
            QPushButton#sendBtn:disabled {{ background-color: #E0E0E0; color: #999; }}
            QPushButton:hover {{ background: {softer_blue}; }}
            QPushButton:pressed {{ transform: scale(0.98); }}
            QFrame {{ background: #FAFAFA; border-radius: 16px; border: 1px solid {border_blue}; }}
            QTextBrowser#responseView {{ 
                background: white; 
                border-radius: 0px; 
                padding: 12px; 
                border: none; 
                font-size: 20px; 
                line-height: 1.6;
            }}
            QTextEdit#inputBox {{ 
                background: white; 
                border-radius: 8px; 
                border: 1px solid {border_blue}; 
                font-size: 18px; 
                padding: 8px;
            }}
            QLabel#loadingLabel {{ color: #666; font-size: 17px; }}
        """)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setOffset(0, 6)
        shadow.setBlurRadius(22)
        shadow.setColor(QColor(0, 0, 0, 40))
        self.main_button.setGraphicsEffect(shadow)

    def toggle(self):
        self.raise_()
        self.expanded = not self.expanded
        self.panel.setVisible(True)
        start_rect = self.geometry()
        end_rect = self._target_geometry(expanded=self.expanded)

        anim = QPropertyAnimation(self, b"geometry", self)
        anim.setDuration(self.ANIM_MS)
        anim.setStartValue(start_rect)
        anim.setEndValue(end_rect)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.finished.connect(lambda: self._on_anim_finished(self.expanded))
        anim.stateChanged.connect(lambda _, __: self._sync_children_geometry())
        anim.start()
        self._anim = anim  # 保留引用避免被回收

    def _on_anim_finished(self, expanded):
        if not expanded:
            self.panel.setVisible(False)
        self._sync_children_geometry()

    def _target_geometry(self, expanded):
        if self.anchor_pos is None:
            self._place_bottom_right()
        anchor = self.anchor_pos
        if expanded:
            size = QSize(self.PANEL_WIDTH, self.PANEL_HEIGHT)
        else:
            size = QSize(self.BUTTON_SIZE, self.BUTTON_SIZE)
        top_left = QPoint(anchor.x() - size.width(), anchor.y() - size.height())
        if self.parent():
            parent_rect = self.parent().rect()
            max_x = parent_rect.width() - size.width()
            max_y = parent_rect.height() - size.height()
            top_left.setX(max(0, min(top_left.x(), max_x)))
            top_left.setY(max(0, min(top_left.y(), max_y)))
        return QRect(top_left, size)

    def _place_bottom_right(self):
        if self.parent():
            parent_rect = self.parent().rect()
            w = parent_rect.width() if parent_rect.width() > 0 else 1200
            h = parent_rect.height() if parent_rect.height() > 0 else 800
            anchor = QPoint(w - self.EDGE_MARGIN, h - self.EDGE_MARGIN)
        else:
            anchor = QPoint(self.PANEL_WIDTH + self.EDGE_MARGIN, self.PANEL_HEIGHT + self.EDGE_MARGIN)
        self.anchor_pos = anchor
        self.setGeometry(self._target_geometry(expanded=False))
        self.show()
        self._sync_children_geometry()

    def _sync_children_geometry(self):
        btn_x = self.width() - self.BUTTON_SIZE
        btn_y = self.height() - self.BUTTON_SIZE
        self.main_button.setGeometry(btn_x, btn_y, self.BUTTON_SIZE, self.BUTTON_SIZE)
        self.main_button.setStyleSheet(self.main_button.styleSheet() + f"border-radius: {self.BUTTON_SIZE // 2}px;")
        self.panel.setGeometry(0, 0, self.PANEL_WIDTH, self.PANEL_HEIGHT)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._sync_children_geometry()
        self.anchor_pos = self.geometry().bottomRight()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_offset = event.pos()
            self.user_dragged = True
            self._loading_timer.stop()
            event.accept()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.drag_offset is not None and event.buttons() & Qt.LeftButton:
            if self.parent():
                new_pos = self.parent().mapFromGlobal(event.globalPos() - self.drag_offset)
                new_pos.setX(max(0, min(new_pos.x(), self.parent().width() - self.width())))
                new_pos.setY(max(0, min(new_pos.y(), self.parent().height() - self.height())))
                self.move(new_pos)
                self.anchor_pos = self.geometry().bottomRight()
            event.accept()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.drag_offset = None
        super().mouseReleaseEvent(event)

    def eventFilter(self, obj, event):
        # 处理输入框的Enter快捷键
        if obj == self.input_box:
            if event.type() == QEvent.KeyPress:
                if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                    # Shift+Enter = 换行（不拦截，允许默认行为）
                    if event.modifiers() & Qt.ShiftModifier:
                        return False  # 允许换行
                    # 单独Enter = 发送消息
                    else:
                        self._on_send()
                        return True  # 拦截事件，不换行

        # 处理主按钮的拖拽
        if obj == self.main_button:
            if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
                self.main_button.setCursor(Qt.ClosedHandCursor)
                self.drag_offset = event.globalPos() - self.frameGeometry().topLeft()
                return False
            if event.type() == QEvent.MouseMove and event.buttons() & Qt.LeftButton and self.drag_offset is not None:
                new_pos = event.globalPos() - self.drag_offset
                if self.parent():
                    max_x = self.parent().width() - self.width()
                    max_y = self.parent().height() - self.height()
                    new_x = max(0, min(new_pos.x(), max_x))
                    new_y = max(0, min(new_pos.y(), max_y))
                    self.move(new_x, new_y)
                    self.anchor_pos = self.geometry().bottomRight()
                else:
                    self.move(new_pos)
                return True
            if event.type() == QEvent.MouseButtonRelease:
                self.main_button.setCursor(Qt.OpenHandCursor)
                self.drag_offset = None
                return False
        return super().eventFilter(obj, event)

    def _show_quick_questions(self):
        """显示快速问题模板"""
        quick_questions = [
            "解释Python中的列表和元组的区别",
            "如何在Python中读写文件？",
            "解释try-except异常处理机制",
            "Python函数的参数类型有哪些？",
            "解释for循环和while循环的区别",
            "什么是列表推导式？举个例子",
            "Python中如何导入和使用模块？",
            "解释字符串的常用操作方法",
            "什么是字典？如何遍历字典？",
            "Python中的lambda函数是什么？"
        ]

        menu_text = "<b>快速提问模板：</b><br><br>"
        for i, question in enumerate(quick_questions, 1):
            menu_text += f"{i}. {question}<br>"
        menu_text += "<br>点击上方问题可直接提问"

        self._append_chat("assistant", menu_text)

    def _on_send(self):
        text = self.input_box.toPlainText().strip()
        if not text:
            self._append_chat("assistant", "请输入问题或代码，我会为你解答计算机二级Python相关问题。")
            return

        # 禁用发送按钮防止重复发送
        self.send_btn.setEnabled(False)

        # 显示用户消息
        self._append_chat("user", text)
        self.input_box.clear()

        # 开始加载动画
        self._set_loading(True)

        # 添加到对话历史
        self.conversation_history.append({"role": "user", "content": text})

        # 限制历史长度
        if len(self.conversation_history) > self.max_history * 2:  # 乘以2因为包含user和assistant
            self.conversation_history = self.conversation_history[-self.max_history * 2:]

        # 创建并启动DeepSeek线程
        self.deepseek_thread = DeepSeekThread(self.conversation_history, self.api_key)
        self.deepseek_thread.response_received.connect(self._handle_deepseek_response)
        self.deepseek_thread.error_occurred.connect(self._handle_deepseek_error)
        self.deepseek_thread.loading_state.connect(self._set_loading)
        self.deepseek_thread.finished.connect(lambda: self.send_btn.setEnabled(True))
        self.deepseek_thread.start()

    def _handle_deepseek_response(self, response):
        """处理DeepSeek API返回的响应"""
        # 添加到对话历史
        self.conversation_history.append({"role": "assistant", "content": response})

        # 显示AI回复
        self._append_chat("assistant", response)

    def _handle_deepseek_error(self, error_msg):
        """处理API错误"""
        error_html = f"<span style='color: #FF4444;'>⚠️ {error_msg}</span><br><br>"
        error_html += "建议：<br>"
        error_html += "1. 检查网络连接<br>"
        error_html += "2. 确认API密钥有效<br>"
        error_html += "3. 稍后重试或联系管理员"

        self._append_chat("assistant", error_html)

        # 如果是API密钥问题，显示提示
        if "401" in error_msg or "authentication" in error_msg.lower():
            QMessageBox.warning(self, "API密钥错误",
                                "请检查API密钥是否正确有效。\n"
                                "如果需要新的API密钥，请访问: https://platform.deepseek.com/api_keys")

    def _clear_conversation(self):
        """清除对话历史"""
        self.conversation_history = []
        self.response_view.clear()
        self._append_chat("assistant", "对话历史已清除。请问我任何计算机二级Python相关问题！")

    def _set_loading(self, loading):
        if loading:
            self.loading_label.setVisible(True)
            self.loading_label.setText("思考中～ ⠁")
            self._loading_index = 0
            self._loading_timer.start(90)
        else:
            self.loading_label.setVisible(False)
            self._loading_timer.stop()
            self.send_btn.setEnabled(True)  # 重新启用发送按钮

    def _tick_loading(self):
        self._loading_index = (self._loading_index + 1) % len(self._loading_frames)
        self.loading_label.setText(f"思考中～ {self._loading_frames[self._loading_index]}")

    def _append_chat(self, role, body_html):
        if role == "user":
            # 右边用户气泡
            if self.user_avatar_path:
                avatar_html = f"<img src='{self.user_avatar_path}' style='width:50px; height:50px; border-radius:50%; object-fit:cover;' />"
            else:
                avatar_html = "<div style='width:50px; height:50px; background:#EDEDED; border-radius:50%; display:flex; align-items:center; justify-content:center; color:#999; font-size:26px;'>👤</div>"

            bubble = (
                f"<table width='100%' style='margin:12px 0;'><tr><td width='100%'></td>"
                f"<td style='vertical-align:bottom; padding-left:10px;'>{avatar_html}</td></tr>"
                f"<tr><td colspan='2' style='text-align:right;'>"
                f"<div style='display:inline-block; max-width:70%; background:#FFD700; color:#111; padding:14px 18px; "
                f"border-radius:15px 15px 4px 15px; border:none; font-size:21px; line-height:1.7; word-wrap: break-word;'>"
                f"{body_html}</div></td></tr></table>"
            )
        else:
            # 左边AI气泡
            avatar_html = "<div style='width:50px; height:50px; background:#4A90E2; border-radius:50%; display:flex; align-items:center; justify-content:center; color:white; font-size:26px; font-weight:bold;'>AI</div>"

            # 改进的Markdown格式处理
            formatted_content = self._markdown_to_html(body_html)

            bubble = (
                f"<table width='100%' style='margin:12px 0;'><tr>"
                f"<td style='vertical-align:bottom; padding-right:10px;'>{avatar_html}</td>"
                f"<td width='100%'></td></tr>"
                f"<tr><td colspan='2' style='text-align:left;'>"
                f"<div style='display:inline-block; max-width:70%; background:#F5F5F5; color:#111; padding:14px 18px; "
                f"border-radius:15px 15px 15px 4px; border:1px solid #E0E0E0; font-size:21px; line-height:1.7; word-wrap: break-word;'>"
                f"{formatted_content}</div></td></tr></table>"
            )

        self.response_view.append(bubble)
        self.response_view.verticalScrollBar().setValue(self.response_view.verticalScrollBar().maximum())

    def _markdown_to_html(self, markdown_text):
        """将Markdown格式转换为HTML"""
        import re

        html = markdown_text

        # 1. 处理代码块（三个反引号）
        # 匹配 ```python ... ``` 或 ``` ... ```
        def replace_code_block(match):
            lang = match.group(1) if match.group(1) else ""
            code = match.group(2)
            # 转义HTML特殊字符
            code = code.replace('<', '&lt;').replace('>', '&gt;')
            return f"<pre style='background:#F5F5F5; padding:10px; margin:8px 0; border-radius:5px; border:1px solid #E0E0E0; overflow-x:auto;'><code>{code}</code></pre>"

        html = re.sub(r'```(\w*)\n(.*?)\n```', replace_code_block, html, flags=re.DOTALL)

        # 2. 处理行内代码（单个反引号）
        html = re.sub(r'`([^`]+)`', r'<code style="background:#F0F0F0; padding:2px 6px; border-radius:3px; font-family:Consolas,monospace;">\1</code>', html)

        # 3. 处理粗体 **text** 或 __text__
        html = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', html)
        html = re.sub(r'__(.+?)__', r'<b>\1</b>', html)

        # 4. 处理斜体 *text* 或 _text_ （注意不要匹配已经处理过的粗体）
        html = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<i>\1</i>', html)
        html = re.sub(r'(?<!_)_(?!_)(.+?)(?<!_)_(?!_)', r'<i>\1</i>', html)

        # 5. 处理标题 # 到 ######
        html = re.sub(r'^######\s+(.+)$', r'<h6 style="margin:10px 0 5px 0;">\1</h6>', html, flags=re.MULTILINE)
        html = re.sub(r'^#####\s+(.+)$', r'<h5 style="margin:10px 0 5px 0;">\1</h5>', html, flags=re.MULTILINE)
        html = re.sub(r'^####\s+(.+)$', r'<h4 style="margin:12px 0 6px 0;">\1</h4>', html, flags=re.MULTILINE)
        html = re.sub(r'^###\s+(.+)$', r'<h3 style="margin:14px 0 7px 0;">\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^##\s+(.+)$', r'<h2 style="margin:16px 0 8px 0;">\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^#\s+(.+)$', r'<h1 style="margin:18px 0 9px 0;">\1</h1>', html, flags=re.MULTILINE)

        # 6. 处理无序列表 - 或 * 开头
        lines = html.split('\n')
        in_list = False
        result_lines = []

        for line in lines:
            stripped = line.strip()
            if stripped.startswith('- ') or stripped.startswith('* '):
                if not in_list:
                    result_lines.append('<ul style="margin:8px 0; padding-left:25px;">')
                    in_list = True
                content = stripped[2:]  # 去掉 "- " 或 "* "
                result_lines.append(f'<li style="margin:3px 0;">{content}</li>')
            else:
                if in_list:
                    result_lines.append('</ul>')
                    in_list = False
                result_lines.append(line)

        if in_list:
            result_lines.append('</ul>')

        html = '\n'.join(result_lines)

        # 7. 处理有序列表 1. 2. 3. 开头
        lines = html.split('\n')
        in_ol = False
        result_lines = []

        for line in lines:
            stripped = line.strip()
            if re.match(r'^\d+\.\s+', stripped):
                if not in_ol:
                    result_lines.append('<ol style="margin:8px 0; padding-left:25px;">')
                    in_ol = True
                content = re.sub(r'^\d+\.\s+', '', stripped)
                result_lines.append(f'<li style="margin:3px 0;">{content}</li>')
            else:
                if in_ol:
                    result_lines.append('</ol>')
                    in_ol = False
                result_lines.append(line)

        if in_ol:
            result_lines.append('</ol>')

        html = '\n'.join(result_lines)

        # 8. 处理换行（普通换行转为<br>）
        html = html.replace('\n', '<br>')

        # 9. 处理链接 [text](url)
        html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" style="color:#2196F3; text-decoration:none;">\1</a>', html)

        return html

    def ensure_inside_parent(self):
        if not self.parent():
            return
        parent_rect = self.parent().rect()
        geo = self.geometry()
        new_x = min(max(0, geo.x()), max(0, parent_rect.width() - geo.width()))
        new_y = min(max(0, geo.y()), max(0, parent_rect.height() - geo.height()))
        self.setGeometry(new_x, new_y, geo.width(), geo.height())
        self.anchor_pos = self.geometry().bottomRight()

    def reposition_on_parent_resize(self):
        if not self.user_dragged:
            self._place_bottom_right()
        else:
            self.ensure_inside_parent()

    def closeEvent(self, event):
        """关闭窗口时确保线程结束"""
        if self.deepseek_thread and self.deepseek_thread.isRunning():
            self.deepseek_thread.quit()
            self.deepseek_thread.wait()
        super().closeEvent(event)