with open('teaching_agent.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 为每个按钮添加唯一的 key
content = content.replace(
    'generate_design = st.button("🎨 生成教学设计", use_container_width=True, type="primary")',
    'generate_design = st.button("🎨 生成教学设计", use_container_width=True, type="primary", key="btn_design")'
)

content = content.replace(
    'generate_ppt = st.button("📊 生成PPT大纲", use_container_width=True, disabled=not st.session_state.get("teaching_design"))',
    'generate_ppt = st.button("📊 生成PPT大纲", use_container_width=True, disabled=not st.session_state.get("teaching_design"), key="btn_ppt")'
)

content = content.replace(
    'generate_slides = st.button("🎬 生成Banana Slides", use_container_width=True, disabled=not st.session_state.get("ppt_outline"))',
    'generate_slides = st.button("🎬 生成Banana Slides", use_container_width=True, disabled=not st.session_state.get("ppt_outline"), key="btn_slides")'
)

with open('teaching_agent.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Added unique keys to buttons')
