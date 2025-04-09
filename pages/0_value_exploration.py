# --- pages/0_value_exploration.py ---

import streamlit as st
from modules.cta_section import render_cta

# 頁面設定
st.set_page_config(
    page_title="價值觀探索｜《影響力》傳承策略平台",
    page_icon="🧭",
    layout="centered"
)

st.markdown("""
<div style='text-align: center;'>
    <h2>🧭 價值觀探索</h2>
    <p style='font-size: 18px;'>人生最重要的，不只是資產的分配，而是價值的延續</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 步驟一：選擇價值觀詞彙
st.markdown("### 🔍 步驟一：請從以下詞彙中選出您最在意的 3 個價值")

values_list = [
    "誠信與正直", "自由與選擇", "責任與承擔", "關係與情感", "學習與成長",
    "財務穩定", "安全與保障", "影響力", "創新與突破", "傳統與延續"
]

selected_values = st.multiselect("選擇您的價值觀：", values_list, max_selections=3)

# 步驟二：情境選擇題
if selected_values:
    st.success("✅ 您選擇的價值觀：" + "、".join(selected_values))
    st.markdown("---")
    st.markdown("### 🧠 步驟二：哪一種情境，最符合您的風格？")

    scenario = st.radio("若今天要規劃家族資產，您會比較傾向哪種方式？", [
        "先和家人談談價值觀和共識，再決定策略",
        "先找顧問做稅務與保單安排，減少風險",
        "自己先思考清楚，把重要的想法寫下來再找人協助"
    ])

    # 步驟三：文字輸入補充
    st.markdown("### 📝 步驟三：還有哪些想法或重要的信念，您希望被保留下來？")
    note = st.text_area("寫下您的信念、初衷、故事或想法（可選填）")

    # 顯示個人摘要
    if st.button("📄 產出我的價值摘要"):
        st.markdown("---")
        st.markdown("### 📋 個人價值觀摘要")
        st.write(f"您在這次探索中，選擇了：**{'、'.join(selected_values)}**")
        st.write(f"您的情境偏好是：**{scenario}**")
        if note:
            st.write("您想被保留的信念內容：")
            st.info(note)

        st.markdown("---")
        st.markdown("🎯 接下來，我們會依據這些線索，引導您設計屬於自己的策略組合與保障結構。")

        render_cta()

# 頁尾資訊
st.markdown("---")
st.markdown("""
<div style='text-align: center; font-size: 14px; color: gray;'>
《影響力》傳承策略平台｜永傳家族辦公室 <a href=\"https://gracefo.com\" target=\"_blank\">https://gracefo.com</a><br>
聯絡信箱：<a href=\"mailto:123@gracefo.com\">123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
