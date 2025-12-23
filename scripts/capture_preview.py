# -*- coding: utf-8 -*-
"""
启动遮罩截屏脚本：运行启动动效并在合适时机截取全屏保存到 screenshots/preview.png
"""
import sys
import os
import pathlib
# ensure project root in sys.path
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from ui.launch_overlay_morph import LaunchOverlay

if __name__ == '__main__':
    app = QApplication(sys.argv)
    overlay = LaunchOverlay()
    overlay.start()

    # 在动画消散后等待 200ms，再截屏
    def take_and_exit():
        screen = app.primaryScreen()
        pix = screen.grabWindow(0)
        out_dir = os.path.join(os.path.dirname(__file__), '..', 'screenshots')
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, 'preview.png')
        pix.save(out_path, 'png')
        print('Saved preview to', out_path)
        sys.exit(0)

    # LaunchOverlay 动画大约 1500 + 800 = 2300ms，延时 2400ms 以确保完全结束
    QTimer.singleShot(2400, take_and_exit)
    sys.exit(app.exec_())
