# -*- coding: utf-8 -*-
"""
修复exam_widget.py中的数据库锁定问题
"""

def fix_exam_widget():
    file_path = "ui/exam_widget.py"

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 修改submit_exam方法
    old_submit = """        try:
            # 判题并保存结果
            total_score = 0
            for question in self.questions:
                score = self.grade_question(question)
                total_score += score

            # 更新考试记录
            self.db.connect()"""

    new_submit = """        try:
            # 统一连接数据库，避免嵌套连接导致锁定
            self.db.connect()

            # 判题并保存结果（使用内部方法，不再嵌套connect）
            total_score = 0
            for question in self.questions:
                score = self.grade_question_internal(question)
                total_score += score

            # 更新考试记录"""

    content = content.replace(old_submit, new_submit)

    # 修改grade_question方法，分离出内部方法
    old_grade = """    def grade_question(self, question):
        \"\"\"判题并返回得分\"\"\"
        question_id = question['id']
        if question_id not in self.answers:
            # 未作答
            return 0

        user_answer = self.answers[question_id]
        correct_answer = question['answer']
        score = question['score']

        is_correct = False

        if question['type'] == '编程题':
            # 编程题通过测试点判题
            score = self.grade_coding_question(question, user_answer)
            is_correct = score > 0
        else:
            # 其他题型直接比对答案
            if question['type'] == '填空题':
                is_correct = user_answer.strip() == correct_answer.strip()
            else:
                is_correct = user_answer == correct_answer

            score = score if is_correct else 0

        # 记录答题详情
        try:
            self.db.connect()
            self.db.cursor.execute('''
                INSERT INTO exam_answers (exam_record_id, question_id, user_answer, is_correct, obtained_score)
                VALUES (?, ?, ?, ?, ?)
            ''', (self.exam_record_id, question_id, user_answer, is_correct, score))

            # 如果答错，加入错题本
            if not is_correct:
                self.add_to_wrong_questions(question_id, 'exam')

            self.db.commit()
        finally:
            self.db.disconnect()

        return score"""

    new_grade = """    def grade_question(self, question):
        \"\"\"判题并返回得分（带数据库连接管理，供外部调用）\"\"\"
        try:
            self.db.connect()
            score = self.grade_question_internal(question)
            self.db.commit()
            return score
        finally:
            self.db.disconnect()

    def grade_question_internal(self, question):
        \"\"\"判题并返回得分（内部方法，假设数据库已连接）\"\"\"
        question_id = question['id']
        if question_id not in self.answers:
            # 未作答
            return 0

        user_answer = self.answers[question_id]
        correct_answer = question['answer']
        score = question['score']

        is_correct = False

        if question['type'] == 'code':
            # 编程题通过测试点判题
            score = self.grade_coding_question_internal(question, user_answer)
            is_correct = score > 0
        else:
            # 其他题型直接比对答案
            if question['type'] == 'fill':
                is_correct = user_answer.strip() == correct_answer.strip()
            else:
                is_correct = user_answer == correct_answer

            score = score if is_correct else 0

        # 记录答题详情（假设已连接）
        self.db.cursor.execute('''
            INSERT INTO exam_answers (exam_record_id, question_id, user_answer, is_correct, obtained_score)
            VALUES (?, ?, ?, ?, ?)
        ''', (self.exam_record_id, question_id, user_answer, is_correct, score))

        # 如果答错，加入错题本
        if not is_correct:
            self.add_to_wrong_questions_internal(question_id, 'exam')

        return score"""

    content = content.replace(old_grade, new_grade)

    # 修改grade_coding_question方法，分离出内部方法
    old_coding = """    def grade_coding_question(self, question, user_code):
        \"\"\"编程题判题（PTA风格多测试点）\"\"\"
        try:
            self.db.connect()
            # 获取测试点
            result = self.db.execute_query(
                'SELECT * FROM test_cases WHERE question_id = ? ORDER BY order_num',
                (question['id'],)
            )
            test_cases = [dict(row) for row in result]

            if not test_cases:
                # 没有测试点，使用标准答案比对
                return question['score'] if user_code.strip() == question['answer'].strip() else 0

            # 运行测试点
            passed_count = 0
            total_score = 0

            for test_case in test_cases:
                passed = self.run_test_case(user_code, test_case)
                if passed:
                    passed_count += 1
                    total_score += test_case['score']

            # 更新答题记录的测试点信息
            self.db.cursor.execute('''
                UPDATE exam_answers
                SET test_cases_passed = ?, test_cases_total = ?
                WHERE exam_record_id = ? AND question_id = ?
            ''', (passed_count, len(test_cases), self.exam_record_id, question['id']))
            self.db.commit()

            return total_score

        except Exception as e:
            print(f"编程题判题失败: {e}")
            return 0
        finally:
            self.db.disconnect()"""

    new_coding = """    def grade_coding_question(self, question, user_code):
        \"\"\"编程题判题（带数据库连接管理，供外部调用）\"\"\"
        try:
            self.db.connect()
            score = self.grade_coding_question_internal(question, user_code)
            self.db.commit()
            return score
        except Exception as e:
            print(f"编程题判题失败: {e}")
            return 0
        finally:
            self.db.disconnect()

    def grade_coding_question_internal(self, question, user_code):
        \"\"\"编程题判题（内部方法，假设数据库已连接）\"\"\"
        # 获取测试点
        result = self.db.execute_query(
            'SELECT * FROM test_cases WHERE question_id = ? ORDER BY order_num',
            (question['id'],)
        )
        test_cases = [dict(row) for row in result]

        if not test_cases:
            # 没有测试点，使用标准答案比对
            return question['score'] if user_code.strip() == question['answer'].strip() else 0

        # 运行测试点
        passed_count = 0
        total_score = 0

        for test_case in test_cases:
            passed = self.run_test_case(user_code, test_case)
            if passed:
                passed_count += 1
                total_score += test_case['score']

        # 更新答题记录的测试点信息
        self.db.cursor.execute('''
            UPDATE exam_answers
            SET test_cases_passed = ?, test_cases_total = ?
            WHERE exam_record_id = ? AND question_id = ?
        ''', (passed_count, len(test_cases), self.exam_record_id, question['id']))

        return total_score"""

    content = content.replace(old_coding, new_coding)

    # 修改add_to_wrong_questions方法，分离出内部方法
    old_wrong = """    def add_to_wrong_questions(self, question_id, source='exam'):
        \"\"\"添加到错题本\"\"\"
        try:
            self.db.connect()
            self.db.cursor.execute('''
                INSERT OR REPLACE INTO wrong_questions
                (user_id, question_id, wrong_count, source, last_wrong_at)
                VALUES (
                    ?,
                    ?,
                    COALESCE((SELECT wrong_count + 1 FROM wrong_questions WHERE user_id = ? AND question_id = ?), 1),
                    ?,
                    CURRENT_TIMESTAMP
                )
            ''', (self.current_user.id, question_id, self.current_user.id, question_id, source))
            self.db.commit()
        finally:
            self.db.disconnect()"""

    new_wrong = """    def add_to_wrong_questions(self, question_id, source='exam'):
        \"\"\"添加到错题本（带数据库连接管理，供外部调用）\"\"\"
        try:
            self.db.connect()
            self.add_to_wrong_questions_internal(question_id, source)
            self.db.commit()
        finally:
            self.db.disconnect()

    def add_to_wrong_questions_internal(self, question_id, source='exam'):
        \"\"\"添加到错题本（内部方法，假设数据库已连接）\"\"\"
        self.db.cursor.execute('''
            INSERT OR REPLACE INTO wrong_questions
            (user_id, question_id, wrong_count, source, last_wrong_at)
            VALUES (
                ?,
                ?,
                COALESCE((SELECT wrong_count + 1 FROM wrong_questions WHERE user_id = ? AND question_id = ?), 1),
                ?,
                CURRENT_TIMESTAMP
            )
        ''', (self.current_user.id, question_id, self.current_user.id, question_id, source))"""

    content = content.replace(old_wrong, new_wrong)

    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("[OK] Database lock issue fixed!")
    print("Changes:")
    print("1. submit_exam: Use single DB connection")
    print("2. Added grade_question_internal method")
    print("3. Added grade_coding_question_internal method")
    print("4. Added add_to_wrong_questions_internal method")
    print("5. Keep original methods for external calls")

if __name__ == '__main__':
    fix_exam_widget()
