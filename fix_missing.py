with open('teaching_agent.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 在第418行后插入缺失的代码
insert_lines = [
    '\n',
    '# 生成教学设计\n',
    'if generate_design:\n',
    '    if not api_key:\n',
    '        st.error("❌ 请先在侧边栏输入 DeepSeek API Key")\n'
]

new_lines = lines[:418] + insert_lines + lines[418:]

with open('teaching_agent.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('Fixed missing code')
