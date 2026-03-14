import re

with open('teaching_agent.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 1. 修改系统提示，要求教学环节使用表格
for i, line in enumerate(lines):
    if '详细的教学环节（包括精确的时间分配、教师活动、学生活动）' in line:
        lines[i] = lines[i].replace(
            '详细的教学环节（包括精确的时间分配、教师活动、学生活动）',
            '教学过程必须使用Markdown表格呈现，表格包含列：教学环节 | 时间 | 教师活动 | 学生活动 | 设计意图'
        )
        print(f'Updated system prompt at line {i+1}')
    if '请以结构化的方式输出，使用 Markdown 格式。' in line and i < 200:
        lines[i] = lines[i].replace(
            '请以结构化的方式输出，使用 Markdown 格式。',
            '请以结构化的方式输出，使用 Markdown 格式，教学过程部分必须使用Markdown表格。'
        )
        print(f'Updated format instruction at line {i+1}')

# 2. 更新 markdown_to_word 函数以支持表格
for i, line in enumerate(lines):
    if '# 处理列表' in line and i > 200:
        # 在处理列表之前插入表格处理逻辑
        table_code = [
            '        # 处理Markdown表格\n',
            '        elif line.startswith("|") and "|" in line[1:]:\n',
            '            # 收集表格行\n',
            '            pass  # 表格在后处理中处理\n',
            '\n',
        ]
        lines = lines[:i] + table_code + lines[i:]
        print(f'Added table handling at line {i+1}')
        break

with open('teaching_agent.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('Done step 1')
