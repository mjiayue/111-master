# -*- coding: utf-8 -*-
"""
代码执行器
用于安全执行用户输入的Python代码
"""
import sys
import io
import contextlib
import signal
from threading import Thread
import queue


class CodeExecutor:
    """代码执行器类"""

    def __init__(self, timeout=5):
        """
        初始化代码执行器
        :param timeout: 超时时间（秒）
        """
        self.timeout = timeout

    def execute(self, code):
        """
        执行Python代码
        :param code: 要执行的代码字符串
        :return: (是否成功, 输出内容, 错误信息)
        """
        if not code or not code.strip():
            return False, '', '代码不能为空'

        # 创建捕获输出的StringIO对象
        output_buffer = io.StringIO()
        error_buffer = io.StringIO()

        # 使用队列在线程间传递结果
        result_queue = queue.Queue()

        def run_code():
            """在单独线程中运行代码"""
            try:
                # 重定向标准输出和标准错误
                with contextlib.redirect_stdout(output_buffer), contextlib.redirect_stderr(error_buffer):
                    # 创建执行环境
                    exec_globals = {
                        '__builtins__': __builtins__,
                        # 可以添加一些安全的内置函数
                    }
                    exec_locals = {}

                    # 执行代码
                    exec(code, exec_globals, exec_locals)

                # 获取输出
                output = output_buffer.getvalue()
                error = error_buffer.getvalue()

                if error:
                    result_queue.put((False, output, error))
                else:
                    result_queue.put((True, output, ''))

            except Exception as e:
                error_msg = f'{type(e).__name__}: {str(e)}'
                result_queue.put((False, output_buffer.getvalue(), error_msg))

        # 创建并启动执行线程
        exec_thread = Thread(target=run_code)
        exec_thread.daemon = True
        exec_thread.start()

        # 等待执行完成或超时
        exec_thread.join(timeout=self.timeout)

        if exec_thread.is_alive():
            # 执行超时
            return False, '', f'代码执行超时（超过{self.timeout}秒）'

        # 获取执行结果
        try:
            success, output, error = result_queue.get_nowait()
            return success, output, error
        except queue.Empty:
            return False, '', '执行出现未知错误'

    def validate_code(self, code):
        """
        验证代码语法
        :param code: 要验证的代码
        :return: (是否有效, 错误信息)
        """
        if not code or not code.strip():
            return False, '代码不能为空'

        try:
            compile(code, '<string>', 'exec')
            return True, ''
        except SyntaxError as e:
            return False, f'语法错误（第{e.lineno}行）: {e.msg}'
        except Exception as e:
            return False, f'编译错误: {str(e)}'
