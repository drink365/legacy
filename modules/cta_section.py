# modules/cta_section.py — 全站 CTA（情感 × 行動）
import streamlit as st

def render_cta():
    st.markdown("---")
    st.markdown("### 🌿 現在，就是把心安下來的開始。")
    st.markdown(
        """
        我們用最簡單的流程，陪你把最重要的事先做好。  
        一次談清楚、確認重點、設計能執行的方案，家的方向就穩了。

        👉 **[預約 1 對 1 規劃](/4_contact)**　｜　📬 <a href="mailto:123@gracefo.com?subject=預約傳承規劃&body=您好，我希望預約諮詢，以下是我方便的時間：">寄信預約</a>
        """,
        unsafe_allow_html=True,
    )
