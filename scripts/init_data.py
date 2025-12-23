# -*- coding: utf-8 -*-
"""
数据初始化脚本
添加Python学习相关的知识点和题目数据
"""
from database.db_manager import db_manager
import json


def init_knowledge_data():
    """初始化知识点数据"""
    db_manager.connect()

    knowledge_data = [
        # Python基础
        ("Python基础", "Python简介", "Python是一种解释型、面向对象、动态数据类型的高级程序设计语言。由Guido van Rossum于1989年底发明，第一个公开发行版发行于1991年。Python语法简洁清晰，特色之一是强制用空白符作为语句缩进。",
         "# Python的Hello World程序\nprint('Hello, World!')\n\n# Python的特点：简洁、易读、易学", "easy", 1),

        ("Python基础", "Python的特点", "Python具有以下特点：\n1. 简单易学：Python语法简洁明了\n2. 免费开源：Python是开源软件\n3. 跨平台：可在Windows、Linux、MacOS等系统运行\n4. 面向对象：支持面向对象编程\n5. 丰富的库：拥有大量第三方库\n6. 可扩展性：可以用C/C++编写扩展模块",
         "# Python的跨平台特性\nimport platform\nprint(f'当前系统: {platform.system()}')\nprint(f'Python版本: {platform.python_version()}')", "easy", 2),

        ("Python基础", "Python开发环境", "Python开发环境包括：\n1. Python解释器：执行Python代码的核心程序\n2. IDLE：Python自带的集成开发环境\n3. PyCharm：专业的Python IDE\n4. VS Code：轻量级但功能强大的编辑器\n5. Jupyter Notebook：交互式编程环境",
         "# 查看Python安装路径\nimport sys\nprint(f'Python路径: {sys.executable}')\nprint(f'Python版本: {sys.version}')", "easy", 3),

        # 数据类型
        ("数据类型", "数字类型", "Python支持三种数字类型：\n1. 整数（int）：如 10, -5, 0\n2. 浮点数（float）：如 3.14, -0.5\n3. 复数（complex）：如 3+4j\n\n数字类型是不可变的，可以进行算术运算。",
         "# 数字类型示例\na = 10          # 整数\nb = 3.14        # 浮点数\nc = 3 + 4j      # 复数\n\nprint(f'整数: {a}, 类型: {type(a)}')\nprint(f'浮点数: {b}, 类型: {type(b)}')\nprint(f'复数: {c}, 类型: {type(c)}')", "easy", 1),

        ("数据类型", "字符串类型", "字符串是由字符组成的序列，用单引号或双引号括起来。\n特点：\n1. 不可变：字符串内容不能修改\n2. 可索引：通过索引访问单个字符\n3. 可切片：获取子字符串\n4. 支持运算：连接（+）、重复（*）",
         "# 字符串操作\ns = 'Hello, Python!'\n\n# 索引\nprint(f'第1个字符: {s[0]}')\n\n# 切片\nprint(f'前5个字符: {s[0:5]}')\n\n# 连接和重复\nprint(f'连接: {s + \" 编程\"}')\nprint(f'重复: {\"Python \" * 3}')", "easy", 2),

        ("数据类型", "列表类型", "列表（list）是Python中最常用的数据类型之一。\n特点：\n1. 有序：元素有固定的顺序\n2. 可变：可以修改元素\n3. 可重复：允许重复元素\n4. 支持多种类型：元素可以是不同类型",
         "# 列表操作\nfruits = ['apple', 'banana', 'orange']\n\n# 添加元素\nfruits.append('grape')\nprint(f'添加后: {fruits}')\n\n# 修改元素\nfruits[0] = 'pear'\nprint(f'修改后: {fruits}')\n\n# 删除元素\nfruits.remove('banana')\nprint(f'删除后: {fruits}')", "medium", 3),

        ("数据类型", "元组类型", "元组（tuple）与列表类似，但是不可变的。\n特点：\n1. 有序：元素有固定的顺序\n2. 不可变：创建后不能修改\n3. 可重复：允许重复元素\n4. 用圆括号表示：如 (1, 2, 3)",
         "# 元组操作\npoint = (10, 20)\nprint(f'坐标: {point}')\n\n# 元组解包\nx, y = point\nprint(f'x={x}, y={y}')\n\n# 元组不可修改（会报错）\n# point[0] = 30  # TypeError", "easy", 4),

        ("数据类型", "字典类型", "字典（dict）是Python中的映射类型，存储键值对。\n特点：\n1. 无序：Python 3.7+保持插入顺序\n2. 可变：可以修改、添加、删除键值对\n3. 键唯一：键不能重复\n4. 快速查找：通过键快速访问值",
         "# 字典操作\nstudent = {\n    'name': '张三',\n    'age': 20,\n    'grade': 85\n}\n\n# 访问\nprint(f'姓名: {student[\"name\"]}')\n\n# 添加\nstudent['gender'] = '男'\n\n# 修改\nstudent['age'] = 21\n\nprint(f'学生信息: {student}')", "medium", 5),

        ("数据类型", "集合类型", "集合（set）是无序且元素唯一的数据类型。\n特点：\n1. 无序：元素没有固定顺序\n2. 唯一：自动去除重复元素\n3. 可变：可以添加、删除元素\n4. 支持集合运算：并集、交集、差集",
         "# 集合操作\nset1 = {1, 2, 3, 4}\nset2 = {3, 4, 5, 6}\n\n# 并集\nprint(f'并集: {set1 | set2}')\n\n# 交集\nprint(f'交集: {set1 & set2}')\n\n# 差集\nprint(f'差集: {set1 - set2}')\n\n# 去重\nnums = [1, 2, 2, 3, 3, 3]\nunique = list(set(nums))\nprint(f'去重: {unique}')", "medium", 6),

        # 运算符与表达式
        ("运算符与表达式", "算术运算符", "Python支持的算术运算符：\n+ 加法\n- 减法\n* 乘法\n/ 除法（结果为浮点数）\n// 整除（结果为整数）\n% 取模（求余数）\n** 幂运算",
         "# 算术运算符示例\na, b = 10, 3\n\nprint(f'{a} + {b} = {a + b}')\nprint(f'{a} - {b} = {a - b}')\nprint(f'{a} * {b} = {a * b}')\nprint(f'{a} / {b} = {a / b}')\nprint(f'{a} // {b} = {a // b}')\nprint(f'{a} % {b} = {a % b}')\nprint(f'{a} ** {b} = {a ** b}')", "easy", 1),

        ("运算符与表达式", "比较运算符", "Python支持的比较运算符：\n== 等于\n!= 不等于\n> 大于\n< 小于\n>= 大于等于\n<= 小于等于\n\n比较运算符返回布尔值（True或False）",
         "# 比较运算符示例\na, b = 10, 5\n\nprint(f'{a} == {b}: {a == b}')\nprint(f'{a} != {b}: {a != b}')\nprint(f'{a} > {b}: {a > b}')\nprint(f'{a} < {b}: {a < b}')\nprint(f'{a} >= {b}: {a >= b}')\nprint(f'{a} <= {b}: {a <= b}')", "easy", 2),

        ("运算符与表达式", "逻辑运算符", "Python支持的逻辑运算符：\nand 逻辑与：两个条件都为True时返回True\nor 逻辑或：至少一个条件为True时返回True\nnot 逻辑非：对条件取反\n\n逻辑运算符用于组合多个条件。",
         "# 逻辑运算符示例\na, b = True, False\n\nprint(f'{a} and {b} = {a and b}')\nprint(f'{a} or {b} = {a or b}')\nprint(f'not {a} = {not a}')\nprint(f'not {b} = {not b}')\n\n# 实际应用\nx = 10\nprint(f'{x} 在 1-20 之间: {1 <= x <= 20}')", "easy", 3),

        # 流程控制
        ("流程控制", "if条件语句", "if语句用于条件判断。\n语法：\nif 条件:\n    语句块1\nelif 条件2:\n    语句块2\nelse:\n    语句块3\n\n注意：Python使用缩进来表示代码块。",
         "# if条件语句示例\nscore = 85\n\nif score >= 90:\n    grade = 'A'\nelif score >= 80:\n    grade = 'B'\nelif score >= 70:\n    grade = 'C'\nelif score >= 60:\n    grade = 'D'\nelse:\n    grade = 'F'\n\nprint(f'分数{score}，等级{grade}')", "easy", 1),

        ("流程控制", "for循环", "for循环用于遍历序列（如列表、元组、字符串）。\n语法：\nfor 变量 in 序列:\n    语句块\n\nrange()函数常与for循环一起使用，生成数字序列。",
         "# for循环示例\n\n# 遍历列表\nfruits = ['apple', 'banana', 'orange']\nfor fruit in fruits:\n    print(fruit)\n\n# 使用range\nfor i in range(1, 6):\n    print(f'{i}的平方是{i**2}')\n\n# 遍历字符串\nfor char in 'Python':\n    print(char, end=' ')", "easy", 2),

        ("流程控制", "while循环", "while循环在条件为True时重复执行。\n语法：\nwhile 条件:\n    语句块\n\n注意：要确保循环能够终止，避免无限循环。",
         "# while循环示例\n\n# 倒计时\ncount = 5\nwhile count > 0:\n    print(f'倒计时: {count}')\n    count -= 1\nprint('发射！')\n\n# 求和\nsum_val = 0\ni = 1\nwhile i <= 10:\n    sum_val += i\n    i += 1\nprint(f'1到10的和: {sum_val}')", "easy", 3),

        ("流程控制", "break和continue", "break：跳出循环\ncontinue：跳过本次循环，继续下一次循环\n\n这两个语句用于控制循环的执行流程。",
         "# break和continue示例\n\n# break示例：查找第一个偶数\nfor i in range(1, 10):\n    if i % 2 == 0:\n        print(f'找到第一个偶数: {i}')\n        break\n\n# continue示例：打印奇数\nfor i in range(1, 10):\n    if i % 2 == 0:\n        continue\n    print(f'奇数: {i}')", "medium", 4),

        # 函数
        ("函数", "函数定义", "函数是组织好的、可重复使用的代码块。\n定义函数使用def关键字：\ndef 函数名(参数):\n    函数体\n    return 返回值\n\n函数可以接收参数并返回结果。",
         "# 函数定义示例\n\ndef greet(name):\n    \"\"\"问候函数\"\"\"\n    return f'你好, {name}！'\n\ndef add(a, b):\n    \"\"\"两数相加\"\"\"\n    return a + b\n\n# 调用函数\nprint(greet('张三'))\nprint(f'5 + 3 = {add(5, 3)}')", "easy", 1),

        ("函数", "函数参数", "Python函数支持多种参数类型：\n1. 位置参数：按位置传递\n2. 默认参数：有默认值的参数\n3. 关键字参数：按参数名传递\n4. 可变参数：*args和**kwargs",
         "# 函数参数示例\n\ndef info(name, age=18, city='北京'):\n    \"\"\"默认参数示例\"\"\"\n    print(f'{name}, {age}岁, 来自{city}')\n\n# 位置参数\ninfo('张三', 20, '上海')\n\n# 默认参数\ninfo('李四')\n\n# 关键字参数\ninfo(city='广州', name='王五', age=25)", "medium", 2),

    ]

    for category, title, content, code_example, difficulty, order_num in knowledge_data:
        query = """
            INSERT INTO knowledge_points (category, title, content, code_example, difficulty, order_num)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        db_manager.insert(query, (category, title, content, code_example, difficulty, order_num))

    print(f"已添加 {len(knowledge_data)} 条知识点数据")

    db_manager.disconnect()


def init_question_data():
    """初始化题目数据"""
    db_manager.connect()

    # 选择题数据
    choice_questions = [
        ("Python基础", "choice", "Python是一种什么类型的语言？",
         json.dumps(["A. 编译型语言", "B. 解释型语言", "C. 汇编语言", "D. 机器语言"], ensure_ascii=False),
         "B", "Python是解释型语言，代码在执行时逐行解释执行，不需要事先编译。", "easy"),

        ("Python基础", "choice", "Python中用于输出内容的函数是？",
         json.dumps(["A. input()", "B. print()", "C. output()", "D. write()"], ensure_ascii=False),
         "B", "print()函数用于输出内容到控制台。", "easy"),

        ("Python基础", "choice", "Python中的注释符号是？",
         json.dumps(["A. //", "B. /* */", "C. #", "D. --"], ensure_ascii=False),
         "C", "Python使用#进行单行注释，使用三引号进行多行注释。", "easy"),

        ("数据类型", "choice", "以下哪个不是Python的基本数据类型？",
         json.dumps(["A. int", "B. float", "C. char", "D. str"], ensure_ascii=False),
         "C", "Python没有char类型，字符也是使用str类型表示。", "medium"),

        ("数据类型", "choice", "Python中表示空值的关键字是？",
         json.dumps(["A. null", "B. NULL", "C. None", "D. nil"], ensure_ascii=False),
         "C", "Python使用None表示空值。", "easy"),

        ("运算符与表达式", "choice", "Python中，3 // 2 的结果是？",
         json.dumps(["A. 1", "B. 1.5", "C. 2", "D. 1.0"], ensure_ascii=False),
         "A", "//是整除运算符，结果取整数部分，3 // 2 = 1。", "easy"),

        ("运算符与表达式", "choice", "Python中，2 ** 3 的结果是？",
         json.dumps(["A. 5", "B. 6", "C. 8", "D. 9"], ensure_ascii=False),
         "C", "**是幂运算符，2 ** 3 = 2³ = 8。", "easy"),

        ("流程控制", "choice", "Python中用于跳出循环的关键字是？",
         json.dumps(["A. exit", "B. break", "C. continue", "D. return"], ensure_ascii=False),
         "B", "break用于跳出整个循环，continue用于跳过本次循环。", "easy"),

        ("函数", "choice", "Python中定义函数使用的关键字是？",
         json.dumps(["A. function", "B. func", "C. def", "D. define"], ensure_ascii=False),
         "C", "Python使用def关键字定义函数。", "easy"),

        ("函数", "choice", "以下关于函数参数的说法，错误的是？",
         json.dumps(["A. 位置参数必须在前", "B. 默认参数必须在后", "C. 可变参数可以接收任意个参数", "D. 关键字参数必须在位置参数之前"], ensure_ascii=False),
         "D", "关键字参数必须在位置参数之后，不能在之前。", "medium"),
    ]

    for category, q_type, question, options, answer, explanation, difficulty in choice_questions:
        query = """
            INSERT INTO questions (category, type, question, options, answer, explanation, difficulty)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        db_manager.insert(query, (category, q_type, question, options, answer, explanation, difficulty))

    print(f"已添加 {len(choice_questions)} 道选择题")

    # 判断题数据
    judge_questions = [
        ("Python基础", "judge", "Python是一种强类型语言。", None, "T",
         "Python是强类型语言，变量类型在运行时确定，但不会自动进行不兼容的类型转换。", "easy"),

        ("Python基础", "judge", "Python中的缩进只是为了美观，没有实际作用。", None, "F",
         "Python使用缩进来表示代码块，缩进是语法的一部分，具有实际作用。", "easy"),

        ("数据类型", "judge", "Python中的列表是不可变的。", None, "F",
         "列表是可变的，可以修改、添加、删除元素。元组才是不可变的。", "easy"),

        ("数据类型", "judge", "Python字符串可以使用单引号或双引号定义。", None, "T",
         "Python中的字符串可以使用单引号、双引号或三引号定义。", "easy"),

        ("运算符与表达式", "judge", "Python中，== 和 = 的作用相同。", None, "F",
         "== 是比较运算符，用于判断相等；= 是赋值运算符，用于赋值。", "easy"),

        ("流程控制", "judge", "Python中的else可以与for循环一起使用。", None, "T",
         "Python的for和while循环都可以有else子句，当循环正常结束时执行。", "medium"),

        ("函数", "judge", "Python函数必须有返回值。", None, "F",
         "Python函数可以没有返回值，此时默认返回None。", "easy"),

        ("函数", "judge", "Python中，函数可以返回多个值。", None, "T",
         "Python函数可以返回多个值，实际上是返回一个元组。", "medium"),
    ]

    for category, q_type, question, options, answer, explanation, difficulty in judge_questions:
        query = """
            INSERT INTO questions (category, type, question, options, answer, explanation, difficulty)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        db_manager.insert(query, (category, q_type, question, options, answer, explanation, difficulty))

    print(f"已添加 {len(judge_questions)} 道判断题")

    # 填空题数据
    fill_questions = [
        ("Python基础", "fill", "Python中用于输入的函数是___。", None, "input()",
         "input()函数用于从控制台接收用户输入。", "easy"),

        ("数据类型", "fill", "Python中，type()函数用于___。", None, "查看数据类型",
         "type()函数用于返回对象的类型。", "easy"),

        ("运算符与表达式", "fill", "Python中，7 % 3 的结果是___。", None, "1",
         "%是取模运算符，7 % 3 = 1（7除以3的余数）。", "easy"),

        ("流程控制", "fill", "Python中，用于跳过本次循环继续下一次循环的关键字是___。", None, "continue",
         "continue用于跳过本次循环的剩余代码，直接进入下一次循环。", "easy"),

        ("函数", "fill", "Python中，lambda表达式用于创建___函数。", None, "匿名",
         "lambda表达式用于创建简单的匿名函数。", "medium"),
    ]

    for category, q_type, question, options, answer, explanation, difficulty in fill_questions:
        query = """
            INSERT INTO questions (category, type, question, options, answer, explanation, difficulty)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        db_manager.insert(query, (category, q_type, question, options, answer, explanation, difficulty))

    print(f"已添加 {len(fill_questions)} 道填空题")

    # 编程题数据
    code_questions = [
        ("Python基础", "code", "编写程序，输出'Hello, Python!'", None,
         "print('Hello, Python!')",
         "使用print()函数输出字符串。", "easy"),

        ("数据类型", "code", "编写程序，创建一个列表[1, 2, 3]并输出。", None,
         "numbers = [1, 2, 3]\nprint(numbers)",
         "使用方括号创建列表，然后用print()输出。", "easy"),

        ("运算符与表达式", "code", "编写程序，计算1到10的和并输出结果。", None,
         "total = sum(range(1, 11))\nprint(total)",
         "使用sum()和range()函数计算1到10的和。", "medium"),

        ("流程控制", "code", "编写程序，使用for循环输出1到5的数字。", None,
         "for i in range(1, 6):\n    print(i)",
         "使用for循环和range()函数遍历1到5的数字。", "easy"),

        ("函数", "code", "编写一个函数，接收两个数并返回它们的和。", None,
         "def add(a, b):\n    return a + b",
         "使用def定义函数，使用return返回结果。", "easy"),
    ]

    for category, q_type, question, options, answer, explanation, difficulty in code_questions:
        query = """
            INSERT INTO questions (category, type, question, options, answer, explanation, difficulty)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        db_manager.insert(query, (category, q_type, question, options, answer, explanation, difficulty))

    print(f"已添加 {len(code_questions)} 道编程题")

    db_manager.disconnect()


def main():
    """主函数"""
    print("=" * 50)
    print("Python学习教辅系统 - 数据初始化")
    print("=" * 50)

    print("\n开始初始化知识点数据...")
    init_knowledge_data()

    print("\n开始初始化题目数据...")
    init_question_data()

    # 统计实际数据量
    db_manager.connect()
    kp_result = db_manager.execute_query("SELECT COUNT(*) FROM knowledge_points")
    q_result = db_manager.execute_query("SELECT COUNT(*) FROM questions")
    kp_count = kp_result[0][0] if kp_result else 0
    q_count = q_result[0][0] if q_result else 0
    db_manager.disconnect()

    print("\n" + "=" * 50)
    print("数据初始化完成！")
    print("=" * 50)
    print(f"\n数据库统计：")
    print(f"  知识点总数：{kp_count} 条")
    print(f"  题目总数：{q_count} 道")
    print("=" * 50)


if __name__ == '__main__':
    main()
