# -*- coding: utf-8 -*-
"""
扩充题库数据
为后续分类添加题目
"""
from database.db_manager import db_manager
import json


def add_more_questions():
    """添加更多题目到数据库"""
    db_manager.connect()

    # 字符串处理题目
    string_questions = [
        ("字符串处理", "choice", "Python中，字符串的 upper() 方法的作用是？",
         json.dumps(["A. 转换为小写", "B. 转换为大写", "C. 首字母大写", "D. 反转字符串"], ensure_ascii=False),
         "B", "upper()方法将字符串中的所有字母转换为大写。", "easy"),

        ("字符串处理", "choice", "Python中，字符串的 split() 方法默认按什么分割？",
         json.dumps(["A. 逗号", "B. 空格", "C. 换行符", "D. 制表符"], ensure_ascii=False),
         "B", "split()方法默认按空格（包括空格、制表符、换行符等空白字符）分割字符串。", "easy"),

        ("字符串处理", "judge", "Python字符串是可变的。", None, "F",
         "Python字符串是不可变的，任何修改操作都会产生新的字符串对象。", "easy"),

        ("字符串处理", "fill", "使用___方法可以将字符串中的所有字母转换为小写。", None, "lower()",
         "lower()方法将字符串中的所有字母转换为小写。", "easy"),

        ("字符串处理", "code", "编写程序，将字符串'hello'重复3次并输出。", None,
         "s = 'hello'\nprint(s * 3)",
         "使用 * 运算符可以重复字符串。", "easy"),
    ]

    # 列表与元组题目
    list_tuple_questions = [
        ("列表与元组", "choice", "Python中，以下哪个方法用于在列表末尾添加元素？",
         json.dumps(["A. add()", "B. append()", "C. insert()", "D. extend()"], ensure_ascii=False),
         "B", "append()方法用于在列表末尾添加一个元素。", "easy"),

        ("列表与元组", "choice", "元组和列表的主要区别是？",
         json.dumps(["A. 元组更快", "B. 元组不可变", "C. 元组占用空间小", "D. 以上都对"], ensure_ascii=False),
         "D", "元组是不可变的，因此比列表更快，占用内存也更小。", "medium"),

        ("列表与元组", "judge", "元组创建后可以修改其中的元素。", None, "F",
         "元组是不可变的，创建后不能修改元素。", "easy"),

        ("列表与元组", "fill", "使用___方法可以删除列表中指定位置的元素并返回该元素。", None, "pop()",
         "pop()方法删除并返回指定位置的元素，默认删除最后一个。", "easy"),

        ("列表与元组", "code", "编写程序，创建包含1到5的列表并输出。", None,
         "numbers = [1, 2, 3, 4, 5]\nprint(numbers)",
         "使用方括号创建列表。", "easy"),
    ]

    # 字典与集合题目
    dict_set_questions = [
        ("字典与集合", "choice", "Python字典的键必须是？",
         json.dumps(["A. 字符串", "B. 数字", "C. 不可变类型", "D. 可变类型"], ensure_ascii=False),
         "C", "字典的键必须是不可变类型，如字符串、数字、元组等。", "medium"),

        ("字典与集合", "choice", "集合中的元素特点是？",
         json.dumps(["A. 有序且唯一", "B. 无序且唯一", "C. 有序可重复", "D. 无序可重复"], ensure_ascii=False),
         "B", "集合中的元素是无序且唯一的。", "easy"),

        ("字典与集合", "judge", "字典的键可以重复。", None, "F",
         "字典的键必须唯一，如果有重复的键，后面的值会覆盖前面的。", "easy"),

        ("字典与集合", "fill", "使用___方法可以获取字典中所有的键。", None, "keys()",
         "keys()方法返回字典中所有键的视图对象。", "easy"),

        ("字典与集合", "code", "编写程序，创建包含姓名和年龄的字典并输出。", None,
         "person = {'name': '张三', 'age': 20}\nprint(person)",
         "使用花括号创建字典，键值对用冒号分隔。", "easy"),
    ]

    # 文件操作题目
    file_questions = [
        ("文件操作", "choice", "Python中，以读写模式打开文件使用的参数是？",
         json.dumps(["A. 'r'", "B. 'w'", "C. 'r+'", "D. 'a'"], ensure_ascii=False),
         "C", "'r+'表示读写模式，文件必须存在。", "medium"),

        ("文件操作", "choice", "使用with语句打开文件的好处是？",
         json.dumps(["A. 自动关闭文件", "B. 更快的读写速度", "C. 可以同时打开多个文件", "D. 防止文件损坏"], ensure_ascii=False),
         "A", "with语句会自动关闭文件，即使发生异常也能确保文件被关闭。", "medium"),

        ("文件操作", "judge", "文件打开后必须手动调用close()方法关闭。", None, "F",
         "使用with语句打开文件会自动关闭，不需要手动调用close()。", "easy"),

        ("文件操作", "fill", "使用___方法可以读取文件的所有内容为一个字符串。", None, "read()",
         "read()方法读取整个文件内容并返回字符串。", "easy"),
    ]

    # 异常处理题目
    exception_questions = [
        ("异常处理", "choice", "Python中捕获异常使用的关键字是？",
         json.dumps(["A. catch", "B. except", "C. error", "D. handle"], ensure_ascii=False),
         "B", "Python使用try-except结构捕获异常，except用于指定要捕获的异常类型。", "easy"),

        ("异常处理", "choice", "以下哪个不是Python的内置异常？",
         json.dumps(["A. ValueError", "B. TypeError", "C. NullException", "D. KeyError"], ensure_ascii=False),
         "C", "Python中没有NullException，空值相关的是AttributeError或TypeError。", "medium"),

        ("异常处理", "judge", "finally块中的代码无论是否发生异常都会执行。", None, "T",
         "finally块中的代码总是会执行，常用于清理资源。", "easy"),

        ("异常处理", "fill", "使用___关键字可以手动抛出异常。", None, "raise",
         "raise关键字用于主动抛出异常。", "easy"),
    ]

    # 面向对象编程题目
    oop_questions = [
        ("面向对象编程", "choice", "Python中定义类使用的关键字是？",
         json.dumps(["A. class", "B. def", "C. object", "D. new"], ensure_ascii=False),
         "A", "Python使用class关键字定义类。", "easy"),

        ("面向对象编程", "choice", "Python中，__init__方法的作用是？",
         json.dumps(["A. 创建对象", "B. 初始化对象", "C. 销毁对象", "D. 复制对象"], ensure_ascii=False),
         "B", "__init__是构造方法，用于初始化对象的属性。", "medium"),

        ("面向对象编程", "judge", "Python支持多重继承。", None, "T",
         "Python支持多重继承，一个类可以继承多个父类。", "medium"),

        ("面向对象编程", "fill", "在类的方法中，第一个参数通常命名为___，表示实例本身。", None, "self",
         "self是约定俗成的参数名，表示类的实例对象本身。", "easy"),

        ("面向对象编程", "code", "编写一个简单的Student类，包含name属性。", None,
         "class Student:\n    def __init__(self, name):\n        self.name = name",
         "使用class定义类，__init__方法初始化属性。", "medium"),
    ]

    # 模块与包题目
    module_questions = [
        ("模块与包", "choice", "Python中导入模块使用的关键字是？",
         json.dumps(["A. include", "B. require", "C. import", "D. using"], ensure_ascii=False),
         "C", "Python使用import关键字导入模块。", "easy"),

        ("模块与包", "choice", "以下哪个是正确的导入方式？",
         json.dumps(["A. import math as m", "B. from math import *", "C. import math", "D. 以上都正确"], ensure_ascii=False),
         "D", "这三种都是正确的导入方式，但通常不推荐使用from module import *。", "medium"),

        ("模块与包", "judge", "一个.py文件就是一个模块。", None, "T",
         "在Python中，每个.py文件都可以作为一个模块被导入。", "easy"),

        ("模块与包", "fill", "使用___可以查看模块或对象的所有属性和方法。", None, "dir()",
         "dir()函数返回对象的所有属性和方法列表。", "medium"),
    ]

    # 常用标准库题目
    stdlib_questions = [
        ("常用标准库", "choice", "Python中，random模块的作用是？",
         json.dumps(["A. 文件处理", "B. 生成随机数", "C. 时间处理", "D. 数学计算"], ensure_ascii=False),
         "B", "random模块用于生成随机数和进行随机选择。", "easy"),

        ("常用标准库", "choice", "time.sleep()函数的作用是？",
         json.dumps(["A. 获取当前时间", "B. 计算时间差", "C. 暂停程序执行", "D. 设置系统时间"], ensure_ascii=False),
         "C", "time.sleep()函数使程序暂停执行指定的秒数。", "easy"),

        ("常用标准库", "judge", "datetime模块可以处理日期和时间。", None, "T",
         "datetime模块提供了处理日期和时间的类和函数。", "easy"),

        ("常用标准库", "fill", "使用os.path.___()可以判断路径是否存在。", None, "exists",
         "os.path.exists()函数用于检查路径是否存在。", "easy"),
    ]

    # 合并所有题目
    all_questions = (string_questions + list_tuple_questions + dict_set_questions +
                    file_questions + exception_questions + oop_questions +
                    module_questions + stdlib_questions)

    # 插入题目
    insert_count = 0
    for category, q_type, question, options, answer, explanation, difficulty in all_questions:
        query = """
            INSERT INTO questions (category, type, question, options, answer, explanation, difficulty)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        try:
            db_manager.insert(query, (category, q_type, question, options, answer, explanation, difficulty))
            insert_count += 1
        except Exception as e:
            print(f"插入失败: {e}")

    db_manager.disconnect()
    return insert_count


if __name__ == '__main__':
    print("=" * 60)
    print("扩充题库数据")
    print("=" * 60)

    count = add_more_questions()

    print(f"\n成功添加 {count} 道新题目！")
    print("=" * 60)
