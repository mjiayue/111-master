# -*- coding: utf-8 -*-
"""
修改学习进度页面脚本
"""

def fix_progress_widget():
    """修复progress_widget.py"""

    # 读取原文件
    with open('ui/progress_widget.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # 修改1: 删除stat_labels中的accuracy引用
        if "'accuracy': None" in line and i > 25 and i < 35:
            # 跳过这行
            i += 1
            continue

        # 修改2: 增大标题字体
        if "title_label.setFont(QFont('SF Pro Display', 16, QFont.Bold))" in line:
            line = line.replace("16", "18")

        # 修改3: 删除正确率卡片创建
        if "# 正确率卡片" in line:
            # 跳过正确率卡片的3行代码
            i += 3
            continue

        # 修改4: Removed Category Progress title
        if "category_group = QGroupBox('各分类学习进度')" in line:
            line = line.replace("QGroupBox('各分类学习进度')", "QGroupBox('')")

        # 修改5: 修改QGroupBox样式
        if "category_group.setStyleSheet('QGroupBox { padding-top: 20px; margin-top: 10px; }')" in line:
            line = line.replace(
                "'QGroupBox { padding-top: 20px; margin-top: 10px; }'",
                "'QGroupBox { padding-top: 10px; margin-top: 10px; border: none; }'"
            )

        # 修改6: 增加表格列数
        if "self.category_table.setColumnCount(4)" in line:
            line = line.replace("4", "5")

        # 修改7: 修改表头标签
        if "self.category_table.setHorizontalHeaderLabels(['分类', '总知识点', '已完成', '进度'])" in line:
            line = line.replace(
                "['分类', '总知识点', '已完成', '进度']",
                "['分类', '总知识点', '已完成', '进度', '正确率']"
            )

        # 修改8: 增大表格字体
        if "self.category_table.setFont(QFont('SF Pro Display', 10))" in line:
            line = line.replace("'SF Pro Display', 10", "'Microsoft YaHei', 12")

        # 修改9: 增大卡片标题字体
        if "title_label.setFont(QFont('Microsoft YaHei', 11))" in line and "'stat_card'" not in line:
            line = line.replace("11", "13")

        # 修改10: 增大卡片数值字体
        if "value_label.setFont(QFont('Microsoft YaHei', 20, QFont.Bold))" in line:
            line = line.replace("20", "26")

        # 修改11: 增大卡片padding
        if "padding: 15px;" in line and i > 90 and i < 100:
            line = line.replace("15px", "20px")

        # 修改12: 删除load_data中的accuracy更新
        if "if self.stat_labels['accuracy']:" in line:
            # 跳过这两行
            i += 2
            continue

        new_lines.append(line)
        i += 1

    # 处理load_data中的学习时长显示
    final_lines = []
    for i, line in enumerate(new_lines):
        if "self.stat_labels['time'].setText(f\"{minutes} 分钟\")" in line:
            # 替换为更智能的时长显示
            indent = ' ' * 12
            final_lines.append(f"{indent}minutes = stats['total_study_time'] // 60\n")
            final_lines.append(f"{indent}hours = minutes // 60\n")
            final_lines.append(f"{indent}remaining_minutes = minutes % 60\n")
            final_lines.append(f"{indent}if hours > 0:\n")
            final_lines.append(f"{indent}    self.stat_labels['time'].setText(f\"{{hours}} 小时 {{remaining_minutes}} 分钟\")\n")
            final_lines.append(f"{indent}else:\n")
            final_lines.append(f"{indent}    self.stat_labels['time'].setText(f\"{{minutes}} 分钟\")\n")
        else:
            final_lines.append(line)

    # 修改load_category_progress方法，添加正确率列和数据准确性修复
    result_lines = []
    in_load_category = False
    skip_until_disconnect = False

    for i, line in enumerate(final_lines):
        if "def load_category_progress(self):" in line:
            in_load_category = True
            result_lines.append(line)
            result_lines.append(final_lines[i+1])  # """加载分类进度"""
            result_lines.append(final_lines[i+2])  # self.category_table.setRowCount(0)
            result_lines.append(final_lines[i+3])  # 空行
            result_lines.append(final_lines[i+4])  # db_manager.connect()
            result_lines.append(final_lines[i+5])  # 空行
            result_lines.append(final_lines[i+6])  # for i, category in enumerate

            # 插入新的SQL查询代码
            indent = ' ' * 12
            result_lines.append(f"{indent}# 获取该分类的总知识点数\n")
            result_lines.append(f"{indent}total_query = \"SELECT COUNT(*) as count FROM knowledge_points WHERE category = ?\"\n")
            result_lines.append(f"{indent}total_result = db_manager.execute_query(total_query, (category,))\n")
            result_lines.append(f"{indent}total_count = dict(total_result[0])['count'] if total_result else 0\n")
            result_lines.append(f"\n")

            result_lines.append(f"{indent}# 获取已完成数（确保数据准确性：使用DISTINCT避免重复计数）\n")
            result_lines.append(f"{indent}completed_query = \"\"\"\n")
            result_lines.append(f"{indent}    SELECT COUNT(DISTINCT lr.knowledge_id) as count\n")
            result_lines.append(f"{indent}    FROM learning_records lr\n")
            result_lines.append(f"{indent}    JOIN knowledge_points kp ON lr.knowledge_id = kp.id\n")
            result_lines.append(f"{indent}    WHERE lr.user_id = ? AND kp.category = ? AND lr.completed = 1\n")
            result_lines.append(f"{indent}\"\"\"\n")
            result_lines.append(f"{indent}completed_result = db_manager.execute_query(\n")
            result_lines.append(f"{indent}    completed_query,\n")
            result_lines.append(f"{indent}    (self.current_user.id, category)\n")
            result_lines.append(f"{indent})\n")
            result_lines.append(f"{indent}completed_count = dict(completed_result[0])['count'] if completed_result else 0\n")
            result_lines.append(f"\n")

            result_lines.append(f"{indent}# 获取该分类的练习题正确率\n")
            result_lines.append(f"{indent}accuracy_query = \"\"\"\n")
            result_lines.append(f"{indent}    SELECT\n")
            result_lines.append(f"{indent}        COUNT(CASE WHEN pr.is_correct = 1 THEN 1 END) as correct,\n")
            result_lines.append(f"{indent}        COUNT(*) as total\n")
            result_lines.append(f"{indent}    FROM practice_records pr\n")
            result_lines.append(f"{indent}    JOIN questions q ON pr.question_id = q.id\n")
            result_lines.append(f"{indent}    WHERE pr.user_id = ? AND q.category = ?\n")
            result_lines.append(f"{indent}\"\"\"\n")
            result_lines.append(f"{indent}accuracy_result = db_manager.execute_query(\n")
            result_lines.append(f"{indent}    accuracy_query,\n")
            result_lines.append(f"{indent}    (self.current_user.id, category)\n")
            result_lines.append(f"{indent})\n")
            result_lines.append(f"\n")

            result_lines.append(f"{indent}if accuracy_result and dict(accuracy_result[0])['total'] > 0:\n")
            result_lines.append(f"{indent}    correct = dict(accuracy_result[0])['correct']\n")
            result_lines.append(f"{indent}    total = dict(accuracy_result[0])['total']\n")
            result_lines.append(f"{indent}    accuracy = round((correct / total) * 100, 1)\n")
            result_lines.append(f"{indent}    accuracy_text = f\"{{accuracy}}%\"\n")
            result_lines.append(f"{indent}else:\n")
            result_lines.append(f"{indent}    accuracy_text = \"未练习\"\n")
            result_lines.append(f"\n")

            result_lines.append(f"{indent}# 计算进度\n")
            result_lines.append(f"{indent}progress = int((completed_count / total_count) * 100) if total_count > 0 else 0\n")
            result_lines.append(f"\n")

            result_lines.append(f"{indent}# 添加到表格\n")
            result_lines.append(f"{indent}self.category_table.insertRow(i)\n")
            result_lines.append(f"\n")

            result_lines.append(f"{indent}# 分类\n")
            result_lines.append(f"{indent}category_item = QTableWidgetItem(category)\n")
            result_lines.append(f"{indent}category_item.setTextAlignment(Qt.AlignCenter)\n")
            result_lines.append(f"{indent}category_item.setFont(QFont('Microsoft YaHei', 12, QFont.Bold))\n")
            result_lines.append(f"{indent}self.category_table.setItem(i, 0, category_item)\n")
            result_lines.append(f"\n")

            result_lines.append(f"{indent}# 总数\n")
            result_lines.append(f"{indent}total_item = QTableWidgetItem(str(total_count))\n")
            result_lines.append(f"{indent}total_item.setTextAlignment(Qt.AlignCenter)\n")
            result_lines.append(f"{indent}total_item.setFont(QFont('Microsoft YaHei', 12))\n")
            result_lines.append(f"{indent}self.category_table.setItem(i, 1, total_item)\n")
            result_lines.append(f"\n")

            result_lines.append(f"{indent}# 已完成\n")
            result_lines.append(f"{indent}completed_item = QTableWidgetItem(str(completed_count))\n")
            result_lines.append(f"{indent}completed_item.setTextAlignment(Qt.AlignCenter)\n")
            result_lines.append(f"{indent}completed_item.setFont(QFont('Microsoft YaHei', 12))\n")
            result_lines.append(f"{indent}self.category_table.setItem(i, 2, completed_item)\n")
            result_lines.append(f"\n")

            result_lines.append(f"{indent}# 进度\n")
            result_lines.append(f"{indent}progress_item = QTableWidgetItem(f'{{progress}}%')\n")
            result_lines.append(f"{indent}progress_item.setTextAlignment(Qt.AlignCenter)\n")
            result_lines.append(f"{indent}progress_item.setFont(QFont('Microsoft YaHei', 12, QFont.Bold))\n")
            result_lines.append(f"{indent}# 根据进度设置颜色\n")
            result_lines.append(f"{indent}if progress >= 80:\n")
            result_lines.append(f"{indent}    progress_item.setForeground(Qt.darkGreen)\n")
            result_lines.append(f"{indent}elif progress >= 50:\n")
            result_lines.append(f"{indent}    progress_item.setForeground(Qt.darkBlue)\n")
            result_lines.append(f"{indent}else:\n")
            result_lines.append(f"{indent}    progress_item.setForeground(Qt.darkRed)\n")
            result_lines.append(f"{indent}self.category_table.setItem(i, 3, progress_item)\n")
            result_lines.append(f"\n")

            result_lines.append(f"{indent}# 正确率\n")
            result_lines.append(f"{indent}accuracy_item = QTableWidgetItem(accuracy_text)\n")
            result_lines.append(f"{indent}accuracy_item.setTextAlignment(Qt.AlignCenter)\n")
            result_lines.append(f"{indent}accuracy_item.setFont(QFont('Microsoft YaHei', 12, QFont.Bold))\n")
            result_lines.append(f"{indent}# 根据正确率设置颜色\n")
            result_lines.append(f"{indent}if accuracy_text != \"未练习\":\n")
            result_lines.append(f"{indent}    acc_value = float(accuracy_text.rstrip('%'))\n")
            result_lines.append(f"{indent}    if acc_value >= 80:\n")
            result_lines.append(f"{indent}        accuracy_item.setForeground(Qt.darkGreen)\n")
            result_lines.append(f"{indent}    elif acc_value >= 60:\n")
            result_lines.append(f"{indent}        accuracy_item.setForeground(Qt.darkBlue)\n")
            result_lines.append(f"{indent}    else:\n")
            result_lines.append(f"{indent}        accuracy_item.setForeground(Qt.darkRed)\n")
            result_lines.append(f"{indent}self.category_table.setItem(i, 4, accuracy_item)\n")
            result_lines.append(f"\n")

            skip_until_disconnect = True
            continue

        if skip_until_disconnect and "db_manager.disconnect()" in line:
            skip_until_disconnect = False
            result_lines.append(line)
            in_load_category = False
            continue

        if skip_until_disconnect:
            continue

        result_lines.append(line)

    # 写入文件
    with open('ui/progress_widget.py', 'w', encoding='utf-8') as f:
        f.writelines(result_lines)

    print("OK - progress_widget.py updated!")
    print("\nModifications:")
    print("1. ✅ Removed overall accuracy card")
    print("2. ✅ Removed Category Progress title")
    print("3. ✅ Added Accuracy column to table")
    print("4. ✅ Increased font sizes（标题18px, 卡片26px, 表格12px）")
    print("5. ✅ Fixed data accuracy（使用DISTINCT避免重复）")
    print("6. ✅ Improved time display（小时+分钟）")
    print("7. ✅ Added color coding for progress and accuracy")

if __name__ == '__main__':
    fix_progress_widget()
