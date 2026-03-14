import re

with open('teaching_agent.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 修复使用说明（用正则替换整块）
pattern1 = r'st\.markdown\("### .. ..\u8bf4\u660e"\)\n    st\.markdown\(""".*?"""\)'
replacement1 = '''st.markdown("### \U0001F4D6 \u4f7f\u7528\u8bf4\u660e")\n    st.markdown("""\n    1. \u8f93\u5165 API Key\n    2. \u586b\u5199\u5b8c\u6574\u7684\u6559\u5b66\u4fe1\u606f\u4ee5\u53ca\u8bbe\u8ba1\u8981\u7d20\n    3. \u70b9\u51fb\u751f\u6210\u6559\u5b66\u8bbe\u8ba1\u6309\u9215\n    4. \u4e0b\u8f7d\u540e\u70b9\u51fb\u751f\u6210PPT\u5927\u7eb2\u6309\u9215\n    5. \u4e0b\u8f7d\u540e\u70b9\u51fb\u5236\u4f5cPPT\u6f14\u793a\u8fdb\u5165Banana Slides\u8fdb\u884c\u751f\u6210\n    """)'''
content = re.sub(pattern1, replacement1, content, flags=re.DOTALL)

# 2. 修复特色功能（用正则替换整块）
pattern2 = r'st\.markdown\("### .. \u7279\u8272\u529f\u80fd"\)\n    st\.markdown\(""".*?"""\)'
replacement2 = '''st.markdown("### \U0001F4A1 \u7279\u8272\u529f\u80fd")\n    st.markdown("""\n    - \U0001F3AF \u57fa\u4e8e\u7269\u7406\u6838\u5fc3\u7d20\u517b\u8bbe\u8ba1\u76ee\u6807\n    - \U0001F4DD \u81ea\u52a8\u751f\u6210\u677f\u4e66\u8bbe\u8ba1\n    - \U0001F465 \u6839\u636e\u5b66\u751f\u60c5\u51b5\u56e0\u6750\u65bd\u6559\n    - \u23F1\uFE0F \u7cbe\u786e\u7684\u65f6\u95f4\u5206\u914d\n    - \U0001F4C4 \u5bfc\u51faWord\u6587\u6863\n    - \U0001F3A8 \u7f8e\u89c2\u7684\u754c\u9762\u8bbe\u8ba1\n    """)'''
content = re.sub(pattern2, replacement2, content, flags=re.DOTALL)

# 3. 修改教学设计系统提示，要求教学流程使用表格
content = content.replace(
    '3. \u8be6\u7ec6\u7684\u6559\u5b66\u73af\u8282\uff08\u5305\u62ec\u7cbe\u786e\u7684\u65f6\u95f4\u5206\u914d\u3001\u6559\u5e08\u6d3b\u52a8\u3001\u5b66\u751f\u6d3b\u52a8\uff09',
    '3. \u6559\u5b66\u73af\u8282\u5fc5\u987b\u4f7f\u7528Markdown\u8868\u683c\u5f62\u5f0f\u5448\u73b0\uff0c\u8868\u683c\u5217\u5305\u542b\uff1a\u6559\u5b66\u73af\u8282\u3001\u65f6\u95f4\u5206\u914d\u3001\u6559\u5e08\u6d3b\u52a8\u3001\u5b66\u751f\u6d3b\u52a8\u3001\u8bbe\u8ba1\u610f\u56fe'
)

old_ending = '\u8bf7\u4ee5\u7ed3\u6784\u5316\u7684\u65b9\u5f0f\u8f93\u51fa\uff0c\u4f7f\u7528 Markdown \u683c\u5f0f\u3002"""'
new_ending = '\u8bf7\u4ee5\u7ed3\u6784\u5316\u7684\u65b9\u5f0f\u8f93\u51fa\uff0c\u4f7f\u7528 Markdown \u683c\u5f0f\uff0c\u6559\u5b66\u6d41\u7a0b\u90e8\u5206\u5fc5\u987b\u4f7f\u7528Markdown\u8868\u683c\u3002"""'
content = content.replace(old_ending, new_ending, 1)

with open('teaching_agent.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done!')
