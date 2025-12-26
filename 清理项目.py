# -*- coding: utf-8 -*-
"""
项目清理脚本
自动删除多余的开发脚本和文档，保留核心文件
"""
import os
import shutil

def clean_project():
    """清理项目多余文件"""

    print("=" * 60)
    print("Python学习教辅系统 - 项目清理工具")
    print("=" * 60)
    print()

    # 项目根目录
    project_root = os.path.dirname(os.path.abspath(__file__))

    # 要删除的scripts文件（保留init_data.py）
    scripts_to_delete = [
        'add_exam_test_cases.py',
        'add_more_questions.py',
        'add_runoob_knowledge.py',
        'capture_preview.py',
        'check_duplicates.py',
        'clean_duplicates.py',
        'final_enhancement.py',
        'fix_exam_db_lock.py',
        'fix_practice_crash.py',
        'fix_progress_widget.py',
        'generate_pdf.py',
        'init_exam_data.py',
        'integrate_exam_feature.py',
        'optimize_profile_widget.py',
        'supplement_knowledge.py',
        'upgrade_database_for_exam.py',
    ]

    # 要删除的根目录文件
    root_files_to_delete = [
        '快速启动指南.md',
        '使用说明.txt',
    ]

    deleted_count = 0

    # 1. 清理scripts目录
    print("【1/4】清理 scripts/ 目录中的辅助脚本...")
    scripts_dir = os.path.join(project_root, 'scripts')
    for script in scripts_to_delete:
        script_path = os.path.join(scripts_dir, script)
        if os.path.exists(script_path):
            try:
                os.remove(script_path)
                print(f"  ✓ 已删除: scripts/{script}")
                deleted_count += 1
            except Exception as e:
                print(f"  ✗ 删除失败: scripts/{script} - {e}")
        else:
            print(f"  - 未找到: scripts/{script}")

    # 2. 清理根目录冗余文档
    print()
    print("【2/4】清理根目录中的冗余文档...")
    for file in root_files_to_delete:
        file_path = os.path.join(project_root, file)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"  ✓ 已删除: {file}")
                deleted_count += 1
            except Exception as e:
                print(f"  ✗ 删除失败: {file} - {e}")
        else:
            print(f"  - 未找到: {file}")

    # 3. 清理__pycache__目录（如果有）
    print()
    print("【3/4】清理Python缓存文件...")
    pycache_count = 0
    for root, dirs, files in os.walk(project_root):
        if '__pycache__' in dirs:
            pycache_dir = os.path.join(root, '__pycache__')
            try:
                shutil.rmtree(pycache_dir)
                relative_path = os.path.relpath(pycache_dir, project_root)
                print(f"  ✓ 已删除: {relative_path}")
                pycache_count += 1
            except Exception as e:
                print(f"  ✗ 删除失败: {pycache_dir} - {e}")

    if pycache_count == 0:
        print("  - 未找到缓存文件")

    # 4. 清理.pyc文件
    print()
    print("【4/4】清理.pyc编译文件...")
    pyc_count = 0
    for root, dirs, files in os.walk(project_root):
        for file in files:
            if file.endswith('.pyc'):
                pyc_path = os.path.join(root, file)
                try:
                    os.remove(pyc_path)
                    relative_path = os.path.relpath(pyc_path, project_root)
                    print(f"  ✓ 已删除: {relative_path}")
                    pyc_count += 1
                except Exception as e:
                    print(f"  ✗ 删除失败: {pyc_path} - {e}")

    if pyc_count == 0:
        print("  - 未找到.pyc文件")

    # 统计信息
    print()
    print("=" * 60)
    print("清理完成！")
    print("=" * 60)
    print(f"总共删除文件数: {deleted_count + pycache_count + pyc_count}")
    print(f"  - scripts脚本: {deleted_count - len(root_files_to_delete)}个")
    print(f"  - 冗余文档: {len(root_files_to_delete)}个")
    print(f"  - __pycache__目录: {pycache_count}个")
    print(f"  - .pyc文件: {pyc_count}个")
    print()
    print("保留的核心文件:")
    print("  ✓ scripts/init_data.py（数据库初始化）")
    print("  ✓ clean_duplicates_and_reconfigure.py（考试配置）")
    print("  ✓ 启动系统.bat（启动脚本）")
    print("  ✓ README.md（项目说明）")
    print("  ✓ 都队_系统文档.md（报告文档）")
    print("  ✓ 都队_工程报告.md（报告文档）")
    print("  ✓ 截图指导.md（截图指南）")
    print("  ✓ 所有核心代码文件（main.py, config.py, models/, ui/, utils/）")
    print()
    print("项目现在更简洁专业了！🎉")
    print()

if __name__ == '__main__':
    # 确认提示
    print()
    print("⚠️  即将清理项目中的多余文件")
    print()
    print("清理内容:")
    print("  1. scripts/目录中的辅助脚本（保留init_data.py）")
    print("  2. 根目录的冗余文档（保留README.md和报告）")
    print("  3. Python缓存文件（__pycache__和.pyc）")
    print()

    confirm = input("确认清理？(输入 yes 继续): ")

    if confirm.lower() in ['yes', 'y', '是']:
        print()
        clean_project()
    else:
        print()
        print("已取消清理操作。")
        print()
