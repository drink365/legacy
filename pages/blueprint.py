# pages/blueprint.py — 幸福傳承藍圖（保留原內容＋統一頁首頁尾＋字寬淡底按鈕）
# -*- coding: utf-8 -*-
import streamlit as st
from ui_shared import ensure_page_config, render_header, render_footer

# ✅ 改成 page_title（原本的 title 會造成 TypeError）
ensure_page_config(page_title="幸福傳承藍圖｜永傳家族辦公室")

# 頁面頂部導覽列
render_header()

# ----------------- 頁面主體 -----------------
st.subheader("🧬 幸福傳承藍圖：從策略到落地的一站式路徑")

st.markdown("""
<div style="font-size:16px; color:#444; line-height:1.8; margin-bottom:20px;">
我們將複雜的家族傳承工作，轉化為<strong>「看得懂、做得到、能長久」</strong>的四個階段。
透過專家深度訪談與數位工具的精準模擬，確保您的傳承方案不僅合法合規，更能凝聚家族共識、永續成長。
</div>
""", unsafe_allow_html=True)

# ----------------- 藍圖四階段 -----------------
st.markdown("### 藍圖建立的四個核心階段")
col1, col2, col3, col4 = st.columns(4)
steps = [
    ("🧭 盤點與定向", "#004c4c", "家族核心價值、資產地圖、潛在風險初診；釐清傳承的起點與終點目標。"),
    ("⚙️ 數據與情境模擬", "#cc6600", "運用數位戰情室工具，模擬不同方案在股權、稅負、現金流上的長期影響。"),
    ("📝 藍圖方案與落地", "#1a4d99", "撰寫可執行的家族憲章、信託架構、保單策略，並協助法律文件簽訂與實施。"),
    ("🔄 持續複盤與調整", "#4d4d4d", "家族重大變動或法規更新時，提供年度複盤與調整建議，確保藍圖常青。"),
]
for col, (title, color, detail) in zip([col1, col2, col3, col4], steps):
    with col:
        st.markdown(f"""
        <div style="background:#fff;border-top:5px solid {color};
            padding:15px;border-radius:12px;box-shadow:0 4px 12px rgba(0,0,0,.08);
            margin-bottom:15px;height:100%;">
            <div style="font-weight:800;font-size:20px;color:{color};margin-bottom:8px;">{title}</div>
            <div style="color:#555;font-size:15px;line-height:1.6;">{detail}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ----------------- 成果範例 -----------------
st.markdown("### 藍圖交付成果範例")
c1, c2 = st.columns(2)
with c1:
    st.markdown("""
    **🗺️ 家族資產/股權地圖（視覺化）**  
    清晰呈現家族成員、資產類別、法律架構與控制權，一目瞭然。  
    **📑 家族憲章/治理框架草案**  
    定義決策機制、財富教育方針與爭議解決程序，確保家風永續。
    """)
with c2:
    st.markdown("""
    **🛡️ 傳承風險報告與對策**  
    針對潛在稅務、流動性與法規風險，提出多套備選方案與執行路徑。  
    **📊 年度複盤與模擬報告**  
    追蹤方案執行進度，並根據外部環境變化提供調整建議。
    """)

st.markdown("---")
st.markdown("### 準備好建立您的永續藍圖了嗎？")
# ✅ 保持字寬淡底：移除 icon / use_container_width
st.page_link("pages/4_contact.py", label="📞 預約深度諮詢，開始啟動藍圖")

st.caption("我們將安排資深顧問，提供一對一的初期評估。")

# 統一頁尾
render_footer()
