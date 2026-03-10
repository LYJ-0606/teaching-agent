# Banana Slides 集成指南

## 🎯 功能说明

Banana Slides 是一个在线 Markdown 演示工具，可以将 Markdown 格式的文本转换为精美的幻灯片演示。

集成后，你的应用将能够：
1. 将生成的 PPT 大纲转换为 Banana Slides 格式
2. 生成在线预览链接，直接在浏览器中查看演示
3. 下载 Slides 文件供离线使用

## 📝 手动集成步骤

### 步骤 1：修改导入部分

在文件开头的导入部分，添加：

```python
import urllib.parse
```

完整的导入部分应该是：
```python
import streamlit as st
from openai import OpenAI
import json
import urllib.parse  # 新增这一行
```

### 步骤 2：添加转换函数

在 `generate_ppt_outline` 函数之后，添加以下函数：

```python
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
```

### 步骤 3：修改按钮布局

找到这一行：
```python
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
```

改为：
```python
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
```

### 步骤 4：添加第三个按钮

在 `with col_btn2:` 代码块之后，添加：

```python
with col_btn3:
    generate_slides = st.button("🎬 生成Banana Slides", use_container_width=True, disabled=not st.session_state.get("ppt_outline"))
```

### 步骤 5：添加生成 Banana Slides 的代码

在 `# 生成PPT大纲` 代码块之后，`# 显示历史结果` 之前，添加：

```python
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
```

### 步骤 6：修改结果显示布局

找到这一行：
```python
col_result1, col_result2 = st.columns([1, 1])
```

改为：
```python
col_result1, col_result2, col_result3 = st.columns([1, 1, 1])
```

### 步骤 7：添加第三列显示

在 `with col_result2:` 代码块之后，添加：

```python
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
```

### 步骤 8：更新侧边栏说明

在侧边栏的使用说明中，将：
```python
7. 查看教学设计和PPT大纲
```

改为：
```python
7. 查看教学设计和PPT大纲
8. 生成Banana Slides在线演示
```

在特色功能中，添加：
```python
- 🎬 Banana Slides在线演示
```

在页脚中，将：
```
Powered by DeepSeek AI | 基于物理核心素养的教学设计
```

改为：
```
Powered by DeepSeek AI | 基于物理核心素养的教学设计 | 集成Banana Slides
```

## ✅ 完成

修改完成后：
1. 保存文件
2. 提交到 Git：
   ```bash
   git add teaching_agent.py
   git commit -m "添加 Banana Slides 集成功能"
   git push
   ```
3. 等待 Streamlit Cloud 自动重新部署（约2-3分钟）

## 🎬 使用方法

1. 生成教学设计
2. 生成 PPT 大纲
3. 点击"生成 Banana Slides"按钮
4. 点击生成的链接，在 Banana Slides 在线编辑器中查看演示
5. 可以下载 Markdown 文件供离线使用

## 💡 提示

- Banana Slides 链接包含完整的演示内容，可以直接分享给他人
- 在 Banana Slides 编辑器中可以进一步编辑和美化演示
- 支持导出为 PDF 或其他格式
