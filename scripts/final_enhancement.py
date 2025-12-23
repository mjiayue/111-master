# -*- coding: utf-8 -*-
"""
最终完善：添加更多高质量知识点和题目
确保项目内容丰富、专业
"""
from database.db_manager import db_manager
import json


def add_advanced_knowledge():
    """添加更多高级知识点"""
    db_manager.connect()

    advanced_knowledge = [
        # 字符串处理高级知识
        ("字符串处理", "字符串格式化",
         "Python提供多种字符串格式化方法：\n1. %格式化：'Hello %s' % name\n2. format()方法：'Hello {}'.format(name)\n3. f-string（推荐）：f'Hello {name}'\n\nf-string是Python 3.6+引入的新特性，最简洁高效。",
         "# 字符串格式化示例\nname = '张三'\nage = 20\nscore = 95.5\n\n# 方法1: %格式化\nprint('姓名：%s，年龄：%d' % (name, age))\n\n# 方法2: format()\nprint('姓名：{}，年龄：{}'.format(name, age))\n\n# 方法3: f-string（推荐）\nprint(f'姓名：{name}，年龄：{age}，成绩：{score:.1f}')",
         "medium", 1),

        ("字符串处理", "正则表达式",
         "正则表达式是处理字符串的强大工具，Python的re模块提供正则表达式支持。\n常用方法：\n- re.match()：从字符串开头匹配\n- re.search()：搜索整个字符串\n- re.findall()：找出所有匹配\n- re.sub()：替换匹配的内容",
         "import re\n\n# 验证邮箱格式\nemail = 'user@example.com'\npattern = r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\\.[a-zA-Z0-9_-]+)+$'\n\nif re.match(pattern, email):\n    print('邮箱格式正确')\n\n# 提取所有数字\ntext = '联系电话：138-1234-5678'\nnumbers = re.findall(r'\\d+', text)\nprint(f'提取的数字：{numbers}')",
         "hard", 2),

        # 列表与元组高级知识
        ("列表与元组", "列表推导式",
         "列表推导式是Python中创建列表的简洁方式。\n语法：[expression for item in iterable if condition]\n\n优点：\n1. 代码简洁\n2. 执行效率高\n3. 可读性强（适度使用）",
         "# 列表推导式示例\n\n# 创建1-10的平方列表\nsquares = [x**2 for x in range(1, 11)]\nprint(f'平方数：{squares}')\n\n# 筛选偶数\neven = [x for x in range(1, 21) if x % 2 == 0]\nprint(f'偶数：{even}')\n\n# 嵌套列表推导式\nmatrix = [[i*j for j in range(1, 4)] for i in range(1, 4)]\nprint(f'矩阵：{matrix}')",
         "medium", 3),

        ("列表与元组", "列表排序与反转",
         "Python提供多种列表排序方法：\n1. sort()：原地排序，改变原列表\n2. sorted()：返回新列表，不改变原列表\n3. reverse()：原地反转\n4. reversed()：返回迭代器\n\n可以通过key参数自定义排序规则。",
         "# 排序示例\nnumbers = [3, 1, 4, 1, 5, 9, 2, 6]\n\n# 原地排序\nnumbers.sort()\nprint(f'升序：{numbers}')\n\nnumbers.sort(reverse=True)\nprint(f'降序：{numbers}')\n\n# 按绝对值排序\ndata = [-5, 2, -3, 4, -1]\nsorted_data = sorted(data, key=abs)\nprint(f'按绝对值排序：{sorted_data}')",
         "medium", 4),

        # 字典与集合高级知识
        ("字典与集合", "字典推导式",
         "字典推导式类似列表推导式，用于创建字典。\n语法：{key: value for item in iterable if condition}\n\n可以快速创建字典、转换数据结构等。",
         "# 字典推导式示例\n\n# 创建平方字典\nsquares = {x: x**2 for x in range(1, 6)}\nprint(f'平方字典：{squares}')\n\n# 交换键值\noriginal = {'a': 1, 'b': 2, 'c': 3}\nswapped = {v: k for k, v in original.items()}\nprint(f'交换后：{swapped}')\n\n# 筛选字典\nscores = {'张三': 85, '李四': 92, '王五': 78}\nhigh_scores = {k: v for k, v in scores.items() if v >= 80}\nprint(f'高分：{high_scores}')",
         "medium", 6),

        # 函数高级知识
        ("函数", "Lambda表达式",
         "Lambda表达式用于创建匿名函数，语法简洁。\n语法：lambda 参数: 表达式\n\n常用场景：\n1. 作为参数传递给高阶函数\n2. 简单的一次性函数\n3. 配合map、filter、sorted等使用",
         "# Lambda表达式示例\n\n# 普通函数\ndef add(x, y):\n    return x + y\n\n# Lambda等价写法\nadd_lambda = lambda x, y: x + y\n\nprint(f'结果：{add_lambda(3, 5)}')\n\n# 配合sorted使用\nstudents = [('张三', 85), ('李四', 92), ('王五', 78)]\nsorted_students = sorted(students, key=lambda x: x[1], reverse=True)\nprint(f'按成绩排序：{sorted_students}')",
         "medium", 3),

        ("函数", "装饰器基础",
         "装饰器是Python的高级特性，用于在不修改函数代码的情况下增加功能。\n本质：装饰器是一个返回函数的函数。\n\n常见应用：\n1. 日志记录\n2. 性能测试\n3. 权限验证\n4. 缓存",
         "# 装饰器示例\nimport time\n\ndef timer(func):\n    \"\"\"计时装饰器\"\"\"\n    def wrapper(*args, **kwargs):\n        start = time.time()\n        result = func(*args, **kwargs)\n        end = time.time()\n        print(f'{func.__name__}耗时：{end-start:.4f}秒')\n        return result\n    return wrapper\n\n@timer\ndef slow_function():\n    time.sleep(1)\n    print('函数执行完成')\n\nslow_function()",
         "hard", 4),

        # 面向对象高级知识
        ("面向对象编程", "类的继承",
         "继承是面向对象编程的重要特性，允许创建基于现有类的新类。\n优点：\n1. 代码复用\n2. 建立类层次结构\n3. 支持多态\n\nPython支持单继承和多继承。",
         "# 继承示例\nclass Animal:\n    def __init__(self, name):\n        self.name = name\n    \n    def speak(self):\n        pass\n\nclass Dog(Animal):\n    def speak(self):\n        return f'{self.name}说：汪汪！'\n\nclass Cat(Animal):\n    def speak(self):\n        return f'{self.name}说：喵喵！'\n\ndog = Dog('旺财')\ncat = Cat('咪咪')\nprint(dog.speak())\nprint(cat.speak())",
         "medium", 2),

        ("面向对象编程", "类的封装",
         "封装是面向对象的三大特性之一，通过访问控制保护数据。\nPython的访问控制：\n1. public：公开属性（默认）\n2. _protected：受保护属性（约定）\n3. __private：私有属性（名称改写）",
         "# 封装示例\nclass BankAccount:\n    def __init__(self, owner, balance=0):\n        self.owner = owner          # 公开属性\n        self._balance = balance     # 受保护属性\n    \n    def deposit(self, amount):\n        \"\"\"存款\"\"\"\n        if amount > 0:\n            self._balance += amount\n            return True\n        return False\n    \n    def get_balance(self):\n        \"\"\"查询余额\"\"\"\n        return self._balance\n\naccount = BankAccount('张三', 1000)\naccount.deposit(500)\nprint(f'余额：{account.get_balance()}元')",
         "medium", 3),

        # 文件操作高级知识
        ("文件操作", "JSON文件处理",
         "JSON是常用的数据交换格式，Python的json模块提供了JSON处理功能。\n主要方法：\n- json.dump()：写入JSON文件\n- json.load()：读取JSON文件\n- json.dumps()：转换为JSON字符串\n- json.loads()：解析JSON字符串",
         "import json\n\n# 写入JSON文件\ndata = {\n    'name': '张三',\n    'age': 20,\n    'scores': [85, 90, 88]\n}\n\nwith open('data.json', 'w', encoding='utf-8') as f:\n    json.dump(data, f, ensure_ascii=False, indent=2)\n\n# 读取JSON文件\nwith open('data.json', 'r', encoding='utf-8') as f:\n    loaded_data = json.load(f)\n    print(loaded_data)",
         "medium", 2),

        ("文件操作", "CSV文件处理",
         "CSV是常用的表格数据格式，Python的csv模块提供了CSV处理功能。\n常用操作：\n1. 读取CSV：csv.reader()\n2. 写入CSV：csv.writer()\n3. 字典格式：csv.DictReader()、csv.DictWriter()",
         "import csv\n\n# 写入CSV文件\ndata = [\n    ['姓名', '年龄', '成绩'],\n    ['张三', 20, 85],\n    ['李四', 21, 92]\n]\n\nwith open('students.csv', 'w', newline='', encoding='utf-8') as f:\n    writer = csv.writer(f)\n    writer.writerows(data)\n\n# 读取CSV文件\nwith open('students.csv', 'r', encoding='utf-8') as f:\n    reader = csv.reader(f)\n    for row in reader:\n        print(row)",
         "medium", 3),
    ]

    count = 0
    for category, title, content, code_example, difficulty, order_num in advanced_knowledge:
        query = """
            INSERT INTO knowledge_points (category, title, content, code_example, difficulty, order_num)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        try:
            db_manager.insert(query, (category, title, content, code_example, difficulty, order_num))
            count += 1
        except Exception as e:
            print(f"插入知识点失败: {e}")

    db_manager.disconnect()
    return count


def add_advanced_questions():
    """添加更多高质量题目"""
    db_manager.connect()

    advanced_questions = [
        # 字符串处理高级题
        ("字符串处理", "choice", "Python中，以下哪种字符串格式化方式是Python 3.6+推荐的？",
         json.dumps(["A. %格式化", "B. format()方法", "C. f-string", "D. 字符串拼接"], ensure_ascii=False),
         "C", "f-string是Python 3.6引入的新特性，语法简洁、性能优秀，是推荐的格式化方式。", "medium"),

        ("字符串处理", "code", "使用f-string格式化输出：姓名张三，成绩85.5分（保留1位小数）",
         None,
         "name = '张三'\nscore = 85.5\nprint(f'姓名{name}，成绩{score:.1f}分')",
         "f-string使用{变量:.格式}语法进行格式化。", "medium"),

        # 列表推导式题
        ("列表与元组", "choice", "列表推导式 [x**2 for x in range(5)] 的结果是？",
         json.dumps(["A. [0, 1, 2, 3, 4]", "B. [1, 4, 9, 16, 25]", "C. [0, 1, 4, 9, 16]", "D. [1, 2, 3, 4, 5]"], ensure_ascii=False),
         "C", "range(5)生成0-4，列表推导式计算每个数的平方：[0, 1, 4, 9, 16]", "medium"),

        ("列表与元组", "code", "使用列表推导式创建1-10的偶数列表",
         None,
         "even_numbers = [x for x in range(1, 11) if x % 2 == 0]\nprint(even_numbers)",
         "列表推导式可以包含if条件进行过滤。", "easy"),

        # 字典推导式题
        ("字典与集合", "choice", "字典推导式的语法格式是？",
         json.dumps(["A. [key: value for item in iterable]", "B. {key: value for item in iterable}", "C. (key: value for item in iterable)", "D. {key, value for item in iterable}"], ensure_ascii=False),
         "B", "字典推导式使用花括号{}，格式为{key: value for item in iterable}", "easy"),

        ("字典与集合", "code", "创建字典，键为1-5，值为对应的平方",
         None,
         "squares = {x: x**2 for x in range(1, 6)}\nprint(squares)",
         "使用字典推导式可以快速创建字典。", "easy"),

        # Lambda表达式题
        ("函数", "choice", "Lambda表达式 lambda x: x * 2 的作用是？",
         json.dumps(["A. 返回x的一半", "B. 返回x的2倍", "C. 返回x的平方", "D. 返回x+2"], ensure_ascii=False),
         "B", "lambda x: x * 2 是一个匿名函数，返回参数的2倍。", "easy"),

        ("函数", "code", "使用lambda表达式和sorted()按成绩降序排序：[('张三',85),('李四',92)]",
         None,
         "students = [('张三', 85), ('李四', 92)]\nresult = sorted(students, key=lambda x: x[1], reverse=True)\nprint(result)",
         "lambda表达式常用作sorted的key参数。", "medium"),

        # 面向对象题
        ("面向对象编程", "choice", "在Python中，子类继承父类使用的语法是？",
         json.dumps(["A. class Child(Parent):", "B. class Child extends Parent:", "C. class Child inherits Parent:", "D. class Child <- Parent:"], ensure_ascii=False),
         "A", "Python使用class Child(Parent):语法实现继承。", "easy"),

        ("面向对象编程", "judge", "Python中，以双下划线开头的属性是私有属性。", None, "T",
         "以__开头的属性会进行名称改写，实现私有化。", "medium"),

        # JSON文件处理题
        ("文件操作", "choice", "Python中处理JSON文件使用哪个模块？",
         json.dumps(["A. json", "B. jsonlib", "C. simplejson", "D. ujson"], ensure_ascii=False),
         "A", "Python标准库提供json模块处理JSON数据。", "easy"),

        ("文件操作", "code", "将字典{'name':'张三','age':20}保存为JSON文件",
         None,
         "import json\ndata = {'name': '张三', 'age': 20}\nwith open('data.json', 'w', encoding='utf-8') as f:\n    json.dump(data, f, ensure_ascii=False)",
         "使用json.dump()保存JSON文件。", "medium"),

        # 常用标准库高级题
        ("常用标准库", "choice", "os.path.join()函数的作用是？",
         json.dumps(["A. 连接字符串", "B. 合并路径", "C. 创建目录", "D. 删除文件"], ensure_ascii=False),
         "B", "os.path.join()用于智能合并路径，自动处理不同操作系统的路径分隔符。", "easy"),

        ("常用标准库", "code", "使用datetime获取当前日期时间并格式化输出",
         None,
         "from datetime import datetime\nnow = datetime.now()\nprint(now.strftime('%Y-%m-%d %H:%M:%S'))",
         "datetime.now()获取当前时间，strftime()格式化输出。", "medium"),
    ]

    count = 0
    for category, q_type, question, options, answer, explanation, difficulty in advanced_questions:
        query = """
            INSERT INTO questions (category, type, question, options, answer, explanation, difficulty)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        try:
            db_manager.insert(query, (category, q_type, question, options, answer, explanation, difficulty))
            count += 1
        except Exception as e:
            print(f"插入题目失败: {e}")

    db_manager.disconnect()
    return count


if __name__ == '__main__':
    print("=" * 60)
    print("最终完善：添加高质量内容")
    print("=" * 60)

    knowledge_count = add_advanced_knowledge()
    print(f"\n新增知识点：{knowledge_count} 个")

    question_count = add_advanced_questions()
    print(f"新增题目：{question_count} 道")

    print("\n" + "=" * 60)
    print("项目完善完成！")
    print("=" * 60)
