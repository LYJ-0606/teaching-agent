with open('teaching_agent.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找行号
start_inst = None
end_inst = None
start_feat = None
end_feat = None

for i, line in enumerate(lines):
    if '使用说明' in line and 'markdown' in line.lower():
        start_inst = i
    if start_inst and end_inst is None and i > start_inst and line.strip() == '""")':
        end_inst = i
    if '特色功能' in line and 'markdown' in line.lower():
        start_feat = i
    if start_feat and end_feat is None and i > start_feat and line.strip() == '""")':
        end_feat = i

print(f'Instructions: lines {start_inst+1} to {end_inst+1}')
print(f'Features: lines {start_feat+1} to {end_feat+1}')

# 新的使用说明
new_inst = [
    '    st.markdown("### 📖 使用说明")\n',
    '    st.markdown("""\n',
    '    1. 输入 API Key\n',
    '    2. 填写完整的教学信息和设计要素\n',
    '    3. 点击生成教学设计按钮\n',
    '    4. 下载教学设计\n',
    '    5. 点击生成PPT大纲按钮\n',
    '    6. 下载PPT大纲\n',
    '    7. 点击制作PPT演示前往Banana Slides\n',
    '    """)\n',
]

# 新的特色功能
new_feat = [
    '    st.markdown("### 💡 特色功能")\n',
    '    st.markdown("""\n',
    '    - 🎯 基于物理核心素养设计目标\n',
    '    - 📝 自动生成板书设计\n',
    '    - 👥 根据学生情况因材施教\n',
    '    - ⏱️ 精确的时间分配\n',
    '    - 📄 导出Word文档\n',
    '    - 🎨 美观的界面设计\n',
    '    """)\n',
]

# 先替换后面的（特色功能），避免行号偏移
lines = lines[:start_feat] + new_feat + lines[end_feat+1:]
# 再替换前面的（使用说明）
lines = lines[:start_inst] + new_inst + lines[end_inst+1:]

with open('teaching_agent.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('Sidebar fixed!')
