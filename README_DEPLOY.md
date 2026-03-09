# 教学设计智能体 - 部署指南

## 🚀 部署到 Streamlit Cloud（推荐）

### 步骤 1：准备 GitHub 仓库

1. 在 GitHub 上创建新仓库
2. 将项目文件上传到仓库：
   - `teaching_agent.py`
   - `requirements.txt`
   - `README.md`
   - `.streamlit/config.toml`

**注意：不要上传 `.streamlit/secrets.toml` 文件！**

### 步骤 2：部署到 Streamlit Cloud

1. 访问 [share.streamlit.io](https://share.streamlit.io)
2. 使用 GitHub 账号登录
3. 点击 "New app"
4. 选择你的仓库、分支和主文件（`teaching_agent.py`）
5. 点击 "Deploy"

### 步骤 3：配置 API Key（可选）

如果你想预配置 API Key：

1. 在 Streamlit Cloud 应用设置中找到 "Secrets"
2. 添加以下内容：
```toml
DEEPSEEK_API_KEY = "your-api-key-here"
```

### 完成！

部署完成后，你会得到一个公开网址，例如：
- `https://your-username-teaching-agent.streamlit.app`

这个网址可以分享给任何人使用！

---

## 🌐 其他部署方案

### 方案 2：Hugging Face Spaces（免费）

1. 访问 [huggingface.co/spaces](https://huggingface.co/spaces)
2. 创建新 Space，选择 Streamlit
3. 上传代码文件
4. 获得公开网址：`https://huggingface.co/spaces/your-username/app-name`

### 方案 3：Railway（免费额度）

1. 访问 [railway.app](https://railway.app)
2. 连接 GitHub 仓库
3. 自动部署
4. 获得公开网址

### 方案 4：自己的服务器

如果你有自己的服务器（阿里云、腾讯云等）：

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用（对外开放）
streamlit run teaching_agent.py --server.address 0.0.0.0 --server.port 8501
```

然后配置防火墙开放 8501 端口，通过 `http://你的服务器IP:8501` 访问。

---

## 📝 注意事项

1. **API Key 安全**：不要在代码中硬编码 API Key
2. **用户输入**：让每个用户自己输入 API Key（当前方案）
3. **成本控制**：如果预配置 API Key，注意使用量和成本
4. **访问限制**：Streamlit Cloud 免费版有一定的资源限制

---

## 🔗 推荐使用 Streamlit Cloud

- ✅ 完全免费
- ✅ 部署简单（3分钟完成）
- ✅ 自动 HTTPS
- ✅ 自动更新（推送到 GitHub 后自动重新部署）
- ✅ 适合教育用途
