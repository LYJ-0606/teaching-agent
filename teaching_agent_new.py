import streamlit as st
from openai import OpenAI
import json
import urllib.parse

# 页面配置
st.set_page_config(
    page_title="教学设计智能体",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    :root {
        --primary-color: #2E86AB;
        --secondary-color: #A23B72;
        --accent-color: #F18F01;
    }
    
    .main-title {
        font-family: 'Segoe UI', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(120deg, #2E86AB, #A23B72, #F18F01);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1.5rem 0;
        margin-bottom: 0.5rem;
    }
    
    .sub-title {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    .info-card {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        border-left: 4px solid #2E86AB;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .stButton>button {
        transition: all 0.3s ease;
        border-radius: 8px;
        font-weight: 600;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #2E86AB;
        box-shadow: 0 0 0 2px rgba(46, 134, 171, 0.1);
    }
    
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 8px;
        padding: 1rem;
        animation: slideIn 0.3s ease;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #2E86AB, transparent);
    }
    
    .stSelectbox label, .stTextInput label, .stTextArea label, .stSlider label {
        font-weight: 600;
        color: #2E86AB;
    }
</style>
""", unsafe_allow_html=True)

# 教学方法定义
TEACHING_METHODS = {
    "讲授法": "教师系统讲解知识，学生听讲、记录和理解",
    "翻转课堂": "学生课前自学，课堂进行讨论、实践和答疑",
    "项目式学习": "以真实项目为驱动，学生通过完成项目掌握知识",
    "探究式学习": "引导学生提出问题、探索和发现知识",
    "合作学习": "学生分组协作，共同完成学习任务",
    "案例教学": "通过分析真实案例，培养学生解决问题的能力",
    "游戏化学习": "将游戏元素融入教学，提高学习兴趣和参与度"
}
