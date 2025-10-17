# -*- coding: utf-8 -*-
import streamlit as st
from ui_shared import ensure_page_config, render_header, render_footer, TAGLINE

ensure_page_config()
render_header()

st.subheader("👑 關於永傳")
st.markdown("""
在永傳，我們相信「家業、家產、家風」缺一不可。  
我們做的，不只是文件與試算，而是**讓家庭的價值與關係，能與資產同頻長久運行**。  
我們以 **專家洞見 × 智能科技 × 幸福傳承** 為核心，把複雜的傳承議題，整理成好理解、可落地的行動。
""")

st.markdown("### 您會得到什麼")
st.markdown("""
- **全貌可視**：把資產、股權、家庭關係、風險熱點整理成一張「傳承地圖」。  
- **選項清楚**：用數據與情境模擬，把不同方案的影響（稅負、現金流、控制權）攤開講清楚。  
- **專家把關**：由**美國會計師、國際律師、財稅顧問**與資產配置專家共同審閱，確保可執行、可監管。  
- **持續陪伴**：重大變動（家族、法規、市場）發生時，我們協助調整藍圖，維持方向一致。
""")

st.markdown("### 我們的三大支柱：家業・家產・家風")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("#### **家業成長**")
    st.caption("治理框架 × 股權與現金流設計；兼顧控制權與營運效率，推動企業長青。")
with col2:
    st.markdown("#### **家產守護**")
    st.caption("風險防護 × 稅務與流動性規劃；在合規前提下守住資產安全與彈性。")
with col3:
    st.markdown("#### **家風永續**")
    st.caption("家族憲章 × 下一代財商與責任；讓家庭文化與資產同頻共振、薪火相傳。")

st.markdown("### 誰在陪您一起走（Founder）")
st.markdown("""
**黃榮如（Grace Huang）** 永傳家族辦公室創辦人。擁有美國會計師（AICPA）資格、台灣會計師（CPA）與國際認證理財規劃顧問（CFP）。  
曾任職於國際四大會計師事務所與外商私人銀行，具備 20 多年實務經驗，擅長於跨境、高資產家庭的資產傳承與稅務規劃。
""")

render_footer()
