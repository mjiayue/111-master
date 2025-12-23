# -*- coding: utf-8 -*-
"""
数据库升级脚本 - 添加考试功能
为系统添加模拟考试功能，包括PTA风格的多测试点系统
"""
import sqlite3
import os
from config import DATABASE_PATH

def upgrade_database():
    """升级数据库，添加考试相关的表"""
    if not os.path.exists(DATABASE_PATH):
        print(f"数据库文件不存在: {DATABASE_PATH}")
        return False

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        print("开始升级数据库...")

        # 1. 创建考试表
        print("创建考试表...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                duration INTEGER NOT NULL,
                total_score INTEGER DEFAULT 100,
                pass_score INTEGER DEFAULT 60,
                category TEXT,
                difficulty TEXT DEFAULT 'medium',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 2. 创建考试题目关联表
        print("创建考试题目关联表...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exam_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exam_id INTEGER NOT NULL,
                question_id INTEGER NOT NULL,
                score INTEGER DEFAULT 10,
                order_num INTEGER DEFAULT 0,
                FOREIGN KEY (exam_id) REFERENCES exams(id),
                FOREIGN KEY (question_id) REFERENCES questions(id),
                UNIQUE(exam_id, question_id)
            )
        ''')

        # 3. 创建测试点表（用于编程题）
        print("创建测试点表...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_cases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id INTEGER NOT NULL,
                input_data TEXT NOT NULL,
                expected_output TEXT NOT NULL,
                score INTEGER DEFAULT 10,
                is_sample BOOLEAN DEFAULT 0,
                time_limit INTEGER DEFAULT 1000,
                memory_limit INTEGER DEFAULT 128,
                description TEXT,
                order_num INTEGER DEFAULT 0,
                FOREIGN KEY (question_id) REFERENCES questions(id)
            )
        ''')

        # 4. 创建考试记录表
        print("创建考试记录表...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exam_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                exam_id INTEGER NOT NULL,
                start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_time TIMESTAMP,
                total_score INTEGER DEFAULT 0,
                obtained_score INTEGER DEFAULT 0,
                status TEXT DEFAULT 'in_progress',
                time_spent INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (exam_id) REFERENCES exams(id)
            )
        ''')

        # 5. 创建考试答题记录表
        print("创建考试答题记录表...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exam_answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exam_record_id INTEGER NOT NULL,
                question_id INTEGER NOT NULL,
                user_answer TEXT,
                is_correct BOOLEAN,
                obtained_score INTEGER DEFAULT 0,
                test_cases_passed INTEGER DEFAULT 0,
                test_cases_total INTEGER DEFAULT 0,
                submit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (exam_record_id) REFERENCES exam_records(id),
                FOREIGN KEY (question_id) REFERENCES questions(id)
            )
        ''')

        # 6. 为错题本表增加来源字段
        print("升级错题本表...")
        try:
            cursor.execute("ALTER TABLE wrong_questions ADD COLUMN source TEXT DEFAULT 'practice'")
            print("  ✓ 添加source字段成功")
        except sqlite3.OperationalError:
            print("  ✓ source字段已存在，跳过")

        # 7. 添加示例考试数据
        print("添加示例考试数据...")
        cursor.execute('''
            INSERT OR IGNORE INTO exams (id, name, description, duration, total_score, pass_score, category, difficulty)
            VALUES (1, 'Python基础考试', 'Python基础知识综合测试，包含选择题、判断题和编程题', 60, 100, 60, 'Python基础', 'easy')
        ''')

        cursor.execute('''
            INSERT OR IGNORE INTO exams (id, name, description, duration, total_score, pass_score, category, difficulty)
            VALUES (2, 'Python进阶考试', 'Python进阶知识测试，包含复杂编程题和算法题', 90, 100, 70, '综合', 'hard')
        ''')

        conn.commit()

        print("\n数据库升级完成！")
        print("新增表格：")
        print("  - exams (考试表)")
        print("  - exam_questions (考试题目关联表)")
        print("  - test_cases (测试点表)")
        print("  - exam_records (考试记录表)")
        print("  - exam_answers (考试答题记录表)")
        print("\n升级字段：")
        print("  - wrong_questions.source (错题来源：practice/exam)")

        conn.close()
        return True

    except Exception as e:
        print(f"数据库升级失败: {e}")
        return False


if __name__ == '__main__':
    print("=" * 50)
    print("   数据库升级脚本 - 添加考试功能")
    print("=" * 50)
    print()

    success = upgrade_database()

    if success:
        print("\n✓ 升级成功！现在可以使用模拟考试功能了。")
    else:
        print("\n✗ 升级失败，请检查错误信息。")

    input("\n按回车键退出...")
