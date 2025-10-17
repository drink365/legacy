# pages/dataroom.py — 數位戰情室（保留原內容＋統一頁首頁尾＋字寬淡底按鈕）
# -*- coding: utf-8 -*-
import streamlit as st
from ui_shared import ensure_page_config, render_header, render_footer

# ✅ 改成 page_title（原本的 title 會造成 TypeError）
ensure_page_config(page_title="數位戰情室｜永傳家族辦公室")

# 渲染統一頁首
render_header()

# ----------------- 頁面主體 -----------------
st.subheader("📈 數位戰情室：數據驅動的傳承決策平台")
st.markdown("""
<div style="font-size:16px; color:#444; line-height:1.8; margin-bottom:20px;">
「數位戰情室」是為專業顧問與家族設計的 <strong>高階模擬與分析工具</strong>。
它將散落在各處的資產、法規與家族關係數據整合為即時儀表板，
讓複雜的傳承決策變得清晰、可驗證。
</div>
""", unsafe_allow_html=True)

# ----------------- 核心功能與價值 -----------------
st.markdown("### 核心功能與價值")
col_func_1, col_func_2 = st.columns(2)

features = [
    ("📊 **情境模擬引擎**", "即時試算不同傳承方案 (如信託、贈與、遺囑) 對未來 5–20 年稅負、現金流和控制權的敏感度影響。"),
    ("🗺️ **家族資產儀表板**", "將所有資產 (海內外房產、股權、保險) 集中視覺化，動態追蹤資產淨值與結構風險。"),
    ("🛡️ **法規風險警報**", "整合主要國家或地區 (如美國、台灣) 的稅法變動，提前預警並提供合規建議。"),
    ("🤝 **多方協作空間**", "允許家族律師、會計師、顧問在統一且安全的環境下，共同審閱與編輯傳承藍圖。"),
]

for i, (title, detail) in enumerate(features):
    target_col = col_func_1 if i % 2 == 0 else col_func_2
    with target_col:
        st.markdown(f"""
        <div style="
            background:#f0f8ff;
            padding:15px;
            border-radius:12px;
            border-left:4px solid #1a4d99;
            margin-bottom:15px;
        ">
            <div style="font-size:18px; color:#1a4d99; margin-bottom:5px;">{title}</div>
            <div style="color:#555; font-size:14px; line-height:1.6;">{detail}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ----------------- 目標用戶與安全機制 -----------------
st.markdown("### 適合對象與安全機制")
col_user, col_safe = st.columns(2)

with col_user:
    st.markdown("#### 誰會使用戰情室？")
    st.markdown("""
    - **高資產客戶**：需要定期審視家族整體資產與傳承進度。  
    - **外部顧問夥伴**：如律師、會計師，利用工具提升服務精準度。  
    - **家族辦公室專業人士**：作為內部品控與決策支持的工具。
    """)

with col_safe:
    st.markdown("#### 平台安全與隱私")
    st.markdown("""
    - **高隱私設計**：嚴格的權限管理與最小化資料原則。  
    - **端到端加密**：確保敏感資產數據在傳輸和儲存過程中的安全。  
    - **獨立伺服器**：確保數據主權與合規性。
    """)

# ----------------- 行動呼籲 (B2B/顧問) -----------------
st.markdown("---")
st.markdown("### 成為數據驅動的頂尖顧問")
col_cta, col_space = st.columns([2, 1])

with col_cta:
    # ✅ 保持字寬淡底：移除 icon / use_container_width
    st.page_link("pages/advisor_home.py", label="🤝 探索顧問夥伴合作方案")
    st.caption("了解如何運用數位工具，將您的專業能力與服務效率提升至新的維度。")

# 統一頁尾
render_footer()
