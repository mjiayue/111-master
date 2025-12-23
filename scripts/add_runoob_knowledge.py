# -*- coding: utf-8 -*-
"""
从菜鸟教程抓取Python知识点
自动补充知识点数据
"""
import sqlite3
from config import DATABASE_PATH

# 菜鸟教程Python知识点（精选整理）
RUNOOB_KNOWLEDGE = {
    'Python基础': [
        {
            'title': 'Python简介与特点',
            'content': '''Python 是一个高层次的结合了解释性、编译性、互动性和面向对象的脚本语言。

**Python的特点：**
1. **易于学习**：Python有相对较少的关键字，结构简单，语法清晰，学习起来更加简单。
2. **易于阅读**：Python代码定义更清晰。
3. **易于维护**：Python的成功在于它的源代码易于维护。
4. **广泛的标准库**：Python的最大的优势之一是丰富的库，跨平台的。
5. **互动模式**：互动模式的支持，可以从终端输入执行代码并获得结果。
6. **可移植**：基于其开放源代码的特性，Python已经被移植到许多平台。
7. **可扩展**：如果你需要一段运行很快的关键代码，可以用C或C++编写。
8. **数据库**：Python提供所有主要的商业数据库的接口。
9. **GUI编程**：Python支持GUI，可以创建和移植到许多系统调用。
10. **可嵌入**：你可以将Python嵌入到C/C++程序，让你的程序获得"脚本化"能力。''',
            'code_example': '''# Python简单示例
print("Hello, World!")

# Python是解释型语言
# 不需要编译，直接运行

# Python支持多种数据类型
number = 100
name = "Python"
is_easy = True

print(f"{name}的版本号是{number}，容易学吗？{is_easy}")''',
            'difficulty': 'easy'
        },
        {
            'title': 'Python环境搭建',
            'content': '''**Python下载安装：**
1. 访问Python官网 www.python.org
2. 下载最新版本的Python
3. 安装时勾选"Add Python to PATH"
4. 验证安装：打开命令行，输入 python --version

**Python IDE选择：**
- **IDLE**：Python自带的集成开发环境
- **PyCharm**：专业的Python IDE
- **VS Code**：轻量级代码编辑器
- **Jupyter Notebook**：适合数据分析

**第一个Python程序：**
1. 打开文本编辑器
2. 输入代码：print("Hello, World!")
3. 保存为 hello.py
4. 运行：python hello.py''',
            'code_example': '''# 检查Python版本
import sys
print("Python版本:", sys.version)

# 检查已安装的模块
import pip
installed_packages = pip.get_installed_distributions()
print("已安装的包数量:", len(list(installed_packages)))

# 交互式Python
# 在命令行输入python进入交互模式
# >>> print("Hello")
# Hello
# >>> 1 + 1
# 2''',
            'difficulty': 'easy'
        },
        {
            'title': 'Python基本语法',
            'content': '''**Python标识符：**
- 第一个字符必须是字母或下划线 _
- 其他部分可以是字母、数字或下划线
- 大小写敏感

**Python保留字：**
and, or, not, if, elif, else, while, for, in, break, continue, pass, def, class, return, yield, import, from, as, try, except, finally, raise, with, lambda, True, False, None等。

**行和缩进：**
Python最具特色的就是使用缩进来表示代码块，不需要使用大括号{}。
缩进的空格数是可变的，但是同一个代码块的语句必须包含相同的缩进空格数。

**注释：**
- 单行注释：# 这是注释
- 多行注释：三个引号 \'''注释内容\''' 或 """注释内容"""''',
            'code_example': '''# 变量赋值
counter = 100          # 整型变量
miles = 1000.0        # 浮点型变量
name = "runoob"       # 字符串

# 多个变量赋值
a = b = c = 1
x, y, z = 1, 2, "hello"

# 代码块和缩进
if True:
    print("True")  # 4个空格缩进
else:
    print("False") # 同样的缩进

# 多行语句
total = 1 + \\
        2 + \\
        3

# 同一行显示多条语句
import sys; x = 'runoob'; print(x)''',
            'difficulty': 'easy'
        },
        {
            'title': 'Python输入输出',
            'content': '''**输出函数 print()：**
- 最常用的输出函数
- 可以输出多个值，用逗号分隔
- 支持格式化输出

**输入函数 input()：**
- 接收用户输入
- 返回值为字符串类型
- 可以设置提示信息

**格式化输出：**
1. **%格式化**：使用 % 操作符
2. **str.format()**：使用 format 方法
3. **f-string**：Python 3.6+ 的格式化字符串字面值''',
            'code_example': '''# 基本输出
print("Hello, World!")
print("Python", "很", "强大")

# 格式化输出
name = "张三"
age = 20

# 方法1: % 格式化
print("姓名: %s, 年龄: %d" % (name, age))

# 方法2: format方法
print("姓名: {}, 年龄: {}".format(name, age))
print("姓名: {0}, 年龄: {1}, 再次提醒: {0}".format(name, age))

# 方法3: f-string (推荐)
print(f"姓名: {name}, 年龄: {age}")

# 输入
user_name = input("请输入你的名字: ")
print(f"欢迎你，{user_name}!")

# 输入数字需要类型转换
age = int(input("请输入年龄: "))
print(f"你的年龄是 {age} 岁")''',
            'difficulty': 'easy'
        }
    ],

    '数据类型': [
        {
            'title': '数字类型详解',
            'content': '''Python 支持三种不同的数字类型：
1. **整型(int)**：通常被称为整型或整数，是正或负整数，不带小数点
2. **浮点型(float)**：由整数部分与小数部分组成
3. **复数(complex)**：由实数部分和虚数部分构成，如 a + bj

**数字类型转换：**
- int(x)：将x转换为一个整数
- float(x)：将x转换到一个浮点数
- complex(x)：将x转换到一个复数

**数学函数：**
abs(), max(), min(), pow(), round(), math.sqrt(), math.ceil(), math.floor()等''',
            'code_example': '''# 整型
a = 100
b = -20
c = 0

# 浮点型
pi = 3.14159
e = 2.71828

# 复数
z = 3 + 4j
print(z.real)  # 实部: 3.0
print(z.imag)  # 虚部: 4.0

# 类型转换
x = 10
y = float(x)    # 10.0
z = complex(x)  # (10+0j)

# 数学运算
print(10 + 3)   # 加法: 13
print(10 - 3)   # 减法: 7
print(10 * 3)   # 乘法: 30
print(10 / 3)   # 除法: 3.333...
print(10 // 3)  # 整除: 3
print(10 % 3)   # 取余: 1
print(10 ** 3)  # 幂运算: 1000

# 数学函数
import math
print(abs(-10))        # 绝对值: 10
print(max(1, 5, 3))    # 最大值: 5
print(min(1, 5, 3))    # 最小值: 1
print(pow(2, 3))       # 2的3次方: 8
print(round(3.14159, 2))  # 四舍五入: 3.14
print(math.sqrt(16))   # 平方根: 4.0''',
            'difficulty': 'easy'
        },
        {
            'title': '字符串类型',
            'content': '''**字符串创建：**
- 单引号：'hello'
- 双引号："hello"
- 三引号：\'''hello\''' 或 """hello"""（支持多行）

**字符串特点：**
1. 不可变：字符串一旦创建，不能修改
2. 有序：可以通过索引访问
3. 可迭代：可以遍历每个字符

**字符串索引：**
- 正向索引：从0开始
- 反向索引：从-1开始（最后一个字符）

**字符串切片：**
str[start:end:step]''',
            'code_example': '''# 字符串创建
s1 = 'hello'
s2 = "world"
s3 = \'''多行
字符串\'''

# 字符串拼接
greeting = s1 + " " + s2
print(greeting)  # hello world

# 字符串重复
print("=" * 20)  # ====================

# 字符串索引
text = "Python"
print(text[0])   # P (第一个字符)
print(text[-1])  # n (最后一个字符)

# 字符串切片
print(text[0:3])   # Pyt
print(text[2:])    # thon
print(text[:4])    # Pyth
print(text[::2])   # Pto (步长为2)
print(text[::-1])  # nohtyP (反转)

# 字符串方法
s = "  Hello World  "
print(s.lower())       # 转小写
print(s.upper())       # 转大写
print(s.strip())       # 去除首尾空格
print(s.replace("o", "0"))  # 替换
print(s.split())       # 分割成列表

# 字符串判断
print("Hello".startswith("H"))  # True
print("Hello".endswith("o"))    # True
print("123".isdigit())          # True
print("abc".isalpha())          # True''',
            'difficulty': 'easy'
        }
    ],

    '列表与元组': [
        {
            'title': '列表(List)详解',
            'content': '''**列表特点：**
1. 有序：元素按照添加顺序排列
2. 可变：可以修改、添加、删除元素
3. 可重复：允许重复元素
4. 异构：可以包含不同类型的元素

**列表创建：**
- 方括号：[1, 2, 3]
- list()函数：list("abc")

**列表操作：**
- 访问：list[index]
- 切片：list[start:end]
- 添加：append(), insert(), extend()
- 删除：remove(), pop(), del, clear()
- 其他：sort(), reverse(), copy()''',
            'code_example': '''# 列表创建
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]
nested = [[1, 2], [3, 4], [5, 6]]

# 列表访问
print(numbers[0])      # 1
print(numbers[-1])     # 5
print(numbers[1:4])    # [2, 3, 4]

# 列表修改
numbers[0] = 10
print(numbers)         # [10, 2, 3, 4, 5]

# 添加元素
numbers.append(6)      # 末尾添加
numbers.insert(0, 0)   # 指定位置插入
numbers.extend([7, 8]) # 扩展列表

# 删除元素
numbers.remove(10)     # 删除指定值
last = numbers.pop()   # 删除最后一个
del numbers[0]         # 删除指定索引
numbers.clear()        # 清空列表

# 列表方法
lst = [3, 1, 4, 1, 5, 9, 2, 6]
print(len(lst))        # 长度: 8
print(max(lst))        # 最大值: 9
print(min(lst))        # 最小值: 1
print(lst.count(1))    # 统计1出现次数: 2
print(lst.index(5))    # 查找5的索引: 4

lst.sort()             # 排序
print(lst)             # [1, 1, 2, 3, 4, 5, 6, 9]

lst.reverse()          # 反转
print(lst)             # [9, 6, 5, 4, 3, 2, 1, 1]

# 列表推导式
squares = [x**2 for x in range(10)]
print(squares)         # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

even = [x for x in range(20) if x % 2 == 0]
print(even)            # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]''',
            'difficulty': 'medium'
        },
        {
            'title': '元组(Tuple)详解',
            'content': '''**元组特点：**
1. 有序：元素按照添加顺序排列
2. 不可变：创建后不能修改
3. 可重复：允许重复元素
4. 异构：可以包含不同类型的元素

**元组 vs 列表：**
- 元组使用圆括号()，列表使用方括号[]
- 元组不可变，列表可变
- 元组更快，占用空间更小
- 元组可作为字典的键，列表不行

**元组操作：**
- 访问：tuple[index]
- 切片：tuple[start:end]
- 连接：tuple1 + tuple2
- 重复：tuple * n
- 成员：in, not in''',
            'code_example': '''# 元组创建
t1 = (1, 2, 3)
t2 = 1, 2, 3           # 省略括号
t3 = (1,)              # 单元素元组，注意逗号
t4 = tuple([1, 2, 3])  # 从列表创建

# 元组访问
print(t1[0])           # 1
print(t1[-1])          # 3
print(t1[1:])          # (2, 3)

# 元组不可修改
# t1[0] = 10  # TypeError: 'tuple' object does not support item assignment

# 但如果元组包含可变对象，可变对象的内容可以修改
t5 = ([1, 2], [3, 4])
t5[0].append(3)
print(t5)              # ([1, 2, 3], [3, 4])

# 元组操作
t6 = (1, 2) + (3, 4)   # 连接: (1, 2, 3, 4)
t7 = (1, 2) * 3        # 重复: (1, 2, 1, 2, 1, 2)

# 元组解包
a, b, c = (1, 2, 3)
print(a, b, c)         # 1 2 3

# 交换变量
x, y = 10, 20
x, y = y, x
print(x, y)            # 20 10

# 元组方法
t8 = (1, 2, 3, 1, 2, 1)
print(t8.count(1))     # 统计1出现次数: 3
print(t8.index(2))     # 查找2的索引: 1

# 元组用途：作为字典的键
coordinates = {(0, 0): "原点", (1, 1): "对角"}
print(coordinates[(0, 0)])  # 原点''',
            'difficulty': 'medium'
        }
    ]
}


