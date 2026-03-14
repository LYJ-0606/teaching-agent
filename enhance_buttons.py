with open('teaching_agent.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 优化教学设计下载按钮显示
old_design_btn = '''# 教学设计下载按钮（在spinner外部，持久显示）
if st.session_state.get("teaching_design_word"):
    st.download_button(
        label="📥 下载教学设计（Word格式）",
        data=st.session_state.teaching_design_word,
        file_name=f"{st.session_state.get('design_subject', '教学')}_{st.session_state.get('design_content', '设计')}_教学设计.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        use_container_width=True,
        key="download_design"
    )'''

new_design_btn = '''# 教学设计下载按钮（在spinner外部，持久显示）
if st.session_state.get("teaching_design_word"):
    st.markdown("---")
    st.markdown("### 📥 下载教学设计")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.download_button(
            label="📥 下载教学设计（Word格式）",
            data=st.session_state.teaching_design_word,
            file_name=f"{st.session_state.get('design_subject', '教学')}_{st.session_state.get('design_content', '设计')}_教学设计.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
            key="download_design",
            type="primary"
        )'''

content = content.replace(old_design_btn, new_design_btn)

# 2. 优化PPT大纲下载按钮显示
old_ppt_btn = '''# PPT大纲下载按钮（在spinner外部，持久显示）
if st.session_state.get("ppt_outline_word"):
    st.download_button(
        label="📥 下载PPT大纲（Word格式）",
        data=st.session_state.ppt_outline_word,
        file_name=f"{st.session_state.get('ppt_subject', '教学')}_{st.session_state.get('ppt_content', '大纲')}_PPT大纲.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        use_container_width=True,
        key="download_ppt"
    )'''

new_ppt_btn = '''# PPT大纲下载按钮（在spinner外部，持久显示）
if st.session_state.get("ppt_outline_word"):
    st.markdown("---")
    st.markdown("### 📥 下载PPT大纲")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.download_button(
            label="📥 下载PPT大纲（Word格式）",
            data=st.session_state.ppt_outline_word,
            file_name=f"{st.session_state.get('ppt_subject', '教学')}_{st.session_state.get('ppt_content', '大纲')}_PPT大纲.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
            key="download_ppt",
            type="primary"
        )'''

content = content.replace(old_ppt_btn, new_ppt_btn)

with open('teaching_agent.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Download buttons enhanced!')
