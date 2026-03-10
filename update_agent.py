#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 读取原文件
with open('teaching_agent.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到需要修改的位置并进行修改
new_lines = []
i = 0

while i < len(lines):
    line = lines[i]
    
    # 1. 在 import json 后添加 import urllib.parse
    if line.strip() == 'import json':
        new_lines.append(line)
        new_lines.append('import urllib.parse\n')
        i += 1
        continue
    
    # 2. 在 generate_ppt_outline 函数后添加新函数
    if i < len(lines) - 1 and 'def generate_ppt_outline' in line:
        # 找到这个函数的结束位置
        new_lines.append(line)
        i += 1
        indent_count = 0
        while i < len(lines):
            new_lines.append(lines[i])
            if 'return response' in lines[i] and indent_count == 0:
                indent_count += 1
                i += 1
                # 添加新函数
                new_lines.append('\n')
                new_lines.append('def convert_to_banana_slides(client, ppt_outline, subject, content):\n')
                new_lines.append('    """将PPT大纲转换为Banana Slides格式的Markdown"""\n')
                new_lines.append('    \n')
                new_lines.append('    system_prompt = """你是一位专业的Banana Slides格式转换专家。\n')
                new_lines.append('Banana Slides使用特殊的Markdown格式来创建演示文稿。\n')
                new_lines.append('\n')
                new_lines.append('格式规则：\n')
                new_lines.append('1. 使用 --- 分隔每一页幻灯片\n')
                new_lines.append('2. 每页第一行使用 # 标题 作为幻灯片标题\n')
                new_lines.append('3. 内容使用标准Markdown格式（列表、加粗、斜体等）\n')
                new_lines.append('\n')
                new_lines.append('请将PPT大纲转换为完整的Banana Slides格式Markdown。"""\n')
                new_lines.append('\n')
                new_lines.append('    user_prompt = f"""请将以下PPT大纲转换为Banana Slides格式的Markdown：\n')
                new_lines.append('\n')
                new_lines.append('**课程**: {subject} - {content}\n')
                new_lines.append('\n')
                new_lines.append('**PPT大纲**:\n')
                new_lines.append('{ppt_outline}\n')
                new_lines.append('\n')
                new_lines.append('要求：\n')
                new_lines.append('1. 每页幻灯片用 --- 分隔\n')
                new_lines.append('2. 保持内容完整和逻辑清晰\n')
                new_lines.append('3. 第一页作为封面，包含课程标题"""\n')
                new_lines.append('\n')
                new_lines.append('    response = client.chat.completions.create(\n')
                new_lines.append('        model="deepseek-chat",\n')
                new_lines.append('        messages=[\n')
                new_lines.append('            {"role": "system", "content": system_prompt},\n')
                new_lines.append('            {"role": "user", "content": user_prompt}\n')
                new_lines.append('        ],\n')
                new_lines.append('        stream=True,\n')
                new_lines.append('        temperature=0.7\n')
                new_lines.append('    )\n')
                new_lines.append('    \n')
                new_lines.append('    return response\n')
                break
            i += 1
        continue
    
    # 3. 修改按钮列布局
    if 'col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])' in line:
        new_lines.append('col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])\n')
        i += 1
        continue
    
    # 4. 在 col_btn2 后添加 col_btn3
    if 'with col_btn2:' in line and i < len(lines) - 2:
        new_lines.append(line)
        new_lines.append(lines[i+1])  # generate_ppt 按钮
        new_lines.append('\n')
        new_lines.append('with col_btn3:\n')
        new_lines.append('    generate_slides = st.button("🎬 生成Banana Slides", use_container_width=True, disabled=not st.session_state.get("ppt_outline"))\n')
        i += 2
        continue
    
    # 5. 在"显示历史结果"前添加生成Banana Slides的代码
    if '# 显示历史结果' in line:
        # 添加生成Banana Slides代码
        new_lines.append('# 生成Banana Slides\n')
        new_lines.append('if generate_slides:\n')
        new_lines.append('    if not api_key:\n')
        new_lines.append('        st.error("❌ 请先在侧边栏输入 DeepSeek API Key")\n')
        new_lines.append('    else:\n')
        new_lines.append('        with st.spinner("🤔 正在生成Banana Slides格式..."):\n')
        new_lines.append('            try:\n')
        new_lines.append('                client = st.session_state.client\n')
        new_lines.append('                ppt_outline = st.session_state.ppt_outline\n')
        new_lines.append('                subject = st.session_state.subject\n')
        new_lines.append('                content = st.session_state.content\n')
        new_lines.append('                response = convert_to_banana_slides(client, ppt_outline, subject, content)\n')
        new_lines.append('                \n')
        new_lines.append('                st.markdown("---")\n')
        new_lines.append('                st.markdown("## 🎬 Banana Slides演示文稿")\n')
        new_lines.append('                slides_container = st.empty()\n')
        new_lines.append('                full_slides = ""\n')
        new_lines.append('                \n')
        new_lines.append('                for chunk in response:\n')
        new_lines.append('                    if chunk.choices[0].delta.content:\n')
        new_lines.append('                        full_slides += chunk.choices[0].delta.content\n')
        new_lines.append('                        slides_container.markdown(full_slides)\n')
        new_lines.append('                \n')
        new_lines.append('                st.session_state.banana_slides = full_slides\n')
        new_lines.append('                \n')
        new_lines.append('                # 生成Banana Slides在线预览链接\n')
        new_lines.append('                encoded_content = urllib.parse.quote(full_slides)\n')
        new_lines.append('                banana_url = f"https://bananaslides.online/?md={encoded_content}"\n')
        new_lines.append('                \n')
        new_lines.append('                st.success("✅ Banana Slides生成完成！")\n')
        new_lines.append('                st.markdown("### 🔗 在线预览")\n')
        new_lines.append('                st.markdown(f"[🎬 点击在Banana Slides中打开演示]({banana_url})")\n')
        new_lines.append('                st.info("💡 提示：点击上方链接可以在Banana Slides在线编辑器中查看和编辑您的演示文稿")\n')
        new_lines.append('                \n')
        new_lines.append('            except Exception as e:\n')
        new_lines.append('                st.error(f"❌ 生成失败: {str(e)}")\n')
        new_lines.append('\n')
        new_lines.append(line)
        i += 1
        continue
    
    # 6. 修改结果显示列布局
    if 'col_result1, col_result2 = st.columns([1, 1])' in line:
        new_lines.append('col_result1, col_result2, col_result3 = st.columns([1, 1, 1])\n')
        i += 1
        continue
    
    # 7. 在 col_result2 后添加 col_result3
    if i < len(lines) - 1 and 'with col_result2:' in line:
        # 找到 col_result2 块的结束
        new_lines.append(line)
        i += 1
        indent_level = 0
        while i < len(lines):
            if lines[i].startswith('with col_result') or lines[i].startswith('# 页脚'):
                # 添加 col_result3
                new_lines.append('\n')
                new_lines.append('with col_result3:\n')
                new_lines.append('    if st.session_state.get("banana_slides"):\n')
                new_lines.append('        with st.expander("🎬 查看Banana Slides", expanded=False):\n')
                new_lines.append('            st.markdown(st.session_state.banana_slides)\n')
                new_lines.append('            st.download_button(\n')
                new_lines.append('                "💾 下载Slides文件",\n')
                new_lines.append('                st.session_state.banana_slides,\n')
                new_lines.append('                file_name=f"{st.session_state.get(\'subject\', \'教学\')}_Slides.md",\n')
                new_lines.append('                mime="text/markdown",\n')
                new_lines.append('                use_container_width=True\n')
                new_lines.append('            )\n')
                new_lines.append('            # 再次显示在线链接\n')
                new_lines.append('            encoded_content = urllib.parse.quote(st.session_state.banana_slides)\n')
                new_lines.append('            banana_url = f"https://bananaslides.online/?md={encoded_content}"\n')
                new_lines.append('            st.markdown(f"[🎬 在Banana Slides中打开]({banana_url})")\n')
                new_lines.append('\n')
                new_lines.append(lines[i])
                i += 1
                break
            new_lines.append(lines[i])
            i += 1
        continue
    
    # 8. 更新使用说明
    if '7. 查看教学设计和PPT大纲' in line:
        new_lines.append(line)
        new_lines.append('    8. 生成Banana Slides在线演示\n')
        i += 1
        continue
    
    # 9. 更新特色功能
    if '- 🎨 美观的界面设计' in line:
        new_lines.append('    - 🎬 Banana Slides在线演示\n')
        new_lines.append(line)
        i += 1
        continue
    
    # 10. 更新页脚
    if 'Powered by DeepSeek AI | 基于物理核心素养的教学设计' in line:
        new_lines.append(line.replace(
            'Powered by DeepSeek AI | 基于物理核心素养的教学设计',
            'Powered by DeepSeek AI | 基于物理核心素养的教学设计 | 集成Banana Slides'
        ))
        i += 1
        continue
    
    new_lines.append(line)
    i += 1

# 写入新文件
with open('teaching_agent.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('✅ Banana Slides功能已成功添加！')
print('📝 主要更新：')
print('  1. 添加了 urllib.parse 导入')
print('  2. 添加了 convert_to_banana_slides 函数')
print('  3. 添加了第三个生成按钮')
print('  4. 添加了 Banana Slides 生成逻辑')
print('  5. 添加了在线预览链接')
print('  6. 更新了界面布局和说明')
