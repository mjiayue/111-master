# -*- coding: utf-8 -*-
"""
完整初始化考试数据
添加考试、关联题目、添加测试点
"""
import sqlite3
from config import DATABASE_PATH


def initialize_exam_data():
    """完整初始化考试数据"""
    print("=" * 70)
    print("   初始化考试数据")
    print("=" * 70)
    print()

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # 步骤1: 创建考试
        print("步骤1: 创建考试...")
        print("-" * 50)

        exams = [
            {
                'name': 'Python基础入门考试',
                'description': '测试Python基础知识，包括变量、数据类型、运算符等基础内容',
                'duration': 45,
                'total_score': 100,
                'pass_score': 60,
                'category': 'Python基础',
                'difficulty': 'easy'
            },
            {
                'name': 'Python进阶考试',
                'description': '测试函数、列表、字典等进阶内容，包含编程题',
                'duration': 60,
                'total_score': 100,
                'pass_score': 70,
                'category': '综合',
                'difficulty': 'medium'
            },
            {
                'name': 'Python编程实战考试',
                'description': '主要测试编程能力，包含多道编程题和算法题',
                'duration': 90,
                'total_score': 100,
                'pass_score': 70,
                'category': '编程',
                'difficulty': 'hard'
            }
        ]

        for exam in exams:
            cursor.execute('''
                INSERT INTO exams (name, description, duration, total_score, pass_score, category, difficulty)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (exam['name'], exam['description'], exam['duration'],
                  exam['total_score'], exam['pass_score'], exam['category'], exam['difficulty']))
            print(f"  [OK] 创建考试: {exam['name']}")

        conn.commit()

        # 步骤2: 关联题目
        print("\n步骤2: 关联题目到考试...")
        print("-" * 50)

        # 考试1: Python基础入门考试 - 选择题和判断题
        cursor.execute("SELECT id FROM questions WHERE type='choice' LIMIT 10")
        choice_questions = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT id FROM questions WHERE type='judge' LIMIT 5")
        judge_questions = [row[0] for row in cursor.fetchall()]

        exam1_id = 1
        order = 0

        for qid in choice_questions[:8]:
            cursor.execute('''
                INSERT OR IGNORE INTO exam_questions (exam_id, question_id, score, order_num)
                VALUES (?, ?, ?, ?)
            ''', (exam1_id, qid, 10, order))
            order += 1

        for qid in judge_questions[:2]:
            cursor.execute('''
                INSERT OR IGNORE INTO exam_questions (exam_id, question_id, score, order_num)
                VALUES (?, ?, ?, ?)
            ''', (exam1_id, qid, 10, order))
            order += 1

        print(f"  [OK] 考试1 关联了 {order} 道题目")

        # 考试2: Python进阶考试 - 选择题、填空题、编程题
        cursor.execute("SELECT id FROM questions WHERE type='choice' LIMIT 5")
        choice_questions2 = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT id FROM questions WHERE type='fill' LIMIT 3")
        fill_questions = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT id FROM questions WHERE type='code' LIMIT 2")
        code_questions = [row[0] for row in cursor.fetchall()]

        exam2_id = 2
        order = 0

        for qid in choice_questions2:
            cursor.execute('''
                INSERT OR IGNORE INTO exam_questions (exam_id, question_id, score, order_num)
                VALUES (?, ?, ?, ?)
            ''', (exam2_id, qid, 10, order))
            order += 1

        for qid in fill_questions:
            cursor.execute('''
                INSERT OR IGNORE INTO exam_questions (exam_id, question_id, score, order_num)
                VALUES (?, ?, ?, ?)
            ''', (exam2_id, qid, 15, order))
            order += 1

        for qid in code_questions:
            cursor.execute('''
                INSERT OR IGNORE INTO exam_questions (exam_id, question_id, score, order_num)
                VALUES (?, ?, ?, ?)
            ''', (exam2_id, qid, 20, order))
            order += 1

        print(f"  [OK] 考试2 关联了 {order} 道题目")

        # 考试3: Python编程实战考试 - 主要是编程题
        cursor.execute("SELECT id FROM questions WHERE type='code' LIMIT 5")
        code_questions_all = [row[0] for row in cursor.fetchall()]

        exam3_id = 3
        order = 0

        for qid in code_questions_all:
            cursor.execute('''
                INSERT OR IGNORE INTO exam_questions (exam_id, question_id, score, order_num)
                VALUES (?, ?, ?, ?)
            ''', (exam3_id, qid, 20, order))
            order += 1

        print(f"  [OK] 考试3 关联了 {order} 道题目")

        # 步骤3: 为编程题添加测试点
        print("\n步骤3: 为编程题添加测试点...")
        print("-" * 50)

        # 获取所有编程题
        cursor.execute("SELECT id, question FROM questions WHERE type='code' LIMIT 10")
        all_code_questions = cursor.fetchall()

        test_case_count = 0

        for qid, question_text in all_code_questions:
            # 检查是否已有测试点
            cursor.execute('SELECT COUNT(*) FROM test_cases WHERE question_id = ?', (qid,))
            if cursor.fetchone()[0] > 0:
                continue

            # 为不同的题目添加不同的测试点
            # 这里简化处理，实际应该根据题目内容定制测试点

            # 测试点模板（通用）
            test_cases = [
                {
                    'input_data': '5\n',
                    'expected_output': '120',
                    'score': 5,
                    'is_sample': 1,
                    'description': '示例测试点'
                },
                {
                    'input_data': '3\n',
                    'expected_output': '6',
                    'score': 5,
                    'is_sample': 0,
                    'description': '测试点1 - 小数值'
                },
                {
                    'input_data': '1\n',
                    'expected_output': '1',
                    'score': 5,
                    'is_sample': 0,
                    'description': '测试点2 - 边界值'
                },
                {
                    'input_data': '10\n',
                    'expected_output': '3628800',
                    'score': 5,
                    'is_sample': 0,
                    'description': '测试点3 - 大数值'
                }
            ]

            for i, tc in enumerate(test_cases):
                cursor.execute('''
                    INSERT INTO test_cases
                    (question_id, input_data, expected_output, score, is_sample, description, order_num)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (qid, tc['input_data'], tc['expected_output'],
                      tc['score'], tc['is_sample'], tc['description'], i))

            test_case_count += len(test_cases)
            print(f"  [OK] 题目 ID:{qid} 添加了 {len(test_cases)} 个测试点")

        print(f"\n  总共添加了 {test_case_count} 个测试点")

        conn.commit()
        conn.close()

        # 步骤4: 显示最终统计
        print("\n" + "=" * 70)
        print("   初始化完成！")
        print("=" * 70)
        print()

        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # 统计考试
        cursor.execute('SELECT COUNT(*) FROM exams')
        exam_count = cursor.fetchone()[0]
        print(f"考试数量: {exam_count} 场")

        # 统计每场考试的题目数
        cursor.execute('''
            SELECT e.name, COUNT(eq.question_id)
            FROM exams e
            LEFT JOIN exam_questions eq ON e.id = eq.exam_id
            GROUP BY e.id
        ''')
        for name, count in cursor.fetchall():
            print(f"  • {name}: {count} 道题")

        # 统计测试点
        cursor.execute('SELECT COUNT(*) FROM test_cases')
        tc_count = cursor.fetchone()[0]
        print(f"\n编程题测试点: {tc_count} 个")

        conn.close()

        return True

    except Exception as e:
        print(f"\n[错误] 初始化失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = initialize_exam_data()

    print()
    if success:
        print("[成功] 考试数据初始化完成！")
        print()
        print("现在可以：")
        print("1. 启动系统")
        print("2. 点击左侧导航栏的'模拟考试'")
        print("3. 选择考试开始测试")
    else:
        print("[失败] 初始化失败，请查看错误信息")

    print()
