# -*- coding: utf-8 -*-
"""
考试功能自动集成脚本
自动修改主窗口并添加示例数据
"""
import os
import sqlite3
from config import DATABASE_PATH

def integrate_exam_module():
    """集成考试模块到主窗口"""
    print("步骤1: 集成考试模块到主窗口...")

    main_window_path = os.path.join('ui', 'main_window.py')

    try:
        # 读取main_window.py
        with open(main_window_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查是否已经集成
        if 'exam_widget' in content:
            print("  [跳过] 考试模块已经集成到主窗口")
            return True

        # 在导入部分添加
        import_line = "from ui.exam_widget import ExamWidget"
        if import_line not in content:
            # 在ProfileWidget导入之后添加
            content = content.replace(
                'from ui.profile_widget import ProfileWidget',
                'from ui.profile_widget import ProfileWidget\n        from ui.exam_widget import ExamWidget'
            )
            print("  [OK] 已添加ExamWidget导入")

        # 在模块初始化部分添加
        exam_module_code = '''        # 添加模拟考试模块
        self.exam_widget = ExamWidget(self.current_user)
        self.stack.addWidget(self.exam_widget)
        self.nav_list.addItem(QListWidgetItem('模拟考试'))

'''

        # 在题库练习之后添加考试模块
        if "self.practice_widget = PracticeWidget(self.current_user)" in content:
            content = content.replace(
                "        self.nav_list.addItem(QListWidgetItem('题库练习'))",
                "        self.nav_list.addItem(QListWidgetItem('题库练习'))\n\n" + exam_module_code.rstrip()
            )
            print("  [OK] 已添加考试模块到导航")

        # 写回文件
        with open(main_window_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print("  [成功] 主窗口集成完成！")
        return True

    except Exception as e:
        print(f"  [失败] 集成失败: {e}")
        return False


def add_sample_exam_data():
    """添加示例考试数据"""
    print("\n步骤2: 添加示例考试数据...")

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # 关联题目到考试1（基础考试）
        print("  正在关联题目到基础考试...")
        cursor.execute('''
            SELECT id FROM questions WHERE type='choice' LIMIT 8
        ''')
        choice_ids = [row[0] for row in cursor.fetchall()]

        for i, qid in enumerate(choice_ids):
            try:
                cursor.execute('''
                    INSERT INTO exam_questions (exam_id, question_id, score, order_num)
                    VALUES (1, ?, 10, ?)
                ''', (qid, i))
            except sqlite3.IntegrityError:
                pass  # 已存在

        cursor.execute('''
            SELECT id FROM questions WHERE type='judge' LIMIT 2
        ''')
        judge_ids = [row[0] for row in cursor.fetchall()]

        for i, qid in enumerate(judge_ids):
            try:
                cursor.execute('''
                    INSERT INTO exam_questions (exam_id, question_id, score, order_num)
                    VALUES (1, ?, 10, ?)
                ''', (qid, len(choice_ids) + i))
            except sqlite3.IntegrityError:
                pass

        print(f"  [OK] 已关联 {len(choice_ids) + len(judge_ids)} 道题到基础考试")

        # 关联题目到考试2（进阶考试）
        print("  正在关联题目到进阶考试...")
        cursor.execute('''
            SELECT id FROM questions WHERE type='code' LIMIT 3
        ''')
        code_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute('''
            SELECT id FROM questions WHERE type='fill' LIMIT 2
        ''')
        fill_ids = [row[0] for row in cursor.fetchall()]

        order = 0
        for qid in fill_ids:
            try:
                cursor.execute('''
                    INSERT INTO exam_questions (exam_id, question_id, score, order_num)
                    VALUES (2, ?, 15, ?)
                ''', (qid, order))
                order += 1
            except sqlite3.IntegrityError:
                pass

        for qid in code_ids:
            try:
                cursor.execute('''
                    INSERT INTO exam_questions (exam_id, question_id, score, order_num)
                    VALUES (2, ?, 30, ?)
                ''', (qid, order))
                order += 1
            except sqlite3.IntegrityError:
                pass

        print(f"  [OK] 已关联 {len(fill_ids) + len(code_ids)} 道题到进阶考试")

        # 为编程题添加简单的测试点
        print("  正在为编程题添加测试点...")
        if code_ids:
            for qid in code_ids[:2]:  # 只为前两道编程题添加
                # 检查是否已有测试点
                cursor.execute('SELECT COUNT(*) FROM test_cases WHERE question_id = ?', (qid,))
                if cursor.fetchone()[0] > 0:
                    continue

                # 添加示例测试点（简单的输入输出）
                test_cases = [
                    ('5\\n', '120', 10, 1),  # 示例
                    ('3\\n', '6', 5, 0),     # 测试点1
                    ('1\\n', '1', 5, 0),     # 测试点2
                ]

                for i, (inp, out, score, is_sample) in enumerate(test_cases):
                    cursor.execute('''
                        INSERT INTO test_cases
                        (question_id, input_data, expected_output, score, is_sample, order_num, description)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (qid, inp, out, score, is_sample, i, f'测试点 {i+1}'))

                print(f"    [OK] 已为题目 {qid} 添加 {len(test_cases)} 个测试点")

        conn.commit()
        conn.close()

        print("  [成功] 示例数据添加完成！")
        return True

    except Exception as e:
        print(f"  [失败] 数据添加失败: {e}")
        return False


if __name__ == '__main__':
    print("=" * 60)
    print("   考试功能自动集成脚本")
    print("=" * 60)
    print()

    success1 = integrate_exam_module()
    success2 = add_sample_exam_data()

    print("\n" + "=" * 60)
    if success1 and success2:
        print("   [成功] 考试功能集成完成！")
        print()
        print("   现在可以：")
        print("   1. 重启系统")
        print("   2. 在左侧导航栏点击'模拟考试'")
        print("   3. 选择考试开始测试")
    else:
        print("   [警告] 部分功能集成失败，请查看上方错误信息")

    print("=" * 60)

    input("\n按回车键退出...")
