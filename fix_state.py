with open('teaching_agent.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到 client = st.session_state.client 这一行（在生成教学设计部分）
for i, line in enumerate(lines):
    if 'client = st.session_state.client' in line and i > 430:
        # 在下一行插入状态设置
        insert_pos = i + 1
        new_lines = [
            '                \n',
            '                # 立即设置标志，启用后续按钮\n',
            '                st.session_state.teaching_design = "generating"\n',
            '                st.session_state.subject = subject\n',
            '                st.session_state.content = content\n',
            '                st.session_state.method = method\n',
            '                \n'
        ]
        
        lines = lines[:insert_pos] + new_lines + lines[insert_pos:]
        break

# 写回文件
with open('teaching_agent.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('Fixed')
