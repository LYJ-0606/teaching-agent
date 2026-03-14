with open('teaching_agent.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_instructions = -1
end_instructions = -1
start_features = -1
end_features = -1

for i, line in enumerate(lines):
    if '### ' in line and '\u4f7f\u7528\u8bf4\u660e' in line:
        start_instructions = i
    if start_instructions > 0 and end_instructions < 0 and i > start_instructions and line.strip() == '""")':
        end_instructions = i
    if '### ' in line and '\u7279\u8272\u529f\u80fd' in line:
        start_features = i
    if start_features > 0 and end_features < 0 and i > start_features and line.strip() == '""")':
        end_features = i

new_instructions = [
    '    st.markdown("### \U0001F4D6 \u4f7f\u7528\u8bf4\u660e")\n',
    '    st.markdown("""\n',
    '    1. \u8f93\u5165 API Key\n',
    '    2. \u586b\u5199\u5b8c\u6574\u7684\u6559\u5b66\u4fe1\u606f\u4ee5\u53ca\u8bbe\u8ba1\u8981\u7d20\n',
    '    3. \u70b9\u51fb\u751f\u6210\u6559\u5b66\u8bbe\u8ba1\u6309\u9215\n',
    '    4. \u4e0b\u8f7d\u540e\u70b9\u51fb\u751f\u6210PPT\u5927\u7eb2\u6309\u9215\n',
    '    5. \u4e0b\u8f7d\u540e\u70b9\u51fb\u5236\u4f5cPPT\u6f14\u793a\u8fdb\u5165Banana Slides\u8fdb\u884c\u751f\u6210\n',
    '    """)\n',
]

new_features = [
    '    st.markdown("### \U0001F4A1 \u7279\u8272\u529f\u80fd")\n',
    '    st.markdown("""\n',
    '    - \U0001F3AF \u57fa\u4e8e\u7269\u7406\u6838\u5fc3\u7d20\u517b\u8bbe\u8ba1\u76ee\u6807\n',
    '    - \U0001F4DD \u81ea\u52a8\u751f\u6210\u677f\u4e66\u8bbe\u8ba1\n',
    '    - \U0001F465 \u6839\u636e\u5b66\u751f\u60c5\u51b5\u56e0\u6750\u65bd\u6559\n',
    '    - \u23F1\uFE0F \u7cbe\u786e\u7684\u65f6\u95f4\u5206\u914d\n',
    '    - \U0001F4C4 \u5bfc\u51faWord\u6587\u6863\n',
    '    - \U0001F3A8 \u7f8e\u89c2\u7684\u754c\u9762\u8bbe\u8ba1\n',
    '    """)\n',
]

lines = lines[:start_features] + new_features + lines[end_features+1:]
lines = lines[:start_instructions] + new_instructions + lines[end_instructions+1:]

with open('teaching_agent.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('Done')
