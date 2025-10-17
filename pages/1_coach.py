# -*- coding: utf-8 -*-
import streamlit as st
from ui_shared import ensure_page_config, render_header, render_footer

# 確保頁面配置統一
ensure_page_config()
# 渲染共用的頁首導航欄
render_header()

st.subheader("🧭 傳承導師：人機協作")
st.markdown("永傳的『傳承導師』扮演家庭與數位工具之間的橋樑。我們結合頂尖顧問的深度洞見，與數據科技的模擬能力，為您定制一份**人機協作、可落地執行**的傳承藍圖。")

st.markdown("---")

st.markdown("### 導師的三大核心價值")
st.markdown("""
1. **深度聆聽與價值引導：** - 區分家族的**情感需求**與**財務目標**，幫助您釐清最在乎的『家風』與『傳承價值』。
2. **複雜情境的數據可視化：**
   - 運用數位模組（如：稅務敏感度、資產地圖），將多種傳承方案的結果**量化、可視化**，讓決策更簡單。
3. **多方協調與落地執行：**
   - 作為您的**專屬專案經理**，協調會計師、律師、信託專家等，確保藍圖完美落地且合規。
""")

st.markdown("---")

st.markdown("### 我們的服務流程")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### **Step 1: 初診與盤點**")
    st.caption("透過線上初診與導師對話，快速建立家族資產與關係的基礎數據庫。")

with col2:
    st.markdown("#### **Step 2: 方案模擬與優化**")
    st.caption("導師運用數據工具進行情境假設，例如稅務壓縮、保單現金流，從數據中選出最佳解。")

with col3:
    st.markdown("#### **Step 3: 藍圖落實與複盤**")
    st.caption("協調專業夥伴，將方案文件化、合法化。並每年固定複盤，確保傳承藍圖跟上人生與法規變化。")

st.markdown("---")
st.markdown("#### 準備好開始您的傳承藍圖嗎？")
st.page_link("pages/4_contact.py", label="✉️ 預約專屬導師深度諮詢", icon=None, use_container_width=True)

# 供專業人士的入口
st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
st.page_link("pages/advisor_home.py", label="👉 我是專業顧問，想了解顧問夥伴計畫", use_container_width=False)

# 渲染共用的頁尾
render_footer()
