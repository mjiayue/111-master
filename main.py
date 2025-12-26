# -*- coding: utf-8 -*-
"""PyPalPrep 入口文件"""
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from ui.main_window import MainWindow
from ui.launch_overlay_clean_login import LaunchOverlay
from models.user import User


def create_app():
    """创建并配置 QApplication 实例"""
    app = QApplication(sys.argv)
    font = QFont()
    font.setFamily("SF Pro Display, PingFang SC, Segoe UI, Microsoft YaHei")
    font.setPointSize(10)
    app.setFont(font)
    app.setApplicationName("Python学习教辅系统")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Python Learning Assistant")
    return app


def launch_main_window(username: str, password: str):
    """登录完成后启动主窗口（此处仍使用简化的默认用户）"""
    app = QApplication.instance()
    if app is None:
        raise RuntimeError("QApplication 未初始化")

    user = User(user_id=1, username=username, nickname=username)
    main_window = MainWindow(user)
    app._main_window = main_window
    main_window.show()
    main_window.raise_()
    main_window.activateWindow()


def run():
    """启动应用"""
    app = create_app()

    overlay = LaunchOverlay()
    overlay.finished.connect(launch_main_window)
    overlay.showFullScreen()

    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
