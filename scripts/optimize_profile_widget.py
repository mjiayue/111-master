# -*- coding: utf-8 -*-
"""
优化个人主页脚本
"""

def optimize_profile_widget():
    """优化profile_widget.py"""

    with open('ui/profile_widget.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    skip_recent_section = False
    skip_count = 0

    for i, line in enumerate(lines):
        # 跳过最近学习记录部分（第132-145行）
        if '最近学习记录表' in line:
            skip_recent_section = True
            continue

        if skip_recent_section:
            # 跳过recent_group相关的13行代码
            if 'main_layout.addWidget(recent_group)' in line:
                skip_recent_section = False
            continue

        # 修改第26行：添加load_my_stats调用
        if 'self.load_recent_records()' in line and i == 25:
            new_lines.append(line)  # 保留load_recent_records
            new_lines.append('        self.load_my_stats()  # 加载统计数据\\n')
            continue

        # 增大数据卡片字体
        if \"t.setFont(QFont('Microsoft YaHei', 10))\" in line:
            line = line.replace(\"10\", \"12\")

        if \"v.setFont(QFont('Microsoft YaHei', 18, QFont.Bold))\" in line:
            line = line.replace(\"18\", \"22\")

        # 增大用户昵称字体
        if \"name_label.setFont(QFont('SF Pro Display', 14, QFont.Bold))\" in line:
            line = line.replace(\"14\", \"18\")

        new_lines.append(line)

    # 写入文件
    with open('ui/profile_widget.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print('OK - profile_widget.py optimized!')
    print('\\nModifications:')
    print('1. Added load_my_stats() call after init_ui')
    print('2. Removed recent learning records section')
    print('3. Increased stat badge fonts (12px/22px)')
    print('4. Increased nickname font (18px)')

if __name__ == '__main__':
    optimize_profile_widget()
