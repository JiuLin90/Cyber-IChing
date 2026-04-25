import streamlit as st
import json
import random

# 设置页面标题
st.set_page_config(page_title="赛博起卦", page_icon="☯️")

# 加载数据库
with open('64G.json', 'r', encoding='utf-8') as f:
    ching_db = json.load(f)

st.title("☯️ 赛博起卦系统")

# 初始化 session 状态，模拟“起卦”和“再次起卦”的循环逻辑
if 'sequence' not in st.session_state:
    st.session_state.sequence = ""

# 界面交互
if len(st.session_state.sequence) < 6:
    st.write(f"当前已掷出 {len(st.session_state.sequence)} 爻")
    if st.button("诚心起卦 / 掷钱", type="primary"):
        res = str(random.randint(0, 1))
        st.session_state.sequence += res
        st.rerun()
else:
    # 结果展示阶段
    final_seq = st.session_state.sequence
    info = ching_db.get(final_seq, {"name": "未知卦", "symbol": "❓"})
    
    st.success(f"得卦：{info['symbol']} {info['name']}")
    
    # 简单的卦画显示
    for i in range(5, -1, -1):
        if final_seq[i] == "1":
            st.markdown(" <p style='color:red; background-color:red; width:200px;'>&nbsp;</p> ", unsafe_allow_html=True)
        else:
            st.markdown(" <p style='color:black;'><span style='background-color:black; width:80px; display:inline-block;'>&nbsp;</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style='background-color:black; width:80px; display:inline-block;'>&nbsp;</span></p> ", unsafe_allow_html=True)

    # 再次起卦功能
    if st.button("再次起卦"):
        st.session_state.sequence = ""
        st.rerun()
