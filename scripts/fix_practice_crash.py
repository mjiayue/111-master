# -*- coding: utf-8 -*-
"""
修复practice_widget.py中的崩溃问题
添加错误处理和调试信息
"""

def fix_practice_widget():
    file_path = "ui/practice_widget.py"

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 修改load_questions方法，添加错误处理
    old_code = """    def load_questions(self):
        \"\"\"加载题目\"\"\"
        category = self.category_combo.currentText()
        q_type = self.type_combo.currentData()
        only_new = self.only_new_checkbox.isChecked()

        db_manager.connect()

        # 构建基础查询和排除已做题目的子查询
        exclude_done = ""
        params = []

        if only_new:
            # 排除已做题目
            exclude_done = " AND id NOT IN (SELECT question_id FROM practice_records WHERE user_id = ?)"
            params.append(self.current_user.id)

        if category == '全部' and not q_type:
            query = f"SELECT * FROM questions WHERE 1=1{exclude_done} ORDER BY RANDOM()"
            results = db_manager.execute_query(query, tuple(params))
        elif category == '全部':
            query = f"SELECT * FROM questions WHERE type = ?{exclude_done} ORDER BY RANDOM()"
            params.insert(0, q_type)
            results = db_manager.execute_query(query, tuple(params))
        elif not q_type:
            query = f"SELECT * FROM questions WHERE category = ?{exclude_done} ORDER BY RANDOM()"
            params.insert(0, category)
            results = db_manager.execute_query(query, tuple(params))
        else:
            query = f"SELECT * FROM questions WHERE category = ? AND type = ?{exclude_done} ORDER BY RANDOM()"
            params = [category, q_type] + params
            results = db_manager.execute_query(query, tuple(params))

        db_manager.disconnect()

        self.current_questions = []
        for row in results:
            q = Question.from_dict(dict(row))
            self.current_questions.append(q)

        if self.current_questions:
            self.current_index = 0
            self.display_question(self.current_questions[0])
            self.update_navigation()
            status = "（仅未做）" if only_new else "（包含已做）"
            QMessageBox.information(self, '成功', f'已加载 {len(self.current_questions)} 道题目{status}！')
        else:
            if only_new:
                QMessageBox.warning(self, '提示', '没有找到未做的题目！\\n提示：可以取消勾选"只显示未做题目"来查看所有题目。')
            else:
                QMessageBox.warning(self, '提示', '没有找到符合条件的题目！')
            self.clear_display()"""

    new_code = """    def load_questions(self):
        \"\"\"加载题目\"\"\"
        try:
            category = self.category_combo.currentText()
            q_type = self.type_combo.currentData()
            only_new = self.only_new_checkbox.isChecked()

            db_manager.connect()

            # 构建基础查询和排除已做题目的子查询
            exclude_done = ""
            params = []

            if only_new:
                # 排除已做题目
                exclude_done = " AND id NOT IN (SELECT question_id FROM practice_records WHERE user_id = ?)"
                params.append(self.current_user.id)

            if category == '全部' and not q_type:
                query = f"SELECT * FROM questions WHERE 1=1{exclude_done} ORDER BY RANDOM()"
                results = db_manager.execute_query(query, tuple(params))
            elif category == '全部':
                query = f"SELECT * FROM questions WHERE type = ?{exclude_done} ORDER BY RANDOM()"
                params.insert(0, q_type)
                results = db_manager.execute_query(query, tuple(params))
            elif not q_type:
                query = f"SELECT * FROM questions WHERE category = ?{exclude_done} ORDER BY RANDOM()"
                params.insert(0, category)
                results = db_manager.execute_query(query, tuple(params))
            else:
                query = f"SELECT * FROM questions WHERE category = ? AND type = ?{exclude_done} ORDER BY RANDOM()"
                params = [category, q_type] + params
                results = db_manager.execute_query(query, tuple(params))

            db_manager.disconnect()

            self.current_questions = []
            for row in results:
                q = Question.from_dict(dict(row))
                self.current_questions.append(q)

            if self.current_questions:
                self.current_index = 0
                self.display_question(self.current_questions[0])
                self.update_navigation()
                status = "（仅未做）" if only_new else "（包含已做）"
                QMessageBox.information(self, '成功', f'已加载 {len(self.current_questions)} 道题目{status}！')
            else:
                if only_new:
                    QMessageBox.warning(self, '提示', '没有找到未做的题目！\\n提示：可以取消勾选"只显示未做题目"来查看所有题目。')
                else:
                    QMessageBox.warning(self, '提示', '没有找到符合条件的题目！')
                self.clear_display()
        except Exception as e:
            # 添加错误处理，防止崩溃
            import traceback
            error_msg = f'加载题目失败: {str(e)}\\n\\n{traceback.format_exc()}'
            print(f'[ERROR] {error_msg}')
            QMessageBox.critical(self, '错误', f'加载题目失败: {str(e)}')
            try:
                db_manager.disconnect()
            except:
                pass"""

    content = content.replace(old_code, new_code)

    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("[OK] Practice widget crash fix applied!")
    print("Changes:")
    print("1. Added try-except wrapper to load_questions method")
    print("2. Added error logging and user-friendly error message")
    print("3. Ensure database disconnection even on error")

if __name__ == '__main__':
    fix_practice_widget()
