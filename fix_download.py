import re

with open('teaching_agent.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 修复教学设计下载按钮：移到 spinner 外部
old_design = '''                st.session_state.teaching_design = full_design
                st.session_state.subject = subject
                st.session_state.content = content
                st.session_state.method = method
                st.success("✅ 教学设计生成完成！")
                
                # 生成Word文档
                word_file = markdown_to_word(full_design, f"{subject} - {content} 教学设计")
                
                # 下载按钮
                st.download_button(
                    label="📥 下载教学设计（Word格式）",
                    data=word_file,
                    file_name=f"{subject}_{content}_教学设计.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"❌ 生成失败: {str(e)}")'''

new_design = '''                st.session_state.teaching_design = full_design
                st.session_state.subject = subject
                st.session_state.content = content
                st.session_state.method = method
                
                # 生成Word文档并保存到session_state
                word_file = markdown_to_word(full_design, f"{subject} - {content} 教学设计")
                st.session_state.teaching_design_word = word_file.read()
                st.session_state.design_subject = subject
                st.session_state.design_content = content
                
                st.success("✅ 教学设计生成完成！")
                
            except Exception as e:
                st.error(f"❌ 生成失败: {str(e)}")

# 教学设计下载按钮（在spinner外部，持久显示）
if st.session_state.get("teaching_design_word"):
    st.download_button(
        label="📥 下载教学设计（Word格式）",
        data=st.session_state.teaching_design_word,
        file_name=f"{st.session_state.get('design_subject', '教学')}_{st.session_state.get('design_content', '设计')}_教学设计.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        use_container_width=True,
        key="download_design"
    )'''

content = content.replace(old_design, new_design)

if old_design in open('teaching_agent.py', 'r', encoding='utf-8').read():
    print('ERROR: old string still found')
else:
    print('Design section updated')

# 修复PPT大纲下载按钮：移到 spinner 外部
old_ppt = '''                st.session_state.ppt_outline = full_ppt
                
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
                
                st.info("💡 提示：下载大纲后，可以点击上方'制作PPT演示'按钮，访问 Banana Slides 在线制作精美的演示文稿")
                
            except Exception as e:
                st.error(f"❌ 生成失败: {str(e)}")'''

new_ppt = '''                st.session_state.ppt_outline = full_ppt
                
                # 生成Word文档并保存到session_state
                word_file = markdown_to_word(full_ppt, f"{subject} - {content} PPT大纲")
                st.session_state.ppt_outline_word = word_file.read()
                st.session_state.ppt_subject = subject
                st.session_state.ppt_content = content
                
                st.success("✅ PPT大纲生成完成！")
                st.info("💡 提示：下载大纲后，可以点击上方'制作PPT演示'按钮，访问 Banana Slides 在线制作精美的演示文稿")
                
            except Exception as e:
                st.error(f"❌ 生成失败: {str(e)}")

# PPT大纲下载按钮（在spinner外部，持久显示）
if st.session_state.get("ppt_outline_word"):
    st.download_button(
        label="📥 下载PPT大纲（Word格式）",
        data=st.session_state.ppt_outline_word,
        file_name=f"{st.session_state.get('ppt_subject', '教学')}_{st.session_state.get('ppt_content', '大纲')}_PPT大纲.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        use_container_width=True,
        key="download_ppt"
    )'''

content = content.replace(old_ppt, new_ppt)

# 删除旧的 st.success PPT（避免重复）
content = content.replace(
    'st.session_state.ppt_outline = full_ppt\n                \n                # 生成Word文档并保存',
    'st.session_state.ppt_outline = full_ppt\n                \n                # 生成Word文档并保存'
)

with open('teaching_agent.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('All fixed!')
