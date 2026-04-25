import streamlit as st
import json
import random

# 页面配置
st.set_page_config(page_title="赛博起卦", page_icon="☯️", layout="centered")

# 加载数据库
@st.cache_data # 缓存数据，提高访问速度
def load_data():
    with open('64G.json', 'r', encoding='utf-8') as f:
        return json.load(f)

ching_db = load_data()

st.title("☯️ 赛博起卦系统")
st.markdown("---")

# 初始化状态
if 'sequence' not in st.session_state:
    st.session_state.sequence = ""

# 定义绘制爻的函数（用于实时显示）
def draw_single_yao(bit, index):
    label = f"第 {index+1} 爻"
    if bit == "1":
        # 阳爻：红色长线
        st.markdown(f"**{label}：阳 (面)**")
        st.markdown("<div style='background-color:#FF4B4B; height:15px; width:100%; border-radius:5px;'></div>", unsafe_allow_html=True)
    else:
        # 阴爻：中间断开
        st.markdown(f"**{label}：阴 (背)**")
        st.write(f" <div style='display:flex; justify-content:space-between;'> <div style='background-color:#31333F; height:15px; width:45%; border-radius:5px;'></div> <div style='background-color:#31333F; height:15px; width:45%; border-radius:5px;'></div> </div> ", unsafe_allow_html=True)
    st.write("")

# --- 交互区域 ---

# 如果还没掷满 6 爻
if len(st.session_state.sequence) < 6:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("诚心掷钱", type="primary", use_container_width=True):
            res = str(random.randint(0, 1))
            st.session_state.sequence += res
            st.rerun()
            
    with col2:
        if st.button("放弃本次", use_container_width=True):
            st.session_state.sequence = ""
            st.rerun()

    # 实时显示已投出的爻（从下往上显示，符合易经传统）
    st.markdown("### 当前卦象：")
    for i, bit in enumerate(reversed(st.session_state.sequence)):
        actual_index = len(st.session_state.sequence) - 1 - i
        draw_single_yao(bit, actual_index)

# 如果 6 爻已满
else:
    final_seq = st.session_state.sequence
    info = ching_db.get(final_seq, {"name": "未知卦", "symbol": "❓"})
    
    st.balloons() # 撒花庆祝
    st.success(f"## 终卦：{info['symbol']} {info['name']}")
    
    # 显示完整的六爻图
    st.markdown("### 卦象复盘 (由上至下)：")
    for i in range(5, -1, -1):
        draw_single_yao(final_seq[i], i)
    
    st.markdown(f"**二进制序列：** `{final_seq}`")
    
    if st.button("再次起卦", type="secondary", use_container_width=True):
        st.session_state.sequence = ""
        st.rerun()

st.markdown("---")
st.caption("基于 Python + Streamlit 部署 | 庚金逻辑 · 己土承载")