def add_runoob_knowledge():
    """添加菜鸟教程的知识点到数据库"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        print("=" * 60)
        print("   从菜鸟教程补充Python知识点")
        print("=" * 60)
        print()

        total_added = 0

        for category, knowledge_list in RUNOOB_KNOWLEDGE.items():
            print(f"\n处理分类: {category}")
            print("-" * 40)

            for knowledge in knowledge_list:
                # 检查是否已存在
                cursor.execute('''
                    SELECT COUNT(*) FROM knowledge_points
                    WHERE category = ? AND title = ?
                ''', (category, knowledge['title']))

                if cursor.fetchone()[0] > 0:
                    print(f"  [跳过] {knowledge['title']} (已存在)")
                    continue

                # 插入知识点
                cursor.execute('''
                    INSERT INTO knowledge_points
                    (category, title, content, code_example, difficulty)
                    VALUES (?, ?, ?, ?, ?)
                ''', (category, knowledge['title'], knowledge['content'],
                      knowledge['code_example'], knowledge['difficulty']))

                print(f"  [OK] 添加: {knowledge['title']}")
                total_added += 1

        conn.commit()
        conn.close()

        print()
        print("=" * 60)
        print(f"   成功添加 {total_added} 个知识点！")
        print("=" * 60)
        print()
        print("现在知识点数量：")

        # 显示最新统计
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT category, COUNT(*) FROM knowledge_points GROUP BY category')
        for row in cursor.fetchall():
            print(f"  • {row[0]}: {row[1]}个")
        conn.close()

        return True

    except Exception as e:
        print(f"\n[错误] 添加知识点失败: {e}")
        return False


if __name__ == '__main__':
    success = add_runoob_knowledge()

    if success:
        print("\n[成功] 知识点数据已更新！")
    else:
        print("\n[失败] 知识点更新失败")

    input("\n按回车键退出...")
