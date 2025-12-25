# -*- coding: utf-8 -*-
"""PyPalPrep 入口文件"""
import sys
import os
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QFont
from ui.main_window import MainWindow
from ui.launch_overlay_clean_login import LaunchOverlay
from models.user import User


def check_and_init_database():
    """检查数据库是否存在，如果不存在则提示初始化"""
    db_path = 'database/python_learning.db'

    if not os.path.exists(db_path):
        # 数据库不存在，提示用户初始化
        reply = QMessageBox.question(
            None,
            '数据库未初始化',
            '检测到数据库文件不存在。\n\n'
            '这可能是您首次使用本系统，或者您克隆了项目但还没有初始化数据库。\n\n'
            '是否立即初始化数据库？\n\n'
            '（初始化将创建题库、知识点和三套完整的模拟考试）',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )

        if reply == QMessageBox.Yes:
            try:
                # 执行初始化
                init_database()
                QMessageBox.information(
                    None,
                    '初始化成功',
                    '数据库初始化完成！\n\n系统已准备就绪，您现在可以登录使用了。'
                )
                return True
            except Exception as e:
                QMessageBox.critical(
                    None,
                    '初始化失败',
                    f'数据库初始化失败：\n\n{str(e)}\n\n请检查错误信息或联系管理员。'
                )
                return False
        else:
            QMessageBox.warning(
                None,
                '无法继续',
                '没有数据库文件，系统无法正常运行。\n\n程序将退出。'
            )
            return False

    return True  # 数据库已存在


def init_database():
    """执行数据库初始化"""
    import shutil

    db_path = 'database/python_learning.db'

    # 如果有旧数据库，备份
    if os.path.exists(db_path):
        backup_path = db_path + '.backup'
        shutil.copy2(db_path, backup_path)
        os.remove(db_path)

    # 执行 scripts/init_data.py
    project_root = os.path.dirname(os.path.abspath(__file__))
    init_script = os.path.join(project_root, 'scripts', 'init_data.py')

    if os.path.exists(init_script):
        import importlib.util
        spec = importlib.util.spec_from_file_location("init_data", init_script)
        init_data = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(init_data)

        if hasattr(init_data, 'init_knowledge_data'):
            init_data.init_knowledge_data()

        if hasattr(init_data, 'init_question_data'):
            init_data.init_question_data()

    # 执行 clean_duplicates_and_reconfigure.py
    config_script = os.path.join(project_root, 'clean_duplicates_and_reconfigure.py')
    if os.path.exists(config_script):
        import importlib.util
        spec = importlib.util.spec_from_file_location("clean_config", config_script)
        clean_config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(clean_config)

        if hasattr(clean_config, 'clean_and_reconfigure'):
            clean_config.clean_and_reconfigure()


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

    # 检查并初始化数据库
    if not check_and_init_database():
        sys.exit(0)  # 用户取消初始化或初始化失败，退出程序

    overlay = LaunchOverlay()
    overlay.finished.connect(launch_main_window)
    overlay.showFullScreen()

    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
