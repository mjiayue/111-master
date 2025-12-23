# -*- coding: utf-8 -*-
"""
添加考试测试点示例数据
为编程题添加PTA风格的多测试点
"""
import sqlite3
from config import DATABASE_PATH

def add_sample_test_cases():
    """添加示例测试点数据"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        print("正在添加考试和测试点示例数据...")

        # 1. 查找编程题（随机选择几道编程题）
        cursor.execute("SELECT id, question FROM questions WHERE type='编程题' LIMIT 5")
        coding_questions = cursor.fetchall()

        if not coding_questions:
            print("警告：数据库中没有编程题，无法添加测试点")
            return

        # 2. 为第一道编程题添加测试点（假设是简单的输入输出题）
        # 示例：求两个数的和
        question_id_1 = coding_questions[0][0]
        print(f"\n为题目 {question_id_1} 添加测试点...")

        test_cases_1 = [
            {
                'question_id': question_id_1,
                'input_data': '3\n5\n',
                'expected_output': '8',
                'score': 5,
                'is_sample': 1,  # 示例测试点
                'description': '示例测试点 1'
            },
            {
                'question_id': question_id_1,
                'input_data': '10\n20\n',
                'expected_output': '30',
                'score': 5,
                'is_sample': 0,
                'description': '测试点 1'
            },
            {
                'question_id': question_id_1,
                'input_data': '0\n0\n',
                'expected_output': '0',
                'score': 5,
                'is_sample': 0,
                'description': '测试点 2 - 边界情况'
            },
            {
                'question_id': question_id_1,
                'input_data': '-5\n10\n',
                'expected_output': '5',
                'score': 5,
                'is_sample': 0,
                'description': '测试点 3 - 负数'
            },
        ]

        for i, tc in enumerate(test_cases_1):
            cursor.execute('''
                INSERT INTO test_cases
                (question_id, input_data, expected_output, score, is_sample, description, order_num)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (tc['question_id'], tc['input_data'], tc['expected_output'],
                  tc['score'], tc['is_sample'], tc['description'], i))
            print(f"  ✓ 添加测试点: {tc['description']}")

        # 3. 为其他编程题也添加测试点
        if len(coding_questions) >= 2:
            question_id_2 = coding_questions[1][0]
            print(f"\n为题目 {question_id_2} 添加测试点...")

            test_cases_2 = [
                {
                    'question_id': question_id_2,
                    'input_data': '5\n',
                    'expected_output': '120',  # 5的阶乘
                    'score': 10,
                    'is_sample': 1,
                    'description': '示例测试点'
                },
                {
                    'question_id': question_id_2,
                    'input_data': '1\n',
                    'expected_output': '1',
                    'score': 5,
                    'is_sample': 0,
                    'description': '测试点 1 - 最小值'
                },
                {
                    'question_id': question_id_2,
                    'input_data': '10\n',
                    'expected_output': '3628800',
                    'score': 5,
                    'is_sample': 0,
                    'description': '测试点 2 - 较大值'
                },
            ]

            for i, tc in enumerate(test_cases_2):
                cursor.execute('''
                    INSERT INTO test_cases
                    (question_id, input_data, expected_output, score, is_sample, description, order_num)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (tc['question_id'], tc['input_data'], tc['expected_output'],
                      tc['score'], tc['is_sample'], tc['description'], i))
                print(f"  ✓ 添加测试点: {tc['description']}")

        # 4. 关联题目到考试
        print("\n关联题目到考试...")

        # 获取所有题目（限制数量）
        cursor.execute("SELECT id FROM questions WHERE type IN ('选择题', '判断题') LIMIT 5")
        choice_questions = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT id FROM questions WHERE type='编程题' LIMIT 3")
        coding_questions_ids = [row[0] for row in cursor.fetchall()]

        # 关联到考试1（基础考试）
        exam_id_1 = 1
        order = 0
        for qid in choice_questions:
            try:
                cursor.execute('''
                    INSERT INTO exam_questions (exam_id, question_id, score, order_num)
                    VALUES (?, ?, ?, ?)
                ''', (exam_id_1, qid, 10, order))
                order += 1
            except sqlite3.IntegrityError:
                pass  # 已存在，跳过

        for qid in coding_questions_ids[:1]:  # 只添加1道编程题
            try:
                cursor.execute('''
                    INSERT INTO exam_questions (exam_id, question_id, score, order_num)
                    VALUES (?, ?, ?, ?)
                ''', (exam_id_1, qid, 20, order))
                order += 1
            except sqlite3.IntegrityError:
                pass

        print(f"  ✓ 已关联 {order} 道题目到考试 1")

        # 关联到考试2（进阶考试）
        exam_id_2 = 2
        order = 0
        for qid in coding_questions_ids:
            try:
                cursor.execute('''
                    INSERT INTO exam_questions (exam_id, question_id, score, order_num)
                    VALUES (?, ?, ?, ?)
                ''', (exam_id_2, qid, 30, order))
                order += 1
            except sqlite3.IntegrityError:
                pass

        print(f"  ✓ 已关联 {order} 道题目到考试 2")

        conn.commit()
        conn.close()

        print("\n✓ 测试点和考试数据添加完成！")
        print("\n说明：")
        print("- 已为编程题添加多个测试点（PTA风格）")
        print("- 测试点包含示例数据和隐藏数据")
        print("- 每个测试点都有独立的分数")
        print("- 已将题目关联到考试")
        return True

    except Exception as e:
        print(f"添加数据失败: {e}")
        return False


if __name__ == '__main__':
    print("=" * 60)
    print("   添加考试测试点示例数据")
    print("=" * 60)
    print()

    success = add_sample_test_cases()

    if success:
        print("\n[OK] 数据添加成功！现在可以体验完整的考试功能了。")
    else:
        print("\n[ERROR] 数据添加失败。")

    input("\n按回车键退出...")
