with open('teaching_agent.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 修复重复导入并添加新导入
content = content.replace(
    'import streamlit as st\nfrom openai import OpenAI\nimport json\nimport urllib.parse\nimport urllib.parse',
    'import streamlit as st\nfrom openai import OpenAI\nimport json\nimport urllib.parse\nfrom docx import Document\nfrom docx.shared import Pt, RGBColor\nfrom docx.enum.text import WD_ALIGN_PARAGRAPH\nimport io'
)

# 2. 添加 Word 转换函数（在 generate_ppt_outline 函数后）
word_function = '''

def markdown_to_word(markdown_text, title):
    """将Markdown文本转换为Word文档"""
    doc = Document()
    
    # 设置标题
    heading = doc.add_heading(title, 0)
    heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # 解析Markdown并添加到文档
    lines = markdown_text.split('\\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # 处理标题
        if line.startswith('# '):
            doc.add_heading(line[2:], level=1)
        elif line.startswith('## '):
            doc.add_heading(line[3:], level=2)
        elif line.startswith('### '):
            doc.add_heading(line[4:], level=3)
        elif line.startswith('#### '):
            doc.add_heading(line[5:], level=4)
        # 处理列表
        elif line.startswith('- ') or line.startswith('* '):
            doc.add_paragraph(line[2:], style='List Bullet')
        elif line.startswith('1. ') or line.startswith('2. ') or line.startswith('3. '):
            doc.add_paragraph(line[3:], style='List Number')
        # 处理加粗
        elif '**' in line:
            p = doc.add_paragraph()
            parts = line.split('**')
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    p.add_run(part)
                else:
                    p.add_run(part).bold = True
        # 普通段落
        else:
            doc.add_paragraph(line)
    
    # 保存到内存
    file_stream = io.BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)
    return file_stream
'''

# 找到 convert_to_banana_slides 函数并删除它
import re
pattern = r'def convert_to_banana_slides.*?return response\n'
content = re.sub(pattern, '', content, flags=re.DOTALL)

# 在 generate_ppt_outline 后添加 word 函数
pattern = r'(def generate_ppt_outline.*?return response\n)'
match = re.search(pattern, content, re.DOTALL)
if match:
    insert_pos = match.end()
    content = content[:insert_pos] + word_function + content[insert_pos:]

# 3. 更新使用说明
content = content.replace(
    '''st.markdown("""
    1. 输入 API Key
    2. 填写完整的教学信息
    3. 选择教学方法和时长
    4. 输入教学重难点
    5. 输入教学目标和其他要求
    6. 点击生成按钮
    7. 查看教学设计和PPT大纲
    8. 生成Banana Slides在线演示
    """)''',
    '''st.markdown("""
    1. 输入 API Key
    2. 填写完整的教学信息及设计要素
    3. 点击生成教学设计
    4. 点击生成PPT大纲
    5. 使用Banana Slides生成PPT
    """)'''
)

# 4. 更新特色功能
content = content.replace(
    '- 🎬 Banana Slides在线演示',
    '- 📄 导出Word文档'
)

# 5. 修改第三个按钮为链接
content = content.replace(
    'with col_btn3:\n    generate_slides = st.button("🎬 生成Banana Slides", use_container_width=True, disabled=not st.session_state.get("ppt_outline"), key="btn_slides")',
    '''with col_btn3:
    st.markdown("""
    <div style='text-align: center; margin-top: 8px;'>
        <a href='https://bananaslides.online/' target='_blank' style='display: inline-block; padding: 0.5rem 2rem; background: linear-gradient(120deg, #F18F01, #FF6B35); color: white; text-decoration: none; border-radius: 8px; font-weight: 600;'>
            🎬 制作PPT演示
        </a>
    </div>
    """, unsafe_allow_html=True)'''
)

# 6. 删除生成 Banana Slides 的代码块
pattern = r'# 生成Banana Slides.*?st\.error\(f"❌ 生成失败: \{str\(e\)\}"\)\n\n'
content = re.sub(pattern, '', content, flags=re.DOTALL)

# 7. 在教学设计生成完成后添加 Word 下载按钮
pattern = r'(st\.session_state\.teaching_design = full_design\n                st\.session_state\.subject = subject\n                st\.session_state\.content = content\n                st\.session_state\.method = method\n                st\.success\("✅ 教学设计生成完成！"\))'
replacement = r'''\1
                
                # 生成Word文档
                word_file = markdown_to_word(full_design, f"{subject} - {content} 教学设计")
                
                # 下载按钮
                st.download_button(
                    label="📥 下载教学设计（Word格式）",
                    data=word_file,
                    file_name=f"{subject}_{content}_教学设计.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )'''
content = re.sub(pattern, replacement, content)

# 8. 在PPT大纲生成完成后添加 Word 下载按钮
pattern = r'(st\.session_state\.ppt_outline = full_ppt\n                st\.success\("✅ PPT大纲生成完成！"\))'
replacement = r'''\1
                
                # 生成Word文档
                word_file = markdown_to_word(full_ppt, f"{subject} - {content} PPT大纲")
                
                # 下载按钮
                st.download_button(
                    label="📥 下载PPT大纲（Word格式）",
                    data=word_file,
                    file_name=f"{subject}_{content}_PPT大纲.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
                
                st.info("💡 提示：下载大纲后，可以点击上方'制作PPT演示'按钮，访问 Banana Slides 在线制作精美的演示文稿")'''
content = re.sub(pattern, replacement, content)

# 9. 删除第三列结果显示（Banana Slides）
content = content.replace(
    'col_result1, col_result2, col_result3 = st.columns([1, 1, 1])',
    'col_result1, col_result2 = st.columns([1, 1])'
)

# 删除 col_result3 块
pattern = r'\nwith col_result3:.*?st\.markdown\(f"\[🎬 在Banana Slides中打开\]\(\{banana_url\}\)"\)\n'
content = re.sub(pattern, '\n', content, flags=re.DOTALL)

with open('teaching_agent.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated successfully!')
