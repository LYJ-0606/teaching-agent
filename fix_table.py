import re

with open('teaching_agent.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 新的 markdown_to_word 函数（支持表格）
new_func = '''def markdown_to_word(markdown_text, title):
    """将Markdown文本转换为Word文档，支持表格"""
    doc = Document()
    
    # 设置标题
    heading = doc.add_heading(title, 0)
    heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # 先把文本按行分割，检测表格块
    lines = markdown_text.split("\\n")
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if not line:
            i += 1
            continue
        
        # 检测表格（以 | 开头）
        if line.startswith("|") and "|" in line[1:]:
            # 收集整个表格
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            
            # 过滤掉分隔行（如 |---|---|）
            data_lines = [l for l in table_lines if not re.match(r"^\\|[-:\\s|]+\\|$", l)]
            
            if len(data_lines) >= 1:
                # 解析表头
                headers = [cell.strip() for cell in data_lines[0].split("|") if cell.strip()]
                n_cols = len(headers)
                n_rows = len(data_lines)
                
                # 创建 Word 表格
                table = doc.add_table(rows=n_rows, cols=n_cols)
                table.style = "Table Grid"
                
                # 填入数据
                for row_idx, row_line in enumerate(data_lines):
                    cells = [cell.strip() for cell in row_line.split("|") if cell.strip()]
                    for col_idx, cell_text in enumerate(cells[:n_cols]):
                        cell = table.cell(row_idx, col_idx)
                        cell.text = cell_text
                        if row_idx == 0:
                            # 表头加粗
                            for para in cell.paragraphs:
                                for run in para.runs:
                                    run.bold = True
                
                doc.add_paragraph()  # 表格后空行
            continue
        
        # 处理标题
        if line.startswith("# "):
            doc.add_heading(line[2:], level=1)
        elif line.startswith("## "):
            doc.add_heading(line[3:], level=2)
        elif line.startswith("### "):
            doc.add_heading(line[4:], level=3)
        elif line.startswith("#### "):
            doc.add_heading(line[5:], level=4)
        # 处理列表
        elif line.startswith("- ") or line.startswith("* "):
            doc.add_paragraph(line[2:], style="List Bullet")
        elif re.match(r"^\\d+\\. ", line):
            doc.add_paragraph(re.sub(r"^\\d+\\. ", "", line), style="List Number")
        # 处理加粗
        elif "**" in line:
            p = doc.add_paragraph()
            parts = line.split("**")
            for idx, part in enumerate(parts):
                if idx % 2 == 0:
                    p.add_run(part)
                else:
                    p.add_run(part).bold = True
        # 普通段落
        else:
            doc.add_paragraph(line)
        
        i += 1
    
    # 保存到内存
    file_stream = io.BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)
    return file_stream
'''

# 替换旧函数
pattern = r'def markdown_to_word\(markdown_text, title\):.*?return file_stream\n'
match = re.search(pattern, content, re.DOTALL)
if match:
    content = content[:match.start()] + new_func + content[match.end():]
    print('Function replaced successfully!')
else:
    print('Pattern not found!')

with open('teaching_agent.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done!')
