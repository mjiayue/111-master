# -*- coding: utf-8 -*-
"""
将README.md转换为PDF
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os


def create_pdf():
    """创建README PDF文档"""

    # 注册中文字体
    # 尝试使用系统字体
    try:
        pdfmetrics.registerFont(TTFont('SimHei', 'C:/Windows/Fonts/simhei.ttf'))
        pdfmetrics.registerFont(TTFont('SimSun', 'C:/Windows/Fonts/simsun.ttc'))
        chinese_font = 'SimHei'
    except:
        print("警告: 未找到中文字体，PDF中可能无法正确显示中文")
        chinese_font = 'Helvetica'

    # 创建PDF
    pdf_path = 'README.pdf'
    doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                           rightMargin=2*cm, leftMargin=2*cm,
                           topMargin=2*cm, bottomMargin=2*cm)

    # 创建样式
    styles = getSampleStyleSheet()

    # 自定义样式
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontName=chinese_font,
        fontSize=24,
        textColor=colors.HexColor('#2196F3'),
        spaceAfter=30,
        alignment=1  # 居中
    )

    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontName=chinese_font,
        fontSize=16,
        textColor=colors.HexColor('#2196F3'),
        spaceAfter=12
    )

    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontName=chinese_font,
        fontSize=14,
        textColor=colors.HexColor('#666666'),
        spaceAfter=10
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontName=chinese_font,
        fontSize=11,
        leading=18,
        spaceAfter=12
    )

    code_style = ParagraphStyle(
        'CustomCode',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=10,
        backColor=colors.HexColor('#F5F5F5'),
        leftIndent=20,
        spaceAfter=12
    )

    # 创建内容列表
    story = []

    # 标题
    story.append(Paragraph('Python学习教辅系统', title_style))
    story.append(Paragraph('使用说明文档', title_style))
    story.append(Spacer(1, 1*cm))

    # 项目简介
    story.append(Paragraph('一、项目简介', heading1_style))
    story.append(Paragraph('本项目是一个基于PyQt5的桌面版Python学习教辅系统，以<b>Python计算机二级考试大纲</b>为基础，为Python学习者提供系统化的学习工具。', body_style))
    story.append(Paragraph('• 版本: 1.0.0', body_style))
    story.append(Paragraph('• 开发语言: Python 3.x', body_style))
    story.append(Paragraph('• 技术栈: PyQt5 + SQLite + Matplotlib', body_style))
    story.append(Spacer(1, 0.5*cm))

    # 系统功能
    story.append(Paragraph('二、系统功能特点', heading1_style))

    features = [
        ('知识点学习模块', '系统化的Python知识点分类、详细讲解、代码示例、学习进度记录'),
        ('题库练习系统', '支持选择题、判断题、填空题、编程题，即时反馈、自动记录错题'),
        ('代码编辑器', '内置Python代码编辑器、实时执行、结果输出、文件保存'),
        ('学习进度跟踪', '总学习时长、完成统计、正确率计算、分类进度展示'),
        ('智能错题本', '自动收集错题、错误次数记录、掌握状态标记'),
        ('成绩统计分析', '准确率饼图、题型分布柱状图、练习记录、可视化展示')
    ]

    for title, desc in features:
        story.append(Paragraph(f'<b>{title}</b>', body_style))
        story.append(Paragraph(desc, body_style))

    story.append(Spacer(1, 0.5*cm))

    # 安装运行
    story.append(Paragraph('三、安装与运行', heading1_style))

    story.append(Paragraph('1. 安装依赖包', heading2_style))
    story.append(Paragraph('pip install -r requirements.txt', code_style))

    story.append(Paragraph('2. 初始化数据', heading2_style))
    story.append(Paragraph('python init_data.py', code_style))

    story.append(Paragraph('3. 启动系统', heading2_style))
    story.append(Paragraph('python main.py', code_style))

    story.append(Spacer(1, 0.5*cm))

    # 使用说明
    story.append(Paragraph('四、使用说明', heading1_style))

    story.append(Paragraph('登录信息', heading2_style))
    story.append(Paragraph('• 用户名: 1', body_style))
    story.append(Paragraph('• 密码: 1', body_style))

    story.append(Spacer(1, 0.5*cm))

    story.append(Paragraph('主要功能模块', heading2_style))
    modules = [
        '知识点学习: 选择分类和知识点，查看内容和代码示例，标记完成',
        '题库练习: 筛选题目，答题，查看解析，自动记录错题',
        '代码编辑器: 编写和运行Python代码，保存代码文件',
        '学习进度: 查看学习统计数据和进度情况',
        '错题本: 管理错题，查看详情，标记已掌握',
        '成绩统计: 查看准确率、题型分布等统计图表'
    ]

    for module in modules:
        story.append(Paragraph(f'• {module}', body_style))

    story.append(Spacer(1, 0.5*cm))

    # 技术亮点
    story.append(Paragraph('五、技术亮点', heading1_style))

    highlights = [
        'MVC架构: 清晰的模型-视图-控制器分离',
        '数据库设计: 规范的关系型数据库设计',
        '界面设计: PyQt5实现的现代化UI',
        '数据可视化: Matplotlib图表展示',
        '代码沙箱: 安全的代码执行环境',
        '模块化设计: 高内聚低耦合的代码结构'
    ]

    for highlight in highlights:
        story.append(Paragraph(f'• {highlight}', body_style))

    story.append(Spacer(1, 0.5*cm))

    # 项目统计
    story.append(Paragraph('六、项目统计', heading1_style))

    stats_data = [
        ['项目', '数量'],
        ['Python代码行数', '2500+ 行'],
        ['知识点数量', '18 个'],
        ['练习题目数量', '28 道'],
        ['功能模块数量', '6 个'],
        ['数据表数量', '7 个']
    ]

    stats_table = Table(stats_data, colWidths=[8*cm, 6*cm])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2196F3')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), chinese_font),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F5F5F5')),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTNAME', (0, 1), (-1, -1), chinese_font),
    ]))

    story.append(stats_table)
    story.append(Spacer(1, 0.5*cm))

    # 常见问题
    story.append(Paragraph('七、常见问题', heading1_style))

    qa_list = [
        ('Q: 启动时提示缺少模块？', 'A: 请安装所需依赖包：pip install PyQt5 matplotlib numpy pillow'),
        ('Q: 如何重置数据？', 'A: 删除database目录下的python_learning.db文件，重新运行init_data.py'),
        ('Q: 代码执行没反应？', 'A: 检查代码语法，注意执行超时时间为5秒'),
    ]

    for q, a in qa_list:
        story.append(Paragraph(f'<b>{q}</b>', body_style))
        story.append(Paragraph(a, body_style))

    story.append(Spacer(1, 1*cm))

    # 版权信息
    story.append(Paragraph('© 2025 Python学习教辅系统 | 基于Python计算机二级考试大纲', body_style))

    # 生成PDF
    doc.build(story)
    print(f"PDF文档已生成: {os.path.abspath(pdf_path)}")


if __name__ == '__main__':
    try:
        create_pdf()
        print("README.pdf 生成成功！")
    except Exception as e:
        print(f"生成PDF时出错: {e}")
        print("请确保已安装reportlab库: pip install reportlab")
