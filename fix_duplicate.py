with open('teaching_agent.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 找到重复的按钮定义并删除
lines = content.split('\n')
new_lines = []
i = 0

while i < len(lines):
    line = lines[i]
    
    # 检查是否是第一个 with col_btn3
    if 'with col_btn3:' in line and i < len(lines) - 3:
        # 添加第一个
        new_lines.append(line)
        new_lines.append(lines[i+1])  # generate_slides 行
        i += 2
        
        # 跳过空行
        while i < len(lines) and lines[i].strip() == '':
            new_lines.append(lines[i])
            i += 1
        
        # 检查是否有重复的 with col_btn3
        if i < len(lines) and 'with col_btn3:' in lines[i]:
            # 跳过重复的块
            i += 2  # 跳过 with col_btn3 和 generate_slides
            # 跳过后面的空行
            while i < len(lines) and lines[i].strip() == '':
                i += 1
        continue
    
    new_lines.append(line)
    i += 1

# 写回文件
with open('teaching_agent.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))

print('Fixed!')
