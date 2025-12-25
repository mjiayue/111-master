# -*- coding: utf-8 -*-
"""
清理数据库中内容重复的题目，重新配置三套完整试卷
"""
import sqlite3

def clean_and_reconfigure():
    conn = sqlite3.connect('database/python_learning.db')
    cursor = conn.cursor()

    try:
        print("Step 1: Finding duplicate questions by content...")

        # 找出所有题目，按内容分组
        cursor.execute('SELECT id, type, question, difficulty FROM questions ORDER BY id')
        all_questions = cursor.fetchall()

        # 按内容去重，保留最小的ID
        unique_questions = {}  # key: (type, question_text, difficulty), value: smallest_id
        duplicate_ids = []

        for q_id, q_type, q_text, q_diff in all_questions:
            key = (q_type, q_text[:100] if q_text else '', q_diff)  # 用前100字符作为key

            if key not in unique_questions:
                unique_questions[key] = q_id
            else:
                # 这是重复的题目
                duplicate_ids.append(q_id)

        print(f"  Total questions: {len(all_questions)}")
        print(f"  Unique questions: {len(unique_questions)}")
        print(f"  Duplicate questions: {len(duplicate_ids)}")

        # 获取去重后的题目列表，按类型和难度分类
        unique_by_type_diff = {}
        cursor.execute('SELECT id, type, difficulty FROM questions WHERE id NOT IN ({})'.format(
            ','.join(map(str, duplicate_ids)) if duplicate_ids else '-1'
        ))

        for q_id, q_type, q_diff in cursor.fetchall():
            key = f"{q_type}_{q_diff}"
            if key not in unique_by_type_diff:
                unique_by_type_diff[key] = []
            unique_by_type_diff[key].append(q_id)

        print("\nStep 2: Available unique questions by type and difficulty:")
        for key, ids in sorted(unique_by_type_diff.items()):
            print(f"  {key}: {len(ids)} questions")

        # 检查是否有足够的题目
        choice_easy = len(unique_by_type_diff.get('choice_easy', []))
        judge_easy = len(unique_by_type_diff.get('judge_easy', []))
        fill_easy = len(unique_by_type_diff.get('fill_easy', []))
        code_easy = len(unique_by_type_diff.get('code_easy', []))

        total_for_40_choice = choice_easy + judge_easy

        print(f"\nStep 3: Checking if we have enough questions for 3 exams:")
        print(f"  Choice+Judge (need 120): {total_for_40_choice}")
        print(f"  Fill (need 9): {fill_easy}")
        print(f"  Code (need 9): {code_easy}")

        if total_for_40_choice < 120:
            print(f"  [WARNING] Not enough choice/judge questions! Need 120, have {total_for_40_choice}")
            print(f"  [SOLUTION] Will use questions from all difficulties")

        if fill_easy < 9:
            print(f"  [WARNING] Not enough fill questions! Need 9, have {fill_easy}")

        if code_easy < 9:
            print(f"  [WARNING] Not enough code questions! Need 9, have {code_easy}")

        # 清空现有考试题目
        print("\nStep 4: Clearing existing exam questions...")
        cursor.execute('DELETE FROM exam_questions WHERE exam_id IN (1, 2, 3)')

        # 更新考试信息
        print("\nStep 5: Updating exam information...")
        cursor.execute('''
            UPDATE exams
            SET name = '计算机二级Python模拟考试（一）',
                description = '基础难度：适合初学者和第一次模考',
                difficulty = '简单'
            WHERE id = 1
        ''')
        cursor.execute('''
            UPDATE exams
            SET name = '计算机二级Python模拟考试（二）',
                description = '中等难度：适合有一定基础的学习者',
                difficulty = '中等'
            WHERE id = 2
        ''')
        cursor.execute('''
            UPDATE exams
            SET name = '计算机二级Python模拟考试（三）',
                description = '高级难度：适合冲刺高分的学习者',
                difficulty = '困难'
            WHERE id = 3
        ''')

        # 为三套试卷分配题目
        print("\nStep 6: Assigning questions to 3 exams (NO DUPLICATES)...")

        used_questions = set()

        # 收集所有可用的选择题和判断题（用于40道选择题）
        all_choice_judge = []
        for key in ['choice_easy', 'choice_medium', 'judge_easy', 'judge_medium']:
            if key in unique_by_type_diff:
                all_choice_judge.extend(unique_by_type_diff[key])

        # 收集所有填空题
        all_fill = []
        for key in ['fill_easy', 'fill_medium']:
            if key in unique_by_type_diff:
                all_fill.extend(unique_by_type_diff[key])

        # 收集所有编程题
        all_code = []
        for key in ['code_easy', 'code_medium']:
            if key in unique_by_type_diff:
                all_code.extend(unique_by_type_diff[key])

        print(f"  Total available: {len(all_choice_judge)} choice/judge, {len(all_fill)} fill, {len(all_code)} code")

        for exam_id in [1, 2, 3]:
            print(f"\n  Configuring Exam {exam_id}...")
            order_num = 1

            # 40道选择题
            choice_count = 0
            for q_id in all_choice_judge:
                if q_id in used_questions:
                    continue
                if choice_count >= 40:
                    break

                cursor.execute('''
                    INSERT INTO exam_questions (exam_id, question_id, score, order_num)
                    VALUES (?, ?, 1, ?)
                ''', (exam_id, q_id, order_num))
                used_questions.add(q_id)
                order_num += 1
                choice_count += 1

            print(f"    Choice/Judge: {choice_count} questions")

            # 3道填空题
            fill_count = 0
            for q_id in all_fill:
                if q_id in used_questions:
                    continue
                if fill_count >= 3:
                    break

                cursor.execute('''
                    INSERT INTO exam_questions (exam_id, question_id, score, order_num)
                    VALUES (?, ?, 5, ?)
                ''', (exam_id, q_id, order_num))
                used_questions.add(q_id)
                order_num += 1
                fill_count += 1

            print(f"    Fill: {fill_count} questions")

            # 3道编程题
            code_count = 0
            scores = [10, 15, 20]
            for q_id in all_code:
                if q_id in used_questions:
                    continue
                if code_count >= 3:
                    break

                cursor.execute('''
                    INSERT INTO exam_questions (exam_id, question_id, score, order_num)
                    VALUES (?, ?, ?, ?)
                ''', (exam_id, q_id, scores[code_count], order_num))
                used_questions.add(q_id)
                order_num += 1
                code_count += 1

            print(f"    Code: {code_count} questions")
            print(f"    Total: {order_num - 1} questions")

        conn.commit()

        # 验证
        print("\n" + "=" * 70)
        print("VERIFICATION:")
        print("=" * 70)

        for exam_id in [1, 2, 3]:
            cursor.execute('''
                SELECT COUNT(*), SUM(score)
                FROM exam_questions
                WHERE exam_id = ?
            ''', (exam_id,))
            count, total = cursor.fetchone()
            print(f"Exam {exam_id}: {count} questions, {total} points")

        # 检查跨试卷重复
        cursor.execute('''
            SELECT question_id, COUNT(DISTINCT exam_id)
            FROM exam_questions
            WHERE exam_id IN (1, 2, 3)
            GROUP BY question_id
            HAVING COUNT(DISTINCT exam_id) > 1
        ''')
        cross_dups = cursor.fetchall()

        if cross_dups:
            print(f"\n[ERROR] {len(cross_dups)} questions appear in multiple exams!")
        else:
            print(f"\n[SUCCESS] NO questions are shared between exams!")

        print("=" * 70)

    except Exception as e:
        conn.rollback()
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == '__main__':
    clean_and_reconfigure()
