#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
自动为 teaching_agent.py 添加 Banana Slides 功能
"""

def add_banana_slides_feature():
    # 读取原文件
    with open('teaching_agent.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 在导入部分添加 urllib.parse
    if 'import urllib.parse' not in content:
        content = content.replace('import json', 'import json\nimport urllib.parse')
    
    # 2. 在 generate_ppt_outline 函数后添加新函数
    new_function = '''
def convert_to_banana_slides(client, ppt_outline, subject, content):
    """将PPT大纲转换为Banana Slides格式的Markdown"""
    
    system_prompt = """你是一位专业的Banana Slides格式转换专家。
Banana Slides使用特殊的Markdown格式来创建演示文稿。

格式规则：
1. 使用 --- 分隔每一页幻灯片
2. 每页第一行使用 # 标题 作为幻灯片标题
3. 内容使用标准Markdown格式（列表、加粗、斜体等）

请将PPT大纲转换为完整的Banana Slides格式Markdown。"""

    user_prompt = f"""请将以下PPT大纲转换为Banana Slides格式的Markdown：

**课程**: {subject} - {content}

**PPT大纲**:
{ppt_outline}

要求：
1. 每页幻灯片用 --- 分隔
2. 保持内容完整和逻辑清晰
3. 第一页作为封面，包含课程标题"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        stream=True,
        temperature=0.7
    )
    
    return response
'''
    
    # 找到 generate_ppt_outline 函数结束的位置
    import re
    pattern = r'(def generate_ppt_outline.*?return response\n)'
    match = re.search(pattern, content, re.DOTALL)
    
    if match and 'def convert_to_banana_slides' not in content:
        insert_pos = match.end()
        content = content[:insert_pos] + new_function + content[insert_pos:]
    
    # 3. 修改按钮行
    content = content.replace(
        'col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])',
        'col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])'
    )
    
    # 4. 添加第三个按钮
    button_code = '''
with col_btn3:
    generate_slides = st.button("🎬 生成Banana Slides", use_container_width=True, disabled=not st.session_state.get("ppt_outline"))
'''
    
    if 'generate_slides' not in content:
        content = content.replace(
            'with col_btn2:\n    generate_ppt = st.button("📊 生成PPT大纲", use_container_width=True, disabled=not st.session_state.get("teaching_design"))',
            'with col_btn2:\n    generate_ppt = st.button("📊 生成PPT大纲", use_container_width=True, disabled=not st.session_state.get("teaching_design"))\n' + button_code
        )
    
    # 5. 添加生成 Banana Slides 的代码
    slides_generation_code = '''
# 生成Banana Slides
if generate_slides:
    if not api_key:
        st.error("❌ 请先在侧边栏输入 DeepSeek API Key")
    else:
        with st.spinner("🤔 正在生成Banana Slides格式..."):
            try:
                client = st.session_state.client
                ppt_outline = st.session_state.ppt_outline
                subject = st.session_state.subject
                content = st.session_state.content
                response = convert_to_banana_slides(client, ppt_outline, subject, content)
                
                st.markdown("---")
                st.markdown("## 🎬 Banana Slides演示文稿")
                slides_container = st.empty()
                full_slides = ""
                
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        full_slides += chunk.choices[0].delta.content
                        slides_container.markdown(full_slides)
                
                st.session_state.banana_slides = full_slides
                
                # 生成Banana Slides在线预览链接
                encoded_content = urllib.parse.quote(full_slides)
                banana_url = f"https://bananaslides.online/?md={encoded_content}"
                
                st.success("✅ Banana Slides生成完成！")
                st.markdown("### 🔗 在线预览")
                st.markdown(f"[🎬 点击在Banana Slides中打开演示]({banana_url})")
                st.info("💡 提示：点击上方链接可以在Banana Slides在线编辑器中查看和编辑您的演示文稿")
                
            except Exception as e:
                st.error(f"❌ 生成失败: {str(e)}")

'''
    
    if '# 生成Banana Slides' not in content:
        # 在生成PPT大纲代码后添加
        content = content.replace(
            '# 显示历史结果\nst.markdown("---")',
            slides_generation_code + '\n# 显示历史结果\nst.markdown("---")'
        )
    
    # 6. 修改结果显示部分
    content = content.replace(
        'col_result1, col_result2 = st.columns([1, 1])',
        'col_result1, col_result2, col_result3 = st.columns([1, 1, 1])'
    )
    
    # 7. 添加第三列显示
    result_col3_code = '''
with col_result3:
    if st.session_state.get("banana_slides"):
        with st.expander("🎬 查看Banana Slides", expanded=False):
            st.markdown(st.session_state.banana_slides)
            st.download_button(
                "💾 下载Slides文件",
                st.session_state.banana_slides,
                file_name=f"{st.session_state.get('subject', '教学')}_Slides.md",
                mime="text/markdown",
                use_container_width=True
            )
            # 再次显示在线链接
            encoded_content = urllib.parse.quote(st.session_state.banana_slides)
            banana_url = f"https://bananaslides.online/?md={encoded_content}"
            st.markdown(f"[🎬 在Banana Slides中打开]({banana_url})")
'''
    
    if 'with col_result3:' not in content:
        # 在 col_result2 后添加
        pattern = r'(with col_result2:.*?use_container_width=True\s*\))'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            insert_pos = match.end()
            content = content[:insert_pos] + '\n' + result_col3_code + content[insert_pos:]
    
    # 8. 更新侧边栏说明
    content = content.replace(
        '7. 查看教学设计和PPT大纲',
        '7. 查看教学设计和PPT大纲\n    8. 生成Banana Slides在线演示'
    )
    
    content = content.replace(
        '- 🎨 美观的界面设计',
        '- 🎬 Banana Slides在线演示\n    - 🎨 美观的界面设计'
    )
    
    content = content.replace(
        'Powered by DeepSeek AI | 基于物理核心素养的教学设计',
        'Powered by DeepSeek AI | 基于物理核心素养的教学设计 | 集成Banana Slides'
    )
    
    # 写入文件
    with open('teaching_agent.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Banana Slides 功能已成功添加到 teaching_agent.py！")
    print("📝 主要更新：")
    print("  1. 添加了 convert_to_banana_slides 函数")
    print("  2. 添加了'生成Banana Slides'按钮")
    print("  3. 添加了 Banana Slides 生成和预览功能")
    print("  4. 添加了在线预览链接（bananaslides.online）")
    print("  5. 更新了界面布局和说明")

if __name__ == '__main__':
    try:
        add_banana_slides_feature()
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
